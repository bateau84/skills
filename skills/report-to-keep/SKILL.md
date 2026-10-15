---
name: report-to-keep
description: Decide whether a temporary report deserves durable repository retention and preserve it faithfully. Use when the user asks to keep, preserve, commit, or promote a report.
---

# Report to Keep

Retention preserves history; it does not make findings more authoritative.

## Method

1. Locate and read the intended report with available file or search tools. Confirm its identity, author/context, evidence, and provisional status; use `report-lifecycle` when checking report quality.
2. Decide whether the report itself has lasting documentary or audit value. Current usefulness alone is not enough.
3. If only a conclusion is durable, incorporate it into the appropriate project document through the normal decision process instead of preserving the raw report as substitute authority.
4. If retention is warranted, choose a non-colliding destination under the repository's report convention, for example `docs/reports/`. No producer-specific namespace is required.
5. Copy the report unchanged with an available file tool. Preserve the source, never overwrite an existing report, and verify the destination matches the source. If no file-copy tool exists, a byte-preserving write followed by comparison is sufficient.
6. State what was retained, where, and why. Commit only when the user or active instructions request a commit.

## Preservation semantics

- Preserve verdicts, confidence, provisional wording, dates, and provenance.
- A failed review remains failed after retention.
- Retention does not turn findings into requirements, approval, architecture, product truth, or stronger evidence.
- Make corrections as explicit follow-up records rather than silently rewriting historical findings.

## Usually keep temporary

- routine review/QA output;
- superseded failure reports whose findings have been corrected;
- one-off design validation or debugging notes;
- transient research incorporated into another durable artifact;
- run summaries reproducible from retained evidence.

## Plausible retention cases

- explicit audit evidence required by the project;
- a postmortem or investigation intentionally kept as history;
- a research dossier maintained as a project artifact;
- a report the user explicitly wants preserved.
