# GitHub Issue Metadata and Projects

Load this reference for GitHub issue types, milestones, Project membership, Project custom fields, organization issue fields, or issue forms. The normal `SKILL.md` owns issue creation, checkboxes, sub-issues, dependencies and safe lifecycle changes.

## 1. Identify where metadata belongs

| Construct | Scope | Use for | Do not confuse with |
| --- | --- | --- | --- |
| Issue type | Organization-managed, applied to issues | Work classification (often Task, Bug, Feature) | Repository label |
| Labels | Repository | Filtering, local categories and automation | Typed field or authorization |
| Assignee | Issue | Responsible GitHub identity | Work approval or scheduling |
| Milestone | Repository, covers issues/PRs | Release or delivery group, roll-up and optional due date | Individual issue deadline or cross-repo Project |
| Organization issue field | Organization-defined, value on **the issue** | Shared Priority, Effort, Severity, Start/Target date | Project-local custom field |
| GitHub Project | User or organization | Cross-repository table, board or roadmap | Repository milestone |
| Project custom field | Individual Project item | Local Status, Iteration, estimates, notes or priority | Issue state or shared organization issue field |
| Issue form/template | Repository | Collect bug details, examples and reproduction | Native typed issue field |
| Sub-issue / blocked-by | Native issue relationships | Separate deliverables / prerequisites | Markdown reference or checkbox |

An issue can belong to multiple Projects; the same Project-local field name may have a **different value in each Project**. Organization issue field values remain the same across Projects, because they belong to the issue. Prefer one authoritative source for a concept such as Priority; avoid hidden duplicates in labels, org fields and per-Project fields.

## 2. Types, labels, assignees and milestones

- **Issue types** are managed at organization level. Default types commonly include Task, Bug and Feature, but they can be disabled, renamed or customized. Select an available type that reflects the *kind* of work, not its status. Do not create/edit organization types while filing a normal issue.
- **Labels** are repository categories. Inspect actual labels and any automations that use them before application. A label such as `agent:ready` or `priority/high` has no built-in universal meaning; local rules govern it.
- **Assignees** must be known intended GitHub identities with suitable eligibility. Assignment may notify them or trigger configured automation. Do not assign an unrelated user just to avoid leaving the field empty.
- **Milestones** group issues and PRs in **one repository**. They can have a name, description and due date; GitHub tracks associated open/closed items and progress. A milestone due date is **not** a separately accepted issue deadline. Use an existing relevant milestone when applicable; do not create a release or new milestone without authority. Another repo's equally named milestone is unrelated.

All four are optional and can coexist. No combination is required as a universal template.

## 3. Organization issue fields

Organizations can configure structured **issue fields**. Supported types are **single-select, text, number, date**. They may provide Priority, Effort, Start date and Target date defaults when enabled, but each organization can edit or delete them. Verify actual names/options before setting a value.

- **Shared value:** An issue's field is consistent across Projects and repositories within the organization. A Project can display issue fields as columns; editing such a column edits the **issue's shared field**, not a new Project field.
- **Pinned fields:** Organization admins can pin fields to particular issue types, or issues without a type. Pinned fields appear in the sidebar/create modal. An unpinned field with no value may be hidden until `Add field` is selected. Absence from one view is not proof the field does not exist.
- **Visibility:** A field can be public or organization-only. Organization-only values may be absent from public views, public Projects, search suggestions and tool results. Do not copy restricted values into a public issue body.
- **Permissions:** Organization admins define fields; authorized repository users can set values where supported. GitHub currently supports issue fields on **issues, not PRs**.
- **Tools:** Use the issue sidebar or a verified API/connector that explicitly supports organization issue fields. Do not assume that `gh issue edit` or `gh project item-edit` can update these shared fields. If tool support is missing, state which value remains unset.
- **Filtering:** When supported and visible, search issues with field qualifiers such as `field.priority:high`, using actual configured field/option names. For fields with spaces, follow GitHub's documented quoting syntax.

If both an organization issue Priority and a Project custom Priority exist, don't silently overwrite both. Inspect ownership and intended mapping, and preserve established values until an authorized choice is made.

## 4. GitHub Projects and custom fields

A GitHub Project can contain issues, PRs and **Project draft issues**, including items from multiple repositories.

- **Membership:** Check whether the item is already in the relevant Project or will be auto-added by a configured workflow. Verify any requested addition; avoid duplicate work or membership in unrelated Projects.
- **Views:** Project table, board and roadmap views support filtering, sorting, grouping and field display. Views do not create separate issue contracts.
- **Project custom fields:** Available types include **single-select, text, number, date, iteration**. Common local fields include Status, Priority, Estimate, Notes or Sprint; **names and options vary by Project**. Iterations represent configured recurring time blocks, not mandatory issue deadlines.
- **Built-in issue columns:** Project views can also show issue fields, assignees, issue types, milestones, parent/sub-issue progress and linked PRs. These display the connected issue's data rather than independent local values.
- **Status versus state:** An issue is open/closed; `Status` may be a Project custom single-select field. A Project automation may set status to Done when an issue closes, or close an issue when a status changes. Inspect the configured workflows before changing either.
- **Project drafts:** Draft issues exist only in a Project until converted into repository issues. They can have title, body, assignee and custom fields; repository labels/milestones require conversion. Do not report a repository issue number, state or URL before creation.
- **Permissions:** Check actual Project access and GitHub CLI's `project` token scope. Issue permissions alone do not prove Project field write capability. Do not modify credentials, scopes or Project workflows as an unannounced side effect.

## 5. Practical operational method

1. Identify the exact owner/repo/issue and check the existing body, type, labels, milestone, assignee, issue fields, Project items, local Project fields and relationships **where available**.
2. Inspect organization issue type and field definitions, Project field choices and workflows, and repository templates/milestones/labels. Distinguish an inaccessible field from a nonexistent one.
3. Select only relevant tracking metadata: classification via type/labels; repo release via milestone; shared facts via org issue field; Project team workflow via membership/custom fields.
4. Use values explicitly requested, already agreed through project conventions, or backed by evidence. Do not guess effort, severity, urgency, due date, owner or status.
5. Change the smallest supported surface and re-read it. A write to a Project field does not prove the org issue field changed. If any operation is unavailable, report partial completion and the exact missing part.

Example **only**: an accepted defect could have issue type `Bug`, a repo `backend` label, a `v2.1` milestone, shared org field `Priority: High`, and an Engineering Project item with its own `Status: In Progress`. Only set values that truly exist and were intended; these are not universal defaults.

## 6. Verified GitHub CLI examples

Check the available version and `--help` flags first. The following are **individual** actions, not a mandatory sequence:

~~~bash
# Inspect persisted issue metadata including project-item links
gh issue view 123 -R OWNER/REPO \
  --json title,state,labels,assignees,milestone,issueType,projectItems

# Apply existing type, milestone, Project membership
gh issue edit 123 -R OWNER/REPO --type "Bug" --milestone "v2.1"
gh issue edit 123 -R OWNER/REPO --add-project "Engineering"

# Inspect Project configuration and membership
gh project list --owner OWNER
gh project field-list 7 --owner OWNER
gh project item-list 7 --owner OWNER --field "Status"

# Add an existing issue only when not already present/auto-added
gh project item-add 7 --owner OWNER --url https://github.com/OWNER/REPO/issues/123

# Set the verified local Status option for this Project item
gh project item-edit 7 --owner OWNER \
  --url https://github.com/OWNER/REPO/issues/123 \
  --field "Status" --value "In Progress"

# Filter issues by an existing organization issue field when visible
gh issue list -R OWNER/REPO --search 'field.priority:high'
~~~

The `gh project` family needs the appropriate `project` token scope. Check with `gh auth status`; a human may need to authorize it via `gh auth refresh -s project`. Do not change token scopes without user authorization. Project item operations can also use verified GraphQL node IDs for scripts; never invent them. For a non-draft issue, update one Project field at a time and verify the saved value.

**Org issue fields use a different operation surface.** If the connector/CLI supports only issue types/labels/Projects, use GitHub's web sidebar or an explicitly supported issue-field API. Do not claim the org issue field changed merely because a similarly named Project field was edited.

## 7. Templates, forms, closure and visibility

- Existing `.github/ISSUE_TEMPLATE/` Markdown templates and YAML forms can predefine a layout, labels, assignees, type or Projects. Inspect their meaning; preserve agreed acceptance, and do not require empty ceremonial sections.
- Issue-form dropdowns and checkboxes become **Markdown body content**. They are not automatically structured organization issue fields or Project custom fields. An explicit existing automation might map them; verify that before claiming structured reporting works.
- Closing reasons include completed and not planned. Closing an issue differs from archiving a Project item, deleting a Project draft or completing a milestone. A PR merge or Project `Done` column does not by itself prove acceptance, even when automation updates status.
- Private project fields and issue fields can have different visibility from the public issue body. Avoid exposing restricted metadata in a public comment or handoff.

## Official sources

- [Organization issue types](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization)
- [Organization issue field definitions](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-fields-in-your-organization)
- [Issue field values and visibility](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/adding-and-managing-issue-fields)
- [Issue fields in Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields/about-issue-fields)
- [Milestones](https://docs.github.com/en/issues/using-labels-and-milestones-to-track-work/about-milestones)
- [Projects](https://docs.github.com/en/issues/planning-and-tracking-with-projects/learning-about-projects/about-projects)
- [Project field types](https://docs.github.com/en/issues/planning-and-tracking-with-projects/understanding-fields)
- [Project items and drafts](https://docs.github.com/en/issues/planning-and-tracking-with-projects/managing-items-in-your-project/adding-items-to-your-project)
- [Project automations](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-built-in-automations)
- [Issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [GitHub CLI: issue edit](https://cli.github.com/manual/gh_issue_edit), [Project item edit](https://cli.github.com/manual/gh_project_item-edit)

Confirm version-sensitive details against the current GitHub environment and CLI before operations.
