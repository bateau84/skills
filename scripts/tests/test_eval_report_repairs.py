"""Independent-review regressions through the actual CLI and pinned engine."""
import io
import json
import os
import stat
import shutil
import sys
import tempfile
import unittest
from contextlib import chdir, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import test_eval_integration as integration
from run_evals import main


class ReportRepairTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        integration.PinnedIntegrationTests.setUpClass()

    def setUp(self):
        self.context = integration.PinnedIntegrationTests()
        self.context.setUp()

    def test_explicit_relative_artifact_aliases_are_repository_anchored_in_all_modes(self):
        for alias in ("--artifact-dir", "--output"):
            for flags in ([], ["--verbose"], ["--json"]):
                with self.subTest(alias=alias, flags=flags), tempfile.TemporaryDirectory() as temp:
                    base = Path(temp)
                    root, caller = base / "repository", base / "caller"
                    root.mkdir()
                    caller.mkdir()
                    shutil.copytree(integration.ROOT / "skills" / "product-acceptance", root / "skills" / "product-acceptance")
                    stdout, stderr = io.StringIO(), io.StringIO()
                    with chdir(caller), patch("run_evals.ROOT", root), \
                         patch.dict(os.environ, {"PATH": os.defpath}, clear=True), \
                         patch("run_evals.runner_git_head", return_value="offline-fixture"), \
                         patch("run_evals.verify_image", return_value={"image_id": "sha256:" + "a" * 64}), \
                         patch.object(self.context.runner.cli, "resolve_engine", return_value="podman"), \
                         patch.object(self.context.runner.cli, "default_auth_path", return_value=base / "absent-auth"), \
                         patch.object(self.context.runner.cli, "default_database_path", return_value=base / "absent-db"), \
                         patch.object(self.context.runner.eval_execute, "invoke_once", side_effect=self.context.invoke), \
                         redirect_stdout(stdout), redirect_stderr(stderr):
                        code = main(["--cases", "product-acceptance:PA3", "--model", "test/model",
                                      "--runner-root", str(self.context.runner.root), "--models-catalog",
                                      str(self.context.runner.root / "tests/fixtures/models-catalog.json"), alias, "reports/run", *flags])
                    self.assertEqual(code, 0, stderr.getvalue())
                    self.assertTrue((root / "reports" / "run" / "run.json").is_file())
                    self.assertEqual(list(caller.iterdir()), [])
                    self.assertTrue((root / "EVAL-RESULTS.md").is_file())
                    directory = str(root / "reports" / "run")
                    if "--json" in flags:
                        events = [json.loads(line) for line in stdout.getvalue().splitlines()]
                        self.assertEqual(events[1]["artifact_dir"], directory)
                        self.assertEqual(events[-1]["artifact_dir"], directory)
                        self.assertEqual(events[-1]["report_path"], directory + "/results.md")
                    else:
                        self.assertEqual(stdout.getvalue().count("Run artifacts: " + directory), 2)
                        self.assertIn("Report: " + directory + "/results.md", stdout.getvalue())

    def exercise_failure(self, stage, flags, *, partial=False, tamper=False, setup=False, grade_kind="pass"):
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            root, caller = base / "repository", base / "caller"
            root.mkdir()
            caller.mkdir()
            shutil.copytree(integration.ROOT / "skills" / "product-acceptance", root / "skills" / "product-acceptance")
            destination = root / "reports" / "run"
            stdout, stderr = io.StringIO(), io.StringIO()
            entered = []
            real_open, real_sync, real_replace = os.open, os.fsync, os.replace
            def corrupt_summary():
                if tamper:
                    manifest = json.loads((destination / "run.json").read_text())
                    manifest["summary"]["candidate_passes"] = 99
                    (destination / "run.json").write_text(json.dumps(manifest))
            def invoke(spec):
                entered.append(spec)
                if stage == "collision" and len(entered) == 1:
                    self.assertTrue((destination / ".eval-run-owner.json").is_file())
                    (destination / "results.md").write_text("MANUAL REPORT CONTENT — must remain unchanged\n")
                if partial:
                    raise AssertionError("PRIVATE ORCHESTRATION PAYLOAD")
                if spec.agent == "eval-judge" and grade_kind != "pass":
                    response = "{}" if grade_kind == "non-evidence" else json.dumps(integration.grade(self.context.case.project_data, False))
                    return 0, self.context.result(spec, text=response)
                return self.context.invoke(spec)
            def opened(path, *args, **kwargs):
                if stage == "write" and str(path).startswith(".results-"):
                    corrupt_summary()
                    raise OSError("PRIVATE REPORT WRITE PAYLOAD")
                return real_open(path, *args, **kwargs)
            def synced(fd):
                info = os.fstat(fd)
                per_run_file = stat.S_ISREG(info.st_mode) and "/.results-" in os.readlink(f"/proc/self/fd/{fd}")
                per_run_directory = stat.S_ISDIR(info.st_mode) and destination.exists() and info.st_ino == destination.stat().st_ino
                root_directory = stat.S_ISDIR(info.st_mode) and info.st_ino == root.stat().st_ino
                if stage == "file-sync" and per_run_file or stage == "directory-sync" and per_run_directory and (destination / "results.md").is_file():
                    corrupt_summary()
                    raise OSError("PRIVATE REPORT DURABILITY PAYLOAD")
                if stage == "root-sync" and root_directory:
                    raise OSError("PRIVATE ROOT DURABILITY PAYLOAD")
                return real_sync(fd)
            def replaced(source, target, *args, **kwargs):
                if stage == "root-write" and target == "EVAL-RESULTS.md":
                    raise OSError("PRIVATE ROOT WRITE PAYLOAD")
                return real_replace(source, target, *args, **kwargs)
            validate_profile = self.context.runner.eval_api.validate_eval_profile
            def profile_validated(profile):
                if setup:
                    raise RuntimeError("PRIVATE SETUP PAYLOAD")
                return validate_profile(profile)
            with chdir(caller), patch("run_evals.ROOT", root), \
                 patch.dict(os.environ, {"PATH": os.defpath}, clear=True), \
                 patch("run_evals.runner_git_head", return_value="offline-fixture"), \
                 patch("run_evals.verify_image", return_value={"image_id": "sha256:" + "a" * 64}), \
                 patch.object(self.context.runner.cli, "resolve_engine", return_value="podman"), \
                 patch.object(self.context.runner.cli, "default_auth_path", return_value=base / "absent-auth"), \
                 patch.object(self.context.runner.cli, "default_database_path", return_value=base / "absent-db"), \
                  patch.object(self.context.runner.eval_execute, "invoke_once", side_effect=invoke), \
                 patch.object(self.context.runner.eval_api, "validate_eval_profile", side_effect=profile_validated), \
                 patch("eval_markdown.os.open", side_effect=opened), \
                 patch("eval_markdown.os.fsync", side_effect=synced), \
                 patch("eval_markdown.os.replace", side_effect=replaced), \
                 redirect_stdout(stdout), redirect_stderr(stderr):
                code = main(["--cases", "product-acceptance:PA3", "--model", "test/model",
                              "--runner-root", str(self.context.runner.root), "--models-catalog",
                              str(self.context.runner.root / "tests/fixtures/models-catalog.json"), "--output", "reports/run", *flags])
            self.assertEqual(code, 2)
            self.assertEqual(len(entered), 0 if setup else 1 if partial else 4)
            self.assertNotIn("PRIVATE", stdout.getvalue() + stderr.getvalue())
            self.assertFalse((caller / "reports").exists())
            if stage == "collision":
                self.assertEqual((destination / "results.md").read_text(), "MANUAL REPORT CONTENT — must remain unchanged\n")
            if stage not in {"root-write", "root-sync"}:
                self.assertFalse((root / "EVAL-RESULTS.md").exists())
            self.assertEqual(list(destination.glob(".results-*.tmp")), [])
            return stdout.getvalue(), stderr.getvalue(), json.loads((destination / "run.json").read_text())["summary"], str(destination)

    def test_per_run_publication_failures_preserve_verified_aggregate_in_all_modes(self):
        codes = {"collision": "per_run_report_collision", "write": "per_run_report_write_failed",
                 "file-sync": "per_run_report_durability_failed", "directory-sync": "per_run_report_durability_failed"}
        for stage, failure_code in codes.items():
            for flags in ([], ["--verbose"], ["--json"]):
                with self.subTest(stage=stage, flags=flags):
                    stdout, stderr, durable, directory = self.exercise_failure(stage, flags)
                    self.assertTrue(durable["all_pass"])
                    self.assertIn(failure_code, stderr)
                    self.assertNotIn("no complete run proof", stderr)
                    if "--json" in flags:
                        events = [json.loads(line) for line in stdout.splitlines()]
                        summary = events[-1]
                        self.assertEqual(summary["event"], "verified-summary")
                        self.assertTrue(summary["all_pass"])
                        self.assertTrue(summary["evaluation_finalized"])
                        self.assertEqual(summary["evaluation_exit_code"], 0)
                        self.assertEqual(summary["artifact_dir"], directory)
                        self.assertEqual(summary["report_publication"]["per_run"], "failed")
                        self.assertEqual(summary["report_publication"]["latest"], "not-written")
                        self.assertEqual(summary["report_publication"]["failure"]["code"], failure_code)
                        self.assertNotIn("report_path", summary)
                        self.assertNotIn("latest_report_path", summary)
                        self.assertEqual(summary["pairs"], durable["pairs"])
                    else:
                        self.assertIn("Completed: 1/1 verified pair artifact(s)", stdout)
                        self.assertIn("1 candidate PASS", stdout)
                        self.assertIn("Manifest: " + directory + "/run.json", stdout)
                        self.assertIn("Reports: per-run failed; latest not-written", stdout)
                        self.assertNotIn("\nReport: ", stdout)
                        self.assertNotIn("\nLatest report: ", stdout)

    def test_publication_failure_does_not_promote_tampered_summary(self):
        for flags in ([], ["--verbose"], ["--json"]):
            with self.subTest(flags=flags):
                stdout, stderr, _, _ = self.exercise_failure("write", flags, tamper=True)
                self.assertNotIn("verified-summary", stdout)
                self.assertNotIn("Completed:", stdout)
                self.assertIn("no complete run proof", stderr)

    def test_root_publication_failure_and_partial_evaluation_are_distinguished_in_all_modes(self):
        for stage in ("root-write", "root-sync", "collision", "write"):
            for partial in (False, True):
                for flags in ([], ["--verbose"], ["--json"]):
                    with self.subTest(stage=stage, partial=partial, flags=flags):
                        stdout, stderr, durable, directory = self.exercise_failure(stage, flags, partial=partial)
                        self.assertEqual(durable["all_pass"], not partial)
                        self.assertIn("eval report publication error", stderr)
                        root_failure = stage.startswith("root-")
                        per_run, latest = ("published", "failed") if root_failure else ("failed", "not-written")
                        if "--json" in flags:
                            event = json.loads(stdout.splitlines()[-1])
                            self.assertEqual(event["event"], "verified-summary")
                            self.assertEqual(event["all_pass"], not partial)
                            self.assertEqual(event["evaluation_exit_code"], 2 if partial else 0)
                            self.assertTrue(event["evaluation_finalized"])
                            self.assertEqual(event["candidate_passes"], 0 if partial else 1)
                            self.assertEqual(event["report_publication"]["per_run"], per_run)
                            self.assertEqual(event["report_publication"]["latest"], latest)
                            self.assertEqual("report_path" in event, root_failure)
                            self.assertNotIn("latest_report_path", event)
                        else:
                            self.assertIn("Completed:", stdout)
                            self.assertIn(f"Reports: per-run {per_run}; latest {latest}", stdout)
                            self.assertIn("Manifest: " + directory + "/run.json", stdout)
                            self.assertIn("0 candidate PASS" if partial else "1 candidate PASS", stdout)
                            self.assertEqual("\nReport: " in stdout, root_failure)
                            self.assertNotIn("\nLatest report: ", stdout)

    def test_owned_setup_error_with_failed_report_exposes_only_partial_verified_aggregate(self):
        for flags in ([], ["--verbose"], ["--json"]):
            with self.subTest(flags=flags):
                stdout, stderr, durable, directory = self.exercise_failure("write", flags, setup=True)
                self.assertEqual(durable, {"status": "running"})
                self.assertIn("per_run_report_write_failed", stderr)
                if "--json" in flags:
                    summary = json.loads(stdout.splitlines()[-1])
                    self.assertEqual(summary["event"], "verified-summary")
                    self.assertFalse(summary["evaluation_finalized"])
                    self.assertIsNone(summary["evaluation_exit_code"])
                    self.assertFalse(summary["all_pass"])
                    self.assertEqual(summary["pairs"], [])
                    self.assertNotIn("report_path", summary)
                else:
                    self.assertIn("Partial: 0/1 verified pair artifact(s)", stdout)
                    self.assertIn("incomplete; no complete run proof", stdout)
                    self.assertIn("Manifest: " + directory + "/run.json", stdout)

    def test_failed_report_does_not_change_negative_or_non_evidence_evaluation_exit(self):
        for kind in ("negative", "non-evidence"):
            for flags in ([], ["--verbose"], ["--json"]):
                with self.subTest(kind=kind, flags=flags):
                    stdout, _, durable, _ = self.exercise_failure("write", flags, grade_kind=kind)
                    self.assertFalse(durable["all_pass"])
                    if "--json" in flags:
                        summary = json.loads(stdout.splitlines()[-1])
                        self.assertEqual(summary["evaluation_exit_code"], 1)
                        self.assertEqual(summary["pairs"], durable["pairs"])
                    else:
                        self.assertIn("finalized; evaluation exit 1", stdout)


if __name__ == "__main__":
    unittest.main()
