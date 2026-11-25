---
name: architectural-spec
description: Define exact implementation-facing APIs, schemas, protocols, configuration shapes, messages, and interfaces after the relevant architecture decisions are settled.
---

# Architectural Specification

Use this skill when behavior and structural choices are accepted and implementation needs an exact contract.

## Boundary

A specification realizes architecture; it does not create new architecture or product semantics. If exact specification reveals the need for a new store, protocol family, compatibility layer, lifecycle state, trust boundary, synchronization mechanism, or other material structural choice, return to design/decision work. Route missing observable semantics to the owning authority.

## Reader orientation

Before detailed fields, interfaces or state tables, briefly explain in ordinary language what the two sides must agree on, why, and one representative example of a successful or failed exchange. Keep exact technical names and unambiguous rules in the specification itself. The example must agree with those rules and does not create an additional guarantee. If you cannot explain the contract without assuming new product meaning, return that choice to its owner instead of adding speculative cases.

## Improve existing specifications

If an existing specification needed for the current change is hard to interpret, rewrite its relevant explanation and organization so a reader can understand what the interface guarantees. Keep exact names, types, ordering, version/compatibility rules, failure outcomes, and testable conditions. Do not trade precision for readability or silently modify an accepted contract. If two meanings remain possible, identify the decision owner and block only the dependent part; don't rebuild unrelated specifications just for style.

## Method

1. **Trace authority.** Identify the accepted behavior and parent architecture this contract realizes, plus any authoritative external protocol or current compatibility surface.
2. **State structural constraints.** Capture only falsifiable constraints that matter: versioning, ordering, atomicity, idempotency, durability, size/latency bounds, validation, serialization, authentication/authorization placement, or compatibility.
3. **Define the exact contract.** Specify names, fields, types, ranges/units, required/optional rules, methods/operations, messages, ordering, state transitions, validation, error representation, and unknown/extension behavior as applicable.
4. **Make invariants and ownership explicit.** State which side owns state and transitions, what must remain true, and any concurrency/atomicity boundary. Do not leave lifecycle or failure transitions implicit behind precise happy-path types.
5. **Specify failure behavior structurally.** Define error classes/statuses, retry/idempotency requirements where architecture already establishes them, partial-operation behavior, and what callers may safely infer. For identity-sensitive idempotency/deduplication seams, carry the accepted request identity/equivalence rule explicitly; if parent authority does not determine that rule, surface the missing authority instead of inventing one. Also make the atomic claim/commit boundary, simultaneous-contender arbitration, and the observable result for every contender explicit. "At most one object exists", "duplicates converge", or equivalent state-only guarantees are insufficient when callers could still observe incompatible outcomes.
6. **Define compatibility and evolution.** When versions or persisted states can coexist:
   - separate **reader acceptance** from **producer emission** rules;
   - distinguish unknown optional extension data from unknown required meaning;
   - specify which types/versions/semantic variants a newer producer may emit while older supported consumers still coexist;
   - define explicit handling for unsupported required meaning, unknown discriminators/types, rollback, and persisted old/new state.
   Do not invent rollout policy that parent architecture/product authority has not settled; surface the missing authority when exact emission/admission behavior is not derivable.
7. **Define security surface when applicable.** State trust boundary, authority/data crossing it, validation/authorization point, secret visibility/logging rules, replay controls, and failure behavior.
8. **Run the two-implementer test.** Two competent implementers reading only this specification should produce interoperable components. If materially incompatible implementations could both satisfy the text, tighten the contract.
9. **Define conformance evidence.** Name the smallest set of tests/proofs covering load-bearing invariants, transitions, edge cases, failures, compatibility, and real composition. When interoperability between independently implemented sides is load-bearing, include at least one composition check that exercises those real sides together rather than proving only schema syntax or one-sided behavior. Record downstream verification requirements in the specification or project's tracking system.

Separate normative contract from examples. Prefer the smallest exact interface that removes material ambiguity.

**Do not fill an authority gap with a permanent default.** An unspecified retention, expiry, reuse, or recovery policy is not permission to require infinite retention, forbid reuse forever, or choose an arbitrary timeout. Preserve the accepted guarantee, state which lifetime or failure boundary remains unsettled, and block only the dependent completeness claim. Do not weaken replay safety to "while the record happens to exist" either. Continue specifying the independent, settled interface details; a clearly labeled proposal can inform the missing decision but cannot become normative through an example or invariant.

## Definition of Done for the specification work

Name the bounded interface outcome and the parent capability it enables. The specification is ready when its accepted scope passes the two-implementer test, applicable artifact-quality conditions hold, and its invariants, lifecycle, failures and compatibility rules have decisive conformance checks. No unresolved decision may be hidden inside the scope claimed ready. Identify the implementation or integration work that owns checks which cannot run until both sides exist.

Finish the specification assignment once those conditions and its acceptance criteria are met. A specified conformance test is a future obligation, not an observed pass; a ready specification does not prove interoperating implementations or product acceptance. Report any dependent gap precisely. New accepted scope or evidence of a material ambiguity can reopen the affected contract; hypothetical extensions and optional refinements do not keep it open indefinitely.

## Durable specification shape

Use the sections that apply:

```markdown
## Derived from
## Satisfies
## Implements
## Scope
## Structural constraints
## Interface / schema / protocol
## Invariants and lifecycle
## Failure behavior
## Compatibility and evolution
## Security surface
## Verification
## Readiness and remaining proof
## Open questions
```

Examples are non-normative unless explicitly stated otherwise.
