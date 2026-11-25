# architectural-spec Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

- The specification traces to accepted behavior and parent architecture and does not create an unapproved structural mechanism or product semantic.
- Exact names, fields, types, validation, ordering, state transitions, ownership, errors, and extension/unknown behavior are implementation-ready where applicable.
- Atomicity, idempotency, concurrency, durability, timeout/retry representation, and partial-operation behavior are explicit when material to the seam.
- For identity-sensitive idempotency/deduplication, the request-equivalence rule is deterministic and traceable to accepted parent authority (or the missing rule is surfaced rather than invented), the claim/commit boundary preserves the accepted invariant, simultaneous equivalent/conflicting contenders have defined arbitration, and every contender has a defined observable result/caller inference.
- Two independent competent implementers could build interoperable sides of the contract without guessing the same unstated rule.
- Failure/lifecycle semantics are as precise as the happy path and remain consistent with accepted authority.
- Missing retention/expiry/reuse authority is visible without silently becoming infinite retention, a temporary TTL, or a weaker replay promise. Settled interface work remains usable; only claims depending on the missing decision remain open.
- Compatibility, migration, mixed-version behavior, and persisted old/new state are specified where coexistence is possible.
- Security boundaries specify validation/authorization placement, secret exposure/logging, replay controls, and failure behavior where relevant.
- Verification hooks cover load-bearing invariants, transitions, failures, compatibility, and real composition rather than only schema syntax.
- Completion is claimed for the specified interface scope, linked to its parent capability. Artifact readiness is supported by contract checks; runtime conformance remains unproven until its evidence exists. Missing authoritative meaning blocks dependent readiness, while optional extensions and unexecuted downstream implementation tests do not automatically block a complete specification-only assignment.

## Review depth

Scale review depth with consequence, interoperability surface, statefulness, and blast radius.
