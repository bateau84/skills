---
name: terraform-provider-actions
description: Implement Terraform Provider actions using the Plugin Framework. Use when developing imperative operations that execute at lifecycle events (before/after create, update, destroy).
metadata:
  copyright: Copyright IBM Corp. 2026
  version: "0.0.1"
---

# Terraform Provider Actions

Use the public Plugin Framework `action` interfaces. Actions are available in Terraform 1.14+ with a supporting framework release; check the repository's pinned Terraform/framework versions before emitting code. An action can be invoked directly or from an accepted lifecycle trigger; it has no resource state or computed outputs.

## Implement the public boundary

1. Implement `action.Action` (`Metadata`, `Schema`, `Invoke`). Derive the type name from `req.ProviderTypeName`.
2. Import **`github.com/hashicorp/terraform-plugin-framework/action/schema`**, not resource/schema. Action attributes are configuration: choose `Required` or `Optional`, validation and a description. Do **not** copy resource `Computed`, plan modifiers or `Default` fields into action attributes. Resolve an optional default in the implementation, distinguishing null from unknown and validating its bounds.
3. Register constructors through **`provider.ProviderWithActions.Actions(context.Context) []func() action.Action`**. Merely placing the file under a service directory does not register it.
4. For provider clients implement `action.ActionWithConfigure`. Read the client from `req.ProviderData`, handle nil, type-check it, and retain the typed client on the action. Provider `Configure` supplies it through `resp.ActionData`. `Meta()`, `conns`, `framework.ActionWithConfigure` and generated `service_package_gen.go` belong to particular repositories, not the public framework.
5. In `Invoke`, decode `req.Config` into a model with public `types.String`, `types.Int64`, etc.; append diagnostics and stop on errors. Recheck required client/configuration rather than panicking.

The executable [provider example](../../examples/reference-go/provider.go) exercises these interfaces against a pinned framework. The API-specific client is deliberately an injected interface, not an invented cloud SDK method.

```go
var _ action.Action = (*RestartAction)(nil)
var _ action.ActionWithConfigure = (*RestartAction)(nil)

func (a *RestartAction) Schema(_ context.Context, _ action.SchemaRequest, resp *action.SchemaResponse) {
    resp.Schema = actionschema.Schema{
        Attributes: map[string]actionschema.Attribute{
            "target": actionschema.StringAttribute{Required: true},
        },
    }
}
```

## Invocation, progress and effects

Use `resp.SendProgress(action.InvokeProgressEvent{Message: "..."})`; `resp.Progress.Set` is not a framework API. Progress is informational, not proof of successful completion. Report diagnostics when the operation fails and include only safe, useful details.

Honor the passed context and an accepted operation timeout. Do not start a goroutine merely to emit progress; use cancellable polling or a bounded ticker when a real asynchronous API requires it, and join every worker. Canceling a local request may not cancel a remote operation: reconcile unknown outcomes before retrying. State the API's idempotency semantics rather than marking every imperative action retry-safe.

Never perform the action during schema/configuration validation or planning. A plan-time API validation, when authorized, is not permission to restart, delete or mutate infrastructure.

## Verification and publication

Compile against the repository's pinned framework. Check registration, missing/wrong provider data, invalid/unknown config, cancellation, remote failure, unknown outcome, repeated invocation and progress/error propagation. A unit test with a fake API client proves local behavior, not cloud acceptance. Run real action acceptance tests only with explicit credentials and side-effect authorization; label unrun checks.

Use the repository's normal layout. Terraform Registry documentation source goes through `terraform-provider-docs`; don't impose AWS-provider-specific `website/docs/actions` or `.changelog` conventions on another provider.

Sources: [implementation and registration](https://developer.hashicorp.com/terraform/plugin/framework/actions/implementation), [action schema](https://pkg.go.dev/github.com/hashicorp/terraform-plugin-framework/action/schema), [provider interfaces](https://pkg.go.dev/github.com/hashicorp/terraform-plugin-framework/provider).
