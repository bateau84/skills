#!/usr/bin/env python3
"""Optional paired skill eval tooling. Launch with python3 -I -B."""
from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from contextlib import ExitStack
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter

# -I removes cwd/PYTHONPATH. Add only this known project implementation root.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from eval_cases import discover, digest, strict_json
from eval_profile import METADATA_SCHEMA, SkillsComparison, SkillsProfile, compile_provider_settings, reasoning_control, sanitized_environment
from eval_runner import RUNNER_REVISION, load_runner, verify_image
from eval_reporting import EvalReporter, boundary_error, invocation_return_state, terminal_text
from eval_markdown import LATEST_NAME, ReportPublicationError, publish_report, read_report_evidence, validate_latest_destination

ROOT = Path(__file__).resolve().parents[1]


def parser():
    p = argparse.ArgumentParser(description="Explicit-load paired skill evals using the pinned external runner; live calls spend inference.")
    mode = p.add_mutually_exclusive_group()
    mode.add_argument("--list", action="store_true", help="List fixtures; never invokes models")
    mode.add_argument("--validate", action="store_true", help="Validate fixture corpus; never invokes models")
    mode.add_argument("--harness-test", action="store_true", help="Run provider-free stdlib tests (including pinned API integration)")
    mode.add_argument("--probe", action="store_true", help="Check existing immutable images without provider inference or acquisition")
    output = p.add_mutually_exclusive_group()
    output.add_argument("--json", action="store_true", help="Live JSONL events with artifact/report locations; human notices on stderr")
    output.add_argument("--verbose", action="store_true", help="Live human results plus bounded attempt timing/exit diagnostics (no payload dumps)")
    p.add_argument("--runner-root", type=Path, help="Clean pinned checkout; default SKILLS_EVAL_RUNNER_ROOT or local sibling opencode-eval-runner")
    p.add_argument("--cases", help="Comma-separated canonical IDs or skill:source-id selectors")
    p.add_argument("--target", "--skills", dest="target", help="Comma-separated skill names; optionally intersect --cases")
    p.add_argument("--all", action="store_true", help="Explicitly select all cases in selected targets (or entire corpus)")
    p.add_argument("--target-kind", choices=("skill",), default="skill")
    p.add_argument("--target-transport", choices=("opencode",), default="opencode")
    p.add_argument("--model", help="Required live target model ID: provider/model (for example openai/gpt-6.1)")
    p.add_argument("--judge-model", help="Optional judge model ID: provider/model; defaults to --model unchanged")
    p.add_argument("--judge-transport", choices=("opencode", "github-copilot-cli"), default="opencode")
    for name in ("reasoning", "target-reasoning", "judge-reasoning"):
        p.add_argument("--" + name)
    p.add_argument("--iterations", type=int, default=1)
    p.add_argument("--parallel", type=int, default=1, help="Bounded concurrent pairs; sides always sequential; >=1")
    p.add_argument("--transport-retries", type=int, default=0, help="0–5; runner replay-safe provider.no-route/Model unavailable policy only")
    p.add_argument("--timeout-seconds", "--inner-timeout", dest="timeout_seconds", type=int, default=240)
    p.add_argument("--container-timeout", "--outer-timeout", dest="container_timeout", type=int, default=300)
    p.add_argument("--engine", choices=("auto", "podman", "docker"), default="auto")
    p.add_argument("--network", help="OCI network mode; live networking is not an offline eval; host weakens isolation")
    p.add_argument("--image", "--opencode-image", dest="opencode_image", help="Required immutable full local OpenCode image ID/digest")
    p.add_argument("--copilot-image", help="Immutable local Copilot judge image ID/digest")
    p.add_argument("--artifact-dir", "--output", dest="artifact_dir", type=Path, help="Fresh single-run directory; default .skill-evals/<run-id>")
    p.add_argument("--provider-config", type=Path, help="V2 provider-only JSON; runtime policy/config inheritance is forbidden")
    for name in ("auth", "database", "models-catalog"):
        p.add_argument("--" + name, type=Path)
    p.add_argument("--env", action="append", default=[], help="Intentional extra provider env variable name; never logs values")
    return p


def csv(value, label):
    if value is None:
        return ()
    values = tuple(s.strip() for s in value.split(","))
    if not all(values):
        raise ValueError(f"{label} contains an empty selector")
    return values


def select(cases, options):
    targets, selectors = csv(options.target, "--target/--skills"), csv(options.cases, "--cases")
    unknown = set(targets) - {c.skill for c in cases}
    if unknown:
        raise ValueError("unknown skill target(s): " + ", ".join(sorted(unknown)))
    candidates = tuple(c for c in cases if not targets or c.skill in targets)
    known = {s for c in candidates for s in c.selectors}
    unknown = set(selectors) - known
    if unknown:
        raise ValueError("unknown case selector(s) for selected targets: " + ", ".join(sorted(unknown)))
    if not (targets or selectors or options.all):
        raise ValueError("explicit --cases, --target/--skills, or --all required; --target-kind skill is NOT selection")
    selected = tuple(c for c in candidates if options.all or not selectors or set(selectors).intersection(c.selectors))
    if not selected:
        raise ValueError("selection matched no cases")
    return selected


def validate_live(options, selected):
    def validate_model_id(value, option):
        if not value or not value.strip() or value != value.strip():
            raise ValueError(f"live execution requires explicit {option} provider/model ID (for example openai/gpt-6.1)")
        provider, separator, model = value.partition("/")
        if not separator or not provider or not model or any(c.isspace() for c in value):
            raise ValueError(f"{option} must be a qualified provider/model ID (for example openai/gpt-6.1); got an unqualified or malformed ID")

    validate_model_id(options.model, "--model")
    if options.judge_model is not None:
        validate_model_id(options.judge_model, "--judge-model")
    if not selected:
        raise ValueError("empty live selection")
    for name in ("iterations", "parallel", "timeout_seconds"):
        if getattr(options, name) < 1:
            raise ValueError(f"{name} must be >=1")
    if not 0 <= options.transport_retries <= 5:
        raise ValueError("transport-retries must be 0–5")
    if options.container_timeout < max(300, options.timeout_seconds + 60):
        raise ValueError("outer timeout must be >=300 and at least inner timeout +60 seconds")
    if options.judge_transport != "opencode" and not options.judge_model:
        raise ValueError("cross-transport judge requires explicit --judge-model")
    for name in ("reasoning", "target_reasoning", "judge_reasoning", "judge_model"):
        value = getattr(options, name)
        if value is not None and (not value.strip() or value != value.strip()):
            raise ValueError(f"{name} must be nonempty without surrounding whitespace")
    if "#" in options.model and (options.target_reasoning or options.reasoning):
        raise ValueError("target model#variant conflicts with explicit reasoning")
    if "#" in (options.judge_model or options.model) and (options.judge_reasoning or options.reasoning):
        raise ValueError("judge model#variant conflicts with explicit reasoning")


def call_budget(case_count, options):
    pairs = case_count * options.iterations
    return {"pairs": pairs, "nominal_target_calls": pairs * 2, "nominal_judge_calls": pairs * 2,
            "maximum_target_calls": pairs * 2 * (options.transport_retries + 1),
            "maximum_judge_calls": pairs * 2 * (options.transport_retries + 1)}


def runner_root(options):
    return options.runner_root or Path(os.environ.get("SKILLS_EVAL_RUNNER_ROOT", str(ROOT.parent / "opencode-eval-runner")))


def freeze_environment(options):
    # Resolve intentional seeds BEFORE dropping inherited runtime-control env.
    for attr, env in (("auth", "OPENCODE_EVAL_RUNNER_AUTH"), ("database", "OPENCODE_EVAL_RUNNER_DB"), ("models_catalog", "OPENCODE_EVAL_RUNNER_MODELS")):
        value = getattr(options, attr) or os.environ.get(env)
        if value:
            try:
                path = Path(value).expanduser().resolve(strict=True)
            except (OSError, RuntimeError) as exc:
                if attr == "models_catalog":
                    raise ValueError("model catalog source is unavailable; check --models-catalog or OPENCODE_EVAL_RUNNER_MODELS") from None
                raise
            if not path.is_file():
                if attr == "models_catalog":
                    raise ValueError("model catalog source is unavailable; check --models-catalog or OPENCODE_EVAL_RUNNER_MODELS")
                raise ValueError(f"{attr} seed is not a file")
            setattr(options, attr, path)
    clean = sanitized_environment(dict(os.environ), tuple(options.env))
    os.environ.clear()
    os.environ.update(clean)


def execute_pair(runner, baseline, candidate, job, run_id, invoker=None, reporter=None):
    with ExitStack() as stack:
        bp = stack.enter_context(baseline.prepare(job.case, job.iteration))
        cp = stack.enter_context(candidate.prepare(job.case, job.iteration))
        if bp["files"] != cp["files"]:
            raise ValueError("skill working-tree bytes changed during pair preparation; no inference started")
        retry = runner.eval_execute.TransientProviderRetryPolicy()
        sides = []
        for profile, prepared in ((baseline, bp), (candidate, cp)):
            sides.append(runner.eval_paired.PairedSideExecution(
                case=job.case, prepared=prepared, target_spec=profile.target_spec(job.case, prepared),
                evidence_requirement=profile.target_evidence_requirement(job.case, prepared), profile=profile,
                project_metadata=profile.artifact_metadata(job.case, prepared),
                target_retry_policy=retry, judge_retry_policy=retry,
                target_max_attempts=profile.options.transport_retries + 1,
                judge_max_attempts=profile.options.transport_retries + 1,
            ))
        invoke = invoker or runner.eval_execute.invoke_once
        if reporter is not None:
            roles = {prepared[phase]: (side, phase) for side, prepared in (("baseline", bp), ("candidate", cp))
                     for phase in ("target", "judge")}
            attempts = {}
            def reporting_invoker(spec):
                side, phase = roles[spec.workspace]
                key = (side, phase)
                attempts[key] = attempts.get(key, 0) + 1
                # Progress describes entry into the invocation boundary, not a
                # completed provider request or an evidence-backed result.
                reporter.invocation(job.case.id, job.iteration, side, phase, attempts[key])
                started = perf_counter()
                try:
                    reply = invoke(spec)
                except Exception:
                    reporter.invocation_finished(job.case.id, job.iteration, side, phase, attempts[key],
                                                 max(0.0, perf_counter() - started), "raised")
                    raise
                elapsed = max(0.0, perf_counter() - started)
                reporter.invocation_finished(job.case.id, job.iteration, side, phase, attempts[key],
                                             elapsed, invocation_return_state(reply))
                return reply
        else:
            reporting_invoker = invoke
        result = runner.eval_paired.run_paired_evaluation(
            run_id=run_id, iteration=job.iteration, baseline=sides[0], candidate=sides[1],
            comparison_extension=SkillsComparison(runner),
            target_invoker=reporting_invoker,
            judge_invoker=reporting_invoker,
        )
        return runner.eval_paired.build_paired_eval_artifact(result)


def summarize(runner, artifacts):
    records = []
    for raw in artifacts:
        artifact = runner.eval_artifacts.validate_paired_eval_artifact(raw)
        sides = artifact["sides"]
        treatment = all(any(check["name"] == "treatment-integrity" and check["status"] == "pass"
                            for check in sides[s]["deterministic_checks"]) for s in ("baseline", "candidate"))
        comparison = artifact["comparison"]
        complete = (treatment and all(sides[s]["classification"] != "non-evidence" for s in sides)
                    and comparison["status"] == "compared"
                    and comparison["decision"]["data"]["treatment_integrity"] is True)
        record = {"case": artifact["case"], "iteration": artifact["iteration"],
                  "paired_artifact_evidence_id": artifact["paired_artifact_evidence_id"],
                  "baseline": sides["baseline"]["classification"], "candidate": sides["candidate"]["classification"],
                  "candidate_absolute_pass": sides["candidate"]["classification"] == "pass",
                  "complete_pair_evidence": complete, "comparison": comparison,
                  "failure_codes": {s: {
                      phase: [attempt["failure"]["code"] for attempt in sides[s][phase]["attempts"] if attempt["failure"]]
                      for phase in ("target", "judge")} for s in sides},
                  "judge_contract_failures": {s: sides[s]["judge"].get("contract_failure", {}).get("code") for s in sides},
                  "checks": {s: sides[s]["deterministic_checks"] for s in sides},
                  "timing": {s: sides[s]["timing"] for s in sides},
                  "attempts": {s: {phase: len(sides[s][phase]["attempts"]) for phase in ("target", "judge")} for s in sides}}
        records.append(record)
    return {"schema": "portable-skills/eval-summary/v1", "pairs": records,
            "complete_pairs": sum(r["complete_pair_evidence"] for r in records),
            "candidate_passes": sum(r["candidate_absolute_pass"] for r in records),
            "all_pass": bool(records) and all(r["candidate_absolute_pass"] and r["complete_pair_evidence"] for r in records),
            "cost": "not-estimated; nominal/maximum invocation counts are spend bounds, not token or monetary cost"}


def run_plan(root, runner, options, plan, providers, invoker=None, reporter=None, *, report_root=None):
    # Prepare metadata and runner-owned path identities BEFORE claiming a run.
    # This store value is only a pure path builder until the actual claim below.
    # Malformed input/preflight never fabricates an evaluation report.
    options.artifact_dir = artifact_directory(root, options, plan.run_id)
    path = options.artifact_dir
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError("artifact directory must not traverse symlinks")
    store = runner.eval_artifacts.RunArtifactStore(path, plan.run_id)
    identities = [runner.eval_artifacts.artifact_identity_for_job(plan.run_id, job) for job in plan.jobs]
    manifest = {
        "schema": runner.eval_artifacts.EVAL_RUN_SCHEMA, "run_id": plan.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "selection": {"cases": [j.case.id for j in plan.jobs], "explicit": True}, "iterations": options.iterations,
        "concurrency": {"standard": 0, "runtime": min(options.parallel, len(plan.jobs))},
        "jobs": [{"case": j.case.id, "iteration": j.iteration, "artifact": store.paired_job_relative_path(i).as_posix()}
                 for j, i in zip(plan.jobs, identities)], "summary": {"status": "running"},
        "project_metadata": {"schema": METADATA_SCHEMA, "runner_revision": RUNNER_REVISION,
                             "implementation_sha256": {p.name: digest(p.read_bytes()) for p in sorted((root / "scripts").glob("*.py"))},
                              "repository_head": runner_git_head(root), "working_tree_bytes": True,
                              "report_sources": [{"case": j.case.id, "source_id": j.case.project_data["source_id"],
                                                  "source": j.case.metadata["source"], "source_sha256": j.case.metadata["source_sha256"]}
                                                 for j in plan.jobs],
                              "report_controls": {"model": options.model, "target_transport": options.target_transport,
                                  "judge_model": options.judge_model or options.model, "judge_transport": options.judge_transport,
                                  "reasoning": reasoning_control(options.model, options.target_reasoning or options.reasoning),
                                  "judge_reasoning": reasoning_control(options.judge_model or options.model, options.judge_reasoning or options.reasoning),
                                  "parallel": options.parallel, "inner_timeout": options.timeout_seconds,
                                  "outer_timeout": options.container_timeout, "transport_retries": options.transport_retries,
                                  "engine": options.engine, "network": options.network or "engine-default-live",
                                  "sampling": "provider-default/uncontrolled"},
                              "budget": call_budget(len({j.case.id for j in plan.jobs}), options)},
    }
    sanitizer = runner.evidence_safety.Sanitizer.from_runtime(
        os.environ, json_sources=[options.auth or runner.cli.default_auth_path(),
                                  *([options.provider_config] if options.provider_config else [])],
        database_sources=[options.database or runner.cli.default_database_path()],
        model_catalog_sources=[options.models_catalog] if options.models_catalog else [])
    # report_root is injectable filesystem I/O for provider-free tests, not a CLI
    # option. Normal commands always use the repository root, never the cwd.
    latest_root = Path(report_root or root).resolve(strict=True)
    validate_latest_destination(latest_root)
    store = runner.eval_artifacts.claim_run_artifact_directory(options.artifact_dir, plan.run_id)
    if any(p != store.owner_path for p in store.root.iterdir()):
        raise ValueError("evaluation run already has history; use a fresh artifact directory")
    store.write_run_manifest(manifest)
    options.latest_report_path = latest_root / LATEST_NAME

    def publish():
        try:
            options.report_path = publish_report(runner, store, identities, manifest, summarize, sanitizer, latest_root=latest_root)
        except ReportPublicationError as exc:
            # The output failure must not hide valid evaluation evidence, but it
            # also must not promote an in-memory or now-tampered summary. Reread
            # ownership, every included pair/hash and the aggregate once more.
            _, _, verified, incomplete = read_report_evidence(runner, store, identities, manifest, summarize)
            evaluation_code = None if incomplete else 2 if verified["orchestration_errors"] else 0 if verified["all_pass"] else 1
            if reporter is not None:
                reporter.summary(verified, len(plan.jobs), store.root, report_path=exc.retained_report,
                                 publication=exc.presentation(), evaluation_finalized=not incomplete,
                                 evaluation_exit_code=evaluation_code)
            raise
    try:
        if reporter is not None:
            reporter.start(plan, options, artifact_dir=store.root, latest_report_path=options.latest_report_path)
        outcome = _run_claimed_plan(root, runner, options, plan, providers, store, identities, manifest, invoker, reporter)
    except Exception:
        # Recovery reads only existing verified artifacts. A still-running manifest
        # cannot be promoted into complete run proof; publication fails closed if
        # storage/ownership/integrity cannot be established.
        publish()
        if reporter is not None:
            reporter.report(options.report_path, artifact_dir=store.root, latest_report_path=options.latest_report_path)
        raise
    publish()
    return outcome


def _run_claimed_plan(root, runner, options, plan, providers, store, identities, manifest, invoker, reporter):
    baseline = SkillsProfile(root, runner, options, "baseline", providers)
    candidate = SkillsProfile(root, runner, options, "candidate", providers)
    for profile in (baseline, candidate):
        runner.eval_api.validate_eval_profile(profile)

    def execute(item):
        job, identity = item
        artifact = execute_pair(runner, baseline, candidate, job, plan.run_id, invoker, reporter)
        store.write_paired_job_artifact(identity, artifact)
        durable = store.read_paired_job_artifact(identity)
        if durable["paired_artifact_evidence_id"] != artifact["paired_artifact_evidence_id"]:
            raise ValueError("durable pair differs from just-written evidence")
        return durable

    errors = []
    # Capture completion/failure for every selected job; never cancel on a
    # behavioral negative. Pair sides remain sequential inside the runner.
    with ThreadPoolExecutor(max_workers=options.parallel) as pool:
        futures = {pool.submit(execute, item): item[0] for item in zip(plan.jobs, identities)}
        for future in as_completed(futures):
            job = futures[future]
            try:
                artifact = future.result()
                if reporter is not None:
                    record = summarize(runner, [artifact])["pairs"][0]
                    reporter.pair(runner, artifact, record)
            except Exception as exc:
                error = {"case": job.case.id, "iteration": job.iteration, "error_type": type(exc).__name__}
                errors.append(error)
                if reporter is not None:
                    reporter.orchestration_error(error)
    # Preserve plan order in durable summaries/JSON even though human progress
    # and verified-pair events now report in completion order.
    job_order = {(j.case.id, j.iteration): i for i, j in enumerate(plan.jobs)}
    errors.sort(key=lambda e: job_order[e["case"], e["iteration"]])
    # Re-read again immediately before summary; storage validates nested and pair
    # identities/hashes. No summary relies on the transient in-memory outcome.
    artifacts = [store.read_paired_job_artifact(identity) for identity in identities
                 if not any(e["case"] == identity.case_id and e["iteration"] == identity.iteration for e in errors)]
    summary = summarize(runner, artifacts)
    summary["orchestration_errors"] = errors
    if len(artifacts) != len(plan.jobs) or errors:
        summary["all_pass"] = False
    manifest["summary"] = summary
    store.write_run_manifest(manifest)
    durable = store.read_run_manifest()["summary"]
    if durable != summary:
        raise ValueError("durable summary mismatch")
    return (2 if errors else 0 if durable["all_pass"] else 1), durable


def runner_git_head(root):
    import subprocess
    return subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()


def artifact_directory(root, options, run_id):
    root = Path(root).absolute()
    path = options.artifact_dir or root / ".skill-evals" / run_id
    if not path.is_absolute():
        path = root / path
    if any(path.resolve().is_relative_to(p) for p in (root / "skills", root / "evaluations" / "selective-enrichment")):
        raise ValueError("output must not contaminate skill directories or historical evidence")
    return path


def run_probe(root, runner, options, case, probe=None):
    from eval_probe import probe_configs
    run_id = "probe-" + uuid.uuid4().hex
    path = artifact_directory(root, options, run_id)
    options.artifact_dir = path
    store = runner.eval_artifacts.claim_run_artifact_directory(path, run_id)
    summary = {"schema": "portable-skills/probe/v1", "status": "running", "observations": {},
               "provider_calls": 0, "credential_mounts": False, "network": "none"}
    manifest = {
        "schema": runner.eval_artifacts.EVAL_RUN_SCHEMA, "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(), "selection": {"case": case.id},
        "iterations": 1, "concurrency": {"standard": 0, "runtime": 1}, "jobs": [], "summary": summary,
        "project_metadata": {"schema": METADATA_SCHEMA, "runner_revision": RUNNER_REVISION,
                             "target_image": options.target_image_proof, "case": case.metadata,
                             "implementation_sha256": {p.name: digest(p.read_bytes()) for p in sorted((root / "scripts").glob("*.py"))}},
    }
    store.write_run_manifest(manifest)
    print("Probe artifacts: " + terminal_text(store.root, 800), file=sys.stderr, flush=True)
    def record(side, observation):
        summary["observations"][side] = observation
        store.write_run_manifest(manifest)
    try:
        summary["configs"] = (probe or probe_configs)(root, runner, options, case, record)
        summary["status"] = "verified"
    except Exception as exc:
        summary.update(status="failed", error_type=type(exc).__name__, error=str(exc))
        store.write_run_manifest(manifest)
        if store.read_run_manifest()["summary"] != summary:
            raise ValueError("failed probe durable manifest mismatch") from exc
        # Probe callbacks/host parsers can fail with raw private payloads. Keep
        # those in the unchanged private manifest, not an exception sent to CLI.
        print("retained probe evidence: " + terminal_text(store.run_manifest_path, 800), file=sys.stderr)
        raise ValueError("provider-free probe failed; retained probe evidence") from exc
    store.write_run_manifest(manifest)
    durable = store.read_run_manifest()
    if durable != manifest or store.run_manifest_path.stat().st_mode & 0o777 != 0o600:
        raise ValueError("probe durable manifest/permissions mismatch")
    return {"artifact": str(store.run_manifest_path), "summary": durable["summary"]}


def main(argv=None, *, report_root=None):
    options = parser().parse_args(argv)
    reporter = EvalReporter(json_output=options.json, verbose=options.verbose)
    catalog_lifetime = ExitStack()
    try:
        if not sys.flags.isolated:
            raise ValueError("launch with python3 -I -B (or the Bun aliases); non-isolated imports are not supported")
        if options.harness_test:
            import unittest
            # Pin default resolution for integration tests; tests inject the
            # invocation boundary, never an actual model/provider call.
            os.environ["SKILLS_EVAL_RUNNER_ROOT"] = str(runner_root(options))
            suite = unittest.defaultTestLoader.discover(str(ROOT / "scripts" / "tests"))
            return 0 if unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful() else 1
        cases = discover(ROOT)
        if options.validate:
            if options.target is not None or options.cases is not None or options.all:
                cases = select(cases, options)
            print(json.dumps({"status": "valid", "fixture_cases": len(cases), "skills": len({c.skill for c in cases}), "provider_calls": 0}))
            return 0
        if options.list:
            if options.target is not None or options.cases is not None or options.all:
                cases = select(cases, options)
            for case in cases:
                print(f"{case.id}\tskill:{case.skill}\t{case.skill}:{case.source_id}")
            return 0
        root = runner_root(options)
        selected = select(cases, options)
        if options.probe and options.judge_transport != "opencode":
            raise ValueError("--probe verifies OpenCode configuration only; Copilot runtime proof is separate")
        if not options.probe:
            validate_live(options, selected)
            reporter.budget(call_budget(len(selected), options))
        provider_doc = strict_json(options.provider_config.read_text()) if options.provider_config else {}
        freeze_environment(options)  # once, before any runner imports or parallel work
        runner = load_runner(root)
        if not options.probe:
            try:
                options.models_catalog = catalog_lifetime.enter_context(
                    runner.model_catalog.pinned_model_catalog(options.models_catalog)
                )
            except Exception:
                raise ValueError("model catalog acquisition or validation failed") from None
        providers = compile_provider_settings(provider_doc, runner, os.environ, options.env)
        options.engine = runner.cli.resolve_engine(options.engine)
        options.target_image_proof = verify_image(runner, options.engine, options.opencode_image, "opencode")
        options.target_image_id = options.target_image_proof["image_id"]
        if options.judge_transport == "opencode":
            options.judge_image_proof = options.target_image_proof
        else:
            options.judge_image_proof = verify_image(runner, options.engine, options.copilot_image, "github-copilot-cli")
        options.judge_image_id = options.judge_image_proof["image_id"]
        if options.probe:
            normalized = SkillsProfile(ROOT, runner, options, "candidate", {}).discover_cases()
            case = next(c for c in normalized if c.id == selected[0].id)
            proof = run_probe(ROOT, runner, options, case)
            configs = {side: {k: v for k, v in result.items() if k != "runner_runtime_evidence"}
                       | {"runtime_evidence_status": result["runner_runtime_evidence"]["status"]}
                       for side, result in proof["summary"]["configs"].items()}
            print(json.dumps({"status": "image-and-effective-config-verified", "target": options.target_image_proof,
                              "artifact": proof["artifact"], "configs": configs,
                              "credential_mounts": False, "network": "none", "provider_calls": 0}))
            return 0
        print("Live network/provider execution; not an offline evaluation.",
              file=sys.stderr if options.json else sys.stdout, flush=True)
        if options.network == "host":
            print("WARNING: --network host shares the host network namespace and weakens isolation.", file=sys.stderr)
        run_id = uuid.uuid4().hex
        options.artifact_dir = artifact_directory(ROOT, options, run_id)
        normalized = SkillsProfile(ROOT, runner, options, "candidate", providers).discover_cases()
        plan = runner.eval_plan.build_run_plan(run_id, normalized, selectors=tuple(c.id for c in selected),
                                               iterations=options.iterations, runtime_parallelism=options.parallel)
        code, summary = run_plan(ROOT, runner, options, plan, providers, reporter=reporter, report_root=report_root)
        reporter.summary(summary, len(plan.jobs), options.artifact_dir, report_path=options.report_path,
                         latest_report_path=options.latest_report_path)
        return code
    except ReportPublicationError as exc:
        failure = exc.presentation()["failure"]
        print(f"eval report publication error ({failure['code']}): {failure['message']}", file=sys.stderr)
        return 2
    except (ValueError, OSError, RuntimeError) as exc:
        print(f"eval configuration/orchestration error: {boundary_error(exc)}", file=sys.stderr)
        return 2
    except Exception as exc:
        # Final process boundary: unexpected/storage/subprocess failures must be
        # exit 2, never an accidental success or behavioral negative. Don't dump
        # arbitrary dependency exception payloads that might contain secrets.
        print(f"eval orchestration error ({type(exc).__name__}); no complete run proof", file=sys.stderr)
        return 2
    finally:
        catalog_lifetime.close()


if __name__ == "__main__":
    raise SystemExit(main())
