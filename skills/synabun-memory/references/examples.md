# Choosing and distilling memories

These are fictional teaching examples, not observations about any user's repository. Never store them as real project history. Replace source placeholders with evidence actually inspected.

## Architecture that proved useful

Weak: “The immutable event architecture is excellent. We spent three days on it.”

Useful: “For a job service with retries and independent review, separating immutable execution attempts from the current task summary let us rebuild state without overwriting the original evidence. In the replay test at <commit/report>, replay preserved completed attempts while recalculating the current summary. Prefer this separation when historical execution facts must survive policy changes. It adds migration and projection code; it is not justified for every small script. Observed <date>.”

Why keep it: it identifies a reusable constraint, benefit, demonstrated behavior, and cost. Approval of the architecture alone would not justify the demonstrated-behavior claim.

## An implementation worth finding again

Weak: “Finally fixed indexing. The code is really good now.”

Useful: “During <project/version> watcher recovery, normal file events resumed but files changed during the outage stayed stale. Reconciliation on recovery was needed in addition to restarting the watcher. The regression at <test/commit> covers changes made while the watcher is stopped and checks the rebuilt index afterward. Keep the reconciliation path when modifying recovery; a healthy watcher alone does not prove a current index. This result covers <tested conditions>, not every remote filesystem. Observed <date>.”

Why keep it: a future maintainer can recognize the trap and find the good implementation without replaying the debugging session.

## A lesson from failure

Weak: “Never trust tests. Mutation testing is always necessary.”

Useful: “The <validator> test passed even when the production condition was removed because the assertion checked only that the function returned. Replacing it with an output assertion caught that deliberately introduced fault in <test/commit>. When testing a rejection rule, demonstrate that the test fails when the rejection is bypassed. This only establishes sensitivity to the tested fault; it does not prove the suite catches every defect. Observed <date>.”

Why keep it: it preserves the failed assumption, causal explanation, prevention step, and scope instead of a sweeping slogan.

## A failure whose cause is not known

If repeated observations make the symptom useful, save only the supported part: “On <version/platform>, <operation> stalled in three runs after <condition>. The cause remains unknown; <suspected mechanism> is untested. Reproduction and logs: <source>. Capture <diagnostic> before restarting next time.”

Do not convert a guessed cause into a known fix. If there is no repeat-use value yet, keep the investigation in its normal issue or report rather than memory.

## Duplicate with new evidence

Existing lesson: the recovery path must reconcile the index.

New result: a second, genuinely independent regression test covers directory moves during the outage.

Action: fetch the existing record, add the new evidence and expanded applicability, and preserve its original limits. Do not write another near-identical memory or call three agents citing the same test “three confirmations.”

## Changed implementation, retained lesson

The original polling fallback is removed after a reliable watcher replaces it.

Action: retire the claim that polling is the current implementation. Keep the supported lesson about recovering missed changes if the new design still faces that risk. Link the old decision to its replacement where supported; do not leave the obsolete implementation advice looking current.

## Old, rare, valuable

A rarely recalled memory explains a destructive restore failure that occurred two years ago. The affected restore mode still exists and the recovery test is still relevant.

Action: keep it. Its age and low access count are not evidence that the risk has disappeared.

## Nothing to remember

A task renames a helper, passes its existing tests, and introduces no new constraint, pattern, or failure lesson.

Action: finish the task without creating a memory. The commit already records the change.

## From experience to a reusable rule

Several independent projects repeatedly establish the same technique and its limits.

Action: propose an update to the relevant engineering skill or project guidance through its normal change process. Keep memory as evidence and a source pointer. Do not silently promote one anecdote into a global instruction, or create a second copy of every document in the memory store.
