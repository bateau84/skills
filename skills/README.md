# Skill Library

Skills are on-demand methodology for any agent or human practitioner. Load them with a native skill tool or read the files directly; no particular agent structure or plugin is assumed.

## Context files

| File | Activity | Purpose |
| --- | --- | --- |
| `SKILL.md` | Practice | **How do I do this work well?** Required. |
| `ASSESSMENT.md` | Review | **Did the work satisfy its inputs and domain obligations?** Optional. |
| `QA.md` | Adversarial validation | **How could this still be wrong after competent work and review?** Optional. |

Any agent may use any of these files for the relevant activity. Review and QA are different perspectives, not fixed agent identities or mandatory workflow stages. QA is not merely stricter assessment. Companions are optional and should add domain-specific value.

`SKILL.md` should support ordinary practice, including the checks needed to produce sound work, without requiring either companion. One agent may use all three perspectives, but switching files does not make its review independent; describe who performed the checks and what evidence they used when independence matters.

## Selecting methodology

| Work | Useful skills |
| --- | --- |
| Product intent and discovery | intent-grilling, product-discovery, risk-driven-planning |
| Human experience | user-story, design-scenario, design-specification, surface/design skills; design-validation for implemented experiences |
| Observable requirements | behavioral-spec, behavioral-requirement, quality-scenario, obligation-contract |
| Technical structure and contracts | architectural-design, architectural-decision, architectural-spec |
| Delivery planning | work-decomposition, risk-driven-planning |
| End-to-end outcome proof | product-acceptance |
| Documentation and knowledge | documentation, learning, report-lifecycle, report-to-keep |
| Cross-domain reconciliation | solution-synthesis, product-lifecycle |
| Implementation | software-engineering and task-relevant language/domain skills |
| Review | relevant assessment companions; design-review for design artifacts |
| Failure investigation | narrow troubleshooting/domain skills matching observed symptoms |
| Residual confidence testing | a small set of QA companions for load-bearing or risky domains |

These methods do not require a particular sequence, separate agents, additional approvals, or a master product document. Reuse the project's existing conversations, decisions, plans, and verification records. A documented decision establishes agreed scope; it does not by itself prove benefit or correctness.

## Loading discipline

Load the smallest useful set. A Go database task might use `golang-common-practice`, `golang-database`, and `golang-testing`, rather than every Go skill. Use `golang-how-to` or `python-how-to` for skill selection in those families.

For TypeScript, start with `typescript-common-practice` and add type safety, async, or testing guidance when material. Add `javascript-runtime` for execution semantics and `browser-runtime` for direct Web API work.

For human-facing work, combine information architecture, interaction design, user flows, visual interface design, accessibility, and surface-specific guidance only for dimensions in scope.

Use `feature-handoff` when another component, repository, or fresh session needs a self-contained implementation request.

Relative references resolve from the skill directory. Bare skill names refer to sibling directories. Examples and artifact identifiers describe useful formats; follow local naming and storage conventions. External CLIs, services, and MCP integrations are explicitly task-specific, not prerequisites for loading the library.

Local `evals/` files contain behavioral scenarios and expected observations. They can be used manually or adapted to a host's evaluation tools; no evaluation framework is required.

The collection also offers [optional root evaluation tooling](../docs/evaluations.md)
for explicitly loaded baseline/candidate trials through a pinned external runner.
It does not add a skill-loading runtime dependency or replace the preserved
four-variant protocol/pilot. [Verification records](../docs/eval-verification.md)
distinguish provider-free harness tests from unexecuted live model trials.

See `PORTING.md` for provenance.
