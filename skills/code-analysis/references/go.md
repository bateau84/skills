# Go investigation lens

Read `go.mod`, relevant `go.work`, build tags, and the actual target/toolchain before interpreting results. Select only the packages on the investigated path.

Ask who owns each goroutine, channel close, context cancellation, response body, transaction, and lock. Follow ownership through early returns and shutdown. For a suspected race or blocked send, identify the concrete overlapping accesses or possible missing receiver, not merely the presence of concurrency.

Use existing `golang-how-to` guidance to select depth such as `golang-concurrency`, `golang-context`, `golang-error-handling`, `golang-safety`, or `golang-troubleshooting`; do not load the whole family.

Focused repository-approved tests, `go vet`, or race-enabled tests may help where supported. Inspect test setup before execution. A passing race-detector run only covers executed paths and interleavings; it does not establish absence of races or goroutine leaks.

Primary reference: [Go race detector](https://go.dev/doc/articles/race_detector). Match commands and library behavior to the inspected toolchain.
