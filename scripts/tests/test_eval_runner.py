import json
import os
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_runner import RUNNER_REVISION, verify_image, load_runner


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

    def test_runner_revision_is_refreshed_pin_and_configuration_errors_are_safe(self):
        from eval_reporting import boundary_error
        from tempfile import TemporaryDirectory

        self.assertEqual(RUNNER_REVISION, "dbbbf2a0740aee7a9e9035cc14a785a9467b8fb1")
        self.assertEqual(
            boundary_error(ValueError(f"runner checkout must be exactly {RUNNER_REVISION}; check out that revision in a dedicated clean checkout")),
            f"runner checkout must be exactly {RUNNER_REVISION}; check out that revision in a dedicated clean checkout",
        )
        self.assertIn("--runner-root", boundary_error(ValueError("runner-root must be the external checkout root; provide --runner-root pointing to the clean repository root")))
        self.assertIn("withheld", boundary_error(ValueError("runner checkout failed: PRIVATE_TOKEN=secret")))
        with TemporaryDirectory() as temp, patch("eval_runner.git", side_effect=[temp, "old-revision"]):
            with self.assertRaisesRegex(ValueError, "dedicated clean checkout"):
                load_runner(Path(temp))

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
        for version, files, passes in (("2.2.2", {"invoke.py": "abc"}, True),
                                       ("2.0.11", {"invoke.py": "abc"}, False),
                                       ("2.2.2", {"invoke.py": "old"}, False)):
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

    def test_model_catalog_resolver_uses_explicit_precedence_and_immutable_snapshot(self):
        import os
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as temp:
            source = Path(temp) / "source.json"
            fixture = self.runner.root / "tests/fixtures/models-catalog.json"
            original = fixture.read_bytes()
            source.write_bytes(original)
            with patch.dict(os.environ, {"OPENCODE_EVAL_RUNNER_MODELS": str(self.runner.root / "absent.json")}):
                with self.runner.model_catalog.pinned_model_catalog(source) as snapshot:
                    source.write_text("private replacement")
                    self.assertEqual(snapshot.read_bytes(), original)
                    self.assertEqual(snapshot.stat().st_mode & 0o777, 0o444)
                    self.assertNotEqual(snapshot.resolve(), source.resolve())
            with patch.dict(os.environ, {"OPENCODE_EVAL_RUNNER_MODELS": str(fixture)}), patch.object(
                self.runner.model_catalog.urllib.request, "urlopen"
            ) as fetch:
                with self.runner.model_catalog.pinned_model_catalog() as snapshot:
                    self.assertEqual(snapshot.read_bytes(), original)
                fetch.assert_not_called()

    def test_default_catalog_fetch_is_bounded_and_snapshot_lives_only_in_context(self):
        import os
        from contextlib import contextmanager
        source = self.runner.root / "tests/fixtures/models-catalog.json"
        payload = source.read_bytes()
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size):
                self.assert_size = size
                nonlocal payload
                chunk, payload = payload[:size], payload[size:]
                return chunk
        with patch.dict(os.environ, {}, clear=True), patch.object(
            self.runner.model_catalog.urllib.request, "urlopen", return_value=Response()
        ) as fetch:
            with self.runner.model_catalog.pinned_model_catalog() as snapshot:
                path = snapshot
                self.assertEqual(snapshot.read_bytes(), source.read_bytes())
                self.assertTrue(snapshot.exists())
            self.assertFalse(path.exists())
            fetch.assert_called_once()


if __name__ == "__main__":
    unittest.main()
