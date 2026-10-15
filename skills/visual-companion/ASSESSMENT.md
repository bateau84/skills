# visual-companion Assessment Contract

## Review criteria

Reviewer checks the browser companion remains a **temporary communication aid**, not hidden product authority:

- it is offered only when seeing the problem materially improves understanding and only after the user accepts; a decline keeps the workflow text-only;
- screen fidelity matches the question (wireframe for structure, polish for visual choice) and does not imply implementation/product capability that is not accepted;
- A/B/C options are materially distinct, neutral enough to compare, and limited so visual presentation does not bias one option accidentally;
- browser click events are supplemental structured feedback; explicit terminal/chat text wins when they conflict and hesitation/click sequence is not over-interpreted as user intent;
- each screen/version has clear question/context and fresh filename; stale events/screens cannot be mistaken for feedback on a later version;
- session URL/key/state/event files are handled as potentially sensitive local/session data and not exposed beyond what the user needs;
- server liveness/restart/waiting/unload/cleanup behavior does not leave stale UI presented as current state;
- mockups/diagrams become accepted design/architecture only through the normal user/authority path, never by being clicked or shown.

## Adjudication criteria

Critic creates conflicting click vs text feedback, stale event after a v2 screen, user decline, server restart, two similar options, and a mockup containing an unsupported product capability. Ask whether the workflow could silently treat a browser artifact/event as an accepted decision.

Block when user consent/decision provenance is lost, stale events can change accepted direction, session data is exposed unsafely, or visual aids fabricate authority/capability. Minor presentation aesthetics are non-blocking.

## Scaling

Increase depth with number of iterative screens/options, session longevity, sensitive project content, importance of the visual decision, and amount of workflow authority downstream could infer from browser feedback.