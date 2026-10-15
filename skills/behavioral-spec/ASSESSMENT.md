# behavioral-spec Reviewer Assessment

Cross-artifact review guidance for any agent performing assessment. Artifact-specific criteria for BR, QS, and OC follow in their own sections. Assess the resulting meaning and evidence, not whether the author reproduced a prescribed checklist or number of artifacts.

## Review criteria

- Every material commitment in the claimed ready scope has obligation coverage. Source-to-obligation relationships make omissions and the impact of changed authority visible; an open question is not satisfied coverage.
- Every normative claim is sourced, necessarily derived, or an ordinary specification choice within agreed scope. Consequential derivations explain what agreed commitment would fail without the obligation; source links alone are insufficient. Alternative realizations and reasonable preferences are not mislabeled as necessities.
- Routine semantic choices are settled and explained within delegated authority; material new capability, scope, risk, guarantee, or reserved preference remains with its owner. Mere ambiguity has not caused unnecessary escalation.
- Source modality is preserved: examples, preferences, permissions, and exploration language are not inflated into mandatory guarantees. Scope exclusions are distinguished from prohibitions, and a minimal version has coherent behavior within its accepted boundary.
- Downstream design, architecture, tests, code, or implementation behavior has not silently become upstream source authority. Applicable accepted obligations remain binding unless properly superseded; conflicts are explicit.
- Relevant actors, boundaries, lifecycle states, ordering, failure/recovery, information/evidence, shared semantics, and preservation/quality conditions are covered to a depth justified by their consequences. There are no material silent omissions or invented obligations merely to populate a lens.
- Environmental and dependency assumptions have an explicit basis and scope. Unaccepted assumptions do not erase accepted adverse conditions, transfer obligations to unspecified actors, or quietly weaken guarantees.
- Invariants hold over the applicable transitions, including failure and recovery. Useful execution/progress is preserved under accepted conditions without inventing unconditional eventual success, automatic recovery, or numeric targets.
- BR/QS/OC selection is proportional; each guarantee has one normative home and related artifacts cross-reference it rather than duplicating it for ceremony.
- The obligation layer and accepted Designer User Stories/Scenarios are semantically compatible where they overlap.
- Normative language is architecture-independent unless structure is itself authoritative.
- Meaning-bearing terms, quantifiers, ordering, temporal language, defaults, exceptions, and triggering conditions admit one falsifiable interpretation. Verification addresses the actual obligation, not merely a neighboring behavior.
- The set resists vacuous satisfaction: useful accepted behavior is possible, triggering conditions are meaningful, and suppressed evidence cannot make an obligation appear satisfied.
- Cross-artifact requirements, scenarios, and contracts do not weaken or contradict one another in consequential combined cases. Known omission, invention, or composition counterexamples are resolved or honestly limit the ready scope.
- Handoff claims are bounded and truthful: consequential choices, coverage limits, and blockers are visible; unresolved dependent meaning is not declared complete, while independent work is not needlessly blocked. No new gate, mandatory notation, or exhaustive-completeness claim substitutes for actual coverage.

## Review depth

Scale with semantic consequence, number of actors/states, temporal behavior, independent parties, failure/recovery branches, compatibility/security impact, and source uncertainty. The criteria describe evidence properties to assess; they do not require exhaustive state enumeration, a fixed artifact count, or Critic-style independent red-teaming.

## Behavioral Requirement artifacts

### Review criteria

- The BR expresses one coherent normative behavior rather than a bundle of loosely related promises.
- Statement and acceptance criteria preserve accepted product meaning without strengthening source modality or inventing scope.
- The requirement is implementation-independent unless an exact structural constraint is authoritative.
- Triggering conditions, actors, quantifiers, ordering, defaults, failure/recovery, and exceptions are explicit where outcome-relevant.
- Acceptance criteria cover the material negative space, not only the happy path.
- The wording resists vacuous satisfaction and cannot pass by suppressing the triggering state or evidence of violation.
- Verification semantics observe the actual promise and can distinguish pass from fail.
- Derived-from provenance points to legitimate semantic authority, not downstream convenience.

### Review depth

Scale with consequence, state/actor combinations, temporal semantics, and failure/recovery complexity.

## Quality Scenario artifacts

### Review criteria

- The QS expresses a real quality under a concrete condition/stimulus, not an adjective such as fast, secure, scalable, reliable, or robust.
- Source-of-stimulus, stimulus, environment, semantic target, response, and response measure are all recoverable from the scenario even though they are not separate durable fields.
- `Derived from` is provenance and is not confused with the classic quality-scenario source of stimulus.
- The target remains semantic rather than prematurely naming an architectural component.
- Acceptance criteria contain the pass/fail response boundary; Verification semantics explain how that boundary is exercised and observed rather than substituting for the measure.
- Numeric thresholds or risk tolerances are supported by accepted authority or defensible derivation, not invented for apparent precision.
- The QS adds meaningful stressed/degraded/boundary quality coverage instead of duplicating a BR.
- Human-facing interaction qualities remain within Designer authority where appropriate.

### Review depth

Scale with quality consequence, uncertainty of thresholds, environment complexity, and difficulty of observing the response.

## Obligation Contract artifacts

### Review criteria

- The seam actually warrants a durable shared semantic contract; the OC is not ceremony for private internals.
- Participants are semantic responsibilities and can be realized independently without freezing architecture.
- Preconditions, guarantees, semantic input/output, failure semantics, and invariant are mutually coherent and implementation-independent.
- Shared ordering, retry, duplication, idempotency, cancellation, lifecycle, authority, evidence, and recovery semantics are explicit where correctness depends on agreement.
- Every consequential guarantee has legitimate semantic authority; architecture merely revealing a seam has not become source authority.
- The OC does not weaken or contradict related BRs/QSs or accepted Designer semantics.
- Verification semantics exercise the actual participating boundary and close the claimed guarantee.
- Concrete schema/API/protocol details are absent unless externally authoritative.

### Review depth

Scale with independent implementation, security/authority consequence, failure ambiguity, and cross-party state/lifecycle complexity.
