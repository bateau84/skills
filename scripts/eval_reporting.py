"""Bounded terminal presentation; never grades, edits, or backfills evidence.

Runtime details come only from verified runner artifacts and the runner's already
redacted result fields. Provisional progress uses only numeric/Boolean return
status, never raw invoker payloads or exception text. Host-created diagnostics
require a separate privacy projection: integrity verification is not redaction.
"""
from __future__ import annotations

import json
import re
import sys
import threading
import unicodedata
from pathlib import Path

from eval_cases import strict_json


# Host check/contract/comparison messages are created AFTER the result sanitizer.
# This is an output-origin policy, not credential scrubbing: copy only known
# literal project rationale, never callback exception strings or arbitrary data.
TREATMENT_REASONS = frozenset({
    "unexpected tool execution mode or actor",
    "baseline executed a tool; no skill/reference context is allowed",
    "candidate loaded or attempted a different skill",
    "read has no exact path",
    "read outside selected practitioner files or before native load",
    "complete observation proves selected native skill was not successfully loaded",
    "complete authoritative trace proves expected treatment",
    *(f"required observation field unavailable: {f}" for f in ("tool", "actor", "input")),
    *(f"native skill {f} unavailable" for f in ("result", "terminal_sequence")),
})
PRIVATE_DIAGNOSTIC = "Host diagnostic withheld; integrity verification does not establish redaction."


def boundary_error(exc):
    """Preserve canonical configuration guidance, never arbitrary host payloads."""
    message = str(exc)
    if message == "durable summary mismatch":
        return "durable summary mismatch; no complete run proof"
    literals = {
        "explicit --cases, --target/--skills, or --all required; --target-kind skill is NOT selection",
        "selection matched no cases", "live execution requires explicit --model",
        "live execution requires explicit --model provider/model ID (for example openai/gpt-6.1)",
        "live execution requires explicit --judge-model provider/model ID (for example openai/gpt-6.1)",
        "--model must be a qualified provider/model ID (for example openai/gpt-6.1); got an unqualified or malformed ID",
        "--judge-model must be a qualified provider/model ID (for example openai/gpt-6.1); got an unqualified or malformed ID",
        "empty live selection",
        "transport-retries must be 0–5", "outer timeout must be >=300 and at least inner timeout +60 seconds",
        "cross-transport judge requires explicit --judge-model", "target model#variant conflicts with explicit reasoning",
        "judge model#variant conflicts with explicit reasoning", "output must not contaminate skill directories or historical evidence",
        "launch with python3 -I -B (or the Bun aliases); non-isolated imports are not supported",
        "--probe verifies OpenCode configuration only; Copilot runtime proof is separate",
        "provider-free probe failed; retained probe evidence", "failed probe durable manifest mismatch",
        "EVAL-RESULTS.md publication lock is unsafe; refusing replacement",
        "EVAL-RESULTS.md is unsafe or unreadable; refusing replacement",
        "EVAL-RESULTS.md is not an unmodified generated report; move it explicitly before retrying",
        "EVAL-RESULTS.md changed during publication; refusing replacement",
        "EVAL-RESULTS.md publication/durability failed; per-run evidence retained",
        "probe durable manifest/permissions mismatch", "durable summary mismatch", "durable pair differs from just-written evidence",
        "provider-config accepts only V2 providers (no plugins/MCP/agents/instructions or unknown keys)",
        "image must be an immutable full local image ID or repository@sha256:digest, not a tag",
        "immutable image is not available locally; acquisition/build is explicit and never automatic",
        "runner checkout must be clean (including untracked/ignored files and bytecode)",
        "runner checkout root does not exist or cannot be resolved; provide --runner-root for a clean checkout",
        "cannot start git; install Git and verify --runner-root",
        "git could not inspect runner checkout; verify --runner-root points to a valid checkout",
        "runner-root must be the external checkout root; provide --runner-root pointing to the clean repository root",
        f"runner checkout must be exactly dbbbf2a0740aee7a9e9035cc14a785a9467b8fb1; check out that revision in a dedicated clean checkout",
        "model catalog acquisition or validation failed",
        "model catalog source is unavailable; check --models-catalog or OPENCODE_EVAL_RUNNER_MODELS",
        "pinned runner imports failed; verify the clean checkout and its Python dependencies",
        "unsupported EvalProfile API; use the pinned runner revision",
        "credential inventory import resolved outside pinned checkout; remove conflicting Python imports and retry",
        "no supported container engine found; install podman or docker",
        *(f"{n} must be >=1" for n in ("iterations", "parallel", "timeout_seconds")),
        *(f"{n} must be nonempty without surrounding whitespace" for n in ("reasoning", "target_reasoning", "judge_reasoning", "judge_model")),
        *(f"{n} contains an empty selector" for n in ("--cases", "--target/--skills")),
    }
    if message in literals:
        return message
    for prefix in ("unknown skill target(s):", "unknown case selector(s) for selected targets:",
                   "--env credentials require a runner-inventoried name", "explicit provider env is missing or empty:",
                   "--env is for provider credentials/settings only, not runtime control:"):
        if message.startswith(prefix):
            return prefix.rstrip(":") + "; supplied values withheld"
    if message.startswith("container engine not found:"):
        return "requested container engine is unavailable; install Podman or Docker or select an available --engine"
    if message.startswith("runner import resolved outside pinned checkout"):
        return "runner import resolved outside pinned checkout; use the clean runner root and remove conflicting Python imports"
    return "configuration/orchestration diagnostic withheld; no complete run proof"


def console_check(check, side):
    name, reason = check["name"], check["reason"]
    metadata = {}
    if name == "nonempty-output":
        safe_reason = "target must produce nonempty assistant text" if reason == "target must produce nonempty assistant text" else PRIVATE_DIAGNOSTIC
    elif name == "treatment-integrity":
        metadata = {"side": side}
        safe_reason = reason if reason in TREATMENT_REASONS else PRIVATE_DIAGNOSTIC
        if reason.startswith("unexpected tool: "):
            safe_reason = "unexpected tool execution; tool identity withheld"
    else:
        name = "deterministic_checks_invalid" if name == "deterministic_checks_invalid" else "unrecognized-check"
        safe_reason = PRIVATE_DIAGNOSTIC
    return {"name": name, "status": check["status"], "reason": safe_reason, "metadata": metadata}


def console_record(record):
    """Non-mutating JSON projection: retain field contracts/verdicts, not host payloads."""
    safe = {**record, "checks": {side: [console_check(check, side) for check in checks]
                                for side, checks in record["checks"].items()}}
    comparison = record["comparison"]
    failure = comparison["failure"]
    if failure:
        code = failure["code"]
        if code == "comparison_side_non_evidence":
            sides = [s for s in ("baseline", "candidate") if record[s] == "non-evidence"]
            message = f"comparison unavailable: {', '.join(sides)} side is non-evidence"
        elif code == "comparison_callback_missing":
            message = "paired comparison extension must define compare_pair"
        else:
            code = code if code in {"comparison_input_invalid", "comparison_output_invalid"} else "comparison_invalid"
            message = PRIVATE_DIAGNOSTIC
        safe["comparison"] = {**comparison, "failure": {"code": code, "message": message}}
    return safe


def terminal_text(value, limit=420):
    """Single bounded line, without ANSI/OSC, C0/C1 or bidi/format controls."""
    text = str(value)
    text = re.sub(r"(?:\x1b\]|\x9d)[^\x07\x1b]*(?:\x07|\x1b\\|$)", "", text)
    text = re.sub(r"(?:\x1b\[|\x9b)[0-?]*[ -/]*[@-~]", "", text)
    text = "".join(" " if c.isspace() else c for c in text
                   if c.isspace() or unicodedata.category(c) not in {"Cc", "Cf", "Cs"})
    text = " ".join(text.split())
    return text if len(text) <= limit else text[:limit - 3] + "..."


def runtime_error_detail(result):
    """Pick an error message, never an assistant/tool/prompt/log-stream dump.

    Only called with an integrity-verified final failed attempt. The pinned
    container's final sink sanitizer owns credential redaction, not this parser.
    """
    if not result:
        return ""
    message = ""
    stdout = result.get("stdout")
    stdout = stdout if isinstance(stdout, str) else ""
    for line in stdout[:200000].splitlines()[:1000]:
        if len(line) > 16384:
            continue
        try:
            event = strict_json(line)
        except (ValueError, RecursionError):
            continue
        if not isinstance(event, dict) or event.get("type") != "error":
            continue
        error = event.get("error")
        if isinstance(error, dict) and isinstance(error.get("message"), str):
            message = error["message"]
    # Do not fall back to stdout: it contains private assistant/tool payloads.
    # stderr is already redacted; use only its first diagnostic line, not a dump.
    if not message:
        stderr = result.get("stderr")
        lines = stderr[:20000].strip().splitlines() if isinstance(stderr, str) else []
        if lines and not lines[0].lstrip().startswith(("{", "[")):
            message = lines[0]
    return terminal_text(message)


def invocation_return_state(reply):
    """Provisional adapter-return status from protocol scalars ONLY, not a grade.

    Raw returns have not passed runner validation/redaction. Do not extract text,
    exceptions, prompts, or log fields here; final detail uses verified artifacts.
    """
    if type(reply) is not tuple or len(reply) != 2:
        return "unrecognized"
    host_code, result = reply
    if type(host_code) is not int or type(result) is not dict or type(result.get("exit_code")) is not int:
        return "unrecognized"
    if host_code != 0 or result["exit_code"] != 0 or result.get("infrastructure_error") is True or result.get("timed_out") is True:
        return "reported-error"
    return "returned"


class EvalReporter:
    def __init__(self, *, json_output=False, verbose=False, stream=None):
        self.json_output, self.verbose = json_output, verbose
        self.stream = stream if stream is not None else sys.stdout
        self._lock = threading.Lock()

    def _lines(self, lines):
        with self._lock:
            print("\n".join(lines), file=self.stream, flush=True)

    def _event(self, event):
        self._lines([json.dumps(event, ensure_ascii=False)])

    def budget(self, budget):
        if self.json_output:
            self._event({"event": "live-spend-plan", **budget})
        else:
            self._lines([
                f"Planned: {budget['pairs']} pair(s); nominal {budget['nominal_target_calls']} target + "
                f"{budget['nominal_judge_calls']} judge attempts; maximum "
                f"{budget['maximum_target_calls']} target + {budget['maximum_judge_calls']} judge attempts.",
                "Invocation budget only; provider requests, tokens and monetary cost are unobserved.",
            ])

    def start(self, plan, options, *, artifact_dir=None, latest_report_path=None):
        if self.json_output:
            if artifact_dir is not None:
                self._event({"event": "run-started", "run_id": plan.run_id, "artifact_dir": str(artifact_dir),
                             "latest_report_path": str(latest_report_path)})
        else:
            cases = len({job.case.id for job in plan.jobs})
            self._lines([f"Running {len(plan.jobs)} paired skill eval(s) ({cases} case(s) x "
                         f"{options.iterations} iteration(s)); parallel={options.parallel}; "
                         f"run {terminal_text(plan.run_id, 100)}.",
                         f"Target: opencode/{terminal_text(options.model, 120)}; "
                          f"judge: {options.judge_transport}/{terminal_text(options.judge_model or options.model, 120)}."])
            if artifact_dir is not None:
                self._lines(["Run artifacts: " + terminal_text(artifact_dir, 800),
                             "Latest report after completion: " + terminal_text(latest_report_path, 800)])

    def invocation(self, case, iteration, side, phase, attempt):
        if not self.json_output:
            self._lines([f"{terminal_text(case, 180)}#{iteration} {side} {phase} "
                          f"attempt {attempt} ..."])

    def invocation_finished(self, case, iteration, side, phase, attempt, elapsed, state):
        if not self.json_output:
            label = {"returned": "returned", "reported-error": "returned (reported error)",
                     "unrecognized": "returned (unrecognized response)", "raised": "raised (host error)"}[state]
            self._lines([f"{terminal_text(case, 180)}#{iteration} {side} {phase} "
                         f"attempt {attempt} {label} in {elapsed:.1f}s; verification pending."])

    def orchestration_error(self, error):
        if not self.json_output:
            self._lines([f"{terminal_text(error['case'], 180)}#{error['iteration']} "
                         f"ERROR (orchestration: {terminal_text(error['error_type'], 80)}); no verified pair."])

    def pair(self, runner, raw, record):
        artifact = runner.eval_artifacts.validate_paired_eval_artifact(raw)
        if self.json_output:
            # IDs still refer to the original durable artifact, not this privacy
            # projection. No artifact, verdict, count, or schema is rewritten.
            self._event({"event": "verified-pair", **console_record(record)})
            return
        sides = artifact["sides"]
        def status(side):
            result = sides[side]
            label = {"pass": "PASS", "fail": "FAIL", "non-evidence": "NON-EVIDENCE"}[result["classification"]]
            semantic = result["judge"]["semantic"]
            return label + (f" {semantic['data']['score'] * 100:.0f}%" if semantic else " (score unavailable)")
        lines = [f"{terminal_text(artifact['case'], 180)}#{artifact['iteration']} "
                 f"baseline {status('baseline')} -> candidate {status('candidate')}"]
        decision = artifact["comparison"]["decision"]
        if decision:
            data = decision["data"]
            value = decision["classification"]
            if value == "unattributed":
                lines.append("  Comparison unattributed: treatment integrity failed; scores do not establish skill value.")
            else:
                lines.append(f"  Paired observation: observed {value} ({data['delta_pp']:+.1f} pp); "
                             "policy, not statistical significance.")
                if data["trap_fixed"] or data["trap_regression"]:
                    lines.append("  Trap: " + ("fixed in this pair." if data["trap_fixed"] else "regressed in this pair."))
        else:
            if artifact["comparison"]["status"] == "invalid":
                failure = console_record(record)["comparison"]["failure"]
                lines.append(f"  Comparison unavailable: invalid ({failure['code']}); no attributed improvement/regression.")
            else:
                lines.append("  Comparison unavailable: non-evidence; no attributed improvement/regression.")
        for name, side in sides.items():
            lines.extend(self._side_details(name, side))
        self._lines(lines)

    def _side_details(self, name, side):
        lines = []
        for phase in ("target", "judge"):
            attempts = side[phase]["attempts"]
            if attempts and attempts[-1]["failure"]:
                last = attempts[-1]
                code = terminal_text(last["failure"]["code"], 80)
                detail = runtime_error_detail(last["result"])
                # Failure messages may hold unredacted host exception payloads.
                lines.append(f"  {name} {phase}: {code}" + (f" — {detail}" if detail else "; no safe runtime detail available."))
            if self.verbose:
                for attempt in attempts[:8]:
                    failure = attempt["failure"]
                    outcome = terminal_text(failure["code"], 80) if failure else "returned"
                    lines.append(f"  {name} {phase} attempt {attempt['attempt']}: {outcome}, "
                                 f"{attempt['duration_seconds']:.1f}s; host exit {attempt['host_exit_code']}.")
                    retry = attempt.get("retry_decision")
                    if retry:
                        lines.append(f"  {name} {phase} retry: {'scheduled' if retry['retry'] else 'not scheduled'}; "
                                     f"replay-safe={'yes' if failure and failure['retry_safe'] else 'no'}.")
                if len(attempts) > 8:
                    lines.append(f"  {len(attempts) - 8} further attempts retained in artifact.")
        if side["judge"].get("contract_failure"):
            code = side["judge"]["contract_failure"]["code"]
            code = code if code in {"judge_spec_invalid", "judge_contract_invalid"} else "judge_contract_failure"
            lines.append(f"  {name} judge: {code} — judge specification/response/no-tool evidence did not satisfy the contract; host diagnostic withheld.")
        checks = [c for c in side["deterministic_checks"] if c["status"] != "pass"]
        for check in checks[:3]:
            safe = console_check(check, name)
            lines.append(f"  {name} {safe['name']}: "
                         f"{safe['status']} — {safe['reason']}")
        semantic = side["judge"]["semantic"]
        if semantic and semantic["status"] == "fail":
            grade = semantic["data"]["grade"]
            unmet = [e for e in grade["expectations"] if not e["met"]]
            forbidden = [e for e in grade["violations"] if e["violated"]]
            counts = []
            if grade["expectations"]:
                counts.append(f"{len(unmet)}/{len(grade['expectations'])} positive criteria unmet")
            if grade["violations"]:
                counts.append(f"{len(forbidden)}/{len(grade['violations'])} forbidden criteria violated")
            if counts:
                lines.append(f"  {name}: " + "; ".join(counts) + ".")
            for item in (unmet + forbidden)[:3]:
                lines.append(f"  {name} {terminal_text(item['id'], 40)}: {terminal_text(item['evidence'])}")
            if len(unmet + forbidden) > 3:
                lines.append("  Further criterion rationales retained in artifact.")
            if grade["trap_observed"]:
                lines.append(f"  {name} trap: {terminal_text(grade['trap_evidence'])}")
            if not unmet and not forbidden and not grade["trap_observed"]:
                lines.append(f"  {name} judge: {terminal_text(semantic['summary'])}")
            if semantic["data"]["score"] == 0:
                lines.append("  Zero is a criterion-level score (criteria can be compound), not a claim every statement was wrong.")
        return lines

    def report(self, path, *, artifact_dir=None, latest_report_path=None):
        if self.json_output:
            self._event({"event": "results-report", "report_path": str(path),
                         **({"artifact_dir": str(artifact_dir)} if artifact_dir is not None else {}),
                         **({"latest_report_path": str(latest_report_path)} if latest_report_path is not None else {})})
        else:
            lines = ["Run artifacts: " + terminal_text(artifact_dir, 800)] if artifact_dir is not None else []
            lines.append("Report: " + terminal_text(path, 800))
            if latest_report_path is not None:
                lines.append("Latest report: " + terminal_text(latest_report_path, 800))
            self._lines(lines)

    def summary(self, summary, expected, artifact_dir, *, report_path=None, latest_report_path=None,
                publication=None, evaluation_finalized=True, evaluation_exit_code=None):
        if self.json_output:
            self._event({"event": "verified-summary", "artifact_dir": str(artifact_dir),
                         **({"report_path": str(report_path)} if report_path is not None else {}),
                         **({"latest_report_path": str(latest_report_path)} if latest_report_path is not None else {}),
                         **({"report_publication": publication, "evaluation_finalized": evaluation_finalized,
                             "evaluation_exit_code": evaluation_exit_code} if publication is not None else {}),
                         **summary, "pairs": [console_record(record) for record in summary["pairs"]]})
            return
        records = summary["pairs"]
        counts = {phase: sum(r["attempts"][side][phase] for r in records for side in ("baseline", "candidate"))
                  for phase in ("target", "judge")}
        errors = len(summary.get("orchestration_errors", []))
        label = "Completed" if evaluation_finalized else "Partial"
        lines = [f"{label}: {len(records)}/{expected} verified pair artifact(s); "
                 f"{summary['complete_pairs']} complete evidence pair(s); "
                 f"{summary['candidate_passes']} candidate PASS; {errors} orchestration error(s).",
                 f"Observed attempts: {counts['target']} target + {counts['judge']} judge "
                  "in verified artifacts" + (" (partial; failed jobs may have additional attempts)." if errors or not evaluation_finalized else "."),
                 "Provider requests, tokens and monetary cost: unobserved.",
                 "Run artifacts: " + terminal_text(Path(artifact_dir).resolve(), 800),
                 "Manifest: " + terminal_text(Path(artifact_dir).resolve() / "run.json", 800)]
        self._lines(lines)
        if report_path is not None:
            self.report(report_path, latest_report_path=latest_report_path)
        if publication is not None:
            failure = publication["failure"]
            self._lines(["Evaluation aggregate: " + (f"finalized; evaluation exit {evaluation_exit_code}." if evaluation_finalized else
                                                     "incomplete; no complete run proof."),
                         f"Reports: per-run {publication['per_run']}; latest {publication['latest']}.",
                         f"Report publication failed ({failure['code']}): {failure['message']}"])
