---
name: teach-me
description: >-
  Teach a subject interactively, one concept at a time, using first-contact
  definitions, grounded analogies, examples, and learner checkpoints. Use when
  asked "teach me about X", "help me understand X", "explain X like I'm
  learning", "teach-me: X", or "what is/how does X work" with clear learning
  intent; also for /pause, /resume, and /done in an active teaching session.
  Not for quick fact lookups or implementation requests without teaching intent.
---

# Teach Me

Adaptive, conversational tutoring. The goal is a correct mental model, not maximum coverage in one answer. Match the learner's prior knowledge and requested depth; do not assume that a technical user is either a beginner or an expert in the current topic.

This skill is a teaching method, not a new agent role or permission boundary. It requires no specific model, Researcher agent, memory service, command router, or external workflow.

## Enter tutor mode

Start when the user explicitly asks to learn, invokes `teach-me: <topic>`, or clearly wants an explanation built over several turns. A bare factual question may be answered directly; do not silently turn every "what is X?" into an ongoing lesson. If the user asks you to build, debug, or change something, honor the actual request rather than replacing it with a tutorial.

If the learner names multiple topics, start with the first prerequisite or the topic they prefer. Keep the remaining topics in view; do not claim they were taught. Follow an explicit request for a complete, single-response explanation instead of enforcing short-turn pacing against the learner's wishes.

## The teaching loop

1. **Define the requested topic first.** In plain language, say what it is and what problem it solves before introducing implementation details. For compound topics, define the whole before unpacking its parts.
2. **Make the idea concrete.** Prefer a short real-world analogy or example when it helps. State where an analogy stops being accurate; do not trade correctness for memorability. Skip contrived analogies when the learner asks for a technical explanation.
3. **Introduce prerequisites in context.** Define unfamiliar technical terms when first used, with a brief explanation anchored to something the learner already knows. Do not dump a glossary at the start, redefine established terms every turn, or explain terms the learner clearly already understands unless requested.
4. **Teach one central concept per turn by default.** Give the mechanism and one useful example or counterexample. Include necessary caveats to prevent a false rule; brevity is not a reason to teach something wrong.
5. **Stop at a meaningful checkpoint.** End with a question, micro-scenario, or invitation that lets the learner indicate understanding, confusion, or a preferred next step. Do not automatically teach the next topic or ask the same ritual question after every sentence.
6. **Adapt the next turn.** If the learner is confused, try a different explanation or smaller example. If they demonstrate understanding or request greater depth, advance. Respect "skip basics", "show code", "go deeper", "keep it short", and similar preferences.

A useful answer usually follows **definition → purpose → example/analogy → limitation when needed → checkpoint**. It is a guide, not a mandatory visible template.

### Example

Learner: `teach-me: mutex`

Tutor: "A **mutex** is a lock that lets only one task at a time enter a protected part of a program. Think of a shared bathroom key: whoever has the key can use the room; others wait until it is returned. In code, a mutex protects shared data from conflicting changes. The analogy does not promise who gets the key next. If two tasks both need to change the same counter, what could go wrong without the lock?"

Stop there. Only introduce other synchronization mechanisms if the learner asks or they become necessary.

## Accuracy and research

- For stable foundational concepts, explain from established knowledge when sufficient.
- For specific software versions, releases, RFCs, papers, or fast-changing behavior, verify consequential details with an available authoritative source (ideally primary documentation). Tool availability determines how; never assume a named Researcher role is installed.
- When verification is unavailable, say what remains uncertain instead of inventing version numbers, behavior, citations, or dates. Continue with a clearly labeled general explanation if useful.
- Distinguish a teaching analogy, simplified example, and production-safe instructions. For safety-sensitive operations, explain prerequisites, risks, and verification boundaries before presenting action steps. Do not execute changes merely because the user asked to be taught.
- If a learner's requested shortcut would create a materially false model, correct the misleading part briefly, then proceed at their requested depth.

## Session continuity and controls

Track session state only within context actually accessible in the conversation: the current topic, meaningful terms already introduced, learner preferences, and whether tutoring is paused. No memory write, external persistence, or fabricated cross-session recall is required. If earlier context is missing, say so and resume from what the learner supplies.

During an active teaching session, support these controls:

| Input | Behavior |
| --- | --- |
| `teach-me: <new topic>` | Begin a new topic; reset topic-specific term tracking, retain stated learner preferences where appropriate. |
| `/pause` or "pause the lesson" | Temporarily suspend the one-concept and first-contact pacing; answer subsequent questions normally while retaining the topic in available context. |
| `/resume` or "resume the lesson" | Resume the same topic and tutoring rhythm using the context still available. |
| `/done` or "end the lesson" | Exit tutor mode; do not carry the tutorial's pacing into unrelated tasks. |

Treat slash inputs as tutor controls only when they are directed to this active lesson and the host has not already reserved them for another command. Briefly acknowledge control changes. Do not claim to delete chat history, clear external state, or register global slash commands.

## Failure modes to avoid

- **Subtopic first:** launching into "memoization" before explaining the requested "compiler".
- **Jargon cascade:** explaining one unknown term using three more undefined ones.
- **Lecturing:** covering several concepts after the learner requested a paced lesson.
- **Analogy as fact:** implying that a bathroom-key mutex guarantees fairness or ordering.
- **False certainty:** guessing what a specific version or paper says rather than verifying.
- **Mode leakage:** continuing to impose tutor pacing after /done or in ordinary implementation work.
- **Condescending repetition:** re-explaining concepts the learner already demonstrated they know.
- **Phantom memory:** claiming a lesson was recalled or saved without accessible evidence.

## Related methods and source

Use `code-analysis` when teaching from a real codebase and `learning` when intentionally recording reusable, evidence-backed engineering lessons. Neither is required for a normal teaching session.

Adapted from `nrkno/mats-opencode-setup/skills/teach-me/SKILL.md` at commit `3f26d834d84e4f24e14366864a9319f81201e6cb` (before the October 2026 repository split). The original first-contact, one-concept, and pause/resume/done behaviors are retained; its mandatory named-agent and SynaBun dependencies are intentionally not ported.
