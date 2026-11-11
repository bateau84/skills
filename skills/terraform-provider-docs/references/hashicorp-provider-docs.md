# HashiCorp Provider Documentation Reference

Source of truth for this skill:
- https://developer.hashicorp.com/terraform/registry/providers/docs

## Core Rules

- Publish provider docs through Terraform Registry using `tfplugindocs`.
- Generate provider docs from schema descriptions and markdown templates.
- Store templates under the repository `templates/` directory with expected naming conventions; generated output goes to `docs/`.
- Keep release tags and manifest metadata valid so Registry can render and display docs.

## Template Paths

Use these template paths when the corresponding provider objects exist:

- `templates/index.md.tmpl`
- `templates/data-sources/<name>.md.tmpl`
- `templates/resources/<name>.md.tmpl`
- `templates/ephemeral-resources/<name>.md.tmpl`
- `templates/list-resources/<name>.md.tmpl`
- `templates/functions/<name>.md.tmpl`
- `templates/guides/<name>.md.tmpl`

## Generation Workflow

HashiCorp recommends wiring generator execution through `go generate`:

```go
//go:generate go run github.com/hashicorp/terraform-plugin-docs/cmd/tfplugindocs generate --provider-name <provider_name>
```

Run from repository root:

```bash
go generate ./...
```

Alternative direct execution:

```bash
go run github.com/hashicorp/terraform-plugin-docs/cmd/tfplugindocs generate --provider-name <provider_name>
```

## Release and Publication Constraints

- Use semantic version tags prefixed with `v`.
- Publish the version as a GitHub release; the tag must be a valid semantic version preceded by `v`, and no branch may have the same name as the tag.
- Publishing creates a webhook on the repository; if it is missing or duplicated, remove the extra webhooks and use Resync on the provider settings page.
- Keep `terraform-registry-manifest.json` in the repository root.
- Understand docs appear by provider version in Registry once the provider release is published.

## Preview and Troubleshooting

- Use HashiCorp's preview process to verify rendering before release when needed.
- If docs are missing or stale in Registry, verify:
  - tag naming, and that no branch shares the tag's name
  - the Registry webhook exists (Resync recreates it)
  - manifest file presence and validity
  - provider version publication state

## Related Canonical Pages

- Provider docs guidance:
  - https://developer.hashicorp.com/terraform/registry/providers/docs
- Terraform Plugin Docs (`tfplugindocs`) source and usage:
  - https://github.com/hashicorp/terraform-plugin-docs
