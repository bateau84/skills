// Version-pinned public Framework example; injected client, no cloud calls.
package reference

import (
	"context"
	"github.com/hashicorp/terraform-plugin-framework/action"
	actionschema "github.com/hashicorp/terraform-plugin-framework/action/schema"
	"github.com/hashicorp/terraform-plugin-framework/datasource"
	"github.com/hashicorp/terraform-plugin-framework/provider"
	providerschema "github.com/hashicorp/terraform-plugin-framework/provider/schema"
	"github.com/hashicorp/terraform-plugin-framework/resource"
	"github.com/hashicorp/terraform-plugin-framework/types"
)

type ActionClient interface {
	Restart(context.Context, string) error
}
type RestartAction struct{ client ActionClient }

var _ action.Action = (*RestartAction)(nil)
var _ action.ActionWithConfigure = (*RestartAction)(nil)

func NewRestartAction() action.Action { return &RestartAction{} }
func (a *RestartAction) Metadata(_ context.Context, req action.MetadataRequest, resp *action.MetadataResponse) {
	resp.TypeName = req.ProviderTypeName + "_restart"
}
func (a *RestartAction) Schema(_ context.Context, _ action.SchemaRequest, resp *action.SchemaResponse) {
	resp.Schema = actionschema.Schema{Attributes: map[string]actionschema.Attribute{
		"target": actionschema.StringAttribute{Required: true},
	}}
}
func (a *RestartAction) Configure(_ context.Context, req action.ConfigureRequest, resp *action.ConfigureResponse) {
	if req.ProviderData == nil {
		return
	}
	client, ok := req.ProviderData.(ActionClient)
	if !ok {
		resp.Diagnostics.AddError("Unexpected provider data", "Expected ActionClient")
		return
	}
	a.client = client
}
func (a *RestartAction) Invoke(ctx context.Context, req action.InvokeRequest, resp *action.InvokeResponse) {
	var config struct {
		Target types.String `tfsdk:"target"`
	}
	resp.Diagnostics.Append(req.Config.Get(ctx, &config)...)
	if resp.Diagnostics.HasError() {
		return
	}
	if a.client == nil || config.Target.IsNull() || config.Target.IsUnknown() || config.Target.ValueString() == "" {
		resp.Diagnostics.AddError("Incomplete action configuration", "A configured client and known nonempty target are required")
		return
	}
	if err := ctx.Err(); err != nil {
		resp.Diagnostics.AddError("Action canceled", err.Error())
		return
	}
	resp.SendProgress(action.InvokeProgressEvent{Message: "Restart requested"})
	if err := a.client.Restart(ctx, config.Target.ValueString()); err != nil {
		resp.Diagnostics.AddError("Restart failed", "Reconcile the remote operation before retrying; inspect provider diagnostics")
	}
}

type ExampleProvider struct{ Client ActionClient }

var _ provider.ProviderWithActions = (*ExampleProvider)(nil)

func (*ExampleProvider) Metadata(_ context.Context, _ provider.MetadataRequest, resp *provider.MetadataResponse) {
	resp.TypeName = "example"
}
func (*ExampleProvider) Schema(_ context.Context, _ provider.SchemaRequest, resp *provider.SchemaResponse) {
	resp.Schema = providerschema.Schema{}
}
func (p *ExampleProvider) Configure(_ context.Context, _ provider.ConfigureRequest, resp *provider.ConfigureResponse) {
	resp.ActionData = p.Client
}
func (*ExampleProvider) Resources(context.Context) []func() resource.Resource       { return nil }
func (*ExampleProvider) DataSources(context.Context) []func() datasource.DataSource { return nil }
func (*ExampleProvider) Actions(context.Context) []func() action.Action {
	return []func() action.Action{NewRestartAction}
}
