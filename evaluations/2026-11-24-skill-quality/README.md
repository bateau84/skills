# Limited revision smoke check — 2026-11-24

**All four tasks met the outcome criteria under both original and revised
skills. This is a non-regression observation, not measured skill lift.**
The revised answers were sometimes more compact, but artifact count and brevity
were not success criteria. In particular, the original three-requirement answer
and the revised one-requirement answer both preserved the accepted behavior.

This packet retains the synthetic task text, answers, judgments, and source
hashes used while reviewing the [skill and evaluation changes](../../docs/skill-eval-improvement-2026-11-24.md).
It is separate from native OpenCode evaluations and from the user's historical
Claude report. No original Claude responses or judgments were available.

## Method and controls

| Control | Observed setup |
| --- | --- |
| Comparison | Original practitioner at `056c9b27da4f03ea7a3495359c4e674a9063f0f3` versus revised working-tree practitioner |
| Tasks | Four fixed response tasks; one output per arm and task |
| Target contexts | Four fresh ChatGPT subagents with no inherited conversation; two related tasks per target context |
| Inputs | Each target was instructed to read only its assigned practitioner and relevant references; evals and companions excluded from the supplied snapshots |
| Restrictions | Instruction-based in a shared environment; no enforced filesystem/tool isolation or native skill-load proof |
| Model controls | No explicit model/effort override; inherited session model. Resolved deployment identities, seeds, and sampling controls were not independently available |
| Absolute judging | Two fresh subagent contexts; each judged only one anonymized arm's four responses against outcome criteria, without the other arm, source skills, or revision mapping |
| Independence | Separate contexts, same inherited model environment and available skill catalog. This is not verified cross-model or human-independent validation |
| Repetitions | One per task/arm; no unsuccessful target samples were discarded or rerun |
| Execution claim | Response products only. No application execution, provider-native runner integration, or general discovery performance was measured |

The current root conversation, shared system instructions and available skill
catalog can affect every subagent. Fresh contexts reduce direct conversation
carryover; they do not remove these shared influences. The four tasks were
selected during development, not held out from all authors.

## Arm mapping and results

`p7` is the original practitioner and maps to judge packet `x9`. `p2` is the
revised practitioner and maps to `x4`. The mapping was withheld from judges.

| Task | Product under review | Original | Revised |
| --- | --- | --- | --- |
| work-1 | Complete requirements for queued export withdrawal, without inventing an interface or deciding pending architecture | All 3 outcome criteria met | All 3 met |
| work-2 | Useful unpublished issue draft that preserves undecided public option/schema | All 3 met | All 3 met |
| work-3 | Minimal usable Go layout with need-based expansion | Both outcome criteria met | Both met |
| work-4 | Honest Python verification status and concrete inspect/fix/rerun plan preserving accepted behavior | All 3 met after judge-input correction below | All 3 met |

These 4/4 observations per arm do not provide a statistical confidence claim,
a comparison against no skill, or evidence that all 590 fixtures now pass.
The original three behavioral requirements remain valid: splitting a product
into more than one requirement is not inherently overproduction.

## Preserved input error and correction

The first `x9` packet summarized task prompts. Its work-4 summary omitted the
supplied filename, test identifier, and numeric exit codes, while the target
answer retained them. The judge correctly noticed those details were unsupported
by its shortened packet. This was an evaluator setup defect, not target invention.

- `inputs/x9-initial-input.json` and `judgments/judge-x9-initial.json` preserve the
  initial packet and all four judgments, including that caveat.
- `inputs/task-prompts.json`, `inputs/x9.json`, and `inputs/x4.json` retain the
  verbatim task text. The `x4` judge received the complete packet initially.
- `judgments/judge-x9-corrected.json` reassesses only work-4 with the corrected
  prompt, in the same judge context. It preserves the PASS and removes the
  unsupported-details caveat. It is not a cold new observation or a target rerun.
- The original work-1 through work-3 judgments remain the retained assessments
  against their initial summarized prompts. Those summaries preserved the
  accepted facts used by their criteria, but this difference remains a limitation.

No grade has been silently replaced. Inputs and raw responses should be examined
alongside the scores; the episode illustrates why exact target-to-judge task
provenance matters.

## Judge calibration observation

A separate fresh context assessed six source-reviewed synthetic examples,
without the expected labels. `inputs/calibration.json` is its actual packet;
`judgments/judge-calibration.json` is its unedited response. The packet used the
production judge system instruction, the scenario/rule/answer fields, and schema
identifiers; the dispatch supplied the strict object shape. It was a manual
subagent invocation, not the native runner's exact serialized invocation.

The observed judgments agree with all six prepared labels: accept an equivalent
iterable type, accept conditional future regeneration, reject an invented public
interface, abstain on absent execution inputs, distinguish prose order from
action order, and reject a polished wrong contract despite embedded judge
instructions. Six examples are a spot check, not broad judge calibration.

The reusable [calibration workflow](../judge-calibration/README.md) exports
oracle-free packets and checks recorded judgments through the production parser.
Its current export format may be richer than this retained manual packet; the
actual input above is frozen rather than regenerated retrospectively.

## Provenance

`manifest.json` records SHA-256 identities for every retained input, response,
and judgment, plus the twelve practitioner/reference files in each supplied
snapshot. Original hashes were checked against the base commit; revised hashes
were checked against the files committed by this change. The snapshots excluded
`ASSESSMENT.md`, `QA.md`, and `evals/`.

`responses/` contains the four complete two-task target answers as JSON string
values, saved in a recordkeeping follow-up without regeneration. Decoding each
`response` value recovers the original bytes, including Markdown hard breaks;
the manifest also records those decoded-response hashes. Judge packets also retain the
per-task extracted text. Absolute scratch paths inside answers are historical
context, not portable links or evidence of native skill discovery.
