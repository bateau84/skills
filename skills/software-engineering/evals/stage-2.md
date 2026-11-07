# Respect per-job retry permission

Continue from the current project and HANDOFF.md. Add a `retry_allowed: bool`
field to `Job`, defaulting to `True` so existing construction remains compatible.

All three entry points must reject an otherwise eligible job with
`retry_allowed=False` using `PermissionError("retry disabled")`. Check this after
job existence and state eligibility, but before the attempt limit. Rejection
must not write or change the stored record. Retried jobs must retain the field.
Preserve the accepted failed/timed_out behavior, success result, attempt limit,
error messages, diagnostic clearing and save-failure behavior.

Make the actual code and test changes, run relevant checks, update README.md and
HANDOFF.md, and report the observed result. No other feature or external
dependency is requested.
