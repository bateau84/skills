---
name: design-specification
description: Produce an implementation-ready human-experience handoff from accepted User Stories, Scenarios, experience goals, and specialist design work. Use before Architecture or implementation depends on human-facing design.
---

# Design Specification

Use when agreed human-facing design must be explicit enough for architecture, planning, implementation, review, and later validation without rediscovering material UX decisions. These are activities any agent may perform.

The specification is a **human-experience contract**, not backend architecture and not a pixel blueprint.

## Make the intended experience visible

Lead a substantial handoff with a short, plain-language walkthrough of one representative user task: what the person tries to do, what they see, what happens if it succeeds, and what an important failure or interruption looks like. Explain the key design choice and any scope limit without making the reader decode UX terms. The detailed flows, states and accessibility rules below remain authoritative; the walkthrough must agree with them and with the accepted product goal. It is not a new approval step.

## Method

1. **Ground the handoff.** Start from accepted product intent, relevant User Stories/Scenarios, existing experience language, and the specialist design work actually needed. State required capability/information dependencies explicitly. A dependency is not evidence of a gap: flag a missing capability only when current evidence establishes that it does not exist, rather than designing around mocks or inventing absence.
2. **State experience intent.** Preserve the human goal, context, and experience principles that explain why the design behaves as it does.
3. **Define information and flow.** Specify relevant information hierarchy/navigation and task flows: entry points, decision branches, success exits, abandonment, error/recovery paths, and preserved progress.
4. **Define views/regions by purpose.** Describe each meaningful view/region/component by the user job it serves, not just its contents or visual form.
5. **Make interaction semantics complete.** For every material action specify:
   ```text
   trigger -> observable response -> resulting state
   ```
   Include all materially possible branches. "Handle errors appropriately" is not a design.
6. **Cover applicable states.** Deliberately consider default, focus, disabled, loading, empty, validation/error, success, interrupted/stale, and domain-specific states. Do not require meaningless states by quota; do not leave reachable states for implementation to invent.
7. **Design recovery and continuity.** State what users retain or lose after error, cancel, back, retry, interruption, refresh/restart, or context change where those conditions are part of the accepted experience. Name re-entry points and truthful terminal states.
8. **Integrate input/focus/accessibility.** Specify keyboard/focus behavior, pointer/touch alternatives, dynamic announcements, destructive-action safeguards, reduced-motion alternatives, and concrete accessibility requirements where relevant. Accessibility may eliminate an otherwise attractive direction.
9. **Define surface/context adaptation.** Specify behavior when viewport, terminal size, input mode, device class, or interaction surface changes enough to affect task completion. Use native conventions for CLI/TUI/web/desktop rather than transplanting another surface's interaction model.
10. **Separate behavior from appearance.** Behavioral intent must remain implementable if visual examples/mockups are removed. Record visual semantics only where hierarchy, meaning, trust, or design language depends on them.
11. **Record consequential design decisions.** When meaningful alternatives existed, compare a small set of genuinely different directions against Stories/Scenarios, accessibility, existing design language, product capability, and constraints; record why the selected direction wins and what trade-off it accepts.
12. **Resolve ambiguity before handoff.** A consequential UX question is either resolved, explicitly tracked as a blocking open question, or safely left as an ordinary implementation detail. "TBD" is not a design decision.
13. **Run the implementation-without-UX-invention test.** A competent implementation team should be able to build the accepted journey without deciding material human semantics. If they would have to invent a state, response, recovery path, focus destination, or user-visible meaning, the design is incomplete.

## Durable handoff shape

Use only sections that apply; keep them proportional.

```markdown
## Experience context

## User Stories / Scenarios

## Information architecture

## User/task flows

## Views / regions / components

## States and interactions

## Failure / recovery / interruption

## Focus / input / accessibility

## Responsive / surface constraints

## Visual semantics

## Design decisions

## Open questions
```

Keep durable stories, scenarios and experience design discoverable in the repository's documented structure. Do not prescribe an Anchor-rooted layout; use the consuming repository's policy and applicable OKF authoring rules.

## Boundary

Do not choose backend protocols, persistence, topology, or schema merely because the design needs a capability. State the capability/experience dependency, then address structural realization through architecture work rather than hiding it in a UX decision.

Do not duplicate complete requirement, quality-scenario, or shared-contract semantics. Reconcile with behavioral specification where human-visible meaning overlaps.
