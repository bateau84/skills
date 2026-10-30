"""Latest-report and visible-location regressions; injected invocation I/O only."""
import copy
import fcntl
import hashlib
import html
import io
import json
import os
import re
import shutil
import stat
import sys
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from contextlib import chdir, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import test_eval_integration as integration
from eval_markdown import LatestReportError, publish_report
from eval_profile import SkillsProfile
from eval_reporting import EvalReporter
from run_evals import main, run_plan, run_probe, summarize


class LatestReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        integration.PinnedIntegrationTests.setUpClass()

    def setUp(self):
        self.context = integration.PinnedIntegrationTests()
        self.context.setUp()

    def run_fixture(self, root, run_id, *, destination=None, invoke=None, reporter=None):
        options = copy.copy(self.context.options)
        options.artifact_dir = destination or root / ".skill-evals" / run_id
        options.auth, options.database, options.models_catalog = (root / "absent-auth", root / "absent-db", root / "absent-models")
        plan = self.context.runner.eval_plan.build_run_plan(run_id, (self.context.case,), select_all=True)
        code, summary = run_plan(integration.ROOT, self.context.runner, options, plan, {}, invoke or self.context.invoke,
                                 reporter=reporter, report_root=root)
        store = self.context.runner.eval_artifacts.RunArtifactStore(options.artifact_dir, run_id)
        identities = [self.context.runner.eval_artifacts.artifact_identity_for_job(run_id, j) for j in plan.jobs]
        return code, summary, store, identities

    def assert_links_exist(self, report):
        destinations = re.findall(r"\]\(([^)]+)\)", report.read_text())
        self.assertGreaterEqual(len(destinations), 2)
        for destination in destinations:
            self.assertTrue((report.parent / unquote(destination)).is_file(), destination)

    def test_completed_run_writes_latest_beside_readme_without_losing_history(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("Offline fixture repository\n")
            self.context.options.artifact_dir = root / ".skill-evals" / "fixture"
            plan = self.context.runner.eval_plan.build_run_plan("latest-fixture", (self.context.case,), select_all=True)
            synced = set()
            real_sync = os.fsync
            def sync(fd):
                info = os.fstat(fd)
                synced.add((stat.S_IFMT(info.st_mode), info.st_ino))
                return real_sync(fd)
            with patch("eval_markdown.os.fsync", side_effect=sync):
                code, summary = run_plan(integration.ROOT, self.context.runner, self.context.options, plan, {},
                                         self.context.invoke, report_root=root)
            self.assertEqual(code, 0)
            latest = root / "EVAL-RESULTS.md"
            self.assertTrue(latest.is_file())
            self.assertEqual(latest.stat().st_mode & 0o777, 0o600)
            self.assertIn((stat.S_IFREG, latest.stat().st_ino), synced)
            self.assertIn((stat.S_IFDIR, root.stat().st_ino), synced)
            text = latest.read_text()
            self.assertIn(".skill-evals/fixture/pairs/", text)
            self.assertIn(summary["pairs"][0]["paired_artifact_evidence_id"], text)
            self.assertTrue((self.context.options.artifact_dir / "results.md").is_file())
            self.assertTrue((self.context.options.artifact_dir / "run.json").is_file())
            self.assertEqual(len(self.context.calls), 4)

    def test_latest_replacement_preserves_every_previous_run_byte(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, first, _ = self.run_fixture(root, "first")
            before = {p: p.read_bytes() for p in first.root.rglob("*") if p.is_file()}
            old_latest = (root / "EVAL-RESULTS.md").read_bytes()
            _, _, second, _ = self.run_fixture(root, "second")
            self.assertNotEqual((root / "EVAL-RESULTS.md").read_bytes(), old_latest)
            self.assertIn("- Run: second", (root / "EVAL-RESULTS.md").read_text())
            self.assertEqual({p: p.read_bytes() for p in before}, before)
            for report in (root / "EVAL-RESULTS.md", first.root / "results.md", second.root / "results.md"):
                self.assertEqual(report.stat().st_mode & 0o777, 0o600)
                self.assert_links_exist(report)
            self.assertEqual(len(self.context.calls), 8)

    def test_root_links_rebase_external_artifact_dir_without_rewriting_rationale(self):
        rationale = "Literal results.md and pairs/case-SKILL-product-acceptance-PA3 are rationale text, not links."
        def invoke(spec):
            if spec.agent == "eval-judge":
                grade = integration.grade(self.context.case.project_data, False)
                grade["expectations"][0]["evidence"] = rationale
                return 0, self.context.result(spec, text=json.dumps(grade))
            return self.context.invoke(spec)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            destination = Path(temp) / "external [artifact] dir" / "run"
            code, _, store, _ = self.run_fixture(root, "external", destination=destination, invoke=invoke)
            self.assertEqual(code, 1)
            latest = root / "EVAL-RESULTS.md"
            self.assertIn("../external%20%5Bartifact%5D%20dir/run/pairs/", latest.read_text())
            self.assertIn(rationale, html.unescape(latest.read_text()))
            self.assertIn(rationale, html.unescape((store.root / "results.md").read_text()))
            self.assert_links_exist(latest)
            self.assert_links_exist(store.root / "results.md")

    def test_unsafe_or_manual_root_content_is_rejected_before_invocations(self):
        for kind in ("manual", "symlink", "directory", "fifo", "hardlink", "edited-generated", "forged-marker", "unsafe-lock"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                latest = root / "EVAL-RESULTS.md"
                outside = root / "outside"
                outside.write_text("manual private content")
                if kind == "symlink":
                    latest.symlink_to(outside)
                elif kind == "directory":
                    latest.mkdir()
                elif kind == "fifo":
                    os.mkfifo(latest)
                elif kind == "hardlink":
                    os.link(outside, latest)
                elif kind == "unsafe-lock":
                    (root / ".EVAL-RESULTS.lock").symlink_to(outside)
                elif kind == "edited-generated":
                    self.run_fixture(root, "previous")
                    latest.write_text(latest.read_text() + "Manual annotation\n")
                elif kind == "forged-marker":
                    body = b"Manually authored text with a matching checksum\n"
                    latest.write_bytes(f"<!-- portable-skills/eval-latest/v1 sha256={hashlib.sha256(body).hexdigest()} -->\n".encode() + body)
                else:
                    latest.write_text("# My manually maintained results\n")
                before = latest.read_bytes() if kind in {"manual", "hardlink", "edited-generated", "forged-marker"} else None
                calls = len(self.context.calls)
                with self.assertRaises(LatestReportError):
                    self.run_fixture(root, "refused")
                self.assertEqual(len(self.context.calls), calls)
                self.assertFalse((root / ".skill-evals" / "refused").exists())
                self.assertEqual(outside.read_text(), "manual private content")
                if before is not None:
                    self.assertEqual(latest.read_bytes(), before)
                if kind == "symlink":
                    self.assertTrue(latest.is_symlink())

    def test_root_changed_after_preflight_retains_owned_report_and_clear_failure(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            stream = io.StringIO()
            changed = False
            def invoke(spec):
                nonlocal changed
                if not changed:
                    changed = True
                    (root / "EVAL-RESULTS.md").write_text("Manual content added during invocation\n")
                return self.context.invoke(spec)
            with self.assertRaisesRegex(LatestReportError, "not an unmodified generated report") as raised:
                self.run_fixture(root, "late-conflict", invoke=invoke, reporter=EvalReporter(json_output=True, stream=stream))
            self.assertEqual((root / "EVAL-RESULTS.md").read_text(), "Manual content added during invocation\n")
            self.assertEqual(raised.exception.retained_report, root / ".skill-evals" / "late-conflict" / "results.md")
            self.assertTrue(raised.exception.retained_report.is_file())
            events = [json.loads(line) for line in stream.getvalue().splitlines()]
            self.assertEqual(events[-1]["event"], "verified-summary")
            self.assertTrue(events[-1]["all_pass"])
            self.assertEqual(events[-1]["report_publication"]["per_run"], "published")
            self.assertEqual(events[-1]["report_publication"]["latest"], "failed")
            self.assertEqual(events[-1]["report_path"], str(raised.exception.retained_report))
            self.assertNotIn("latest_report_path", events[-1])
            self.assertEqual(events[-1]["artifact_dir"], str(raised.exception.retained_report.parent))
            self.assertEqual(len(self.context.calls), 4)

    def test_tampered_pair_or_false_summary_cannot_update_latest(self):
        for kind in ("pair", "summary"):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                _, _, store, identities = self.run_fixture(root, "tamper-test")
                before = (root / "EVAL-RESULTS.md").read_bytes()
                (store.root / "results.md").unlink()  # only fresh test-owned reports
                manifest = store.read_run_manifest()
                if kind == "pair":
                    pair = store.read_paired_job_artifact(identities[0])
                    pair["sides"]["candidate"]["classification"] = "fail"
                    store.paired_job_path(identities[0]).write_text(json.dumps(pair))
                else:
                    manifest["summary"]["candidate_passes"] = 99
                    store.write_run_manifest(manifest)
                with self.assertRaises(Exception):
                    publish_report(self.context.runner, store, identities, manifest, summarize,
                                   self.context.runner.evidence_safety.Sanitizer(), latest_root=root)
                self.assertEqual((root / "EVAL-RESULTS.md").read_bytes(), before)
                self.assertFalse((store.root / "results.md").exists())

    def test_root_atomic_failure_preserves_old_latest_and_new_per_run_report(self):
        for stage in ("replace", "directory-sync"):
            with self.subTest(stage=stage), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                self.run_fixture(root, "previous")
                before = (root / "EVAL-RESULTS.md").read_bytes()
                real_replace, real_sync = os.replace, os.fsync
                def fail_latest(source, destination, *args, **kwargs):
                    if stage == "replace" and destination == "EVAL-RESULTS.md":
                        raise OSError("PRIVATE FILESYSTEM DIAGNOSTIC")
                    return real_replace(source, destination, *args, **kwargs)
                def fail_sync(fd):
                    info = os.fstat(fd)
                    if stage == "directory-sync" and stat.S_ISDIR(info.st_mode) and info.st_ino == root.stat().st_ino:
                        raise OSError("PRIVATE DURABILITY DIAGNOSTIC")
                    return real_sync(fd)
                with patch("eval_markdown.os.replace", side_effect=fail_latest), patch("eval_markdown.os.fsync", side_effect=fail_sync):
                    with self.assertRaises(LatestReportError) as raised:
                        self.run_fixture(root, "publication-failure")
                self.assertEqual(raised.exception.code, "latest_report_write_failed" if stage == "replace" else "latest_report_durability_failed")
                if stage == "replace":
                    self.assertEqual((root / "EVAL-RESULTS.md").read_bytes(), before)
                else:
                    # Replacement can be visible before directory durability is
                    # acknowledged. Still fail, never claim publication success.
                    self.assertIn("- Run: publication-failure", (root / "EVAL-RESULTS.md").read_text())
                self.assertTrue(raised.exception.retained_report.is_file())
                self.assertEqual(list(root.glob(".EVAL-RESULTS-*.tmp")), [])

    def test_latest_is_last_published_not_last_started_with_concurrent_whole_runs(self):
        entered, release = threading.Event(), threading.Event()
        def slow(spec):
            if spec.agent == "eval-target" and not spec.skill:
                entered.set()
                if not release.wait(20):
                    raise AssertionError("offline concurrency fixture timed out")
            return self.context.invoke(spec)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with ThreadPoolExecutor(max_workers=2) as pool:
                early = pool.submit(self.run_fixture, root, "started-first-published-last", invoke=slow)
                self.assertTrue(entered.wait(10))
                later = pool.submit(self.run_fixture, root, "started-last-published-first")
                _, _, later_store, _ = later.result(timeout=20)
                before = {p: p.read_bytes() for p in later_store.root.rglob("*") if p.is_file()}
                self.assertIn("- Run: started-last-published-first", (root / "EVAL-RESULTS.md").read_text())
                release.set()
                _, _, early_store, _ = early.result(timeout=20)
            self.assertIn("- Run: started-first-published-last", (root / "EVAL-RESULTS.md").read_text())
            self.assertLess(early_store.read_run_manifest()["created_at"], later_store.read_run_manifest()["created_at"])
            self.assertEqual({p: p.read_bytes() for p in before}, before)
            self.assert_links_exist(root / "EVAL-RESULTS.md")
            self.assertEqual(len(self.context.calls), 8)

    def test_concurrent_publication_holds_kernel_lock_until_both_views_are_published(self):
        import eval_markdown
        held, release = threading.Event(), threading.Event()
        real_publish = eval_markdown._publish_latest
        def hold_first(directory, text):
            if "- Run: one\n" in text:
                held.set()
                if not release.wait(20):
                    raise AssertionError("offline publication fixture timed out")
            return real_publish(directory, text)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, one, one_ids = self.run_fixture(root, "one")
            _, _, two, two_ids = self.run_fixture(root, "two")
            # Republish only fresh test-owned evidence, never a historical run.
            (one.root / "results.md").unlink()
            (two.root / "results.md").unlink()
            sanitizer = self.context.runner.evidence_safety.Sanitizer()
            def publish(store, identities):
                return publish_report(self.context.runner, store, identities, store.read_run_manifest(), summarize,
                                      sanitizer, latest_root=root)
            with patch("eval_markdown._publish_latest", side_effect=hold_first), ThreadPoolExecutor(max_workers=2) as pool:
                first = pool.submit(publish, one, one_ids)
                self.assertTrue(held.wait(10))
                descriptor = os.open(root / ".EVAL-RESULTS.lock", os.O_RDWR | os.O_NOFOLLOW)
                try:
                    # Synchronous kernel evidence, not a sleep-based guess that
                    # the other worker is blocked inside the publication window.
                    with self.assertRaises(BlockingIOError):
                        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
                finally:
                    os.close(descriptor)
                second = pool.submit(publish, two, two_ids)
                release.set()
                first.result(timeout=20)
                second.result(timeout=20)
            self.assertIn("- Run: two", (root / "EVAL-RESULTS.md").read_text())
            self.assert_links_exist(root / "EVAL-RESULTS.md")
            self.assertEqual(len(self.context.calls), 8)  # no calls while publishing

    def test_startup_and_completion_paths_from_arbitrary_cwd_in_every_cli_mode(self):
        for flags in ([], ["--verbose"], ["--json"]):
            with self.subTest(flags=flags), tempfile.TemporaryDirectory() as temp:
                base = Path(temp)
                root, caller = base / "repository", base / "caller-cwd"
                root.mkdir()
                caller.mkdir()
                (root / "README.md").write_text("Offline fixture repository\n")
                shutil.copytree(integration.ROOT / "skills" / "product-acceptance", root / "skills" / "product-acceptance")
                stdout, stderr = io.StringIO(), io.StringIO()
                locations = []
                def invoke(spec):
                    # Actual owned artifacts and announced locations must exist
                    # before the first potentially long invocation boundary.
                    if not locations:
                        if "--json" in flags:
                            event = json.loads(stdout.getvalue().splitlines()[-1])
                            self.assertEqual(event["event"], "run-started")
                            artifact_dir = Path(event["artifact_dir"])
                            self.assertEqual(event["latest_report_path"], str(root / "EVAL-RESULTS.md"))
                        else:
                            line = next(line for line in stdout.getvalue().splitlines() if line.startswith("Run artifacts: "))
                            artifact_dir = Path(line.split(": ", 1)[1])
                            self.assertIn("Latest report after completion: " + str(root / "EVAL-RESULTS.md"), stdout.getvalue())
                        self.assertTrue((artifact_dir / "run.json").is_file())
                        self.assertTrue((artifact_dir / ".eval-run-owner.json").is_file())
                        self.assertEqual(artifact_dir.parent, root / ".skill-evals")
                        self.assertFalse((root / "EVAL-RESULTS.md").exists())
                        locations.append(artifact_dir)
                    return self.context.invoke(spec)
                with chdir(caller), patch("run_evals.ROOT", root), \
                     patch.dict(os.environ, {"PATH": os.defpath, "OPENCODE_EVAL_RUNNER_MODELS": str(self.context.runner.root / "tests/fixtures/models-catalog.json")}, clear=True), \
                     patch("run_evals.runner_git_head", return_value="offline-fixture-head"), \
                     patch("run_evals.verify_image", return_value={"image_id": "sha256:" + "a" * 64}), \
                     patch.object(self.context.runner.cli, "resolve_engine", return_value="podman"), \
                     patch.object(self.context.runner.eval_execute, "invoke_once", side_effect=invoke), \
                     redirect_stdout(stdout), redirect_stderr(stderr):
                    code = main(["--cases", "product-acceptance:PA3", "--model", "test/model",
                                 "--runner-root", str(self.context.runner.root), *flags])
                self.assertEqual(code, 0, stderr.getvalue())
                self.assertEqual(list(caller.iterdir()), [])
                self.assert_links_exist(root / "EVAL-RESULTS.md")
                if "--json" in flags:
                    events = [json.loads(line) for line in stdout.getvalue().splitlines()]
                    self.assertEqual([e["event"] for e in events], ["live-spend-plan", "run-started", "verified-pair", "verified-summary"])
                    self.assertEqual(events[-1]["artifact_dir"], str(locations[0]))
                    self.assertEqual(events[-1]["latest_report_path"], str(root / "EVAL-RESULTS.md"))
                else:
                    self.assertEqual(stdout.getvalue().count("Run artifacts: " + str(locations[0])), 2)
                    self.assertEqual(stdout.getvalue().count("Report: " + str(locations[0] / "results.md")), 1)
                    self.assertTrue(stdout.getvalue().endswith("Latest report: " + str(root / "EVAL-RESULTS.md") + "\n"))
                    if not flags and os.environ.get("SKILLS_EVAL_TEST_PRINT_LOCATIONS") == "1":
                        print("OFFLINE INJECTED-I/O FIXTURE — actual human location output (not a live run):")
                        print("\n".join(line for line in stdout.getvalue().splitlines() if line.startswith(
                            ("Run artifacts:", "Latest report", "Completed:", "Manifest:", "Report:"))))

    def test_bad_cli_does_not_create_run_or_replace_previous_latest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.run_fixture(root, "previous")
            before = (root / "EVAL-RESULTS.md").read_bytes()
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()), patch("run_evals.load_runner") as loader:
                code = main(["--cases", "unknown:case", "--model", "test/model", "--artifact-dir", str(root / "bad-run")], report_root=root)
            self.assertEqual(code, 2)
            loader.assert_not_called()
            self.assertFalse((root / "bad-run").exists())
            self.assertEqual((root / "EVAL-RESULTS.md").read_bytes(), before)

    def test_root_reports_share_origin_aware_privacy_projection(self):
        secret = "PRIVATE-HOST-CALLBACK-NOT-IN-CREDENTIAL-INVENTORY"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with patch.object(SkillsProfile, "deterministic_checks", side_effect=RuntimeError(secret)):
                code, _, store, identities = self.run_fixture(root, "private-host-failure")
            self.assertEqual(code, 1)
            self.assertIn(secret, json.dumps(store.read_paired_job_artifact(identities[0])))
            self.assertNotIn(secret, (root / "EVAL-RESULTS.md").read_text())
            self.assertIn("withheld", (root / "EVAL-RESULTS.md").read_text())

    def test_root_latest_includes_negative_non_evidence_partial_and_owned_setup_failure(self):
        for kind, expected in (("negative", 1), ("non-evidence", 1), ("partial", 2), ("setup", None)):
            with self.subTest(kind=kind), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                self.run_fixture(root, "previous-pass")
                previous = (root / ".skill-evals" / "previous-pass" / "results.md").read_bytes()
                def invoke(spec):
                    if kind == "partial":
                        raise AssertionError("PRIVATE ORCHESTRATION MESSAGE")
                    if spec.agent == "eval-judge":
                        response = "{}" if kind == "non-evidence" else json.dumps(integration.grade(self.context.case.project_data, False))
                        return 0, self.context.result(spec, text=response)
                    return self.context.invoke(spec)
                if kind == "setup":
                    with patch.object(self.context.runner.eval_api, "validate_eval_profile", side_effect=RuntimeError("PRIVATE SETUP")):
                        with self.assertRaises(RuntimeError):
                            self.run_fixture(root, kind, invoke=invoke)
                else:
                    code, _, _, _ = self.run_fixture(root, kind, invoke=invoke)
                    self.assertEqual(code, expected)
                text = (root / "EVAL-RESULTS.md").read_text()
                self.assertIn("- Run: " + kind, text)
                self.assertNotIn("PRIVATE", text)
                self.assertIn({"negative": "FAIL 0%", "non-evidence": "NON-EVIDENCE score unavailable",
                               "partial": "INCOMPLETE", "setup": "INCOMPLETE"}[kind], text)
                self.assertEqual((root / ".skill-evals" / "previous-pass" / "results.md").read_bytes(), previous)
                self.assert_links_exist(root / "EVAL-RESULTS.md")

    def test_probe_launch_announces_owned_artifacts_without_latest_evaluation_report(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            options = self.context.options
            options.artifact_dir = root / "probe"
            stderr = io.StringIO()
            def probe(project, runner, controls, case, record):
                self.assertIn("Probe artifacts: " + str(options.artifact_dir), stderr.getvalue())
                self.assertTrue((options.artifact_dir / "run.json").is_file())
                return {"offline_storage_fixture": True}
            with redirect_stderr(stderr):
                proof = run_probe(integration.ROOT, self.context.runner, options, self.context.case, probe)
            self.assertEqual(proof["artifact"], str(options.artifact_dir / "run.json"))
            self.assertFalse((root / "EVAL-RESULTS.md").exists())


if __name__ == "__main__":
    unittest.main()
