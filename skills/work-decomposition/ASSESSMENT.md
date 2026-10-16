# Work Decomposition — Conformance Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

- Group boundaries follow coherent capabilities/modules rather than file counts. Merge/separate decisions name real ownership, dependency, safety, contract, resource, composition, context-load, reasoning-horizon, or feasibility consequences.
- Dependencies reflect real semantic/build/integration order and avoid artificial serialization.
- Parallel groups account for the host's actual coordination facilities, stale reads, and shared mutable state as well as semantic dependencies. Overlap has a proportionate ownership/isolation/re-read/integration arrangement, not an assumed automatic lock guarantee. No blanket serialization is imposed on independent work.
- Integration work and cross-boundary verification have clear ownership.
- Change surfaces cite current inspection of relevant producers, consumers, generated artifacts, tests, docs, and mutable resources, or are labeled unverified with discovery ownership. For executable handoff, write scope covers owned implementation/integration/documentation/verification or missing work is explicitly assigned elsewhere. Planning-only analysis may defer exact scope, but its contract must permit later scoping without inventing product meaning.
- Every accepted obligation assigned to a task is represented by its outcome, constraints, acceptance criteria, integration contract, or explicit proof path rather than merely appearing in an ownership map.
- Acceptance criteria are falsifiable and sufficient to prove the task's stated outcome. When an executable scope exists, the task can be executed without silently requiring mutation outside that surface; in planning-only mode, its semantic contract is specific enough for later delivery planning to derive that bounded executable surface without inventing new meaning.
- Cross-task responsibilities are not left ownerless between task boundaries.
- Agreed design/architecture/requirements remain inputs; any decision update has explicit authorization and ownership. Ordinary realization is not needlessly escalated, and unresolved product meaning is not delegated implicitly to implementation.
- Each task has one primary coherent outcome and can state an objective and verification expectation without duplicating sibling work. Its expected working set and reasoning horizon fit one focused execution loop; broad tasks are split when they combine independently useful outcomes, materially separate context areas, discovery that can reshape implementation, or independently meaningful verification.
- No fixed step/file/token ceiling is used as a substitute for judgment, and tightly coupled work is not fragmented when separation would mainly add handoffs or repeated context loading.
- The decomposition can be revised when execution reveals materially broader scope while preserving valid completed evidence and contracts.
- Each accepted assembled scenario lists the groups it needs and its integration/proof owner. Narrower local evidence is not presented as sufficient for the composition; proof ownership need not be a separate task per seam.

## Review depth

Scale review depth with consequence, uncertainty, boundary count, and blast radius.
