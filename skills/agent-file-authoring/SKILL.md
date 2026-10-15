---
name: agent-file-authoring
description: Author concise agent instructions and role charters. Use when changing agent prompts, scope, permissions, handoffs, evidence duties, or completion rules in any host's agent configuration. Not for reusable skill authoring (use skill-authoring).
---

# Agent File Authoring

Agent files are executable role charters. Keep them **small enough that the profession remains visible**.

## Authoring method

1. Read the host's instruction format, current project requirements, relevant evaluations, and existing permissions before editing. Do not assume a particular agent directory or runtime.
2. Define the role in this order:
   - **profession / authority** — what judgment this role owns;
   - **quality instincts** — what a strong practitioner notices and optimizes for;
   - **hard boundaries / execution contract** — what it may not decide or mutate, plus only the workflow mechanics the model must remember.
3. Prefer broad principles that transfer across repositories. Do not turn one incident, language, tool, or file layout into a universal directive.
4. Leave professional methods to the practitioner. When delegation is available and requested, handoffs should pass outcomes, constraints, scope, and evidence rather than prescribe ordinary specialist technique. A method belongs in the handoff only when an agreed requirement or host constraint fixes it.
5. Treat permissions and control-plane enforcement as the hard boundary. Do not restate mechanically enforced rules as long procedural checklists unless model behavior still depends on remembering the distinction.
6. Keep the charter about the role's profession. Cross-cutting mechanics shared across roles—report formats, learning bookkeeping, generic evidence procedure—belong in shared on-demand methodology or mechanical enforcement when available; keep only the trigger/ownership hook in the role charter. Do not copy a completion-report template, learning-record schema, or generic evidence checklist into the role when a shared mechanism already owns it.
7. When adding a rule, remove or merge superseded prose. Do not append a second policy layer that says the same thing differently.
8. Historical prompt wording is implementation, not authority. Before deleting a rule, identify the accepted behavior it served. If the behavior is still required, give it a **production home**: control-plane enforcement, the responsible agent charter, or a shared on-demand skill that the production role is instructed to load. Behavioral evals verify that production home; they never create or replace production behavior.
9. Preserve authority ownership. A role may notice outside its domain without gaining authority to decide or mutate there.
10. Keep permissions least-privilege. Where independent review is part of the workflow, keep it outcome-neutral and preserve its independence; do not make an author dictate the review verdict.
11. Use the host's existing state and tools where available. Do not invent a parallel workflow protocol or assume shared-state services exist.
12. Add or adapt realistic behavioral evals for changed **decisions and outcomes**, not required phrases. When moving an old rule to a new production home, name the decision/outcome regression the eval must still catch—for example known-incomplete completion, authority crossing, or coordinator method prescription. Include ordinary work as well as traps so the learned strategy is professional judgment, not universal refusal/escalation.
13. Do not weaken a realistic eval merely because the current model fails it.
14. Search for contradictory old wording, validate deterministic CI, and run the smallest relevant live eval set before merge.

A useful test: **would these instructions help an experienced human professional exercise judgment, or are they micromanaging the profession?**

Review guidance lives in `ASSESSMENT.md`; adversarial validation lives in `QA.md`. Keep these optional perspectives distinct from the authoring method.
