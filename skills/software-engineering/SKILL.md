---
name: software-engineering
description: "Baseline engineering discipline for changing software. Use when authoring or editing application and library code, services, CLIs, APIs, scripts, tests, build logic, generators, migration code, infrastructure-as-code, or code-bearing configuration, including one-line fixes, refactors, algorithms, and code deletion. Not for docs-only, research-only, design-only, commit-only, PR-only, or technical operations that do not change program-bearing source. Combine with task-relevant language/framework/domain guidance."
license: MIT
metadata:
  author: Bateau
  version: "1.2.0"
---

# Software Engineering

This is the baseline discipline for changing software. It does not replace language, framework, testing, security, observability, Git, or domain skills. Load those when the task needs them.

## Core rules

- **Correctness first.** Clever code that is wrong has no value. Verify the defining behavior, important edge cases, failure paths, and compatibility obligations that actually apply.
- **Prefer the smallest complete solution.** Solve the accepted problem fully with the least new mechanism. Do not add speculative abstractions, extensibility, compatibility layers, feature flags, scaffolding, or TODO architecture for imagined future work.
- **Deletion beats coexistence.** When a replacement makes implementation obsolete, remove the obsolete path once its remaining uses are checked. Do not keep dead code "for later."
- **Make intent explicit.** Names, interfaces, state transitions, errors, and important decisions should reveal what the code means without requiring archaeology.
- **Fail visibly.** Surface and preserve actionable errors. Do not silently swallow failures, convert them into success, or hide partial failure behind fallback behavior unless accepted semantics explicitly require that behavior.
- **Respect accepted authority.** Implementation realizes accepted product, design, specification, security, lifecycle, and architecture meaning. It does not invent missing meaning.

## Deep modules and information locality

Prefer **deep modules**: substantial behavior behind a small, stable interface.

The interface is **everything a caller must know to use the module correctly**. This includes not only functions and parameters, but also required ordering, invariants, state transitions, error modes, configuration, and other protocol knowledge.

- **Depth is a property of the interface, not implementation size.** A large implementation composed from many internal modules can still present one small external seam.
- **Hide coordination, not only code.** If callers must perform the same multi-step sequence, track internal state, understand lifecycle rules, or preserve invariants themselves, that complexity is part of the interface. Prefer moving that protocol behind the module.
- **Prefer outcome-oriented operations over mechanism-oriented choreography.** Let callers state what they need; let the owning module perform the required transitions, validation, recovery, and bookkeeping when those mechanics belong together.
- **Watch for repeated orchestration.** If several callers must know `A → B → C`, inspect B's state, recover through D, then retry C, consider whether that sequence should become one deeper operation.
- **Keep behavior that changes together close together.** A rule should ideally have one owning implementation rather than being reconstructed across callers.
- **Keep implementation detail behind the narrowest useful boundary.**
- **Avoid shallow indirection.** Wrappers, managers, factories, helpers, adapters, or interfaces that mostly forward calls without hiding complexity add surface without adding leverage.
- **Do not split one behavior across many files or modules merely to make pieces smaller.**
- **Use the deletion test.** If removing a seam forces callers to absorb meaningful coordination, decisions, invariants, or protocol knowledge, the seam is hiding useful complexity. If callers can use the underlying capability correctly with no material new knowledge or choreography, the seam may only be pass-through indirection.
- **Treat the interface as the primary test surface.** Important behavior should normally be verifiable through the same seam callers use rather than by reaching through it into implementation details.
- If a small behavior change requires tracing unrelated layers or widespread implementation knowledge, first consider whether the module boundary is too shallow or the information is too scattered.
- Preserve an existing good boundary rather than introducing a new abstraction simply because the change touches it.
- Do not introduce speculative seams merely for architectural neatness. A seam should hide real complexity, isolate meaningful variation, or improve locality.
- A boundary can earn its place with one implementation when it hides cohesive coordination or owns a real rule. The implementation count alone does not establish its value.

A short function or small file is not automatically simple. Likewise, a module containing substantial internal machinery can be simple to use when callers only need to understand a small, stable contract.

## Keep the code easy to change

Strategic programming means making bounded design investments so the code remains easy to change. Use this method when accepted work exposes duplicated rules, repeated caller coordination, hidden dependencies, or recurring workarounds. When the existing design fits the change clearly, implement directly; no refactor or alternatives report is required.

1. **Ground the difficulty.** Inspect the affected rule, callers, and constraints. Distinguish a problem in current work, preparation for accepted upcoming work, and an imagined future feature.
2. **Compare the useful paths.** Consider direct implementation and the smallest preparation that removes the difficulty. Judge complexity across the affected behavior, not only the immediate diff. Include preparation, review, verification, migration risk, and delayed delivery. Direct implementation or deliberate deferral can be sound when accepted guarantees still hold.
3. **Keep decisions within authority.** Make ordinary internal design and local refactoring choices within the task. Route substantive changes to shared contracts, component responsibilities, persistence, or product meaning to their owner. A refactor preserves observable behavior; changed success, failure, retry, or cancellation meaning is a behavioral decision.
4. **Preserve and verify.** Separate behavior-preserving preparation from the intended functional change so tests and review can distinguish them. Reuse relevant checks and add evidence for material gaps, including failure, ordering, and compatibility behavior where applicable. Do not rewrite correct expectations merely to fit a new structure.
5. **Stop at useful preparation.** Stop when the accepted change can be implemented clearly. Check consumers before removing superseded paths. Do not finish an imagined future architecture or expand into unrelated cleanup.

For a material choice, use the existing result, PR explanation, or decision record: concrete difficulty, chosen path and reason, immediate benefit versus conditional future benefit, preservation evidence, and a useful revisit trigger when deferring. A recorded concern remains unresolved; it cannot make unmet required work complete. No extra stage, report, or fixed refactoring budget is required.

## Tests and honest green

Tests are part of implementation when behavior changes.

- Add or update tests alongside the code. Bugs should gain a regression test when the behavior can be exercised.
- Test the defining behavior before exotic cases.
- Prefer real inputs through the real code path. Mock external boundaries when needed; do not mock away the behavior being verified.
- A test that passes because expected pipeline output was hand-injected, the component under test was bypassed, the hard case was skipped, or the assertion was weakened is not evidence of correctness.
- Do not claim build, test, lint, security, runtime, or integration success without observed evidence.
- Load `test-driven-development` when a test-first workflow materially helps implement or fix the behavior; load the applicable language testing skill when writing or changing tests. A trivial change does not need an elaborate test process.

## Errors and operational visibility

Operational behavior should be diagnosable at the boundary where it matters.

- For runtime boundaries, important decisions, retries, external calls, state transitions, and failure paths, add structured signals that let an operator understand what happened.
- Prefer useful, bounded signals over logging everything. Pure local computations do not need artificial telemetry.
- Use logs for discrete events and failure context, metrics for aggregate health/volume/latency, and traces when cross-boundary causality matters.
- Load an applicable observability skill when the task introduces or materially changes operational behavior.

Observability is part of behavior when operators depend on it; it is not decorative instrumentation added after the feature.

## Change hygiene

Keep the change easy to understand, review, revert, and maintain.

- Follow established repository conventions unless the task intentionally changes them.
- Keep unrelated cleanup out of the change. Local cleanup that directly removes complexity introduced or exposed by the change is appropriate.
- Do not edit generated output directly when the source generator owns it.
- Do not preserve obsolete compatibility by default. Preserve it only when an accepted contract or migration obligation requires it.
- Before declaring the implementation done, inspect the resulting diff for accidental complexity, duplicate paths, dead code, stale comments, and missing tests.

## Commits and pull requests

Commits and PRs are engineering artifacts, not afterthoughts.

- When the task includes creating commits, load `git-commit-discipline` before committing. Keep commits coherent, reviewable, and independently understandable.
- When the task includes creating or updating a pull request, load `pr-educational-body` before composing the PR body. Explain why the change exists, the conceptual delta, the important implementation concerns, and observed verification.
- Do not mix unrelated work into a commit or PR simply because it is nearby.

The detailed commit and PR formats live in those skills; do not duplicate them here.

## Completion check

Before returning implementation work, ask:

1. Does the code implement the accepted behavior, including important failure and edge cases?
2. Is there a smaller complete solution across the affected behavior, and did any preparation remove a concrete difficulty without expanding beyond its purpose?
3. Did the change leave obsolete code, duplicate paths, speculative scaffolding, or shallow indirection behind?
4. What must a caller know to use this correctly? Are ordering rules, lifecycle/state mechanics, invariants, recovery, or repeated orchestration leaking through an interface that should own them?
5. Are errors surfaced and operational signals appropriate to the behavior?
6. Do tests exercise the real behavior and explain why the result is green?
7. Is the resulting diff focused and understandable?
8. If committing or opening a PR is in scope, were the dedicated Git/PR skills loaded?

If any answer exposes a real implementation gap, fix it within scope or report the blocker with evidence to the user or responsible collaborator. Do not manufacture completion.

## Evaluation

Optional maintainer exercises: [decision cases](evals/evals.json) test judgment, while the [two-change artifact exercise](evals/artifact-workflow.md) examines actual edits and a fresh recipient's follow-up work. Neither is required during normal implementation. Fixtures and proposed checks are not executed results.
