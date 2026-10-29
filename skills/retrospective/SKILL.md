---
name: retrospective
description: Facilitate a retrospective (retro, coding-session retro, sprint retro, lessons learned) after a coding session, milestone, sprint, incident response, or meaningful batch of engineering or agent work. Use to examine what worked, what was difficult, what to preserve, and what to try next. Not for deliverable acceptance, incident root-cause diagnosis, or memory cleanup alone.
---

# Retrospective

A retrospective examines **how work happened** so future work can benefit from the experience. It is not a pass/fail assessment of the deliverable, an incident investigation, a blame exercise, or a quota of process changes. **A useful retrospective may recommend no changes.** Treat successful practices as important evidence, not just background to failure analysis. **There is only one method: an evidence-led deep retrospective.** It examines the original work rather than producing a summary-only alternative. Depth of conclusions must match evidence quality; missing host history is an explicit limit, not permission to treat the coordinator's account as proof.

## When and what to review

Use after a coding session, meaningful milestone, sprint, difficult implementation, incident response, or representative batch of work; revisit at a useful cadence if work is ongoing. **A single session is a valid scope**, including the current or unfinished session when requested. If the user gives no scope, start with the current session or the most clearly relevant work in context; do not invent a larger milestone. Do not require a retro after every task. Keep the window bounded and state whether the work actually finished.

Establish the intended outcome, observed result, work in scope, participants, and any earlier improvement experiments due for follow-up. If direct evidence is too thin to support meaningful conclusions, report an **incomplete deep retrospective**, naming unavailable sources and questions left unresolved. Do not invent a shorter retrospective tier or larger milestone.

## Facilitate the reflection

1. **Independently reconstruct the work.** Start from original sessions and relevant child-agent sessions when accessible, then corroborate with plans, commits/PRs, tests, CI, reviews, incident notes, task records and participants. Examine actual user requests/corrections, dispatched agents and original prompts, skill loads, tool calls/outcomes/retries, handoffs and final responses where recorded. Use bounded native traces or full session exports, following pages and relevant child-session links; do not dump entire transcripts into context. General's summary is a navigation aid, **not independent proof**. Prefer a separate investigator (the Researcher responsibility when available), but never require a named agent or one host. If full history is unavailable, state the exact coverage, compaction gaps and missing sources instead of calling the window complete.
2. **Follow up on previous experiments first.** For each accepted experiment, distinguish implemented from merely agreed, then report observed benefit, no benefit, harm, inconclusive evidence, or no opportunity to try it. Compare measures only when their definitions and collection methods are comparable. Do not repeat a previously rejected change without new evidence.
3. **Ask what worked.** Identify helpful decisions, techniques, tools, collaboration, recovery, and unexpectedly effective approaches. Explain the enabling conditions and whether the success might transfer to another situation. Ask what should be protected from unnecessary change.
4. **Ask what was difficult.** Find friction, delays, rework, avoidable confusion, surprises, and unmet expectations. Include collaboration, handoffs, human experience, and tooling, not only technical failures. Give specific episodes rather than generic complaints.
5. **Understand, don't guess.** Link material episodes to original session/message/tool-call IDs or other stable sources when available. Compare intent, dispatch prompt, actual tools/skills, agent response, verification and user experience before explaining friction. Distinguish observed events, participants' accounts, hypotheses, and confirmed causes. Check plausible alternatives and conflicting evidence. An agent reporting success, a green test, a review verdict, a skill load, or a correlated metric does not by itself prove a good user outcome or a causal explanation. Multiple accounts of the same event are not independent confirmation.
6. **Invite the people's perspective.** Share a provisional, balanced account and ask participants, especially the person receiving the work, what felt effective or painful and what the evidence missed. Incorporate corrections without erasing disagreements. If participation is unavailable, label the missing perspective; do not simulate it.
7. **Distil learning before proposing change.** Separate (a) successful practices worth repeating, (b) supported failure lessons, (c) unanswered questions worth investigating, and (d) possible improvements. Preserve both positive and negative experience, including the conditions under which a lesson applies. Do not turn a single episode into a universal rule.
8. **Choose experiments only when justified.** Suggest at most one or two small, reversible, high-value changes, with a reason, an observable next-retro check (quantitative or qualitative), and a responsible owner or decision-maker if known. Zero is valid. Present proposals for an appropriate decision; the retrospective itself does not authorize editing code, agents, skills, plugins, policies, or memories beyond the permissions already granted for the task.

Apply the same independent deep method to every requested scope; bound the search by relevant work rather than an arbitrary event count. When original history cannot be accessed, inspect what is available and report which claims remain unverified. Never call a summary-only handoff a completed retrospective. One well-grounded lesson is better than a ceremonial report with fabricated sections.

## Session evidence and privacy

Review event order, not just counts: which user decisions changed direction; why agents were chosen; what dispatch prompts actually required; whether skills loaded when needed and were applied; tool failures and retries; handoffs and independent verification; and relevant child sessions. Compare token/time costs only across comparable windows and task difficulty. A long investigation or failed call is not automatically waste. Identify gaps from missing history, compaction, inaccessible children and truncated output.

Access prompts and tool output only within the host's existing permissions and the user's authorized scope. Prefer short, redacted findings with source IDs over raw prompt/output copies. Do not persist secrets, private conversation dumps or complete transcripts in reports or memory. No new access rights, automatic capture, role mandate or surveillance are implied.

## Optional engineering-environment opportunities

**Only after exploring what worked and what was difficult**, use these prompts when a concrete episode suggests an opportunity. They are not a mandatory audit or a reason to manufacture improvements.

- **Navigation and information access:** If locating code, understanding dependencies, or obtaining logs or documentation was difficult, examine where discovery broke down. Would a small pointer to authoritative docs, clearer ownership, or appropriately scoped read-only access have helped? Prefer discoverable references over copying large documents into always-on prompts.
- **Automated checks before more instructions:** When a mechanical error escaped, inspect the repository's *existing* test, lint, type-check, build, hook, and CI commands first. Ask whether a useful check already exists but is skipped, unwired, misconfigured, or silently failing. Where reliable and proportionate, prefer deterministic checks for mechanically detectable mistakes; reserve reviewer guidance for judgments a check cannot make. Propose new checks only after examining existing coverage and maintenance cost. Absence of a particular check is not automatically a defect.
- **Instruction and context overhead:** When long steering files or repeated reminders seemed ineffective, examine redundant or non-actionable instructions. Consider brief navigation pointers or on-demand skills instead of expanding global prompts. Implementation and review may need different context, but do not impose one universal division of responsibility or remove essential rules without evidence.
- **Tool economy:** If repeated searches, tool failures, or high token/time costs materially affected the work, investigate the *reason*: poor discovery, missing information, redundant exploration, or an appropriate deep investigation. Tool-call counts and token usage alone do not establish waste; efficiency changes should not sacrifice correctness or necessary evidence.

Keep any supported environmental observation within the normal **keep doing**, **difficulties**, **learning**, or **optional experiments** sections. Do not silently edit checks, instructions, tools, or permissions as part of the retrospective.

## Output and follow-through

Summarize succinctly, with source pointers where available:

- **Scope, outcome and evidence coverage:** what was attempted, what is known, which original sessions and child sessions were examined, and where trace evidence is incomplete.
- **Previous experiments:** what was tried and whether it helped, harmed, or remains untested.
- **Keep doing:** effective practices, why they helped, and conditions for reuse.
- **Difficulties:** material friction and its effect, without assigning blame.
- **Learning and uncertainty:** supported causes or patterns versus hypotheses and missing perspectives.
- **Optional experiments:** zero to two candidate changes, their expected signal, and next check; identify what awaits a decision.
- **Follow-up:** how accepted experiments and preserved practices will be revisited.

Do not invent a required report path, agent hierarchy, cadence, metrics system, or approval workflow. If the user asks for a quick conversation rather than a document, use the same reasoning in a concise dialogue. A proposed change is not a completed change; pass accepted work to normal implementation and verification processes.

Use the sibling **learning** skill when a verified, reusable lesson deserves durable notes; use **synabun-memory** only when that integration is installed and relevant. A normal project document or other authorized store is enough. Retain source, date, applicability limits, and confidence; avoid secrets, raw transcripts, and routine session history. Zero new memories is valid. Revisit earlier experiments at the next meaningful retrospective, whether or not a memory service exists.
