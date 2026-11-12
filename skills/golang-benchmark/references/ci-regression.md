# CI Benchmark Regression Detection

> **Run these tools in CI only, not on local machines.** Local benchmark results are noisy due to background processes, thermal throttling, and inconsistent CPU frequency — regressions detected locally are unreliable and waste developer time. Even shared CI runners can produce significant variance (5-10%); use statistical methods like `benchstat` with multiple iterations and relative comparisons to filter noise, or invest in dedicated benchmark runners for critical paths.

## benchdiff

Runs Go benchmarks on two git refs and uses `benchstat` to display deltas. Caches results for non-worktree refs so re-runs are fast. Prevents macOS sleep during benchmarks.

```bash
go install filippo.io/mostly-harmless/benchdiff@latest
```

```bash
# Compare current worktree against HEAD (default)
benchdiff -- -benchmem

# Compare two specific refs
benchdiff -base-ref main -head-ref feature-branch

# Compare against a specific commit or tag
benchdiff -base-ref v1.2.0

# Pass extra flags to go test — everything after -- goes to go test
benchdiff -- -benchmem -count=10 -benchtime=3s

# Filter to specific benchmarks
benchdiff -- -benchmem -count=10 -bench=BenchmarkParse

# Target a specific package
benchdiff -- -benchmem -count=10 ./pkg/parser/...

# Clear cached results (useful after rebasing or when cache is stale)
benchdiff -clear-cache

# Combine: compare main with 10 iterations, filtered to critical benchmarks
benchdiff -base-ref main -- -benchmem -count=10 -bench='BenchmarkParse|BenchmarkEncode'
```

Best for: quick PR-to-base comparisons in git-based workflows. Leverages `benchstat` for statistical rigor and caches non-worktree refs so re-runs only re-measure the worktree.

## cob

**Workspace safety:** cob may checkout/reset revisions as part of its comparison. Use a disposable clean checkout with an explicit base, not an active worktree containing uncommitted work. A branch name alone is not evidence that a benchmark used the intended base/current commits.

Compares benchmarks between HEAD and HEAD~1, failing the CI job if performance degrades beyond a configurable threshold (default 20%).

```bash
go install github.com/knqyf263/cob@latest
```

```bash
# Run with default 20% threshold — compares HEAD vs HEAD~1
cob

# Stricter threshold for critical paths (10% regression = failure)
cob -threshold 0.1

# Compare against a specific base commit
cob -base main

# Only report regressions (ignore improvements)
cob -only-degression

# Choose which metrics to compare (default: ns/op,B/op)
cob -compare "ns/op,B/op,allocs/op"

# Custom go test arguments
cob -bench-args "test -run '^$' -bench BenchmarkParse -benchmem ./pkg/parser/..."

# Increase benchmark duration for more stable results
cob -bench-args "test -run '^$' -bench . -benchmem -benchtime=3s ./..."

# Skip cob for a specific commit: include [skip cob] in commit message
```

**Caution:** `cob` uses `git reset` internally, which can cause data loss if uncommitted changes exist. Always commit your work before running. Additionally, `cob` requires all benchmarks to pass; it skips CI gating if any benchmark fails. For safety, run only in CI pipelines, not locally. Note that `cob` compares single runs without `benchstat`-style statistics, making it more susceptible to noise than `benchdiff`.

Best for: simple post-commit regression gating in CI where statistical rigor is less critical than fast feedback.

## gobenchdata

[Upstream gobenchdata](https://github.com/bobheadxi/gobenchdata) parses Go benchmarks into JSON, supports historical trend visualization, and can compare two JSON datasets. The GitHub Action **runs its own benchmarks**; its `BENCHMARKS_OUT` input names the JSON output path, not a file of captured raw `go test` text.

```bash
go install go.bobheadxi.dev/gobenchdata@latest
go test -run '^$' -bench=. -benchmem -count=5 ./... | gobenchdata --json current.json

# Compare normalized JSON files from a fixed base/current environment:
gobenchdata checks generate
gobenchdata checks eval base.json current.json
```

A valid `gobenchdata-checks.yml` uses a **diff expression** and a numeric threshold on that expression, not per-metric `thresholds: [{metric,max}]` entries:

```yaml
checks:
  - name: No slowdown above ten percent
    package: .
    benchmarks: [".*"]
    diff: (current.NsPerOp - base.NsPerOp) / base.NsPerOp * 100
    thresholds:
      max: 10
```

When using `bobheadxi/gobenchdata@v1` in GitHub Actions, supply `GO_BENCHMARKS`, `GO_TEST_FLAGS`, `GO_TEST_PKGS`, and optional `CHECKS`/`CHECKS_CONFIG`/publication settings according to the [upstream action inputs](https://github.com/bobheadxi/gobenchdata). Do not combine the Action with a redundant separate benchmark step or treat `PRUNE_COUNT` as a CLI `--count` switch. Confirm the base JSON was generated for a different revision under comparable hardware; avoid comparing a branch against itself.

Best for: historical trends with controlled CI comparison; consider `benchstat` for statistically assessed repeated measurements.

## Tool Selection Guide

| Tool | Statistical rigor | Dashboard | Best for |
| --- | --- | --- | --- |
| **benchdiff** | High (uses benchstat) | No | Local dev + CI PR comparisons |
| **cob** | Low (single comparison) | No | Quick CI gate, simple setup |
| **gobenchdata** | Medium (configurable checks) | Yes (Vue.js on gh-pages) | Long-term trend tracking |
| **benchstat** (raw) | High | No (CSV export) | Maximum control, custom workflows |

## Noisy Neighbor Mitigation

Cloud CI environments share hardware with other jobs. Expect 5-10% variance even on quiet machines.

### Why CI benchmarks are noisy

- **Shared CPU/memory** — other CI jobs compete for resources
- **Thermal throttling** — sustained load reduces clock speed
- **Different hardware across runs** — CI runners may have different specs
- **Kernel scheduling** — context switches add unpredictable latency
- **Disk I/O contention** — shared storage affects I/O-bound benchmarks

### Strategies

**Statistical rigor** — run with `-count=10` or more and compare with `benchstat`. A single run is meaningless. benchstat's p-value test filters out noise-induced false positives.

**Relative comparison in same job** — run both base and head benchmarks in the same CI job on the same machine, rather than comparing against historical absolute values. This cancels out machine-to-machine variation. Tools like `benchdiff` do this automatically by checking out both git refs.

**Dedicated benchmark runners** — for critical path benchmarks, use self-hosted CI runners with no other workloads. This eliminates noisy neighbors entirely but costs more infrastructure.

**Conservative thresholds** — set regression thresholds higher on shared CI (20%+) than on dedicated runners (10%). Tight thresholds on noisy environments produce false positives that erode trust. GitHub-hosted runners show ~2-3% coefficient of variation in the best case; to guarantee <1% false positive rate, you need a 7%+ performance gate.

**Never "retry until pass"** — rerunning benchmarks until they pass introduces selection bias. If a benchmark is flaky, fix the noise source (more iterations, dedicated runner, wider threshold) rather than retrying.

## System Tuning for Self-Hosted Runners

> **WARNING: These commands modify kernel and CPU settings. Apply them ONLY on dedicated CI runners, NEVER on developer machines or shared servers.**

When you control the CI hardware, these settings dramatically reduce benchmark variance by eliminating the main sources of non-determinism.

### Disable CPU frequency scaling

Variable CPU frequency makes benchmark times meaningless — the same code runs at different speeds depending on load and thermals:

```bash
# Set all CPUs to "performance" governor (fixed maximum frequency)
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
```

### Disable Turbo Boost

Turbo Boost temporarily increases clock speed but throttles under sustained load, creating variance between the start and end of a benchmark run:

```bash
# Intel
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo

# AMD
echo 0 | sudo tee /sys/devices/system/cpu/cpufreq/boost
```

### Pin benchmarks to specific CPU cores

Prevents the OS from migrating the benchmark process across cores, which causes cache thrashing (L1/L2 caches are per-core):

```bash
# Pin to cores 2 and 3 (leave cores 0-1 for OS and other processes)
taskset -c 2,3 go test -bench=. -count=10 ./...
```

### Disable SMT (Hyper-Threading)

SMT shares execution units between logical cores on the same physical core, causing unpredictable contention:

```bash
# Disable SMT system-wide
echo off | sudo tee /sys/devices/system/cpu/smt/control

# Or disable individual sibling cores (check /sys/devices/system/cpu/cpu*/topology/thread_siblings_list)
echo 0 | sudo tee /sys/devices/system/cpu/cpu1/online  # if cpu0 and cpu1 are siblings
```

### Combined CI setup script

```bash
#!/bin/bash
# benchmark-setup.sh — run on self-hosted CI runner before benchmarks
set -euo pipefail

echo "=== Configuring CPU for stable benchmarks ==="
echo performance | sudo tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor
echo 1 | sudo tee /sys/devices/system/cpu/intel_pstate/no_turbo 2>/dev/null || true
echo off | sudo tee /sys/devices/system/cpu/smt/control 2>/dev/null || true

echo "=== Running benchmarks on isolated cores ==="
taskset -c 2,3 go test -bench=. -benchmem -count=10 ./... | tee bench.txt
```
