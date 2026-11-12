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
├── internal/              # Private application code (`internal/` MUST be used for non-exported packages)
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

For simple tools a root `main.go` is sufficient; the following optional `cmd/` layout is useful if additional commands are expected:

```
my-tool/
├── cmd/
│   └── my-tool/
│       └── main.go        # Single main package
├── internal/
│   └── core.go            # Application logic
├── go.mod
├── Makefile               # Build automation (optional but recommended)
├── .gitignore             # Git ignore patterns
├── .golangci.yml          # Linter configuration (optional)
├── LICENSE                # License file (recommended)
└── README.md
```

## Libraries (Reusable Code)

```
my-library/
├── example/               # Example
├── logger/                # Public package
│   ├── logger.go
│   └── logger_test.go
├── internal/
│   └── impl/              # Private implementation details
│       └── core.go
├── go.mod
├── go.sum
├── Makefile               # Build automation
├── .gitignore             # Git ignore patterns
├── .golangci.yml          # Linter configuration
├── LICENSE                # License file
└── README.md
```

**Key points for libraries:**

- Put public API in root-level directories (e.g., `logger/`)
- Use `internal/` for private implementation
- Don't use `cmd/` (unless you have example binaries)

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

### Don't Do This

```
myproject/
├── src/              # Go doesn't use /src (Java pattern)
├── main.go           # Don't put main at root
├── utils/            # Generic package name
├── helpers/          # Generic package name
└── common/           # Generic package name
```

### Do This Instead

```
myproject/
├── cmd/
│   └── myapp/
│       └── main.go   # Main in cmd/
├── internal/
│   ├── util/         # Specific utility names
│   └── format/       # Or domain-specific names
└── pkg/              # Only if useful to others
```
