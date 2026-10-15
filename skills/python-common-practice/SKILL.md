---
name: python-common-practice
description: "Python verification, code-quality posture, and skill-family conventions. Use alongside relevant python-* implementation or review skills for repository-aware checks and diagnose-before-fixing discipline."
license: MIT
metadata:
  author: Bateau
  version: "3.0.0"
---

# Python Common Practice

The Python-specific base layer for the `python-*` skill family.

## Scope

This skill provides engineering guidance for any agent. Follow the user's task, repository conventions, and host permissions; no role hierarchy or orchestration framework is assumed.

Use it only to improve the quality and verification of already-authorized Python work.

## Inner verification loop

Use the repository's configured tools. A common baseline is:

```bash
uv sync
uv run ruff check .
uv run ruff format --check .
uv run pytest
uv run mypy .   # or pyright / ty when configured
```

Do not assume every project uses every tool. Read `pyproject.toml` and current repository guidance first.

A domain skill may require stronger checks such as coverage, async tests, security scanning, or profiling. Treat those as verification expectations when relevant.

When conclusions rely on verification, record the commands, scope, and observed outcomes in the task summary or the project's verification record. Distinguish unrun checks and limitations from passing results.

## Diagnose before fixing

Reproduce and inspect failures before editing. Use focused tests, traceback inspection, debugger/profiler output, type-checker output, or runtime instrumentation as appropriate. Change one causal factor, then re-run the focused check.

## Dependency posture

Prefer the standard library when it is sufficient. New runtime dependencies are a maintenance commitment and should be justified by the task and accepted architecture.

Use the project's actual package manager. Prefer `uv` only when the repository already uses it or the authorized task includes adopting it.

## Strictness posture

Generic Python guidance never overrides accepted repository authority. When framework convention and accepted architecture differ, current authority wins and the trade-off should be explicit.

## Cross-reference style

Sibling skills are referenced by bare local name such as `python-testing`, `python-fastapi`, or `python-error-handling`.

Load the smallest useful set rather than the entire Python family.
