# Portable agent skills

This repository provides **methodology**, independent of any agent harness, control plane, agent role or execution workflow. The consuming repository defines its own authority, file layout, permissions, and task orchestration.

**Migration note:** This library was seeded from Loom and MATS. Some older skills still carry role names, product-specific paths or control-plane assumptions. They are legacy material to audit and migrate, not a license to impose those assumptions on new consumers. The skills touched by this change use repository-owned paths and coordination.

## Skill components

| File | Purpose | Required? |
| --- | --- | --- |
| `SKILL.md` | How to perform the specialized work | Yes |
| `ASSESSMENT.md` | Independent, normal review of the result against accepted inputs | No |
| `QA.md` | Independent adversarial checks for residual false confidence | No |

Assessment and QA are distinct perspectives, not mandatory ceremonies or requirements for dedicated agent roles. Consumers may assign them to any capable independent agent.

## Selection and authority

- Load the **smallest relevant skill set** for the task; use additional skills only when their distinct concerns matter.
- Skills do not create product requirements, accept decisions for the user, grant tool permissions, or dictate workflow gates.
- Prefer current repository authority and observed implementation over unsupported assumptions in examples or older instructions.
- Leave repository-specific paths, IDs, document types, graph vocabulary, and mandatory updates to the consuming repository's `AGENTS.md` or equivalent policy.
- Knowledge format, indexing, logging, graph mechanics, and their structural validation belong to the portable `okf-authoring` skill maintained in [nrkno/okf-mcp](https://github.com/nrkno/okf-mcp). Domain-specific skills decide substantive content.

## Documentation authoring

The documentation skills are independently selectable:

| Concern | Skill |
| --- | --- |
| Preserve agreed user intent in a durable Anchor | `anchor-authoring` |
| Explore ambiguous user-owned product intent | `intent-grilling` |
| User Story and human-facing Scenario | `user-story`, `design-scenario` |
| Human-experience specification | `design-specification` |
| Functional requirement | `behavioral-requirement` |
| Shared semantic guarantees | `obligation-contract` |
| Measurable quality condition | `quality-scenario` |
| Architectural design, decision, specification | `architectural-design`, `architectural-decision`, `architectural-spec` |
| Current implementation and publication documentation | `documentation` |
| Task decomposition and cross-session handoff | `work-decomposition`, `feature-handoff` |

For material parallel work, first establish shared **outcomes and contracts**, then give agents bounded responsibility and verification expectations. A downstream handoff must make sense without the original conversation. The number of document types and review steps scales with real ambiguity and risk, not a fixed pipeline.

**First principles are not an Anchor deliverable.** They may be synthesized later from repeated, evidenced product and engineering decisions, when they become apparent and useful.

Other language, framework, design, testing, and operational skills in this repository remain optional domain methods. See [PORTING.md](PORTING.md) for historical import decisions; it is not a present-day control-plane contract.
