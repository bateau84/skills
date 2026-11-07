---
name: technology-impact
description: "Assess a capability's purpose and wider consequences using Neil Postman's seven questions. Use when adopting technology or materially changing autonomy, permissions, billing, data retention, shared terminology, human workflows, or control over a system. Not a mandatory checklist for routine fixes or behavior-preserving refactors; use product-discovery for uncertain value and architectural-decision for technical selection."
---

# Technology Impact

A technically correct capability can solve the wrong problem, move work onto someone else, or quietly change who controls the system. Examine those consequences before committing dependent work. This is an engineering adaptation of Postman's questions, not a new approval gate, agent role, or permission to change accepted intent.

## Choose the useful depth

- **Routine, low-impact work:** skip a formal assessment when purpose and consequences are already understood. Do not require seven answers, a report, or a specialist dispatch for a local fix.
- **Material feature or workflow change:** establish the problem, beneficiary, and new burdens; use the other questions where they could change the decision.
- **Consequential change:** consider all seven questions for material changes to autonomy, authority, financial exposure, privacy/retention, security boundaries, shared meanings, or hard-to-reverse dependencies. Judge consequences, not diff size: a one-line permission/default change can qualify. A genuinely irrelevant dimension needs only a brief reason, not an invented risk.

Reuse an applicable accepted analysis. Revisit affected conclusions only when scope, evidence, assumptions, or operating conditions change. Uncertainty is not itself a reason to block unrelated work or restart discovery.

## Seven questions, translated into engineering work

| Question | What to inspect |
| --- | --- |
| **1. Which concrete problem needs solving?** | Current friction and evidence; the useful outcome rather than the proposed mechanism. Compare doing less, using the existing path, or a non-technical change when direction is open. |
| **2. Who needs that problem solved?** | Actual beneficiaries, their context, and whose convenience or incentives drive the proposal. Distinguish observed benefit from a hypothesis. |
| **3. Which new problems does the solution introduce?** | Failure modes, maintenance, cognitive load, dependencies, cost, migration and exit. Include burdens transferred rather than eliminated. |
| **4. Who bears the downside?** | Users, operators, maintainers, excluded users, affected third parties or institutions. A benefit to the sponsor does not establish a benefit to everyone. |
| **5. Which meanings change?** | Before/after promises behind terms such as complete, verified, available or autonomous. Trace changed meanings into contracts, interfaces, docs and tests; a rename cannot authorize a weaker guarantee. |
| **6. Who gains or loses power?** | Control over decisions, data, money and access; provider dependence, incentives and lock-in as well as runtime permissions. Who can inspect, contest, override, revoke or leave, under the accepted constraints? |
| **7. What other uses become possible?** | Plausible beneficial reuse, accidental misuse and adversarial repurposing, including combinations of individually harmless capabilities. Distinguish technical possibility from authorization. |

## Turn answers into decisions, not paperwork

1. **Ground the scope.** Read the accepted goal, constraints, current behavior and relevant prior decisions. Separate evidence, inference and unknowns. Do not invent user research or reopen fixed choices just to produce alternatives.
2. **Find decision-changing consequences.** Use the depth above. For each material concern, state the affected actor, causal path, consequence and supporting evidence or uncertainty. Neither seven reassuring answers nor an imagined catastrophe proves anything.
3. **Compare and dispose.** Keep, narrow, replace or defer a proposal within existing authority. Record whether a concern is addressed by an accepted constraint, needs a mitigation or evidence, requires an owner decision, is advisory, or is irrelevant with a reason. Acknowledgement alone does not resolve it. Optional hardening is not a new requirement; credible material failures under actual conditions still matter.
4. **Preserve ownership.** Product meaning and risk acceptance remain with their existing owners. Technical realization, human-facing design, requirements and delivery planning retain theirs. Route only the unresolved decision and pause only unsafe or dependent work. Do not implement a newly imagined use, weaken a guarantee, add permissions or accept financial exposure through this assessment.
5. **Carry the result into normal work.** Put material conclusions once in the existing Anchor, decision, design, plan, result or PR; link rather than copy. Carry accepted mitigations into an outcome, owner, dependency and observable check. Keep proposed obligations separate from accepted ones. Record residual uncertainty and a useful revisit condition when relevant. No separate Postman document or runtime schema is required.
6. **Verify the consequence that matters.** Test or inspect the actual affected boundary when authorized. For consequential work, have the existing independent review path challenge material conclusions and proof; the producer's checklist is not independent evidence. Use the assessment or QA companion for those perspectives. Where no independent reviewer is available, disclose self-review rather than claiming independence. Unrun checks remain unrun; a benefit hypothesis remains a hypothesis until observed.

Example: automatic provider fallback may reduce manual switching while changing who can spend money. A responsive endpoint does not establish that usage is included. Preserve the accepted billing constraint, identify the evidence needed at the real account/transport boundary, and route missing authorization to its owner rather than treating connectivity as permission.

## Composition and attribution

Strategic programming in `software-engineering` asks whether the implementation stays easy to change; this method asks whether the capability and its wider consequences are justified. Use `product-discovery` for uncertain value, `anchor-authoring` for agreed intent, architecture skills for realization, `ubiquitous-language` for terminology, and `work-decomposition` for accepted work. These are optional collaborators, not a required sequence or bundle.

Question themes follow Neil Postman's lecture *The Surrender of Culture to Technology*, as summarized by [Scott Berkun](https://scottberkun.com/2016/the-7-questions-for-any-technological-idea/), which links the lecture. The wording and engineering method here are adaptations, not verbatim quotations or a claim that Postman specified this workflow.

[Decision cases](evals/evals.json) are synthetic maintainer exercises, not executed results. They do not prove deployed skill discovery or agent behavior.
