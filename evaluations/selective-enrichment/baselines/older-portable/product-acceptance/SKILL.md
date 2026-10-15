---
name: product-acceptance
description: Product Acceptance planning, proof, and audit methodology. Use when proving that a non-trivial accepted outcome works through the real assembled production-owned path, or when planning/auditing that evidence. Not for local unit/component test mechanics or ordinary code review.
license: MIT
metadata:
  author: Bateau
  version: "1.0.0-portable-baseline"
---

# Product Acceptance

**Not for:** replacing unit/component/contract test strategy, code review, or specialist design validation. This skill proves assembled-product outcomes and composes those narrower evidence sources.

Product Acceptance answers a question no component-level test can answer:

> **Does the assembled product, as intended to ship, actually deliver the accepted outcome?**

This skill supplies methodology only. It does not grant product, design, architecture, planning, review, or adjudication authority.

## Activities

Select the activity needed by the task.

- **Plan:** Derive the smallest discriminating set of accepted-outcome scenarios and place production-composition proofs at the right dependency point.
- **Prove:** Define or implement a proof that enters through a real product boundary and exercises the real product-owned composition. Language/framework testing skills still govern mechanics.
- **Audit:** Decide whether claimed Product Acceptance evidence actually proves the accepted outcome, including mock-boundary integrity and human-experience evidence when applicable.

## Core distinction: local evidence vs product evidence

Useful local evidence includes unit tests, component tests, package/service integration tests, contract tests, backend pipeline tests, UI rendering/accessibility tests, static analysis, and code review.

These can prove their own scope perfectly and still leave the assembled product broken.

**Product Acceptance evidence composes those parts through a meaningful external path.**

Do not downgrade local tests; classify them correctly. They are supporting evidence, not a substitute for the final composition proof.

## Product-owned boundary rule

For the specific scenario under proof, identify every component owned by the product between the external entry point and the externally meaningful outcome.

A Product Acceptance proof uses the real production implementation of each mandatory product-owned component on that path.

Examples of product-owned components:

- shipped web/desktop/TUI/CLI frontend;
- application HTTP/RPC server;
- internal queue/scheduler/router;
- persistence layer and migrations;
- product-defined worker/service;
- product-side adapter translating between internal and external contracts.

A mock, demo implementation, fixture-only alternate, stub, fake service, or fallback that replaces one of those mandatory components **cannot** be the evidence for that scenario.

### True external fakes are allowed

A deterministic fake may replace a dependency **outside** the product boundary when using the real service is unsafe, expensive, flaky, unavailable, or destructive.

Examples: fake YouTube/GitHub/cloud API server while running the real product frontend/backend/database; local SMTP catcher; hardware simulator; external test payment gateway.

The fake must preserve the contract behavior needed by the scenario. If the scenario specifically claims compatibility with the real external system, separate provider/contract verification may still be required.

## Scenario selection

Product Acceptance is not exhaustive combinatorial testing. Choose scenarios that discriminate whether the **product outcome** is coherent.

Prefer accepted human-facing scenarios for human-facing work. For technical-only outcomes, derive system scenarios from acceptance criteria and mandatory shared obligations.

A scenario is valuable when it crosses one or more of:

- user-facing surface → backend;
- API → durable state → later read;
- scheduler/event → worker → side effect;
- multiple independently implemented components;
- authority/policy boundary;
- lifecycle/recovery boundary;
- migration/compatibility boundary;
- critical failure/retry/defer path.

Choose the **smallest set whose failure would reveal materially different composition defects**. Do not create one scenario per requirement mechanically.

## Plan

### Inventory meaningful outcomes

Read the accepted goal, criteria, minimal version and exclusions; accepted experience/design/user stories/scenarios; behavioral requirements and shared obligations; accepted architecture; known external dependencies and deployment shape.

Group acceptance criteria into externally meaningful outcomes. A group can share one Product Acceptance scenario when one real path proves them together.

### Draw the product boundary

For each scenario record:

```text
Entry point → product-owned components → true external dependency (real/sandbox/fake)
            → externally meaningful result
```

Mark every product-owned component as **must be real** in the proof.

### Specify provenance

State how test state originates.

Good: browser creates configuration through real API, then scheduler/run consumes persisted configuration; CLI writes configuration through real command path, later command reads it; event enters real handler and produces state consumed by next real component.

Bad: test inserts DB rows representing state the preceding product component should have produced; test calls a downstream package directly while claiming frontend/API workflow works; test sets a value then asserts the same value exists without traversing the intended path.

Fixture setup is acceptable for static prerequisites; it is not acceptable for the behavior under proof.

### Include outcome and failure semantics

The proof must assert the externally meaningful result. When the accepted outcome promises recovery, deferment, retry, idempotency, explainability, or visible errors, include a scenario that proves the promise through the assembled product.

### Place the proof

Schedule the proof at the earliest point all necessary product-owned realizations exist. Run a final representative Product Acceptance set after all implementation work and before shipping.

Human-facing product changes also need implemented-experience validation against accepted design evidence. Product Acceptance and design validation complement each other: engineering proof establishes functioning composition; experience validation establishes accepted human design fidelity.

## Prove

A proof specification contains:

```markdown
### <identifier> — <descriptive scenario>

**Accepted outcome:** <criteria/story/scenario links>
**Entry point:** <browser|CLI|API|scheduler|event|...>
**Product-owned path:** <ordered components; all real>
**External substitutions:** <dependency → fake/sandbox/real + why>
**State provenance:** <how scenario state is produced by the real path>
**Action:** <what is performed>
**Externally meaningful assertion:** <what proves the user/system outcome>
**Failure/recovery assertion:** <when applicable>
**Human-design validation:** <required evidence path or n/a>
```

Implementation mechanics belong to relevant testing guidance. Do not prescribe Playwright, Cypress, httptest, Docker, testcontainers, etc. unless accepted architecture/stack chooses them or the implementer owns that local tool choice.

### Proof integrity

A proof is invalid if production code switches to a mock path; the harness replaces a product-owned missing component; the proof begins downstream of its claimed boundary; required state is hand-injected instead of produced upstream; assertions stop at internal status while the promise is a user-visible/external outcome; the hard step is skipped/disabled; or a human-facing scenario lacks implementation-level design validation when design materially matters.

## Audit

Audit every claimed scenario in order:

1. **Relevance:** Does it prove an accepted outcome/scenario, mandatory obligation, or critical recovery promise? Generic smoke with no outcome trace is useful but not Product Acceptance.
2. **Entry:** Does it start where the real consumer/system stimulus starts? If it jumps into the middle, name the upstream behavior left unproven.
3. **Product boundary:** Enumerate the path from evidence, not architecture claims. Each mandatory component must be real; a product-owned mock/stub/fallback/demo fails the proof; uncertainty prevents PASS until established.
4. **External substitution:** Confirm each fake/sandbox replaces a true external dependency and preserves needed semantics. Do not reject a good test merely because a third party is simulated.
5. **State provenance:** Trace material state backward. It must come from the actual upstream product stage unless a static prerequisite unrelated to behavior under proof.
6. **Outcome:** The final assertion must mean something at the accepted-outcome level. HTTP 200, a row, or a rendered component may be intermediate evidence but insufficient for user explanation or eligible work surviving quota exhaustion.
7. **Failure/recovery:** Include promised recovery, idempotency, deferment, retry, or visible diagnosis.
8. **Human experience:** For materially design-constrained behavior, require current implementation-level experience validation. Engineering judgment alone does not replace accepted design evidence.

## Local-green/product-broken regression pattern

Accepted outcome and complete-looking requirements/UI design; backend integration tests pass; frontend component tests pass using application mocks; production frontend still falls back to mock data because real backend capability is absent; locally green, globally unusable.

The correct verdict is **Product Acceptance FAIL**. Neither suite is fraudulent inside its own scope; the error is treating their union as proof of production composition. Correct by exercising real built frontend against real product backend/state path, with a fake only beyond the product boundary.
