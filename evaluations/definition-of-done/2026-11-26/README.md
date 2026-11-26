# Completion ownership: focused lifecycle execution

The corrected candidate completed one actual **General → Coder → Reviewer → General** sequence. Coder returned local DONE with independent review still open. General dispatched a fresh Reviewer while keeping the parent PARTIAL, then declared the parent DONE only after the independent review and combined acceptance. This is the focused execution counterpart to the agents fixture `done-shared-quality-owner-lifecycle`.

This record addresses the cross-agent ownership ambiguity reported against agents PR #17. It supplements the [earlier samples](../2026-11-25/README.md); their source hashes and observations remain unchanged. It does not reproduce the alleged failure under the older agent instructions or establish an efficiency improvement.

## Observed sequence

| Transition | Local result | Parent state and remaining owner |
| --- | --- | --- |
| General dispatches Coder | Implementation, regression verification and documentation assigned to Coder. | PARTIAL; independent review belongs to Reviewer, combined acceptance to General. |
| Coder returns | DONE; real CSV repair, updated documentation and five passing tests. | PARTIAL; review remains mandatory and open under Reviewer. |
| General dispatches Reviewer | A different agent starts with `fork_turns="none"`, accepted requirements, current source and raw test output. Producer assessments are excluded from its initial context. | PARTIAL; dispatch alone does not establish review completion. |
| Reviewer returns | DONE / APPROVE; source coverage and five independently rerun tests support the bounded verdict. | PARTIAL; General still owns combined acceptance. |
| General accepts the combined result | Both contributions satisfy the unchanged contract. | DONE; no open obligation remains at the accepted parent boundary. |

The [five-event record](lifecycle/records/events.jsonl) carries the owners and evidence references at each transition. The supervisor separately [captured the live intermediate state](lifecycle/records/supervisor-at-review.json): Coder was complete, the distinct Reviewer was running, and no final parent handback existed. These are recorded semantic completion states, not native Loom status transitions.

## Inputs and evidence

- [Accepted contract](lifecycle/project/CONTRACT.md) and [General request](lifecycle/REQUEST.md).
- Exact [General](lifecycle/records/general-dispatch.json), [Coder](lifecycle/records/coder-dispatch.json) and [Reviewer](lifecycle/records/reviewer-dispatch.json) dispatch arguments and returned agent IDs.
- [Original fixture](lifecycle/before) and [resulting project](lifecycle/project). Only the exporter, tests and behavior README changed; the contract and unrelated cache file remained unchanged.
- [Coder handback](lifecycle/records/CODER.md), [independent review](lifecycle/records/REVIEWER.md) and [General acceptance](lifecycle/records/RESULT.md).
- Raw [baseline failure](lifecycle/records/baseline-tests.txt), [Coder run](lifecycle/records/coder-tests.txt), [Reviewer run](lifecycle/records/reviewer-tests.txt) and [supervisor rerun](lifecycle/records/supervisor-tests.txt).
- [Manifest](manifest.json): repository bases, candidate instruction hashes, reported instruction use, retained-file hashes and limitations.

The original module produced **two passing tests and one escaping failure**. Coder repaired the exporter with the standard library and expanded relevant checks to both columns, newline forms, exact record endings and existing value conversion. The final suite has **five passing tests**, independently rerun by Reviewer and the supervisor. The failing baseline establishes the fixture's CSV bug; it is not a pre-correction agent baseline.

## Method and limits

All three roles were fresh collaboration agents. The General request contained the accepted task and observation requirements, not the evaluation rubric or an expected verdict. General produced the specialist requests under the candidate charter. Reviewer first formed source observations without producer conclusions; General subsequently confirmed that no earlier unresolved finding required reconciliation.

The supervisor also sent [two retained messages](lifecycle/records/supervisor-messages.json), requesting exact dispatch capture and a progress note about remaining verification. The latter restated the accepted boundary and continuation. This was a supervised focused execution, not an unaided comparative trial.

Candidate charters and supplied completion skills were checked against the recorded SHA-256 values. General loaded no methodology skills. Coder used the supplied `software-engineering` plus four unpinned installed helpers; Reviewer used supplied `software-engineering` and `product-acceptance`. Other completion skills made available to the agents are distinguished from reported use in the manifest. Full tool traces were not exported; the retained records cannot establish every individual read or recreate an exact model session.

The observations support the demonstrated local-to-review-to-parent transition on Python 3.12.14. They do not establish reduced tokens, time, cost or scope drift, effectiveness across models, native OpenCode/Loom behavior, or every missing-owner, failed-proof and review-defect path. The full model-backed fixture suite and a matched comparison were not run. Structural fixture validation remains separate from this behavioral observation.

## Reproduce

1. Copy `lifecycle/before/` into a new disposable `project/` and create an initial local Git commit if the reviewer needs a diff. The new commit identity may differ; the input file hashes must match the manifest.
2. Supply the candidate role files and named skill directories identified in the manifest as `instructions/`. Verify their hashes. Create an empty `records/` directory.
3. Adapt the absolute temporary paths in the saved request and dispatch input to that workspace. Start a fresh General with the saved General dispatch and actual fresh specialist delegation available. Do not supply this README, previous results or evaluation expectations to the producer or initial Reviewer.
4. Observe actual delegation, source edits, local status, open parent obligations and independent review. Save the outputs before interpreting them. Run `python3 -B -m unittest -v` from the resulting `project/` to check the retained code independently.

For a controlled comparison, pin the model, both repositories, all helper skills, permissions and host context on each side. This record makes no such comparison claim. These files are evaluation evidence, not a new required work-report format.
