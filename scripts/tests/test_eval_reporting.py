"""Provider-free presentation tests using the real pinned paired engine."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_reporting import EvalReporter
from run_evals import summarize
import test_eval_integration as integration


class ReportingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        integration.PinnedIntegrationTests.setUpClass()

    def setUp(self):
        self.context = integration.PinnedIntegrationTests()
        self.context.setUp()
        self.stream = io.StringIO()
        self.reporter = EvalReporter(stream=self.stream)

    def test_compound_failure_reports_scores_rule_count_rationale_not_all_wrong(self):
        judges = 0
        def invoke(spec):
            nonlocal judges
            if spec.agent == "eval-judge":
                judges += 1
                response = integration.grade(self.context.case.project_data, judges == 1)
                response["expectations"][0]["evidence"] = "Missing provenance, but downstream routing evidence remains valid."
                return 0, self.context.result(spec, text=json.dumps(response))
            return self.context.invoke(spec)
        artifact = self.context.pair(invoke)
        summary = summarize(self.context.runner, [artifact])
        self.reporter.pair(self.context.runner, artifact, summary["pairs"][0])
        self.reporter.summary(summary, 1, Path("/tmp/replay"))

        output = self.stream.getvalue()
        self.assertIn("SKILL-product-acceptance-PA3#1", output)
        self.assertIn("baseline PASS 100% -> candidate FAIL 0%", output)
        self.assertIn("observed regression (-100.0 pp)", output)
        self.assertIn("not statistical significance", output)
        self.assertIn("1/1 positive criteria unmet", output)
        self.assertIn("E1: Missing provenance", output)
        self.assertIn("compound", output)
        self.assertIn("Observed attempts: 2 target + 2 judge", output)
        self.assertIn("Run artifacts: /tmp/replay", output)
        self.assertIn("Manifest: /tmp/replay/run.json", output)
        self.assertNotIn("paired_artifact_evidence_id", output)
        self.assertNotIn('"event"', output)

    def test_structured_runtime_error_not_stdout_text_or_host_exception(self):
        def invoke(spec):
            result = self.context.result(spec, exit_code=1)
            result["stdout"] = json.dumps({"type": "text", "text": "PRIVATE ANSWER"}) + "\n" + json.dumps({
                "type": "error", "error": {"message": "Invalid model reference: gpt-6-luna\u001b[31m\n\u202e"}})
            return 0, result
        artifact = self.context.pair(invoke)
        summary = summarize(self.context.runner, [artifact])
        self.reporter.pair(self.context.runner, artifact, summary["pairs"][0])
        output = self.stream.getvalue()
        self.assertIn("NON-EVIDENCE (score unavailable)", output)
        self.assertIn("Invalid model reference: gpt-6-luna", output)
        self.assertNotIn("candidate FAIL", output)
        self.assertNotIn("PRIVATE ANSWER", output)
        self.assertNotIn("\u001b", output)
        self.assertNotIn("\u202e", output)

    def test_json_events_preserve_exact_existing_schema_and_no_human_progress(self):
        from run_evals import call_budget
        artifact = self.context.pair()
        summary = summarize(self.context.runner, [artifact])
        reporter = EvalReporter(json_output=True, stream=self.stream)
        budget = call_budget(1, self.context.options)
        reporter.budget(budget)
        reporter.invocation("case", 1, "candidate", "target", 1)
        reporter.pair(self.context.runner, artifact, summary["pairs"][0])
        reporter.summary(summary, 1, Path("/tmp/replay"))
        events = [json.loads(line) for line in self.stream.getvalue().splitlines()]
        self.assertEqual(events, [{"event": "live-spend-plan", **budget},
                                 {"event": "verified-pair", **summary["pairs"][0]},
                                 {"event": "verified-summary", "artifact_dir": "/tmp/replay", **summary}])

    def test_tampered_pair_never_prints_verdict_or_detail(self):
        artifact = self.context.pair()
        record = summarize(self.context.runner, [artifact])["pairs"][0]
        artifact["sides"]["candidate"]["classification"] = "fail"
        with self.assertRaises(self.context.runner.eval_artifacts.EvalArtifactError):
            self.reporter.pair(self.context.runner, artifact, record)
        self.assertEqual(self.stream.getvalue(), "")

    def test_live_driver_emits_progress_then_verified_results_without_changing_artifacts(self):
        from run_evals import run_plan
        with tempfile.TemporaryDirectory() as temp:
            self.context.options.artifact_dir = Path(temp) / "run"
            plan = self.context.runner.eval_plan.build_run_plan("reporting-test", (self.context.case,), select_all=True)
            code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {},
                                     self.context.invoke, reporter=self.reporter, report_root=Path(temp))
            store = self.context.runner.eval_artifacts.claim_run_artifact_directory(self.context.options.artifact_dir, "reporting-test")
            self.assertEqual(store.read_run_manifest()["summary"], summary)
            output = self.stream.getvalue()
            self.assertEqual(code, 0)
            self.assertIn("baseline target attempt 1 ...", output)
            self.assertIn("candidate judge attempt 1 ...", output)
            self.assertIn("baseline PASS 100% -> candidate PASS 100%", output)
            self.assertLess(output.index("candidate judge attempt"), output.index("candidate PASS"))

    def test_main_output_modes_route_json_notices_to_stderr_and_keep_durable_summary(self):
        from run_evals import main
        for flags in ([], ["--json"], ["--verbose"]):
            with self.subTest(flags=flags), tempfile.TemporaryDirectory() as temp:
                stdout, stderr = io.StringIO(), io.StringIO()
                destination = Path(temp) / "run"
                # Substitute only external image/engine and invocation I/O.
                # Actual selection, profiles, paired engine, storage and reporting run.
                with patch.dict(os.environ, {"PATH": os.defpath}, clear=True), \
                     patch("run_evals.verify_image", return_value={"image_id": "sha256:" + "a" * 64}), \
                     patch.object(self.context.runner.cli, "resolve_engine", return_value="podman"), \
                     patch.object(self.context.runner.eval_execute, "invoke_once", side_effect=self.context.invoke), \
                     redirect_stdout(stdout), redirect_stderr(stderr):
                    code = main(["--cases", "product-acceptance:PA3", "--model", "test/model", "--network", "host",
                                  "--artifact-dir", str(destination), *flags], report_root=Path(temp))
                self.assertEqual(code, 0, stderr.getvalue())
                self.assertIn("weakens isolation", stderr.getvalue())
                durable = json.loads((destination / "run.json").read_text())["summary"]
                if "--json" in flags:
                    events = [json.loads(line) for line in stdout.getvalue().splitlines()]
                    self.assertEqual([e["event"] for e in events], ["live-spend-plan", "run-started", "verified-pair", "verified-summary"])
                    self.assertEqual(events[-1], {"event": "verified-summary", "artifact_dir": str(destination),
                                                "report_path": str(destination / "results.md"),
                                                "latest_report_path": str(Path(temp) / "EVAL-RESULTS.md"), **durable})
                    self.assertIn("not an offline evaluation", stderr.getvalue())
                else:
                    self.assertIn("candidate PASS 100%", stdout.getvalue())
                    self.assertIn("Planned:", stdout.getvalue())
                    self.assertIn("Completed:", stdout.getvalue())
                    self.assertNotIn('"event"', stdout.getvalue())
                    self.assertEqual("host exit 0" in stdout.getvalue(), "--verbose" in flags)
                    self.assertEqual(stdout.getvalue().count("Report: " + str(destination / "results.md")), 1)
                    self.assertTrue(stdout.getvalue().endswith("Latest report: " + str(Path(temp) / "EVAL-RESULTS.md") + "\n"))

    def test_output_flags_mutually_exclusive_before_any_live_work(self):
        import subprocess
        script = integration.ROOT / "scripts" / "run_evals.py"
        proc = subprocess.run([sys.executable, "-I", "-B", str(script), "--json", "--verbose"],
                              capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(proc.stdout, "")
        self.assertIn("not allowed with argument", proc.stderr)

    def test_verbose_is_bounded_and_runner_redaction_hides_credentials(self):
        from container.evidence_safety import Sanitizer
        from container.invoke import sanitize_result_for_output
        secret = "fictional-reporting-credential-987654321"
        def invoke(spec):
            result = self.context.result(spec, exit_code=1)
            result["stdout"] = json.dumps({"type": "error", "error": {
                "message": "provider unavailable " + secret + "\u001b]52;c;bad\u0007\u202e\n" + "z" * 10000,
                "private_payload": "DO NOT PRINT PAYLOAD"}})
            result["stderr"] = "DO NOT PRINT SECONDARY LOGS"
            return 0, sanitize_result_for_output(result, Sanitizer((secret,)))
        artifact = self.context.pair(invoke)
        summary = summarize(self.context.runner, [artifact])
        reporter = EvalReporter(verbose=True, stream=self.stream)
        reporter.pair(self.context.runner, artifact, summary["pairs"][0])
        output = self.stream.getvalue()
        self.assertNotIn(secret, output)
        self.assertNotIn("DO NOT PRINT", output)
        self.assertNotIn("\u001b", output)
        self.assertNotIn("\u202e", output)
        self.assertIn("provider unavailable", output)
        self.assertIn("host exit 0", output)
        self.assertLess(len(output), 2000)

    def test_invalid_judge_missing_capture_and_native_absence_remain_distinct(self):
        for failure in ("judge", "capture", "native"):
            with self.subTest(failure=failure):
                self.stream.seek(0)
                self.stream.truncate()
                def invoke(spec):
                    if failure == "judge" and spec.agent == "eval-judge":
                        return 0, self.context.result(spec, text="{}")
                    if spec.skill:
                        ev = self.context.evidence(ended=failure != "capture")
                        return 0, self.context.result(spec, evidence=ev)
                    return self.context.invoke(spec)
                artifact = self.context.pair(invoke)
                summary = summarize(self.context.runner, [artifact])
                self.reporter.pair(self.context.runner, artifact, summary["pairs"][0])
                output = self.stream.getvalue()
                if failure == "native":
                    self.assertIn("candidate FAIL 100%", output)
                    self.assertIn("Comparison unattributed", output)
                    self.assertIn("not successfully loaded", output)
                else:
                    self.assertIn("candidate NON-EVIDENCE", output)
                    self.assertIn("judge_contract_invalid" if failure == "judge" else "evidence_incomplete", output)

    def test_observed_retry_counts_not_nominal_budget_and_unredacted_exception_hidden(self):
        from run_evals import call_budget, run_plan
        self.context.options.transport_retries = 1
        attempts = {}
        def invoke(spec):
            key = spec.workspace
            attempts[key] = attempts.get(key, 0) + 1
            if not spec.skill and spec.agent == "eval-target" and attempts[key] == 1:
                return 1, self.context.result(spec, evidence=self.context.evidence(), exit_code=1,
                                              stderr="provider.no-route Model unavailable")
            return self.context.invoke(spec)
        artifact = self.context.pair(invoke)
        summary = summarize(self.context.runner, [artifact])
        self.reporter.budget(call_budget(1, self.context.options))
        self.reporter.summary(summary, 1, Path("/tmp/replay"))
        self.assertIn("nominal 2 target + 2 judge", self.stream.getvalue())
        self.assertIn("maximum 4 target + 4 judge", self.stream.getvalue())
        self.assertIn("Observed attempts: 3 target + 2 judge", self.stream.getvalue())
        with tempfile.TemporaryDirectory() as temp:
            self.context.options.artifact_dir = Path(temp) / "run"
            plan = self.context.runner.eval_plan.build_run_plan("reporting-error", (self.context.case,), select_all=True)
            def broken(spec):
                raise AssertionError("UNREDACTED PRIVATE HOST EXCEPTION")
            code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, broken,
                                     reporter=self.reporter, report_root=Path(temp))
            self.reporter.summary(summary, 1, self.context.options.artifact_dir)
        output = self.stream.getvalue()
        self.assertEqual(code, 2)
        self.assertIn("orchestration: AssertionError", output)
        self.assertIn("partial; failed jobs may have additional attempts", output)
        self.assertNotIn("UNREDACTED PRIVATE", output)

    def test_exact_10pp_material_improvement_and_trap_fix_are_observations_only(self):
        self.context.case = next(c for c in self.context.candidate.discover_cases()
                                 if c.id == "SKILL-software-engineering-SoftwareEngineering-01")
        self.context.job = self.context.runner.eval_plan.expand_jobs((self.context.case,), iterations=1)[0]
        for trap in (False, True):
            with self.subTest(trap=trap):
                self.stream.seek(0)
                self.stream.truncate()
                judges = 0
                def invoke(spec):
                    nonlocal judges
                    if spec.agent == "eval-judge":
                        judges += 1
                        response = integration.grade(self.context.case.project_data)
                        if judges == 1:
                            if trap:
                                response["trap_observed"] = True
                            else:
                                response["expectations"][-1]["met"] = False
                            response["passed"] = False
                        return 0, self.context.result(spec, text=json.dumps(response))
                    return self.context.invoke(spec)
                artifact = self.context.pair(invoke)
                summary = summarize(self.context.runner, [artifact])
                self.reporter.pair(self.context.runner, artifact, summary["pairs"][0])
                output = self.stream.getvalue()
                self.assertIn("observed material-improvement (+10.0 pp)", output)
                self.assertIn("not statistical significance", output)
                self.assertEqual("Trap: fixed in this pair" in output, trap)

    def test_parallel_completion_is_prompt_and_pair_blocks_do_not_interleave(self):
        import threading
        from run_evals import run_plan
        first_waiting, second_reported = threading.Event(), threading.Event()
        report_pair = self.reporter.pair
        self.context.options.parallel = self.context.options.iterations = 2
        first_workspace = None
        lock = threading.Lock()
        def invoke(spec):
            nonlocal first_workspace
            # Invocation order is not a stable job identifier. Use the configured
            # prompt unchanged; only hold the first entered invocation I/O.
            with lock:
                if first_workspace is None:
                    first_workspace = spec.workspace
                hold = spec.workspace == first_workspace and not first_waiting.is_set()
            if hold:
                first_waiting.set()
                # A finished pair must report even while another pair is waiting.
                # Either job may enter first, so release when any pair is reported.
                if not second_reported.wait(5):
                    raise AssertionError("completion reporting blocked on a pending pair")
            return self.context.invoke(spec)
        # Release for whichever independent pair finishes first (not scheduling order).
        def report_any(runner, artifact, record):
            report_pair(runner, artifact, record)
            second_reported.set()
        self.reporter.pair = report_any
        with tempfile.TemporaryDirectory() as temp:
            self.context.options.artifact_dir = Path(temp) / "run"
            plan = self.context.runner.eval_plan.build_run_plan("reporting-parallel", (self.context.case,), select_all=True,
                                                              iterations=2, runtime_parallelism=2)
            code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, invoke,
                                     reporter=self.reporter, report_root=Path(temp))
        self.assertEqual(code, 0)
        self.assertEqual(summary["complete_pairs"], 2)
        self.assertEqual(self.stream.getvalue().count("baseline PASS 100% -> candidate PASS 100%"), 2)
        self.assertEqual(self.stream.getvalue().count("Paired observation: observed neutral"), 2)
        for iteration in (1, 2):
            for side in ("baseline", "candidate"):
                for phase in ("target", "judge"):
                    prefix = f"SKILL-product-acceptance-PA3#{iteration} {side} {phase} attempt 1 returned in"
                    self.assertEqual(self.stream.getvalue().count(prefix), 1)

    def test_terminal_text_strips_controls_and_bounds_diagnostic_line(self):
        from eval_reporting import terminal_text, runtime_error_detail
        dirty = "\u001b[31mred\u001b[0m\u001b]8;;https://unsafe\u0007link\u001b]8;;\u0007\r\n\u009b2J\u202e\u0000" + "x" * 1000
        clean = terminal_text(dirty, 60)
        self.assertEqual(len(clean), 60)
        self.assertTrue(clean.startswith("redlink "))
        self.assertTrue(clean.endswith("..."))
        self.assertNotIn("https://unsafe", clean)
        self.assertEqual(runtime_error_detail({"stdout": "PRIVATE RAW LOG", "stderr": ""}), "")

    def test_optional_or_malformed_diagnostic_streams_do_not_change_non_evidence_exit(self):
        from run_evals import run_plan
        from eval_reporting import runtime_error_detail
        for stdout, stderr in ((None, None), ([], {"private": "never repr this"}),
                               ("[" * 2000 + "]" * 2000, "")):
            with self.subTest(stdout_type=type(stdout).__name__):
                self.assertEqual(runtime_error_detail({"stdout": stdout, "stderr": stderr}), "")
                def invoke(spec):
                    result = self.context.result(spec, exit_code=1)
                    result.update(stdout=stdout, stderr=stderr)
                    return 0, result
                with tempfile.TemporaryDirectory() as temp:
                    self.context.options.artifact_dir = Path(temp) / "run"
                    plan = self.context.runner.eval_plan.build_run_plan("optional-streams", (self.context.case,), select_all=True)
                    code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, invoke,
                                             reporter=self.reporter, report_root=Path(temp))
                self.assertEqual(code, 1)
                self.assertEqual(summary["orchestration_errors"], [])
        self.assertNotIn("never repr this", self.stream.getvalue())

    def test_host_callback_faults_are_private_in_human_and_json_but_artifacts_unchanged(self):
        from eval_profile import SkillsProfile, SkillsComparison
        from container.evidence_safety import Sanitizer
        from container.invoke import sanitize_result_for_output
        from run_evals import run_plan
        name, secret = "REPORT_SECRET_TOKEN", "fictional-reporting-host-callback-secret-20261014"
        self.context.options.env = [name]
        def invoke(spec):
            inventory = Sanitizer.from_runtime({name: secret})
            self.assertIn(secret, inventory.credentials)
            return 0, sanitize_result_for_output(self.context.result(spec), inventory)
        for callback, owner in (("deterministic_checks", SkillsProfile), ("judge_spec", SkillsProfile),
                                ("parse_judge", SkillsProfile), ("compare_pair", SkillsComparison)):
            for mode in ({}, {"verbose": True}, {"json_output": True}):
                with self.subTest(callback=callback, mode=mode), tempfile.TemporaryDirectory() as temp:
                    self.context.options.artifact_dir = Path(temp) / "run"
                    plan = self.context.runner.eval_plan.build_run_plan("private-callback", (self.context.case,), select_all=True)
                    stream = io.StringIO()
                    reporter = EvalReporter(stream=stream, **mode)
                    with patch.dict(os.environ, {name: secret}), \
                         patch.object(owner, callback, side_effect=RuntimeError("private host callback failed: " + secret)):
                        code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, invoke,
                                                 reporter=reporter, report_root=Path(temp))
                    store = self.context.runner.eval_artifacts.RunArtifactStore(self.context.options.artifact_dir, plan.run_id)
                    artifact = store.read_paired_job_artifact(self.context.runner.eval_artifacts.artifact_identity_for_job(plan.run_id, plan.jobs[0]))
                    self.assertIn(secret, json.dumps(artifact))  # actual runner host-catch AFTER result sanitizer
                    self.assertEqual(store.read_run_manifest()["summary"], summary)
                    before = json.dumps(summary, sort_keys=True)
                    reporter.summary(summary, 1, self.context.options.artifact_dir)
                    output = stream.getvalue()
                    markdown = (self.context.options.artifact_dir / "results.md").read_text()
                    self.assertEqual(code, 1)
                    self.assertNotIn(secret, output)
                    self.assertNotIn(secret, markdown)
                    self.assertNotIn(secret, (Path(temp) / "EVAL-RESULTS.md").read_text())
                    self.assertNotIn("private host callback failed", output)
                    self.assertEqual(json.dumps(summary, sort_keys=True), before)
                    if mode.get("json_output"):
                        events = [json.loads(line) for line in output.splitlines()]
                        self.assertEqual([e["event"] for e in events], ["run-started", "verified-pair", "verified-summary"])
                        events = events[1:]
                        for key in ("baseline", "candidate", "complete_pair_evidence", "attempts", "paired_artifact_evidence_id"):
                            self.assertEqual(events[0][key], summary["pairs"][0][key])
                        self.assertEqual(events[1]["complete_pairs"], summary["complete_pairs"])
                        self.assertEqual(set(events[0]), {"event", *summary["pairs"][0]})
                    elif callback == "deterministic_checks":
                        self.assertIn("deterministic_checks_invalid", output)
                        self.assertIn("diagnostic withheld", output)

    def test_unknown_check_payload_and_malformed_callback_return_are_not_console_rationale(self):
        from eval_profile import SkillsProfile
        from run_evals import run_plan
        secret = "PRIVATE-CALLBACK-DETAIL-AND-METADATA"
        for kind in ("known-name", "unknown-name", "malformed"):
            for mode in ({}, {"verbose": True}, {"json_output": True}):
                with self.subTest(kind=kind, mode=mode), tempfile.TemporaryDirectory() as temp:
                    self.context.options.artifact_dir = Path(temp) / "run"
                    plan = self.context.runner.eval_plan.build_run_plan("private-check", (self.context.case,), select_all=True)
                    stream = io.StringIO()
                    reporter = EvalReporter(stream=stream, **mode)
                    checks = [object()] if kind == "malformed" else [self.context.runner.eval_api.CheckOutcome(
                        "treatment-integrity" if kind == "known-name" else secret,
                        "non-evidence", "arbitrary rationale " + secret, {"private": secret})]
                    with patch.object(SkillsProfile, "deterministic_checks", return_value=checks):
                        code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {},
                                                 self.context.invoke, reporter=reporter, report_root=Path(temp))
                    reporter.summary(summary, 1, self.context.options.artifact_dir)
                    self.assertEqual(code, 1)
                    self.assertNotIn(secret, stream.getvalue())
                    self.assertNotIn(secret, (self.context.options.artifact_dir / "results.md").read_text())
                    self.assertNotIn(secret, (Path(temp) / "EVAL-RESULTS.md").read_text())
                    self.assertIn("diagnostic withheld", stream.getvalue())

    def test_probe_callback_and_malformed_provider_json_keep_private_diagnostics_off_console(self):
        from run_evals import main, run_probe
        secret = "PRIVATE-PROBE-CALLBACK-AND-JSON-KEY"
        self.context.options.target_image_proof = {"test": "injected probe; no image proof"}
        with tempfile.TemporaryDirectory() as temp:
            self.context.options.artifact_dir = Path(temp) / "probe"
            def failed_probe(root, runner, options, case, record):
                record("baseline", {"private_observation": secret})
                raise RuntimeError("private probe callback failed: " + secret)
            stderr = io.StringIO()
            with redirect_stderr(stderr):
                with self.assertRaises(ValueError) as raised:
                    run_probe(integration.ROOT, self.context.runner, self.context.options, self.context.case, failed_probe)
            self.assertNotIn(secret, str(raised.exception))
            self.assertNotIn(secret, stderr.getvalue())
            self.assertIn("retained probe evidence", stderr.getvalue())
            durable = json.loads((self.context.options.artifact_dir / "run.json").read_text())
            self.assertIn(secret, durable["summary"]["error"])
            self.assertEqual(durable["summary"]["status"], "failed")

        for probe in (False, True):
            for flags in ([], ["--verbose"], ["--json"]):
                with self.subTest(probe=probe, flags=flags), tempfile.TemporaryDirectory() as temp:
                    provider = Path(temp) / "provider.json"
                    provider.write_text('{"' + secret + '":1,"' + secret + '":2}')
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with redirect_stdout(stdout), redirect_stderr(stderr), patch("run_evals.load_runner") as loader:
                        code = main(["--cases", "product-acceptance:PA3", "--model", "test/model", "--provider-config", str(provider),
                                     *(["--probe"] if probe else []), *flags])
                    self.assertEqual(code, 2)
                    loader.assert_not_called()
                    self.assertNotIn(secret, stdout.getvalue() + stderr.getvalue())
                    self.assertIn("diagnostic withheld", stderr.getvalue())

    def test_four_attempt_returns_precede_next_phase_and_verified_verdict_with_elapsed_time(self):
        from run_evals import run_plan
        entered = []
        def invoke(spec):
            entered.append(self.stream.getvalue())
            return self.context.invoke(spec)
        with tempfile.TemporaryDirectory() as temp, patch("run_evals.perf_counter", side_effect=[10, 10.25, 11, 11.5, 12, 12.75, 13, 14]):
            self.context.options.artifact_dir = Path(temp) / "run"
            plan = self.context.runner.eval_plan.build_run_plan("attempt-returns", (self.context.case,), select_all=True)
            code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, invoke,
                                     reporter=self.reporter, report_root=Path(temp))
        self.assertEqual(code, 0)
        self.assertEqual(len(entered), 4)
        for index, (side, phase) in enumerate((("baseline", "target"), ("baseline", "judge"), ("candidate", "target"))):
            self.assertIn(f"{side} {phase} attempt 1 returned", entered[index + 1])
            self.assertNotIn("PASS", entered[index + 1])
        output = self.stream.getvalue()
        self.assertIn("candidate judge attempt 1 returned in 1.0s", output)
        self.assertLess(output.index("candidate judge attempt 1 returned"), output.index("candidate PASS"))
        self.assertEqual(sum("returned in" in line for line in output.splitlines()), 4)

    def test_failed_raised_and_malformed_attempt_returns_are_generic_not_grades_or_exceptions(self):
        from run_evals import run_plan
        for outcome in ("error", "raised", "malformed"):
            with self.subTest(outcome=outcome), tempfile.TemporaryDirectory() as temp:
                stream = io.StringIO()
                self.context.options.artifact_dir = Path(temp) / "run"
                plan = self.context.runner.eval_plan.build_run_plan("attempt-errors", (self.context.case,), select_all=True)
                def invoke(spec):
                    if outcome == "raised":
                        raise ValueError("PRIVATE EXCEPTION DETAILS")
                    if outcome == "malformed":
                        return 0, "PRIVATE MALFORMED PAYLOAD"
                    return 0, self.context.result(spec, exit_code=1)
                code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, invoke,
                                         reporter=EvalReporter(stream=stream), report_root=Path(temp))
                output = stream.getvalue()
                self.assertEqual(code, 1)
                expected = {"error": "returned (reported error)", "raised": "raised (host error)",
                            "malformed": "returned (unrecognized response)"}[outcome]
                self.assertIn(f"baseline target attempt 1 {expected} in", output)
                self.assertIn(f"candidate target attempt 1 {expected} in", output)
                self.assertNotIn("PRIVATE", output)
                self.assertNotIn("candidate FAIL", output)

    def test_retry_start_and_return_labels_match_actual_attempts_and_json_has_no_human_updates(self):
        from run_evals import run_plan
        self.context.options.transport_retries = 1
        for json_output in (False, True):
            with self.subTest(json_output=json_output), tempfile.TemporaryDirectory() as temp:
                stream = io.StringIO()
                attempts = {}
                def invoke(spec):
                    attempts[spec.workspace] = attempts.get(spec.workspace, 0) + 1
                    if not spec.skill and spec.agent == "eval-target" and attempts[spec.workspace] == 1:
                        return 1, self.context.result(spec, evidence=self.context.evidence(), exit_code=1,
                                                      stderr="provider.no-route Model unavailable")
                    return self.context.invoke(spec)
                self.context.options.artifact_dir = Path(temp) / "run"
                plan = self.context.runner.eval_plan.build_run_plan("attempt-retry", (self.context.case,), select_all=True)
                reporter = EvalReporter(stream=stream, json_output=json_output)
                code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, invoke,
                                         reporter=reporter, report_root=Path(temp))
                reporter.summary(summary, 1, self.context.options.artifact_dir)
                self.assertEqual(code, 0)
                output = stream.getvalue()
                if json_output:
                    self.assertEqual([json.loads(line)["event"] for line in output.splitlines()], ["run-started", "verified-pair", "verified-summary"])
                else:
                    self.assertIn("baseline target attempt 1 returned (reported error)", output)
                    self.assertIn("baseline target attempt 2 returned in", output)
                    self.assertEqual(sum("verification pending." in line and "attempt" in line for line in output.splitlines()), 5)
                    self.assertIn("Observed attempts: 3 target + 2 judge", output)


if __name__ == "__main__":
    unittest.main()
