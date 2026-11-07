# Queue retry fixture

This is a small, trusted, in-process Python project. The public Python entry
points `jobqueue.api.retry`, `jobqueue.cli.retry`, and
`jobqueue.scheduler.retry` represent three callers; they are not an HTTP
server or an executable CLI. Python 3.10+ and the standard library are sufficient.

## Accepted behavior

- `retry(store, job_id)` returns the saved `Job` after success.
- A missing job raises `LookupError("job not found")` without a write.
- Only `failed` jobs are retryable initially. Other states raise
  `ValueError("job is not failed")` without a write. This check precedes the limit.
- Three attempts is the limit. At or above it, raise
  `ValueError("retry limit reached")` without a write.
- Success changes state to `queued`, adds exactly one attempt and clears
  `last_error`, with exactly one store write.
- A save failure raises `OSError("storage unavailable")`; the stored record,
  attempt count, diagnostic and successful-write count remain unchanged.
- The three entry points have the same policy. Keep their signatures usable.
  Internal organization is an implementation choice.
- This project has no concurrency, disk format, remote service, plugin,
  automatic retry or mixed-version deployment requirement.

## Development

Run `python3 -B -m unittest discover -s tests -v` from this directory.
Add relevant tests when behavior changes. Keep accepted behavior current here.
Use `HANDOFF.md` for a short durable result if a later maintainer needs context.
