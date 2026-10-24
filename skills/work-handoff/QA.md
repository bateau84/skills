# Work Handoff — Quality Assurance

Assume a competent author and reviewer produced a plausible handoff. Attack failures that could still send an independent recipient to pursue the **wrong outcome**.

## QA criteria

- **Superseded decision replay:** Could the handoff preserve an attractive early proposal while omitting a later correction that changes the required outcome?
- **Fake readiness:** Can two reasonable implementers disagree about essential product meaning because an unresolved owner decision is hidden as an engineering detail?
- **Lost-context simulation:** Remove the conversation and inaccessible session links. Does the receiving agent still know what is authoritative and how to assess completion?
- **Readable-summary trap:** The opening sounds simple and faithful, but later criteria contain opaque jargon, an extra MUST, or a reversed exclusion that a human reader might miss. Compare the complete artifact against the actual accepted decisions, not just its introduction.
- **Simplification-destroys-meaning trap:** Rewording an important error outcome, ordering rule, compatibility limit or interface detail makes the document sound easier while changing its meaning. Read the plain example and exact technical clauses together.
- **Semantic downgrade/upgrade:** Did a MUST become merely optional, or did a suggested API, internal implementation or convenient example become a MUST across a component boundary?
- **Wrong-work false positive:** Could a trivial change satisfy the written acceptance bullets while the true user-visible outcome remains broken?
- **Evidence drift:** Could a resolved bug, obsolete path, stale incident report, or superseding PR invalidate the handoff's premise?
- **Privacy and authority:** Could publishing to another team expose private material or grant permission to implement a tentative decision despite an apparently polished contract?
- **Fragmentation:** Could a set of individually plausible handoffs omit the integrated scenario, owner, or dependency that makes the total work actually useful?

Probe plausible misdirection and confidence failures, not exotic redesign. QA does not create product authority or require a separate approval stage.
