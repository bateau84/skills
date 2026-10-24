# GitHub Issue — Quality Assurance

Assume normal issue-management checks passed. Probe failure modes where the GitHub UI appears organized but reality is misleading.

## QA criteria

- **Fake hierarchy:** An issue body links child issues or contains checkboxes, but the native sub-issue relationship and project roll-up do not exist.
- **Fake sequencing:** A parent-child relationship appears to express "blocked by"; agents may start dependent work before prerequisites because a native blocking relation was never created.
- **Concurrent body overwrite:** A metadata edit or template rewrite resets another agent's completed checkboxes, new evidence, or acceptance changes.
- **Readable front, opaque contract:** The introduction is understandable but the acceptance checkboxes still use vague or academic terms, hide rejected options or include an invented stronger promise. A human approves the apparent goal without noticing the actual work would differ.
- **Simplification hides regression:** A well-intentioned rewrite drops a necessary failure condition, compatibility guarantee or precise term, making the issue easier to read but impossible to verify against the approved behavior.
- **Duplicate under retries:** An ambiguous create timeout leads to duplicate issues because the published list was not checked before retry.
- **Misleading owner/status:** Labels, assignee or Project status convey authorization or completion that neither the owner nor evidence actually granted.
- **Two sources of Priority:** The organization issue field and a Project custom field have the same name but different values, and an agent wrongly treats them as one.
- **Field visibility trap:** An unpinned or organization-only field is hidden from the agent, leading it to declare the field absent, invent a duplicate, or reveal restricted data.
- **Automation feedback:** Changing Project Status triggers a configured issue-closing workflow, unexpectedly overriding accepted open-issue state.
- **Project draft illusion:** A Project-only draft is reported as a published repository issue; repository-specific labels or milestones are attached before conversion.
- **Milestone as deadline:** A repository milestone's due date is stated as an issue-specific deadline or confused with a similarly named milestone elsewhere.
- **Form-value illusion:** A dropdown submitted through an issue form becomes body Markdown but is treated as if it had populated a native organization issue field.
- **Orphaning and cross-repo confusion:** A moved sub-issue loses a meaningful parent, an issue number resolves in the wrong repository, or a closed parent conceals open required children.
- **False completion:** A PR is merged or a checkbox is ticked while product acceptance, integration, rollout or a referenced blocker remains unresolved.
- **Confidentiality and hostile content:** A public issue exposes sensitive logs, and untrusted issue comments can instruct the agent to change permissions or ignore repository policy.

Challenge plausible false confidence, not unrelated process preferences. This file grants no authority to alter issue governance or close work without evidence.
