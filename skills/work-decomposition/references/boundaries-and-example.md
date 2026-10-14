# Worked Boundaries and Candidate Group Record

These are illustrative planning examples, not a fixed task count, schedule, or evaluated result. Apply the decisions in [SKILL.md](../SKILL.md) to current evidence.

## Example 1: merge an endpoint's analytical concerns

An agreed feature adds one decision-detail endpoint. Current inspection shows route registration, request validation, handler, response serialization, and API documentation share the same owner, small module surface, dependency position, and local verification path.

Keep them in one coherent group, or mark the documentation concern as a merge candidate if its delivery ownership is still undecided. Five concerns do not justify five handoffs. The group owns an externally usable endpoint, schema-conformant errors, tests, and documentation—not just a handler file. Inspect the caller and generated API client before asserting the surface is complete.

## Example 2: separate a hazardous operation despite one storage theme

An accepted architecture requires an additive schema/read compatibility change and a separately deployed irreversible backfill. Both are “database work,” but merging would hide rollout safety and a hard prerequisite. Current inspection also finds API and worker consumers.

- **Compatibility group:** real schema, API/worker consumers, tests, and rollback-compatible reads/writes as accepted. Owns the relevant interface guarantee.
- **Backfill group:** accepted irreversible data transformation, restart/runbook checks, and integrity verification. Depends on the established compatibility guarantee and deployment prerequisites; does not choose new data-loss policy.
- **Proof responsibility:** one named group/person exercises real upgrade from historical state, then API/worker behavior after transformation. The proof may be part of backfill delivery; no task per database boundary is required.

If the accepted inputs do not specify transformation semantics or permitted loss, flag that decision for its owner. Choosing query structure or test mechanics within the agreed transformation is ordinary implementation, not a new product decision.

## Example 3: cross-component composition without task explosion

**Accepted outcome:** browser-created configuration leads to persisted decisions that the user can inspect; quota exhaustion preserves eligible work for later resume.

**Illustrative current inspection:** `web/decision-client`, `app/config-api`, `app/decision-api`, `worker/discovery`, and `db/migrations` have been inspected along with their tests. These example paths are not claims about this skills repository.

| Candidate | Outcome / obligations preserved | Surface and boundary | Dependencies / proof |
| --- | --- | --- | --- |
| Configuration and decision API | Persist accepted configuration and expose real decision reasons, enforcing accepted auth/schema | API module, migrations, contract tests; coherent server/storage owner | Supplies stable API/schema to UI and worker; owns API/storage conformance |
| Discovery and durable resume | Use persisted configuration; preserve eligibility across quota and resume according to accepted guarantee | Worker/queue/provider adapter and tests; distinct lifecycle owner | Uses the established storage/contract; owns worker/adapter conformance |
| User journey and assembled proof | Built UI consumes real details, no product-side mock; agreed status/recovery controls | UI/client tests plus real browser/API/worker proof; coherent consumer responsibility | Needs both server and worker for final proof; owns creation → discovery → explanation and quota → resume scenarios |

UI development may proceed against the agreed interface while backend work proceeds, but mocks remain local scaffolding, not final acceptance. Final assembled proof needs all real stages. A shared generated API client or migration file needs an explicit integrator/publication arrangement. A shared temporary database needs isolation or ordered runs even if source files are disjoint.

This grouping is not universal: shared ownership and small surface might favor a single vertical group; separate delivery/safety responsibilities might justify more. Name the consequence of the boundary rather than preserving this table mechanically.

## Candidate group template

```markdown
### <candidate name>

- Outcome / responsibility / exclusions:
- Grounded surface: <paths, interfaces, mutable resources + inspection evidence>
  Unverified targets / discovery owner:
  Authorized executable scope, if applicable:
- Depends on: <group + capability/contract, or none>
- Coordination: <shared state; actual host facilities; isolation/integrator/re-read choice>
- Obligations preserved: <guarantee → outcome/constraint + proof>
- Seam participants / integration owner:
- Local and cross-boundary verification: <falsifiable expectations>
- Assembled scenarios enabled: <accepted outcome; peer prerequisites; proof owner, or none + why>
- Boundary reason: <what goes wrong if merged, or merge candidate>
- Unresolved decision: <exact question + decision owner, or none>
```

An output can be a table or brief prose instead. Compactness must not erase guarantees, proof ownership, or safety. In planning-only mode exact write permissions can remain deferred with discovery ownership; executable handoff must account for the required implementation and proof surfaces.
