---
name: terraform-provider-docs
description: Create, update, and review Terraform provider documentation for Terraform Registry using HashiCorp-recommended patterns, tfplugindocs templates, and schema descriptions. Use when adding or changing provider configuration, resources, data sources, ephemeral resources, list resources, functions, or guides; when validating generated docs; and when troubleshooting missing or incorrect Registry documentation.
---

# Terraform Provider Docs

## Follow This Workflow

1. Confirm scope and documentation targets.
- Map code changes to the exact doc targets: provider index, resources, data sources, ephemeral resources, list resources, functions, or guides.
- Decide whether content should come from schema descriptions, templates, or both.

2. Write schema descriptions first.
- Add precise user-facing descriptions to schema fields so generated docs stay aligned with behavior.
- Keep wording specific to argument purpose, constraints, defaults, and computed behavior.

3. Add or update template files in `templates/`.
- Create only files that map to implemented provider objects.
- Use HashiCorp-recommended template paths:
  - `templates/index.md.tmpl`
  - `templates/data-sources/<name>.md.tmpl`
  - `templates/resources/<name>.md.tmpl`
  - `templates/ephemeral-resources/<name>.md.tmpl`
  - `templates/list-resources/<name>.md.tmpl`
  - `templates/actions.md.tmpl` (generic) and `templates/actions/<action type name>.md.tmpl` (per action)
  - `templates/functions/<name>.md.tmpl`
  - `templates/guides/<name>.md.tmpl`
- Omit the provider prefix from `<name>` (`templates/resources/widget.md.tmpl` for `acme_widget`). Render the generated schema with `{{ .SchemaMarkdown | trimspace }}`.
- Keep templates focused on overview and examples; rely on generated sections for field-by-field details.
- Example directories for resources and data sources include the provider prefix: `examples/resources/acme_widget/resource.tf`, `examples/data-sources/acme_widget/data-source.tf`; actions use `examples/actions/<action_type>/action.tf`. Template file names omit the prefix.
- Examples for list resources use the `.tfquery.hcl` extension (`examples/list-resources/<name>/list-resource.tfquery.hcl`).
- Migrating hand-written docs from `website/docs/r` or `docs/resources`: run `tfplugindocs migrate` instead of deleting and recreating them.

4. Generate documentation with `tfplugindocs`.
- Prefer repository defaults when configured:
```bash
go generate ./...
```
- Otherwise run the generator directly:
```bash
go run github.com/hashicorp/terraform-plugin-docs/cmd/tfplugindocs generate --provider-name <provider_name>
```
- Re-run generation after every schema or template edit.

5. Validate the generated markdown.
- Verify files in `docs/` match the current provider implementation.
- Verify examples are valid HCL and reflect current argument/attribute names.
- Verify required/optional/computed semantics in docs match schema behavior.

6. Apply Registry publication rules before release.
- Use semantic version tags prefixed with `v` (for example `v1.2.3`).
- Publish the version as a GitHub release (the Registry ingests it through a webhook), and make sure no branch has the same name as the tag (for example a branch named `v1.2.3`).
- Keep `terraform-registry-manifest.json` in the repository root.
- Expect docs to be versioned in Registry and switchable with the version selector.

7. Preview or troubleshoot publication when needed.
- Use the HashiCorp preview process to inspect rendered docs before release when accuracy risk is high.
- If docs are missing in Registry, check tag format, whether a branch shares the tag's name, that the Registry webhook exists (remove duplicate webhooks, then use Resync on the provider settings page), manifest file presence, and provider publication status.

## Enforce Quality Bar

- Keep documentation behaviorally accurate; never describe unsupported arguments or attributes.
- Keep examples minimal, realistic, and runnable.
- Keep terminology and naming consistent across provider, resources, and data sources.
- Avoid duplicating generated argument/attribute blocks in manual templates.
- Keep doc changes tied to the same PR as schema/API changes whenever possible.

## Load References On Demand

- Read `references/hashicorp-provider-docs.md` for source-backed rules and official links.
- Load only the sections needed for the current change to keep context lean.
