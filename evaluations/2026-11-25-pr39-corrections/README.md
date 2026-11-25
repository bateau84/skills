# PR #39 correction record — 2026-11-25

This record addresses the review of `8e6f6514eccdab14e4cd18bd0be82d1d18ed69e3`.
The corrections preserve the existing outcome/convention design and the 590-case
corpus. They do not establish general improvement in agent performance.

## Review findings

| Finding | Correction | Verification |
| --- | --- | --- |
| MAJOR-01: calibration names reveal expected verdicts | Export fresh random opaque IDs, shuffle cases, and retain a separate private ID map bound to the exact fixture and packet. The checker also verifies the mapped scenario/response, not just hashes. Public reports preserve packet order. | Counterfactual source-name/expected-label test; strict binding and no-clobber tests; six-case repeat below. |
| MAJOR-02: IxD-01 invents automated migration execution | Accept scriptable listing plus interactive-only apply that refuses unavailable confirmation safely. Keep unsafe application and hanging for unavailable input as failures. Audit all 45 reclassified preexisting cases for equivalent mistakes. | Full case-by-case audit and an explicit safe counterexample; fresh contrasting product-policy tasks below. |
| MAJOR-03: ORM guidance contradicts its commit-safe fixture | Explain successful `session.begin()` commits and session cleanup separately. Explain `run_sync()` as an API bridge, not isolation. Direct rollback tests to a connection-owned outer transaction and savepoints. | Bounded runtime counterexample and commit-safe cleanup probe; independent source review. |
| MINOR-01: Markdown pools different measures | Group comparison classifications by outcome, convention, legacy unclassified rubric, and unknown/unavailable basis. | Mixed-basis and historical-decision regression coverage through the actual report renderer. |

The implementation review also caught two remaining Pydantic outcome criteria
that still required particular APIs after the trap had been corrected, plus two
Terraform documentation cases that rejected supported example filename variants.
These are corrected in the final audit below. The review did not change
the new comparison tasks, their rubrics, or the practitioner snapshots.

## Semantic audit of the reclassified cases

[rubric-audit.json](rubric-audit.json) records all **45** preexisting cases that
gained criterion classifications in the reviewed PR. **16 needed correction;
29 were retained.** Thirteen cases received wording corrections and four received
criterion-type changes; one case is in both groups. Three cases moved specific
preferences to the convention axis. The remaining type change moves FastAPI's
explicit no-duplicate-route-validation requirement to the outcome axis.

Representative corrections:

- IxD-01 accepts safe refusal of unattended apply; a CLI does not imply that all
  its mutations must be automatable.
- Configuration loading tests the required values and source precedence while
  accepting equivalent Viper or Pydantic loading mechanisms.
- FastAPI response safety permits a demonstrably safe explicit payload; resource
  ownership does not require an `app.state` attachment by name.
- Working Swagger delivery need not use one exact handler/import combination.
  Go diagnostic reproduction need not always be an automated test. Terraform
  example names can use supported suffix variants while preserving generator
  discovery paths and required extensions.
- File placement and PR body grouping remain conventions where the task did not
  make them part of the product contract.
- Web history and URL behavior must be coherent and preserve any accepted
  sharing contract. Intentionally local state is permitted with explicit
  consequences, rather than silently inventing a shareable-state requirement.

[ixd-counterexample.json](ixd-counterexample.json) retains a worked interactive-only
migration design and the expected source-review assessment. It is an authored
counterexample, **not a model observation**. It keeps the original scenario and
shows why omitting `--yes` can still satisfy the product.

The audit does not reclassify the 477 untouched legacy cases or claim an
exhaustive semantic audit of the 68 new cases. Coverage stays **590 cases across
124 skills**, of which 113 cases explicitly classify criteria.

## Calibration repeat

The original [2026-11-24 input and judgments](../2026-11-24-skill-quality/README.md#judge-calibration-observation)
remain unchanged. Their descriptive IDs exposed intended interpretations, so
that 6/6 agreement is now labeled **cue-confounded**.

The repeat retains the exact [public packet](calibration/input.json),
[first judgment](calibration/observed.json), and [checker result](calibration/check.json).
**All six judgments agree with the prepared labels.** The checker uses the
production grade/abstention parser and compares each Boolean or allowed
abstention reason. It does not count parser acceptance as label agreement.

The supplied packet contains only opaque IDs, complete scenarios/rubrics/answers,
the judge system instruction, and schema templates. Its canonical SHA-256 is
`34aee1cd1ef2bea27ae76e21eb1feb49c4d3af89d1232e474c23f71c1e3387f5`.
The private map is retained separately by the maintainer and is deliberately
absent from this repository. Public file-byte hashes in `sha256.json` use a
different representation from this canonical JSON identity.

One fresh judge context received only that packet. It had no inherited
conversation and was instructed not to inspect other files, mappings, source
labels, or earlier verdicts. The requested judge selector was **`gpt-6.2-sol`**,
with **high** reasoning effort; targets inherited the surrounding session model
without an override. Resolved deployment identities were not independently
attested. Filesystem/tool restrictions were instructions in a shared environment,
not enforced isolation. The invocation was a manual subagent exercise using the
production instruction/parser, not a native provider-runner invocation.

Six authored examples remain a narrow calibration check. No claim of general
judge reliability or independent deployment identity follows from this repeat.
See the [reusable workflow](../judge-calibration/README.md) to create another
packet and private map. A maintainer with the retained map can reproduce this
specific check using `--check`, `--mapping`, and `--packet`.

## Database runtime check

[database/transaction_probe.py](database/transaction_probe.py), its
[dependency versions](database/requirements.txt), and its
[recorded result](database/result.json) retain a small async SQLAlchemy probe.
It used Python 3.12.14, SQLAlchemy 2.0.58, aiosqlite 0.21.0, SQLite 3.53.1,
`NullPool`, and explicit SQLite transaction-control events.

| Observation | Rows observed |
| --- | ---: |
| Successful ordinary `session.begin()`, then later session rollback | 1 persisted |
| Uncommitted `run_sync()` work, followed by session close | 0 persisted |
| Outer transaction plus savepoints, after async and synchronous application commits | 2 visible within the test; outer transaction remained active |
| Fresh physical connection after closing the session and rolling back the outer transaction | 0 persisted |

This verifies the relevant API/ownership boundary on the recorded SQLite setup.
It does **not** execute PostgreSQL/asyncpg, the pytest fixture lifecycle, or an
agent-generated application. The skill continues to require proper backend and
driver SAVEPOINT support and a fresh-read cleanup check.

## New original-versus-revised response comparison

**Both usable task pairs pass under original and revised guidance. The third
pair is non-evidence because its frozen rubric adds a requirement and the judges
handle equivalent behavior inconsistently. No behavioral lift is established.**

A fresh task-author context prepared three new prompts without reading the
source skills, existing evals or prior experiment artifacts. The complete tasks
and outcome criteria were frozen before target runs; see
[revision/tasks.json](revision/tasks.json), the
[freeze manifest](revision/freeze-manifest.json), and the author's
[rationale](revision/maintainer-rationale.json). The rationale was withheld from
targets and judges. Practitioner snapshots stayed unchanged through all runs.

| Control | Recorded setup |
| --- | --- |
| Original | Pre-PR commit `056c9b27da4f03ea7a3495359c4e674a9063f0f3`; arm `p-2bec22be48ed` |
| Revised | Corrected practitioner files; arm `p-12648b54d6e3`; exact source hashes in the manifest |
| Targets | Six fresh contexts with no inherited conversation; one task and one arm each; one response per context; no target reruns |
| Target material | Exact prompt and assigned practitioner; evaluation criteria, companion files, other outputs and arm mapping excluded from supplied material |
| Target model | Inherited parent model/effort; no explicit override; resolved deployment and sampling controls unavailable |
| Absolute judges | Two fresh contexts, each receiving only one anonymized arm's three complete prompts, frozen criteria and unedited answers |
| Judge setting | Requested `gpt-6.2-sol`, high reasoning; resolved deployment not independently attested; first complete judgments retained |
| Matching | Production parser and retained verifier check full task, rubric, answer, system instruction and template identities; neither arm uses a shortened scenario |
| Isolation | Instruction-based restrictions in a shared environment/catalog; no enforced filesystem isolation or native skill-load proof |
| Execution | Response/design products only; no generated fixture or CLI was executed |

| Task | Original first judgment | Revised first judgment | Evidentiary disposition |
| --- | --- | --- | --- |
| Dock-scheduling fixture tolerates service commits and handled rollback | PASS, 9/9 criteria | PASS, 9/9 criteria | Limited non-regression |
| Live-human erase policy with unattended viewer inventory/preview | PASS, 9/9 criteria | PASS, 9/9 criteria | Limited non-regression |
| Accepted signed-plan unattended execution | FAIL, 9/10 criteria | PASS, 10/10 criteria | **Non-evidence; no improvement credited** |

The third task's prompt permits retries with the same target set and **a valid
approval**. Frozen criterion r8 instead says **the same applicable approval**.
Both answers permit an authorized human to issue a fresh approval for the same
unchanged plan and operation after the first approval expires. The original-arm
judge penalizes that renewal; the revised-arm judge accepts the corresponding
behavior. That difference is not evidence of a better product.

A separate fresh review context received the full prompt, unchanged criteria and
both anonymized answers, without their grades, sources or arm mapping. Its
[first review](revision/rubric-review-observed.json) finds r8 conflicting and r6
ambiguous about whether optional operator inspection itself must be terminal-free.
Both answers already offer machine-readable inspection, so r6 did not produce
the observed difference. The review assesses rubric validity, not a replacement
score. Its [exact input](revision/rubric-review-input.json) is retained.

[revision/comparison.json](revision/comparison.json) records the maintainer's
non-evidence disposition separately from all raw grades. Neither task text,
criteria, target answer nor first judgment was changed. The affected task was
not rerun or silently converted into another success. The
[skill-authoring evaluation guidance](../../skills/skill-authoring/references/evaluation-design.md)
now calls for valid-alternative checks, preservation of task quantifiers,
withheld calibration identifiers, and retaining invalid comparisons without
crediting apparent gains.

[revision/manifest.json](revision/manifest.json) identifies source snapshots,
targets, packets and first judgments. Raw inputs retain historical absolute
paths for provenance; those paths are not needed to inspect the public record.
Run this provider-free integrity check from the repository root:

```sh
python3 -I -B evaluations/2026-11-25-pr39-corrections/revision/verify.py
```

The saved [check result](revision/check.json) verifies artifact identity and grade
schema, not rubric validity. The two usable pairs are a narrow non-regression
observation with one sample each. They are not a statistical result, a no-skill
comparison, or an application-execution benchmark. The unsuccessful third pair
also shows why six successful calibration examples cannot establish general
judge reliability.

## Harness verification

- Fixture validation: **590 cases, 124 skills, zero provider calls**.
- Full provider-free harness against runner
  `dbbbf2a0740aee7a9e9035cc14a785a9467b8fb1`: **182 tests run; 178 passed and
  four optional MCP SDK checks skipped locally**. Reference CI installs those
  dependencies separately.
- Focused calibration utility: 11 tests passed. Markdown renderer: 26 passed.
  These are subsets of the full harness, not additional independent observations.

CI run links and the tested commit are recorded in the PR after publication.
No full 590-case model benchmark was requested or executed in this correction
cycle. Provider-free validation is harness evidence, not behavioral lift.
