# golang-safety Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic supplies extreme/malformed values, path tricks/symlinks, repeated requests, cancellation at destructive boundaries, and concurrent access. Probe crash, corruption, OOM/FD/goroutine exhaustion, partial destructive state, and invariant bypass through conversion/truncation.

Any plausible violation of a mandatory safety/data-integrity/availability/security guarantee is blocking. Defensive hardening beyond the accepted threat/consequence can be non-blocking.

## QA depth

Increase depth with untrusted input, privilege/destructive operations, persistence/filesystem/process access, unsafe/cgo/atomics, concurrency, and exposure to high request volume.
