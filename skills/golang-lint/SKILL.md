---
name: golang-lint
description: "Linting best practices and golangci-lint configuration for Golang projects — running linters, configuring .golangci.yml, suppressing warnings with nolint directives, interpreting lint output, and selecting linters. Use when configuring golangci-lint, asking about lint warnings or nolint suppressions, setting up code quality tooling, or choosing linters. Also use when the user mentions golangci-lint, go vet, staticcheck, or revive."
license: MIT
metadata:
  author: Bateau
  version: "1.0.0"
  adapted-from: samber/cc-skills-golang@golang-lint
---

> Adapted from `samber/cc-skills-golang@golang-lint`. Pair with `golang-common-practice` for shared verification guidance.

**Persona:** You are a Go code quality engineer. You treat linting as a first-class part of the development workflow — not a post-hoc cleanup step.

**Modes:**

- **Setup mode** — configuring `.golangci.yml`, choosing linters, enabling CI: follow the configuration and workflow sections sequentially.
- **Coding mode** — writing new Go code: run the configured lint checks as part of the verification loop (see `golang-common-practice`). Use automatic fixes only when permitted, inspect the resulting diff, and avoid unrelated changes.
- **Interpret/fix mode** — reading lint output, suppressing warnings, fixing issues on existing code: start from "Interpreting Output" and "Suppressing Lint Warnings". Keep legacy cleanup scoped to the requested work.

**Dependencies:**

- golangci-lint: `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest`

# Go Linting

## Overview

`golangci-lint` is the standard Go linting tool. It aggregates 100+ linters into a single binary, runs them in parallel, and provides a unified configuration format. Run it frequently during development and always in CI.

When a project uses golangci-lint, its configured `.golangci.yml` (or another supported configuration path) is the source of truth for enabled linters. Follow the repository's actual configuration and installed major version; see the [configuration documentation](https://golangci-lint.run/docs/configuration/).

## Quick Reference

```bash
# Run all configured linters
golangci-lint run ./...

# Auto-fix issues where possible
golangci-lint run --fix ./...

# Format code (golangci-lint v2+)
golangci-lint fmt ./...

# Run a single linter only
golangci-lint run --enable-only govet ./...

# List all available linters
golangci-lint linters

# Verbose output with timing info
golangci-lint run --verbose ./...
```

## Configuration

Select linters according to the project's risks and existing policy rather than assuming a universal preset. See the **[linter reference](./references/linter-reference.md)** for categories, descriptions, and applicability; confirm supported names and settings against the installed version.

## Suppressing Lint Warnings

Use `//nolint` directives sparingly — fix the root cause first.

```go
// Good: specific linter + justification
//nolint:errcheck // fire-and-forget logging, error is not actionable
_ = logger.Sync()

// Bad: blanket suppression without reason
//nolint
_ = logger.Sync()
```

Rules:

1. **//nolint directives MUST specify the linter name**: `//nolint:errcheck` not `//nolint`
2. **//nolint directives MUST include a justification comment**: `//nolint:errcheck // reason`
3. **The `nolintlint` linter enforces both rules above** — it flags bare `//nolint` and missing reasons
4. **NEVER suppress security linters** (gosec, bodyclose, sqlclosecheck) without a very strong reason

For comprehensive patterns and examples, see **[nolint directives](./references/nolint-directives.md)** — when to suppress, how to write justifications, patterns for per-line vs per-function suppression, and anti-patterns.

## Development Workflow

1. **Linters SHOULD be run after every significant change**: `golangci-lint run ./...`
2. **Auto-fix what you can**: `golangci-lint run --fix ./...`
3. **Format before committing**: `golangci-lint fmt ./...`
4. **Incremental adoption on legacy code**: set `issues.new-from-rev` in `.golangci.yml` to only lint new/changed code, then gradually clean up old code

Makefile targets (recommended):

```makefile
lint:
	golangci-lint run ./...

lint-fix:
	golangci-lint run --fix ./...

fmt:
	golangci-lint fmt ./...
```

For CI pipeline setup (GitHub Actions with `golangci-lint-action`), see the `golang-continuous-integration` skill.

## Interpreting Output

Each issue follows this format:

```
path/to/file.go:42:10: message describing the issue (linter-name)
```

The linter name in parentheses tells you which linter flagged it. Use this to:

- Look up the linter in the [reference](./references/linter-reference.md) to understand what it checks
- Suppress with `//nolint:linter-name // reason` if it's a false positive
- Use `golangci-lint run --verbose` for additional context and timing

## Common Issues

| Problem | Solution |
| --- | --- |
| "deadline exceeded" | Set or increase `run.timeout` in `.golangci.yml`; golangci-lint v2 defaults to no timeout (`0`) |
| Too many issues on legacy code | Set `issues.new-from-rev: HEAD~1` to lint only new code |
| Linter not found | Check `golangci-lint linters` — linter may need a newer version |
| Conflicts between linters | Disable the less useful one with a comment explaining why |
| v1 config errors after upgrade | Run `golangci-lint migrate` to convert config format |
| Slow on large repos | Reduce `run.concurrency` or exclude paths with `linters.exclusions.paths` / `formatters.exclusions.paths` |

## Parallelizing Legacy Codebase Cleanup

When adopting linting on a legacy codebase, address the applicable categories below. One practitioner can cover them sequentially. Parallel contributors are optional; categories can touch the same files, so coordinate mutation ownership rather than assuming isolation or host locks.

- Automatic fixes: Run configured automatic fixes only within the authorized cleanup scope and inspect the diff
- Security: Fix security linter findings (bodyclose, sqlclosecheck, gosec)
- Error handling: Fix errcheck, nilerr, and wrapcheck findings
- Style and formatting: Fix gofumpt, goimports, and revive findings
- Code quality: Fix gocritic, unused, and ineffassign findings

## Cross-References

- → See `golang-continuous-integration` skill for CI pipeline with golangci-lint-action
- → See `golang-code-style` skill for style rules that linters enforce
- → See `golang-security` skill for SAST tools beyond linting (gosec, govulncheck)
- → See `golang-continuous-integration` skill for automated AI-driven code review in CI using these guidelines
