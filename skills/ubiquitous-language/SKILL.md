---
name: ubiquitous-language
description: Establish and maintain a shared domain vocabulary across people, agents, requirements, code, APIs, and documentation. Use when domain terms are ambiguous, synonyms drift, one word has several meanings, names conflict across artifacts, a bounded context needs a glossary, or a change introduces or renames a business concept. Not for language-specific identifier style (use the relevant language naming skill), ordinary copyediting (use documentation), or deciding product behavior (use behavioral-spec).
---

# Ubiquitous Language

A shared language makes domain meaning explicit and consistent **within a defined context**. The vocabulary is a record of agreements, not a substitute for discovering or agreeing what the system should do.

## Working principles

- **Meaning before naming.** Explain a concept by what it is, does, and excludes before proposing its name. A definition must distinguish it from nearby concepts.
- **Context before consistency.** Different bounded contexts may correctly use the same word differently. Do not force a global dictionary or rename unrelated concepts to match.
- **Evidence before authority.** Separate stakeholder intent, accepted requirements/decisions, current code/API behavior, and informal usage. Current implementation is evidence of usage, not automatic proof of intended meaning.
- **Agreement before canonization.** Label unconfirmed terms `proposed` or `unresolved`; do not declare them accepted or silently resolve disagreements on behalf of stakeholders.
- **Precision without ceremony.** Record only terms that affect decisions, boundaries, user understanding, contracts, or recurring confusion. Small questions may need only a short clarification.
- **Changes are not just words.** Renaming public APIs, database fields, events, logs, or persisted documents may be a compatibility change. Do not perform a rename unless it is in scope and its impact is accounted for.

## Method

1. **Identify the context and existing vocabulary.** Name the bounded context, affected audience, and why a shared meaning is needed. Search repository instructions, indexes, and affected documents for its existing vocabulary, including definitions embedded in other documents. Reuse that home; do not create a competing dictionary or assume similarly named records govern the same context. If a word crosses contexts, identify the boundary explicitly.
2. **Collect actual usage.** Look at relevant stakeholder language, domain examples, accepted product artifacts, code and interfaces, and documentation. Record where claims come from and whether they describe intent or observed behavior. Do not assume one artifact overrides another without a known authority rule.
3. **Find semantic collisions.** Look for:
   - different words for one concept (synonyms);
   - one word for different concepts (overloading);
   - definitions that disagree about lifecycle, ownership, invariants, or outcomes;
   - misleading technical names used as business terms;
   - translated labels that imply a different meaning.
4. **Clarify the distinction.** For every consequential collision, ask what observable example distinguishes the meanings. Propose candidate terms only after the distinction is clear. If the product meaning is unsettled, preserve the question and route it to the appropriate decision owner; do not settle it by editing a glossary.
5. **Record an appropriately small vocabulary.** When writing is in scope, update the existing vocabulary. If none exists and consequential terms recur across affected artifacts, create a small, durable vocabulary in the repository's established documentation structure. Link affected documents to it rather than duplicating definitions. Agreement is needed before accepting a meaning, not before recording it: preserve proposed and unresolved entries too. For each important term, record its context, definition, nearby exclusions, example, source, and acceptance status. Include aliases/deprecated terms only when they exist and matter. Record relationships between terms when that avoids ambiguity.
6. **Apply within authorized scope.** Reuse accepted terms in new requirements, design notes, UI copy, code, APIs, tests, and agent handoffs as applicable. Report inconsistencies in out-of-scope or externally owned artifacts; do not quietly make bulk renames or alter behavioral contracts.
7. **Check the result.** Verify that a reader can distinguish neighboring terms using examples, the same term means the same thing inside the context, different concepts are not accidentally merged, and unresolved conflicts remain visible rather than becoming false agreements.

## Findings and handoffs

For each material unresolved collision, preserve the conflicting source locations, a distinguishing example, its consequence, and the decision needed. Name the responsible owner when known; otherwise keep ownership unknown. Link the vocabulary entry and the project's existing finding or work record when available. Use accessible artifacts or include the essential evidence in the handoff so the next reader does not need the original conversation.

Before reporting completion, distinguish verified corrections, unresolved decisions, and remaining out-of-scope work. Carry their sources and acceptance status into handoffs; recording or forwarding a finding does not resolve it. A bounded audit may be complete while its findings remain open. Do not claim affected documents or consumers are aligned unless they were checked.

## Suggested record (adapt to the repository)

Keep the vocabulary near the domain material it governs (for example, `docs/domain/<context>/vocabulary.md`). There is no required file path, tool, format, or central registry.

```markdown
### <Term> — <accepted | proposed | unresolved>
- Context: <where the term applies>
- Meaning: <observable, distinguishing definition>
- Not: <nearest misleading alternative or exclusion>
- Example: <one representative use>
- Related terms / aliases: <only if useful>
- Basis: <decision, stakeholder statement, or observed artifact>
- Open question: <only if unresolved>
```

A single clarified term may suffice for an isolated ambiguity; trivial naming or copyediting needs no glossary. Recurring consequential terms warrant the reuse or creation described above. For review-only work, report discrepancies and the proposed vocabulary location or edits without writing files. Prefer the smallest result that fixes the actual ambiguity.

## Example: unresolved lifecycle vocabulary

Suppose one specification calls a workflow `completed` when execution stops, while another uses `completed` only when its goal is achieved.

- Identify the two observable meanings: *execution ended* versus *goal satisfied*.
- Show a counterexample: execution can end with the goal unmet.
- Mark the collision unresolved; do not make either definition canonical without an accepted decision.
- Once resolved, align the glossary and in-scope artifacts. Treat changed API/state semantics as a behavior change, not a terminology cleanup.

## Boundaries with neighboring skills

- **behavioral-spec / anchor-authoring:** establish product meaning and accepted behavior; this skill makes agreed terminology clear and traces unresolved semantic questions.
- **architectural-design / architectural-spec:** define component and interface realization; this skill checks the terms used but does not choose an architecture.
- **documentation:** communicates implemented behavior; this skill establishes or checks shared domain vocabulary without replacing documentation work.
- **language naming skills:** handle idiomatic identifier syntax; this skill addresses domain meaning regardless of implementation language.
- **information-architecture:** organizes concepts for discovery and navigation; this skill establishes distinctions between concepts.
