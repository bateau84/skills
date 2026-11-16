"""Compose the skills no-pull guard with the real pinned runner command builder."""
import json
import os
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from unittest.mock import patch

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from eval_runner import load_runner


class OciCommandCompositionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root = Path(__file__).resolve().parents[2]
        cls.runner = load_runner(Path(os.environ.get(
            "SKILLS_EVAL_RUNNER_ROOT", str(root.parent / "opencode-eval-runner"),
        )))

    def check_command(self, engine, *, claude=True, host_env=None):
        environment = {} if host_env is None else host_env
        identity = "sha256:" + "a" * 64
        prefix = (["podman", "--remote=false"] if engine == "podman" else
                  ["docker", "--host", environment.get("DOCKER_HOST", "unix:///var/run/docker.sock")])
        if not claude:
            prefix = [engine]
        image = {
            "Id": identity,
            "Config": {"Labels": {
                "org.opencontainers.image.version": "2.2.6",
                "io.opencode-eval-runner.invoke-adapter": "opencode-eval-runner/opencode-invoke/v1",
                "io.opencode-eval-runner.claude-version": "2.1.318",
            }},
        }
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            workspace = root / "workspace"
            workspace.mkdir()
            config = root / "config.json"
            config.write_text("{}\n")
            catalog = root / "models.json"
            catalog.write_text("{}\n")
            auth = root / "empty-auth.json"
            auth.write_text("{}\n")
            arguments = [
                "invoke", "--transport", "opencode", "--engine", engine,
                "--image", identity, "--workspace", str(workspace),
                "--config", str(config), "--models-catalog", str(catalog),
                "--prompt-file", str(root / "prompt.txt"), "--output", str(root / "result.json"),
                "--model", "claude-agent/test-model" if claude else "openai/test-model",
            ]
            if claude:
                profile = root / "dedicated-profile"
                profile.mkdir(mode=0o700)
                credential = profile / ".credentials.json"
                credential.write_text("{}\n")
                credential.chmod(0o600)
                arguments += ["--claude-config-dir", str(profile)]
            else:
                arguments += ["--auth", str(auth)]
            options = self.runner.cli.parser().parse_args(arguments)
            # The actual image verifier and both command-building layers run.
            # Only OCI process I/O and executable discovery are substituted.
            with patch.dict(os.environ, {}, clear=True), patch.object(
                self.runner.cli, "resolve_engine", return_value=engine,
            ), patch("runner.oci_image.subprocess.run", return_value=SimpleNamespace(
                returncode=0, stdout=json.dumps(image), stderr="",
            )) as process:
                command, result = self.runner.cli.build_container_command(
                    options, root / "input", root / "output", host_env=environment,
                )
            if claude:
                process.assert_called_once()
                self.assertEqual(process.call_args.args[0], prefix + [
                    "image", "inspect", "--format", "{{json .}}", identity,
                ])
            else:
                process.assert_not_called()
            self.assertEqual(command[:len(prefix) + 1], prefix + ["run"])
            self.assertEqual(command.count("run"), 1)
            self.assertEqual(command.count("--pull=never"), 1)
            self.assertGreater(command.index("--pull=never"), len(prefix))
            self.assertEqual(command[-1], identity)
            self.assertIn("--read-only", command)
            self.assertIn("no-new-privileges", command)
            self.assertEqual(result, root / "result.json")

    def test_claude_podman_prefix_survives_skills_guard(self):
        self.check_command("podman")

    def test_claude_docker_prefix_survives_skills_guard(self):
        self.check_command("docker")

    def test_claude_custom_local_docker_socket_is_preserved(self):
        self.check_command("docker", host_env={"DOCKER_HOST": "unix:///run/user/1000/docker.sock"})

    def test_legacy_commands_still_receive_one_no_pull_option(self):
        for engine in ("podman", "docker"):
            with self.subTest(engine=engine):
                self.check_command(engine, claude=False)


if __name__ == "__main__":
    unittest.main()
