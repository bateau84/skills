"""Single compatibility boundary to the clean, exact external runner checkout.

Nothing from Loom's agent/plugin runtime is imported or copied. Keep this module
small: transport, observer, retry safety and storage are external runner policy.
"""
from __future__ import annotations

import importlib
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

from eval_cases import digest

RUNNER_REVISION = "1262ac8c2eebbd10af572e3e3560318f6113233b"
LOOM_METHOD_REVISION = "c16e2c793b8faa8d21cf2ca9833606676e461e79"
PROFILE_API = "opencode-eval-runner/eval-profile/v1"


def git(root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError as exc:
        raise ValueError("cannot inspect pinned runner checkout with git") from exc


def load_runner(root: Path):
    root = root.expanduser().resolve(strict=True)
    if git(root, "rev-parse", "--show-toplevel") != str(root):
        raise ValueError("runner-root must be the external checkout root")
    if git(root, "rev-parse", "HEAD") != RUNNER_REVISION:
        raise ValueError(f"runner checkout must be exactly {RUNNER_REVISION}")
    if git(root, "status", "--porcelain", "--ignored", "--untracked-files=all"):
        raise ValueError("runner checkout must be clean (including untracked/ignored files and bytecode)")
    # Do not write __pycache__ in the read-only dependency, even in test imports.
    sys.dont_write_bytecode = True
    sys.path.insert(0, str(root))
    modules = {}
    for name in ("eval_api", "eval_plan", "eval_paired", "eval_artifacts", "eval_execute", "eval_evidence", "cli"):
        mod = importlib.import_module(f"runner.{name}")
        if Path(mod.__file__).resolve() != root / "runner" / f"{name}.py":
            raise ValueError(f"runner import resolved outside pinned checkout: {name}")
        modules[name] = mod
    if modules["eval_api"].EVAL_PROFILE_API != PROFILE_API:
        raise ValueError("unsupported EvalProfile API")
    safety = importlib.import_module("container.evidence_safety")
    if Path(safety.__file__).resolve() != root / "container" / "evidence_safety.py":
        raise ValueError("credential inventory import resolved outside pinned checkout")
    modules["evidence_safety"] = safety
    # The pinned runner's command builder owns every OCI option. This additional
    # fail-closed acquisition guard is the only adjustment: never implicitly pull.
    cli = modules["cli"]
    if not getattr(cli.build_container_command, "skills_no_pull", False):
        original = cli.build_container_command

        def local_only(*args, **kwargs):
            command, result_path = original(*args, **kwargs)
            if command[1] != "run":
                raise ValueError("pinned runner OCI command contract changed")
            return command[:2] + ["--pull=never"] + command[2:], result_path

        local_only.skills_no_pull = True
        cli.build_container_command = local_only
    return SimpleNamespace(root=root, **modules)


def container_sources(root: Path) -> dict[str, str]:
    return {
        p.relative_to(root / "container").as_posix(): digest(p.read_bytes())
        for p in sorted((root / "container").rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts
    }


IMAGE_PROBE = r'''
import hashlib, json, pathlib, subprocess
root = pathlib.Path('/opt/opencode-eval-runner/container')
files = {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
version = subprocess.check_output([BINARY, '--version'], text=True).strip()
print(json.dumps({'files': files, 'version': version}))
'''


def build_probe_command(runner, engine, identity, code, workspace, config, root, transport="opencode"):
    """Use runner OCI isolation, but mount NO credentials for zero-inference probes."""
    inputs, outputs = root / "input", root / "output"
    inputs.mkdir()
    outputs.mkdir()
    # Explicit empty placeholders prevent automatic host seed discovery. Their
    # bind options are removed before execution: even empty auth/catalogue files
    # are not mounted during provider-free proof.
    auth, models = root / "empty-auth.json", root / "empty-models.json"
    auth.write_text("{}\n")
    models.write_text("{}\n")
    args = argparse.Namespace(
        transport=transport, engine=engine, network="none", image=identity,
        workspace=str(workspace), workspace_mode="ro", output=str(outputs / "probe.json"),
        mount=[], model="unused/probe", reasoning=None, agent=None, skill=None, expected_plugin=None,
        auth=str(auth), models_catalog=str(models), config=str(config), config_root=None,
        env=[], timeout_seconds=45,
    )
    command, _ = runner.cli.build_container_command(args, inputs, outputs, host_env={})
    for source, target in ((auth, "/seed/auth.json"), (models, "/seed/models.json")):
        bind = runner.cli.bind_arg(source, target, readonly=True)
        index = next(i for i in range(len(command) - len(bind) + 1) if command[i:i + len(bind)] == bind)
        del command[index:index + len(bind)]
    if any(marker in part for part in command for marker in ("/seed/auth.json", "/seed/models.json", "/seed/opencode.db", "/seed/opencode-config")):
        raise ValueError("provider-free probe must not mount auth/catalogue/database/config-root seeds")
    return command[:-1] + ["--entrypoint=python3", command[-1], "-I", "-B", "-c", code]


def verify_image(runner, engine: str, image: str, transport: str) -> dict:
    """Zero inference, no network/pull/build. Compare image adapter bytes to pin."""
    if not image or not re.fullmatch(r"(?:sha256:)?[0-9a-f]{64}|[^\s]+@sha256:[0-9a-f]{64}", image):
        raise ValueError("image must be an immutable full local image ID or repository@sha256:digest, not a tag")
    proc = subprocess.run([engine, "image", "inspect", image], capture_output=True, text=True, timeout=30)
    if proc.returncode:
        raise ValueError("immutable image is not available locally; acquisition/build is explicit and never automatic")
    inspected = json.loads(proc.stdout)[0]
    identity = inspected.get("Id", inspected.get("ID"))
    if not isinstance(identity, str) or not re.fullmatch(r"(?:sha256:)?[0-9a-f]{64}", identity):
        raise ValueError("engine did not return a full image ID")
    binary, expected = ("opencode", "2.0.23") if transport == "opencode" else ("copilot", "1.0.83")
    code = "BINARY = " + repr(binary) + "\n" + IMAGE_PROBE
    with tempfile.TemporaryDirectory(prefix="skills-image-compatibility-") as temp:
        root = Path(temp)
        workspace = root / "workspace"
        workspace.mkdir()
        config = root / "config.json"
        config.write_text("{}\n")
        command = build_probe_command(runner, engine, identity, code, workspace, config, root, transport)
        proc = subprocess.run(command, env={"PATH": os.environ.get("PATH", os.defpath)},
                              text=True, capture_output=True, timeout=45)
    if proc.returncode:
        raise ValueError(f"provider-free image compatibility probe failed (exit {proc.returncode}): {proc.stderr[-4000:]}")
    observed = json.loads(proc.stdout)
    if observed["files"] != container_sources(runner.root):
        raise ValueError("host/image mismatch: image container adapter bytes differ from pinned runner")
    if not re.search(rf"(?<![\d.]){re.escape(expected)}(?![\d.])", observed["version"]):
        raise ValueError(f"host/image mismatch: {binary} must be {expected}")
    return {"image_id": identity, "requested_identity": image, "transport": transport,
            "platform": inspected.get("Os", "unknown") + "/" + inspected.get("Architecture", "unknown"),
            "cli_version": observed["version"], "container_sha256": observed["files"]}
