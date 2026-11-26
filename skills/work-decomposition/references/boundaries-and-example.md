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

## Example 3: usable milestones, then coherent tasks

**Accepted outcome:** browser-created configuration leads to persisted decisions that the user can inspect; quota exhaustion preserves eligible work for later resume.

**Illustrative current inspection:** `web/decision-client`, `app/config-api`, `app/decision-api`, `worker/discovery`, and `db/migrations` have been inspected along with their tests. These example paths are not claims about this skills repository.

Start with the outcomes to demonstrate, then identify the task groups needed for each:

| Proposed milestone | Contribution and evidence | Work needed / boundary |
| --- | --- | --- |
| Configure discovery and inspect a real decision | Establish the shortest useful explanation journey: create configuration in the built UI, let the real worker produce a decision, and reload its persisted reason through the real API/UI | Real configuration, schema, auth, discovery, persistence and details path for this scenario; no product-side fallback. A genuine external provider fake may supply normal responses. |
| Resume eligible work after quota exhaustion | Extend the working journey to the accepted recovery promise: exhaust quota, inspect retained work and understandable interruption status, then resume through the product and observe later results | Real defer/resume behavior and controls, plus rechecking the earlier explanation journey. Preserve the accepted no-loss and authority rules throughout. |

These are bounded proof scopes, not permission to ship incomplete recovery or weaken the accepted behavior. If safe execution of the first scenario requires a foundation from the second, bring that prerequisite forward and explain why. Keep unproved recovery visible after the first demonstration.

Within the first milestone, API/storage, worker/adapter, and UI/integration can still be separate tasks when ownership and execution context justify them. Each owns the part needed for the same real journey; do not require the complete future API or worker surface before composing it. The integration owner runs the assembled proof. Small shared scope may instead fit one vertical task. Local mocks can support parallel implementation against an agreed interface, but cannot satisfy the milestone.

Waves schedule the tasks using real dependencies and shared-state constraints. A generated client or migration file needs an integrator/publication arrangement; a temporary database needs isolation or ordered runs. None of these scheduling choices establishes product acceptance by itself.

After the first demonstration, inspect whether the explanation is usable and whether the chosen boundaries compose cleanly. Carry observed gaps into the next milestone, retain valid work and evidence, and revisit only affected remaining detail. Later outcomes keep their owners and proof paths even while their task breakdown remains coarse.

## Candidate group template

```markdown
### <candidate name>

- Outcome / responsibility / exclusions:
- Parent contribution: <larger outcome this work advances>
- Grounded surface: <paths, interfaces, mutable resources + inspection evidence>
  Unverified targets / discovery owner:
  Authorized executable scope, if applicable:
- Depends on: <group + capability/contract, or none>
- Coordination: <shared state; actual host facilities; isolation/integrator/re-read choice>
- Obligations preserved: <guarantee → outcome/constraint + proof>
- Seam participants / integration owner:
- Completion:
  - Acceptance criteria: <observable conditions allocated to this group>
  - Applicable Definition of Done: <shared baseline reference; obligations allocated to this group>
  - Required evidence: <what establishes those conditions at this boundary>
  - Return boundary: <return when this group's allocated conditions are evidenced; otherwise name the unmet condition>
  - Mandatory downstream obligations: <remaining review/proof; responsible owner; parent acceptance boundary kept open>
- Milestone or scenario enabled: <accepted outcome; peer prerequisites; assembly/proof owner; or enabling risk and dependent outcome>
- Execution fit: <why this fits one focused loop; context surface, material reasoning transitions, uncertainty, retry/verification boundary>
- Boundary reason: <what goes wrong if merged, or merge candidate>
- Unresolved decision: <exact question + decision owner, or none>
```

An output can be a table or brief prose instead. Compactness must not erase guarantees, proof ownership, or safety. In planning-only mode exact write permissions can remain deferred with discovery ownership; executable handoff must account for the required implementation and proof surfaces.
