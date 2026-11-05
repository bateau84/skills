# Vocabulary maintenance with real files and a fresh handoff

This is a manual artifact exercise, separate from the JSON response evaluations.
The ordinary `run_evals.py` profile supplies read-only practitioner files and
forbids file mutation and delegation; it cannot execute this exercise. Running
the JSON fixtures or describing edits does not establish a pass here.

Use an isolated writable copy of the inputs below. Supply the practitioner
`SKILL.md` and the task to a fresh agent with ordinary file tools. Do not provide
these evaluator checks, other agents' conversations, or expected results.
Only the fixture's documentation and index may change; no external services,
code, API changes, or Git publication are involved.

## Phase 1: documentation maintenance

Task:

> Improve the backup documentation. The guide and architecture explanation use
> inconsistent outcome language. Make the affected documents clear and
> consistent with the accepted requirements, and leave a concise maintenance
> handoff for the next person. Use the ubiquitous-language skill. Read the
> project's instructions and documents. You may edit only this project's
> documentation and index. Return actual changed paths and anything still
> needing a decision.

## Phase 2: fresh recipient

Copy the resulting project into a new working directory. Start a different fresh
agent with that copy, the same practitioner skill, and this task only. Do not pass
the first agent's chat, final answer, or these evaluator checks.

> Continue from docs/backup/maintenance.md. Add a short troubleshooting section
> to the user guide explaining a failed copy and a verified successful backup.
> Use the existing project documentation and vocabulary. Update the maintenance
> handoff with what you checked and anything still needing a decision. Use the
> ubiquitous-language skill. Documentation edits only.

## Evidence to inspect

- Phase 1 creates a small backup vocabulary and makes it discoverable from the
  affected documents or index. The important terms do not remain only in chat.
- Finished and Succeeded retain the accepted D-7, BR-12 and BR-13 meanings and
  source links, including an unsuccessful finished execution.
- Cancelled remains unresolved with both draft sources, a distinguishing example,
  consequence, needed decision, and unknown owner. No agent invents acceptance.
- The recipient finds and reuses the existing vocabulary, preserves the open
  cancellation question, and completes the independent troubleshooting edit.
- Accepted decision and requirement meanings, IDs, sources, and verification
  obligations stay intact; adding a useful vocabulary link is allowed. Draft
  proposals remain proposals. Neither runtime behavior nor API compatibility is
  claimed verified.
- Inspect the actual files, links, diff and accessible handoff, not just a final
  claim that the work was done. Check for a competing vocabulary or broken links.

Record the skill revision or content hash each participant actually read, the
input fixture, changed paths, checks performed, and any remaining limits. A
successful rehearsal demonstrates only these artifacts and tasks. It does not
prove automatic discovery, the deployed agent prompts, native OpenCode skill
loading, Loom record/routing behavior, or performance across models.

## Input project

The inventory below is complete and initially contains no vocabulary document.
Create each file at its shown path in the isolated project.

### `AGENTS.md`

```markdown
# Documentation conventions
Backup domain documents belong in `docs/backup/` and are linked from README.md.
Accepted requirements and decisions retain their IDs and sources. Draft notes do not establish accepted behavior.
This assignment permits documentation edits only. Runtime code, APIs and stored formats are outside scope.
Use `docs/backup/maintenance.md` for a short handoff of this documentation work.
```

### `README.md`

```markdown
# Local backup
- [Accepted decision](docs/backup/decision.md)
- [Requirements](docs/backup/requirements.md)
- [User guide](docs/backup/guide.md)
- [Architecture explanation](docs/backup/architecture.md)
- [Cancellation design draft](docs/backup/cancel-design-draft.md)
- [Cancellation product draft](docs/backup/cancel-product-draft.md)
- [Maintenance notes](docs/backup/maintenance.md)
```

### `docs/backup/architecture.md`

```markdown
# Architecture explanation
This explanation describes the accepted [requirements](requirements.md).
The execution is Done when the requested backup outcome has been verified.
A failed execution can stop without becoming Done.
Cancelled means the execution has stopped, following the [product draft](cancel-product-draft.md).
```

### `docs/backup/cancel-design-draft.md`

```markdown
# Cancellation design note
Status: draft; no accepted cancellation decision.
Proposal: Cancelled means that stopping has been requested, even if copying continues briefly.
```

### `docs/backup/cancel-product-draft.md`

```markdown
# Cancellation product note
Status: draft; no accepted cancellation decision.
Proposal: Cancelled means the execution has actually stopped.
No decision owner has been assigned for resolving these proposals.
```

### `docs/backup/decision.md`

```markdown
# D-7 — Local backup outcome language
Status: accepted by the product owner.
Finished means backup execution has stopped, including after failure.
Succeeded means the requested backup outcome has been verified.
A finished execution need not have succeeded.
This decision does not settle cancellation terminology.
```

### `docs/backup/guide.md`

```markdown
# User guide
The word Done means the backup has stopped running. A failed copy can still be Done.
For a successfully verified backup, the guide also says Done.
A requested cancellation is called Cancelled here, following the [design draft](cancel-design-draft.md).
```

### `docs/backup/maintenance.md`

```markdown
# Documentation maintenance
Record the result of the current documentation task here for the next maintainer.
```

### `docs/backup/requirements.md`

```markdown
# Accepted backup requirements
## BR-12 — Finished execution
Source: [D-7](decision.md)
Status: accepted.
An execution is Finished once it has stopped, whether normally or after failure.
Verification: check normal stop and failed-copy cases.
## BR-13 — Verified backup outcome
Source: [D-7](decision.md)
Status: accepted.
An execution is Succeeded only when its requested backup outcome has been verified.
Verification: a failed copy may be Finished but must not be Succeeded.
```
