---
name: work-decomposition
description: Find coherent implementation work boundaries and dependencies before creating a delivery plan. Use when agreed work admits several plausible task splits.
---

# Work Decomposition

Analyze finely; dispatch coarsely.

## Method

1. Start from accepted outcomes, obligations, architecture, and design—not files.
2. Group work by coherent capability/module boundary.
3. Separate work only when the boundary matters to dependency order, ownership, verification, safety, or independent execution.
4. Preserve integration work across meaningful seams.
5. Keep independently runnable work parallel when dependencies permit it. Bounded write scopes may overlap; treat overlap as a semantic-coordination signal, not an automatic reason to serialize, because runtime file locks serialize concrete mutations.
6. Prefer deep-module tasks over one-task-per-file decomposition.
7. Treat agreed design/architecture/requirements as inputs. Do not silently rewrite them during implementation; explicitly include decision updates in the task scope when needed.

## Output to Planner

For each candidate group provide:
- objective;
- natural write surface;
- dependencies;
- relevant skill names;
- verification expectations;
- integration/acceptance implications.

Use the resulting boundaries in the project's delivery plan. A dependency graph is useful when needed; no planner agent or orchestration system is required.
