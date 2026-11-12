# Go Workspaces (go.work)

## go.work vs go.mod

| Scenario                                       | Use       |
| ---------------------------------------------- | --------- |
| Single module project                          | `go.mod`  |
| Developing multiple related local modules      | `go.work` |
| Monorepo with separate Go modules              | `go.work` |
| Testing local changes across module boundaries | `go.work` |
| Published library consumed by others           | `go.mod`  |

## Workspace Commands

```bash
go work init                    # Initialize workspace
go work use ./services/auth     # Add module to workspace
go work edit -dropuse ./old-module    # Remove module from workspace
go work sync                    # Sync workspace with module changes
```

## Key Points

- Workspaces eliminate the need for `replace` directives during local development — the workspace automatically resolves local modules
- Choose whether to version workspace files according to the repository contract; libraries must also be tested with `GOWORK=off` so workspace overrides do not hide invalid module requirements
- `go.work` is for development only — it does not affect how consumers of your published modules resolve dependencies
- Keep workspace member modules in conventional directories (`cmd/`, `internal/`, `pkg/`) with clear boundaries
