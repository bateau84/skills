# Accepted CSV change

The parent outcome is a completed CSV-escaping repair that lets an operator inspect exported completed-job IDs and terminal outcomes offline without broken rows or values.

## Acceptance

- Commas, quotes and embedded newlines round-trip through CSV reading.
- Preserve the existing header, row order, plain output and LF record endings.
- Use the existing Python-only setup without new dependencies.
- Update the behavior documentation to match the result.

## Shared Definition of Done

Accepted behavior is implemented, regression tests pass, behavior documentation is current, and independent review of the source and evidence is complete.

## Accepted responsibility allocation

- Coder owns implementation, regression verification and the behavior documentation for this assignment.
- Reviewer owns independent source and evidence review of the delivered change.
- General owns coordination and acceptance of the combined parent outcome.

Required local verification is `python3 -B -m unittest -v`. Independent review is a separate responsibility in the shared quality baseline. No deployment, release, public communication or unrelated cache work is requested. No commits or pushes are authorized for the task; the initial local fixture commit is supplied context.
