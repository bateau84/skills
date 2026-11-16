import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_runner import build_probe_command, load_runner
from eval_probe import effective_agent_matches, isolated_skill_catalog
from eval_profile import SkillsProfile
from run_evals import parser, run_probe

ROOT = Path(__file__).resolve().parents[2]


class ProbeBoundaryTests(unittest.TestCase):
    def test_probe_manifest_retains_failure_observation_and_private_permissions(self):
        runner = load_runner(Path(os.environ.get("SKILLS_EVAL_RUNNER_ROOT", str(ROOT.parent / "opencode-eval-runner"))))
        options = parser().parse_args([])
        options.target_image_proof = {"test": "storage-only injected probe; not runtime evidence"}
        case = SkillsProfile(ROOT, runner, options, "candidate", {}).discover_cases()[0]
        for failed in (True, False):
            with tempfile.TemporaryDirectory() as temp:
                options.artifact_dir = Path(temp) / "proof"
                def probe(root, runner, options, case, record):
                    record("baseline", {"storage_test_input": True})
                    if failed:
                        raise ValueError("bounded test probe failure")
                    return {"storage_test_result": True}
                if failed:
                    with self.assertRaisesRegex(ValueError, "retained probe evidence"):
                        run_probe(ROOT, runner, options, case, probe)
                else:
                    self.assertEqual(run_probe(ROOT, runner, options, case, probe)["summary"]["status"], "verified")
                manifest = options.artifact_dir / "run.json"
                self.assertEqual(manifest.stat().st_mode & 0o777, 0o600)
                import json
                durable = json.loads(manifest.read_text())
                self.assertEqual(durable["summary"]["status"], "failed" if failed else "verified")
                self.assertEqual(durable["summary"]["observations"]["baseline"], {"storage_test_input": True})

    def test_stock_browser_deny_extension_is_not_a_permission_mismatch_or_allow_exception(self):
        deny = {"action": "*", "resource": "*", "effect": "deny"}
        expected = {"system": "isolated system", "permissions": [deny]}
        actual = {"system": "isolated system", "permissions": [
            {"action": "*", "resource": "*", "effect": "allow"}, deny, deny,
            {"action": "browser", "resource": "*", "effect": "deny"}]}
        self.assertTrue(effective_agent_matches(actual, expected, ["opencode.browser"]))
        self.assertFalse(effective_agent_matches(actual, expected, []))
        actual["permissions"][-1]["effect"] = "allow"
        self.assertFalse(effective_agent_matches(actual, expected, ["opencode.browser"]))
        actual["permissions"][-1] = {"action": "read", "resource": "*", "effect": "deny"}
        self.assertFalse(effective_agent_matches(actual, expected, ["opencode.browser"]))

    def test_opencode_226_stock_browser_skill_deny_preserves_isolation(self):
        # The installed 2.2.6 runtime appends both denies, after the configured
        # agent rule. This is a real probe observation, not a new allow rule.
        deny = {"action": "*", "resource": "*", "effect": "deny"}
        browser_deny = {"action": "browser", "resource": "*", "effect": "deny"}
        skill_deny = {"action": "skill", "resource": "browser", "effect": "deny"}
        expected = {"system": "isolated system", "permissions": [deny]}
        prefix = [
            {"action": "*", "resource": "*", "effect": "allow"},
            {"action": "read", "resource": "*.env", "effect": "ask"},
            deny, deny,
        ]
        actual = {"system": "isolated system",
                  "permissions": prefix + [browser_deny, skill_deny]}
        self.assertTrue(effective_agent_matches(actual, expected, ["opencode.browser"]))
        self.assertFalse(effective_agent_matches(actual, expected, []))

        for rules in (
            prefix + [browser_deny, {**skill_deny, "effect": "allow"}],
            prefix + [browser_deny, {**skill_deny, "resource": "*"}],
            prefix + [{**browser_deny, "effect": "allow"}, skill_deny],
            prefix + [skill_deny],
            prefix + [browser_deny, {"action": "read", "resource": "*", "effect": "allow"}, skill_deny],
        ):
            with self.subTest(rules=rules):
                self.assertFalse(effective_agent_matches(
                    {"system": "isolated system", "permissions": rules},
                    expected, ["opencode.browser"],
                ))

        candidate = {"system": "candidate system", "permissions": [
            deny,
            {"action": "skill", "resource": "agent-run-audit", "effect": "allow"},
            {"action": "read", "resource": ".opencode/skills/agent-run-audit/SKILL.md", "effect": "allow"},
        ]}
        candidate_actual = {"system": "candidate system", "permissions": (
            prefix + candidate["permissions"] + [browser_deny, skill_deny]
        )}
        self.assertTrue(effective_agent_matches(candidate_actual, candidate, ["opencode.browser"]))

    def test_isolated_skill_catalog_excludes_browser_even_when_skill_hidden(self):
        clean = {
            "skills": [], "plugins": ["opencode.tool.skill", "eval-runtime-observer"],
            "workspace_evals": [], "loom_seed_exists": False,
        }
        self.assertTrue(isolated_skill_catalog(clean, []))
        self.assertFalse(isolated_skill_catalog(clean, ["agent-run-audit"]))
        self.assertTrue(isolated_skill_catalog(
            {**clean, "skills": ["agent-run-audit"]}, ["agent-run-audit"],
        ))
        for contaminated in (
            {**clean, "plugins": clean["plugins"] + ["opencode.browser"]},
            {**clean, "skills": ["browser"]},
            {**clean, "skills": ["agent-run-audit", "browser"]},
            {**clean, "plugins": clean["plugins"] + ["arbitrary.plugin"]},
            {**clean, "workspace_evals": ["/workspace/hidden/evals"]},
            {**clean, "loom_seed_exists": True},
        ):
            with self.subTest(contaminated=contaminated):
                self.assertFalse(isolated_skill_catalog(contaminated, []))

    def test_real_runner_probe_builder_excludes_all_credential_mounts_and_environment(self):
        runner = load_runner(Path(os.environ.get("SKILLS_EVAL_RUNNER_ROOT", str(ROOT.parent / "opencode-eval-runner"))))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            workspace = root / "workspace"
            workspace.mkdir()
            config = root / "config.json"
            config.write_text("{}")
            with patch.object(runner.cli, "resolve_engine", return_value="podman"):
                command = build_probe_command(runner, "podman", "sha256:" + "a" * 64,
                                              "print('zero inference')", workspace, config, root)
            joined = " ".join(command)
            for forbidden in ("/seed/auth.json", "/seed/opencode.db", "/seed/opencode-config",
                              "OPENAI_API_KEY", "GH_TOKEN", "GITHUB_TOKEN"):
                self.assertNotIn(forbidden, joined)
            self.assertIn("--pull=never", command)
            self.assertEqual(command[command.index("--network") + 1], "none")
            self.assertIn("--read-only", command)
            self.assertIn(f"{config}:/seed/opencode.json:ro", command)
            self.assertIn(f"{root / 'empty-models.json'}:/seed/models.json:ro", command)
            self.assertEqual((root / "empty-models.json").read_text(), "{}\n")
            self.assertIn("-I", command)


if __name__ == "__main__":
    unittest.main()
