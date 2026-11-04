# Code Analysis Assessment

Assess the analysis against its question and inspected code, not against how many issues it found. This is an optional review perspective, not a required approval stage.

- **Path identity:** Can the claimed entry-to-outcome path be reconstructed from the cited revision and source locations? Check the actual dispatcher, callback registration, configuration, or caller rather than relying on similarly named symbols.
- **Boundary completeness:** For the question at hand, are relevant error, cancellation, cleanup, state, and cross-language edges covered? Are unsupported or dynamic edges marked as unknown rather than silently omitted?
- **Finding validity:** Does each confirmed defect establish a reachable trigger and consequence? Check the strongest caller guarantee or guard that could make the allegation false. Does the claimed contract come from accepted behavior rather than the analyst's preferred design?
- **Evidence calibration:** Are static proof, runtime reproduction, tool diagnostics, hypotheses, and intended behavior distinguished? Do successful tests cover the asserted property rather than a mocked substitute?
- **Negative evidence:** Are unused-code and no-caller claims supported beyond an empty, stale, filtered, or language-limited index? Is a no-findings result scoped to what was examined?
- **Impact accuracy:** Are direct consumers distinguished from possible indirect consumers? Were serialized contracts, generated sources, and registration/configuration checked where relevant?
- **Bounded delivery:** Does the answer resolve the requested question without unauthorized edits, a general audit, fabricated test execution, or a merge/security/performance verdict it cannot support?

Re-check decisive source locations and evidence. Record unavailable evidence as a review limit; do not convert a self-review into a claim of independent verification.
