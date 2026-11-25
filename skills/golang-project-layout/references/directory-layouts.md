# Directory Layouts

## Example Layout for a Larger Multi-Binary Application (Not Universal)

```
project/
├── cmd/                    # Entry points - ONE subdirectory per main package
│   ├── server/            # Main application #1
│   │   └── main.go
│   ├── client/            # Main application #2
│   │   └── main.go
│   └── migrate/           # Main application #3
│       └── main.go
│   └── cli/               # Main application #4
│       └── main.go
│   └── worker/            # Main application #5
│       └── main.go
├── internal/              # Private import boundaries when needed
│   ├── app/              # Application initialization
│   ├── config/           # Configuration loading
│   ├── handler/          # HTTP/request handlers
│   ├── model/            # Data models/domain
│   └── service/          # Business logic
├── pkg/                   # Public libraries (optional - only if useful to others)
│   └── logger/
│       └── logger.go
├── api/                   # API definitions (optional)
│   └── openapi.yaml
├── configs/               # Configuration files (optional)
│   └── config.yaml
├── scripts/               # Build/deployment scripts (optional)
├── go.mod
├── go.sum
├── Makefile               # Build automation
├── .gitignore             # Git ignore patterns
├── .golangci.yml          # Linter configuration
├── LICENSE                # License file
└── README.md
```

## Small Projects (Single Binary)

Start with one package for a small standalone command:

```
my-tool/
├── go.mod
├── main.go
└── main_test.go
```

Add another root Go file when it improves cohesion. A Makefile, lint config,
`cmd/`, `internal/`, and dependency injection are optional responses to real
needs, not a starter kit. Preserve a repository's established layout when fixing
an existing small tool rather than relocating it for symmetry.

## Libraries (Reusable Code)

A small public library can expose its package at the module root:

```
my-library/
├── go.mod
├── library.go
└── library_test.go
```

Add root-level subpackages for separate public capabilities and `internal/` for
private import boundaries when needed. A `pkg/` wrapper is not required.

## The cmd/ Directory Convention

`cmd/` is a conventional home for multiple entry points or mixed repositories, not a Go language requirement. A small standalone command can live in the module root. Keep initialization and wiring readable; supporting Go files in a command package are valid. Place reusable private implementation under `internal/` when it adds useful boundaries; public libraries need not live in `pkg/`.

### Single Application

```
cmd/
└── myapp/
    └── main.go    // package main; additional source files are allowed
```

### Multiple Applications

When you need multiple binaries (e.g., server, CLI tool, migration utility):

```
cmd/
├── server/
│   └── main.go        // Runs the API server
├── client/
│   └── main.go        // CLI client tool
├── worker/
│   └── main.go        // Background worker
└── migrate/
    └── main.go        // Database migration utility
```

Each `main.go`:

- Declares `package main`
- Has its own `func main()`
- Can be built independently: `go build -o ./bin/ ./cmd/...`

**Building all binaries:**

```bash
go build -o ./bin/ ./cmd/...        # Build all main packages
go build ./cmd/server     # Build specific binary
```

## Common Mistakes to Avoid

- Treating `cmd/`, `pkg/`, `internal/`, or a multi-module workspace as universal requirements.
- Adding empty handler/service/repository layers or tooling for hypothetical growth.
- Moving a working root command merely because a larger example uses `cmd/`.
- Replacing meaningful package names with catch-all `utils`, `helpers`, or `common`.

The [Go module layout guide](https://go.dev/doc/modules/layout) explicitly permits
small root command and library packages. Use larger examples only when their
boundaries solve a current problem.
