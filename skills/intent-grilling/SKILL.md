---
name: intent-grilling
description: Clarify materially ambiguous user product intent through focused, evidence-aware questions. Use before portable Anchor authoring when user-owned scope or success is unclear; not for routine technical decisions or mandatory interviews.
---

# Intent Grilling

Use when an idea or request has unresolved **user-owned** outcomes, trade-offs, or scope that would materially affect independent implementation. Do not interview by default when the intent is already clear.

The goal is enough understanding for `anchor-authoring`, not an exhaustive product specification.

## Method

1. Identify the highest-impact unresolved question about product intent, outcome, accepted risk, or scope.
2. Check existing documentation, code evidence, and permitted research before asking: do not ask the user to repeat what is already known.
3. Ask one consequential question at a time. When useful, recommend an answer and state one short reason and a meaningful alternative. Keep the question neutral.
4. Record the user's actual resolution separately from agent proposals and objective observations. Ambiguous replies are not approval of a stronger guarantee.
5. Challenge contradictions, weak assumptions, unintended scope expansion, and premature architecture.
6. Follow semantic dependencies as needed, but stop once the goal, observable success, scope, exclusions and reserved decisions are sufficiently clear.
7. Pass the resolved intent and any material open questions to `anchor-authoring` or the repository's existing accepted-intent document. The receiving agent must not need this conversation to recover the agreed meaning.

## Questions to avoid

Do not offload ordinary expert decisions (language, database, library, packages, task breakdown) to the user. Ask only when such a decision itself expresses an actual user preference or material risk trade-off.

## Boundary

This skill does not publish, accept, or authorize an Anchor, require any control-plane tool, dictate its path, or start execution. The consuming repository and `anchor-authoring` determine how the durable result is recorded and how genuine acceptance is evidenced.

Do not create `first-principles.md` during intent elicitation. Broad first principles may only emerge later from accumulated project evidence.
