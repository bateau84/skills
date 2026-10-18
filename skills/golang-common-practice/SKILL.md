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

After each coherent implementation change, run the **smallest relevant check** for changed packages or affected behavior. For example, adapt `go test ./path/to/package`, `go build ./path/to/package`, or a configured linter to the actual repository. Broaden to `./...`, `go vet`, race detection, vulnerability scans, fuzzing, or benchmarks when changed behavior, repository policy, or credible material risk makes that coverage necessary.

An unrelated existing warning or optional hardening idea is not a mandate to expand the change. Record what was checked and the limits of those results; do not claim full-suite validation from a focused check.

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
