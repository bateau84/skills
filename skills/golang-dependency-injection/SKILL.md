---
name: golang-dependency-injection
description: "google/wire, uber-go/dig, uber-go/fx, samber/do, manual constructor injection, and service containers in Go. Use when designing service architecture, setting up dependency injection, refactoring tightly coupled code, or managing singletons and service factories."
license: MIT
metadata:
  author: Bateau
  version: "1.1.0"
  adapted-from: samber/cc-skills-golang@golang-dependency-injection
---

> Adapted from `samber/cc-skills-golang@golang-dependency-injection`. Pair with `golang-common-practice` for shared verification guidance.

**Persona:** You are a Go software architect. You guide teams toward testable, loosely coupled designs — you choose the simplest DI approach that solves the problem, and you never over-engineer.

**Modes:**

- **Design mode** (new project, new service, or adding a service to an existing DI setup): assess the existing dependency graph and lifecycle needs; recommend manual injection or a library from the decision table; then generate the wiring code.
- **Refactor mode** (existing coupled code): map three things — (1) global variables and `init()` service setup, (2) concrete type dependencies that should become interfaces, (3) service-locator anti-patterns (container passed as argument) — then propose a scoped migration plan.

# Dependency Injection in Go

Dependency injection (DI) means passing dependencies to a component rather than having it create or find them. In Go, this is how you build testable, loosely coupled applications — your services declare what they need, and the caller (or container) provides it.

This skill is not exhaustive. When using a DI library (google/wire, uber-go/dig, uber-go/fx, samber/do), refer to the library's official documentation and code examples for current API signatures.

For interface-based design foundations (accept interfaces, return structs), see the `golang-structs-interfaces` skill.

## Best Practices Summary

1. Dependencies MUST be injected via constructors — NEVER use global variables or `init()` for service setup
2. Prefer manual constructor injection when the actual dependency graph and lifecycle are manageable; there is no universal service-count cutoff.
3. Interfaces MUST be defined where consumed, not where implemented — accept interfaces, return structs
4. NEVER use global registries or package-level service locators
5. The DI container MUST only exist at the composition root (`main()` or app startup) — NEVER pass the container as a dependency; agents navigating by lexical search cannot trace an implicit registration chain, so explicit wiring at the root is the only reliably visible path
6. **Match initialization to readiness:** eagerly construct and validate critical dependencies; laziness is an optional lifecycle policy, not a default that may hide startup failures.
7. **Choose lifetime explicitly:** shared pools/caches usually have an owned process lifetime; stateless services do not inherently require transient containers.
8. **Mock at the interface boundary** — DI makes this trivial
9. **Keep the dependency graph shallow** — deep chains signal design problems
10. **Choose the right DI library** for your project size and team — see the decision table below

## Why Dependency Injection?

| Problem without DI | How DI solves it |
| --- | --- |
| Functions create their own dependencies | Dependencies are injected — swap implementations freely |
| Testing requires real databases, APIs | Pass mock implementations in tests |
| Changing one component breaks others | Loose coupling via interfaces — components don't know each other's internals |
| Services initialized everywhere | Centralized container manages lifecycle (singleton, factory, lazy) |
| All services loaded at startup | Lazy loading — services created only when first requested |
| Global state and `init()` functions | Explicit wiring at startup — predictable, debuggable |

DI shines in applications with many interconnected services — HTTP servers, microservices, CLI tools with plugins. For a small script with 2-3 functions, manual wiring is fine. Don't over-engineer.

## Manual Constructor Injection (No Library)

For small projects, pass dependencies through constructors. See [Manual DI examples](./references/manual-di.md) for a complete application example.

```go
// ✓ Good — explicit dependencies, testable
type UserService struct {
    db     UserStore
    mailer Mailer
    logger *slog.Logger
}

func NewUserService(db UserStore, mailer Mailer, logger *slog.Logger) *UserService {
    return &UserService{db: db, mailer: mailer, logger: logger}
}

// main.go — manual wiring
func main() {
    logger := slog.Default()
    db := postgres.NewUserStore(connStr)
    mailer := smtp.NewMailer(smtpAddr)
    userSvc := NewUserService(db, mailer, logger)
    orderSvc := NewOrderService(db, logger)
    api := NewAPI(userSvc, orderSvc, logger)
    api.ListenAndServe(":8080")
}
```

```go
// ✗ Bad — hardcoded dependencies, untestable
type UserService struct {
    db *sql.DB
}

func NewUserService() *UserService {
    db, _ := sql.Open("postgres", os.Getenv("DATABASE_URL")) // hidden dependency
    return &UserService{db: db}
}
```

Manual DI breaks down when:

- The actual graph has substantial cross-dependencies and a container demonstrably simplifies composition, not merely because it crossed a service-count threshold
- You need lifecycle management (health checks, graceful shutdown)
- You want lazy initialization or scoped containers
- Wiring order becomes fragile and hard to maintain

## DI Library Comparison

Go has three main approaches to DI libraries:

- [google/wire examples](./references/google-wire.md) — Compile-time code generation
- [uber-go/dig + fx examples](./references/uber-dig-fx.md) — Reflection-based framework
- [samber/do examples](./references/samber-do.md) — Generics-based, no code generation

### Choose by lifecycle and maintainability

Manual wiring is statically visible. Wire generates wiring but **google/wire is no longer maintained**; do not recommend it as the default for new projects. Existing Wire projects can retain a maintained fork when deliberately supported. `dig`/`fx` resolve constructors at runtime and ordinarily reuse one instance per container; a transient factory must be designed explicitly. `samber/do/v2` type-checks provider signatures, but missing providers and dependency cycles still fail at runtime. Generics do not prove a complete graph or make it inherently easier to trace than other containers.

For `fx`, register every constructor including the final API, then use lifecycle hooks. A blocking `api.Run()` in `fx.Invoke` prevents startup from reaching `app.Run()`; use an `OnStart` that starts bounded owned work and an `OnStop` that cancels and joins it. Startup must report configuration/bind errors before readiness.

For `do/v2`, a provider has signature `func(do.Injector) (T, error)`, not `func(*do.Injector)`. Plain constructors need adapters; every dependency and the final API must be registered. See the [compiling v2 example and isolation test](../../examples/reference-go/di.go), which constructs a real graph, clones it, and overrides a value before invoking it. Avoid mixing v1 and v2 APIs.

## Testing with DI

DI makes testing straightforward — inject mocks instead of real implementations:

```go
// Define a mock
type MockUserStore struct {
    users map[string]*User
}

func (m *MockUserStore) FindByID(ctx context.Context, id string) (*User, error) {
    u, ok := m.users[id]
    if !ok {
        return nil, ErrNotFound
    }
    return u, nil
}

// Test with manual injection
func TestUserService_GetUser(t *testing.T) {
    mock := &MockUserStore{
        users: map[string]*User{"1": {ID: "1", Name: "Alice"}},
    }
    svc := NewUserService(mock, nil, slog.Default())

    user, err := svc.GetUser(context.Background(), "1")
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    if user.Name != "Alice" {
        t.Errorf("got %q, want %q", user.Name, "Alice")
    }
}
```

### Testing with samber/do — Clone and Override

Register the complete graph once, clone the injector, then override dependencies **before** resolving the service in that clone. An empty `do.New()` has no magically available providers. Cloning an injector does not imply every already-created external object is deeply copied; test the actual lifetimes.

```go
original := NewServices() // defines Config and *Service providers; see linked example
isolated := original.Clone()
do.OverrideValue(isolated, Config{Name: "test"})
service := do.MustInvoke[*Service](isolated)
```

The [pinned test](../../examples/reference-go/reference_test.go) verifies both clone isolation and a missing-provider error, using actual do/v2, not a copied fake container.

## When to Adopt a DI Library

| Signal | Action |
| --- | --- |
| < 10 services, simple dependencies | Stay with manual constructor injection |
| Repeated wiring/lifecycle friction | Compare manual wiring with a maintained DI library against actual change and ownership costs; count alone is not a decision rule |
| Significant lifecycle coordination | Consider supported lifecycle tooling such as Fx or an explicit owner; do not prefer unmaintained Wire for new work or claim generics prove a complete graph |
| Need health checks, graceful shutdown | Use a library with built-in lifecycle support |
| Team unfamiliar with DI concepts | Start manual, migrate incrementally |

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Global variables as dependencies | Pass through constructors or DI container |
| `init()` for service setup | Explicit initialization in `main()` or container |
| Depending on concrete types | Accept interfaces at consumption boundaries |
| Passing the container everywhere (service locator) | Inject specific dependencies, not the container |
| Deep dependency chains (A->B->C->D->E) | Flatten — most services should depend on repositories and config directly |
| Creating a new container per request | One container per application; use scopes for request-level isolation |

## Cross-References

- For detailed samber/do usage patterns, consult its official documentation (→ See `golang-pkg-go-dev` skill)
- → See `golang-structs-interfaces` skill for interface design and composition
- → See `golang-testing` skill for testing with dependency injection

## References

- [samber/do/v2 documentation](https://do.samber.dev) | [github.com/samber/do/v2](https://github.com/samber/do)
- [google/wire user guide](https://github.com/google/wire/blob/main/docs/guide.md)
- [uber-go/fx documentation](https://uber-go.github.io/fx/)
- [uber-go/dig](https://github.com/uber-go/dig)

Maintenance source: [Wire status](https://github.com/google/wire), [do/v2 API](https://pkg.go.dev/github.com/samber/do/v2), [Fx lifecycle](https://uber-go.github.io/fx/lifecycle.html).
