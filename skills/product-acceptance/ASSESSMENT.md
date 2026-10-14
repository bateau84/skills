# Product Acceptance — Conformance Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

- The scenario set traces to accepted criteria, including load-bearing recovery and human-experience promises, without mechanically duplicating every lower-level test.
- Every full-claim PASS enters at the claimed consumer/stimulus boundary. The path identifies real implementations of all mandatory product-owned stages, including adapters, persistence, and initialization where relevant.
- True external fakes preserve scenario-relevant semantics and have explicit evidence limits. Local mocks remain legitimate evidence for narrower claims; live providers are not required without a claim-specific reason.
- Static prerequisites are distinguished from behavior-produced state. Material state is traceable to this run's upstream production path; injected state does not stand in for the behavior claimed.
- The tested build/deployment/configuration is identified and corresponds to the shipping artifact, or its claim-relevant equivalence is explained. Evidence has not been invalidated by later relevant changes.
- Assertions reach the promised external outcome rather than stopping at request initiation or internal status. Agreed no-loss/retry/recovery and materially constrained human experience have current evidence.
- Proof records contain action, expected/observed results, run identity, reproducible evidence, substitutions, and remaining gaps. Observed failure is FAIL; skipped/inconclusive/unexecuted claims are UNPROVEN.
- For a local-only change, the reason narrower regression/contract proof suffices is explicit; no new E2E ceremony is imposed without an assembled-outcome need.

## Review depth

Scale review depth with consequence, uncertainty, boundary count, and blast radius.
