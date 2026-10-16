# Retrospective — Quality Assurance

Adversarial checks for an apparently balanced, well-sourced retrospective. Look for shared blind spots, misleading evidence, and changes that might destroy what worked.

## QA criteria

| Probe | What should be challenged |
| --- | --- |
| All reviews and CI checks passed, but the user struggled through repeated handoffs. | A green technical result must not erase poor collaboration or usability. |
| The report lists only failures because telemetry flags errors. | Valuable successful decisions and enabling conditions may be invisible to the counters. |
| The report praises a skill because it loaded in sessions that later received approval. | Correlation, selection bias, and alternative explanations prevent a causal claim. |
| Several agents cite the same underlying failure log. | Repeated commentary must not be mistaken for independent instances. |
| An intervention lowered errors after an observer/plugin upgrade. | Detector changes, window differences, and missing exposure may invalidate the trend. |
| An experiment was accepted but never deployed. | A better subsequent outcome cannot be credited to a change that was not applied. |
| A fix proposal would remove a safeguard that also prevented real damage. | Consider downside, trade-off, ownership, and whether a safer reversible experiment exists. |
| One severe but rare incident is hidden by many minor successful events. | Raw counts must not overwhelm severity or unrepresented human experience. |
| An effective one-off practice is written as permanent agent policy. | Scope, preconditions, conflicting cases, and strength of evidence must be preserved. |
| Logs are missing and participant feedback is unavailable. | No confident root-cause narrative, invented satisfaction, or automatic change should follow. |
| The retro proposes no changes and is labeled unproductive. | Verified successes and lessons can make a zero-proposal retrospective valuable. |
| A retro's proposed change is recorded as implemented and successful. | Proposals, approval, implementation, observation, and learning require distinct evidence. |
| A missed mechanical error prompts another Reviewer or AGENTS.md instruction. | First inspect existing lint/type-check/test commands and whether they are run; a deterministic check may address the mechanism more reliably. |
| Numerous tool calls are labeled waste while key files were difficult to discover. | Consider missing navigation pointers, hidden dependencies, unavailable information, and necessary exploratory work before declaring calls excessive. |
| The user asks to reflect on an unfinished coding session. | A single session can be reflected on without fictional completion or a mandatory milestone-sized process. |

When challenging a finding, name the observation, the plausible counterexample, its consequence, and what additional evidence would decide it. Do not force a new experiment or a review stage solely to satisfy QA.
