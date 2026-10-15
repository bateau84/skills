---
name: anchor-authoring
description: Capture and maintain a durable, user-accepted product or change Anchor that preserves intent, scope, and observable outcomes for independent agents and later sessions. Use when a material outcome needs shared semantic authority; not for technical architecture, task plans, or premature first-principles documents.
---

# Anchor Authoring

An Anchor preserves **what the user means and why it matters**, in a form that another agent can understand without the initiating conversation. It is product intent, not an implementation plan, an exhaustive specification, or an automatic approval gate.

Use for a new capability, a material change in intended behavior, or an ambiguity that will affect independent work. Reuse or amend an existing Anchor for smaller changes instead of creating a new one by default.

## Method

1. **Discover before drafting.** Read applicable existing product intent, requirements, design, and decisions through the repository's knowledge system. Inspect current behavior when it matters. An implementation is evidence of current reality, not authority to redefine the user's goal.
2. **Recover the user's actual request.** Preserve the intended benefit, affected users or actors, relevant context, and meaningful wording. Distinguish the user's explicit decisions from agent recommendations and inferred consequences. Do not paste a conversation transcript.
3. **Separate outcomes from solutions.** State what must be possible or observable, what is excluded, and which constraints are already accepted. Keep ordinary technology, component, or task choices open to later specialists.
4. **Resolve consequential ambiguity.** First consult existing sources. Ask the user only about unresolved choices they own and that materially change success, scope, guarantees, or risk acceptance. Explain the trade-off and recommend an option when useful; do not demand an interview when the request is already clear.
5. **Make the outcome falsifiable.** Define a small set of observable success/acceptance conditions and important negative boundaries. Do not invent numeric targets or guarantees where the user supplied none.
6. **Preserve decision lineage.** Record material choices, their reason, rejected alternatives when relevant, and outstanding questions. Mark proposals as proposals; do not silently convert exploratory language into commitments.
7. **Check for parallel-use ambiguity.** Ask whether independent agents could implement mutually incompatible meanings while still claiming they followed this Anchor. Resolve important semantic differences before relying on the Anchor for delegation; defer implementation detail.
8. **Present the interpreted intent.** Give the user a concise opportunity to correct material misunderstandings. Record acceptance only when it actually occurred. Do not claim acceptance from silence or a tool result. Small, already clear changes may use previously accepted authority without an extra ceremony.
9. **Publish to the repository's chosen location.** Follow its `AGENTS.md` (or equivalent), artifact naming rules, and `okf-authoring` if available. Make provenance and relevant relationships discoverable. No global folder structure, ID format, or harness command is imposed by this skill.
10. **Run the fresh-session test.** Another agent should understand the expected outcome, constraints, accepted decisions, and genuinely unresolved questions without the originating chat.

## Proportional artifact

Use only the sections required to retain meaning:

```markdown
# <Descriptive product or change outcome>

## Context and motivation
<The problem and who needs the result.>

## Intended outcome
<What the user wants to accomplish.>

## Observable success
- <Externally meaningful, falsifiable outcome>

## Scope and exclusions
<Relevant in-scope / out-of-scope boundaries.>

## Constraints and reserved decisions
<Accepted limits and decisions that require the user's authority.>

## Decisions and rationale
<Only material decisions already made, with their basis.>

## Open questions
<Only remaining unresolved, consequential questions.>

## Sources and acceptance
<Durable source references; accepted, proposed, or unconfirmed status,
with acceptance evidence when applicable.>
```

Do not copy placeholders or create empty sections. The repository's document-format skill owns frontmatter, index/log updates, and graph representation; this skill owns **substantive Anchor quality**.

## First principles emerge later

**Do not generate a `first-principles.md` while establishing an Anchor.**

First principles are broader lessons recognized **after** enough project work makes them apparent: repeated requirements, design trade-offs, architecture decisions, implementation outcomes, and real-use evidence. A candidate principle should be backed by more than a convenient early assumption. Record observations in their normal owning artifacts, then synthesize a separate first-principles document later if the recurring principle has lasting value.

Do not turn the synthesis into an unapproved new product constraint. When a proposed principle would restrict later work or alter accepted outcomes, seek the appropriate user decision.

## Boundary

- An Anchor defines product/change direction; Behavioral Requirements, Scenarios, and other specialist artifacts refine its meaning when useful.
- Neither this skill nor document formatting grants permission to implement, approve, or change user-owned intent.
- Different control planes may route or persist Anchors differently; their commands, states, and roles are not requirements of this skill.
