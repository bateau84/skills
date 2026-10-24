---
name: github-issue
description: Turn chat discussions, ideas, action points, bugs, plans, and handoff notes into self-contained GitHub issues a new agent can act on without the original conversation. Use when asked to draft, write, file, create, or improve an issue or backlog ticket. Not for a standalone cross-component contract (use feature-handoff) or detailed task decomposition (use work-decomposition).
---

# GitHub Issue

Convert relevant conversation context into a **durable work request**, not a chat summary. A competent agent opening the issue in a fresh session should understand the outcome, boundaries, and proof of completion well enough to proceed with the repository's normal discovery, planning, implementation, and review practices.

An issue preserves the user's decisions; it does not grant new authority, approve tentative ideas, or dictate an execution workflow.

## Select the right artifact

- **GitHub issue:** a durable item of work or investigation for a repository, whether it began as an idea, bug, request, decision, plan, or action point.
- **`feature-handoff`:** a portable contract for functionality another component must provide. When that handoff needs tracking in GitHub, use its established requirements as input to this skill; do not replace the contract with a vague issue or paste raw YAML without explaining the intended outcome.
- **`work-decomposition`:** optional help identifying coherent units and dependencies when one conversation contains several independent outcomes. The GitHub issue is not a substitute for a detailed delivery plan.

An idea can be captured before it is ready to implement. Do not call it implementation-ready when the owner has not decided what the outcome should mean.

## Method

1. **Identify the request and target.** Determine what the user wants captured and which repository owns it. A referenced repository is not necessarily the target. Verify the target from context or repository evidence. If it is unresolved, prepare a draft and say where publication is blocked.
2. **Reconstruct the actual decisions.** Extract the latest accepted outcomes, constraints, exclusions, priorities, and known facts. Distinguish user decisions from agent suggestions, exploratory examples, hypotheses, and rejected or superseded ideas. Later explicit decisions take precedence over earlier speculation. Preserve meaningful conflict as an open decision; do not resolve it by invention.
3. **Ground the issue in the current project.** When accessible, inspect relevant repository instructions, documents, code boundaries, existing issues and PRs. Verify names, paths, current behavior and duplicate work before claiming them. If current reality differs from the conversation, describe the discrepancy; do not assert that the old observation is still true. Do not turn unverified paths or guessed root causes into facts.
4. **Choose a coherent issue boundary.** Prefer one outcome that a new agent can understand, deliver, and verify. Split unrelated work only when it has genuinely independent outcomes or ownership, not into one issue per file or conversation bullet. Keep prerequisites and integration responsibility visible. Do not create a swarm of issues just because many ideas appeared in chat.
5. **Decide what kind of work is actually ready.**
   - **Implementable:** intended behavior, scope, constraints and observable success are sufficiently settled; ordinary technical discovery remains for the implementing agent.
   - **Investigation:** the problem or desired improvement is real enough to examine, but evidence, cause, or feasibility is missing. Acceptance is a bounded, useful finding or recommendation, not an unapproved fix.
   - **Decision/proposal:** a user-owned product or policy choice is still open. Capture the decision needed and options already discussed; do not silently choose one and assign implementation.
   Use the repository's existing issue types and labels if appropriate. Do not invent a new required state machine or treat a label as proof of readiness.
6. **Write for independent execution.** State the problem/need and why it matters; the desired observable outcome; relevant current behavior and reproduction when known; in/out scope; accepted constraints and non-goals; acceptance criteria; prerequisites and durable references. Include only implementation details already decided or necessary to understand a real interface. Summarize accepted plans at the outcome/constraint level or link durable plan artifacts; leave fresh execution planning to the receiving agent.
7. **Preserve evidence and uncertainty honestly.** Distinguish observed behavior from suspected cause, accepted contract from suggested design, and confirmed facts from information to verify. Record unresolved questions with the decision owner or investigation needed. If an open question changes the required outcome, mark the issue as not yet implementable instead of burying it under acceptance criteria.
8. **Protect information.** Before putting anything in a potentially public issue, remove secrets, tokens, private URLs, credentials, sensitive logs, and personal data. Check repository visibility and the intended audience. Never assume that a private chat, session artifact, internal file or linked document is accessible to another agent; include the necessary permitted facts in the issue itself.
9. **Run the cold-start test.** Read only the proposed issue, with no source chat. Could a fresh agent explain (a) why this exists, (b) what should change or be learned, (c) how to know it is complete, (d) what is out of scope or undecided, and (e) where to find its durable inputs? If not, repair the issue. A cold agent may inspect the repository; it must not need to recover the original conversation.
10. **Publish only when requested.** When the user asks to create or file an issue, use an available authorized GitHub integration. Check likely duplicates and relevant conventions first. Use only verified labels, projects, milestones, and assignees; don't assign people or set priorities without basis. When asked only to draft, return the proposed title and Markdown body without publishing. After publication, verify the saved title/body and return its actual URL. If publishing fails, state that clearly and provide the draft; never claim success from a prepared body.

## Default GitHub issue shape

Prefer natural Markdown, not a rigid YAML schema. Keep the issue as short as possible while preserving the handoff. Omit sections that add no information, and adapt headings to repository conventions.

```markdown
Title: <verb + outcome, or "Investigate/Decide..." if not ready>

## Outcome
<What becomes true or what question will be answered, and why it matters>

## Context
<Current behavior, observed evidence, and the minimum history needed>

## Scope
- In scope: <accepted work>
- Out of scope: <important exclusions, if any>

## Acceptance criteria
- [ ] <Observable outcome or bounded investigation result>
- [ ] <Relevant regression, integration, or documentation expectation>

## Constraints and decisions
<Established requirements, compatibility boundaries, and relevant decisions>

## Dependencies and references
<Accessible, useful repository paths, issue/PR links, specifications, or evidence>

## Open decisions
<Blocking choices and decision owners, only when relevant>
```

For a bug, add precise reproduction steps and expected/actual behavior **only when known**. For investigation, specify what evidence and decision it must deliver. For a proposal, avoid implementation acceptance criteria until scope is accepted. For a larger request, describe its top-level outcome and link real dependent issues; avoid duplicating their whole contents.

## Non-negotiable quality boundaries

- **No authority laundering:** "Could", "maybe" and examples are not MUST requirements. Record alternatives as alternatives. A conversational idea is not approval to change product behavior.
- **No fake precision:** Never invent commands, reproduction steps, line numbers, repository paths, root causes, owners, effort estimates, acceptance tests, or source citations.
- **No hidden transcript dependency:** "As discussed", "see our chat" or an inaccessible session link cannot be the only statement of a decision. Retain only context needed for this task, not an indiscriminate transcript dump.
- **No premature design:** Specify externally checkable success. Do not force a guessed architecture, file list, agent role, PR structure, phase schedule, or workflow where the repository has not decided it.
- **No duplicate or unapproved side effects:** Search related issues/PRs when possible. If work is already tracked or done, report that rather than silently creating a duplicate. Do not use issue creation as permission to implement the task or to modify unrelated resources.
- **No empty readiness claims:** If the goal is materially unsettled, author an investigation/decision issue or a draft with an explicit blocker. "Acceptance: implement the feature" is not independently actionable.

## Publication fallback

This skill works without `gh` or a GitHub connector. Produce a copy/paste-ready title and Markdown body, identify the target repository if known, and state any blockers. Do not imply that publication, issue assignment, testing, review or implementation has occurred.

Optional companion files in this directory provide separate conformance review and adversarial checks. They are not required approval stages.
