# behavioral-spec Quality Assurance

Cross-artifact adversarial validation for any agent. Assume competent production and conformance review; attack residual semantic false confidence without inventing new requirements.

## QA criteria

- Start from accepted anchor meaning, not only the producer's coverage map. Construct a plausible conforming system that still defeats a commitment the bundle claims to cover.
- Construct sequences where individually reasonable BRs, QSs, OCs, and Designer Scenarios compose into contradictory outcomes, especially across cancellation/completion, partial effects/retry, or authority changes.
- Construct a materially different realization that satisfies accepted authority but violates a claim labeled necessarily derived. Distinguish a mislabeled legitimate specifier choice from an unauthorized product or architecture constraint.
- Remove or vary an unaccepted environmental/dependency assumption. Look for guarantees that hold only because an adverse condition was silently excluded or an obligation was assigned to an unspecified actor.
- Search for a downstream implementation or architecture premise that has been laundered into product truth through wording or examples.
- Attack ambiguous quantifiers and temporal terms such as all, any, never, final, eventual, retry, cancel, available, atomic, and complete.
- Find vacuous implementations that satisfy the literal text while defeating the accepted outcome, including ones that preserve safety by permanently denying useful work. Also attack progress claims whose unstated conditions weaken accepted safety.
- Search for missing actor/state combinations, unspecified defaults, suppressed evidence, and success-only semantics. Revisit consequential cases dismissed as irrelevant, not every possible combination.
- Ask whether two independent implementations could each claim conformance while disagreeing on a load-bearing meaning.
- Challenge verification semantics that observe a neighboring behavior rather than the actual normative guarantee.
- Attack false closure: can a recorded open question, circular derivation, repeated pass with no new findings, or an arbitrary scope boundary conceal a known unmet commitment? Conversely, has one local gap unnecessarily blocked unrelated settled work?

## QA depth

Increase depth where one shared semantic mistake could survive Producer, Designer/Architect reconciliation, and normal review. Choose probes independently of the producer's examples; challenge bounded-coverage claims without demanding proof about every imaginable system or promoting a probe into new product authority.

## Behavioral Requirement artifacts

### QA criteria

- Find an implementation that passes every literal criterion while violating the accepted user/system outcome.
- Attack all/any/never/eventual/final ordering and exception language for hidden alternate interpretations.
- Exercise edge sequences: duplicate action, interruption, stale state, retry, cancellation, concurrent change, and recovery where applicable.
- Search for an omitted actor/state whose behavior would be decided by implementation.
- Check that a structural mechanism has not been disguised as behavioral necessity.
- Attack verification semantics that can pass without exercising the actual trigger or observing the actual outcome.

### QA depth

Increase depth where a small wording ambiguity could authorize materially different behavior.

## Quality Scenario artifacts

### QA criteria

- Construct a system that passes the happy path but fails the claimed quality under a realistic degraded, peak, recovery, adversarial, or partial-failure environment.
- Vary the stimulus source and timing to expose a scenario that only works for the producer's assumed sequence.
- Attack invented precision: thresholds with no authority, measurements that ignore tail behavior, averages hiding failure, or success metrics that can be gamed.
- Search for an architectural target smuggled into the scenario such that an equally valid realization is excluded.
- Check whether the verification method can observe the actual response measure under the stated environment.
- Look for overlapping BR/QS language that creates contradictory guarantees or double-counts the same obligation.

### QA depth

Increase depth where a quality can look healthy under nominal tests while failing at the operational boundary that matters.

## Obligation Contract artifacts

### QA criteria

- Give the contract to two independent implementers and find any load-bearing meaning they could interpret differently while each satisfies the text.
- Attack timeout, duplicate, stale, retry, cancellation, partial completion, restart, and unavailable-peer cases where applicable.
- Search for authority or provenance that can be detached, replayed, substituted, or accepted by the wrong participant.
- Look for a guarantee that is true locally on each side but false across the seam because ownership/order/atomicity is undefined.
- Challenge whether the OC is compensating for an architecture choice rather than expressing stable semantics.
- Attack verification that checks only one participant or mocks away the actual cross-party guarantee.
- Search for an omitted failure meaning that would force architecture or implementation to invent product semantics later.

### QA depth

Increase depth where independently correct parties can compose into a semantically incorrect system.
