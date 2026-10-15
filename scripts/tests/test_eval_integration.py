"""Real pinned runner lifecycle/storage with ONLY its invocation I/O substituted.

Synthetic observer events constrain profile assertions; they are not evidence
that a runtime model loaded a skill. No test calls invoke_once or a provider.
"""
import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_cases import strict_json
from eval_profile import JUDGE_SCHEMA, SkillsProfile
from eval_runner import load_runner
from run_evals import execute_pair, parser, run_plan, summarize

ROOT = Path(__file__).resolve().parents[2]


def grade(data, passed=True):
    return {"schema": JUDGE_SCHEMA, "passed": passed,
            "expectations": [{"id": f"E{i+1}", "met": passed, "evidence": "observed response passage"} for i in range(len(data["expectations"]))],
            "violations": [{"id": f"N{i+1}", "violated": False, "evidence": "not present in answer"} for i in range(len(data["must_not"]))],
            "trap_observed": False, "trap_evidence": "no trap in response", "summary": "test judge response"}


class PinnedIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runner = load_runner(Path(os.environ.get("SKILLS_EVAL_RUNNER_ROOT", str(ROOT.parent / "opencode-eval-runner"))))
        # These are external runner-owned builders, not copied schema/accounting.
        from container.runtime_evidence import build_runtime_evidence, unsupported_runtime_evidence
        cls.build_evidence = staticmethod(build_runtime_evidence)
        cls.unsupported_evidence = staticmethod(unsupported_runtime_evidence)

    def setUp(self):
        self.options = parser().parse_args(["--model", "test/model", "--reasoning", "medium"])
        self.options.engine = "podman"
        self.options.target_image_id = self.options.judge_image_id = "sha256:" + "a" * 64
        self.options.target_image_proof = self.options.judge_image_proof = {"test_boundary": "synthetic invocation adapter; no runtime image proof"}
        self.baseline = SkillsProfile(ROOT, self.runner, self.options, "baseline", {})
        self.candidate = SkillsProfile(ROOT, self.runner, self.options, "candidate", {})
        self.case = next(c for c in self.candidate.discover_cases() if c.id == "SKILL-product-acceptance-PA3")
        self.job = self.runner.eval_plan.expand_jobs((self.case,), iterations=1)[0]
        self.calls = []

    def evidence(self, tool=None, input_value=None, *, ended=True, result_state="available", input_state="available", actor="eval-target"):
        available = lambda value: {"state": "available", "value": value}
        records = []
        if tool:
            start = {"kind": "native_start", "sequence": 1, "invocation_id": "n1",
                     "tool": available(tool), "session_id": available("ses"), "agent": available(actor),
                     "message_id": available("msg"), "call_id": available("call"), "parent_session_id": available(None),
                     "input": available(input_value), "boundary": "decoded-tool-execute"}
            terminal = {"kind": "native_terminal", "sequence": 2, "invocation_id": "n1", "tool": available(tool),
                        "session_id": available("ses"), "agent": available(actor), "message_id": available("msg"),
                        "call_id": available("call"), "outcome": "success", "result": available({"content": "loaded practitioner"}),
                        "boundary": "session.tool.success"}
            for field, state, obj in (("input", input_state, start), ("result", result_state, terminal)):
                if state != "available":
                    obj[field] = {"state": state, "reason": "test exact field unavailable"}
            records = [start, terminal]
        return self.build_evidence({"capture_started": True, "capture_ended": ended, "records": records,
                                    "observer_failures": 0, "callback_failures": 0,
                                    "issues": [] if ended else ["missing_capture_end"]})

    def result(self, spec, *, evidence=None, text=None, exit_code=0, stderr=""):
        if evidence is None:
            evidence = self.evidence("skill", {"id": spec.skill}) if spec.skill else self.evidence()
        if text is None:
            text = json.dumps(grade(self.case.project_data)) if spec.agent == "eval-judge" else "Practical first response to supplied scenario."
        return {"schema": "opencode-eval-runner/v1", "transport": spec.transport, "model": spec.model,
                "reasoning": spec.reasoning or "provider-default", "reasoning_source": "explicit" if spec.reasoning else "provider-default",
                "exit_code": exit_code, "text": text, "stderr": stderr, "runtime_evidence": evidence}

    def invoke(self, spec):
        self.calls.append(spec)
        return 0, self.result(spec)

    def pair(self, invoker=None):
        return execute_pair(self.runner, self.baseline, self.candidate, self.job, "test-run", invoker or self.invoke)

    def test_four_calls_real_profile_fresh_projects_same_budget_blind_judges(self):
        def invoke(spec):
            self.calls.append(spec)
            self.assertEqual(spec.workspace_mode, "ro")
            self.assertIsNone(spec.config_root)
            self.assertIsNone(spec.expected_plugin)
            config = strict_json(spec.config.read_text())
            self.assertEqual(config["plugins"], ["-opencode.skill"])
            self.assertNotIn("mcp", config)
            self.assertTrue(spec.workspace.exists())
            if spec.agent == "eval-judge":
                self.assertEqual(list(spec.workspace.rglob("SKILL.md")), [])
                self.assertNotIn("treatment", spec.prompt)
                self.assertNotIn("baseline", spec.prompt)
                self.assertNotIn("candidate", spec.prompt)
                self.assertNotIn("skills_loaded", spec.prompt)
            elif spec.skill:
                skill_dir = spec.workspace / ".opencode" / "skills" / spec.skill
                self.assertTrue((skill_dir / "SKILL.md").is_file())
                self.assertTrue((skill_dir / "references" / "proof-and-example.md").is_file())
                self.assertFalse((skill_dir / "evals").exists())
                self.assertFalse((skill_dir / "QA.md").exists())
                self.assertFalse((skill_dir / "ASSESSMENT.md").exists())
                self.assertIn("explicitly load skill", config["agents"]["eval-target"]["system"])
                self.assertNotIn("A skips discovery provenance", spec.prompt)
            else:
                self.assertEqual(list(spec.workspace.rglob("SKILL.md")), [])
            return 0, self.result(spec)

        artifact = self.pair(invoke)
        self.assertEqual([c.agent for c in self.calls], ["eval-target", "eval-judge", "eval-target", "eval-judge"])
        self.assertEqual(len({c.workspace for c in self.calls}), 4)
        self.assertEqual(self.calls[0].prompt, self.calls[2].prompt)
        self.assertEqual(self.calls[0].model, self.calls[2].model)
        self.assertEqual(self.calls[0].reasoning, self.calls[2].reasoning)
        self.assertEqual(self.calls[0].timeout_seconds, self.calls[2].timeout_seconds)
        self.assertTrue(all(not c.workspace.exists() for c in self.calls))
        summary = summarize(self.runner, [artifact])
        self.assertTrue(summary["all_pass"])
        self.assertEqual(artifact["comparison"]["decision"]["classification"], "neutral")

    def test_complete_native_absence_is_failure_not_diagnostic_success(self):
        def invoke(spec):
            result = self.result(spec, evidence=self.evidence())
            result.update(skills_loaded=["product-acceptance"], tools=["skill"], actions=[{"tool": "skill", "args": {"id": "product-acceptance"}}])
            return 0, result

        artifact = self.pair(invoke)
        self.assertEqual(artifact["sides"]["candidate"]["classification"], "fail")
        self.assertIsNotNone(artifact["sides"]["candidate"]["judge"]["semantic"])
        self.assertEqual(artifact["comparison"]["decision"]["classification"], "unattributed")
        self.assertNotIn("delta_pp", artifact["comparison"]["decision"]["data"])
        self.assertFalse(summarize(self.runner, [artifact])["all_pass"])

    def test_incomplete_candidate_skips_judge_and_blocks_comparison(self):
        def invoke(spec):
            self.calls.append(spec)
            ev = self.evidence("skill", {"id": spec.skill}, ended=False) if spec.skill else self.evidence()
            return 0, self.result(spec, evidence=ev)

        artifact = self.pair(invoke)
        self.assertEqual(len(self.calls), 3)
        self.assertEqual(artifact["sides"]["candidate"]["classification"], "non-evidence")
        self.assertEqual(artifact["comparison"]["status"], "non-evidence")

    def test_exact_required_input_or_result_unavailable_never_backfilled(self):
        for field in ("input_state", "result_state"):
            for state in ("redacted", "omitted", "unsupported"):
                with self.subTest(field=field, state=state):
                    def invoke(spec):
                        ev = self.evidence("skill", {"id": spec.skill}, **{field: state}) if spec.skill else self.evidence()
                        result = self.result(spec, evidence=ev)
                        result["skills_loaded"] = ["product-acceptance"]
                        return 0, result
                    artifact = self.pair(invoke)
                    self.assertEqual(artifact["sides"]["candidate"]["classification"], "non-evidence")
                    self.assertEqual(artifact["comparison"]["status"], "non-evidence")

    def test_unknown_actor_and_baseline_contamination_prevent_attribution(self):
        for candidate_actor in ("other-agent", "eval-target"):
            def invoke(spec):
                if spec.agent == "eval-target":
                    ev = self.evidence("skill", {"id": "product-acceptance"}, actor=candidate_actor if spec.skill else "eval-target")
                    return 0, self.result(spec, evidence=ev)
                return 0, self.result(spec)
            artifact = self.pair(invoke)
            self.assertEqual(artifact["sides"]["baseline"]["classification"], "fail")
            self.assertEqual(artifact["comparison"]["decision"]["classification"], "unattributed")

    def test_missing_runtime_object_is_non_evidence_and_no_judge(self):
        def invoke(spec):
            self.calls.append(spec)
            result = self.result(spec)
            result.pop("runtime_evidence")
            result["skills_loaded"] = ["product-acceptance"]
            return 0, result
        artifact = self.pair(invoke)
        self.assertEqual(len(self.calls), 2)
        self.assertEqual(artifact["comparison"]["status"], "non-evidence")

    def test_empty_output_and_invalid_judge_are_non_evidence_not_semantic_false(self):
        for failure in ("target", "judge"):
            def invoke(spec):
                target = spec.agent == "eval-target"
                text = "" if target and failure == "target" else "{}" if not target and failure == "judge" else None
                return 0, self.result(spec, text=text)
            artifact = self.pair(invoke)
            self.assertEqual(artifact["sides"]["candidate"]["classification"], "non-evidence")
            if failure == "judge":
                self.assertEqual(artifact["sides"]["candidate"]["judge"]["contract_failure"]["code"], "judge_contract_invalid")

    def test_retries_only_runner_replay_safe_signature_and_attempts_persisted(self):
        self.options.transport_retries = 2
        attempts = {}
        def invoke(spec):
            self.calls.append(spec)
            key = (spec.workspace, spec.agent)
            attempts[key] = attempts.get(key, 0) + 1
            if not spec.skill and spec.agent == "eval-target" and attempts[key] == 1:
                return 1, self.result(spec, evidence=self.evidence(), exit_code=1, stderr="provider.no-route Model unavailable")
            return 0, self.result(spec)
        artifact = self.pair(invoke)
        self.assertEqual(len(self.calls), 5)
        prior = artifact["sides"]["baseline"]["target"]["attempts"]
        self.assertEqual(len(prior), 2)
        self.assertTrue(prior[0]["retry_decision"]["retry"])
        self.assertTrue(summarize(self.runner, [artifact])["all_pass"])

    def test_observed_invocation_cannot_retry_even_on_matching_provider_error(self):
        self.options.transport_retries = 2
        def invoke(spec):
            self.calls.append(spec)
            if spec.skill:
                return 1, self.result(spec, exit_code=1, stderr="provider.no-route Model unavailable")
            return 0, self.result(spec)
        artifact = self.pair(invoke)
        self.assertEqual(len(self.calls), 3)
        attempts = artifact["sides"]["candidate"]["target"]["attempts"]
        self.assertEqual(len(attempts), 1)
        self.assertFalse(attempts[0]["failure"]["retry_safe"])
        self.assertFalse(attempts[0]["retry_decision"]["retry"])

    def test_product_timeout_and_unsupported_boundary_are_non_evidence_no_retry(self):
        self.options.transport_retries = 1
        for kind in ("timeout", "unsupported"):
            def invoke(spec):
                if spec.skill:
                    if kind == "timeout":
                        return 0, self.result(spec, exit_code=124)
                    return 0, self.result(spec, evidence=self.unsupported_evidence("unsupported transport"))
                return 0, self.result(spec)
            artifact = self.pair(invoke)
            self.assertEqual(artifact["sides"]["candidate"]["classification"], "non-evidence")
            self.assertEqual(len(artifact["sides"]["candidate"]["target"]["attempts"]), 1)

    def test_completed_negative_exit_one_independent_of_relative_value(self):
        def invoke(spec):
            if spec.agent == "eval-judge":
                return 0, self.result(spec, text=json.dumps(grade(self.case.project_data, False)))
            return self.invoke(spec)
        artifact = self.pair(invoke)
        self.assertEqual(artifact["sides"]["candidate"]["classification"], "fail")
        self.assertEqual(artifact["comparison"]["decision"]["classification"], "neutral")
        self.assertFalse(summarize(self.runner, [artifact])["all_pass"])
        self.assertEqual(summarize(self.runner, [artifact])["complete_pairs"], 1)

    def test_copilot_judge_unsupported_runtime_is_allowed_only_for_text_judgment(self):
        self.options.judge_transport = "github-copilot-cli"
        self.options.judge_model = "test-judge"
        def invoke(spec):
            self.calls.append(spec)
            ev = self.unsupported_evidence("copilot") if spec.agent == "eval-judge" else None
            return 0, self.result(spec, evidence=ev)
        artifact = self.pair(invoke)
        self.assertEqual([s.transport for s in self.calls], ["opencode", "github-copilot-cli", "opencode", "github-copilot-cli"])
        self.assertTrue(summarize(self.runner, [artifact])["all_pass"])

    def test_actual_runner_owned_storage_reread_tamper_and_summary(self):
        artifact = self.pair()
        with tempfile.TemporaryDirectory() as temp:
            store = self.runner.eval_artifacts.claim_run_artifact_directory(Path(temp) / "run", "test-run")
            identity = self.runner.eval_artifacts.artifact_identity_for_job("test-run", self.job)
            store.write_paired_job_artifact(identity, artifact)
            self.assertEqual(store.read_paired_job_artifact(identity), artifact)
            self.assertTrue(summarize(self.runner, [store.read_paired_job_artifact(identity)])["all_pass"])
            tampered = copy.deepcopy(artifact)
            tampered["sides"]["candidate"]["judge"]["semantic"]["data"]["score"] = 0
            store.paired_job_path(identity).write_text(json.dumps(tampered))
            with self.assertRaises(self.runner.eval_artifacts.EvalArtifactError):
                store.read_paired_job_artifact(identity)
            with self.assertRaises(self.runner.eval_artifacts.EvalArtifactError):
                summarize(self.runner, [tampered])

    def test_driver_persists_four_call_summary_from_verified_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            self.options.artifact_dir = Path(temp) / "run"
            plan = self.runner.eval_plan.build_run_plan("driver-test", (self.case,), select_all=True)
            code, summary = run_plan(ROOT, self.runner, self.options, plan, {}, self.invoke, report_root=Path(temp))
            self.assertEqual(code, 0)
            store = self.runner.eval_artifacts.claim_run_artifact_directory(self.options.artifact_dir, "driver-test")
            self.assertEqual(store.read_run_manifest()["summary"], summary)
            self.assertEqual(summary["pairs"][0]["attempts"], {
                "baseline": {"target": 1, "judge": 1}, "candidate": {"target": 1, "judge": 1}})

    def test_driver_negative_non_evidence_and_orchestration_exit_codes(self):
        for kind, expected in (("negative", 1), ("non-evidence", 1), ("orchestration", 2)):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                self.options.artifact_dir = Path(temp) / "run"
                plan = self.runner.eval_plan.build_run_plan("exit-test", (self.case,), select_all=True)
                def invoke(spec):
                    if kind == "orchestration":
                        raise AssertionError("test boundary orchestration bug")
                    if spec.agent == "eval-judge":
                        return 0, self.result(spec, text="{}" if kind == "non-evidence" else json.dumps(grade(self.case.project_data, False)))
                    return self.invoke(spec)
                code, summary = run_plan(ROOT, self.runner, self.options, plan, {}, invoke, report_root=Path(temp))
                self.assertEqual(code, expected)
                self.assertFalse(summary["all_pass"])

    def test_parallel_pairs_have_distinct_projects_and_preserve_side_order(self):
        import threading
        lock = threading.Lock()
        seen = []
        self.options.parallel = self.options.iterations = 2
        with tempfile.TemporaryDirectory() as temp:
            self.options.artifact_dir = Path(temp) / "run"
            plan = self.runner.eval_plan.build_run_plan("parallel-test", (self.case,), select_all=True,
                                                       iterations=2, runtime_parallelism=2)
            def invoke(spec):
                with lock:
                    seen.append(spec)
                return 0, self.result(spec)
            code, summary = run_plan(ROOT, self.runner, self.options, plan, {}, invoke, report_root=Path(temp))
            self.assertEqual(code, 0)
            self.assertEqual(len(seen), 8)
            self.assertEqual(len({s.workspace for s in seen}), 8)
            self.assertEqual(summary["complete_pairs"], 2)
            for record in summary["pairs"]:
                self.assertEqual(record["attempts"], {"baseline": {"target": 1, "judge": 1}, "candidate": {"target": 1, "judge": 1}})

    def test_judge_tools_or_incomplete_capture_cannot_authorize_a_grade(self):
        for contaminated in (True, False):
            def invoke(spec):
                if spec.agent == "eval-judge":
                    ev = self.evidence("read", {"path": "/workspace/hidden"}, actor="eval-judge") if contaminated else self.evidence(ended=False)
                    return 0, self.result(spec, evidence=ev)
                return self.invoke(spec)
            artifact = self.pair(invoke)
            self.assertEqual(artifact["sides"]["candidate"]["classification"], "non-evidence")
            self.assertEqual(artifact["sides"]["candidate"]["judge"]["contract_failure"]["code"], "judge_contract_invalid")

    def test_actual_runner_command_uses_generated_config_readonly_project_no_loom_and_never_pull(self):
        import argparse
        from unittest.mock import patch
        from run_evals import freeze_environment
        with self.candidate.prepare(self.case, 1) as prepared:
            spec = self.candidate.target_spec(self.case, prepared)
            temp = spec.config.parent
            auth, models = temp / "auth.json", temp / "models.json"
            auth.write_text("{}")
            models.write_text("{}")
            args = argparse.Namespace(transport=spec.transport, engine=spec.engine, image=spec.image,
                                      network=spec.network, workspace=str(spec.workspace), workspace_mode=spec.workspace_mode,
                                      output=str(temp / "result.json"), mount=[], skill=spec.skill, agent=spec.agent,
                                      model=spec.model, reasoning=spec.reasoning, expected_plugin=None,
                                      auth=str(auth), models_catalog=str(models), config=str(spec.config),
                                      config_root=None, env=[], timeout_seconds=240)
            with patch.dict(os.environ, {"PATH": os.defpath, "OPENCODE_EVAL_RUNNER_CONFIG_ROOT": "/loom",
                                         "OPENCODE_EVAL_RUNNER_CONFIG": "/bad", "OPENCODE_EVAL_RUNNER_IMAGE": "float"}, clear=True):
                freeze_environment(self.options)
                command, _ = self.runner.cli.build_container_command(args, temp / "input", temp / "output", host_env={})
            self.assertIn("--pull=never", command)
            self.assertIn("--read-only", command)
            self.assertIn(f"{spec.workspace}:/workspace:ro", command)
            self.assertIn(f"{spec.config}:/seed/opencode.json:ro", command)
            self.assertNotIn("/loom:/seed/opencode-config:ro", command)
            self.assertEqual(command[-1], self.options.target_image_id)

    def test_actual_comparison_material_policy_uses_boolean_fraction_delta(self):
        self.case = next(c for c in self.candidate.discover_cases() if c.id == "SKILL-software-engineering-SoftwareEngineering-01")
        self.job = self.runner.eval_plan.expand_jobs((self.case,), iterations=1)[0]
        judges = 0
        def invoke(spec):
            nonlocal judges
            if spec.agent == "eval-judge":
                judges += 1
                response = grade(self.case.project_data)
                if judges == 1:
                    response["expectations"][-1]["met"] = False
                    response["passed"] = False
                return 0, self.result(spec, text=json.dumps(response))
            return self.invoke(spec)
        artifact = self.pair(invoke)
        self.assertEqual(artifact["comparison"]["decision"]["classification"], "material-improvement")
        self.assertEqual(artifact["comparison"]["decision"]["data"]["delta_pp"], 10)
        self.assertTrue(summarize(self.runner, [artifact])["all_pass"])

    def test_reference_read_must_start_after_successful_native_load_terminal(self):
        def events(tool, args, iid, start, terminal):
            a = lambda value: {"state": "available", "value": value}
            identity = {"invocation_id": iid, "tool": a(tool), "session_id": a("ses"),
                        "agent": a("eval-target"), "message_id": a("msg"), "call_id": a(iid)}
            return [{**identity, "kind": "native_start", "sequence": start,
                     "parent_session_id": a(None), "input": a(args), "boundary": "decoded-tool-execute"},
                    {**identity, "kind": "native_terminal", "sequence": terminal,
                     "outcome": "success", "result": a({"content": "success"}), "boundary": "session.tool.success"}]
        for read_start, expected in ((2, "fail"), (4, "pass")):
            def invoke(spec):
                if spec.skill:
                    records = events("skill", {"id": spec.skill}, "load", 1, 3)
                    records += events("read", {"path": f".opencode/skills/{spec.skill}/references/proof-and-example.md"}, "read", read_start, 5)
                    ev = self.build_evidence({"capture_started": True, "capture_ended": True,
                                              "records": records, "observer_failures": 0, "callback_failures": 0, "issues": []})
                    return 0, self.result(spec, evidence=ev)
                return self.invoke(spec)
            artifact = self.pair(invoke)
            self.assertEqual(artifact["sides"]["candidate"]["classification"], expected)


if __name__ == "__main__":
    unittest.main()
