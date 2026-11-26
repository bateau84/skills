# Product Acceptance — Conformance Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

- The scenario set traces to accepted criteria, including load-bearing recovery and human-experience promises, without mechanically duplicating every lower-level test.
- Existing scenarios and evidence were inspected before adding proof. Consolidation preserves distinct composition failures and provenance; costly qualification remains owned and executed at the required boundary. Reuse checks artifact/configuration applicability and evidence quality without substituting a prior verdict for independent assessment.
- A milestone claim identifies its contribution to the parent goal and the bounded outcome actually demonstrated. Earlier relevant behavior remains supported; unfinished later capabilities do not invalidate a valid narrower claim or become implicitly accepted by it.
- Every full-claim PASS enters at the claimed consumer/stimulus boundary. The path identifies real implementations of all mandatory product-owned stages, including adapters, persistence, and initialization where relevant.
- True external fakes preserve scenario-relevant semantics and have explicit evidence limits. Local mocks remain legitimate evidence for narrower claims; live providers are not required without a claim-specific reason.
- Static prerequisites are distinguished from behavior-produced state. Material state is traceable to this run's upstream production path; injected state does not stand in for the behavior claimed.
- The tested build/deployment/configuration is identified and corresponds to the shipping artifact, or its claim-relevant equivalence is explained. Evidence has not been invalidated by later relevant changes.
- Assertions reach the promised external outcome rather than stopping at request initiation or internal status. Agreed no-loss/retry/recovery and materially constrained human experience have current evidence.
- Proof records contain action, expected/observed results, run identity, reproducible evidence, substitutions, and remaining gaps. Observed failure is FAIL; skipped/inconclusive/unexecuted claims are UNPROVEN.
- Completion is scoped to the claim and includes all shared quality obligations required at that acceptance boundary, with evidence from their responsible owners. Locally complete implementation does not satisfy or waive pending independent review or composed proof. A finished assessment may report FAIL or UNPROVEN without declaring the product done. Sufficient evidence supports closure; optional suggestions do not create new acceptance blockers.
- For a local-only change, the reason narrower regression/contract proof suffices is explicit; no new E2E ceremony is imposed without an assembled-outcome need.
- Milestone feedback distinguishes observed criterion failures from new improvement suggestions and identifies affected next work without changing accepted meaning or inventing an approval stage.

## Review depth

Scale review depth with consequence, uncertainty, boundary count, and blast radius.
