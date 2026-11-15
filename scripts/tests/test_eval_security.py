import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_profile import sanitized_environment, provider_settings, practitioner_files, companion_file, effective_config


class SecurityTests(unittest.TestCase):
    def test_all_treatments_disable_stock_skill_content_but_keep_native_loader(self):
        for side in ("baseline", "candidate", "judge"):
            config = effective_config(side, "s", {}, ("SKILL.md",))
            self.assertEqual(config["plugins"], ["-opencode.skill"])
            self.assertNotIn("-opencode.tool.skill", config["plugins"])
            self.assertNotIn("-opencode.config.skill", config["plugins"])

    def test_practitioner_copy_filters_evaluator_resources_and_rejects_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "s"
            source.mkdir()
            for name in ("SKILL.md", "QA.md", "ASSESSMENT.md", "evals/cases.json", "reference/evaluation.md", "references/useful.md", ".opencode/config.json", "agents/s.agent.md", "AGENTS.md"):
                path = source / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(name)
            self.assertEqual(set(practitioner_files(source)), {"SKILL.md", "references/useful.md"})
            (source / "references" / "escape.md").symlink_to(Path(temp) / "secret.md")
            with self.assertRaises(ValueError):
                practitioner_files(source)

    def test_environment_drops_control_injection_but_keeps_credentials(self):
        env = sanitized_environment({
            "PATH": "/bin", "HOME": "/home/example", "OPENAI_API_KEY": "secret",
            "OPENCODE_EVAL_RUNNER_CONFIG_ROOT": "/loom", "OPENCODE_CONFIG_CONTENT": "bad",
            "OPENCODE_EVAL_RUNNER_IMAGE": "float", "PYTHONPATH": "/inject",
        }, ())
        self.assertEqual(env, {"PATH": "/bin", "HOME": "/home/example", "OPENAI_API_KEY": "secret"})
        for name in ("PYTHONPATH", "OPENCODE_EVAL_RUNNER_CONFIG", "LD_PRELOAD"):
            with self.assertRaises(ValueError):
                sanitized_environment({}, (name,))

    def test_provider_config_rejects_runtime_contamination(self):
        for key in ("plugins", "mcp", "agents", "instructions", "skills", "unknown", "provider"):
            with self.assertRaises(ValueError):
                provider_settings({key: {}})
        with self.assertRaises(ValueError):
            provider_settings({"providers": {"x": {"package": "malicious-package"}}})
        for config in ({"providers": {"x": {"body": {"messages": ["instructions"]}}}},
                       {"providers": {"x": {"models": {"m": {"variants": [{"id": "v", "body": {}}]}}}}}):
            with self.assertRaises(ValueError):
                provider_settings(config)
        self.assertEqual(provider_settings({"providers": {"x": {"settings": {"apiKey": "secret"}}}}),
                         {"providers": {"x": {"settings": {"apiKey": "secret"}}}})

    def test_current_v2_effective_config_has_deny_default_and_narrow_allow(self):
        baseline = effective_config("baseline", "s", {}, ("SKILL.md", "references/guide.md"))
        candidate = effective_config("candidate", "s", {}, ("SKILL.md", "references/guide.md"))
        self.assertEqual(baseline["agents"]["eval-target"]["permissions"],
                         [{"action": "*", "resource": "*", "effect": "deny"}])
        rules = candidate["agents"]["eval-target"]["permissions"]
        self.assertEqual(rules[1], {"action": "skill", "resource": "s", "effect": "allow"})
        self.assertTrue(all(r["action"] in {"*", "read", "skill"} for r in rules))
        self.assertNotIn("permission", candidate)
        self.assertNotIn("tools", candidate["agents"]["eval-target"])


    def test_companion_bytes_are_explicitly_selected_and_symlink_safe(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "s"
            source.mkdir()
            for name in ("SKILL.md", "ASSESSMENT.md", "QA.md"):
                (source / name).write_text(name)
            self.assertEqual(set(practitioner_files(source)), {"SKILL.md"})
            self.assertEqual(companion_file(source, "assessment"), ("ASSESSMENT.md", b"ASSESSMENT.md"))
            self.assertEqual(companion_file(source, "qa"), ("QA.md", b"QA.md"))
            (source / "QA.md").unlink()
            (source / "QA.md").symlink_to(source / "ASSESSMENT.md")
            with self.assertRaisesRegex(ValueError, "non-symlink"):
                companion_file(source, "qa")
            (source / "ASSESSMENT.md").unlink()
            with self.assertRaisesRegex(ValueError, "non-symlink"):
                companion_file(source, "assessment")

    def test_companion_permissions_are_different_on_each_side_without_affecting_default(self):
        for comparison, companion in (("assessment", "ASSESSMENT.md"), ("qa", "QA.md")):
            base_files = {"SKILL.md": b"skill", "references/guide.md": b"guide"}
            candidate_files = {**base_files, companion: b"companion"}
            baseline = effective_config("baseline", "s", {}, base_files, comparison=comparison)
            candidate = effective_config("candidate", "s", {}, candidate_files, comparison=comparison)
            def permissions(config):
                return config["agents"]["eval-target"]["permissions"]
            self.assertIn({"action": "skill", "resource": "s", "effect": "allow"}, permissions(baseline))
            self.assertNotIn({"action": "read", "resource": f".opencode/skills/s/{companion}", "effect": "allow"}, permissions(baseline))
            self.assertIn({"action": "read", "resource": f".opencode/skills/s/{companion}", "effect": "allow"}, permissions(candidate))
            self.assertNotIn(companion, baseline["agents"]["eval-target"]["system"])
            self.assertIn(companion, candidate["agents"]["eval-target"]["system"])
        default = effective_config("baseline", "s", {}, {"SKILL.md": b"skill"})
        self.assertEqual(default["agents"]["eval-target"]["permissions"], [{"action": "*", "resource": "*", "effect": "deny"}])


if __name__ == "__main__":
    unittest.main()
