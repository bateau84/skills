---
name: product-acceptance
description: Plan and prove agreed outcomes through the real assembled product-owned path. Use for end-to-end acceptance testing, product review, recovery proofs, or locally green but product-broken evidence. Not for unit/component test mechanics or ordinary code review.
license: MIT
---

# Product Acceptance

Product Acceptance asks: **Does the assembled product, as intended to ship, deliver the accepted outcome?** Local suites can be correct in their own scope while their composition is unusable. Classify them as supporting evidence, not as assembled-product proof.

This is methodology, not permission or a new approval stage. Use agreed requirements, scope exclusions, design, architecture, and project instructions as inputs. Choose ordinary tools and proof mechanics within your task; do not redefine the user's product promise to fit the implementation. Resolve an ambiguous promise with its decision owner, while continuing independent work.

## 1. Select claim-appropriate scenarios

Group accepted criteria into externally meaningful outcomes. Choose the smallest scenario set whose failures would expose materially different composition defects—not one test per requirement or only paths known to work. Use accepted human scenarios and setup-to-first-result, supported-change, and recovery coverage when relevant; optional lifecycle suggestions do not become requirements.

Useful discriminators include UI → API, command → durable state → later read, scheduler → worker → side effect, policy/auth boundaries, upgrade/migration, and interruption/retry. One scenario may prove several related criteria. A happy path cannot alone prove an agreed no-loss or recovery promise. Keep internal invariants in narrower tests when those are sufficient. A pure local change with unchanged public behavior and adequate contract/regression evidence need not manufacture a new expensive E2E test.

Plan proof when its real components will exist; execute representative final proofs after relevant integration changes. If tools or components are unavailable, specify the executable strategy and mark proof pending rather than substituting a demo. For human-facing outcomes, include current implemented-experience evidence where accepted design materially constrains comprehension, controls, accessibility, or responsive behavior. Functional status alone does not prove that experience.

## 2. Draw the boundary before choosing doubles

For each scenario write:

```text
consumer/stimulus entry → product-owned stages → external dependency → meaningful result
```

Mark ownership and real/substituted implementation at every stage. Product-owned stages can include the shipped UI/CLI, server, internal router/queue/scheduler, worker, persistence/migrations, and product-side provider adapter. Ownership follows responsibility, not whether a stage runs locally or remotely. Start where the claimed consumer or stimulus starts: a direct API test may prove an API promise but not a browser journey.

**Every mandatory product-owned stage on the claimed path must use its real production implementation.** A missing endpoint, application mock fallback, demo worker, or fixture-only alternate cannot prove the full scenario. Retain useful narrower evidence and name the skipped behavior rather than discarding all local tests.

A true external dependency may be faked for safety, cost, availability, or determinism: e.g. a provider API, SMTP catcher, hardware simulator, or payment sandbox. Run the real product-side adapter. State which relevant semantics the fake preserves—auth failures, payloads, pagination, quota, ordering, timing, retries, or side effects as the claim requires. A clock/network fixture must not implement the scheduler/recovery behavior it is meant to stimulate. Do not demand a live third party solely to call a proof end-to-end. Conversely, a fake cannot establish live-provider compatibility; obtain suitable provider/contract evidence or explicitly limit that claim.

## 3. Trace state provenance and shipping fidelity

For every material state value consumed later, record **who produced it, through which path, in which run**. Creating configuration via the real command/API, then having the real scheduler consume it, preserves provenance. Inserting a discovered item directly into storage and invoking routing skips discovery; it can prove routing, not discovery → routing.

Fixtures are valid for static prerequisites outside the claim (e.g. an existing account for a routing-only test). They are invalid substitutes for behavior under proof (e.g. a pre-created account when proving registration). Likewise, an accepted upgrade claim can legitimately start with historical stored data, but must run the real migration; injecting already-migrated rows does not prove upgrade. Document reset/isolation and ensure later reads use state from this run, not cache, demo data, or leftovers.

Identify the build/version, package or image, entry command, deployment/configuration, feature flags, and relevant schema used. Exercise the artifact intended to ship, or explain why the tested artifact is equivalent for this claim. Dev-only routing, stale assets, disabled migrations, and test-mode substitutions can invalidate fidelity. A temporary database or local deployment is fine when it runs the relevant real implementations and shipping configuration semantics; production credentials or destructive live data are not required. Revalidate after changes that could invalidate the evidence.

## 4. Execute and record the outcome, not merely initiation

Tie each scenario to accepted criteria and observe the externally meaningful result. `HTTP 202`, a row, a rendered component, or telemetry may be intermediate evidence; when the promise is later explanation, durable completion, or recovery, continue to that result. For promised retry/deferment/idempotency/no-loss, produce and resume state through the real path and observe the relevant later outcome, not just queue-unit success.

Record at least: **claim; entry/path; real stages; external substitutions and evidence limits; prerequisite and produced-state provenance; build/configuration; action; expected/observed outcome; failure/recovery checks; evidence location; status and gaps**. See the directly linked [proof template and worked local-green/product-broken example](references/proof-and-example.md) for a reusable record.

Use PASS only for an executed claim supported by this evidence. An observed violated outcome is FAIL; an unavailable, skipped, uncertain, or inconclusive proof is UNPROVEN. Scope statuses to the claim: narrower routing PASS does not imply full-journey PASS. Plans and fixtures are not execution evidence. Keep logs/assertions/screenshots or transcripts with the run identity and reproduction steps; redact secrets and user data.

## Supporting perspectives and evaluation

- [ASSESSMENT.md](ASSESSMENT.md): conformance of claims and proof records to accepted obligations.
- [QA.md](QA.md): residual false confidence after competent execution and review.
- [Portable evaluation cases](evals/cases.md): bundled prompts, evaluator observations, and standalone execution instructions. Fixtures alone are not evidence that evaluations have run.

**Standalone package:** copy this complete directory, including `references/` and `evals/`. All necessary guidance and case instructions travel with it. Optional collection-only maintenance resources, when using the full library checkout, are `evaluations/selective-enrichment/README.md` (matched comparison protocol) and `evaluations/selective-enrichment/PROVENANCE.md` (baseline identities/adaptation mapping), relative to the collection root. They are not standalone dependencies; without the preserved comparison materials, run the bundled cases as decision exercises rather than claiming a four-variant comparison.

**Source lineage:** selectively adapted from Bateau's MIT-declared `nrkno/mats-opencode-setup`, `skills/product-acceptance/{SKILL.md,ASSESSMENT.md,evals/evals.json}`, revision `3f26d834d84e4f24e14366864a9319f81201e6cb`. Original SKILL SHA-256: `88a202e543b9b6967c76eadd77f94fa892ec8c25f671d0cdfa26047373fd504c`. This is not a verbatim copy: portable boundary/provenance/proof methodology was retained, runtime-specific routing and gate choreography removed, and shipping-fidelity guidance brought into the practitioner path. No external checkout is required to use this package.
