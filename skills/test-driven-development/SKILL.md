---
name: test-driven-development
description: "Test-Driven Development and test-suite maintenance for any language. Use when implementing a feature test-first, choosing the next example, turning a bug into regression protection, evolving an API from tests, deciding when to Fake It or Triangulate, judging honest-green evidence, consolidating redundant tests, investigating slow suites, or using targeted mutation testing. Covers the Test List, Red-Green-Refactor, design feedback, test lifecycle and cost, boundary tests, and test doubles. Pair with the language testing skill for mechanics."
license: MIT
metadata:
  author: Bateau
  version: "1.3.0"
---

> Language-agnostic TDD methodology with explicit guidance about test integrity and test doubles. Language mechanics live in skills such as `golang-testing` and `python-testing`. Follow the project's testing conventions and the host's execution permissions.

**Persona:** You let tests drive the next behavior and expose design pressure. You do not write new production behavior until a failing test demands it, and you do not trust a green bar until you know why it is green.

## Inspect existing protection

Before adding a test, inspect the affected behavior, existing assertions, fixtures, and execution path. Check relevant regression history and repository test commands when available. Determine what already detects the failure and what remains unproved; a test name or coverage percentage is not enough. Keep this local to the change unless suite maintenance is the task.

Choose examples from accepted outcomes, invariants, and credible failure modes. Where the project uses Domain-Driven Design, use its ubiquitous language and existing domain/consistency boundaries: exercise a rule through its owning interface, and retain integration evidence for contracts across boundaries. Do not derive a test inventory from every class or impose a new domain model for testing.

Prefer extending a suitable existing test or case table when it preserves clear intent and failure diagnosis. Add a separate test when it supplies a distinct example, regression guard, or boundary proof. A pure behavior-preserving refactor can use existing protection; it does not require inventing new behavior to obtain a Red.

## Start with a Test List

Before non-trivial coding, make a small working list of behaviors or examples implied by the accepted contract, accounting for existing protection. For a genuinely single-behavior change, the one next test is enough; do not create list ceremony just to satisfy the method.

The Test List is not a complete up-front test plan. It is a queue of useful next questions. Update it whenever implementation teaches you something new.

Prefer this order:

1. the **defining case** — the central property that makes the behavior correct;
2. the smallest counterexample that prevents a trivial or over-fitted implementation;
3. important boundaries, errors, invariants, and integration cases;
4. newly discovered cases exposed by the implementation.

Choose **one** item and drive it through Red → Green → Refactor before choosing the next. If a test requires a large conceptual leap, split it.

## The core loop

TDD is a tight loop over one conceptual behavior at a time.

### 1. Red — specify the next behavior

Write or extend the smallest test that expresses the next behavior, then run it. An existing regression test that already fails for the intended reason can supply this Red.

A useful Red:

- fails because the intended behavior is missing or wrong;
- reaches the code path you mean to exercise;
- fails at the meaningful assertion or observable boundary;
- is small enough that the reason for failure is obvious.

A compile/type failure caused specifically because the test references the next not-yet-existing API can count as Red: it proves that interface is missing. Add only enough interface to make the test runnable, then continue until the test fails on the intended behavior. Do not count setup mistakes, bad imports, broken fixtures, unrelated dependency failures, or unexplained failures as Red.

If the new test passes immediately, determine why. The behavior may already exist, the assertion may be weak, or the test may not reach the intended path. Do not advance on an unexplained green.

### 2. Green — make the smallest coherent change

Write only enough production code to make the current test pass while preserving previous tests.

There are three classic strategies for moving from a failing example toward general code:

- **Obvious Implementation** — implement the direct solution when it is genuinely obvious and small.
- **Fake It** — use a deliberately simple or hard-coded implementation to reach green quickly when the design is uncertain.
- **Triangulate** — once green, start the next Red with another example that forces an over-fitted implementation to change. Repeat with the smallest useful examples until the implementation expresses the accepted rule rather than a special case.

A temporary Fake It implementation is valid TDD. It is not completion. If the accepted behavior is broader than the example, add the next discriminating test. One added example may only eliminate one fake; keep triangulating when another simple wrong implementation still satisfies the suite. Refactor under green once the tests constrain the accepted rule.

Do not build speculative generality, future options, or cases no accepted behavior requires.

### 3. Refactor — improve the design while green

With all relevant tests green, improve structure without changing behavior.

Refactoring includes production code **and test code**:

- improve names and APIs;
- remove duplication;
- simplify control flow;
- improve cohesion and locality;
- remove test setup noise;
- extract helpers that clarify intent;
- delete obsolete scaffolding from Fake It steps.

Run focused checks after meaningful changes and the affected suite at the appropriate integration boundary, as described under Inner-loop execution. Apply the test lifecycle decisions below when redundant or costly protection is exposed. If behavior changes, you left Refactor and need a new Red.

### 4. Update the Test List

Mark the driven behavior complete, add anything learned, and choose the next smallest useful test.

Then repeat.

## Choosing the next test

The next test should teach you something or force useful progress.

Prefer tests that:

- define the main behavior before exotic edge cases;
- distinguish the desired behavior from the simplest wrong implementation;
- force one missing rule at a time;
- expose uncertainty in the API or design;
- exercise a boundary that lower-level tests cannot prove.

Avoid writing five failing tests at once. Multiple Reds make it harder to know which change caused progress and encourage implementing ahead.

## TDD is also a design method

The test is the first client of the production interface.

Pay attention to friction:

- If the test needs excessive setup, the production API may be too hard to use.
- If the test must understand many unrelated implementation details, responsibilities may be scattered.
- If every test needs many mocks, coupling may be too high.
- If a tiny behavior requires changes across many files, locality may be poor.
- If you cannot name the behavior cleanly in a test, the contract may be unclear.

Do not automatically "fix" test friction with more mocks or helpers. First ask whether the production design is creating the friction.

A useful heuristic: if a focused test requires understanding roughly five or more implementation files, inspect the design boundary before normalizing that complexity.

## Behavior, examples, and invariants

- **Test behavior, not implementation.** Prefer externally meaningful results: returned values, persisted state, emitted events, protocol messages, operator-visible signals, or other accepted outputs.
- **Preserve regression protection.** Reproduce a bug with a new or existing discriminating test before fixing it when practical. Keep protection against the defect while the contract applies; the original test file or shape need not remain forever.
- **Use examples to discover the rule.** When one example permits a trivial implementation, add the smallest second example that forces the actual rule.
- **Test invariants directly.** For state machines, parsers, encoders, stores, or security rules, identify properties that must remain true across examples.

### Operations and inverses

Round-trip tests are valuable for pairs such as encode/decode, add/remove, or serialize/parse:

`decode(encode(x)) == x`

But a round trip can pass when **both sides are wrong in the same way**. When the representation or behavior has independent meaning, also use known-answer tests for each side.

## Maintain the test lifecycle

Treat tests as maintained code. During relevant refactoring or a suite review, choose deliberately:

| Decision | Evidence and constraint |
| --- | --- |
| Keep or improve | The test protects a distinct accepted behavior or failure mechanism. Improve reliability, setup, or diagnostics where useful. |
| Extend | An existing test can cover the missing case clearly without mixing unrelated behaviors. |
| Consolidate or replace | Surviving tests preserve the same required assertions, meaningful inputs, and boundary semantics with less execution or maintenance cost. |
| Retire | The accepted behavior has been removed, or identified remaining coverage provides equivalent protection. Check compatibility and historical regression obligations first. |

For consolidation, start from a passing relevant baseline, identify the surviving protection, and verify it after the edit. For a historical defect or consequential invariant, replay the known counterexample or use a bounded deliberate defect when needed to establish that the replacement still detects it. A green suite alone, matching coverage numbers, or similar test names do not establish equivalence. Never delete the only guard for a still-required behavior to meet a time or count target.

Prefer the least costly test that faithfully exercises the claim. Put a rule's example matrix near its owning interface; retain representative higher-level tests for real wiring and materially different failure modes. Similar assertions across layers can be justified by persistence, serialization, authorization, scheduling, recovery, or platform semantics. Inspect those mechanisms before calling coverage redundant.

Consolidation should preserve readable scenarios and useful failure isolation. Do not turn independent tests into a large shared-state script or hide the oracle in complicated helpers just to reduce lines. Some repeated setup is clearer than an abstraction.

Separate temporary diagnostic probes from durable regression protection. Retain a probe as a permanent test when it guards an ongoing contract or credible regression; otherwise remove temporary instrumentation after the diagnosis. Tests of shared fixtures or acceptance oracles can be valuable when those components could falsely certify the product.

Use the existing Test List, diff, review, or verification note for consequential choices: what protection survives, what cost changes, and what remains uncertain. No per-test form, deletion quota, or whole-suite audit is required for routine work. See [framework basis and examples](references/test-lifecycle.md) for rationale.

## Honest green — test integrity

A passing test counts only when **real input at the level under test travels through the real behavior path being claimed**.

"Real input" does not mean every unit test must boot the full product. A unit test may call a unit directly; an integration test may use an in-memory database or faithful fake when database-specific semantics are not the claim; a boundary test may fake an external service. What must remain real is the behavior whose correctness the test claims to prove.

A test is faking success when it:

- hand-injects the output the code under test was supposed to produce;
- mocks or stubs past the very behavior under proof;
- skips, xfails, comments out, or weakens the hard case to obtain green;
- asserts mainly on values the test itself planted rather than values produced by the behavior;
- replaces the missing implementation with equivalent logic inside the fake or fixture.

If a meaningful test cannot pass without bypassing the behavior, fix the implementation within scope or report the design/scope gap with evidence rather than massaging the test green.

The fingerprint to watch for is: *"the test passes because I supplied the thing the system was supposed to create."*

## Mutation testing — challenge a green suite

Mutation testing deliberately changes production behavior and checks whether the tests detect it. A mutation caught by a relevant failing test is **killed**; one that still passes **survives**. Unlike coverage, this tests the strength of assertions; unlike fuzzing, it changes code rather than inputs. It complements TDD and boundary tests, not replaces them.

Use it selectively after relevant tests are green: prioritize changed decisions, boundary conditions, authorization, state transitions, recovery, and bugs that escaped tests. Start with a few realistic manual mutations or a narrowly scoped existing tool. A trivial change need not gain another stage, tool dependency, or score target.

Before a probe, preserve the current work and use an isolated test copy that includes the actual candidate changes. Establish a passing baseline with real tests collected, change one production behavior without changing the tests, and inspect why the tests fail or remain green. Classify survivors rather than assuming each is a defect; do not count build/setup failures or unexplained timeouts as assertion-based kills. Restore only the deliberate mutation, retain justified test improvements, and rerun the relevant suite and final diff check.

Use [targeted mutation testing](./references/mutation-testing.md) for the bounded procedure, survivor triage, and evidence format. Language testing skills own tool compatibility and execution details. When mutation testing is skipped or blocked for material risk, briefly record why and what evidence remains; do not present an unrun probe as passing.

## Test doubles — choosing boundaries

TDD itself does not require one mocking school. Prefer a **classical/sociable style** when real local collaboration is part of the claim:

- mock or stub true system boundaries such as network APIs, clocks, nondeterministic services, or expensive external systems;
- prefer real collaborators or behaviorally faithful in-memory fakes inside the owned codebase;
- avoid mocking the immediate collaborator when that collaboration is the behavior under proof;
- never put production-equivalent decision logic into a fake, because production and fake can then be wrong identically.

A more interaction-heavy/mockist style can also be TDD. If the agreed architecture or test boundary requires interaction assertions, keep them focused on observable protocol obligations rather than incidental call choreography.

A fixture is **input to** the behavior: sample payloads, files, database starting state, or protocol messages. It is not a substitute for output the behavior itself must create.

## Unit TDD does not prove every boundary

When accepted behavior crosses process, storage, protocol, filesystem, database, CLI, browser, or service boundaries, inspect existing higher-level evidence and add or adapt the smallest test needed to prove the changed composition.

Use the testing pyramid pragmatically:

- many focused unit tests for fast design feedback;
- integration/contract tests for owned boundaries;
- acceptance/end-to-end tests for load-bearing flows that cannot be proven below.

Do not claim a system behavior solely from unit tests whose doubles bypass the relevant composition.

Outside-in TDD is valid when a higher-level acceptance test usefully defines the feature. Keep the inner unit loop small rather than trying to make every Red an end-to-end test.

## Observability can be behavior

Logs, metrics, traces, and events are testable when they are part of an accepted operator or integration contract.

Test the semantic signal — level/category, stable fields, event type, or required context — rather than brittle wording or incidental formatting. Do not turn every internal log line into a public contract.

## Existing code and characterization

When changing poorly understood legacy behavior, a characterization test may first pin the current observable behavior so the change can be made safely.

A characterization test is not proof that the current behavior is correct. Once the desired change is clear, drive the new behavior with the normal Red → Green → Refactor loop.

## Inner-loop execution

Use the focused test for each Red and Green. Broaden to the affected package/module and relevant integration checks as changes interact, and satisfy the repository's required verification at its defined handoff, merge, or release boundary. A slow package suite need not run after every small edit unless policy or the changed risk requires it. Never advance while a relevant failure is unresolved or green is unexplained.

When cost matters, inspect available timings, dependencies, flakes/retries, and fixture maintenance. Consider cumulative cost: duration multiplied by run frequency, matrix size, and repeated agent work. Test scope and resource cost are different dimensions; a test called "unit" can be costly and an integration test can be cheap. Use observed data or label estimates and unknowns; do not claim savings without a comparable measurement.

Reuse prior execution evidence only after checking its tested revision/artifact, selected tests, relevant configuration/platform, and whether later changes invalidate the claim. Independent review still examines the code and evidence; it need not repeat an identical expensive run solely because the reviewer changed. Rerun for relevant changes, suspect evidence, missing coverage, or required policy.

Keep rapid feedback and broader qualification explicit. Moving a required slow check to an existing later stage must preserve its ownership and execution before the claim depends on it. Do not silently skip, quarantine, weaken, or redefine a required check to save time. Bound commands according to the active execution policy and report unexecuted obligations honestly.

Stop expanding verification once accepted behavior, material risks, and applicable required checks have sufficient evidence. Test count, code coverage, a fixed pyramid ratio, and a universal runtime threshold are not substitutes for this judgment.

## Anti-patterns

- **Test-after dressed as TDD** — production behavior exists first and the test merely confirms it.
- **Unexplained Red** — treating syntax, fixture, environment, or dependency failure as proof that the target behavior is missing.
- **Unexplained Green** — assuming a new test proves something because it passes immediately.
- **Permanent Fake It** — leaving a hard-coded example implementation when the accepted behavior requires generalization.
- **Assertion-free tests** — exercising code without discriminating expected behavior.
- **One mega-test** — many conceptual behaviors in one failure.
- **Testing incidental internals** — coupling tests to private structure that can change without changing behavior.
- **Mocking away the proof** — replacing the behavior under test with a double.
- **Testing the framework** — proving the ORM/router/library works rather than proving your logic.
- **Green at all costs** — weakening assertions, skipping cases, or seeding outputs merely to obtain green.
- **Refactor plus behavior change** — silently adding requirements while supposedly cleaning up.
- **Round-trip only** — letting two mutually wrong implementations validate each other.
- **Mutation-score theater** — widening exclusions, weakening behavior, or adding brittle tests merely to reach a number; calling a manual sample a whole-suite score.
- **Additive-only maintenance** — adding another test before inspecting existing protection, preserving obsolete tests indefinitely, or repeating the same scenario matrix at every layer without a distinct failure mechanism.
- **Cost-only deletion** — removing slow tests or moving them out of the required path without preserving the behavior and boundary they prove.

## Cross-references

- The project's testing conventions and host instructions — scope, execution policy, and evidence expectations;
- `golang-testing`, `python-testing`, `typescript-testing`, or another language testing skill — framework and language mechanics;
- the applicable language `*-common-practice` skill — compile/check/lint inner-loop mechanics.

---

This skill owns the TDD **method**. Language testing skills own testing **mechanics**. Load both for test-first implementation work.
