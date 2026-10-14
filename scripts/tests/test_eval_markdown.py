"""Provider-free report tests through the pinned engine and owned storage."""
import copy
import io
import html
import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import redirect_stderr, redirect_stdout
from unittest.mock import patch
from urllib.parse import unquote

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import test_eval_integration as integration
from eval_markdown import ReportPublicationError, publish_report, markdown_text
from eval_profile import SkillsProfile, SkillsComparison
from eval_reporting import EvalReporter
from run_evals import run_plan, summarize, main


class MarkdownTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        integration.PinnedIntegrationTests.setUpClass()

    def setUp(self):
        self.context = integration.PinnedIntegrationTests()
        self.context.setUp()

    def run_fixture(self, directory, invoke=None, cases=None, iterations=1, parallel=1, reporter=None):
        options = self.context.options
        options.artifact_dir = directory
        options.iterations, options.parallel = iterations, parallel
        # Do not inventory real host credentials in synthetic tests. These absent,
        # test-owned seeds exercise the real scanner's missing-source behavior.
        options.auth = directory.parent / "absent-auth"
        options.database = directory.parent / "absent-db"
        options.models_catalog = directory.parent / "absent-models"
        plan = self.context.runner.eval_plan.build_run_plan("markdown-fixture", cases or (self.context.case,),
                    select_all=True, iterations=iterations, runtime_parallelism=parallel)
        code, summary = run_plan(integration.ROOT, self.context.runner, options, plan, {}, invoke or self.context.invoke,
                                 reporter=reporter, report_root=directory.parent)
        self.assertTrue((directory.parent / "EVAL-RESULTS.md").is_file())
        store = self.context.runner.eval_artifacts.RunArtifactStore(directory, plan.run_id)
        identities = [self.context.runner.eval_artifacts.artifact_identity_for_job(plan.run_id, j) for j in plan.jobs]
        return code, summary, store, identities, (directory / "results.md").read_text()

    def test_run_automatically_publishes_private_report_from_verified_artifacts(self):
        with tempfile.TemporaryDirectory() as temp:
            self.context.options.artifact_dir = Path(temp) / "run"
            plan = self.context.runner.eval_plan.build_run_plan("markdown-fixture", (self.context.case,), select_all=True)
            code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {}, self.context.invoke, report_root=Path(temp))
            report = self.context.options.artifact_dir / "results.md"
            self.assertTrue(report.is_file())
            self.assertEqual(report.stat().st_mode & 0o777, 0o600)
            text = report.read_text()
            self.assertEqual(code, 0)
            self.assertIn("Candidate absolute results", text)
            self.assertIn("Paired comparison", text)
            self.assertIn("PASS 100%", text)
            self.assertIn("2 target + 2 judge", text)
            self.assertIn(summary["pairs"][0]["paired_artifact_evidence_id"], text)
            self.assertIn("test/model", text)
            self.assertNotIn("Practical first response", text)

    def test_compound_negative_and_baseline_fail_candidate_pass_preserve_policy(self):
        for candidate_pass in (False, True):
            with self.subTest(candidate_pass=candidate_pass), tempfile.TemporaryDirectory() as temp:
                judges = 0
                def invoke(spec):
                    nonlocal judges
                    if spec.agent == "eval-judge":
                        judges += 1
                        grade = integration.grade(self.context.case.project_data, candidate_pass and judges == 2)
                        grade["expectations"][0]["evidence"] = "Missing provenance, but routing evidence remains valid."
                        return 0, self.context.result(spec, text=json.dumps(grade))
                    return self.context.invoke(spec)
                code, summary, _, _, text = self.run_fixture(Path(temp) / "run", invoke)
                self.assertEqual(code, 0 if candidate_pass else 1)
                self.assertIn("1/1 positive criteria unmet", text)
                self.assertIn("Missing provenance, but routing evidence remains valid.", text)
                self.assertIn("Zero is a criterion-level score", text)
                self.assertIn("material-improvement" if candidate_pass else "neutral", text)
                self.assertEqual(summary["candidate_passes"], int(candidate_pass))

    def test_non_evidence_runtime_reason_and_treatment_failure_not_fake_score(self):
        for kind in ("runtime", "native", "capture", "judge"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                def invoke(spec):
                    if kind == "runtime":
                        result = self.context.result(spec, exit_code=1)
                        result["stdout"] = json.dumps({"type": "error", "error": {"message": "Invalid model reference: test"}})
                        return 0, result
                    if kind == "judge" and spec.agent == "eval-judge":
                        return 0, self.context.result(spec, text="{}")
                    if spec.skill:
                        return 0, self.context.result(spec, evidence=self.context.evidence(ended=kind != "capture"))
                    return self.context.invoke(spec)
                code, _, _, _, text = self.run_fixture(Path(temp) / "run", invoke)
                self.assertEqual(code, 1)
                if kind == "native":
                    self.assertIn("FAIL 100%", text)
                    self.assertIn("unattributed", text)
                    self.assertNotIn("(+100.0 pp)", text)
                else:
                    self.assertIn("NON-EVIDENCE score unavailable", text)
                    self.assertNotIn("NON-EVIDENCE 0%", text)
                    self.assertIn({"runtime": "Invalid model reference", "capture": "evidence_incomplete",
                                   "judge": "judge_contract_invalid"}[kind], html.unescape(text))

    def test_host_callbacks_remain_private_in_report_even_when_raw_json_contains_secret(self):
        secret = "fictional-private-host-callback-12345"
        for callback, owner in (("deterministic_checks", SkillsProfile), ("judge_spec", SkillsProfile),
                                ("parse_judge", SkillsProfile), ("compare_pair", SkillsComparison)):
            with self.subTest(callback=callback), tempfile.TemporaryDirectory() as temp, \
                 patch.object(owner, callback, side_effect=RuntimeError(secret)):
                code, _, store, identities, text = self.run_fixture(Path(temp) / "run")
                self.assertEqual(code, 1)
                self.assertIn(secret, json.dumps(store.read_paired_job_artifact(identities[0])))
                self.assertNotIn(secret, text)
                self.assertIn("withheld", text)

    def test_partial_parallel_results_are_in_plan_order_without_invented_pass(self):
        import threading
        ready = threading.Event()
        first = self.context.case
        second = next(c for c in self.context.candidate.discover_cases() if c.id == "SKILL-product-acceptance-PA4")
        def invoke(spec):
            if first.project_data["prompt"] in spec.prompt:
                if not ready.wait(5):
                    raise AssertionError("fixture synchronization timed out")
                raise AssertionError("PRIVATE ORCHESTRATION MESSAGE")
            result = self.context.result(spec)
            if spec.agent == "eval-judge":
                ready.set()
            return 0, result
        with tempfile.TemporaryDirectory() as temp:
            code, summary, _, _, text = self.run_fixture(Path(temp) / "run", invoke, (first, second), parallel=2)
            self.assertEqual(code, 2)
            self.assertEqual(len(summary["pairs"]), 1)
            rows = [line for line in text.splitlines() if line.startswith("| SKILL-")]
            self.assertIn("PA3", rows[0])
            self.assertIn("unavailable | unavailable", rows[0])
            self.assertIn("PA4", rows[1])
            self.assertIn("PASS 100%", rows[1])
            self.assertIn("partial; failed jobs may have additional", text)
            self.assertNotIn("PRIVATE ORCHESTRATION", text)

    def test_pre_execution_profile_failure_after_ownership_reports_incomplete(self):
        for json_output in (False, True):
            with self.subTest(json_output=json_output), tempfile.TemporaryDirectory() as temp:
                destination = Path(temp) / "run"
                output = io.StringIO()
                reporter = EvalReporter(json_output=json_output, stream=output)
                with patch.object(self.context.runner.eval_api, "validate_eval_profile", side_effect=RuntimeError("PRIVATE SETUP")):
                    with self.assertRaises(RuntimeError):
                        self.run_fixture(destination, reporter=reporter)
                text = (destination / "results.md").read_text()
                self.assertIn("INCOMPLETE", text)
                self.assertIn("unavailable | unavailable", text)
                self.assertNotIn("PASS 100%", text)
                self.assertNotIn("PRIVATE SETUP", text)
                if json_output:
                    events = [json.loads(line) for line in output.getvalue().splitlines()]
                    self.assertEqual([e["event"] for e in events], ["run-started", "results-report"])
                    self.assertEqual(events[-1], {"event": "results-report", "report_path": str(destination / "results.md"),
                                                 "artifact_dir": str(destination), "latest_report_path": str(Path(temp) / "EVAL-RESULTS.md")})
                else:
                    self.assertEqual(output.getvalue().count("Report: " + str(destination / "results.md")), 1)
                    self.assertTrue(output.getvalue().endswith("Latest report: " + str(Path(temp) / "EVAL-RESULTS.md") + "\n"))
                self.assertEqual(self.context.calls, [])

    def test_report_rejects_pair_and_summary_tampering_before_rendering(self):
        for tamper in ("pair", "summary"):
            with self.subTest(tamper=tamper), tempfile.TemporaryDirectory() as temp:
                _, _, store, identities, _ = self.run_fixture(Path(temp) / "run")
                (store.root / "results.md").unlink()  # only fresh test-owned output
                expected = store.read_run_manifest()
                if tamper == "pair":
                    artifact = store.read_paired_job_artifact(identities[0])
                    artifact["sides"]["candidate"]["classification"] = "fail"
                    store.paired_job_path(identities[0]).write_text(json.dumps(artifact))
                else:
                    expected["summary"]["candidate_passes"] = 99
                    store.write_run_manifest(expected)  # schema-valid but false summary
                with self.assertRaises(Exception):
                    publish_report(self.context.runner, store, identities, expected, summarize,
                                   self.context.runner.evidence_safety.Sanitizer())
                self.assertFalse((store.root / "results.md").exists())

    def test_no_overwrite_report_collision_symlink_and_old_run(self):
        with tempfile.TemporaryDirectory() as temp:
            _, _, store, identities, original = self.run_fixture(Path(temp) / "run")
            before = {p: p.read_bytes() for p in store.root.rglob("*.json")}
            sanitizer = self.context.runner.evidence_safety.Sanitizer()
            with self.assertRaises(ReportPublicationError) as collision:
                publish_report(self.context.runner, store, identities, store.read_run_manifest(), summarize, sanitizer)
            self.assertEqual(collision.exception.code, "per_run_report_collision")
            self.assertEqual((store.root / "results.md").read_text(), original)
            with self.assertRaises(ValueError):
                self.run_fixture(store.root)
            self.assertEqual({p: p.read_bytes() for p in before}, before)
            (store.root / "results.md").unlink()
            outside = Path(temp) / "outside.md"
            outside.write_text("untouched")
            (store.root / "results.md").symlink_to(outside)
            with self.assertRaises(ReportPublicationError) as collision:
                publish_report(self.context.runner, store, identities, store.read_run_manifest(), summarize, sanitizer)
            self.assertEqual(collision.exception.code, "per_run_report_collision")
            self.assertEqual(outside.read_text(), "untouched")
            self.assertEqual(list(store.root.glob(".results-*.tmp")), [])

    def test_symlink_run_path_is_rejected_before_ownership_or_calls(self):
        with tempfile.TemporaryDirectory() as temp:
            outside = Path(temp) / "outside"
            outside.mkdir()
            linked = Path(temp) / "linked"
            linked.symlink_to(outside, target_is_directory=True)
            with self.assertRaises(ValueError):
                self.run_fixture(linked / "run")
            self.assertEqual(list(outside.iterdir()), [])
            self.assertEqual(self.context.calls, [])

    def test_symlink_evidence_and_changed_owner_cannot_publish_outside_owned_run(self):
        for attack in ("evidence", "owner"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory() as temp:
                _, _, store, identities, _ = self.run_fixture(Path(temp) / "run")
                (store.root / "results.md").unlink()
                expected = store.read_run_manifest()
                if attack == "evidence":
                    artifact = store.paired_job_path(identities[0])
                    outside = Path(temp) / "outside.json"
                    outside.write_bytes(artifact.read_bytes())
                    artifact.unlink()
                    artifact.symlink_to(outside)
                else:
                    store.owner_path.write_text(json.dumps({"run_id": "another-run"}))
                with self.assertRaises(self.context.runner.eval_artifacts.EvalArtifactError):
                    publish_report(self.context.runner, store, identities, expected, summarize,
                                   self.context.runner.evidence_safety.Sanitizer())
                self.assertFalse((store.root / "results.md").exists())

    def test_observed_retry_budget_and_trap_policy_are_not_new_experiments(self):
        self.context.options.transport_retries = 1
        attempts = {}
        def invoke(spec):
            attempts[spec.workspace] = attempts.get(spec.workspace, 0) + 1
            if spec.agent == "eval-target" and not spec.skill and attempts[spec.workspace] == 1:
                return 1, self.context.result(spec, evidence=self.context.evidence(), exit_code=1,
                                              stderr="provider.no-route Model unavailable")
            return self.context.invoke(spec)
        with tempfile.TemporaryDirectory() as temp:
            _, _, _, _, text = self.run_fixture(Path(temp) / "run", invoke)
            self.assertIn("3 target + 2 judge", text)
            self.assertIn("Planned nominal: 2 target + 2 judge; maximum: 4 target + 4 judge", text)
            self.assertEqual(sum(attempts.values()), 5)
        self.context.options.transport_retries = 0
        self.context.case = next(c for c in self.context.candidate.discover_cases()
                                 if c.id == "SKILL-software-engineering-SoftwareEngineering-01")
        judges = 0
        def invoke_trap(spec):
            nonlocal judges
            if spec.agent == "eval-judge":
                judges += 1
                grade = integration.grade(self.context.case.project_data)
                if judges == 1:
                    grade["trap_observed"] = True
                    grade["passed"] = False
                return 0, self.context.result(spec, text=json.dumps(grade))
            return self.context.invoke(spec)
        with tempfile.TemporaryDirectory() as temp:
            code, _, _, _, text = self.run_fixture(Path(temp) / "run", invoke_trap)
            self.assertEqual(code, 0)
            self.assertIn("material-improvement (+10.0 pp)", html.unescape(text))
            self.assertIn("Trap: fixed in this pair", html.unescape(text))
            self.assertIn("not statistical significance", text)

    def test_hostile_case_identity_and_metadata_do_not_manufacture_markdown_links(self):
        from dataclasses import replace
        hostile = 'case\n# Fake PASS | [link](https://evil) <img src=x>\u202e'
        case = replace(self.context.case, id=hostile, selectors=(hostile,))
        with tempfile.TemporaryDirectory() as temp:
            code, _, store, _, text = self.run_fixture(Path(temp) / "run", cases=(case,))
            self.assertEqual(code, 0)
            self.assertNotIn("# Fake PASS", text)
            self.assertNotIn("<img", text)
            self.assertNotIn("[link]", text)
            rows = [line for line in text.splitlines() if line.startswith("| case")]
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0].count("|"), 6)
            for destination in re.findall(r"\]\(([^)]+)\)", text):
                self.assertTrue((store.root / unquote(destination)).is_file())

    def test_markdown_hostile_rationale_is_bounded_safe_and_known_credentials_redacted(self):
        hostile = '\n# Forged PASS\n| fake | [click](https://evil) <script>bad</script> `code`\x1b[31m\u202e' + 'z' * 10000
        sanitizer = self.context.runner.evidence_safety.Sanitizer(("inventoried-secret",))
        projected = markdown_text(hostile + "inventoried-secret", sanitizer)
        self.assertNotIn("\n", projected)
        self.assertNotIn("<script>", projected)
        self.assertNotIn("[click]", projected)
        self.assertNotIn("|", projected)
        self.assertNotIn("\x1b", projected)
        self.assertNotIn("\u202e", projected)
        self.assertLess(len(projected), 1000)
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ, {"REPORT_SECRET_TOKEN": "inventoried-secret"}):
            self.context.options.model = "inventoried-secret"
            def invoke(spec):
                if spec.agent == "eval-judge":
                    grade = integration.grade(self.context.case.project_data, False)
                    grade["expectations"][0]["evidence"] = hostile
                    return 0, self.context.result(spec, text=json.dumps(grade))
                return self.context.invoke(spec)
            _, _, _, _, text = self.run_fixture(Path(temp) / "run", invoke)
            self.assertNotIn("inventoried-secret", text)
            self.assertNotIn("# Forged", text)
            self.assertNotIn("<script>", text)
            self.assertNotIn("[click]", text)
            self.assertEqual(text.count("| Case / iteration |"), 1)

    def test_publication_is_deterministic_and_links_resolve_to_actual_json(self):
        with tempfile.TemporaryDirectory() as temp:
            _, _, store, identities, first = self.run_fixture(Path(temp) / "run", iterations=2, parallel=2)
            (store.root / "results.md").unlink()
            publish_report(self.context.runner, store, identities, store.read_run_manifest(), summarize,
                           self.context.runner.evidence_safety.Sanitizer())
            self.assertEqual((store.root / "results.md").read_text(), first)
            for destination in re.findall(r"\]\(([^)]+)\)", first):
                target = store.root / unquote(destination)
                self.assertTrue(target.is_file())
                self.assertTrue(target.resolve().is_relative_to(store.root))
            rows = [line for line in first.splitlines() if line.startswith("| SKILL-")]
            self.assertIn(" / 1 |", rows[0])
            self.assertIn(" / 2 |", rows[1])

    def test_cli_error_before_ownership_has_no_report_or_fake_execution(self):
        with tempfile.TemporaryDirectory() as temp, redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), \
             patch("run_evals.load_runner") as loader:
            destination = Path(temp) / "run"
            self.assertEqual(main(["--cases", "product-acceptance:PA3", "--artifact-dir", str(destination)], report_root=Path(temp)), 2)
            loader.assert_not_called()
            self.assertFalse(destination.exists())

    def test_complete_selected_suite_parallel_cli_report_has_every_case_iteration(self):
        cases = tuple(c for c in self.context.candidate.discover_cases() if c.project_data["skill"] == "product-acceptance")
        by_prompt = {c.project_data["prompt"]: c for c in cases}
        def invoke(spec):
            if spec.agent == "eval-judge":
                packet = json.loads(spec.prompt.split("UNTRUSTED SCENARIO/RESPONSE AND RUBRIC DATA:\n", 1)[1])
                case = by_prompt[packet["scenario"]]
                return 0, self.context.result(spec, text=json.dumps(integration.grade(case.project_data)))
            return self.context.invoke(spec)
        with tempfile.TemporaryDirectory() as temp:
            destination = Path(temp) / "run"
            stdout, stderr = io.StringIO(), io.StringIO()
            with patch.dict(os.environ, {"PATH": os.defpath}, clear=True), \
                 patch("run_evals.verify_image", return_value={"image_id": "sha256:" + "a" * 64}), \
                 patch.object(self.context.runner.cli, "resolve_engine", return_value="podman"), \
                 patch.object(self.context.runner.eval_execute, "invoke_once", side_effect=invoke), \
                 redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(["--all", "--target", "product-acceptance", "--iterations", "2", "--parallel", "3",
                             "--model", "test/model", "--artifact-dir", str(destination), "--json"], report_root=Path(temp))
            self.assertEqual(code, 0, stderr.getvalue())
            text = (destination / "results.md").read_text()
            rows = [line for line in text.splitlines() if line.startswith("| SKILL-")]
            self.assertEqual(len(rows), len(cases) * 2)
            self.assertIn("18/18", text)
            self.assertIn("36 target + 36 judge", text)
            events = [json.loads(line) for line in stdout.getvalue().splitlines()]
            self.assertEqual(events[-1]["report_path"], str(destination / "results.md"))
            self.assertEqual(len(events[-1]["pairs"]), 18)
            manifest = json.loads((destination / "run.json").read_text())
            for row, job in zip(rows, manifest["jobs"], strict=True):
                self.assertIn(f"{job['case']} / {job['iteration']}", row)

    def test_main_negative_non_evidence_and_orchestration_modes_always_locate_report(self):
        for kind, expected in (("negative", 1), ("non-evidence", 1), ("orchestration", 2)):
            for flags in ([], ["--verbose"], ["--json"]):
                with self.subTest(kind=kind, flags=flags), tempfile.TemporaryDirectory() as temp:
                    destination = Path(temp) / "run"
                    stdout, stderr = io.StringIO(), io.StringIO()
                    def invoke(spec):
                        if kind == "orchestration":
                            raise AssertionError("PRIVATE ORCHESTRATION")
                        if spec.agent == "eval-judge":
                            text = "{}" if kind == "non-evidence" else json.dumps(integration.grade(self.context.case.project_data, False))
                            return 0, self.context.result(spec, text=text)
                        return self.context.invoke(spec)
                    with patch.dict(os.environ, {"PATH": os.defpath}, clear=True), \
                         patch("run_evals.verify_image", return_value={"image_id": "sha256:" + "a" * 64}), \
                         patch.object(self.context.runner.cli, "resolve_engine", return_value="podman"), \
                         patch.object(self.context.runner.eval_execute, "invoke_once", side_effect=invoke), \
                         redirect_stdout(stdout), redirect_stderr(stderr):
                        code = main(["--cases", "product-acceptance:PA3", "--model", "test/model", "--artifact-dir", str(destination), *flags], report_root=Path(temp))
                    self.assertEqual(code, expected, stderr.getvalue())
                    self.assertTrue((destination / "results.md").is_file())
                    self.assertNotIn("PRIVATE ORCHESTRATION", (destination / "results.md").read_text())
                    if "--json" in flags:
                        events = [json.loads(line) for line in stdout.getvalue().splitlines()]
                        self.assertEqual(events[-1]["event"], "verified-summary")
                        self.assertEqual(events[-1]["report_path"], str(destination / "results.md"))
                        self.assertFalse(events[-1]["all_pass"])
                        self.assertEqual(events[-1]["candidate_passes"], 0)
                    else:
                        self.assertEqual(stdout.getvalue().count("Report: "), 1)
                        self.assertTrue(stdout.getvalue().endswith("Latest report: " + str(Path(temp) / "EVAL-RESULTS.md") + "\n"))

    def test_atomic_publication_fsyncs_file_and_directory_and_cleans_failed_temp(self):
        from eval_markdown import _publish_text
        with tempfile.TemporaryDirectory() as temp:
            store = self.context.runner.eval_artifacts.claim_run_artifact_directory(Path(temp) / "run", "publication-fixture")
            fsync = os.fsync
            with patch("eval_markdown.os.fsync", wraps=fsync) as sync:
                _publish_text(store, "# fixture\n")
                self.assertEqual(sync.call_count, 2)
            (store.root / "results.md").unlink()
            with patch("eval_markdown.os.link", side_effect=OSError("fixture publication failure")):
                with self.assertRaises(ReportPublicationError) as failed:
                    _publish_text(store, "# fixture\n")
                self.assertEqual(failed.exception.code, "per_run_report_write_failed")
            self.assertFalse((store.root / "results.md").exists())
            self.assertEqual(list(store.root.glob(".results-*.tmp")), [])

    def test_credential_inventory_failure_withholds_metadata_not_execution_truth(self):
        with tempfile.TemporaryDirectory() as temp:
            _, _, store, identities, _ = self.run_fixture(Path(temp) / "run")
            (store.root / "results.md").unlink()
            publish_report(self.context.runner, store, identities, store.read_run_manifest(), summarize,
                           self.context.runner.evidence_safety.Sanitizer(inventory_complete=False))
            text = (store.root / "results.md").read_text()
            self.assertNotIn("test/model", text)
            self.assertNotIn("SKILL-product-acceptance", text)
            self.assertIn("PASS 100%", text)

    def test_replay_saved_live_artifacts_is_fresh_owned_copy_not_new_run_or_history_mutation(self):
        from types import SimpleNamespace
        # Known existing PA3 evidence is an optional read-only integration input,
        # not required checked-in fixture bytes and never a destination to repair.
        runs = ("b37e2e84878c4d93b39d13297c37795e", "a18ce3576b5c4ffbb96e42c8df94dc3f", "c41bc593f7984c84b9cedb9c7e0b691c")
        found = 0
        for run_id in runs:
            original = integration.ROOT / ".skill-evals" / run_id
            if not (original / "run.json").is_file():
                continue
            found += 1
            source = self.context.runner.eval_artifacts.RunArtifactStore(original, run_id)
            manifest = source.read_run_manifest()
            before = {p: p.read_bytes() for p in original.rglob("*") if p.is_file()}
            with tempfile.TemporaryDirectory() as temp:
                store = self.context.runner.eval_artifacts.claim_run_artifact_directory(Path(temp) / "replay", run_id)
                identities, artifacts = [], []
                for job in manifest["jobs"]:
                    identity = self.context.runner.eval_artifacts.artifact_identity_for_job(run_id,
                                    SimpleNamespace(case=SimpleNamespace(id=job["case"]), iteration=job["iteration"]))
                    artifact = source.read_paired_job_artifact(identity)
                    identities.append(identity)
                    artifacts.append(artifact)
                    store.write_paired_job_artifact(identity, artifact)
                copied = copy.deepcopy(manifest)
                copied["project_metadata"]["replay"] = True
                copied["project_metadata"]["report_controls"] = artifacts[0]["sides"]["candidate"]["project_metadata"]["controls"]
                copied["summary"] = summarize(self.context.runner, artifacts)
                copied["summary"]["orchestration_errors"] = []
                store.write_run_manifest(copied)
                publish_report(self.context.runner, store, identities, copied, summarize,
                               self.context.runner.evidence_safety.Sanitizer())
                text = (store.root / "results.md").read_text()
                self.assertIn("Replay of saved evidence, not a new evaluation run", text)
                for artifact in artifacts:
                    self.assertIn(artifact["paired_artifact_evidence_id"], text)
                    for side in ("baseline", "candidate"):
                        self.assertIn(artifact["sides"][side]["classification"].upper(), text)
                if os.environ.get("SKILLS_EVAL_TEST_PRINT_REPLAY") == "1":
                    print("READ-ONLY SAVED-EVIDENCE REPLAY EXCERPT (not a new model run):")
                    print("\n".join(line for line in text.splitlines() if line.startswith("| SKILL-") or
                                    "criterion-level" in line or "candidate E1" in line or "Invalid model reference" in line))
            self.assertEqual({p: p.read_bytes() for p in before}, before)
        if not found:
            # The defining report path is covered by mandatory synthetic tests;
            # absence of private local history is not a product test dependency.
            self.assertEqual(self.context.calls, [])


if __name__ == "__main__":
    unittest.main()
