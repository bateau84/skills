---
name: work-decomposition
description: Find coherent, context-bounded work groups, change surfaces, and dependencies before creating a delivery plan. Use when agreed work admits several splits, oversized execution units, one-task-per-file fragmentation, hidden integration work, or shared-state parallelism risks. Not for inventing product requirements or fixed scheduling policy.
---

# Work Decomposition

**Analyze finely; dispatch coherently.** Keep each task small enough that its owner can understand, perform and verify it without keeping several largely separate problems in mind. Ten concerns may need three tasks, or one broad concern may need several. Task count is not the goal: too many fragments add handoffs; oversized tasks cause repeated reading, lost context and expensive retries.

This skill proposes work groups and dependency/coordination facts for the project's delivery plan; it does not require a planner agent, scheduler, or plugin. Ordinary implementation choices remain within implementation scope. Accepted product meaning, design, architecture, constraints, and exclusions remain inputs: ask their decision owner about unresolved meaning, and do not hide a changed promise inside an implementation task. A decision update needs authorization and a named owner, not just a writable requirements file.

## 1. Discover the work before drawing task lines

Start from outcomes and guarantees, not a file list. Inventory mandatory requirements, rules that must remain true, agreed scenarios, interfaces, and exclusions. Use these questions only when they change the work:

- **Capability:** what distinct outcomes must become true?
- **Ownership:** which module or responsibility naturally owns each concern?
- **Boundary:** where do data, control, permissions, state, evidence, or failures cross between components? What must both sides agree on?
- **Composition:** which user-visible outcomes need several real product-owned parts? Record which groups together enable each scenario; a scenario is not automatically another task.
- **Change surface:** inspect current producers, consumers, schemas, configuration, generated sources, tests, and documentation relevant to the outcome. Ground paths and resources in current inspection; mark guesses `[unverified]`. Include shared databases, test ports, caches, and indexes.
- **Preservation:** what must stay true during rollout and afterward? Check migration, compatibility, safety, and recovery where they matter.

Read-only discovery can extend beyond likely write paths. A likely change surface is not proof that no other consumer matters, nor permission to edit outside scope. Inspect important neighbors before handing off executable work. Request the smallest needed write scope through the host's normal process. Planning-only work may leave exact paths unresolved when the uncertainty and discovery owner are clear.

## 2. Group, then test every proposed separation

Prefer a **merge** when concerns have the same natural owner, dependency position, closely related files, and verification story; fit one focused task; and gain no meaningful independent execution or context reduction from separation. Route registration, validation, handler, serialization, and API documentation for one small endpoint usually belong together. Separate bullets, names, files, clauses, or stories are not reasons to split.

Keep groups **separate** when merging would hide an important boundary:

| Boundary test | Why it matters |
| --- | --- |
| Different natural owner or module responsibility | Prevents duplicate implementation and ambiguous handoff. |
| Hard dependency or independently landing contract sides | Prevents downstream work assuming a capability that does not exist yet. |
| Safety, irreversible migration, or separate rollout/rollback | Keeps a hazardous operation from disappearing inside routine edits. |
| Shared mutable resource requiring coordinated publication | Prevents lost writes, incompatible snapshots, or unsafe tests. |
| Multiple independently delivered product stages | Makes integration and proof prerequisites visible; does not require one task per connection. |
| Meaningful independent parallelism | Allows genuinely independent progress, not repeated coordination. |
| Context needed to understand and verify the task | Avoids requiring several independent investigations or a large changing working set at once. |

For each boundary, name what breaks if it is removed. If nothing material breaks, consider merging. Conversely, split a broad group when it hides a safety, dependency, ownership, or context problem. One coherent task can own implementation, tests, and docs across several files; it need not be one task per layer.

### Size by execution fit, not by task count

Ask whether the owner can finish this outcome with a stable, relevant set of inputs. Check whether parts can be useful or verified independently, whether unrelated modules and decisions must stay active together, and how much valid work a late failure would force the next attempt to repeat.

Separate an investigation or decision from dependent implementation when its answer could reshape that implementation. For example, deciding what restart must mean can be one task; implementing the agreed behavior can be the next. A small implementation and its regression tests normally stay together. Many mechanical edits with the same context may also fit one task.

Do not impose a fixed maximum for files, tokens, steps, tasks, or session resumes. Repeated rereading, lost constraints, new unrelated questions, or resumed runs without a useful result are reasons to inspect task size—not proof by themselves that work is wasted. Preserve sound work and narrow the unfinished part before dispatching again. A fresh session with the same oversized assignment does not fix the task.

If execution reveals more scope, uncertainty or context than planning could know, **split only the remaining work**. Keep completed evidence attached to the result it actually proves. Update dependencies and remaining verification; do not mark the original task complete merely because its unfinished work was handed over.

### Handoffs that let the next task start fresh

At meaningful task boundaries, identify what the next owner needs without requiring the old conversation. Use one short entry in the existing result store or project notes: goal and revision, decisions or changes, evidence and limits, unresolved work, and next useful step. Link to code, documents and full evidence. No new report file, schema, plugin or approval stage is required.

A reference must be retrievable, and a sampled excerpt may omit important qualifications. The recipient should read essential records in full and check their revision and applicability. A handoff does not certify completion or create authority. Preserve an important rejected option and its reason when that prevents reopening the same discussion; do not carry every speculative branch forward.

A continuation may use earlier conclusions. An independent first assessment instead needs accepted requirements, current artifacts and source evidence before prior opinions. Keep earlier finding references available for reconciliation before its final verdict. Session choice and host context settings remain the caller's responsibility.

## 3. Preserve guarantees and the assembled proof path

Assign each obligation to an outcome, constraint and testable verification, not merely a label. Across groups, name both sides, the shared guarantee, and who integrates and proves it. Keep local verification distinct from whole-product proof. Separate UI and backend tests do not establish that the real UI and backend work together.

For each accepted whole-product scenario, record the required groups and proof owner. The sibling `product-acceptance` is optional guidance when available. Without it, state the accepted claim, meaningful entry, real product-owned stages, where state comes from, external substitutions and their limits, and an externally meaningful assertion. Record evidence or mark the check unexecuted. The [worked example](references/boundaries-and-example.md) illustrates prerequisites and proof ownership. Integration or acceptance can stay in an existing group when coherent. Test an uncertain connection early when its failure could invalidate dependent work, not as a ritual for every group.

## 4. Describe safe parallelism without assuming a runtime

Dependency independence is necessary but not sufficient. Check contracts, files, generated outputs, shared test state, caches, databases, ports, and publication steps. Inspect the host's actual coordination facilities; **do not assume file locks exist or that a lock makes overlapping work correct**. A lock on one edit may still allow stale reads, incompatible changes or test interference.

Overlap needs coordination, not a blanket ban on parallelism. Use disjoint ownership or isolated worktrees/test resources, an agreed interface, or an integrator who publishes changes in order. Before an overlapping edit, reread after intervening changes, reconcile with the current contract, and verify the combined result. Order conflicting operations when safe coordination is unavailable. Independent analysis or disjoint changes can still proceed. Keep the logical dependency separate from the host's coordination limits.

## Output: compact candidate groups

For each group provide:

- **Outcome and responsibility:** what becomes true, its owner, and exclusions.
- **Grounded change surface:** inspected files, interfaces or resources and evidence; `[unverified]` guesses plus needed discovery. Include authorized write scope for executable work.
- **Depends on / coordination:** prerequisites, shared contracts, shared-state risks, and the available coordination method.
- **Obligations preserved:** guarantees translated into outcome, constraint and proof; participants and integration owner.
- **Verification:** testable local and cross-boundary expectations; relevant guidance only where useful.
- **Assembled scenarios enabled:** accepted outcomes, required peer groups, and proof owner; `none` with a reason where appropriate.
- **Execution fit:** why the task is small and coherent enough; needed context, important uncertainty, retry cost, and the result references the next owner will need.
- **Boundary reason:** what would break if groups were merged, or `merge candidate`.

Use identifiers and scheduling detail only as requested. Candidate analysis is not a final schedule. Preserve necessary work when groups are merged or split; do not let shorter descriptions erase proof or safety ownership.

## References and evaluation

- [Worked boundaries and group template](references/boundaries-and-example.md): endpoint merging, migration separation, and combined proof.
- [ASSESSMENT.md](ASSESSMENT.md): normal conformance checks.
- [QA.md](QA.md): residual coupling and false-confidence attacks.
- [Portable evaluation cases](evals/cases.md): bundled prompts and standalone execution instructions.
- [Context and handoff cases](evals/context-and-handoffs.json): task sizing, preserving work, and useful result references. These are fixtures, not executed results.

**Standalone package:** copy this complete directory, including `references/` and `evals/`. No sibling skill is required. Optional collection-only maintenance resources, when using the full library checkout, are `evaluations/selective-enrichment/README.md` (matched comparison protocol) and `evaluations/selective-enrichment/PROVENANCE.md` (baseline identities/adaptation mapping), relative to the collection root. They are not standalone dependencies; without the preserved comparison materials, run the bundled cases as decision exercises rather than claiming a four-variant comparison.

**Source lineage:** selectively adapted from `nrkno/mats-opencode-setup`, `skills/work-decomposition/{SKILL.md,ASSESSMENT.md,evals/evals.json}`, revision `3f26d834d84e4f24e14366864a9319f81201e6cb`. Original SKILL SHA-256: `2c9e7b190e1863a937e302dc1593fe19b578bb184db52a73893ba3e1681c64d2`; no separate license field was declared there. This is not a verbatim copy: grouping, guarantee, and composition methods were retained; fixed agent/scheduling routing removed; host-dependent stale-read/shared-state coordination made explicit. No external checkout is required to use this package.
