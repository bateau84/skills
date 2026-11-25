# Completion and evidence

Use this reference when defining or reviewing the point at which a product change, milestone, task, or investigation is complete. The normal method remains in `SKILL.md`; this reference explains the distinctions and their grounding.

## Give each kind of statement one job

| Statement | Question it answers |
| --- | --- |
| Purpose and parent goal | Why does this work matter, and which larger outcome does it advance? |
| Scope and responsibility | What does this assignment own, preserve, and exclude? |
| Acceptance criteria | Which observable conditions establish this particular outcome? |
| Definition of Done | Which shared quality obligations apply to completed work? |
| Evidence and return boundary | What establishes fulfillment, and when should the owner return or report a blocker? |

Together these form a **completion contract**. This is a useful name for existing information, not a new required document, schema, status service, or approval stage. Keep it in the accepted request, plan, issue, specification, or handoff. Link the owning sources instead of copying them into a competing authority.

Reuse the project's Definition of Done. Its relevant obligations may include verification, compatibility, documentation, maintainability, security, and review, according to the actual project. Work-specific criteria do not replace that baseline; the baseline does not invent a new product feature. Where no named baseline exists, make applicable existing quality obligations explicit. Do not fabricate numeric thresholds or require a new organizational policy before a simple change can proceed.

## Keep the claim at its actual level

A task can complete one contribution while the milestone still needs another contribution or integration proof. A milestone can deliver a useful increment while later product capabilities remain. Define completion for the bounded goal or version; ongoing ownership of a product is not an endless task.

An architecture assignment can finish with a coherent, reviewable design whose obligations, interfaces, open decisions, and conformance checks are clear. That is evidence about the design artifact. The implementation later needs its own evidence that it conforms and serves the accepted user outcome. A verification plan is not the result of running it.

An investigation can finish by disproving a proposed approach. For example, testing whether an existing storage primitive can provide the accepted atomic update may establish that it cannot. A bounded finding, reproducible evidence, and the resulting owner decision can satisfy the investigation, while the dependent implementation remains blocked. If required evidence was unavailable, say so; neither exhaustion nor an expired timebox proves the answer.

## Example: a bounded CLI change

The parent goal is to let a scheduled operator script read job state without parsing presentation text. This assignment adds `status --json`; a future monitoring dashboard is outside its scope.

Acceptance is observable: the command returns the agreed fields and exit meanings, and the existing text mode remains compatible. The applicable Definition of Done supplies the existing repository's regression, documentation, and review obligations. Evidence comes from the real command with representative success and failure inputs, relevant compatibility checks, and the changed usage documentation. No universal coverage percentage or live production deployment is implied.

Once those conditions have sufficient current evidence, return the scoped result. A concrete serialization defect remains required work even if a checklist missed it. A speculative dashboard or unrelated naming cleanup is advisory. If a required platform check could not run, identify the missing proof and its effect on completion instead of reporting an unqualified DONE.

## Stop, block, and reopen truthfully

- **DONE:** the assigned outcome and applicable quality obligations are supported by sufficient current evidence.
- **PARTIAL:** useful work is preserved, but some assigned work or required proof remains.
- **BLOCKED:** a missing prerequisite, permission, or owner decision prevents necessary progress. Preserve independent useful work where possible.

Use the host's equivalent states when it has them. Keep these assignment states separate from evidence statuses: PASS supports a particular checked claim, FAIL records a violation, and UNPROVEN records missing or inconclusive proof. An assessment can be complete with a FAIL finding while the assessed product remains incomplete.

Before extending work, identify the accepted outcome at risk and the evidence or decision the next step could change. Fix a real in-scope defect; investigate a credible material uncertainty proportionately; keep optional improvement separate. Reopen only affected completion claims when relevant changes or counterevidence undermine them. Do not restart broad review because an unchanged preference is repeated, and do not convert a loop limit or handoff into acceptance.

## Practice sources and adaptation limits

- [Scrum Guide, 2020](https://scrumguides.org/scrum-guide.html), Product Goal, Sprint Goal, Increment, and Definition of Done: a shared quality commitment and usable, integrated increments support transparent progress toward a larger goal. This library borrows those distinctions without requiring Scrum roles, events, or adoption.
- [Scrum.org: DoD and acceptance criteria](https://www.scrum.org/node/72145): DoD concerns the integrated Increment; acceptance criteria concern a particular backlog item. The broader completion-contract terminology above is this library's adaptation, not an official Scrum artifact.
- [NASA Systems Engineering Handbook §6.2](https://www.nasa.gov/reference/6-2-requirements-management/): parent/child and design/test traceability make missing obligations and unsupported additions visible. Use links and proportionate records here, not an aerospace-scale matrix by default.
- [NASA §5.3, Product Verification](https://www.nasa.gov/reference/5-3-product-verification/), and [§5.4, Product Validation](https://www.nasa.gov/reference/5-4-product-validation/): distinguish specified conformance from suitability for stakeholder expectations; plan, execute, and assess appropriate evidence at the claimed level. Their certification and project governance are not imported.
- [Google Engineering Practices: The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html): balance meaningful quality with progress and identify optional polish. This supports proportionate closure, not acceptance of a known required failure.
- [Agile Alliance: Timebox](https://agilealliance.org/glossary/timebox/): an agreed time limit ends an activity and prompts assessment of what was achieved. It does not establish that its goal was achieved.

These sources ground the method. They do not establish that this wording reduces agent cost or drift; that requires observed behavior from appropriately scoped evaluations or real runs.
