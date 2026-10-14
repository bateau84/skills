---
name: work-decomposition
description: Work-boundary analysis for planning. Use when requirements, shared obligations, architecture, or designs admit multiple plausible splits or risk over-decomposition. Not for final scheduling or assignment.
metadata:
  version: "1.2.0-portable-baseline"
---

# Work Decomposition

Find the smallest coherent work boundaries before creating dispatchable tasks.

## Boundary

This skill produces **candidate work groups**, not a plan. It is not for final scheduling, task assignment, or final plan compression.

It decomposes what work exists (obligations); the delivery plan decomposes how to execute it. Candidate groups can feed risk analysis, then planning. For meaningful product-owned boundaries/non-trivial outcomes, acceptance planning groups obligations into assembled scenarios; it does not create implementation groups here.

The delivery plan still determines tasks/subtasks, dependency order, phases, assignment, compression, and whether a scenario becomes dedicated verification or folds into existing verification.

Do not preserve an analytical boundary just because it helped you reason.

## Core rule

**Analyze finely. Dispatch coarsely.** The analysis may discover ten concerns while the final plan needs only three tasks. Separate only when the boundary matters to execution, ownership, safety, contract realization, product composition, or session feasibility.

## Normal path

### 1. Start from guarantees

Read the accepted outcome, behavioral requirements, shared obligations, architectural realizations, invariants, coverage, accepted human scenarios and scope fence. Treat them as coverage obligations, not automatic task boundaries. A contract seam reveals coupling; a scenario reveals product-composition coverage; neither is automatically a separate implementation task. Multiple guarantees may belong to one group.

### 2. Examine useful lenses

Use only lenses that materially change the work shape:

- **Capability:** What distinct outcomes must become true? Detect missing work.
- **Ownership:** Which component/subsystem/specialist naturally owns a concern? Detect responsibility boundaries.
- **Boundary:** Where do data/control/authority/lifecycle/evidence/failure semantics cross meaningful API, database, filesystem, process, provider, tool, credential or policy boundaries? Expose integration and preserve shared guarantees across both sides.
- **Product composition:** Which externally meaningful outcomes need several product-owned components? Mark later acceptance proof and which groups must all land first; do not split implementation merely to mirror scenarios.
- **Change surface:** Which files/interfaces/schemas/configuration/mutable resources are affected? Ground current-codebase claims in same-session evidence; label unsupported targets `[unverified]`. Expose shared ownership and potential write conflicts.
- **Invariant:** What must remain true during and after change? Detect work capability decomposition misses.

### 3. Group before returning

Prefer one group when concerns have the same natural owner, same dependency position, closely related surfaces, fit one session, and gain no meaningful parallelism from separation.

Keep separate when merging would hide a real ownership, dependency, contract, safety, product-composition, or session boundary.

### 4. Apply the separation test

Identify a valid reason for every separate group:

- different natural owner;
- hard dependency;
- resource/write-safety boundary;
- contract realization requiring independently landing both sides before integration proof;
- product composition requiring independently landing real components before acceptance;
- meaningful independent parallelism;
- one-session feasibility.

If none apply, mark a merge candidate.

## Output

Return compact candidates with:

- Outcome: what becomes true.
- Ownership boundary: component/subsystem/responsibility.
- Change surface: grounded resources or `[unverified]`.
- Depends on: candidate group or none.
- Obligations preserved: identifiers or none.
- Product scenarios enabled: accepted scenario/outcome identifiers or none.
- Boundary reason: why separation matters, or merge candidate.

Do not assign final task identifiers, phases, waves, or scheduling in this candidate analysis.

## Planning seam

Planning may merge candidates, turn them into subtasks, split for dispatch safety, or discard distinctions with no execution value. After risk triage, non-trivial cross-component outcomes need acceptance scenario planning. Project task-scope/dependency/write-safety/scheduling/compression rules remain authoritative.

## Failure boundaries

Do not separate merely for separate input bullets, different names/files, independently describable invariants/clauses/stories/scenarios, or manufactured theoretical parallelism.

Do not optimize group count. Optimize for the **smallest coherent decomposition preserving all required work, cross-boundary guarantees, and a path to prove the assembled outcome**.
