---
name: prototyping
description: Question-led design exploration through scenario walkthroughs, state sketches, behavioral pseudocode, comparative analysis, CLI transcripts, and rendered or interactive prototypes. Use when interaction, visual character, or capability decisions need evidence before commitment, or alternatives need comparison. Not for the final design contract (→ `design-specification`) or validating an actual implementation (→ `design-validation`).
metadata:
  version: "1.0.0"
---

# Prototyping

## What this skill is for

Prototyping is the practice of making design decisions concrete and testable at lower cost than full implementation. Its purpose is to *reduce uncertainty* — to move from "I think this will work" to "I have evidence this works (or doesn't)" before committing to a Design Spec or to code.

A prototype is a tool for making decisions. It may be the requested deliverable, but its appearance or interactivity alone does not make it an implementation contract or a working product.

**Load this skill when:**
- Design decisions are genuinely unresolved and building the wrong thing is costly
- The interaction model is unclear — you don't yet know how the system should respond to user actions
- Two or more design approaches exist and you need to compare them against real scenarios before choosing
- A scenario walkthrough would reveal whether the design handles the user's goal — but the Design Spec hasn't been written yet
- A novel interaction pattern needs to be specified precisely enough to reveal ambiguity
- Visual character, composition, density, motion, or another sensory quality needs comparison through actual samples

**Do NOT load this skill when:**
- The design is already specified to a level sufficient for implementation — prototyping is for resolving uncertainty, not for creating deliverables from a resolved design
- You are evaluating an existing implementation (→ `design-validation`)
- You are ready to commit the resolved design into a handoff contract (→ `design-specification`)

**Boundary with `design-specification`:** A prototype explores a design question; the accepted Design Spec defines the implementation contract. Prototype when uncertainty warrants it, including while refining an existing design. Record resolved choices and remaining limits in the appropriate part of the spec; do not impose a whole-project prototype-before-spec stage.

**Boundary with `design-validation`:** Prototyping investigates a proposed concept or change, including changes to existing products. Design-validation evaluates the actual implementation against accepted intent. An interactive prototype remains a prototype unless its production capability has been established.

**Boundary with `experience-design`:** Experience-design produces scenarios. Prototyping uses those scenarios as test inputs to evaluate whether the proposed design handles them. Scenarios are the fuel; this skill defines how to use them.

---

## Why prototyping exists

Prototypes let a team explore, compare, and discard ideas without the commitment of full production implementation. The benefit depends on what uncertainty they resolve; a prototype without a consequential question can waste time as readily as code can.

Before making one, state the question, the observation that would inform the decision, and what this artifact cannot establish. For a small accepted correction, inspect the relevant states directly instead of creating an elaborate prototype.

**What prototypes expose:**
- **Gaps**: interactions the design has not specified ("what happens when the user presses Escape here?")
- **Contradictions**: two design decisions that conflict when applied to the same scenario
- **Dead ends**: flows with no exit, or states the user cannot leave
- **Over-complexity**: when the prototype becomes as complex as the implementation — a signal that the design needs simplification, not more specification

---

## Decision prototyping vs validation prototyping

Two useful purposes are decision exploration and evaluation. Choose methods based on the question and available evidence, not the practitioner's identity.

**Decision prototyping** — resolving a design question before it becomes speculation
- Purpose: compare approaches or work out interaction details before committing to the spec
- Evaluation question: "Which approach handles the important scenarios better, and what does each reveal about edge cases?"
- Completion criterion: the design question is answered with sufficient evidence to record it as a Design Decision
- Formats: comparative scenario analysis, behavioral pseudocode, state-transition sketches, rendered or interactive samples

**Validation prototyping** — simulating whether the design works for its intended user
- Purpose: test whether the design's interaction model works from a new-user perspective
- Evaluation question: "At each step, would a user trying to achieve this goal know what to do, and would the system's response confirm progress?"
- Completion criterion: the scenario is walked through step by step and gaps/contradictions are surfaced
- Formats: structured scenario walkthroughs using the four cognitive walkthrough questions
- Evidence boundary: A cognitive walkthrough is an expert prediction, not observed user behavior. Use actual participant observations or recordings when available and identify their source and limits. An agent acting as a user or clicking through a prototype does not establish learnability for the intended population.

---

## The fidelity spectrum

Fidelity describes how closely the prototype matches the final design. The right fidelity is the **minimum needed to answer the design question** — not the maximum the designer can produce.

Choose fidelity independently for each relevant dimension; these are working distinctions, not required stages:

| Dimension | Low fidelity | Medium fidelity | High fidelity |
|---|---|---|---|
| **Visual or sensory detail** | Rough composition or dialogue sketch | Selected type, color, density, or voice samples | Closely rendered appearance, motion, or audio for the question |
| **Interactivity** | Static states or narrated response | Key transitions simulated or executable | Realistic interaction for the tested journey |
| **Content** | Minimal labeled examples | Representative content and lengths | Realistic varied data needed for the decision |
| **Coverage** | One decisive scenario | Relevant success, failure, and recovery cases | Broader journeys where the question warrants them |
| **Implementation realism** | Proposed behavior only | Explicitly simulated dependencies | Verified integration for the tested slice |

**Match the artifact to the uncertainty:** Use a rough sketch to compare composition, a transcript to inspect command semantics, an interactive slice to investigate feedback timing, or a carefully rendered view to compare visual character. Look and feel can be investigated early when they are load-bearing; unresolved interaction decisions do not forbid visual exploration. Conversely, polished visuals add little evidence to a question about cancellation or persisted state.

Use representative content when judging density, labels, composition, or tone. Limit investment to the part being investigated and remain willing to discard it. Higher visual fidelity does not imply broader behavior coverage, production readiness, or verified usability.

---

## The five prototyping formats

The five formats are arranged by use case, not sequence. Combine or adapt them to the available tools and the question; they are not a closed list of permitted tools or outputs.

### Format 1: Structured scenario walkthrough

The scenario walkthrough applies cognitive walkthrough questions (Flaherty, 2022) to a proposed journey. It can expose ambiguity and predict learnability problems; it is not equivalent to watching a participant use a prototype.

**When to use:** When you need to test whether the design handles a specific user goal end-to-end. Use for primary task flows, critical error paths, and scenarios that involve state changes.

**Structure:**

```
Scenario: [Brief name — who is doing what]
User context: [Who this user is, what they know, what they're trying to do]
Starting state: [What the user sees / has when the scenario begins]

Step [N]: [User goal at this step]
  User sees:    [What is visible or available at this point in the design]
  User does:    [The action the user takes]
  System responds: [What the interface does in response]
  State after:  [What the interface state is now]
  Design gaps:  [What this step reveals the design has not yet specified]
```

**Example (TUI file navigation):**

```
Scenario: Operator deletes a stale log file
User context: SRE using a TUI file manager; comfortable with keyboard navigation;
  has never seen a delete confirmation before in this tool.
Starting state: File list view, 'app.log.2024-01-01' is focused.

Step 1: User decides to delete the focused file
  User sees:    File list with 'app.log.2024-01-01' highlighted.
                Status bar shows: "j/k: navigate  Enter: open  ?:help  q:quit"
  User does:    Presses 'd' (guessing this is delete — it's a common convention)
  System responds: [DESIGN GAP: Delete key not in status bar — user may guess 'd',
                   'Delete', or give up. Design must decide: which key? Is it shown?]
  State after:  [Depends on resolution of gap above]
  Design gaps:  Delete affordance is not discoverable from the status bar alone.
                The design must specify: (a) which key triggers delete,
                (b) whether it appears in the status bar, (c) whether a confirmation
                dialog appears before deletion.

Step 2: [After gap is resolved] Confirmation dialog appears
  User sees:    Modal: "Delete 'app.log.2024-01-01'? [y/N]"
  User does:    Presses 'y'
  System responds: File is deleted; file list updates; focus moves to next item.
  State after:  File list view; the deleted file is absent; next file is focused.
  Design gaps:  What happens if the file list was sorted by modification date and
                'next item' is now a very different file? Is this the right focus behavior?
```

**The four cognitive walkthrough questions** — apply at each step to evaluate the design from a new user's perspective (Flaherty, 2022):

1. **Will the user try to achieve the right result?** — Does the design make the goal clear and the next action obvious?
2. **Will the user notice the correct action is available?** — Is the interactive element that achieves the step visible or findable?
3. **Will the user associate the action with the result?** — Will the user understand the label, key, or affordance?
4. **After acting, will the user see that progress was made?** — Does the system feedback confirm the action was correct?

A step that fails one of these questions is a design gap — not a user error.

---

**CLI surface: command transcript** — the scenario walkthrough for CLI takes the form of a command transcript. This is the most powerful CLI prototyping artifact: it shows exactly what the user types and what the tool outputs, making the design concrete before any code is written.

**When to use (CLI transcript):** When command input, output, recovery, or scripting semantics are uncertain. Show the relevant invocations and streams, then record accepted behavior in the spec. A short transcript can be precise; covering every invocation is unnecessary unless the question requires it.

**Structure:**

```
# [Scenario description: who is doing what, in what context]
$ [command the user types]
[output the tool produces — exactly as the user would see it]
$ echo $?
[exit code]

# [Next scenario or error path]
```

**For partial-effect or batch CLI workflows**, render the requested success, no-op/impossible-operation, interruption or mid-batch failure, and non-interactive/piped scenarios as *actual transcripts* rather than listing them as future work. Show command, relevant stdout/stderr, exit status, and resulting persisted state (or explicitly unknown state) for each. When a rollback or retry guarantee has not been accepted, show the design question instead of inventing its result. This is a risk-driven coverage rule, not a mandatory exhaustive matrix for every simple CLI.

**Example — package installation tool (primary flow + error paths):**

```
# User: install a package in a clean project
$ pkg install express
  Fetching express@4.18.2 from registry...
  Installing dependencies (12 packages)...
✓ express@4.18.2 installed in 2.3s

$ echo $?
0

# User: install a package in silent mode (CI context)
$ pkg install express --quiet
$ echo $?
0

# User: install a non-existent package
$ pkg install does-not-exist
error: package 'does-not-exist' not found in registry
  Did you mean: does-not-exist-lib?

$ echo $?
1

# User: install when a required peer dependency is missing
$ pkg install react-dom
warning: react-dom@18.2.0 requires react@^18.0.0 (not installed)
  Install react first: pkg install react
error: dependency 'react' not satisfied

$ echo $?
2

# User: try to install when network is unavailable
$ pkg install express
error: cannot reach registry — check network connectivity
  Last successful registry contact: 2 hours ago

$ echo $?
3
```

**What the transcript reveals:**
- Whether automation needs distinct exit codes for different failure modes, or a shared non-zero code with structured diagnostics is sufficient for callers
- Whether the output is correctly split between stdout (data) and stderr (diagnostics) — the transcript makes this ambiguous until the spec is explicit
- Whether error messages are constructive (suggestion for typo, actionable resolution for dependency failure)
- Whether `--quiet` suppresses ALL output, or just progress output (the transcript above leaves this a design gap: does the final confirmation line appear in quiet mode?)
- Whether the progress indicators are TTY-only (would they corrupt a piped consumer?)

**Flag interaction matrix** — for complex flag combinations, prototype as a table rather than a transcript:

| Flag combination | Expected behavior | Exit code |
|---|---|---|
| `install <pkg>` | Install at latest compatible version | 0 success, 1 not-found, 2 dep-conflict, 3 network |
| `install <pkg> --quiet` | Install, no stdout output | Same codes |
| `install <pkg> --dry-run` | Show what would be installed, don't install | 0 always |
| `install <pkg> --exact` | Install at exact version, fail if unavailable | 0, 1, 3 |
| `install <pkg> --force` | Install even if dep conflicts exist | 0 or 3 |

**Design gaps the flag matrix typically reveals:** Does `--quiet --dry-run` produce any output? Does `--force` suppress the dependency warning entirely or still print it to stderr? The matrix forces these to be answered before coding begins.

---

---

### Format 2: State-transition sketch

The state-transition sketch makes relevant states explicit, with transitions labeled by trigger and feedback. It can reveal missing states and impossible transitions; its coverage must still be inspected.

**Two manifestations:**
- **TUI terminal state sketch** — character-cell sketch or rendered terminal sample of key states with labeled regions and key bindings (see below)
- **Component state-transition diagram** — textual enumeration of all states a component passes through, with entry conditions, exit conditions, and transitions

**When to use:** When the design question is "what states does this screen or component have, and how does it transition between them?" Use for interactive components with multiple states (forms, modals, search, async operations) and for TUI navigation design.

**TUI terminal state sketch** — use character-cell sketches or actual terminal renderings as available. Sketches support structure and state reasoning; check cell width, clipping, contrast, resize behavior, and terminal interaction in an actual rendering or runtime when those are the question.

**When to use (TUI sketches):** When designing TUI layout, navigation, or state transitions. Investigate structure, visible state, key bindings, and interaction details together where they constrain one another.

**Structure:**

```
[State name: brief description of when this state occurs]

┌─ [Title bar / app name] ──────────────────────────────────────┐
│ [Menu bar or navigation hints]                                 │
├────────────────────────────────────────────────────────────────┤
│ [REGION NAME]     │ [REGION NAME]                              │
│ [content]         │ [content]                                  │
│                   │                                            │
├────────────────────────────────────────────────────────────────┤
│ [Status bar: mode indicator, key hints, system status]         │
└────────────────────────────────────────────────────────────────┘
[State label: current mode, what triggered this state, focus location]
```

**Example — system metrics TUI, three key states:**

```
[State: list-view — initial state, no panel selected]

┌─ sysmon v1.0 ──────────────────────────────────────────────────┐
│ Processes   Memory   Disk   Network                            │
├───────────────────────┬────────────────────────────────────────┤
│ PROCESS LIST          │ DETAIL PANEL                           │
│ > nginx (PID 1234)    │ [empty — no process selected]          │
│   postgres (PID 5678) │                                        │
│   redis (PID 9012)    │ Press Enter to view process detail     │
│   ...                 │                                        │
├───────────────────────┴────────────────────────────────────────┤
│ j/k:navigate  Enter:select  /: filter  q:quit  ?:help          │
└────────────────────────────────────────────────────────────────┘
[Focus: process list, first item]

[State: detail-view — user pressed Enter on a process]

┌─ sysmon v1.0 ──────────────────────────────────────────────────┐
│ Processes   Memory   Disk   Network                            │
├───────────────────────┬────────────────────────────────────────┤
│ PROCESS LIST          │ nginx (PID 1234)                       │
│ > nginx (PID 1234)    │ CPU:  2.1%   MEM: 45MB                 │
│   postgres (PID 5678) │ User: www-data                         │
│   redis (PID 9012)    │ Uptime: 14d 3h                         │
│                       │ Connections: 248                       │
├───────────────────────┴────────────────────────────────────────┤
│ Esc:back  k:kill  r:restart  Tab:switch-panel  q:quit          │
└────────────────────────────────────────────────────────────────┘
[Focus: detail panel; Tab moves focus to process list]

[State: kill-confirmation — user pressed 'k' in detail view]

┌─ sysmon v1.0 ──────────────────────────────────────────────────┐
│ Processes   Memory   Disk   Network                            │
├───────────────────────┬────────────────────────────────────────┤
│ PROCESS LIST          │ nginx (PID 1234)                       │
│ > nginx (PID 1234)    │ CPU:  2.1%   MEM: 45MB                 │
│   ...                 │                                        │
│          ┌─ Confirm ──────────────────────┐                    │
│          │ Kill process nginx (PID 1234)? │                    │
│          │ [Yes]  [No]                    │                    │
│          └────────────────────────────────┘                    │
├───────────────────────┴────────────────────────────────────────┤
│ Enter:confirm  Esc:cancel                                      │
└────────────────────────────────────────────────────────────────┘
[Focus: confirmation dialog, 'No' default; Esc returns to detail-view]
```

**Artifact completeness:** Draw every state that the prototyping request explicitly asks to compare; do not replace a requested screen with "the other state would look similar." Label active region, focus, key bindings, entry/exit transitions, and changes to populated/empty panels. A key binding map must cover requested recovery and clearing actions (for example, clearing a namespace filter) as well as navigation; mark undecided behavior as a concrete design gap.

**What the state sketch reveals:**
- Whether all key states are accounted for (what happens when the process list is empty? When filtering returns no results?)
- Whether the key binding map is consistent across states (does `q` always quit, or does it sometimes go back?)
- Whether focus is specified for each state transition (where does focus go when the confirmation dialog is dismissed?)
- Whether the status bar message is complete and up-to-date for each state

**Key binding map** — after sketching states, produce a key binding map to catch conflicts:

| Key | State: list-view | State: detail-view | State: confirmation |
|---|---|---|---|
| j / ↓ | Move down in list | Scroll detail panel | — |
| k / ↑ | Move up in list | Scroll detail panel | — |
| Enter | Open detail view | [no action] | Confirm |
| Esc | — | Return to list | Cancel |
| Tab | — | Switch focus to list | — |
| k | — | Kill process | — |
| q | Quit | Quit | — |
| ? | Help | Help | — |

**Design gap revealed:** `k` means both "move up" (in vi key bindings, j/k navigation) and "kill process" (in detail view). The table makes this visible — the same key has two different meanings depending on state. Is this intentional? Does the status bar make this clear?

---

**Component state-transition diagram** — for components with complex state models:

**Structure:**

```
Component: [Name]

States:
  [state-name]: [what this state looks like / what the user perceives]
    Entry: [what causes entry into this state]
    User can: [what actions are available in this state]
    Exits to: [state → trigger]

Transitions:
  [state-A] → [state-B]: [trigger] → [system action + user feedback]
```

**Example — form with async validation:**

```
Component: Username registration field

States:
  empty: Input field, placeholder "Choose a username", no indicator.
    Entry: Initial page load; user clears the field.
    User can: Type in the field.
    Exits to: typing → user types

  typing: Input shows typed text, no validation indicator yet.
    Entry: User types at least one character.
    User can: Continue typing; tab/click away; submit.
    Exits to: validating → user pauses (300ms debounce); field-blurred → user tabs away

  validating: Input shows typed text + loading spinner. Submit button disabled.
    Entry: User pauses for 300ms OR tabs away while typing.
    User can: Continue typing (cancels current validation, restarts debounce).
    Exits to: available → server says username is free
               taken → server says username is taken
               error → server is unreachable

  available: Input shows typed text + green check icon. Submit button enabled.
    Entry: Server validates username as free.
    User can: Submit form; continue editing.
    Exits to: typing → user edits; submitted → user submits

  taken: Input shows typed text + red X icon. Error: "Username taken. Try: username42"
    Entry: Server confirms username is already registered.
    User can: Edit the username; take the suggestion.
    Exits to: typing → user edits; typing → user clicks suggestion (fills field)

  error: Input shows typed text + warning icon. "Couldn't verify — try again."
    Entry: Server is unreachable or returns 5xx.
    User can: Submit anyway (optimistic) or wait and retry.
    Exits to: typing → user edits; submitted → user submits despite error

Transitions:
  empty → typing: first keystroke → no feedback (too early to validate)
  typing → validating: 300ms pause after last keystroke → loading spinner appears,
    submit button disables
  validating → available: server 200 "free" → spinner replaced by ✓, submit enables
  validating → taken: server 200 "taken" → spinner replaced by ✗, error message appears
  validating → error: server 4xx/5xx or timeout → warning icon, retry message
  taken → typing: user edits → indicator clears (wait for next debounce)
  available → typing: user edits → ✓ clears immediately (don't show stale green)

Design gaps revealed:
  - What happens when 'validating' → user types faster than the debounce? Specify:
    each new keystroke restarts the 300ms timer; the in-flight request is canceled.
  - 'error' state allows submit — what does the server do with an unvalidated username?
    Spec must decide: server validates at submit regardless; client-side is advisory.
  - Suggestion in 'taken' state: is "Try: username42" a clickable link that fills
    the field, or decorative text? Spec must be explicit.
```

---

---

### Format 3: Behavioral pseudocode

For novel or complex interaction patterns, behavioral pseudocode makes the interaction logic explicit at a level that reveals ambiguity — without being implementation code.

**When to use:** When prose cannot fully specify a complex interaction because the logic has branches, conditions, or sequences that are genuinely ambiguous unless made explicit. Not for simple interactions that prose handles well.

**Structure:**

```
On [trigger] in [context/state]:
  If [condition]:
    [system action]
    [user-visible feedback]
  Else if [other condition]:
    [system action]
    [user-visible feedback]
  Else:
    [fallback behavior]
    [user-visible feedback]
```

**Example — modal close behavior:**

```
On key press Escape in modal-open state:
  If form has unsaved changes (any field differs from persisted value):
    Show confirmation dialog: "Discard changes? [Discard] [Keep Editing]"
    If user selects Discard:
      Close modal, discard form state, return focus to trigger element
    If user selects Keep Editing:
      Close confirmation dialog, return focus to first changed field in form
    If user presses Escape again (while confirmation is open):
      Treat as Keep Editing — do not close the modal
  Else (form is clean — no unsaved changes):
    Close modal immediately, return focus to trigger element

On modal close (by any trigger — Escape, X button, Discard confirmation):
  Ensure: focus returns to the element that triggered modal open
  Ensure: body scroll is re-enabled (if it was locked on modal open)
  Ensure: modal is removed from the accessibility tree (aria-hidden or removed from DOM)
```

**What behavioral pseudocode reveals:**
- The definition of "unsaved changes" must be specified — what constitutes a change? Initial value vs current value? Any touched field vs any field with a different value than persisted state?
- "Trigger element" must be tracked — the design must decide when to record the trigger (on open) and where to store it (in component state? global focus management?)
- The double-Escape case reveals ambiguity in the escape handling — the design must decide whether Escape in the confirmation dialog means "cancel the cancel" or "cancel the modal"

---

---

### Format 4: Comparative scenario analysis

When two or more design approaches exist, run the same scenario through each to reveal which handles the important cases more gracefully.

**When to use:** When a genuine design decision exists between two approaches with different trade-offs, and the decision should be grounded in how each approach handles real scenarios — not personal preference.

**Structure:**

```
Design question: [The decision being made]
Evaluation scenario: [The scenario used to compare approaches]

Approach A: [Name]
  Description: [Brief — what this approach is]
  Walkthrough: [How the scenario plays out]
  Strengths revealed: [What this approach handles well]
  Gaps revealed: [What this approach handles poorly or leaves unspecified]

Approach B: [Name]
  [Same structure]

Decision: [Which approach is recommended, and why — one or two sentences grounded in the scenario evidence]
Record as: [Design Decision in the spec — the chosen approach becomes a Design Decision with its rationale]
```

**Example — CLI help discovery approach:**

```
Design question: Should the CLI show contextual help on invalid input,
  or require the user to run --help explicitly?

Evaluation scenario: New user types 'deployctl deploy prod' (missing required
  --service flag) as their first command.

Approach A: Silent error, user must run --help
  Description: Invalid invocations exit with error and tell the user to
    run --help for correct usage.
  Walkthrough:
    $ deployctl deploy prod
    error: missing required flag --service
    Run 'deployctl deploy --help' for usage.
    $ echo $?
    1
  Strengths revealed: Clean output; no unrequested text; scripting-friendly.
  Gaps revealed: New user receives no hint about what --service expects;
    the error message is terse; user may not know whether 'prod' was valid.

Approach B: Inline help on error
  Description: Invalid invocations show the relevant usage excerpt inline
    with the error message.
  Walkthrough:
    $ deployctl deploy prod
    error: missing required flag --service

    Usage: deployctl deploy --service <name> [--environment <env>] [--dry-run]

    Examples:
      deployctl deploy --service api --environment prod
      deployctl deploy --service api --service worker --environment staging

    $ echo $?
    1
  Strengths revealed: New user has enough context to retry without --help;
    the error + usage appear together.
  Gaps revealed: Output is verbose for scripted contexts; the usage text
    appears on every error even for experienced users who know the syntax.

Decision: Approach B for interactive contexts, Approach A for --quiet mode.
  The contextual usage excerpt is the right default: new users retry immediately
  without needing to run --help separately. Scripts using --quiet see only the
  terse error and exit code.
Record as: Design Decision — "Invalid CLI invocations display contextual usage
  excerpt by default; --quiet mode suppresses the usage excerpt and shows only
  the error message and exit code."
```

---

### Format 5: Rendered or sensory prototype

Use actual samples when the question concerns appearance, composition, density, motion, sound, or the feel of an interaction. Choose the available medium that can expose the issue: HTML/CSS in a browser, a native or mobile preview, rendered terminal states, or spoken dialogue samples. A browser rendering of a desktop concept can inform visual composition; it does not verify native behavior. A transcript can test voice sequencing and wording; it cannot establish acoustic clarity or timing.

**How to use it:** Name the intended character and the decision under review. Render a representative view or short journey with realistic content. For alternatives, keep the scenario, data, and viewing conditions comparable; vary the consequential design choices. Inspect the actual output rather than treating source code or a description of the intended result as visual evidence. Use relevant surface guidance and `visual-art-direction` for craft decisions.

**Choose and report the evidence level:**
- **Static sample:** Can inform hierarchy, typography, rhythm, color, density, composition, tone, and fit at the sampled size. It does not establish transitions, keyboard focus, responsiveness between samples, or task success.
- **Interactive prototype:** Can demonstrate the transitions and input behavior actually implemented and exercised. Mark simulated data and dependencies; it does not establish persistence, latency, synchronization, reliability, or production capability beyond the evidence available.
- **Real product observation:** Can establish observed behavior in the named build and environment. Use `design-validation` for implementation conformance; user-population claims still need appropriate user evidence.

Use the tools the host actually provides. No particular browser server, preview skill, design application, or simulator is mandatory. If rendering or audio is unavailable, provide the best usable artifact, identify what remains unassessed, and avoid claiming visual or sensory validation. Do not substitute a generated picture for exact interaction behavior or a functioning interface.

---

## Scenario walkthroughs as AI-usable validation

A scenario walkthrough applies the four cognitive walkthrough questions (Flaherty, 2022) systematically to a proposed journey. Use it for analytical inspection, alongside rendered, interactive, or participant evidence where the question needs those forms.

**What good scenario walkthroughs surface:**
- **Missing states**: steps where the design doesn't specify what the user sees or what happens
- **Undefined interactions**: steps where the user must do something but the design hasn't decided what that is
- **Forced paths**: places where the user has no recovery route — they're stuck
- **Invisible affordances**: steps where the correct action is not visible or findable from the design
- **Stale feedback**: steps where the system response doesn't confirm that the action was correct

**The procedure:**
1. Choose a specific user — their context, experience level, and goal (not "the user" in the abstract, but "a developer who has never used this tool before and is trying to deploy their first service")
2. Choose a specific task — the scenario walkthrough is for ONE task, not the entire system
3. Walk through step by step: for each step, fill in the five fields (user sees, user does, system responds, state after, design gaps)
4. Apply the four cognitive walkthrough questions at each step — don't skip steps that "seem obvious"
5. Record all gaps: steps where the design doesn't specify what happens are the primary output

**What scenario walkthroughs do NOT surface:**
- Whether the design actually meets real user needs (requires real users — this is the limitation of all expert review methods)
- Whether the visual appearance achieves its intent (inspect rendered samples; sketches alone do not establish finished appearance)
- Whether the interaction is fast enough for expert users who have learned it (requires observation over time)

Record missing signals as open questions with the evidence needed to resolve them. Seek that evidence before commitment when the risk warrants it; do not automatically defer a decisive user or visual question until after implementation.

---

## Prototype-to-spec transition

A prototype is "done" when it has answered the design questions it was created to answer — not when it is complete, detailed, or polished.

**Readiness check:** For the investigated slice, check relevant states, actions, transitions, visual or sensory decisions, and unresolved assumptions. Prefer recording answered questions in the Design Spec over creating another prototype. Repeat only for a named uncertainty that another scenario, rendering, or experiment can reduce.

**When to transition:**
- The specific question has enough evidence for an accepted decision, including its limits
- The affected behavior and visual intent can be recorded without inventing decisions hidden in the prototype
- Material unresolved questions are assigned an appropriate next check rather than presented as settled
- The existing spec can be updated proportionally; a bounded change does not require a new whole-product document

**How to transition:**

Each prototype artifact maps to elements in the Design Spec (see `design-specification` skill):

| Prototype artifact | Becomes in the Design Spec |
|---|---|
| Scenario walkthrough | Scenarios (Experience context) + User/task flows |
| CLI command transcript | Command invocations (Behavioral specification), Exit states, Output format |
| Terminal state sketch | Views, Regions, States (Behavioral specification), Layout constraints |
| Key binding map | Focus behavior, Interaction/actions (Behavioral specification) |
| State-transition sketch | States + Transitions (States and interactions) |
| Behavioral pseudocode | Interactions/actions with conditional logic (Behavioral specification) |
| Rendered or sensory sample | Accepted visual or sensory intent, references, representative states, and evidence limits |
| Design gaps discovered | Open design questions |
| Design decisions made | Design decisions |

The Design Spec is the implementation contract. Prototype artifacts inform it and may accompany it. Do not promote prototype code to production merely because it looks complete; production readiness requires the appropriate engineering work and verification.

**Prototype limbo anti-pattern:** The failure pattern where a prototype is refined indefinitely instead of transitioning to a spec. Signs: the prototype is growing in detail, not in answered questions. No design questions remain open, but the prototype "isn't ready yet." Fix: the prototype is ready when its questions are answered, not when it is finished.

---

## Fidelity selection guidance

| If the design question is about... | Use | Fidelity |
|---|---|---|
| Does this overall approach work at all? | Comparative scenario analysis | Low |
| What is the basic command structure? | CLI command transcript (primary flow only) | Low |
| What states does this screen have? | Terminal state sketch (key states only) | Low |
| Does the task flow work end-to-end? | Structured scenario walkthrough | Medium |
| Are the key bindings consistent and conflict-free? | Key binding map + state sketches | Medium |
| How does the CLI handle error cases? | CLI command transcript (primary + error paths) | Medium |
| What exactly happens at each transition? | State-transition sketch with full transition table | Medium |
| How does complex conditional logic work? | Behavioral pseudocode | Medium |
| Does this visual direction fit the intended experience? | Comparable rendered samples with representative content | Enough visual detail to judge the difference; behavior may remain simulated |
| Does an interaction or spoken response feel understandable? | Interactive slice or actual audio sample | Enough timing and input realism for the question |
| Is the affected interaction model specified? | Relevant walkthrough and states; pseudocode if needed | Coverage appropriate to the change |
| Am I ready to update the Design Spec? | Review evidence and remaining questions for the investigated slice | No fixed fidelity requirement |

---

## Anti-patterns

**1. Using the wrong evidence for the question**
Judging visual character from prose, or treating a polished screen as proof of usable behavior. Fix: render when appearance matters, exercise interactions when behavior matters, and use actual user evidence for claims about users. Investigate these together when they constrain each other; do not force visual exploration to wait for every interaction decision.

**2. Treating the prototype as the implementation contract**
Handing over an exploratory artifact while leaving consequential choices or simulated capabilities implicit. Fix: record accepted behavior, visual intent, and evidence limits in the Design Spec. A prototype can accompany that contract or be the requested exploration deliverable; it does not silently resolve its own gaps.

**3. Happy-path-only scenarios**
Walking through only the success case (valid input, all systems up, no prior state). Fix: for every success-path walkthrough, add at least one error-path walkthrough (invalid input, system unavailable, prior failed state). Error paths reveal more design gaps than success paths.

**4. Investment beyond the question**
Refining unrelated details or completing every state before comparing an uncertain approach. Fix: the question drives fidelity and coverage. If two-panel versus single-panel navigation is unresolved, make comparable slices sufficient to judge that difference rather than fully building only one.

**5. Prototyping without a design question**
"Let's prototype the onboarding flow" without naming what question the prototype will answer. Fix: before starting, complete this sentence: "This prototype will tell us whether [design decision] by showing us [observable evidence]."

**6. Skipping "obvious" steps in scenario walkthroughs**
The step that seems obvious to the designer who has been thinking about it for days is the step that reveals the most gaps — because that's where the designer's assumptions are invisible. Apply the four cognitive walkthrough questions at every step, especially the "obvious" ones.

**7. Treating one tool's absence as a blocker, or inventing tool access**
Use an available format that produces useful evidence and state what remains unknown. A transcript can expose command contracts without a GUI; a state sketch can expose missing transitions without a simulator. Where the question needs actual rendering, interaction, or audio, name that limit instead of claiming a textual substitute verified it. Use richer tools when available and appropriate.

---

## Sources

- [Houde, S. and Hill, C. (1997), What Do Prototypes Prototype?](https://hci.stanford.edu/courses/cs294h/2006/readings/houde-prototypes-97.pdf) — choose prototypes by questions about role, look and feel, and implementation; detail is not completeness.
- [GOV.UK Service Manual, Making prototypes](https://www.gov.uk/service-manual/design/making-prototypes) — choose appropriate fidelity, compare and discard ideas, and distinguish prototype code from production readiness.
- Nielsen, J. (2003). "Paper Prototyping: Getting User Data Before You Code." Nielsen Norman Group. [nngroup.com/articles/paper-prototyping/] — early exploration and feedback; no universal cost multiplier is assumed here.
- Pernice, K. (2016). "UX Prototypes: Low Fidelity vs. High Fidelity." Nielsen Norman Group. [nngroup.com/articles/ux-prototype-hi-lo-fidelity/] — fidelity dimensions (interactivity, visuals, content); designer attachment anti-pattern.
- Flaherty, K. (2022). "Evaluate Interface Learnability with Cognitive Walkthroughs." Nielsen Norman Group. [nngroup.com/articles/cognitive-walkthroughs/] — the four cognitive walkthrough questions; learnability evaluation method.
- Gothelf, J. & Seiden, J. (2021). *Lean UX* (3rd ed.). — decision prototyping concept; minimum viable prototype principle. [partially verified]
- Carroll, J.M. (1995). *Scenario-Based Design*. — scenarios as design hypotheses evaluable through structured analysis. [partially verified]
- The evidence distinctions and surface examples here adapt those principles to available host tools; they do not establish empirical effectiveness across every surface.

---
