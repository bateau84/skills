---
name: behavioral-spec
description: Derive bounded, implementation-independent requirements from agreed product intent through goal refinement, coverage lenses, obstacle analysis, provenance tracking, and counterexample checks. Use to select, author, and reconcile Behavioral Requirements (BR), Quality Scenarios (QS), and Obligation Contracts (OC) without expanding scope. Not for concrete API/schema/protocol realization (use architectural-spec) or human-centered stories and scenarios (use user-stories-and-scenarios).
---

# Behavioral Specification

Use this skill for substantive behavioral specification. It provides common reasoning for behavioral requirements, quality scenarios, and shared semantic contracts.

**Expand the consequences of the anchor, not the scope of the product.** Use lightweight goal refinement and obstacle analysis to produce the smallest coherent set of observable obligations. Thoroughness means covering material meaning, not maximizing artifact count or claiming to exhaust every imaginable case.

## Boundary

Own **what must be observably or semantically true**, not structural realization. Do not choose components, schemas, protocols, storage, libraries, deployment topology, or implementation mechanisms unless accepted external/product authority itself fixes them.

An agent writing specifications may resolve ordinary semantic detail within the agreed task. It may not silently create a new capability, scope, material guarantee, risk acceptance, or user-reserved preference. This method adds no roles, approval stages, or mandatory modeling notation. An "anchor" here means the project's agreed product intent or brief, not a required artifact system.

## Make the intended behavior easy to check

For substantial requirements, start the bundle index or existing overview with a brief explanation in everyday language: what the user wants to accomplish, what success looks like, one useful example (including an important failure when relevant), and what is deliberately outside scope. This lets the user check the interpretation before technical wording spreads into design and architecture. It is an explanation of the accepted requirements, **not a second source of requirements**. If the explanation and precise clauses disagree, resolve the mismatch; don't bury it in jargon or silently invent a stronger promise. Ordinary specification choices remain with the author, not a new user sign-off.

## Common method

### 1. Establish the accepted meaning

Read the accepted anchor and applicable accepted obligations. Extract actors, capabilities, outcomes, constraints, exclusions, and meaning-bearing terms before drafting requirements. Existing accepted obligations remain binding unless their owning authority supersedes them; surface conflicts rather than choosing whichever source is convenient.

Where the anchor uses these headings, interpret them by semantic role; other anchor formats are equally valid:

| Anchor element  | Extract                                                                             |
| --------------- | ----------------------------------------------------------------------------------- |
| Picture         | Actors, objects, capabilities, and the intended situation.                          |
| Done            | Observable outcomes that distinguish fulfillment from activity.                     |
| Minimal version | The accepted capability boundary, not permission for incoherent behavior within it. |
| Not this        | Scope exclusions, distinguished from actual prohibitions.                           |
| Forces          | Binding constraints, preferences, and tensions, preserving their strength.          |

Preserve source modality. A suggestion, example, preference, possibility, or exploration prompt does not become a mandatory guarantee merely because it appears in accepted context. An excluded capability is not automatically forbidden. Resolve consequential meanings of words such as _shared_, _automatic_, _available_, _cancelled_, and _complete_: could two implementers interpret them differently and produce observably different outcomes?

For each candidate normative claim distinguish:

- **sourced** — explicitly fixed by accepted authority;
- **derived** — a necessary consequence of it;
- **specified** — an ordinary semantic choice the specification author may settle inside the agreed scope;
- **open** — materially changes capability, scope, risk, guarantee, or reserved preference and needs owning authority.

These are reasoning states, not mandatory document fields. A reasonable choice is not necessarily a logical consequence. Settle routine detail within delegated authority and explain the choice; do not escalate every ambiguity or disguise a preference as necessity.

### 2. Refine commitments by necessity

For each commitment ask: **what must be true for this to hold?** Follow consequential dependencies until the resulting behavior has clear conditions and a real verification path.

- Separate conditions that must **all** hold from **alternative ways** to satisfy a condition. Do not turn one convenient alternative into a derived obligation.
- Explain each consequential derivation: **without this obligation, which accepted commitment could fail, and how?** A source link alone does not demonstrate necessity.
- Keep the source-to-obligation relationship visible enough to check coverage and revisit affected obligations when authority changes. Reuse existing navigation and artifact relationships where available; do not create a second normative ledger.
- Identify who must perform or preserve each observable obligation, and which other parties rely on it, without selecting implementation components.

### 3. Sweep applicable behavior

Use these lenses as discovery questions, not as a template that demands a requirement in every row:

| Lens                     | Questions                                                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Actors and authority     | Who may initiate, observe, change, approve, or stop behavior? What may each party rely on?                                                         |
| Inputs and boundaries    | What happens with missing, invalid, duplicate, conflicting, stale, empty, or extreme inputs?                                                       |
| State and lifecycle      | What is true before, during, and after the behavior? Which transitions and terminal outcomes are allowed or forbidden?                             |
| Time and ordering        | What takes precedence? What happens when events overlap, arrive late, or occur in a different order?                                               |
| Failure and recovery     | What happens on interruption, cancellation, timeout, partial success, dependency failure, retry, or restart?                                       |
| Information and evidence | What must remain identifiable, preserved, attributable, or observable? Can attempted work be mistaken for actual success?                          |
| Shared boundaries        | Where must independently realized parties agree on identity, ownership, status, completion, or responsibility?                                     |
| Quality and preservation | Under which conditions must behavior remain useful and correct? What accepted compatibility, security, or existing behavior must remain unchanged? |

Investigate a case when it could alter an accepted outcome, violate a constraint, or expose an unresolved responsibility. Include consequential combinations, especially concurrency and destructive effects; avoid a full Cartesian enumeration of irrelevant cases. A lens does not authorize new capabilities, numerical quality targets, automatic recovery, or new security mechanisms. Note consequential exclusions or assumptions with their basis instead of silently omitting them.

### 4. Analyze obstacles, invariants, and progress

For each promise ask: **how could this become false?** Describe plausible in-scope events or sequences, including failures at shared boundaries, rather than only ideal operation.

For each material obstacle, identify the existing obligation that handles it, derive a necessary obligation, settle a delegated semantic choice, or raise the exact authority gap. An obstacle is a discovery result, not automatic authority to add a feature.

Distinguish:

- **Invariants:** what must remain true throughout the applicable states and transitions, including failure and recovery?
- **Progress obligations:** what must remain possible or eventually happen, under which accepted conditions and dependencies?

Check both. A system that never starts useful work can satisfy a non-overlap rule while defeating the accepted capability. Conversely, an accepted safety guarantee does not establish unconditional eventual success, automatic retries, or a deadline.

Expose assumptions about the environment, other actors, and dependencies. Establish their source and scope; an unaccepted assumption is not a fact. Do not assume away an accepted failure case, transfer a system obligation to an unspecified actor, or weaken a guarantee just to make the contract appear complete.

### 5. Reconcile without importing downstream authority

First derive obligation meaning from agreed product intent. Then compare it with design, architecture, tests, code, and implementation evidence. Downstream material may expose a gap, conflict, missing case, or feasibility concern; it does not silently become upstream product truth. Feed newly discovered cases back through the same provenance and derivation checks.

User stories and human-centered scenarios may constrain observable experience. Requirements, quality scenarios, shared contracts, and design must agree before architecture depends on them; disagreements are gaps to resolve rather than permission to silently overwrite another agreed decision.

Check architecture leakage: could materially different architectures satisfy an obligation while preserving the same meaning? If not, verify that the structural constraint is itself agreed; otherwise rewrite the obligation or address the structural choice in architecture work.

### 6. Write the smallest falsifiable contract

Make each normative claim precise about its applicable conditions, actor, required outcome or invariant, and consequential ordering or exceptions. State a concrete observation that would falsify it. Avoid vague qualities, hidden defaults, ambiguous quantifiers, and claims that pass only because their triggering state is unreachable or evidence is suppressed.

Event/state sentence patterns can help express meaning, for example: **while [state], when [event], [actor] shall [observable response].** Use them where useful, not as a substitute for discovery or as a mandatory syntax.

Choose the artifact whose semantic role is primary:

- **Behavioral Requirement:** one normative observable behavior.
- **Quality Scenario:** a quality must hold measurably under a meaningful condition/stimulus. Make the QS normative when the obligation exists specifically under a condition, load, degradation, threat, or recovery situation. Add a BR only for a distinct baseline behavior meaningful independently of that scenario.
- **Obligation Contract:** independently realized parties must share semantic agreement at a correctness-sensitive seam. Make the OC normative for that shared meaning. Add a BR only for a distinct system-level outcome outside the seam contract.

Give each guarantee one normative home. Cross-reference related artifacts instead of making BR/QS/OC copies for symmetry or completeness. State what must be observed to prove or falsify the obligation, not implementation-specific test mechanics unless the verification surface is itself authoritative. Keep its basis, applicability, dependencies, and verification intent clear within the existing artifact formats.

### 7. Challenge the set in both directions

Before handoff, apply three bounded counterexample checks:

- **Omission:** could a plausible system satisfy every written obligation yet violate an accepted anchor commitment? Add missing meaning or expose the unresolved gap.
- **Invention:** could a system satisfy the accepted authority while violating a supposedly derived obligation? It is not necessary as claimed; establish it as a legitimate specified choice, route a material decision to its owner, or remove it.
- **Composition:** can all applicable obligations hold together in the same execution? Check consequential intersections such as cancellation during completion, retry after partial success, or authority changing during execution.

These are practitioner self-checks, not an assertion of independent review or a new approval gate. Correct the affected meaning and repeat the affected checks; do not restart unrelated specification work.

### 8. Stop at bounded coverage

A handoff is ready only for the scope whose accepted meaning is sufficiently settled for downstream realization:

- Every material commitment in that scope has obligation coverage; unresolved gaps are identified with their owning authority and affected dependencies, not counted as satisfied coverage.
- Every normative obligation has a legitimate basis and a real falsification criterion. Relevant lenses, obstacles, invariants, progress conditions, and interactions have been considered at a depth proportionate to their consequences.
- No known in-scope counterexample or unresolved conflict defeats the claimed coverage. Assumptions and remaining uncertainty are visible, not presented as proof of exhaustive completeness.

Continue and hand off independent, unaffected specification while an authority question is open. Do not declare the dependent portion or whole assignment complete just because its gap has been recorded. Summarize the ready scope, consequential choices, coverage limits, and blockers using the project's existing notes or handoff surface, not a new required artifact. A fresh counterexample or changed anchor reopens affected coverage, not the entire process by default.

## Worked example

Illustration only, not a requirement for every project: **two sessions may execute a shared workflow, but must never execute the same logical task concurrently.**

A per-session non-overlap rule misses the cross-session promise. Denying every start meets non-overlap but defeats the execution capability. A shared SQLite database is one possible realization, not a necessary consequence. Lost contact does not prove execution stopped or authorize an automatic retry; applicable failure assumptions and any recovery promise need their own basis. The useful contract identifies task identity, the scope of non-overlap, and conditions for useful execution without silently choosing a storage or coordination mechanism.

## Durable bundle

Keep related obligations and their source relationships discoverable using the project's conventions. If a new file-based bundle is useful, this is one possible layout, not a required namespace:

```text
docs/requirements/<anchor-slug>/
  index.md
  requirements/
    br-NNN-<descriptive-slug>.md
  quality-scenarios/
    qs-NNN-<descriptive-slug>.md
  obligation-contracts/
    oc-NNN-<descriptive-slug>.md
```

In this layout, use separate BR/QS/OC numbering. The bundle index is navigation and relationship context, not a replacement for the artifacts. Other identifiers and layouts are valid when relationships remain clear.

Existing flat BR/OC bundles remain valid until an intentional migration updates them and their references; do not move artifacts merely to match this example.

Read the artifact reference before authoring each artifact type:

- [Behavioral Requirement](references/behavioral-requirement.md)
- [Quality Scenario](references/quality-scenario.md)
- [Obligation Contract](references/obligation-contract.md)
