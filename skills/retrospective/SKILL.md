---
name: retrospective
description: Facilitate a retrospective (retro, sprint retro, lessons learned) after a milestone, sprint, incident response, or meaningful batch of engineering or agent work. Use to examine what worked, what was difficult, what to preserve, and what to try next. Not for deliverable acceptance, incident root-cause diagnosis, or memory cleanup alone.
---

# Retrospective

A retrospective examines **how work happened** so future work can benefit from the experience. It is not a pass/fail assessment of the deliverable, an incident investigation, a blame exercise, or a quota of process changes. **A useful retrospective may recommend no changes.** Treat successful practices as important evidence, not just background to failure analysis.

## When and what to review

Use after a meaningful milestone, sprint, difficult implementation, incident response, or representative batch of work; revisit at a useful cadence if work is ongoing. Do not require a retro after every task. Keep the window bounded and state whether the work actually finished; a stalled or partial effort can still be reflected on without declaring completion.

Establish the intended outcome, observed result, work in scope, participants, and any earlier improvement experiments due for follow-up. If the available work is too thin to support meaningful conclusions, offer a narrower conversation or defer the full retrospective rather than inventing patterns.

## Facilitate the reflection

1. **Gather an evidence-based timeline.** Use the records already available: conversations or sessions, plans, commits and PRs, test and CI outcomes, reviews, incident notes, action/task evidence, and relevant memory. Use telemetry only when present and helpful. Bound the search to relevant work; do not dump entire logs into context. Missing Loom, a memory service, or telemetry must not prevent a useful retrospective.
2. **Follow up on previous experiments first.** For each accepted experiment, distinguish implemented from merely agreed, then report observed benefit, no benefit, harm, inconclusive evidence, or no opportunity to try it. Compare measures only when their definitions and collection methods are comparable. Do not repeat a previously rejected change without new evidence.
3. **Ask what worked.** Identify helpful decisions, techniques, tools, collaboration, recovery, and unexpectedly effective approaches. Explain the enabling conditions and whether the success might transfer to another situation. Ask what should be protected from unnecessary change.
4. **Ask what was difficult.** Find friction, delays, rework, avoidable confusion, surprises, and unmet expectations. Include collaboration, handoffs, human experience, and tooling, not only technical failures. Give specific episodes rather than generic complaints.
5. **Understand, don't guess.** Distinguish observed events, participants' accounts, hypotheses, and confirmed causes. Check plausible alternatives and conflicting evidence. An agent reporting success, a green test, a review verdict, a skill load, or a correlated metric does not by itself prove a good user outcome or a causal explanation. Multiple accounts of the same event are not independent confirmation.
6. **Invite the people's perspective.** Share a provisional, balanced account and ask participants, especially the person receiving the work, what felt effective or painful and what the evidence missed. Incorporate corrections without erasing disagreements. If participation is unavailable, label the missing perspective; do not simulate it.
7. **Distil learning before proposing change.** Separate (a) successful practices worth repeating, (b) supported failure lessons, (c) unanswered questions worth investigating, and (d) possible improvements. Preserve both positive and negative experience, including the conditions under which a lesson applies. Do not turn a single episode into a universal rule.
8. **Choose experiments only when justified.** Suggest at most one or two small, reversible, high-value changes, with a reason, an observable next-retro check (quantitative or qualitative), and a responsible owner or decision-maker if known. Zero is valid. Present proposals for an appropriate decision; the retrospective itself does not authorize editing code, agents, skills, plugins, policies, or memories beyond the permissions already granted for the task.

Adapt facilitation depth to the amount of work and its significance. A short retrospective with one meaningful lesson is better than a ceremonial report with fabricated sections.

## Output and follow-through

Summarize succinctly, with source pointers where available:

- **Scope and outcome:** what was attempted and what is known about the result.
- **Previous experiments:** what was tried and whether it helped, harmed, or remains untested.
- **Keep doing:** effective practices, why they helped, and conditions for reuse.
- **Difficulties:** material friction and its effect, without assigning blame.
- **Learning and uncertainty:** supported causes or patterns versus hypotheses and missing perspectives.
- **Optional experiments:** zero to two candidate changes, their expected signal, and next check; identify what awaits a decision.
- **Follow-up:** how accepted experiments and preserved practices will be revisited.

Do not invent a required report path, agent hierarchy, cadence, metrics system, or approval workflow. If the user asks for a quick conversation rather than a document, use the same reasoning in a concise dialogue. A proposed change is not a completed change; pass accepted work to normal implementation and verification processes.

Use the sibling **learning** skill when a verified, reusable lesson deserves durable notes; use **synabun-memory** only when that integration is installed and relevant. A normal project document or other authorized store is enough. Retain source, date, applicability limits, and confidence; avoid secrets, raw transcripts, and routine session history. Zero new memories is valid. Revisit earlier experiments at the next meaningful retrospective, whether or not a memory service exists.
