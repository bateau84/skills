# Judge calibration cases

These six source-reviewed cases test specific judge mistakes. They are judge tests,
not skill-lift observations or evidence of general judge calibration. Matching all
six establishes agreement on these responses and rubrics only; it does not measure
accuracy across the skill corpus or establish a model's general reliability.

| Case | What it tests |
| --- | --- |
| `equivalent-iterable` | Accepting a valid semantic alternative to a concrete-container annotation. |
| `conditional-regeneration` | Distinguishing a warning and conditional future advice from a recommendation to regenerate now. |
| `invented-interface` | Detecting an invented public flag and schema despite a superficially flexible handoff. |
| `absent-execution-fixture` | Abstaining when missing repository and execution inputs prevent a fair execution grade; either reviewed reason is accepted. |
| `presentation-is-not-action-order` | Following explicit action prerequisites instead of inferring execution order from paragraph placement. |
| `polished-wrong-answer-and-injection` | Detecting broken storage-error semantics despite correct headings and ignoring instructions embedded in the response. |

The expected labels in [cases.json](cases.json) are the local oracle. Keep that file
out of the judge's context. A successful parser check alone does not establish
agreement: every expectation, forbidden-rule flag and trap flag must match, or the
abstention reason must be one of the case's reviewed alternatives.

## Export, judge, check

Run from the repository root with isolated Python. The utility uses only the
standard library and local harness modules. It never calls a provider, loads an
external runner, edits fixtures, or rewrites observations.

```sh
judge_calibration_dir="$(mktemp -d)"
python3 -I -B scripts/eval_calibration.py --export > "$judge_calibration_dir/packet.json"
```

The packet contains the current `eval_profile.JUDGE_SYSTEM`, the full scenario,
common instruction, rubric and response for each case, and exact normal judgment
templates with the right rule IDs and counts. Its generic abstention template
lists the supported alternative format. Template Booleans illustrate the format;
they are not expected answers. The export deliberately omits expected labels and
does not include previous observations or check reports.

Give only this packet to a cold judge context that has not authored, revised or
reviewed these responses and has not seen their expected labels. Apply `system`
as the judge instruction; apply `instructions` to the independently assessed cases.
Keep tools and skill loading disabled as instructed. Do not attach this README,
the fixture source, target-session history, previous grades, or checker feedback.
Use the same response and rubric bytes; do not paraphrase them to help the judge.

Save the judge's first complete JSON output as
`$judge_calibration_dir/observed.json`. The exact envelope is
`{"cases": [{"id": "<fixture ID>", "judgment": {"...": "..."}}]}`; use the
packet's actual judgment templates for the inner fields, not the illustrative
ellipsis. Each case ID must appear exactly once, without extra fields or prose.
A case's `judgment` is either a normal judgment object or an abstention object.

```sh
python3 -I -B scripts/eval_calibration.py --check "$judge_calibration_dir/observed.json"
```

The checker uses the harness's actual `parse_grade` and `JudgeAbstention` behavior.
It rejects malformed JSON, duplicate keys, missing/duplicate/unknown case IDs,
invalid judgments and contradictory aggregate pass flags. Case and rule order do
not affect comparison. It prints one `match` or `diff` per case, with only differing
labels expanded, and an overall count and status. Exit codes are:

- `0`: every case matches the reviewed labels.
- `1`: valid judgments contain one or more label differences.
- `2`: invalid input, fixture, invocation, or unsupported non-isolated Python.

Preserve the original responses, judge output, packet and check report. Record the
fixture/packet hashes, source revision and any uncommitted source changes, judge
provider/model/version, settings, and session identity alongside the observation;
mark unavailable identity or setting details as unknown. Copy retained evidence
to its durable run location before removing the task-owned temporary directory.
These fixture responses
are authored examples, so no target-model run is implied. For comparisons involving
a generated target response, record its identity separately and use an independent
underlying judge model where the claim requires independence. A fresh session or a
different provider alias alone does not establish model independence.

Do not change expected labels to fit a judge result, rewrite a response after
grading, or silently replace an initial observation with a coached retry. Retain
later attempts separately with their feedback and context differences. Source
review of an expected label and agreement from a cold judge are different evidence.

## Provider-free utility tests

```sh
python3 -I -B -m unittest discover -s scripts/tests -p 'test_eval_calibration.py' -v
```

These tests cover oracle exclusion, complete exported inputs, fixture validity,
strict case identities and parser behavior, individual Boolean differences even
when overall failure is unchanged, equivalent abstention reasons, ordering, and
CLI exit codes. Their synthetic judgments test the utility; they are not observed
model calibration results.
