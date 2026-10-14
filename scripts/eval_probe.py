"""Provider-free stock configuration/catalog probe; no model prompt is resumed.

OCI options and server lifecycle are delegated to the pinned runner. This probes
effective configuration, not model behavior or a successful native skill load.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

from eval_cases import digest
from eval_profile import SkillsProfile
from eval_runner import build_probe_command


def effective_agent_matches(actual, expected, plugins):
    if not actual or actual.get("system") != expected["system"]:
        return False
    # Stock 2.0.23 BrowserConnection.make appends this hard deny after config.
    # Recognize only that exact source-backed rule, never arbitrary extensions.
    suffix = list(expected["permissions"])
    if "opencode.browser" in plugins:
        suffix.append({"action": "browser", "resource": "*", "effect": "deny"})
    return actual.get("permissions", [])[-len(suffix):] == suffix


PROBE_CODE = r'''
import hashlib, json, os, pathlib, sys
sys.dont_write_bytecode = True
sys.path.insert(0, '/opt/opencode-eval-runner')
from container.invoke import (prepare_opencode_env, _start_preflight_server,
    _standalone_json_request, _stop_preflight_server, unwrap_api_data,
    runtime_sanitizer, configure_runtime_observer_env, finalize_runtime_observer)
from container.native_observer import RuntimeObservationTransport, OBSERVER_STREAM_ENV
from container.runtime_evidence import build_runtime_evidence
env = prepare_opencode_env()
sanitizer = runtime_sanitizer(env)
configure_runtime_observer_env(env, sanitizer)
transport = RuntimeObservationTransport()
env[OBSERVER_STREAM_ENV] = transport.endpoint
server, url, authorization = _start_preflight_server(env, 30)
try:
    def request(path, method='GET', payload=None):
        return unwrap_api_data(_standalone_json_request(url, path, method=method,
            payload=payload, timeout=20, authorization=authorization))
    session = request('/api/session', 'POST', {'title': 'provider-free config probe',
        'agent': AGENT, 'location': {'directory': '/workspace'}})
    # The pinned SessionPrompt.prepare activation barrier does NOT infer a model.
    request('/api/session/' + session['id'] + '/prompt', 'POST',
        {'text': 'zero-inference configuration activation', 'resume': False})
    query = '?location%5Bdirectory%5D=%2Fworkspace'
    agents = request('/api/agent' + query)
    skills = request('/api/skill' + query)
    plugins = request('/api/plugin' + query)
    reads = {}
    for name in FILES:
        path = pathlib.Path('/workspace/.opencode/skills/' + SKILL + '/' + name)
        reads[name] = {'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                       'readable': True, 'write_bits': bool(path.stat().st_mode & 0o222)}
    result = {'agents': agents, 'skills': [s['id'] for s in skills],
        'plugins': [p['id'] for p in plugins], 'files': reads,
        'workspace_evals': list(str(p) for p in pathlib.Path('/workspace').rglob('evals')),
        'workspace_files': sorted(str(p.relative_to('/workspace')) for p in pathlib.Path('/workspace').rglob('*') if p.is_file()),
        'workspace_symlinks': [str(p) for p in pathlib.Path('/workspace').rglob('*') if p.is_symlink()],
        'workspace_read_only': bool(os.statvfs('/workspace').f_flag & os.ST_RDONLY),
        'loom_seed_exists': pathlib.Path('/seed/opencode-config').exists(),
        'provider_calls': 0}
finally:
    _stop_preflight_server(server)
capture = finalize_runtime_observer(transport, env)
result['runner_protocol'] = {
    'schema': 'opencode-eval-runner/v1', 'transport': 'opencode',
    'model': 'unused/probe', 'reasoning': 'provider-default',
    'reasoning_source': 'provider-default', 'exit_code': 0, 'text': '',
    'runtime_evidence': build_runtime_evidence(capture, sanitizer)}
print(json.dumps(result))
'''


def probe_configs(root: Path, runner, options, case, record=None):
    results = {}
    for side in ("baseline", "candidate", "judge"):
        profile = SkillsProfile(root, runner, options, "candidate" if side == "candidate" else "baseline", {})
        with profile.prepare(case, 1) as prepared:
            workspace = prepared["judge"] if side == "judge" else prepared["target"]
            phase = "judge" if side == "judge" else profile.side
            config = prepared["configs"][phase][0]
            temp = config.parent
            agent_id = "eval-judge" if side == "judge" else "eval-target"
            code = ("AGENT=" + repr(agent_id) + "\nSKILL=" + repr(case.project_data["skill"]) + "\nFILES="
                    + repr(list(prepared["files"]) if side == "candidate" else []) + "\n" + PROBE_CODE)
            command = build_probe_command(runner, options.engine, options.target_image_id, code, workspace, config, temp)
            proc = subprocess.run(command, env={"PATH": os.environ.get("PATH", os.defpath)}, capture_output=True, text=True, timeout=60)
            if proc.returncode:
                raise ValueError(f"{side} provider-free effective-config probe failed (exit {proc.returncode}): {proc.stderr[-4000:]}; no runtime proof")
            result = json.loads(proc.stdout)
            configured = json.loads(config.read_text())
            agent = next((a for a in result["agents"] if a["id"] == agent_id), None)
            expected = configured["agents"][agent_id]
            observation = {"actual_agent": agent, "expected_agent": expected,
                           "agent_ids": [a["id"] for a in result["agents"]],
                           "skill_ids": result["skills"], "plugin_ids": result["plugins"],
                           "files": result["files"], "workspace_evals": result["workspace_evals"],
                           "workspace_files": result["workspace_files"], "workspace_symlinks": result["workspace_symlinks"],
                           "workspace_read_only": result["workspace_read_only"],
                           "loom_seed_exists": result["loom_seed_exists"],
                           "runner_protocol": result["runner_protocol"],
                           "effective_config_sha256": prepared["configs"][phase][1],
                           "practitioner_sha256": {name: digest(content)
                                                   for name, content in prepared["files"].items()} if side == "candidate" else {}}
            if record:
                record(side, observation)
            # Stock agent defaults/global rules precede configured agent rules;
            # Permission.evaluate uses the last match. Verify the exact suffix.
            if not effective_agent_matches(agent, expected, result["plugins"]):
                raise ValueError(f"{side}: stock runtime effective agent system/permissions differ from generated config: "
                                 + json.dumps({"agent_ids": [a["id"] for a in result["agents"]],
                                               "actual_agent": agent, "expected_agent": expected}))
            desired_skills = [case.project_data["skill"]] if side == "candidate" else []
            unknown_plugins = [p for p in result["plugins"] if not (p.startswith("opencode.") or p == "eval-runtime-observer")]
            if result["skills"] != desired_skills or result["workspace_evals"] or result["loom_seed_exists"] or unknown_plugins:
                raise ValueError(f"{side}: runtime catalog/config contamination or rubric exposure")
            if not all(value["readable"] and not value["write_bits"] for value in result["files"].values()):
                raise ValueError("selected practitioner reference is not readable/read-only")
            expected_files = sorted(f".opencode/skills/{case.project_data['skill']}/{name}" for name in prepared["files"]) if side == "candidate" else []
            if result["workspace_files"] != expected_files or result["workspace_symlinks"] or not result["workspace_read_only"]:
                raise ValueError(f"{side}: workspace bytes are not isolated/exactly selected/read-only")
            if any(value["sha256"] != digest(prepared["files"][name]) for name, value in result["files"].items()):
                raise ValueError("container practitioner bytes differ from copied working-tree provenance")
            protocol = runner.cli.validate_container_result(result["runner_protocol"])
            readiness = runner.eval_evidence.check_evidence_readiness(
                protocol["runtime_evidence"], runner.eval_api.EvidenceRequirement(("native", "code_mode_execution")))
            if readiness.status != "ready" or protocol["runtime_evidence"]["observations"]:
                raise ValueError(f"{side}: zero-inference observer/schema probe is not complete empty evidence: {readiness.reasons}")
            results[side] = {"status": "effective-config-verified", "skill_ids": result["skills"],
                             "reference_files": list(result["files"]), "provider_calls": 0,
                             "workspace_read_only": result["workspace_read_only"],
                             "runner_runtime_evidence": protocol["runtime_evidence"]}
    return results
