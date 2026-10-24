# Cross-component work handoffs

Use this **optional specialization** of `work-handoff` when one component, repository, service, or fresh session needs behavior supplied by another. It preserves the existing `feature-handoff` technique without making its extra interface detail mandatory for ordinary bugs or enhancements.

## Explain the handoff before the interface details

Open with ordinary words describing **what the first component needs**, **what the receiving component should provide**, and **what the user or caller will notice**. A concrete example is often clearer than a list of internal names. Keep source and target names, required-versus-suggested status, exact fields, exceptions and acceptance conditions visible afterward; the easy explanation must not replace or contradict them.

If using the YAML variant below, make the `objective`, `need`, requirement text and acceptance text understandable to a person reading it directly. Keep the legacy machine-readable shape when a consumer needs it; do not silently change its schema in the name of readability.

## Contract boundary

Identify the **source** need and the **target** responsibility. State what must hold **across that seam**, not which internal files or design pattern the receiver should choose. The source's current implementation is not by itself authority to demand one architecture.

Use deliberate normative levels:

- **MUST:** essential for the established consumer requirement.
- **SHOULD:** expected unless the receiver has a supported reason not to.
- **MAY:** optional.

Keep a stable ID for each distinct normative promise when useful. Define acceptance with externally observable conditions. Interfaces (endpoint, schema, command, event, payload) must be marked **required**, **suggested**, or **example**; the existence of a plausible example does not make it a requirement.

If resolving the handoff would decide correctness-sensitive product semantics, identify the decision owner and refer to accepted `behavioral-spec` or other governing artifacts. A handoff is not a substitute for a durable authoritative contract when one is required.

## Structured variant

The parent skill's compact Markdown form is sufficient for most cases. When an interface-heavy cross-component contract benefits from a portable machine-readable representation, use a structure like:

~~~yaml
kind: work-handoff
version: 1
work_type: cross-component-dependency
title: <short title>

source:
  component: <source component or responsibility>
  need: <why the consumer needs the dependency>

target:
  component: <receiving component or responsibility>

objective: <outcome the dependency enables>

context:
  current_behavior:
    - <observed limitation or existing behavior>

requested_behavior:
  - <external observable outcome>

requirements:
  - id: REQ-001
    level: MUST
    text: <one falsifiable requirement>

acceptance:
  - id: AC-001
    given: <starting condition>
    when: <trigger>
    then: <observable result>

constraints:
  - <accepted constraint, if any>

non_goals:
  - <explicit exclusion, if any>

interface:
  status: suggested # required | suggested | example
  description: <contract or proposal>

open_questions:
  - <unresolved owner decision, if any>

evidence:
  - <accessible durable source or observation>
~~~

Omit unneeded optional sections. If an existing consumer explicitly depends on the **original** `feature-handoff` v1 YAML shape and `kind: feature-handoff`, preserve that shape for the handoff rather than silently breaking its consumer. That compatibility case does **not** require retaining a second skill.

## Example: registered agent discovery

The frontend needs a backend-supported way to discover currently registered agents.

- Source: an agent-selection frontend must display available agents and their names.
- Target: backend agent discovery responsibility.
- Required: expose registered agents and the name of each one.
- Conditional: return role/responsibility metadata when available; agents without such metadata remain discoverable.
- Suggested, **not required**: `GET /agents` returning normalized agent descriptions.
- Acceptance: the source can list an existing agent by name, including one without role metadata.
- Open decision: whether arbitrary frontmatter fields are exposed or only known normalized fields.

Do not copy this endpoint or metadata policy into unrelated requests. The point is to retain a consumer-level contract while leaving internal design choices open.
