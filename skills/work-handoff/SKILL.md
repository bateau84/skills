---
name: work-handoff
description: Turn chat decisions, ideas, plans, action points, bugs, faults, enhancements, investigations, and cross-component dependencies into a self-contained work assignment for a fresh agent or another system. Use when asked to hand off, package, transfer, or preserve work so a recipient without the original conversation can act on it. Not for GitHub issue tracking mechanics (use github-issue) or detailed execution planning (use work-decomposition).
---

# Work Handoff

Produce a **standalone work contract**, not a conversation summary. Someone arriving in a fresh session must understand what the work is, why it matters, what is already decided, what must remain true, and how to recognize a useful result. The recipient may need to investigate the actual codebase, but must not need the source chat to recover the intent.

A handoff can be pasted into another agent session, stored as a document, or published as a GitHub issue. **This skill owns the meaning; the destination does not change that meaning.** Use `github-issue` for publishing, relationships, metadata, and other GitHub-specific management. Neither skill creates permission to implement an unapproved idea.

## Make it clear to humans as well as agents

A person who took part in the discussion must be able to read the handoff and say **"Yes, that is what we agreed"** — or point to the exact statement that differs. A new agent must be able to carry out the same work without the chat. These are **two checks**, not a requirement for a new approval step.

- Start with a few plain sentences: what is happening now, what needs to change (or be investigated), and why. For non-trivial work, add one concrete example of the expected behavior or a failure worth preventing.
- Write like you are explaining the work to a capable teammate, not writing an academic paper. Use familiar words, short sentences, and descriptive headings. State who does what and what happens as a result. Avoid abstract nouns and unexplained internal shorthand when ordinary words would be clearer.
- State accepted decisions and important exclusions **in language the person can compare with the original discussion**. Show suggestions and open questions separately; don't hide a stronger interpretation in technical wording.
- Explain a necessary technical term briefly at first use. Keep exact commands, field names, error meanings, requirement levels, IDs, and conditions when they matter. Plain language must **not** change or weaken a real guarantee.
- Describe acceptance in observable terms a person can recognize. Test names, internal file paths, and links can support an acceptance check, but must not be the only explanation of what success means.
- Make the actual requirements and criteria readable, not just an introductory summary. If a section is hard to interpret, rewrite that section **in place**. Do not add a friendly overview while leaving conflicting or opaque requirements underneath.
- Be complete enough to preserve meaning, but do not paste a transcript, repeat the same rule in several sections, or add an explanation for every obvious term.

**Example (only when these facts were agreed):**

- Opaque: "Introduce structured status emission while preserving legacy invocation semantics."
- Clear: "Add `--json` to the `status` command so scripts can read the result. Running `status` without `--json` must still show the same text and use the same exit codes."

The second version tells a person what they will see **and** gives an agent a testable target. Use examples to explain agreed requirements, not to invent new ones.

## Scope and authority

- Preserve **accepted** intent, requirements, constraints, exclusions, and relevant decisions. A question, example, agent proposal, or convenient implementation is not automatically approved.
- Treat later explicit corrections as superseding earlier suggestions. Preserve unresolved contradictions as decisions, not as invented conclusions.
- Explain the required outcome before prescribing a mechanism. Include a required method or interface only when it was actually established.
- Distinguish observations, reported symptoms, hypotheses, and unverified repository claims. Do not invent root causes, reproduction steps, paths, sources, tests, or owners.
- Do not convert the handoff into a scheduler, fixed agent chain, task-by-file breakdown, or authorization to modify code. The recipient uses its normal project instructions and planning/review practices.
- An issue or another session may be the destination, not the source of authority. Publishing does not approve an undecided product choice.

## Method

1. **Identify the work and receiver.** Establish the outcome or bounded question and the repository, component, or responsibility that should address it, when known. A mentioned repository is not necessarily the target. Do not invent a target.
2. **Recover the final intent.** Extract the latest accepted decisions from the conversation and relevant accessible artifacts. Separate accepted requirements, optional ideas, rejected approaches, and unresolved questions. Keep only the history needed to explain consequential choices.
3. **Check the current reality where possible.** Consult relevant project files, specifications, issues/PRs, and observed evidence when accessible. Verify claimed behavior and whether the work is already complete. An old observation is not proof of the current state; mark unsupported details as unverified.
4. **Choose a useful work unit.** Keep one coherent responsibility and outcome per handoff. If there are truly independent outcomes or owners, prepare separate handoffs and explain their connection. Avoid one handoff per substep or file. Use `work-decomposition` when grouping is actually difficult.
5. **Make readiness truthful.**
   - **Implementation:** the desired outcome and governing constraints are agreed; routine engineering discovery and design can be left to the recipient.
   - **Investigation:** the problem or question is clear, but cause, impact, feasibility, or evidence still needs work. Acceptance is a bounded finding and recommendation, not an unapproved fix.
   - **Decision/proposal:** a user-owned scope, product meaning, or risk choice is open. State who should decide and what evidence/options are available; do not frame implementation as already approved.
6. **Capture the necessary context in plain language.** Describe what happens now, why the request exists, what was agreed, what must remain unchanged, relevant dependencies, and evidence. Start with the human-visible result; add technical details only where needed to implement or check it. Link durable accessible records; include essential facts when a future recipient cannot access a session link or private artifact. Do not paste the chat.
7. **Define completion at the right boundary.** Use falsifiable, observable acceptance criteria or a clear investigation/decision deliverable. For a feature or bug, cover relevant regression or interaction behavior; for a cross-component dependency, describe what the receiving side must expose to its consumer. Distinguish what remains to verify from what is already proven.
8. **Surface uncertainty without fabricating closure.** Separate routine implementing-agent choices from genuinely reserved product/architecture decisions. Identify blocking questions, affected owners, and immediate next step where necessary. Avoid turning optional detail into blocking ceremony.
9. **Run both reader tests.** First, compare the actual sentences and acceptance criteria with accepted user decisions: could a human involved in the discussion spot a misinterpretation, changed promise, missing exclusion, or unexplained term without decoding academic language? Then run the **cold-start test**: can an agent with only the handoff explain the goal, constraints, evidence, unanswered questions and success checks? Repair unclear sections in place without changing the agreed meaning. Then stop; do not execute the work unless separately requested.

## Default artifact

Use clear, compact Markdown unless the caller or destination requires another format. Omit optional sections that add no value. The headings are guidance, not a fixed schema.

~~~markdown
# <Short title that says what needs to happen>

**Work:** Implementation | Investigation | Decision/proposal
**For:** <Known repository, team, component or responsibility>

## What we want
<What should change or what question should be answered, and why it matters>

## Why this is needed
<What happens today, what we observed, and any important earlier decision>

## What we agreed
<Expected behavior and key limits; what must stay unchanged or is out of scope>
<Keep exact technical names and MUST/SHOULD/MAY levels where they matter>

## Done when
- <Result someone can observe, or a useful investigation/decision result>
- <Important regression or end-to-end check, when relevant>

## Related work and evidence
<Useful accessible specs, issues, PRs, examples or observations>

## Still to decide
<Only consequential unresolved choices and their owners>
~~~

A small change may need only objective, context, and acceptance. A complicated migration may need more constraints and evidence. Stable IDs (for example `REQ-001`, `AC-001`) are useful when requirements are already referenced; avoid numbering merely for formality.

### Domain-specific handoff

- **Bug/fault:** observed versus expected behavior, reproduction **if known**, affected environment, evidence, and a verification target. Separate a known defect from a possible diagnosis.
- **Adjustment/enhancement:** desired change plus what must **remain** compatible or unchanged.
- **Feature:** user-observable capability, scope, exclusions, and accepted success criteria.
- **Investigation:** the question, currently known facts, limits on evidence, and the decision or result to produce.
- **Plan/action points:** preserve accepted outcomes, dependencies, and sequencing constraints; don't turn the handoff into a second detailed execution plan.
- **Cross-component dependency:** clearly distinguish source need, target responsibility, externally observable contract, requirement strength, and required versus suggested interfaces. For a structured variant and example, read [Cross-component handoffs](references/cross-component.md).

## Output and delivery

When asked to *prepare a handoff*, output the artifact without a long preface. If asked to *create a GitHub issue*, use this skill to preserve the intended work, then `github-issue` to publish and organize it. The receiving agent must be able to read the issue alone. If GitHub tooling or target access is absent, provide a paste-ready artifact and be explicit that no issue was created. Do not assign, implement, or publish work based solely on the act of preparing a handoff.

Keep credentials, personal data, private customer context, and inaccessible source artifacts out of public destinations. A link alone is insufficient if the receiving agent has no access to the underlying source.
