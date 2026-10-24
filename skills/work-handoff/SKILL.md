---
name: work-handoff
description: Turn chat decisions, ideas, plans, action points, bugs, faults, enhancements, investigations, and cross-component dependencies into a self-contained work assignment for a fresh agent or another system. Use when asked to hand off, package, transfer, or preserve work so a recipient without the original conversation can act on it. Not for GitHub issue tracking mechanics (use github-issue) or detailed execution planning (use work-decomposition).
---

# Work Handoff

Produce a **standalone work contract**, not a conversation summary. Someone arriving in a fresh session must understand what the work is, why it matters, what is already decided, what must remain true, and how to recognize a useful result. The recipient may need to investigate the actual codebase, but must not need the source chat to recover the intent.

A handoff can be pasted into another agent session, stored as a document, or published as a GitHub issue. **This skill owns the meaning; the destination does not change that meaning.** Use `github-issue` for publishing, relationships, metadata, and other GitHub-specific management. Neither skill creates permission to implement an unapproved idea.

## Scope and authority

- Preserve **accepted** intent, requirements, constraints, exclusions, and relevant decisions. A question, example, agent proposal, or convenient implementation is not automatically approved.
- Treat later explicit corrections as superseding earlier suggestions. Preserve unresolved contradictions as decisions, not as invented conclusions.
- Explain the required outcome before prescribing a mechanism. Include a required method or interface only when it was actually established.
- Distinguish observations, reported symptoms, hypotheses, and unverified repository claims. Do not invent root causes, reproduction steps, paths, sources, tests, or owners.
- Do not convert the handoff into a scheduler, fixed agent chain, task-by-file breakdown, or authorization to modify code. The recipient uses its normal project instructions and planning/review practices.
- An issue or another session may be the destination, not the source of authority. Publishing does not approve an undecided product choice.

## Method

1. **Identify the work and receiver.** Establish the outcome or bounded question and the repository, component, or responsibility that should address it, when known. A mentioned repository is not necessarily the target. Do not invent a target.
2. **Recover the final intent.** Extract the latest accepted decisions from the conversation and relevant accessible artifacts. Separate accepted requirements, optional ideas, rejected approaches, and unresolved questions. Keep only the history needed to explain consequential choices.
3. **Check the current reality where possible.** Consult relevant project files, specifications, issues/PRs, and observed evidence when accessible. Verify claimed behavior and whether the work is already complete. An old observation is not proof of the current state; mark unsupported details as unverified.
4. **Choose a useful work unit.** Keep one coherent responsibility and outcome per handoff. If there are truly independent outcomes or owners, prepare separate handoffs and explain their connection. Avoid one handoff per substep or file. Use `work-decomposition` when grouping is actually difficult.
5. **Make readiness truthful.**
   - **Implementation:** the desired outcome and governing constraints are agreed; routine engineering discovery and design can be left to the recipient.
   - **Investigation:** the problem or question is clear, but cause, impact, feasibility, or evidence still needs work. Acceptance is a bounded finding and recommendation, not an unapproved fix.
   - **Decision/proposal:** a user-owned scope, product meaning, or risk choice is open. State who should decide and what evidence/options are available; do not frame implementation as already approved.
6. **Capture the necessary context.** Describe the relevant current behavior, reason the work arose, accepted target behavior, boundaries, preserving guarantees, cross-component dependencies, and known evidence. Link durable accessible records; inline essential facts when the future recipient cannot access a session link or private artifact. Do not paste the whole chat.
7. **Define completion at the right boundary.** Use falsifiable, observable acceptance criteria or a clear investigation/decision deliverable. For a feature or bug, cover relevant regression or interaction behavior; for a cross-component dependency, describe what the receiving side must expose to its consumer. Distinguish what remains to verify from what is already proven.
8. **Surface uncertainty without fabricating closure.** Separate routine implementing-agent choices from genuinely reserved product/architecture decisions. Identify blocking questions, affected owners, and immediate next step where necessary. Avoid turning optional detail into blocking ceremony.
9. **Run the cold-start test.** Read only the proposed handoff, without source chat. Can the recipient explain the intended result, accepted limits, evidence, unresolved decisions, and success checks? If not, repair the artifact. Then stop; do not execute the work unless separately requested.

## Default artifact

Use clear, compact Markdown unless the caller or destination requires another format. Omit optional sections that add no value. The headings are guidance, not a fixed schema.

~~~markdown
# <Short outcome-oriented title>

**Work:** Implementation | Investigation | Decision/proposal
**Target:** <Known repository, component or responsibility, if any>

## Objective
<What should become true, or what question must be resolved, and why>

## Context and evidence
<Relevant current state, observations, provenance, important accepted decisions>

## Requirements and boundaries
<Accepted outcomes; critical MUST/SHOULD/MAY distinctions where useful>
<Constraints and important exclusions>

## Acceptance
- <Observable condition or bounded investigation/decision deliverable>
- <Regression/integration proof when relevant>

## Dependencies and references
<Durable applicable specifications, issues, PRs, paths, other work>

## Open decisions
<Only genuinely unresolved decisions, their owners, and consequences>
~~~

A small change may need only objective, context, and acceptance. A complicated migration may need more constraints and evidence. Stable IDs (for example `REQ-001`, `AC-001`) are useful when requirements are already referenced; avoid numbering merely for formality.

### Domain-specific handoff

- **Bug/fault:** observed versus expected behavior, reproduction **if known**, affected environment, evidence, and a verification target. Separate a known defect from a possible diagnosis.
- **Adjustment/enhancement:** desired change plus what must **remain** compatible or unchanged.
- **Feature:** user-observable capability, scope, exclusions, and accepted success criteria.
- **Investigation:** the question, currently known facts, limits on evidence, and the decision or result to produce.
- **Plan/action points:** preserve accepted outcomes, dependencies, and sequencing constraints; don't turn the handoff into a second detailed execution plan.
- **Cross-component dependency:** clearly distinguish source need, target responsibility, externally observable contract, requirement strength, and required versus suggested interfaces. For a structured variant and example, read [Cross-component handoffs](references/cross-component.md).

## Output and delivery

When asked to *prepare a handoff*, output the artifact without a long preface. If asked to *create a GitHub issue*, use this skill to preserve the intended work, then `github-issue` to publish and organize it. The receiving agent must be able to read the issue alone. If GitHub tooling or target access is absent, provide a paste-ready artifact and be explicit that no issue was created. Do not assign, implement, or publish work based solely on the act of preparing a handoff.

Keep credentials, personal data, private customer context, and inaccessible source artifacts out of public destinations. A link alone is insufficient if the receiving agent has no access to the underlying source.
