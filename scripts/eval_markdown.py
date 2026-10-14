"""Deterministic, private report projection of reread runner-owned evidence.

No model calls, grades, or replacement artifact authority. The pinned store has
no public text-publication API; only this fixed sibling file uses a small atomic,
no-clobber text sink. All JSON reads and integrity checks remain runner-owned.
"""
from __future__ import annotations

import fcntl
import hashlib
import io
import os
import re
import stat
import uuid
from contextlib import contextmanager
from urllib.parse import quote

from eval_cases import strict_json
from eval_reporting import EvalReporter, terminal_text

REPORT_NAME = "results.md"
REPORT_TITLE = "# Skill evaluation results"
LATEST_NAME = "EVAL-RESULTS.md"
LATEST_LOCK = ".EVAL-RESULTS.lock"
LATEST_MARKER = "portable-skills/eval-latest/v1"
LATEST_HEADER = re.compile(re.escape(f"<!-- {LATEST_MARKER} sha256=".encode()) + rb"([0-9a-f]{64}) -->\n")


PUBLICATION_FAILURES = {
    "per_run_report_collision": "Per-run results.md already exists; refusing to overwrite it.",
    "per_run_report_write_failed": "Per-run results.md could not be written; host diagnostic withheld.",
    "per_run_report_durability_failed": "Per-run results.md durability could not be confirmed; a complete file may be visible.",
    "latest_report_lock_unsafe": "EVAL-RESULTS.md publication lock is unsafe; refusing replacement",
    "latest_report_destination_unsafe": "EVAL-RESULTS.md is unsafe or unreadable; refusing replacement",
    "latest_report_destination_unrecognized": "EVAL-RESULTS.md is not an unmodified generated report; move it explicitly before retrying",
    "latest_report_changed": "EVAL-RESULTS.md changed during publication; refusing replacement",
    "latest_report_write_failed": "EVAL-RESULTS.md publication/durability failed; per-run evidence retained",
    "latest_report_durability_failed": "EVAL-RESULTS.md durability could not be confirmed; per-run evidence retained and a complete root file may be visible.",
}


class ReportPublicationError(ValueError):
    """Operation-owned safe diagnostics, never arbitrary caught exception text."""
    def __init__(self, code):
        super().__init__(PUBLICATION_FAILURES[code])
        self.code = code
        self.retained_report = None
        self.per_run_status = "failed"
        self.latest_status = "not-written"

    def presentation(self):
        return {"per_run": self.per_run_status, "latest": self.latest_status,
                "failure": {"code": self.code, "message": PUBLICATION_FAILURES[self.code]}}


class LatestReportError(ReportPublicationError):
    def __init__(self, message=None, *, code=None):
        if code is None:
            code = next(key for key, value in PUBLICATION_FAILURES.items() if key.startswith("latest_") and value == message)
        super().__init__(code)
        self.per_run_status = "not-written"
        self.latest_status = "failed"


def markdown_text(value, sanitizer, limit=600):
    # Redact BEFORE clipping/flattening/escaping, including host-origin metadata.
    safe, _ = sanitizer.redact_text(str(value))
    text = terminal_text(safe, limit)
    # Encode syntax as entities, not raw HTML or backslash-dependent constructs.
    # In particular pipes, newlines, brackets, backticks and angle brackets cannot
    # manufacture tables, headings, links, HTML or code blocks.
    return "".join(f"&#{ord(c)};" if c in "\\`*_{}[]()<>#+!|&~:=" else c for c in text)


def evidence_link(store, path, label, sanitizer, link_base=None):
    path.relative_to(store.root)  # Validate ownership separately from URL rebasing.
    if any(p.is_symlink() for p in (path, *path.parents) if p.is_relative_to(store.root)):
        raise ValueError("report evidence link is a symlink")
    if not path.is_file() or not path.resolve().is_relative_to(store.root.resolve()):
        raise ValueError("report evidence link is outside run ownership")
    # Do not put an inventoried credential into a URL (escaping is not redaction).
    relative = os.path.relpath(path, link_base or store.root)
    if sanitizer.redact_text(relative)[1]:
        return markdown_text(label + " (path withheld)", sanitizer)
    return f"[{markdown_text(label, sanitizer)}]({quote(relative, safe='/')})"


def render_report(runner, store, manifest, artifacts, summary, sanitizer, *, incomplete=False, link_base=None):
    md = lambda value, limit=600: markdown_text(value, sanitizer, limit)
    records = summary["pairs"]
    planned = len(manifest["jobs"])
    errors = summary["orchestration_errors"]
    metadata = manifest.get("project_metadata", {})
    lines = [REPORT_TITLE, "",
             "Deterministic projection of reread, integrity-verified artifacts; no regrade or new model summary.", "",
             f"- Run: {md(manifest['run_id'])}",
             f"- Run artifacts (relative to this report): {md(os.path.relpath(store.root, link_base or store.root))}",
             f"- Created (observed): {md(manifest['created_at'])}",
             f"- Repetitions: {manifest['iterations']}; effective pair concurrency: {manifest['concurrency']['runtime']}",
             f"- Runner revision: {md(metadata.get('runner_revision', 'unavailable'))}",
             f"- Repository HEAD: {md(metadata.get('repository_head', 'unavailable'))}; provenance uses working-tree bytes, not HEAD alone."]
    if metadata.get("replay"):
        lines.append("- Replay of saved evidence, not a new evaluation run.")
    controls = metadata.get("report_controls", {})
    if controls:
        lines.extend(["", "## Run settings", ""])
        for key in ("target_transport", "model", "judge_transport", "judge_model", "reasoning", "judge_reasoning",
                    "parallel", "inner_timeout", "outer_timeout", "transport_retries", "engine", "network", "sampling"):
            if key in controls:
                value = controls[key]
                if key in {"reasoning", "judge_reasoning"}:
                    value = f"{value['level']} ({value['source']})"
                lines.append(f"- {md(key)}: {md(value if value is not None else 'provider-default')}")
    lines.extend(["", "## Candidate absolute results", "",
                  f"- Verified pair artifacts: {len(records)}/{planned}; complete usable pair evidence: {summary['complete_pairs']}.",
                  f"- Candidate PASS: {summary['candidate_passes']}; FAIL: {sum(r['candidate'] == 'fail' for r in records)}; "
                  f"NON-EVIDENCE: {sum(r['candidate'] == 'non-evidence' for r in records)}; no verified pair: {planned - len(records)}.",
                  "- Run outcome: " + ("INCOMPLETE — no complete run proof." if incomplete or errors else
                                        "PASS." if summary["all_pass"] else "NOT PASS — behavioral negative, non-evidence, or incomplete pair/comparison proof."),
                  "- FAIL is a behavioral negative; NON-EVIDENCE is unusable/missing proof, not a zero score.",
                  "", "## Paired comparison", "",
                  "Observed pair policy only (unchanged 10pp/trap threshold), not statistical significance, discovery, or general superiority.",
                  "Candidate absolute PASS is separate from baseline performance and relative value. Treatment failure prevents attribution."])
    values = {}
    for record in records:
        comparison = record["comparison"]
        value = comparison["decision"]["classification"] if comparison["decision"] else "unavailable"
        values[value] = values.get(value, 0) + 1
    lines.append("- " + ("; ".join(f"{md(k)}: {v}" for k, v in sorted(values.items())) or "No verified comparisons."))
    counts = {phase: sum(r["attempts"][s][phase] for r in records for s in ("baseline", "candidate"))
              for phase in ("target", "judge")}
    budget = metadata.get("budget", {})
    lines.extend(["", "## Execution and coverage", "",
                  f"- Observed attempts in verified artifacts: {counts['target']} target + {counts['judge']} judge" +
                  (" (partial; failed jobs may have additional unrecorded attempts)." if errors or incomplete else ".")])
    if budget:
        lines.append(f"- Planned nominal: {budget['nominal_target_calls']} target + {budget['nominal_judge_calls']} judge; "
                     f"maximum: {budget['maximum_target_calls']} target + {budget['maximum_judge_calls']} judge attempts.")
    lines.extend(["- Provider HTTP requests, tokens and monetary cost: unobserved. Native invocations may contain multiple model/tool steps.",
                  "- Coverage is the explicit selected cases/repetitions only; missing jobs are not fabricated PASS rows.",
                  "", "## Cases (plan order)", "",
                  "| Case / iteration | Baseline | Candidate | Paired observation | Evidence |",
                  "| --- | --- | --- | --- | --- |"])
    by_key = {(a["case"], a["iteration"]): a for a in artifacts}
    for job in manifest["jobs"]:
        key = (job["case"], job["iteration"])
        artifact = by_key.get(key)
        name = f"{md(key[0])} / {key[1]}"
        if artifact is None:
            lines.append(f"| {name} | unavailable | unavailable | no verified pair; orchestration incomplete | unavailable |")
            continue
        def status(side):
            data = artifact["sides"][side]
            semantic = data["judge"]["semantic"]
            score = f"{semantic['data']['score'] * 100:.0f}%" if semantic else "score unavailable"
            return f"{data['classification'].upper()} {score}"
        decision = artifact["comparison"]["decision"]
        observation = "unavailable; non-evidence or invalid comparison"
        if decision:
            observation = decision["classification"]
            if observation != "unattributed":
                observation += f" ({decision['data']['delta_pp']:+.1f} pp)"
        link = evidence_link(store, store.root / job["artifact"], "paired JSON", sanitizer, link_base)
        lines.append(f"| {name} | {status('baseline')} | {status('candidate')} | {md(observation)} | {link} |")
    lines.extend(["", "## Decisive details and provenance", ""])
    for artifact in artifacts:
        key = (artifact["case"], artifact["iteration"])
        lines.extend([f"### {md(key[0])} / {key[1]}", ""])
        # Share the origin-aware terminal projection (including callback masking),
        # then escape its safe lines for Markdown. Never copy arbitrary JSON text.
        stream = io.StringIO()
        record = next(r for r in records if (r["case"], r["iteration"]) == key)
        EvalReporter(stream=stream).pair(runner, artifact, record)
        lines.extend("- " + md(line.strip()) for line in stream.getvalue().splitlines()[1:])
        if artifact["comparison"]["status"] == "invalid":
            lines.append("- Comparison host diagnostics withheld; integrity verification does not establish redaction.")
        candidate = artifact["sides"]["candidate"]
        provenance = candidate["project_metadata"]
        source = next((s for s in metadata.get("report_sources", []) if s["case"] == key[0]), {})
        if source:
            lines.append(f"- Source identifier: {md(source['source_id'])}")
        for field in ("source_id", "source", "source_sha256", "rubric_sha256", "effective_config_sha256"):
            if field in provenance:
                lines.append(f"- {md(field)}: {md(provenance[field])}")
        lines.append(f"- Paired artifact SHA-256: {md(artifact['paired_artifact_evidence_id'])}")
        for side in ("baseline", "candidate"):
            timing = artifact["sides"][side]["timing"]
            for field in ("started_at", "finished_at", "duration_seconds"):
                if timing.get(field) is not None:
                    lines.append(f"- {side} {md(field)} (observed): {md(timing[field])}")
        lines.append("")
    if errors or incomplete:
        lines.extend(["## Unverified execution", "",
                      "Run orchestration did not establish complete evidence. Host diagnostics are withheld; retained private JSON may contain more detail."])
        for error in errors:
            lines.append(f"- {md(error['case'])} / {error['iteration']}: no verified pair.")
    lines.extend(["", "## Retained evidence and privacy", "",
                  evidence_link(store, store.run_manifest_path, "Run manifest and detailed summary", sanitizer, link_base), "",
                  "Report permissions default to 0600: metadata and safe reasons can still be private. "
                  "Linked raw JSON is private operational evidence and can contain unredacted host diagnostics. "
                  "Do not publish it; integrity IDs are not credential-privacy certification.", ""])
    return "\n".join(lines)


def _publish_text(store, text):
    """Atomic create-only publication in the already claimed directory on Linux."""
    try:
        directory = os.open(store.root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
    except OSError as exc:
        raise ReportPublicationError("per_run_report_write_failed") from exc
    temporary = ".results-" + uuid.uuid4().hex + ".tmp"
    operation = "write"
    def assert_owner():
        owner_fd = os.open(store.owner_path.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
        with os.fdopen(owner_fd, "r", encoding="utf-8") as stream:
            if strict_json(stream.read()) != {"run_id": store.run_id}:
                raise ValueError("report run ownership mismatch")
    try:
        # Bind the final sink to the same owner inode/directory, not a resolved
        # symlink destination. Recheck ownership immediately before publication.
        assert_owner()
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(text)
            stream.flush()
            operation = "durability"
            os.fsync(stream.fileno())
        # link is atomic and fails on ANY existing destination, even a dangling
        # symlink. replace() would incorrectly overwrite prior reports/history.
        operation = "write"
        assert_owner()
        operation = "publish"
        os.link(temporary, REPORT_NAME, src_dir_fd=directory, dst_dir_fd=directory, follow_symlinks=False)
        operation = "write"
        os.unlink(temporary, dir_fd=directory)
        operation = "durability"
        os.fsync(directory)
    except OSError as exc:
        code = ("per_run_report_collision" if operation == "publish" and isinstance(exc, FileExistsError) else
                "per_run_report_durability_failed" if operation == "durability" else "per_run_report_write_failed")
        raise ReportPublicationError(code) from exc
    finally:
        try:
            os.unlink(temporary, dir_fd=directory)
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise ReportPublicationError("per_run_report_write_failed") from exc
        finally:
            os.close(directory)
    return store.root / REPORT_NAME


@contextmanager
def _latest_lock(root):
    """Serialize cooperating whole commands, using a stable private Linux flock."""
    directory = lock = None
    try:
        directory = os.open(root, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
        lock = os.open(LATEST_LOCK, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK,
                       0o600, dir_fd=directory)
        info = os.fstat(lock)
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1 or info.st_size != 0:
            raise LatestReportError("EVAL-RESULTS.md publication lock is unsafe; refusing replacement")
        os.fchmod(lock, 0o600)
        fcntl.flock(lock, fcntl.LOCK_EX)
    except OSError as exc:
        if lock is not None:
            os.close(lock)
        if directory is not None:
            os.close(directory)
        raise LatestReportError("EVAL-RESULTS.md publication lock is unsafe; refusing replacement") from exc
    except LatestReportError:
        if lock is not None:
            os.close(lock)
        if directory is not None:
            os.close(directory)
        raise
    try:
        yield directory
    finally:
        # Closing releases flock. Never unlink its inode while another writer
        # may already be waiting on it (that would allow two independent locks).
        os.close(lock)
        os.close(directory)


def _latest_signature(directory):
    try:
        info = os.stat(LATEST_NAME, dir_fd=directory, follow_symlinks=False)
    except FileNotFoundError:
        return None
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns, info.st_ctime_ns)


def _check_latest(directory):
    """A checksum marker identifies unedited generated content, not authenticity."""
    before = _latest_signature(directory)
    if before is None:
        return None
    try:
        fd = os.open(LATEST_NAME, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=directory)
    except OSError as exc:
        raise LatestReportError("EVAL-RESULTS.md is unsafe or unreadable; refusing replacement") from exc
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        os.close(fd)
        raise LatestReportError("EVAL-RESULTS.md is unsafe or unreadable; refusing replacement")
    with os.fdopen(fd, "rb") as source:
        header = source.readline(200)
        marker = LATEST_HEADER.fullmatch(header)
        if marker is None:
            raise LatestReportError("EVAL-RESULTS.md is not an unmodified generated report; move it explicitly before retrying")
        digest = hashlib.sha256()
        title = source.readline(100)
        if title != (REPORT_TITLE + "\n").encode():
            raise LatestReportError("EVAL-RESULTS.md is not an unmodified generated report; move it explicitly before retrying")
        digest.update(title)
        for chunk in iter(lambda: source.read(65536), b""):
            digest.update(chunk)
        if digest.hexdigest().encode() != marker[1] or before != _latest_signature(directory):
            raise LatestReportError("EVAL-RESULTS.md is not an unmodified generated report; move it explicitly before retrying")
    return before


def validate_latest_destination(root):
    """Reject ambiguous/unsafe existing root content before inference starts."""
    with _latest_lock(root) as directory:
        _check_latest(directory)


def _publish_latest(directory, text):
    temporary = ".EVAL-RESULTS-" + uuid.uuid4().hex + ".tmp"
    operation = "write"
    try:
        before = _check_latest(directory)
        body = text.encode("utf-8")
        header = f"<!-- {LATEST_MARKER} sha256={hashlib.sha256(body).hexdigest()} -->\n".encode()
        fd = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=directory)
        with os.fdopen(fd, "wb") as stream:
            os.fchmod(stream.fileno(), 0o600)
            stream.write(header + body)
            stream.flush()
            operation = "durability"
            os.fsync(stream.fileno())
        operation = "write"
        if before != _latest_signature(directory):
            raise LatestReportError("EVAL-RESULTS.md changed during publication; refusing replacement")
        os.replace(temporary, LATEST_NAME, src_dir_fd=directory, dst_dir_fd=directory)
        operation = "durability"
        os.fsync(directory)
    except OSError as exc:
        code = "latest_report_durability_failed" if operation == "durability" else "latest_report_write_failed"
        raise LatestReportError(code=code) from exc
    finally:
        try:
            os.unlink(temporary, dir_fd=directory)
        except FileNotFoundError:
            pass
        except OSError as exc:
            raise LatestReportError(code="latest_report_write_failed") from exc


def read_report_evidence(runner, store, identities, expected_manifest, summarize):
    """One integrity-checked snapshot, also used to verify failed-publication output."""
    manifest = store.read_run_manifest()
    if manifest != expected_manifest:
        raise ValueError("durable summary mismatch")
    incomplete = manifest["summary"].get("status") == "running"
    errors = manifest["summary"].get("orchestration_errors", [])
    artifacts = []
    recovered_errors = []
    for identity, job in zip(identities, manifest["jobs"], strict=True):
        if job != {"case": identity.case_id, "iteration": identity.iteration,
                   "artifact": store.paired_job_relative_path(identity).as_posix()}:
            raise ValueError("report job identity mismatch")
        missing = any(e["case"] == identity.case_id and e["iteration"] == identity.iteration for e in errors)
        if incomplete and not store.paired_job_path(identity).exists() and not store.paired_job_path(identity).is_symlink():
            missing = True
            recovered_errors.append({"case": identity.case_id, "iteration": identity.iteration})
        if not missing:
            artifacts.append(store.read_paired_job_artifact(identity))
    summary = summarize(runner, artifacts)
    summary["orchestration_errors"] = errors + recovered_errors
    if len(artifacts) != len(identities) or errors or incomplete:
        summary["all_pass"] = False
    if not incomplete and summary != manifest["summary"]:
        raise ValueError("durable summary mismatch")
    return manifest, artifacts, summary, incomplete


def publish_report(runner, store, identities, expected_manifest, summarize, sanitizer, *, latest_root=None):
    """Reread all sources, reject tampering/false summaries, then publish once."""
    manifest, artifacts, summary, incomplete = read_report_evidence(runner, store, identities, expected_manifest, summarize)
    text = render_report(runner, store, manifest, artifacts, summary, sanitizer, incomplete=incomplete)
    if latest_root is None:
        return _publish_text(store, text)
    # One verified snapshot, one renderer, two locations. Rebase actual evidence
    # links at render time, never substitute prefixes in arbitrary Markdown text.
    latest = render_report(runner, store, manifest, artifacts, summary, sanitizer,
                           incomplete=incomplete, link_base=latest_root)
    latest += "\nLatest report-published run, not newest start. Per-run history remains unchanged.\n\n"
    retained = None
    try:
        with _latest_lock(latest_root) as directory:
            retained = _publish_text(store, text)
            # The report now exists: link it only after owned publication.
            latest += evidence_link(store, retained, "Immutable per-run report", sanitizer, latest_root) + "\n"
            _publish_latest(directory, latest)
    except LatestReportError as exc:
        # A refused root replacement must not destroy valid per-run history.
        if retained is None:
            try:
                retained = _publish_text(store, text)
            except ReportPublicationError as per_run_error:
                per_run_error.latest_status = "failed"
                raise
        exc.retained_report = retained
        exc.per_run_status = "published"
        raise
    return retained
