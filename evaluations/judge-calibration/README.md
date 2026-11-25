# Judge calibration cases

These six source-reviewed cases test specific judge mistakes. They are judge
tests, not skill-lift observations or evidence of general judge reliability.
Agreement on all six establishes agreement on these responses and rubrics only.

**The initial 2026-11-24 calibration exposed descriptive source case IDs.** Its
6/6 agreement is retained as historical, cue-confounded evidence. It does not
establish that the judge reached those conclusions without answer cues. The
corrected workflow below hides both explicit labels and source identifiers.

| Maintainer-only source case | What it tests |
| --- | --- |
| `equivalent-iterable` | Accepting a valid semantic alternative to a concrete-container annotation. |
| `conditional-regeneration` | Distinguishing a warning and conditional future advice from a recommendation to regenerate now. |
| `invented-interface` | Detecting an invented public flag and schema despite a superficially flexible handoff. |
| `absent-execution-fixture` | Abstaining when missing repository and execution inputs prevent a fair execution grade. |
| `presentation-is-not-action-order` | Following explicit action prerequisites instead of inferring execution order from paragraph placement. |
| `polished-wrong-answer-and-injection` | Detecting broken storage-error semantics despite correct headings and ignoring embedded judge instructions. |

Keep this README, [cases.json](cases.json), expected labels, ID mappings and
previous observations out of the judge context. A successful parser check alone
does not establish agreement: every expectation, forbidden-rule flag and trap
flag must match, or the abstention reason must be a reviewed alternative.

## Export, judge, check

Run from the repository root with isolated Python. The utility uses only the
standard library and local harness modules. It never calls a provider or loads
an external runner. Create a task-owned private directory:

```sh
judge_calibration_dir="$(mktemp -d)"
python3 -I -B scripts/eval_calibration.py --export \
  --mapping "$judge_calibration_dir/private-map.json" \
  > "$judge_calibration_dir/packet.json"
```

Every export creates fresh random opaque IDs and shuffles case order. Both the
case inputs and result templates use only those opaque IDs. Neither source names,
known fixture order, expected labels, nor mapping hashes are exported. The packet
contains the current judge system instruction and complete task/rubric/response
bytes; template Booleans illustrate the format, not the correct answers.

The mapping is a **separate private file**, created with mode `0600` and without
overwriting an existing file or symlink. It binds opaque IDs to source IDs and
records identities for the exact fixture and exported packet. Never attach it
to the judge prompt, place it in a target-visible workspace, or commit it to a
public evidence bundle. Keep it in the maintainer's private run records.

Give **only `packet.json`** to a fresh judge context that has not authored,
reviewed, or previously graded these responses and has not seen source names or
expected labels. Apply the packet's `system` and `instructions`. Use enforceable
context/tool restrictions when available; otherwise record instruction-only
isolation. Do not give the judge the repository, this README, mapping, checker
feedback, or an explanation of which cases ought to pass. Do not paraphrase the
scenario or response. Preserve the first complete response, including failures.

Save the result as `$judge_calibration_dir/observed.json`. The result envelope
is `{"cases": [{"id": "<opaque ID>", "judgment": {"...": "..."}}]}`; use the
packet's actual inner templates, without extra prose or keys. Then check it:

```sh
python3 -I -B scripts/eval_calibration.py \
  --check "$judge_calibration_dir/observed.json" \
  --mapping "$judge_calibration_dir/private-map.json" \
  --packet "$judge_calibration_dir/packet.json"
```

The checker validates the complete ID mapping, exact packet and fixture identity,
and the task/response associated with each mapped ID. Swapped mappings, altered
inputs, changed expected labels, duplicate/missing IDs and malformed judgments
fail. The production `parse_grade` and `JudgeAbstention` validate every judgment.
The public check report uses opaque IDs in packet order, preserving the mapping's
separation from public results. Valid results may be returned in any order.

Exit codes:

- `0`: every case agrees with the reviewed labels.
- `1`: valid judgments contain one or more label differences.
- `2`: invalid input, mapping, fixture, invocation, or non-isolated Python.

## Historical results

Old source-named judgments can be checked only through the explicit legacy path:

```sh
python3 -I -B scripts/eval_calibration.py --legacy-identifiers --check \
  evaluations/2026-11-24-skill-quality/judgments/judge-calibration.json
```

The output labels this as source-ID-exposed evidence, not blinded calibration.
Do not rewrite historical inputs/grades to make them appear blinded after the
fact. The [correction record](../2026-11-25-pr39-corrections/README.md) distinguishes
the original observation from the repeat with opaque IDs.

## Evidence and limitations

Retain the exact packet, first judgment, check report, source revision, instruction
identities and model settings. Preserve the private map separately. Mark resolved
model identities, seeds or other unavailable controls as unknown. A model selector,
provider alias or fresh context does not establish independently verified model
identity or isolation. These are authored examples; they imply no target-model
execution. A different requested judge model remains distinct from an attested
underlying deployment identity.

Do not change expected labels to fit the judge, rewrite responses after grading,
or silently replace an initial result with a coached retry. Later attempts must
retain their feedback/context differences. Copy the intended records to their
durable public/private destinations before removing the temporary directory.

## Provider-free utility tests

```sh
python3 -I -B -m unittest discover -s scripts/tests -p 'test_eval_calibration.py' -v
```

Tests cover withheld source IDs and labels in every public field, shuffled order,
unchanged packets under counterfactual source-name/label changes, private file
permissions/no-clobber behavior, exact mapping/packet/fixture binding, individual
Boolean differences, equivalent abstentions, and explicit legacy handling.
Synthetic test grades validate the checker; they are not model observations.
