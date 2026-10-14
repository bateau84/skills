---
name: work-decomposition
description: Divide accepted outcomes into coherent, independently implementable tasks, with shared contracts and integration proof. Use when meaningful work admits several viable parallel splits; not to mandate a specific planner, harness or task graph.
---

# Work Decomposition

Analyze finely; dispatch coarsely.

## Method

1. Start from accepted intent, behavior, contracts, architecture, and design—not file counts.
2. Ensure shared semantic meanings are settled enough that independent agents cannot reasonably implement incompatible behavior. Route missing **user-owned** meaning back to the appropriate authority rather than guessing.
3. Group work by coherent capability or module boundaries. Separate only where dependency order, responsibility, safety, verification, or independent execution benefits.
4. Make load-bearing shared interfaces, failure semantics, and invariants explicit before parallel implementation; reference their authoritative documents.
5. Keep independent work parallel when dependencies permit. Overlapping write surfaces demand coordination; do not assume the runtime provides file locks or an automatic merge mechanism.
6. Assign ownership of integration work, shared documentation updates, and cross-component verification. Do not leave these between tasks.
7. Prefer coherent module tasks over one-task-per-file decomposition; preserve the ability to integrate and test a real end-to-end outcome.
8. Treat accepted product/design/architecture documents as authority inputs. Do not let implementation tasks silently rewrite that authority; assign authorized documentation changes to the appropriate owner.

## Output to coordinating agent

For each candidate task or group, provide:
- intended observable outcome and acceptance;
- relevant authority references and agreed shared contracts;
- natural implementation/write scope;
- dependencies and parallelization assumptions;
- relevant skills and constraints;
- test/proof expectations;
- integration and shared-documentation owner.

The consuming planner or coordinating agent owns the actual task graph and dispatch. This skill prescribes no control plane or role.
