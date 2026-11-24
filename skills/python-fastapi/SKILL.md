---
name: python-fastapi
description: "Building HTTP APIs with FastAPI — APIRouter organization, path/query/body params, Pydantic request/response models, dependency injection with Depends, app.state and lifespan, HTTPException and error responses, status codes, async vs sync endpoints, and the auto-generated OpenAPI/Swagger docs. Use when adding or reviewing FastAPI routes, wiring dependencies, shaping request/response models, structuring an API package, or documenting an HTTP API. Also use when the user mentions FastAPI, uvicorn, APIRouter, Depends, or OpenAPI in Python. Not for Pydantic model design (→ See `python-pydantic`) or async patterns (→ See `python-async`)."
license: MIT
metadata:
  author: Bateau
  version: "1.2.0"
---

> Pair with `python-common-practice`, `python-pydantic` (models), `python-async` (async endpoints), and `python-error-handling` (exceptions) as relevant.

**Persona:** You are a Python API engineer. You let FastAPI's type system do the validation and documentation, and you keep handlers thin.

# FastAPI

FastAPI derives validation, serialization, and OpenAPI docs from declared types. Keep the HTTP boundary clear and follow the project's existing structure. Extract domain logic when it has independent complexity or reuse; a small handler does not need a new service layer or `core/` package. Address the requested route or lifecycle problem before proposing broader changes.

## Structure with APIRouter

Group routes with `APIRouter` when a resource or shared configuration benefits from it. Keep a small existing app in place when a route-level change does not require reorganization.

```python
# api/routes/stats.py
from fastapi import APIRouter

router = APIRouter(prefix="/stats", tags=["stats"])

@router.get("", response_model=StatsOut)
async def get_stats(state=Depends(get_state)) -> StatsOut:
    return build_stats(state)

# api/app.py
app.include_router(stats.router)
```

`tags` group endpoints in the Swagger UI; `prefix` keeps paths DRY.

**Feature locality:** co-locating related routes, models, and logic can improve discoverability when consistent with project conventions. Keep meaningful dependency boundaries and review cohesion as files grow; roughly 500 lines is a heuristic rather than a required limit. Do not reorganize an existing FastAPI project solely because an agent maintains it.

## Declare request and response models

Declare the public response shape through a supported return annotation **or** `response_model`. Both can be used; the decorator takes precedence. Returning a dict or ORM object is valid when the response model validates and filters it correctly. Do not expose internal fields. → See `python-pydantic`.

A directly returned `Response`/`JSONResponse` bypasses this automatic conversion and filtering. Construct only the approved public payload yourself on that path, or return ordinary data through the declared response model. Verify actual HTTP output, not only the model declaration.

```python
class RuleIn(BaseModel):
    pattern: str
    action: Literal["allow", "deny"]

@router.post("/rules", response_model=RuleOut, status_code=201)
async def create_rule(rule: RuleIn) -> RuleOut:   # body parsed + validated automatically
    ...
```

- A Pydantic-typed parameter → request **body**. A scalar with no default → required **query/path** param. `Query()`/`Path()`/`Body()` add constraints and docs.
- Set explicit `status_code` for creates (201) and no-content (204). The default 200 is wrong for those.
- Use `response_model` to strip sensitive/internal fields even when the object has them.

## Dependencies with `Depends`

Dependencies are FastAPI's DI: declare what a handler needs; FastAPI resolves and caches it per request. Use them for shared state, auth, and guards.

```python
def get_db(request: Request):
    return request.app.state.db

def require_auth(db=Depends(get_db)) -> User:
    # raises HTTPException(401) if not authenticated
    ...

@router.post("/items")
async def create_item(user=Depends(require_auth)):   # 401 short-circuits before body runs
    ...
```

A dependency that `raise`s `HTTPException` short-circuits the handler — clean for auth and precondition checks. Dependencies can `yield` to run teardown after the response.

**`Depends()` resolves at runtime — the resolved type is invisible from the handler signature alone.** Add a type annotation and a one-line docstring to each dependency so the contract is visible without tracing the chain:

```python
def require_auth(db: Session = Depends(get_db)) -> User:
    """Return the authenticated User or raise HTTPException(401)."""
    ...
```

## App state and lifespan

Open shared resources (DB pool, httpx client, scheduler) once at startup via the `lifespan` context manager, stash them on `app.state`, and close them on shutdown. Do not open a client per request (→ See `python-async`).

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db = await create_db_pool()   # startup
    yield
    await app.state.db.aclose()             # shutdown

app = FastAPI(lifespan=lifespan)
```

Prefer `lifespan` over the deprecated `@app.on_event("startup")`/`("shutdown")`.

## async vs sync handlers

Use `async def` when the body `await`s I/O. Use plain `def` for purely sync/CPU work — FastAPI runs `def` handlers in a threadpool so they don't block the loop. The dangerous combination is sync blocking I/O inside an `async def` handler: it freezes the event loop (→ See `python-async`).

## Errors

Raise `HTTPException(status_code, detail)` for expected client-facing errors. For cross-cutting mapping (a domain exception → a 4xx/5xx), register an exception handler rather than wrapping every route in try/except. → See `python-error-handling`.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Exposing internal fields in output | Declare the public response shape and verify filtering; direct `Response` objects need an explicitly safe payload. |
| Blocking I/O inside `async def` | Make it `await` async I/O, or use a `def` handler (threadpool). |
| Manual JSON parsing / validation in the handler | Type the param with a Pydantic model; FastAPI validates it. |
| 200 for a resource creation | Set `status_code=201`. |
| Resources opened per request | Open once in `lifespan`, share via `app.state`. |
| `@app.on_event` for startup | Use the `lifespan` context manager. |
| Complex domain logic mixed with HTTP handling | Extract that logic along existing project boundaries when it improves reuse or clarity. |
| Undocumented `Depends()` chain | Annotate and docstring each dependency function (see Depends section). |

## References

- [FastAPI documentation](https://fastapi.tiangolo.com/)
- [Response models and return types](https://fastapi.tiangolo.com/tutorial/response-model/)
- [Returning a Response directly](https://fastapi.tiangolo.com/advanced/response-directly/)
- [FastAPI — Lifespan events](https://fastapi.tiangolo.com/advanced/events/)
- [Starlette documentation](https://www.starlette.io/)
