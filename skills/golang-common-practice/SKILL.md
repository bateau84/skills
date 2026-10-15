---
name: golang-common-practice
description: "Go verification, code-quality posture, and skill-family conventions. Use alongside relevant golang-* implementation or review skills for repository-aware checks and diagnose-before-fixing discipline."
license: MIT
metadata:
  author: Bateau
  version: "3.0.0"
  adapted-from: samber/cc-skills-golang
---

# Go Common Practice

The Go-specific base layer for the `golang-*` skill family.

## Scope

This skill provides engineering guidance for any agent. Follow the user's task, repository conventions, and host permissions; no role hierarchy or orchestration framework is assumed.

Use this skill only to improve the quality and verification of already-authorized Go work.

## Inner verification loop

After each meaningful implementation change, run the checks applicable to the repository:

```bash
go build ./...
go vet ./...
go test ./...
golangci-lint run   # when configured
```

Add `go test -race ./...` when concurrency is load-bearing.

A domain skill may require stronger checks such as `govulncheck`, fuzzing, benchmarks, or profiling. Treat those as verification expectations when relevant.

Do not use automatic fix flags as a substitute for understanding changes.

When conclusions rely on test/build/lint/security/runtime results, record the commands, scope, and observed outcomes in the task summary or the project's verification record. Distinguish unrun checks and limitations from passing results.

## Diagnose before fixing

Prefer evidence over intuition. Reproduce and inspect the failure before changing code. When profiling, race detection, static analysis, or runtime tracing is relevant, run the diagnostic first, change one causal factor, then re-check.

## Strictness posture

`MUST`/`NEVER`/`SHOULD` in the Go skills express engineering guidance, not additional runtime permissions.

When local accepted architecture intentionally differs from a generic skill recommendation, current repository authority wins. Name the trade-off rather than silently forcing the generic pattern.

## Cross-reference style

Sibling skills are referenced by bare local name, for example `golang-testing` or `golang-error-handling`.

Load the smallest useful set rather than every Go skill.
