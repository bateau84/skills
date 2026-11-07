"""Provider-free checks of the manual fixture and its independent oracle."""
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PACKET = ROOT / "skills" / "software-engineering" / "evals"


class StrategicFixtureTests(unittest.TestCase):
    def check_fixture(self, project, stage):
        return subprocess.run(
            [sys.executable, "-I", "-B", str(PACKET / "verify_artifacts.py"), str(project), "--stage", stage],
            capture_output=True, text=True, timeout=20, check=False,
        )

    def test_seed_satisfies_its_existing_contract(self):
        result = self.check_fixture(PACKET / "fixture", "seed")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("Ran 5 tests", result.stderr)

    def test_seed_does_not_already_satisfy_the_requested_feature(self):
        result = self.check_fixture(PACKET / "fixture", "first")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("test_allowed_retries", result.stderr)
        self.assertIn("ValueError: job is not failed", result.stderr)

    def test_limit_mutation_is_rejected_by_a_behavior_assertion(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            shutil.copytree(PACKET / "fixture", project)
            for name in ("api", "cli", "scheduler"):
                path = project / "jobqueue" / f"{name}.py"
                source = path.read_text()
                self.assertIn("job.attempts >= 3", source)
                path.write_text(source.replace("job.attempts >= 3", "job.attempts > 3"))
            result = self.check_fixture(project, "seed")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("test_limit_rejections", result.stderr)
            self.assertIn("AssertionError: ValueError not raised", result.stderr)

    def test_ignoring_requested_id_is_rejected_by_a_behavior_assertion(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            shutil.copytree(PACKET / "fixture", project)
            for name in ("api", "cli", "scheduler"):
                path = project / "jobqueue" / f"{name}.py"
                source = path.read_text()
                self.assertIn("store.get(job_id)", source)
                path.write_text(source.replace("store.get(job_id)", 'store.get("job")'))
            result = self.check_fixture(project, "seed")
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("test_selects_requested_job_and_preserves_other_records", result.stderr)
            self.assertIn("AssertionError", result.stderr)


if __name__ == "__main__":
    unittest.main()
