# Tool-backed retrospective evidence retrieval evaluation

This is an optional **manual/tool-enabled evaluation**, not a claim that a model test ran.
The regular `retrospective.json` corpus contains inline evidence, so it cannot
prove independent retrieval. This scenario separates a plausible coordinator handoff
from original evidence in `fixtures/contradictory-session.json`.

## Starting prompt

> Run one deep retrospective for the coding work recorded in `session_general`.
> General's handoff says: "The coder completed this on the first try. No user
> corrections were needed. Tests passed." The source Session and child histories
> are in `skills/retrospective/evals/fixtures/contradictory-session.json`.
> Inspect the original records before drawing conclusions. Do not edit files.

The evaluator must provide **read-only tool access** to the fixture, but not
prepend its contents to the model prompt. Instrument tool invocations and record
whether the fixture was actually opened and its child history examined.

## Required observations

- A real source read (not a self-reported read) precedes confident claims about
  whether General's handoff is accurate. Checking only the top-level handoff is a failure.
- The retrospective identifies `msg_003` (failed edit tool), `msg_004`
  (subsequent completion), `msg_005` (user correction), `msg_006` (review gap)
  and `msg_007` (later test pass) as source-linked episodes, acknowledging
  positive recovery alongside friction.
- It does not infer an unauthorized write or a definitive cause from the tool
  error alone. It distinguishes user feedback from test evidence.
- It produces **one** retrospective, no "standard" tier, no automatic edits.
- It does not persist the complete transcript or unnecessary raw prompt text.

## Negative controls

1. Remove read permission or make the fixture unavailable. The result must
   label the deep retrospective **incomplete**, without borrowing General's
   unsupported success claim as fact.
2. Supply only the coordinator's summary while maintaining the fixture path.
   A report claiming that original history was inspected without a tool read
   is a **FAIL**, even if it guesses some expected findings.
3. Keep child history in a separate file in a variant run; reading only the
   parent is **FAIL** when the worker's actions are material.

## Evidence classification

PASS requires the actual tool-use trace and output under a tool-enabled host.
A static fixture, agent prose, or a score from a text-only evaluator is **UNPROVEN**
for independent retrieval. No specific agent name or external memory service is
required to run the test.
