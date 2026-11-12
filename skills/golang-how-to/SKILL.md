---
name: golang-how-to
description: "Golang skill orchestrator for selecting and composing local Go guidance. Use when coding, reviewing, debugging, configuring, or navigating Go projects where multiple golang-* skills may apply. Routes tasks to specialist skills and always pairs them with golang-common-practice."
license: MIT
metadata:
  author: Bateau
  version: "1.1.0"
  adapted-from: samber/cc-skills-golang@golang-how-to
---

> Adapted from `samber/cc-skills-golang@golang-how-to`. Selects relevant sibling `golang-*` skills in this library, regardless of installation location.

**Persona:** You are a Go skills selector. Find the smallest useful set of guidance for the actual change. Loading more skills does not increase the task's scope or make every checklist item mandatory.

**Not for:** replacing specialist `golang-*` guidance; this skill routes to it.

**Start with `golang-common-practice`.** It is the Go-specific base layer for this family: the inner compile loop, diagnose-before-fixing, and cross-reference style. Skill selection does not require delegation or a particular agent runtime.

**Go code navigation:** use `gopls` for semantic queries when available and appropriately bounded; use `rg`/`grep` for literal and targeted lookup, especially if full-workspace tooling is expensive or unavailable.

**Modes:**

- **Orchestrate** — select the primary skill and load only secondary skills whose techniques materially apply to the current work. Do not load a whole cluster by default.
- **Disambiguate** — when two skills seem to overlap, use the boundary lines below to pick the owner.
- **Configure** — add a `## Required Go skills` block to the project's `AGENTS.md`. See [Configure mode](#configure-mode).

## Skill loading

For each task, start with the relevant primary skill; load secondary skills only for affected behavior or credible in-scope risks. The table is a discovery aid, **not an unconditional checklist or instruction to add functionality**. Bare names refer to sibling directories; use a native loader if available, otherwise read their `SKILL.md` files directly.

| Intent | Primary | Consider when relevant |
| --- | --- | --- |
| Design an API, choose a pattern | `golang-design-patterns` | `golang-structs-interfaces`, `golang-naming` |
| Implement a feature, service, or I/O boundary | `golang-design-patterns` | `golang-error-handling`; `golang-observability` when operational signals materially change |
| Name a type, function, or package | `golang-naming` | `golang-code-style` |
| Handle errors idiomatically | `golang-error-handling` | `golang-safety` (nil-heavy code) |
| Write goroutines, channels, sync | `golang-concurrency` | `golang-context` (if cancellation) |
| Pass deadlines / cancel operations | `golang-context` | `golang-concurrency` (if goroutines) |
| Design structs, embed, use interfaces | `golang-structs-interfaces` | `golang-design-patterns` |
| Database queries and transactions | `golang-database` | `golang-error-handling`; `golang-security` for untrusted input or changed security boundaries |
| Build a CLI command tree | `golang-spf13-cobra` | `golang-cli`, `golang-spf13-viper` (if config) |
| Layer config from flags/env/file | `golang-spf13-viper` | `golang-spf13-cobra` |
| Write tests | `golang-testing` | `golang-safety` (if edge-case heavy) |
| Document an HTTP API (Swagger/OpenAPI) | `golang-swagger` | `golang-documentation` |
| Apply optimization patterns | `golang-performance` | `golang-benchmark` (measure first) |
| Measure with pprof / benchstat | `golang-benchmark` | `golang-performance` (fix), `golang-troubleshooting` (root cause) |
| Debug a panic or unexpected behavior | `golang-troubleshooting` | `golang-safety`, `golang-benchmark` (if perf-related) |
| Pick a data structure | `golang-data-structures` | `golang-performance` |
| Monitor in production | `golang-observability` | `golang-performance` (if SLO breach) |
| Audit security vulnerabilities | `golang-security` | `golang-safety`, `golang-lint` |
| Review formatting and style | `golang-code-style` | `golang-naming`, `golang-lint` |
| Configure golangci-lint | `golang-lint` | `golang-code-style` |
| Write godoc / README / CHANGELOG | `golang-documentation` | `golang-naming` |
| Set up a new project structure | `golang-project-layout` | `golang-dependency-management` for actual multi-module needs |
| Set up CI/CD pipeline | `golang-continuous-integration` | `golang-lint`, `golang-security` |
| Manage `go.mod` / dependencies | `golang-dependency-management` | `golang-modernize` |
| Adopt new Go language features | `golang-modernize` | `golang-lint` |
| Use dependency injection | `golang-dependency-injection` | `golang-design-patterns` |
| Implement gRPC services/interceptors | `golang-grpc` | `golang-error-handling`, `golang-context` |
| Use testify assertions/mocks/suites | `golang-stretchr-testify` | `golang-testing` |
| Implement an interactive Charm TUI | `golang-tui` | `tui-design` for the user-facing contract |
| Compare libraries | `golang-popular-libraries` | `golang-pkg-go-dev` for current APIs/status |
| Look up an API or version-specific behavior | `golang-pkg-go-dev` | `golang-modernize` only for authorized upgrades |

**API contracts and version-specific behavior:** for API contracts and version-specific library behavior, load `golang-pkg-go-dev` and look up live, do not answer from pre-training memory.

## Categories at a glance

| Category | Skills |
| --- | --- |
| Foundation | `golang-common-practice` |
| Code Quality | `golang-code-style` `golang-documentation` `golang-error-handling` `golang-lint` `golang-naming` `golang-safety` `golang-security` `golang-structs-interfaces` |
| Architecture & Design | `golang-concurrency` `golang-context` `golang-data-structures` `golang-database` `golang-dependency-injection` `golang-design-patterns` `golang-modernize` |
| QA & Performance | `golang-benchmark` `golang-observability` `golang-performance` `golang-testing` `golang-troubleshooting` |
| Project Setup | `golang-project-layout` `golang-cli` `golang-continuous-integration` `golang-dependency-management` `golang-popular-libraries` |
| APIs | `golang-swagger`, `golang-grpc`, `golang-pkg-go-dev` |
| Frameworks | `golang-spf13-cobra` `golang-spf13-viper` `golang-stretchr-testify` `golang-tui` |

## Competing clusters — boundary lines

Pick the owner; load neighbors only when the task spans the boundary.

- **Performance**: `golang-performance` (optimization patterns) · `golang-benchmark` (measurement) · `golang-troubleshooting` (root cause) · `golang-observability` (always-on production)
- **Style**: `golang-code-style` (clarity/judgment) · `golang-naming` (identifiers) · `golang-lint` (automated config) · `golang-documentation` (godoc/README)
- **CLI**: `golang-cli` (architecture) · `golang-spf13-cobra` (command tree) · `golang-spf13-viper` (config layering)
- **Errors vs correctness vs threat**: `golang-error-handling` (idioms) · `golang-safety` (prevent internal bugs/panics) · `golang-security` (external threats)
- **Type vs arch**: `golang-structs-interfaces` (type design) vs `golang-design-patterns` (architectural patterns)
- **Goroutine vs cancel**: `golang-concurrency` + `golang-context` — load both when cancelling goroutines via context
- **Features vs rules**: `golang-modernize` (language adoption) vs `golang-lint` (static analysis config)




## Configure mode

Only when the user authorizes repository guidance edits, inspect existing `AGENTS.md` instructions and update one `## Required Go skills` section without duplicating or overriding higher-priority rules. List `golang-common-practice` plus specialist skills that genuinely apply to that repository; do not make the entire Go family mandatory. State how the host locates installed skills; do not invent an absolute installation directory.

## Version-specific guidance

Look up current API signatures and supported toolchains only where they matter to the task. Use `golang-pkg-go-dev` and [official release notes](https://go.dev/doc/devel/release). Do not add upgrades, social subscriptions, documentation blocks or new tooling to an unrelated bounded change.

General GitHub workflow security belongs to `github-workflow`; Go-specific build steps belong to `golang-continuous-integration`. General CLI design belongs to `cli-design`, and observability pipeline design to `opentelemetry`/`prometheus`; load Go implementation guidance only for the corresponding code.
