---
name: code-analysis
description: "Evidence-backed investigation of existing source code. Use when explaining unfamiliar code, tracing execution or data flow, locating behavior, checking a suspected defect, or assessing change impact across callers and dependencies. Not a replacement for a PR review verdict, a security audit, measured performance analysis (use performance), or implementation (use software-engineering)."
---

# Code Analysis

Answer a bounded question about what the code actually does. A useful result is an evidence-backed explanation, impact map, or defect finding; discovering a bug is not required. Analysis alone does not authorize repairs, refactoring, dependency installation, or changes to live systems.

## Establish the question and source

- State the question, relevant behavior, scope, and stopping point. Reuse supplied context; ask only when a missing fact materially changes the answer. A small explanation should remain small.
- Identify the inspected revision or supplied excerpt, relevant local edits, entry points, runtime/toolchain, and configuration. Do not combine different revisions into one claimed execution path.
- Separate implemented behavior from intended behavior. Use accepted requirements, contracts, and tests as evidence of intent, while checking whether tests exercise that contract. Comments and names are leads, not proof. Describe a contract ambiguity rather than silently deciding it.

## Trace the smallest complete path

Start at the actual entry point or affected symbol. Follow the relevant callers, dispatch or registration, transformations, state ownership, dependencies, and externally visible outcome. Read enough surrounding code to explain preconditions, return values, errors, and side effects.

When the question involves state or lifetime, follow creation, use, failure, cancellation, cleanup, and shutdown as applicable. Check alternate callers or configurations that could invalidate the conclusion. Do not expand an ordinary question into a whole-repository audit.

For change impact, distinguish observed direct consumers, plausible indirect effects, and unknown consumers. Follow serialized messages, generated interfaces, configuration, callbacks, plugin registration, and foreign-language boundaries when they are on the path; a symbol graph alone may not connect them. Identify the source of generated code before proposing changes.

## Use structural tools without trusting them blindly

When available, use code-intelligence tools for definitions, references, callers, dependency edges, and impact queries. Check their workspace/revision, language coverage, freshness, and truncation or degradation signals before relying on them. Confirm decisive edges against the current source.

No particular MCP server or query name is required. If an index is unavailable, stale, incomplete, or unsupported, use bounded text search and direct file reads, then follow imports, registrations, configuration, and call sites manually. Separate resolved edges from inferred ones. An empty reference result or search miss is not proof that code is unused, unreachable, or safe to remove. Do not repair an index or install a tool without the needed authority.

## Test the explanation, not just the suspicion

For a suspected problem, build the causal chain:

```text
reachable input/state -> relevant branch or interleaving -> observed consequence
```

Identify the violated contract or concrete consequence and look for a caller guarantee, guard, cleanup owner, or alternative explanation that would disprove the finding. Complexity, naming, or stylistic preference alone is not a defect.

Use the smallest decisive evidence available: source reasoning, a focused test, a reproduction, or an observed trace. Static reasoning can establish a defect when its preconditions and consequence are demonstrable; label it as static evidence, not a runtime reproduction. A suspicious pattern without those facts remains a hypothesis with a specific next check.

For timing, resource use, or throughput claims, distinguish a plausible mechanism from a measured bottleneck. Use `performance` for measurement methodology rather than claiming that code shape proves production cost.

## Verify within the permitted environment

Read the repository's toolchain and check commands before choosing verification. Use the relevant language reference below only when it affects the question. Verify consequential version-specific behavior against the repository's pinned versions and official documentation; do not upgrade the project to make a check convenient.

Tests, imports, builds, analyzers, and package scripts can execute repository code, run hooks, access credentials or networks, and alter state. Inspect the relevant setup and respect host permissions; prefer bounded checks in a disposable environment when appropriate. Do not assume that a command called "check" is read-only. Do not install tools, run migrations, contact production, or apply fixes merely to complete an analysis.

Record what actually ran, its relevant configuration, result, and limits. When execution is unavailable or unsafe, continue with source evidence and identify the missing check. Passing compilation, lint, or tests only supports the properties and paths those checks cover.

## Return a proportionate result

Lead with the answer. Include only the detail needed to make it checkable:

- **Explanation or impact:** the relevant path and boundaries, with file/symbol locations and line ranges where available.
- **Confirmed findings, when present:** trigger, consequence, evidence, and severity based on actual impact. Distinguish runtime reproduction from static proof. Suggest a bounded correction without applying it unless asked.
- **Uncertainty and coverage:** hypotheses with the evidence needed to resolve them, inspected scope/revision, checks actually run, and material gaps.

Do not manufacture a findings table for correct code, rank unsupported suspicions as confirmed defects, or claim repository-wide safety from a scoped investigation. Stop when the question is answered to the supported confidence level or the remaining evidence is explicitly unavailable.

## Language depth and adjacent work

Load only references relevant to the path; mixed-language paths may need more than one.

| Surface | Direct reference | Existing depth to compose when needed |
| --- | --- | --- |
| Go | [Go](references/go.md) | `golang-how-to` and the relevant Go specialist |
| Python | [Python](references/python.md) | `python-how-to` and the relevant Python specialist |
| TypeScript | [TypeScript](references/typescript.md) | `typescript-type-safety`, `typescript-async` |
| JavaScript runtime | [JavaScript](references/javascript.md) | `javascript-runtime`; `browser-runtime` for browser APIs |
| Rust | [Rust](references/rust.md) | Repository conventions and official toolchain/library documentation |

These references select investigation questions, not five copies of this workflow. Other languages remain usable through the core method and their actual language/runtime documentation. Sibling skills are optional depth where available, not hidden prerequisites.

A PR review can use these traces as evidence but still needs change-specific regression assessment. Security investigation needs the applicable security guidance; performance work needs measurements; implementation uses `software-engineering` and relevant testing skills. This skill does not decide merge readiness or product acceptance.
