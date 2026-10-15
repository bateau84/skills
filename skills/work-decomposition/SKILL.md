---
name: work-decomposition
description: Find coherent work groups, change surfaces, and dependencies before creating a delivery plan. Use when agreed work admits several splits, one-task-per-file fragmentation, hidden integration work, or shared-state parallelism risks. Not for inventing product requirements or fixed scheduling policy.
---

# Work Decomposition

**Analyze finely; dispatch coarsely.** Ten concerns may need only three execution units. Optimize for the smallest coherent decomposition that preserves obligations, real boundaries, and a way to prove the assembled outcome—not for task count.

This skill proposes work groups and dependency/coordination facts for the project's delivery plan; it does not require a planner agent, scheduler, or plugin. Ordinary realization choices belong within implementation scope. Accepted product meaning, design, architecture, constraints, and exclusions remain inputs: ask their decision owner about unresolved semantics, do not hide a changed promise inside an implementation group. A decision update needs explicit authorization and a named owner, not just a writable requirements file.

## 1. Discover the work before drawing task lines

Start from outcomes and guarantees, not a file list. Inventory mandatory obligations, invariants, agreed scenarios, interfaces, and exclusions. Use these lenses only when they change the work:

- **Capability:** what distinct outcomes must become true? Exposes missing work.
- **Ownership:** which module/subsystem/responsibility naturally owns each concern? Exposes handoffs.
- **Boundary:** where do data, control, authority, lifecycle, evidence, or failure semantics cross API, storage, process, provider, credential, or policy seams? Exposes integration and shared guarantees.
- **Composition:** which externally meaningful outcomes need several real product-owned stages? Record which groups together enable each assembled scenario; a scenario is not automatically another implementation task.
- **Change surface:** inspect current producers, consumers, schemas, configuration, generated sources, tests, and documentation relevant to the outcome. Ground paths/interfaces/resources in current inspection; mark guesses `[unverified]`. Include mutable non-file resources such as a shared database, test port, cache, or index.
- **Invariant:** what must stay true during rollout and afterward? Exposes migration, compatibility, safety, and recovery work a capability list can miss.

Read-only discovery can extend beyond likely write paths. A natural change surface is a hypothesis, not proof that no other consumer matters, and not permission to write outside granted scope. Inspect load-bearing neighbors before executable handoff; when required writes exceed permission, request the smallest needed scope through the available project/host process. Planning-only work may defer exact scopes if uncertainty and discovery ownership are explicit.

## 2. Group, then test every proposed separation

Prefer a **merge** when concerns share the natural owner, dependency position, closely related surface, and verification story; fit a manageable session; and gain no meaningful independent execution from separation. Route registration, validation, handler, serialization, and API annotation for one small endpoint usually belong together. Separate bullets, names, files, clauses, or stories are not separation reasons.

Keep groups **separate** when merging would hide a consequential boundary:

| Boundary test | Why it matters |
| --- | --- |
| Different natural owner or module responsibility | Prevents duplicate implementation and ambiguous handoff. |
| Hard dependency or independently landing contract sides | Prevents downstream work assuming a capability/contract that does not exist yet. |
| Safety, irreversible migration, or separate rollout/rollback | Keeps a hazardous operation from disappearing inside routine edits. |
| Shared mutable resource requiring coordinated publication | Prevents lost writes, incompatible snapshots, or unsafe tests. |
| Multiple independently delivered product stages | Makes integration/proof prerequisites visible; does not require one task per seam. |
| Meaningful independent parallelism | Allows genuinely independent progress, not theoretical concurrency with repeated coordination. |
| Context/session feasibility | Keeps one execution unit understandable and verifiable without losing the overall obligation. |

For each surviving boundary, name what breaks if it is removed. If nothing material breaks, mark a merge candidate. Conversely, try splitting a broad group: if a safety, dependency, or ownership concern disappears inside it, separate or make that responsibility explicit. A deep-module group may own implementation, tests, and docs across several files; it need not be one task per layer.

## 3. Preserve guarantees and the assembled proof path

Assign each obligation to an outcome/constraint and falsifiable verification, not merely a label in an ownership map. At cross-group seams, name both sides, the shared guarantee, and who integrates and proves conformance. Keep local verification distinct from assembled-product proof. UI and backend component suites do not establish their real composition.

For each accepted assembled scenario, record all required groups and who owns the proof once they exist. The library sibling `product-acceptance` is optional scenario-design guidance when available. Without that sibling, specify the accepted claim, meaningful entry, real product-owned stages, state-producing path, external substitutions and their limits, and an externally meaningful assertion; record evidence or mark the proof unexecuted. The bundled [worked example](references/boundaries-and-example.md) illustrates group prerequisites and proof ownership. Integration or acceptance can live in an existing group when coherent; do not manufacture one integration task per boundary. An early vertical proof is useful where a concrete unresolved seam could invalidate downstream work, not as ritual for every group.

## 4. Describe safe parallelism without assuming a runtime

Dependency independence is necessary but not sufficient. Check semantic contracts, files, generated outputs, shared test state, caches, databases, ports, and publication steps. Inspect the host's actual coordination facilities; **do not assume file locks exist or that a lock makes overlapping work semantically safe**. A lock on one mutation may still allow stale reads, incompatible edits, generated-file races, or test interference.

Overlap is a coordination signal, not a blanket ban on parallelism. Choose a proportionate arrangement: disjoint ownership or isolated worktrees/test resources; an agreed stable interface; or a designated integrator/serialized publication for a shared surface. Before applying an overlapping edit, re-read after intervening changes, reconcile against the current contract, and verify the combined result. Order genuinely conflicting operations when safe coordination is unavailable. Independent analysis or disjoint changes can still proceed concurrently. Separate the logical dependency from the host-specific coordination constraint in the output.

## Output: compact candidate groups

For each group provide:

- **Outcome and responsibility:** what becomes true, natural owner/module, explicit exclusions.
- **Grounded change surface:** files/interfaces/resources inspected and evidence; `[unverified]` guesses plus discovery needed. Exact authorized write scope when this is an executable handoff.
- **Depends on / coordination:** semantic prerequisites, contracts expected from peers, shared-state risks and host-dependent coordination choice.
- **Obligations preserved:** identifiers or plain-language guarantees translated into outcome/constraint/proof; seam participants and integration owner.
- **Verification:** falsifiable local and cross-boundary expectations; relevant specialist guidance only where useful.
- **Assembled scenarios enabled:** which accepted outcomes/scenarios, required peer groups, and proof owner; `none` with reason where appropriate.
- **Boundary reason:** consequence of merging, or `merge candidate`.

Use identifiers and scheduling detail only as requested by the project. Candidate analysis is not a final schedule. Preserve necessary work when groups are later merged or split; do not let compression erase proof or safety ownership.

## References and evaluation

- [Worked boundaries and group template](references/boundaries-and-example.md): endpoint merging, migration separation, and combined proof.
- [ASSESSMENT.md](ASSESSMENT.md): normal conformance checks.
- [QA.md](QA.md): residual coupling and false-confidence attacks.
- [Portable evaluation cases](evals/cases.md): bundled prompts, evaluator observations, and standalone execution instructions. Fixtures alone are not claimed results.

**Standalone package:** copy this complete directory, including `references/` and `evals/`. No sibling skill is required. Optional collection-only maintenance resources, when using the full library checkout, are `evaluations/selective-enrichment/README.md` (matched comparison protocol) and `evaluations/selective-enrichment/PROVENANCE.md` (baseline identities/adaptation mapping), relative to the collection root. They are not standalone dependencies; without the preserved comparison materials, run the bundled cases as decision exercises rather than claiming a four-variant comparison.

**Source lineage:** selectively adapted from `nrkno/mats-opencode-setup`, `skills/work-decomposition/{SKILL.md,ASSESSMENT.md,evals/evals.json}`, revision `3f26d834d84e4f24e14366864a9319f81201e6cb`. Original SKILL SHA-256: `2c9e7b190e1863a937e302dc1593fe19b578bb184db52a73893ba3e1681c64d2`; no separate license field was declared there. This is not a verbatim copy: grouping, guarantee, and composition methods were retained; fixed agent/scheduling routing removed; host-dependent stale-read/shared-state coordination made explicit. No external checkout is required to use this package.
