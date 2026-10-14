# Product Acceptance Decision Cases

Prepared evaluation inputs, **not executed results**. Adapted from the older source's eight product-acceptance cases; fidelity and paired setup/scope cases extend the accepted findings. Source identity and adaptation limits are recorded in the bundled [SKILL.md](../SKILL.md). Evidence packets below are case facts, not claims about this repository.

### Standalone execution

In a fresh session, explicitly load the bundled `SKILL.md` and allow its practitioner reference when useful; then give only one selected **Prompt** and the common instruction below. Withhold evaluator observations, companion rubrics, and other participants' answers. Retain the first answer, actual loads, and any feedback rounds; judge the produced finding/proof against the case's evaluator observations for correctness, preserved obligations, actionable evidence, and proportionality. Record missed defects, unnecessary blockers, correction rounds, and cost only where observed; do not score document length or claim an application ran.

> Work from the supplied task and evidence packet within its stated scope. Produce the requested practical artifact and rationale. Treat supplied facts as evidence for this decision exercise, not as actions you performed. State missing evidence and unresolved decisions precisely; continue independent work where possible. Use available reference material when useful. Do not invent requirements, tool execution, or results.

A no-skill control omits skill/reference context but keeps the same prompt, model, tools, common instruction, and budget in another fresh session. Four-variant comparisons additionally require genuinely preserved current/older-portable materials and identified repaired bytes: never reconstruct a baseline from memory or call a single-package exercise that comparison. The full collection optionally provides `evaluations/selective-enrichment/README.md` and historical baseline/pilot records relative to its root; these collection-only maintenance resources are not required for this standalone exercise. Explicit loading tests task performance, not discovery.

## PA1 — local green, missing product stage

**Prompt:** Assess this evidence and write a scoped acceptance finding with the next proof needed. The accepted browser journey lets a user configure discovery and later inspect persisted accept/reject reasons. Backend routing tests pass. Frontend rendering tests pass against application mocks. Inspection of the shipping client shows it still uses an in-memory decision-detail fallback because the app has no real detail endpoint. The team claims the two green suites prove the journey. No assembled run occurred.

**Evaluator observations:** Reject full-journey PASS; distinguish valid local evidence from missing product-owned implementation. The known missing endpoint/fallback is a defect, not merely an unavailable test. Require real built UI → API/state → later UI reasons, without patching in a test-only endpoint. Do not demand a live external provider absent a compatibility claim.

## PA2 — allow an external fake, limit compatibility

**Prompt:** Audit a supplied run record. The browser runs the shipping-equivalent built SPA, real app API/auth, real worker and real migrations/persistence in an isolated temporary database. An existing account is a static prerequisite; registration is not claimed. The browser creates configuration, the real scheduler produces items, and a later browser read checks persisted reasons for accepted and rejected items. A local fake replaces only the external video API; the real product adapter runs. Fake payload/pagination/quota semantics match those needed for this scenario. The record contains build/configuration, run identity, assertions and logs. Is this valid for the stated journey? Can the same record prove compatibility with the live provider? State limits and needed evidence, not a blanket no-fakes rule.

**Evaluator observations:** Potentially valid supplied journey proof, not a claim of participant execution. Allow the fake and static account. Live-provider compatibility needs suitable independent evidence; do not require live traffic just to accept the narrower journey.

## PA3 — injected behavior versus static prerequisite

**Prompt:** Classify two proofs. A claims discovery → routing → action, but inserts a discovered-item row before running the real router/adapter and observing the action. B claims routing → action only; it uses an existing account and supplied item as prerequisites and runs the real routing/action path. Write the supported claim and gap for each, and a corrected plan for A. Do not discard useful narrower evidence.

**Evaluator observations:** A skips discovery provenance, so no full-claim PASS; preserve routing proof. B's prerequisites can be legitimate for its narrower claim. Correct A by real discovery stimulus/state production; do not prohibit all seeding or pretend the plan executed.

## PA4 — discriminating scenario selection

**Prompt:** Plan evidence for 18 agreed requirements: six concern one create/edit/save browser workflow, four interruption/recovery, five later analytics history, and three internal invariants fully covered by current integration tests. Relevant design requires understandable mobile recovery status. Propose the smallest materially discriminating set, trace coverage, list real-stage/prerequisite needs and meaningful assertions. There are no execution results yet. Avoid one E2E per requirement and avoid declaring all recovery proved by the happy path.

**Evaluator observations:** Group coherent paths (create/edit/save, recovery, later history), retain local invariant proof, and include design evidence where material. Show real composition/provenance and required groups, not just names; mark plans unexecuted. A justified combined history/save proof is acceptable if it covers distinct defects.

## PA5 — accepted mobile experience not yet validated

**Prompt:** The real assembled browser workflow completed in a recorded run. The final functional assertions pass. The accepted design requires interruption status to be understandable on mobile and recovery controls to remain visible. No implemented mobile experience was inspected; only desktop status codes were asserted. Assess the claims and propose bounded additional evidence without inventing a redesign or requiring a named design agent.

**Evaluator observations:** Functional proof remains useful; experience/full-design claim is unproven. Request current implementation-level mobile comprehension/control evidence against accepted design, not new UX scope or mandatory named roles.

## PA6 — near miss: local-only patch

**Prompt:** Choose verification for a pure internal Unicode-normalization fix. Inspection shows no product/component-boundary change; existing public contract cases capture unchanged behavior, and focused regression cases cover the bug. Do you require a new browser/system proof? Give rationale and relevant checks. No new user journey or compatibility promise is part of this patch.

**Evaluator observations:** No ceremonial new E2E. Retain relevant contract/regression verification and explain claim appropriateness. Do not say no testing is needed or create new scope.

## PA7 — initiation is not explanation; recovery is not queue-unit green

**Prompt:** The agreed promise is later explanation of each item and no silent loss of eligible work on quota exhaustion. A real UI/API run asserts only `POST /run = 202`. Queue-unit tests pass, but no assembled quota/defer/resume test or later reason read exists. Write a proof plan with externally meaningful assertions, state provenance, and statuses based on this evidence. External-provider simulation is allowed, but the worker/queue/adapter are product-owned.

**Evaluator observations:** Neither later explanation nor recovery is proved by this evidence. Plan real later reason reads and real produced/deferred/resumed state, observe no loss and any agreed duplicate semantics. Do not invent exactly-once guarantees; do not simulate the product-owned worker or mark planned scenarios PASS.

## PA8 — stale/dev build and upgrade fidelity

**Prompt:** Audit an upgrade proof. Shipping release R runs packaged assets with direct API routing and real startup migrations. The successful proof used dev assets with a proxy, release R-1 server code, and a seed script that inserted already-migrated rows. Its final page assertions pass. The promise is that existing users can upgrade from the prior schema and inspect their saved history. Explain defects and minimal corrected proof, including any legitimate historical fixture input. No live production credentials are available.

**Evaluator observations:** Wrong composition and replaced migration cannot prove the upgrade. Use shipping artifact/configuration semantics, historical pre-upgrade state and real startup migration followed by real user read. Allow isolated temporary data; do not require production secrets or reject historical fixtures as such.

## PA9 — API claim versus browser claim

**Prompt:** A run enters the real public API, creates state through the real server/worker/database, and reads a durable result through the real API. Evidence and shipping-equivalence are identified. Assess (a) the accepted API-consumer promise and (b) a proposed claim that the same test proves a browser user can create/read that result. No browser path ran. Explain which scope can pass and which additional evidence is needed.

**Evaluator observations:** Real API evidence can support the API claim without a browser mandate. Browser promise needs its actual client integration/experience proof. Do not promote API proof to browser proof or block the API proof merely for lacking UI.
