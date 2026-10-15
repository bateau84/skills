---
name: user-stories-and-scenarios
description: Capture small human-centered User Stories and concrete end-to-end design Scenarios (including a meaningful failure, interruption, or edge condition) from agreed product intent. Use for durable US/SC design artifacts. Not for system requirements or measurable quality scenarios (use behavioral-spec), or implementation design.
---

# User Stories and Scenarios

Two small, implementation-independent design artifacts. A **User Story** states who is trying to achieve what, in what context, and how they know they succeeded. A **Scenario** exercises that intent in a concrete situation, including what happens when it goes wrong. Write a story first when the human goal itself needs to be pinned down; add scenarios when journeys, branches, interruptions, or failures need to be evaluated.

## User Story

Use when a human-facing capability or change needs a durable statement of **who is trying to achieve what, in what context, and how they know they succeeded**.

A User Story is design authority about human intent. It is not a Behavioral Requirement, architecture, task, or UI component specification.

### Method

1. Identify the closest accepted product/user authority for the human need.
2. Name the actor by meaningful role/context, not a generic "user" when the context changes design decisions.
3. State the trigger or situation that creates the need.
4. State the human goal/outcome, not the feature or interface mechanism.
5. State observable success from the person's perspective.
6. Keep the story implementation-independent. Do not prescribe screens, APIs, storage, components, or technical workflow.
7. Keep one coherent human goal per story. Split stories when actors, goals, or success conditions materially differ.
8. Do not use a Story to create product capability absent from accepted authority. Surface the gap instead.
9. Use Scenarios for concrete end-to-end situations, branches, interruptions, or failures that exercise the story.

### Durable artifact

Use the consuming repository's OKF relationship vocabulary and heading rules when publishing the document. The example `## Derived from` heading is illustrative; relationship type and path are repository-owned.

Store the story in the location and naming convention established by the consuming repository. For example, repositories using numbered stories may choose `us-NNN-<descriptive-slug>.md`; this skill does not impose an Anchor-rooted path.

```markdown
# US-NNN — <descriptive title>

**Actor / context:**
<who, and context that materially affects the need>

**Trigger:**
<what situation causes the need>

**Goal:**
<what the person needs to accomplish or understand>

**Observable success:**
<what the person can observe/know when the goal is achieved>

## Derived from
- <closest accepted product/user authority>
```

Prefer this explicit form over ceremonial "As a / I want / so that" prose when the latter hides context or success semantics.

## Design Scenario

Use when design needs a concrete situation against which journeys, interaction states, recovery, and later Product Acceptance can be evaluated.

A Design Scenario is **human-centered**. It is distinct from a system Quality Scenario: SC describes a person's situation and journey; QS describes a measurable system quality under a stimulus/environment.

### Method

1. Trace the scenario to an accepted User Story/product need or other accepted human-facing authority.
2. Make the context concrete enough to affect design: actor, environment/device/work setting, prior knowledge, urgency/interruption, or other relevant conditions.
3. State the person's goal before describing interface steps.
4. Describe the meaningful task/journey sequence at human-visible level. Do not prescribe backend/system flow.
5. Include at least one realistic failure, interruption, mistaken action, missing information, degraded response, or edge condition when it could materially change the experience. A happy-path-only scenario rarely exposes enough design.
6. State the observable outcome: what the person sees/knows/can do at success, recovery, abandonment, or terminal failure.
7. Mark consequential assumptions instead of presenting guessed user knowledge/context as fact.
8. Keep the scenario implementation-independent enough that several interface realizations could satisfy it.
9. Reuse accepted Scenarios as design-validation and Product Acceptance inputs; do not rewrite them merely to match implementation.

### Durable artifact

Use the consuming repository's OKF relationship vocabulary and heading rules when publishing the document. The example `## Derived from` heading is illustrative; relationship type and path are repository-owned.

Use the consuming repository's document path and naming rules. A numbered scenario may use `sc-NNN-<descriptive-slug>.md`; no Anchor-rooted layout is required by this skill.

```markdown
# SC-NNN — <descriptive title>

**Context:**
<actor + concrete situation/constraints>

**Goal:**
<what the person needs to achieve>

**Scenario:**
<human-visible sequence/situation>

**Failure / edge condition:**
<meaningful failure, interruption, mistake, degraded state, or boundary case>

**Observable outcome:**
<what success/recovery/failure looks like to the person>

## Derived from
- <US and/or closest accepted human-facing authority>
```
