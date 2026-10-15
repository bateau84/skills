# Targeted mutation testing

Mutation testing asks whether tests detect deliberately wrong production behavior. Use it to strengthen evidence for an accepted requirement, not to invent requirements or a universal quality score. The method also works on an existing suite; it does not require replaying TDD history.

## Choose proportionate scope

Prefer changed or high-consequence decisions: inclusive/exclusive boundaries, authorization, validation, error propagation, state transitions, persistence, retry limits, and recovery. A few hand-selected mutations can answer a narrow question more cheaply than mutating the whole repository.

Start with one to three plausible defects or an equivalent bounded tool run. This is a starting heuristic, not a required count. Agree source scope, test scope, total runtime, per-mutant timeout, and concurrency within the task's existing budget. Stop or narrow the run when the budget is exhausted; preserve partial results without calling the untested remainder passed.

Do not install tools, change CI requirements, upload source/reports to external services, or launch expensive full-repository runs merely because this skill mentions them. Follow existing permissions and repository policy. Prefer local reports and an already configured tool. If automation is unavailable or incompatible, use a safe manual sample or explicitly record that the check was not run.

## Smallest useful procedure

1. **Preserve and isolate.** Record the source revision and relevant pending edits. Prefer a disposable copy/worktree containing the actual candidate, including uncommitted changes under test; a clean checkout of an older commit is not the candidate. Protect unrelated edits. Use test-only resources, not live systems or production credentials.
2. **Establish a baseline.** Run the selected tests without a mutation under the intended environment. Confirm the intended tests were collected and passed, not all skipped. A failing, flaky, or empty baseline makes the mutation result inconclusive until understood.
3. **Introduce one defect.** Change a production decision while keeping the tests fixed, for example `age >= 18` to `age > 18`, suppressing error propagation, or omitting a required state update. Automated tools may schedule many independent single-mutation cases; do not combine defects in a manual probe. Exclude tests, fixtures, generated code, and third-party code from the mutation targets unless that code itself is the agreed subject.
4. **Observe, do not infer.** Run the selected tests against the mutated source, not a stale build, cached result, installed package, or mock of the target. Record the mutation and failing test/signal. A nonzero process exit alone does not prove a meaningful kill.
5. **Triage and improve.** For a real gap, derive the next test from the accepted behavior. Observe that the new test fails against the mutant and passes against restored production code. Keep that test; never change expected outputs to agree with the mutant. Rerun the affected mutation after a fix, identifying new evidence separately from the original run.
6. **Restore and verify.** Remove only the deliberate mutations and temporary configuration you own. Do not reset/clean a shared working tree to undo a probe. Inspect the final diff and rerun the focused and relevant containing suite against restored code. Keep wanted test improvements and unrelated work intact. If interrupted, verify restoration before continuing or handing off.

Example: tests at ages 17 and 19 allow both `>= 18` and `> 18` to pass. The mutation survives. Add the contract-derived boundary example at 18: it fails on `> 18` and passes on the original `>= 18`. This proves detection of that sampled defect, not all possible boundary defects.

## Classify results honestly

Keep raw tool labels and your interpretation distinct; tools do not all classify or score mutants identically.

| Observation | Interpretation and action |
| --- | --- |
| Relevant test fails on the intended changed behavior | Assertion-based kill. Preserve the test identity and failure reason. |
| Tests pass despite behavior violating the accepted contract | Surviving real gap. Add a discriminating test or report the unmet verification obligation. |
| Target is not reached or relevant tests were not selected | Coverage/selection gap, not equivalence or success. Check scope, imports, build output, and test discovery. |
| Changed implementation has the same accepted observable behavior for all relevant inputs | Equivalent mutation, with a specific justification. Do not add brittle tests to distinguish equivalent implementations. |
| Mutation affects behavior outside the agreed contract | Explain the scope boundary. Do not silently narrow an existing requirement or label an unknown survivor equivalent. |
| Syntax/type/build/setup/import/tool failure prevents the intended test | Invalid mutation or infrastructure failure, not a runtime assertion kill. Deliberate public type-contract checks are separate type evidence. |
| Timeout, flaky failure, cancellation, or interrupted run | Keep separate from assertion kills and investigate. A repeatable violation of an accepted time/liveness bound may be evidence for that bound; an unexplained timeout is not. |

For unknown survivors, retain uncertainty and the next useful check. A surviving mutant is not automatically a product defect: the real issue may be missing assertions, missing execution, equivalent behavior, or unsupported tooling.

If a tool reports a mutation score, include its version, definition/denominator, source/test scope, and raw counts for killed, survived, uncovered, invalid, timeout/error, and untested outcomes where available. State which categories the tool includes or excludes; do not silently recalculate a more flattering score. Compare scores only under comparable scopes/settings. A hand-selected sample is not a whole-suite mutation score, and 100% of generated mutants killed does not prove all behavior correct.

## Evidence without a new reporting stage

Put a short record in the existing verification notes or PR. No new ledger, approval, agent, or required document is introduced.

```text
Purpose: <accepted behavior and plausible defect>
Candidate: <revision plus relevant pending changes>
Method/scope: <manual or tool/version; source and selected tests>
Budget: <time/timeout/concurrency bounds>
Baseline: <command, collected tests, observed result>
Mutations: <IDs or diffs; observed failures/survivors/other outcomes>
Triage: <real gaps, justified equivalence/exclusions, unresolved cases>
Follow-up: <test improvements and rerun results, or remaining limits>
Restoration: <mutation removed; final diff and containing suite result>
```

For a trivial change with no material mutation-testing value, no extra record is required. When risk is material and the check is skipped/blocked, give the reason and alternative evidence rather than treating absence of the tool as a blocker by itself. Actual unmet mandatory behavior remains a blocker regardless of tool availability.

## Review and QA use

Assessment checks whether scope, baseline, classification, follow-up, and restoration support the claimed result. QA tries a plausible defect likely to slip through those checks: an uncovered guard, a mocked-away effect, stale generated output, or a survivor dismissed without evidence. Both perspectives remain bounded by the accepted task and permissions. Switching perspectives within one session is not independent review.

Language tool mechanics live in `golang-testing`, `typescript-testing`, and `python-testing`. Consult the installed tool's documentation before choosing version-specific commands and filters.
