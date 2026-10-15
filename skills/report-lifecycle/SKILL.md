---
name: report-lifecycle
description: Create concise execution reports with faithful findings, evidence, uncertainty, and provenance. Use when later retrieval, audit, or handoff needs a file report; ordinary in-session findings do not require one.
---

# Report Lifecycle

Reports record observed work; persistence alone does not approve their conclusions.

## When to persist

Prefer an in-session summary. Create a file only when the assignment, later retrieval, audit trail, or another consumer materially benefits from one.

## Method

1. Choose a non-colliding location according to repository conventions. For temporary reports, use the host's supported scratch location and avoid accidentally staging them.
2. Record title, purpose, date/context, producing agent or author when known, scope, findings, evidence, uncertainty, and outstanding work. Use local frontmatter/schema only when the repository requires it.
3. Separate observed results from hypotheses and recommendations. Include exact verification commands and outcomes when consequential; do not describe unrun checks as passed.
4. Verify the file exists, is readable, and any evidence links resolve. If a repository index or schema validator is used, validate it before claiming indexed discoverability; plain file handoff requires no indexing service.
5. Keep verdict, evidence, uncertainty, provenance, and provisional wording faithful to the work. A valid file is not proof that its conclusions are correct.
6. Handoff the report path with a compact summary of results and limitations.

## Retention

Temporary reports remain temporary unless the user or repository needs lasting history. Use `report-to-keep` for retention decisions. Preserve durable conclusions in the project's appropriate requirements, design, architecture, or documentation records; do not silently make a raw report substitute for an agreed decision.
