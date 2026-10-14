---
name: intent-grilling
description: Turn fuzzy product intent into an actionable product brief through one-question-at-a-time adversarial interviewing. Use when shaping an idea or pressure-testing scope and success criteria before execution.
---

# Intent Grilling

Use this skill when the user expresses a fuzzy product idea, asks to shape an idea, or wants to pressure-test product intent before autonomous execution.

The goal is shared understanding sufficient for a product brief, not exhaustive product design.

## Interview loop

1. Identify the highest-impact unresolved branch of product intent.
2. Before asking the user, determine whether the repository, current docs, prior accepted authority, or bounded research can answer it.
   - If yes, resolve it autonomously and record the evidence.
   - If no, ask the user.
3. Ask exactly **one** user question at a time.
4. Every user question includes:
   - the question;
   - your recommended answer;
   - one short reason for that recommendation.
5. Record the exact resolution before moving to the next branch.
6. Challenge contradictions, weak assumptions, hidden scope expansion, and premature implementation constraints.
7. Follow dependencies between decisions branch-by-branch. Do not dump a checklist of questions.
8. Stop interviewing when the brief can state all of these clearly:
   - Goal;
   - observable success / Acceptance Criteria;
   - v1 scope;
   - explicit Not This boundaries;
   - user-owned decisions/authority;
   - important product context;
   - no unresolved user-owned branch that would materially change those sections.

## Question discipline

Prefer questions about **what outcome the user wants**, not how to implement it.

Do not ask the user:
- which programming language to use;
- which database/library/framework to use;
- how to structure internal components;
- technical questions the agent can reasonably research later, unless the user has an explicit preference or constraint.

Do ask when the answer is genuinely user-owned, for example:
- which outcome matters more when goals conflict;
- what should or should not be in v1;
- subjective workflow/product preferences;
- whether a material guarantee may be weakened;
- whether a material risk is acceptable.

## Recommendations

Do not make the user invent every answer from scratch.

For each question, propose the answer you currently recommend based on known intent and explain the trade-off briefly.

The recommendation is not authority. The user's answer controls product intent.

## Product brief handoff

When the interview is ready:

1. Summarize the resolved goal, success criteria, scope, exclusions, constraints, and remaining uncertainty.
2. Use the project's existing brief format and location if a durable artifact is needed; otherwise present the brief inline.
3. Show the complete brief to the user and resolve material corrections. Do not assume acceptance of a new product direction.
4. Record the agreed decisions and continue with the requested work using available tools and local workflow conventions.

Do not add a routine "should I continue?" checkpoint once the user has agreed to the brief and requested execution.
