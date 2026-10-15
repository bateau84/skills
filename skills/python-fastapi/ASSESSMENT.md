# python-fastapi Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer checks FastAPI’s dependency/request lifecycle matches real ASGI behavior:

- sync vs async endpoints/dependencies use the right execution model; blocking work does not freeze the event loop;
- `Depends`/yield dependencies acquire and finalize DB sessions/resources exactly once across success, exception, streaming, and cancellation;
- authn/authz dependencies execute on every protected path and object/tenant authorization is not confused with schema validation;
- request/query/path/body coercion and Pydantic validation do not silently accept values whose semantics should be strict; response models do not hide fields/errors unexpectedly;
- `HTTPException`/handlers map domain failures to stable status/body without leaking internals; 422/validation behavior is understood if externally visible;
- lifespan startup/shutdown owns clients/pools/background resources; `BackgroundTasks` is not treated as durable job execution;
- middleware/order/CORS/trusted-host/proxy/header behavior preserves security and tracing context;
- streaming/websocket/client-disconnect and cancellation semantics are tested where used;
- OpenAPI reflects actual auth/status/schema behavior and integration tests exercise the ASGI surface rather than only calling functions.
