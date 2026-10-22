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
3. Prefer broad principles that transfer across repositories. Do not turn one incident, language, tool, or file layout into a universal directive. Use ordinary, consistent terms and explain necessary technical distinctions with examples.
4. Leave professional methods to the practitioner. Handoffs pass the goal, scope, decisions, evidence and remaining work through existing records or references, not ordinary specialist technique or whole conversations. A method belongs in the handoff only when an agreed requirement or host constraint fixes it.
5. Treat permissions and control-plane enforcement as the hard boundary. Do not restate mechanically enforced rules as long procedural checklists unless model behavior still depends on remembering the distinction.
6. Keep the charter about the role's profession. Shared report formats, learning bookkeeping and evidence procedures belong in on-demand methodology or existing tools; keep only the role's trigger and responsibility. Do not require a separate report file for every dispatch when one existing result can serve both the caller and the next specialist.
7. Replace or merge superseded rules; do not append a second policy layer. Read the resulting charter together with its selected skills and automatic host context. Resolve contradictions such as "always send earlier findings" alongside "form an independent opinion", or "keep working until done" alongside an oversized assignment. Use the same terms for goal, decision, evidence, remaining work and next step across the affected guidance.
8. Historical prompt wording is implementation, not authority. Before deleting a rule, identify the accepted behavior it served. If still required, give it a production home: enforcement, the responsible charter, or an on-demand skill the role actually loads. Evals verify that home; they do not replace production instructions.
9. Preserve authority ownership. A role may notice outside its domain without gaining authority to decide or mutate there. A handoff must not promote an assumption or reported pass into accepted authority.
10. Keep permissions least-privilege and reviews outcome-neutral. Separate an independent first assessment from a follow-up: the first forms observations from current artifacts and source evidence before earlier opinions, then reconciles unresolved findings before the final verdict. A follow-up uses the relevant prior findings from the start. Check automatic context, not just the dispatch text; starting fresh cannot erase opinions already supplied.
11. Use existing host state and tools where available. Prefer fresh sessions for new bounded work, while allowing same-task reuse when context remains useful. Repeated resumes without progress call for narrowing or a different approach, not an arbitrary count limit or automatic approval. Keep these choices with the caller, not a new workflow engine; do not assume an uninstalled context-control feature exists.
12. Add realistic behavioral evals for changed decisions and outcomes, not required phrases. Cover ordinary successful continuation as well as fresh dispatch, overgrown tasks, stale handoffs, known-incomplete work and authority crossing. Score actions and resulting artifacts, not just the final prose.
13. Do not weaken a realistic eval merely because the current model fails it.
14. Search for contradictory old wording, validate deterministic CI, and run the smallest relevant live eval set before merge. State explicitly which checks did not run.

A useful test: **would these instructions help an experienced human professional exercise judgment, or are they micromanaging the profession?**

Review guidance lives in `ASSESSMENT.md`; adversarial validation lives in `QA.md`. Keep these optional perspectives distinct from the authoring method. [Context-policy cases](evals/context-policy.json) test contradictory handoffs and oversimplified session rules; fixture existence is not a passing result.
