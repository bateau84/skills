---
name: terraform-provider-resources
description: Implement Terraform Provider resources and data sources using the Plugin Framework. Use when developing CRUD operations, schema design, state management, and acceptance testing for provider resources.
metadata:
  copyright: Copyright IBM Corp. 2026
  version: "0.0.1"
---

# Terraform Plugin Framework Resources

Implement the **public Plugin Framework**, not a mixture of legacy SDKv2 and the Terraform AWS provider's private helper packages. Follow existing repository conventions and pinned framework/CLI versions. Use `terraform-provider-testing` for acceptance machinery and `terraform-provider-docs` for Registry output.

## Model, registration and configuration

A managed resource implements `resource.Resource` with `Metadata`, `Schema`, `Create`, `Read`, `Update`, and `Delete`. Add `resource.ResourceWithConfigure` when it needs a provider client; optional import support uses `resource.ResourceWithImportState`. Register its constructor in `provider.Provider.Resources`. A data source implements the separate `datasource.DataSource` interface and is registered in `DataSources`; do not give it managed-resource CRUD semantics.

```go
type WidgetResource struct { client WidgetClient }

var _ resource.Resource = (*WidgetResource)(nil)
var _ resource.ResourceWithConfigure = (*WidgetResource)(nil)

func (r *WidgetResource) Configure(_ context.Context, req resource.ConfigureRequest, resp *resource.ConfigureResponse) {
    if req.ProviderData == nil { return }
    client, ok := req.ProviderData.(WidgetClient)
    if !ok {
        resp.Diagnostics.AddError("Unexpected provider data", "Expected WidgetClient")
        return
    }
    r.client = client
}
```

`WidgetClient` is an application interface the provider supplies, not a framework API. Provider `Configure` puts the configured client in `resp.ResourceData` (and `DataSourceData` for data sources). Check nil before operations. Interfaces such as `framework.ResourceWithConfigure`, `r.Meta()`, `conns.AWSClient`, `tfresource`, `tftags`, `acctest` and service-registration generators are **Terraform AWS provider internals**. Use them only inside that repository with its actual imports and conventions; they are not portable stand-alone examples.

## Schema and unknown values

Use `resource/schema` and `types` from `github.com/hashicorp/terraform-plugin-framework`. Give each model field a matching `tfsdk` tag. Required, optional and computed have different contracts; select them from the API, not from desired test output. Keep null and unknown distinct until the value is established.

For a server-generated identity, a public schema uses `schema.StringAttribute{Computed: true}` and a `types.String` model field. Apply `UseStateForUnknown` only when that value is actually stable; a blanket modifier can hide replacement or update semantics. Set replacement modifiers for immutable configured properties when required by the API.

## CRUD as a state contract

**Create:** read the plan, stop on diagnostics, call the API with context, capture the returned identity, then populate the complete persisted state. Preserve that identity when a subsequent read fails so that users can reconcile an already-created object instead of creating a duplicate.

**Read:** decode prior state and refresh it from the API. A confirmed absent managed object removes the resource from state with `resp.State.RemoveResource(ctx)`. Authentication, timeout, permission denial and eventual-consistency delay are not “not found”; keep the prior identity and return a useful diagnostic. A data-source lookup not found normally returns a diagnostic, not a resource-state removal.

**Update:** read the proposed plan, apply only allowed changes, and persist values consistent with the plan and confirmed API response. For unknown results, reconcile before retrying. Do not reset a known stable identity just because the plan has unknown computed fields.

**Delete:** read prior state, invoke a cancellable deletion, and verify the accepted deletion completion condition. An API's confirmed already-absent response may count as successful deletion. Do not report success on a generic error or an operation merely queued unless that is the agreed deletion contract.

Use bounded polling for eventual consistency and asynchronous operations, with an explicit terminal condition and cancellation. Never hide arbitrary API failures behind retry loops.

## Import and tests

An import method can call `resource.ImportStatePassthroughID(ctx, path.Root("id"), req, resp)` when the public import contract is exactly that identity. Composite identifiers need real parsing/validation and must round-trip through `Read`.

Test Create → Read → Update → Read → Delete, absent objects, cancellation, malformed import, drift, sensitive values, unknown plans and failed post-create reads. Acceptance checks must exercise the actual provider with a safe account, then verify cleanup. Examples copied from terraform-provider-aws may depend on its `acctest` utilities and are not a substitute for a compiling standalone test.

Before claiming completion: compile/type-check the changed package, validate schema diagnostics, inspect state after failures, run the relevant acceptance lane when authorized, and distinguish unrun cloud operations from successful unit tests. Preserve provider-prefix documentation and repository publication policy rather than inventing a `website/docs/r` layout.

Sources: [resources](https://developer.hashicorp.com/terraform/plugin/framework/resources), [data sources](https://developer.hashicorp.com/terraform/plugin/framework/data-sources), [public Configure interfaces](https://pkg.go.dev/github.com/hashicorp/terraform-plugin-framework/resource#ResourceWithConfigure).
