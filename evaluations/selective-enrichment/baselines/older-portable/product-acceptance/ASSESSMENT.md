# Product Acceptance — Older Portable Assessment

Normal conformance criteria adapted without named roles:

1. Scenarios trace to accepted outcomes/design/obligations and discriminate rather than mirror requirements.
2. Product boundaries are explicit and every mandatory product-owned component is real.
3. External fakes are beyond the product boundary, preserve needed semantics, and do not make the scenario easier than production.
4. State under proof is produced upstream through the real product path, not injected after behavior under claim.
5. Build/deployment/configuration corresponds to the shipping artifact, not stale/dev-only composition.
6. Assertions reach externally meaningful outcomes, not only codes/rows/telemetry.
7. Promised failure/retry/recovery/idempotency/explanation paths are represented.
8. Human-facing scenarios include current experience evidence where design materially constrains the journey.
9. External behavior, timing, auth, and data semantics are realistic enough for the claim.
10. Selection does not omit the highest-risk composition boundary in favor of known-working paths.

Scale with breadth, statefulness, external boundaries, human complexity, security/data consequence, recovery, deployment variance, and environment/test-double risk.
