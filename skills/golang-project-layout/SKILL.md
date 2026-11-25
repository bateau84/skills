---
name: golang-project-layout
description: "Golang project layouts, workspaces, `cmd`/`internal`/`pkg` conventions, monorepos, and module splits. Use when starting a new Go project, organizing an existing codebase, setting up a monorepo, creating CLI tools with multiple mains, or deciding between directory conventions."
user-invocable: true
license: MIT
compatibility: Designed for Claude Code or similar AI coding agents, and for projects using Golang.
metadata:
  author: samber
  version: "1.3.0"
  openclaw:
    emoji: "📁"
    homepage: https://github.com/samber/cc-skills-golang
    requires:
      bins:
        - go
    install: []
allowed-tools: Read Edit Write Glob Grep Bash(go:*) Bash(golangci-lint:*) Bash(git:*) Agent AskUserQuestion
---

**Persona:** You are a Go project architect. You right-size structure to the problem — a script stays flat, a service gets layers only when justified by actual complexity.

Not for choosing between specific libraries or frameworks (→ See `golang-popular-libraries`).

# Go Project Layout

## Choose structure from the current job

Follow the existing repository layout and accepted architecture. For a new small command, start with a root `main` package and co-located tests. Add package boundaries for actual reuse, separate binaries, or ownership needs; possible future growth alone does not require them. A 100-line CLI does not need architecture selection or dependency-injection machinery.

Ask about architecture only when an unresolved choice materially affects the requested product. Use manual parameter or constructor passing when collaborators need substitution; consider a DI library only when the actual wiring problem warrants it. See `golang-design-patterns` or `golang-dependency-injection` for those larger decisions.

## 12-Factor App

For deployed services, apply relevant [12-Factor App](https://12factor.net/) conventions such as external config and graceful shutdown. Do not add service infrastructure to a standalone tool that does not need it.

## Quick Start: Choose Your Project Type

| Project Type | Use When | Key Directories |
| --- | --- | --- |
| **CLI Tool** | Building a command-line application | Root `main` for a small command; `cmd/{name}/` for multiple commands; `internal/` only where needed |
| **Library** | Creating reusable code for others | Public package at module root (and root-level subpackages where useful), `internal/` for private implementation |
| **Service** | HTTP API, microservice, or web app | `cmd/{service}/`, `internal/`, `api/`, `web/` |
| **Monorepo** | Related packages or independently versioned modules | One module by default; use `go.work` only for actual multi-module development |
| **Workspace** | Developing multiple local modules | `go.work`, replace directives |

## Module Naming Conventions

Your module path in `go.mod` MUST match your repository URL, use lowercase only, and hyphens for multi-word segments: `github.com/jdoe/payment-processor`. Avoid generic names like `myproject` or `utils`. → See `golang-naming` skill for complete package naming conventions.

## Directory Layout

A simple single-command module may place `package main` at the root; `cmd/<name>/` is a useful convention for multi-binary and mixed command/library repositories, not a universal requirement. Keep entry points thin; put private implementation under `internal/` as needed. Public libraries often expose a root package—`pkg/` is not mandatory. Follow [Go module layout guidance](https://go.dev/doc/modules/layout).

See [directory layout examples](references/directory-layouts.md) for universal, small project, and library layouts, plus common mistakes.

## Organising Internal Code: Vertical Slices vs. Horizontal Layers

**Horizontal layers:** separate directories by layer — `internal/handler/`, `internal/service/`, `internal/model/`. This is what the reference layouts show.

**Vertical slices:** consider organising by feature when changes repeatedly cross layers. Preserve meaningful package and deployment boundaries, and follow the project's existing conventions unless restructuring is in scope.

```
# Horizontal — layer-based
internal/{handler,service,model}/

# Vertical — feature-based
internal/{order,payment,user}/   # each dir: handler + service + types in 1–3 files
```

A vertical layout can keep related feature behavior close together and reduce cross-directory navigation for humans and agents. Horizontal layers can be useful when shared responsibilities form stable boundaries. Judge locality against representative changes in this project; file or directory counts alone do not establish an agent-failure risk or prove one layout superior.

**File consolidation:** Keep related behavior discoverable without excessive fragmentation. Large files can also obscure boundaries; roughly 500 lines of business logic can prompt a cohesion review, but it is a heuristic, not a universal ceiling. Follow existing package conventions and treat generated/test files according to their purpose.

## Add tooling when it serves a current need

A minimal Go module does not require a Makefile, linter configuration, CI, or other scaffolding. Preserve existing tooling; add new files only for a requested or demonstrated workflow.

- **Makefile** — useful for repeated multi-step commands; direct `go build` / `go test` may be sufficient.
- **.gitignore** — add patterns for actual local outputs or secrets; retain intentional source artifacts and vendored dependencies.
- **.golangci.yml** — add when the project adopts or customizes that linter. See `golang-lint` when relevant.

For application configuration with Cobra + Viper, see [config reference](references/config.md).

## Tests, Benchmarks, and Examples

Co-locate `_test.go` files with the code they test. Use `testdata/` for fixtures. See [testing layout](references/testing-layout.md) for file naming, placement, and organization details.

## Go Workspaces

Use `go.work` when developing multiple related modules in a monorepo. See [workspaces](references/workspaces.md) for setup, structure, and commands.

## Initialization Checklist

When starting a new Go project:

- [ ] Check accepted scope and existing conventions; resolve only material unknown choices
- [ ] Add dependency-injection structure only for actual collaborators and substitution needs
- [ ] Decide project type (CLI, library, service, monorepo)
- [ ] Right-size the structure to the project scope
- [ ] Consider vertical slices where they improve locality for representative changes
- [ ] Choose module name (matches repo URL, lowercase, hyphens)
- [ ] Run `go mod init github.com/user/project-name`
- [ ] Choose a root `main` for a simple command or `cmd/{name}/main.go` for a multi-command/mixed repository
- [ ] Use `internal/` for private import boundaries when needed; public APIs may live at the module root
- [ ] For actual multi-module workspaces: decide whether a `go.work` is needed; a monorepo can be one module
- [ ] Run `gofmt -w .` to ensure formatting
- [ ] Add tooling/ignore files only for actual needs; do not ignore intentionally vendored dependencies

## Related Skills

→ `golang-cli` — CLI tool structure and Cobra/Viper patterns. → `golang-dependency-injection` — DI approach comparison. → `golang-lint` — golangci-lint configuration. → `golang-continuous-integration` — CI/CD pipeline setup. → `golang-design-patterns` — architectural patterns including vertical-slice philosophy.
