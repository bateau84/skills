---
name: golang-error-handling
description: "Wrap, propagate, and inspect errors in Go — `%w`, `errors.Is`, `errors.As`, `errors.Join`, sentinel errors, custom error types, `panic`/`recover`, and the single handling rule. Use when creating or wrapping errors, designing an error API, deciding between error wrapping and panic, or inspecting errors up the call stack. Not for slog setup (→ See `golang-observability`)."
license: MIT
metadata:
  author: Bateau
  version: "1.1.0"
  adapted-from: samber/cc-skills-golang@golang-error-handling
---

> Adapted from `samber/cc-skills-golang@golang-error-handling`. Pair with `golang-common-practice` for shared verification guidance.

**Persona:** You are a Go reliability engineer. You treat every error as an event that must either be handled or propagated with context — silent failures and duplicate logs are equally unacceptable.

**Modes:**

- **Coding mode** — writing new error handling code. Follow the best practices sequentially; inspect relevant adjacent code for swallowed errors and log-and-return pairs. An authorized read-only collaborator may help when available, but delegation is not required.
- **Review mode** — reviewing a PR's error handling changes. Focus on the diff: check for swallowed errors, missing wrapping context, log-and-return pairs, and panic misuse. Sequential.
- **Audit mode** — auditing existing error handling across a codebase. Cover every applicable independent category (creation, wrapping, single-handling rule, panic/recover, structured logging).

# Go Error Handling Best Practices

This skill guides the creation of robust, idiomatic error handling in Go applications. Follow these principles to write maintainable, debuggable, and production-ready error code.

## Best Practices Summary

1. **Returned errors MUST always be checked** — NEVER discard with `_`
2. **Errors MUST be wrapped with context** using `fmt.Errorf("{context}: %w", err)`
3. **Error strings MUST be lowercase**, without trailing punctuation
4. **Use `%w` internally, `%v` at system boundaries** to control error chain exposure
5. **MUST use `errors.Is` for sentinel matching and `errors.As`/`errors.AsType` for typed chain inspection** instead of direct comparison or bare type assertions. For Go 1.26+, prefer `errors.AsType[T](err)` when `T` implements `error`; use `errors.As(err, &target)` for Go <1.26 or for non-error interface targets.
6. **SHOULD use `errors.Join`** (Go 1.20+) to combine independent errors
7. **Errors MUST be either logged OR returned**, NEVER both (single handling rule)
8. **Use sentinel errors** for expected conditions, custom types for carrying data
9. **NEVER use `panic` for expected error conditions** — reserve for truly unrecoverable states
10. **SHOULD use `slog`** (Go 1.21+) for structured error logging — not `fmt.Println` or `log.Printf`
11. **Use `samber/oops`** for production errors needing stack traces, user/tenant context, or structured attributes
12. **Log HTTP requests** with structured middleware capturing method, path, status, and duration
13. **Use log levels** to indicate error severity
14. **Never expose technical errors to users** — translate internal errors to user-friendly messages, log technical details separately
15. **Keep log grouping low-cardinality** — at logging/APM boundaries, keep message templates stable and attach IDs, paths, line numbers, and counts as structured attributes. Error values may include useful operational context, but avoid putting high-cardinality data into the stable log message used for grouping.

## Detailed Reference

- **[Error Creation](./references/error-creation.md)** — How to create errors that tell the story: error messages should be lowercase, no punctuation, and describe what happened without prescribing action. Covers sentinel errors (one-time preallocation for performance), custom error types (for carrying rich context), and the decision table for which to use when.

- **[Error Wrapping and Inspection](./references/error-wrapping.md)** — Why `fmt.Errorf("{context}: %w", err)` beats `fmt.Errorf("{context}: %v", err)` (chains vs concatenation). How to inspect chains with `errors.Is`, `errors.As`, and Go 1.26+ `errors.AsType` for type-safe error handling, and `errors.Join` for combining independent errors.

- **[Error Handling Patterns and Logging](./references/error-handling.md)** — The single handling rule: errors are either logged OR returned, NEVER both (prevents duplicate logs cluttering aggregators). Panic/recover design, `samber/oops` for production errors, and `slog` structured logging integration for APM tools.

## Parallelizing Error Handling Audits

When auditing error handling across a large codebase, cover each applicable category below. One practitioner can do this sequentially. If parallel collaborators are available and authorized, divide read-only inspection and reconcile findings; coordinate any overlapping repairs explicitly rather than assuming host locks or isolated files.

- Error creation — validate `errors.New`/`fmt.Errorf` usage, low-cardinality messages, custom types
- Error wrapping — audit `%w` vs `%v`, verify `errors.Is`/`errors.As` patterns
- Single handling rule — find log-and-return violations, swallowed errors, discarded errors (`_`)
- Panic/recover — audit `panic` usage, verify recovery at goroutine boundaries
- Structured logging — verify `slog` usage at error sites, check for PII in error messages

## Cross-References

- For the full samber/oops API, builder patterns, and logger integration, consult its official documentation (→ See `golang-pkg-go-dev` skill)
- → See `golang-observability` for structured logging setup, log levels, and request logging middleware
- → See `golang-safety` for nil interface trap and nil error comparison pitfalls
- → See `golang-naming` for error naming conventions (ErrNotFound, PathError)
- → See `golang-continuous-integration` skill for automated AI-driven code review in CI using these guidelines

## References

- [lmittmann/tint](https://github.com/lmittmann/tint)
- [samber/oops](https://github.com/samber/oops)
- [samber/slog-multi](https://github.com/samber/slog-multi)
- [samber/slog-sampling](https://github.com/samber/slog-sampling)
- [samber/slog-formatter](https://github.com/samber/slog-formatter)
- [samber/slog-http](https://github.com/samber/slog-http)
- [samber/slog-sentry](https://github.com/samber/slog-sentry)
- [log/slog package](https://pkg.go.dev/log/slog)
