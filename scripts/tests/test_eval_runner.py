import json
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_runner import verify_image, load_runner


class ImageBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2]
        cls.runner = load_runner(Path(os.environ.get("SKILLS_EVAL_RUNNER_ROOT", str(root.parent / "opencode-eval-runner"))))
    def test_all_authored_python_and_embedded_provider_free_probes_compile(self):
        from eval_probe import PROBE_CODE
        from eval_runner import IMAGE_PROBE
        for path in Path(__file__).resolve().parents[1].rglob("*.py"):
            compile(path.read_bytes(), str(path), "exec")
        compile(PROBE_CODE, "config-probe", "exec")
        compile(IMAGE_PROBE, "image-probe", "exec")
    def test_mutable_tags_and_missing_local_image_fail_before_execution(self):
        runner = SimpleNamespace(root=Path("/not-used"))
        with patch("eval_runner.subprocess.run") as run:
            for image in ("edge", "ghcr.io/example:sha-1262ac8", None, "sha256:abc"):
                with self.assertRaises(ValueError):
                    verify_image(runner, "podman", image, "opencode")
            run.assert_not_called()
            run.return_value = SimpleNamespace(returncode=125, stdout="", stderr="not present locally")
            with self.assertRaisesRegex(ValueError, "not available locally"):
                verify_image(runner, "podman", "sha256:" + "a" * 64, "opencode")
            self.assertEqual(run.call_count, 1)
            self.assertEqual(run.call_args.args[0][1:3], ["image", "inspect"])

    def test_adapter_hash_and_cli_version_required_no_pull_or_network(self):
        runner = self.runner
        identity = "sha256:" + "a" * 64
        for version, files, passes in (("2.0.23", {"invoke.py": "abc"}, True),
                                       ("2.0.11", {"invoke.py": "abc"}, False),
                                       ("2.0.23", {"invoke.py": "old"}, False)):
            with patch("eval_runner.container_sources", return_value={"invoke.py": "abc"}), patch("eval_runner.subprocess.run") as run, patch.object(runner.cli, "resolve_engine", return_value="podman"):
                run.side_effect = [SimpleNamespace(returncode=0, stdout=json.dumps([{"Id": identity}])),
                                   SimpleNamespace(returncode=0, stdout=json.dumps({"version": version, "files": files}))]
                if passes:
                    self.assertEqual(verify_image(runner, "podman", identity, "opencode")["image_id"], identity)
                else:
                    with self.assertRaisesRegex(ValueError, "host/image mismatch"):
                        verify_image(runner, "podman", identity, "opencode")
                command = run.call_args.args[0]
                self.assertIn("--pull=never", command)
                self.assertEqual(command[command.index("--network") + 1], "none")
                self.assertIn("-I", command)
                self.assertNotIn("invoke.py", command)


if __name__ == "__main__":
    unittest.main()
