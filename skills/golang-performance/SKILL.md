---
name: golang-performance
description: "Allocation reduction, CPU efficiency, memory layout, GC tuning, pooling, caching, and hot-path optimization in Go. Use when profiling or a benchmark has identified a bottleneck and you need the matching optimization pattern, or when reviewing code for allocation and GC hotspots. Not for measurement methodology (→ See `golang-benchmark`) or debugging misbehavior (→ See `golang-troubleshooting`)."
license: MIT
metadata:
  author: Bateau
  version: "1.0.0"
  adapted-from: samber/cc-skills-golang@golang-performance
---

> Adapted from `samber/cc-skills-golang@golang-performance`. Pair with `golang-common-practice` for shared verification guidance.

**Persona:** You are a Go performance engineer. You never optimize without profiling first — measure, hypothesize, change one thing, re-measure.

**Modes:**

- **Review mode (architecture)** — broad scan of a package or service for structural anti-patterns (missing connection pools, unbounded goroutines, wrong data structures). Cover three concerns: (1) allocation and memory layout, (2) I/O and concurrency, (3) algorithmic complexity and caching, within the requested scope.
- **Review mode (hot path)** — focused analysis of a single function or tight loop identified by the caller. Work sequentially; one sub-agent is sufficient.
- **Optimize mode** — a bottleneck has been identified by profiling. Follow the iterative cycle (define metric → baseline → diagnose → improve → compare) sequentially — one change at a time is the discipline.

**Dependencies:**

- benchstat: `go install golang.org/x/perf/cmd/benchstat@latest`

# Go Performance Optimization

## Core Philosophy

1. **Profile before optimizing** — use evidence from the actual workload to locate hot spots (→ See `golang-troubleshooting` skill)
2. **Match the change to the measured bottleneck** — reducing allocations can help when allocation/GC work is material; it does not fix dominant external latency
3. **Preserve correctness and document measured trade-offs** — retain output, ownership, and concurrency contracts before comparing speed or allocation results. Record the workload/toolchain when quoting measurements; do not project a universal multiplier

## Rule Out External Bottlenecks First

Before optimizing Go code, verify the bottleneck is in your process — if 90% of latency is a slow DB query or API call, reducing allocations won't help.

**Diagnose:** 1- `fgprof` — captures on-CPU and off-CPU (I/O wait) time; if off-CPU dominates, the bottleneck is external 2- `go tool pprof` (goroutine profile) — many goroutines blocked in `net.(*conn).Read` or `database/sql` = external wait 3- Distributed tracing (OpenTelemetry) — span breakdown shows which upstream is slow

**When external:** optimize that component instead — query tuning, caching, connection pools, circuit breakers (→ See `golang-database` skill, [Caching Patterns](references/caching.md)).

## Iterative Optimization Methodology

### The cycle: Define Goals → Benchmark → Diagnose → Improve → Benchmark

Create an owned directory inside the task's shell script or subshell, with cleanup
on exit. Preserve the relevant comparison in the agreed evidence location before
that shell scope exits:

```bash
task_bench_dir="$(mktemp -d "${TMPDIR:-/tmp}/go-bench.XXXXXXXX")" || exit 1
trap 'rm -rf -- "$task_bench_dir"' EXIT
```

1. **Define your metric** — latency, throughput, memory, or CPU? Without a target, optimizations are random
2. **Write an atomic benchmark** — isolate one function per benchmark to avoid result contamination (→ See `golang-benchmark` skill)
3. **Measure baseline** — `go test -bench=BenchmarkMyFunc -benchmem -count=6 ./pkg/... | tee "$task_bench_dir/before.txt"`
4. **Diagnose** — use the **Diagnose** lines in each deep-dive section to pick the right tool
5. **Improve** — apply ONE optimization at a time with an explanatory comment
6. **Compare** — after the change, repeat the same benchmark into `"$task_bench_dir/after.txt"`, then run `benchstat "$task_bench_dir/before.txt" "$task_bench_dir/after.txt"`; inspect the comparison and uncertainty
7. **Commit** — paste the benchstat output in the commit body so reviewers and future readers see the exact improvement; follow the `perf(scope): summary` commit type
8. **Repeat** — retain the relevant comparison before reusing filenames, then tackle the next measured bottleneck

Refer to library documentation for known patterns before inventing custom solutions. Use a task-owned temporary directory for measurements, retain the relevant comparison in the agreed evidence location, and clean up temporary work. A pooled buffer must not be returned to the pool while a caller still owns a view of its contents.

## Decision Tree: Where Is Time Spent?

| Bottleneck | Signal (from pprof) | Action |
| --- | --- | --- |
| Too many allocations | `alloc_objects` high in heap profile | [Memory optimization](references/memory.md) |
| CPU-bound hot loop | function dominates CPU profile | [CPU optimization](references/cpu.md) |
| GC pauses / OOM | high GC%, container limits | [Runtime tuning](references/runtime.md) |
| Network / I/O latency | goroutines blocked on I/O | [I/O & networking](references/io-networking.md) |
| Repeated expensive work | same computation/fetch multiple times | [Caching patterns](references/caching.md) |
| Wrong algorithm | O(n²) where O(n) exists | [Algorithmic complexity](references/caching.md#algorithmic-complexity) |
| Lock contention | mutex/block profile hot | → See `golang-concurrency` skill |
| Slow queries | DB time dominates traces | → See `golang-database` skill |

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Optimizing without profiling | Locate the actual bottleneck before choosing a technique |
| Default `http.Client` without Transport | `MaxIdleConnsPerHost` defaults to 2; set to match your concurrency level |
| Logging in hot loops | Log calls prevent inlining and allocate even when the level is disabled. Use `slog.LogAttrs` |
| `panic`/`recover` as control flow | panic allocates a stack trace and unwinds the stack; use error returns |
| `unsafe` without a demonstrated need and correctness argument | Consider only after safer alternatives, with lifetime/aliasing proof and representative measured benefit; no percentage threshold makes it safe |
| Assuming a memory-limit percentage guarantees safety | Measure runtime and non-runtime memory, leave appropriate headroom, and verify load behavior before selecting `GOMEMLIMIT` |
| Replacing reflection without checking semantics | Compare appropriate typed operations on the measured hot path, preserving nil, element, and nested-value behavior |

## Deep Dives

- [Memory Optimization](references/memory.md) — allocation patterns, backing array leaks, sync.Pool, struct alignment
- [CPU Optimization](references/cpu.md) — inlining, cache locality, false sharing, ILP, reflection avoidance
- [I/O & Networking](references/io-networking.md) — HTTP transport config, streaming, JSON performance, cgo, batch operations
- [Runtime Tuning](references/runtime.md) — GOGC, GOMEMLIMIT, GC diagnostics, GOMAXPROCS, PGO
- [Caching Patterns](references/caching.md) — algorithmic complexity, compiled patterns, singleflight, work avoidance
- [Production Observability](references/observability.md) — Prometheus metrics, PromQL queries, continuous profiling, alerting rules

## CI Regression Detection

Automate benchmark comparison in CI to catch regressions before they reach production. → See `golang-benchmark` skill for `benchdiff` and `cob` setup.

## Cross-References

- → See `golang-benchmark` skill for benchmarking methodology, `benchstat`, and `b.Loop()` (Go 1.24+)
- → See `golang-troubleshooting` skill for pprof workflow, escape analysis diagnostics, and performance debugging
- → See `golang-data-structures` skill for slice/map preallocation and `strings.Builder`
- → See `golang-concurrency` skill for worker pools, `sync.Pool` API, goroutine lifecycle, and lock contention
- → See `golang-safety` skill for defer in loops, slice backing array aliasing
- → See `golang-database` skill for connection pool tuning and batch processing
- → See `golang-observability` skill for continuous profiling in production
