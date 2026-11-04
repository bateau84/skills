---
name: code-analysis
description: "Evidence-backed investigation of existing source code and engineering quality. Use when explaining unfamiliar code, tracing execution or data flow, locating behavior, checking a suspected defect, assessing change impact, checking methods or practices, evaluating test adequacy and usefulness, examining modularity/reuse/deep modules, or identifying justified refactoring opportunities. Not a replacement for a PR review verdict, a security audit, measured performance analysis (use performance), or implementation (use software-engineering)."
---

# Code Analysis

Answer a bounded question about what the code does and, when requested, how well its engineering choices serve its actual needs. A useful result is an evidence-backed explanation, impact map, quality assessment, or improvement candidate; discovering a bug or recommending changes is not required. Analysis alone does not authorize repairs, refactoring, new tests, dependency installation, or changes to live systems.

## Establish the question and source

- State the question, relevant behavior, scope, and stopping point. Reuse supplied context; ask only when a missing fact materially changes the answer. A small explanation should remain small. For a quality analysis, cover the requested practices, tests, modularity, reuse, and improvement opportunities, or explain what could not be assessed.
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

## Assess methods and practices in context

For quality work, identify the requested methods, accepted repository rules, and relevant observed conventions. Separate a binding rule from a convention or optional design heuristic. Determine each practice's purpose and applicable scope before judging its presence or consistency; do not impose a catalog of patterns on every codebase.

Trace representative implementations and counterexamples, not just names or imports. Report observed, inconsistent, absent within the inspected scope, not applicable with a reason, or unknown. Cite locations and explain the effect on correctness or maintenance. When counting adoption, state what qualified for the denominator, what was sampled, and what remains uninspected; a sample is not a repository-wide percentage.

Presence is not effectiveness: an interface may not decouple anything, and a named pattern may add cost without solving the local problem. Conversely, a simpler implementation may meet the same need. Do not infer historical practices such as test-first development from a final source/test snapshot; use trustworthy process evidence or leave that claim unknown.

## Assess whether tests protect real behavior

Build a small map for the relevant contracts and credible failure modes:

```text
accepted behavior/risk -> production path -> existing test and assertion -> wrong behavior it would detect
```

Read tests, fixtures, doubles, and setup, plus relevant discovery configuration, skip conditions, and CI selection. Distinguish a test existing, being selected, being executed, and proving the claim. Inspect unit, integration, contract, or acceptance coverage where the behavior actually crosses those boundaries; do not demand every test level for every behavior.

A useful test discriminates correct behavior from a plausible wrong implementation. Identify whether it asserts an outcome produced by the code, a required interaction, or only something the fixture itself supplied. Flag ceremonial or weak-for-the-claim tests with a concrete explanation: the target was mocked away, the expected value was planted, the assertion is tautological, the meaningful failure is swallowed, or the check never runs. Do not label all mocks, snapshots, smoke tests, or interaction assertions ceremonial; judge the actual obligation they protect and the test's stated level.

Before reporting a missing test, trace the accepted behavior or source-backed risk and search for equivalent protection elsewhere in the relevant suite and configuration. Name the inspected scope, the reachable failure, and the observation that should distinguish success from failure. Prefer strengthening an existing test when sufficient. If the inventory or behavior contract is incomplete, say coverage is unverified, not absent. Do not invent unsupported requirements, imaginary edge cases, test results, or a quota of additional tests. An adequate result with no justified additions is valid.

Coverage and test counts are supporting signals, not proof of meaningful assertions. A bounded mutation or fault probe can test whether a specific assertion detects a realistic wrong behavior, but only with permission and isolation. Use the test-integrity and targeted-mutation guidance in `test-driven-development` and relevant language testing skills when needed; this does not require adopting TDD. Distinguish a proposed probe, static counterexample, and executed result. A surviving mutation needs triage; an equivalent mutation or setup failure is not automatically a missing test or a useful kill.

## Assess modularity, reuse, and module depth

Follow responsibility and state ownership, dependency direction, cycles, and the places that must change together. Evaluate cohesive boundaries and information hiding rather than rewarding more files, classes, or layers. Cite concrete leakage, repeated coordination, or change propagation, and identify boundaries that already work well.

A deep module provides useful behavior while keeping what callers must know small. Inspect the whole caller contract: types and options, ordering rules, state assumptions, error handling, cleanup, and details callers must reproduce. A short signature can conceal a large informal contract. File length, nested calls, or implementation size alone do not establish depth.

Compare similar boundaries to assess whether this approach is used consistently. Identify useful deep modules, shallow pass-throughs or leaky boundaries worth investigating, and justified exceptions. A small adapter may preserve compatibility or isolate an external dependency; it is not defective simply for being thin. Do not force every module into the same shape or merge unrelated responsibilities to manufacture depth.

For reuse, look for shared behavior or policy with compatible contracts and real current or accepted consumers. Distinguish duplicated knowledge that must stay synchronized from coincidentally similar code with different meanings. Check whether extraction removes caller knowledge and duplicated decisions, or instead adds configuration, coupling, and indirection. Do not invent future consumers or recommend a generic framework merely to remove repeated lines.

## Make improvement candidates checkable

Keep confirmed defects separate from behavior-preserving refactoring opportunities and measurement hypotheses. For each worthwhile candidate, give the current evidence/baseline, the smallest useful change to investigate, expected benefit, compatibility and behavior constraints, trade-offs, and a concrete way to verify the benefit. Prioritize by supported impact, confidence, and change risk; retaining the current design is a valid recommendation.

Use measurements appropriate to the claim: independently maintained copies of a rule, affected callers or modules for a specific change, caller-side setup obligations, dependency edges, or observed latency/allocations under a stated workload. Record units, scope, collection method, and comparable conditions. These are signals, not universal quality thresholds. Separate measured current facts, estimated benefits, and a proposed after-state; do not invent a speedup, maintenance saving, overall quality score, or numerical module-depth score. A qualitative trade-off is acceptable when a reliable number is unavailable.

Do not call a behavior change a refactor. State the existing contract and regression protection that would need preserving; expose uncertain semantics before recommending consolidation. Measured performance work belongs with `performance`, design decisions with the applicable design skills, and implementation with separately authorized engineering work.

## Verify within the permitted environment

Read the repository's toolchain and check commands before choosing verification. Use the relevant language reference below only when it affects the question. Verify consequential version-specific behavior against the repository's pinned versions and official documentation; do not upgrade the project to make a check convenient.

Tests, imports, builds, analyzers, and package scripts can execute repository code, run hooks, access credentials or networks, and alter state. Inspect the relevant setup and respect host permissions; prefer bounded checks in a disposable environment when appropriate. Do not assume that a command called "check" is read-only. Do not install tools, run migrations, contact production, or apply fixes merely to complete an analysis.

Record what actually ran, its relevant configuration, result, and limits. When execution is unavailable or unsafe, continue with source evidence and identify the missing check. Passing compilation, lint, or tests only supports the properties and paths those checks cover.

## Return a proportionate result

Lead with the answer. Include only the detail needed to make it checkable:

- **Explanation or impact:** the relevant path and boundaries, with file/symbol locations and line ranges where available.
- **Confirmed findings, when present:** trigger, consequence, evidence, and severity based on actual impact. Distinguish runtime reproduction from static proof. Suggest a bounded correction without applying it unless asked.
- **Quality analysis, when requested:** practice adoption and fit; test effectiveness and evidence-backed gaps; modularity, reuse, and depth consistency; prioritized improvement candidates with baselines and validation. Include sound choices worth retaining. Mark any unassessed requested area explicitly.
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

The module-depth lens follows John Ousterhout's [Modular Design lecture notes](https://web.stanford.edu/~ouster/cgi-bin/cs190-spring16/lecture.php?topic=modularDesign): information hiding and caller-facing complexity, not a line-count rule or numeric score.
