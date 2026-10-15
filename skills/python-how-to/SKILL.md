---
name: python-how-to
description: "Select the smallest relevant python-* skill set for Python implementation, review, debugging, or configuration. Pair technical Python work with python-common-practice for shared verification guidance."
license: MIT
metadata:
  author: Bateau
  version: "1.1.0"
---

> Selects relevant sibling `python-*` skills in this library, regardless of installation location.

**Persona:** You are a Python skills orchestrator. For every Python task, identify all relevant skills and load them together — a task rarely belongs to a single skill.

**Start with `python-common-practice`.** It is the Python-specific base layer for this family: the inner check loop (ruff, pytest, type checker), diagnose-before-fixing, and cross-reference style. Skill selection does not require delegation or a particular agent runtime.

**Modes:**

- **Orchestrate** — for any Python coding, review, debug, or setup task, load the primary skill plus all applicable secondary skills simultaneously.
- **Disambiguate** — when two skills seem to overlap, use the boundary lines below to pick the owner.

## Skill loading

For each task, read or load the primary skill and applicable secondary skills. Bare names refer to sibling directories in this library; use a native loader if available, otherwise read their `SKILL.md` files directly. No fixed installation path is assumed.

| Intent | Primary | Also load |
| --- | --- | --- |
| Build / review a FastAPI endpoint | `python-fastapi` | `python-pydantic`, `python-async`, `python-error-handling` |
| Define a data model or validate input | `python-pydantic` | `python-type-checking` |
| Load typed app configuration | `python-pydantic` | `python-common-practice` |
| Write or run concurrent I/O | `python-async` | `python-error-handling` |
| Call an external HTTP API (httpx) | `python-async` | `python-error-handling`, `python-observability` |
| Schedule background jobs (APScheduler) | `python-async` | `python-observability` |
| Write tests | `python-testing` | `python-async` (async tests) |
| Add type hints / fix a type error | `python-type-checking` | `python-pydantic` |
| Design error flow / custom exceptions | `python-error-handling` | `python-fastapi` (HTTP mapping) |
| Add logging, metrics, or tracing | `python-observability` | `python-error-handling` |
| Database queries / repository / migrations | `python-database` | `python-error-handling`, `python-testing` |
| Configure linting / formatting | `python-lint` | `python-type-checking` |
| Choose an architecture or design pattern | `python-design-patterns` | `python-type-checking`, `python-observability` (instrument as you build) |
| Manage dependencies / virtualenv | `python-common-practice` | `python-lint` |
| Set up a new project | `python-design-patterns` | `python-common-practice`, `python-lint`, `python-testing` |

## Categories at a glance

| Category | Skills |
| --- | --- |
| Foundation | `python-common-practice` |
| Code Quality | `python-lint` `python-type-checking` `python-error-handling` |
| Architecture & Design | `python-design-patterns` `python-async` `python-database` |
| Web & Data | `python-fastapi` `python-pydantic` |
| QA & Observability | `python-testing` `python-observability` |
| Project Setup | `python-common-practice` |

All listed names refer to sibling skills in this library.

## Competing clusters — boundary lines

Pick the owner; load the neighbor only when the task spans the boundary.

- **`python-pydantic` vs `python-type-checking`** — Pydantic does **runtime** validation of external data at the boundary; type-checking does **static** analysis of internal code. Modeling an API payload → pydantic. Annotating a pure function or fixing a checker error → type-checking.
- **`python-error-handling` vs `python-observability`** — error-handling owns control flow (what to catch, raise, chain). Observability owns recording (logging the error, incrementing an error metric). Catching and re-raising → error-handling; deciding *how* to log it → observability.
- **`python-async` vs `python-fastapi`** — fastapi owns the request/response surface and DI; async owns coroutines, concurrency, and not blocking the loop. The danger zone (sync I/O in an `async def` handler) is owned by `python-async`.
- **`python-lint` vs `python-type-checking`** — ruff owns style, imports, and lint rules; the type checker owns type correctness. They run side by side; neither subsumes the other.


## References

- [The Python Standard Library](https://docs.python.org/3/library/)
- [The Python Language Reference](https://docs.python.org/3/reference/)
