---
name: design-validation
description: Evaluate the real implemented human-facing experience against accepted design, representative Scenarios, visual craft, accessibility, and usability evidence without silently redesigning it. Also use to review a proposed design before implementation for coherence, state coverage, visual intent, accessibility, and implementation-ready precision.
---

# Design Validation

Answer: **does the real implementation express the accepted design and allow the accepted journeys to succeed?**

Validation is evidence, not design authority. Do not revise accepted design merely to make implementation pass.

Load the smallest relevant surface skills when platform-specific interaction is materially under test, and load the implementation-focused `accessibility-implementation` skill when accessibility conformance is materially under test. Those skills provide specialist checks; this skill owns the evidence method and drift judgment.

## Method

1. **Establish the reference and observation boundary.** Read accepted Experience Design, relevant US/SC artifacts, and surface/accessibility decisions. Identify the exact build/version, environment, viewport/terminal/device/input mode, data/permissions, and other conditions actually observed.
2. **Observe the real product first.** Use the implemented surface, not a prototype/mock substitute. When direct interaction or rendered observation is unavailable, say which claims are limited to code/static inspection; do not convert inferred behavior into observed evidence.
3. **Walk representative Scenarios.** Exercise load-bearing human journeys end to end, including applicable loading, empty, validation/error, cancellation, interruption, recovery, focus, and degraded states—not only the photogenic happy path.
4. **Run spec-fidelity comparison.** For each load-bearing design assertion compare:
   ```text
   accepted design -> observed implementation -> user consequence
   ```
   Classify drift as:
   - **Behavioral** — response, state, error/recovery, transition;
   - **Structural** — IA, navigation, task sequence/context;
   - **Accessibility** — focus/input/semantics/announcements/contrast or accepted accessibility behavior;
   - **Visual** — hierarchy, semantic tokens, and accepted character/composition/type/density/imagery/motion intent.
5. **Do a second-pass usability attack.** Apply the relevant usability heuristics and a cognitive walkthrough to catch issues the design itself failed to anticipate. Keep these separate from spec deviations: they may indicate an upstream design gap rather than implementation drift.
6. **Judge severity by human consequence.** Consider task blockage, ambiguity, data/safety consequence, loss of control/recovery, trust, accessibility exclusion, frequency, and primary-journey impact—not pixel distance.
7. **Distinguish correction ownership.**
   - **Implementation drift:** accepted design is clear; the implementer can correct it.
   - **Design decision required:** design is ambiguous/wrong or a real constraint requires a new human-facing choice.
   - **Missing product/behavior/architecture capability:** report the gap to the responsible collaborator or user; do not fake it in validation.
8. **Record evidence limitations and negative space.** State untested scenarios, states, surfaces, input modes, environments, or observer-only checks. A PASS cannot claim more than was actually exercised.
9. **Match each claim to its evidence.** Rendered observation can support expert visual critique; direct interaction can support the behavior actually exercised. Actual focus, assistive-technology announcements, timing/animation, device ergonomics, user preference, and perceived emotional response need their corresponding observation or research. Do not require a human to perform every check that available tools can establish, or present an agent's judgment as representative-user evidence.
10. **When no accepted Design Spec exists**, heuristic/usability findings are not spec deviations. State that design intent cannot be traced and avoid retroactively inventing one.

## Finding shape

Every actionable finding should contain:

```text
Finding: <short title>
Drift: behavioral | structural | accessibility | visual | heuristic
Impact: cosmetic | minor | major | critical
Location: <where/how observed>
Accepted intent: <design/scenario reference, or heuristic when no spec>
Observed: <real implementation evidence>
User consequence: <what changes for the person>
Owner: implementation-fix | designer-decision | other-authority
Required correction/question: <next action>
```

An observation without accepted-intent traceability or user consequence is not automatically a defect.

## Review craft in the rendered experience

When visual quality is part of the accepted brief, compare the actual implementation with its visual intent and representative examples. Use `visual-art-direction` for contextual craft judgment and `visual-interface-design` for visual semantics. Inspect the whole composition before small details: attention order, grouping, rhythm, typography, density, color relationships, imagery, coherence, and applicable motion. Include the states and supported sizes that could materially change the conclusion, using realistic content.

Record concrete observations and their consequences. Distinguish:

- **Accepted visual intent violated:** actionable visual drift, even if the main task remains operable; cite the decision and observed difference.
- **Usability or accessibility defect:** report its own impact; attractive presentation cannot cancel it.
- **Craft opportunity:** a reasoned improvement when existing intent is ambiguous or the result could better serve it; route the design question without inventing an obligation.
- **Preference:** an alternative aesthetic with no established defect; do not turn it into a failing gate.

Compare static appearance from screenshots, motion from live interaction or recordings, terminal behavior from actual terminal evidence, and spoken pacing from audio/interaction. Code and tokens alone cannot establish rendered polish. A screenshot cannot establish keyboard operation, screen-reader behavior, task completion, or product capability. Name unavailable checks instead of fabricating an observation.

For a proposed innovative interaction, compare the observed outcome and learning/recovery cost with the stated baseline when such evidence exists. Keep benefit hypotheses separate from demonstrated improvements. Do not average serious task or accessibility defects away in a visual-quality score.

## Validation result

PASS only when the exercised accepted journeys and load-bearing design assertions conform within acceptable variation and no material required state remains unverified.

Accept minor implementation variation when it preserves task completion, meaning, accessibility, and accepted design intent. Do not fail on harmless pixel differences. When conformance passes but aesthetic response or innovation benefit remains untested, state those limits separately; conformance does not prove excellence.

A scenario blocked by a missing/mock product capability is evidence that the intended experience does not exist; it cannot pass through a prototype substitute.

## Before implementation: reviewing a proposed design

Review the design itself before implementation.

Check for:

- clear user goal and task flow;
- complete material states: default, loading, empty, error, success, disabled/recovery as applicable;
- visible system status and recoverability;
- keyboard/focus/accessibility behavior;
- responsive or surface-specific constraints;
- honest content: no fabricated metrics, testimonials, capabilities, or guarantees;
- consistent hierarchy and interaction grammar;
- an explicit, context-appropriate visual direction where visual quality is in scope, with enough examples and craft decisions to preserve it;
- a credible benefit hypothesis and baseline for consequential novelty, without presenting proposed functionality as accepted capability;
- no accidental technical-realization decisions outside Designer authority;
- enough precision for downstream implementation and validation.

Return concrete findings. Do not replace the design with a different preferred aesthetic unless the accepted design is actually defective.
