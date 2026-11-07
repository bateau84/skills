# Strategic programming across two real changes

This manual exercise checks actual files and a fresh maintainer's follow-on
change. It is separate from the JSON response cases. The ordinary skill runner
is read-only and cannot execute it. No model run occurs when validating this
packet or running its provider-free integrity tests.

## Inputs and comparison

- [Seed project](fixture/README.md): Python 3.10+ and the standard library; three
  public Python entry points repeat an in-process retry policy.
- [First task](stage-1.md): accepted timed-out retry support.
- [Second task](stage-2.md): a newly revealed per-job retry permission.
- [Contract checker](verify_artifacts.py): evaluator-owned behavior checks.
  It does not decide whether the structure is good.

Use two identical disposable copies of `fixture/`, with ordinary file tools and
no external services or publication. For an instruction comparison, supply the
old and revised agent guidance while keeping skill bytes fixed. For a skill
comparison, keep agent guidance fixed and vary only the skill bytes. A combined
old/new agent-and-skill run checks integration, but cannot isolate which change
caused an outcome. Record that distinction.

Keep the starting tree, task text, model/settings, tool access and budget the
same across arms. Pin and retain the exact guidance each participant receives;
do not use a moving `main` as the baseline. Neither arm sees the other's work.
This trusted local exercise is not a sandbox for hostile agent code.

## First change

Give a fresh agent only its project copy, applicable practitioner guidance and
the text of `stage-1.md`. Do not disclose the second task, evaluator rubric,
contract checker or another participant's conversation. The project initially
has no HANDOFF.md. The agent chooses its own internal organization and relevant
verification. Do not prompt it to create a particular helper or abstraction.

After it finishes, preserve the resulting tree, diff, handoff, actual checks and
limitations. Run its tests from the project directory, then independently run:

```sh
python3 -I -B /path/to/evals/verify_artifacts.py /path/to/result --stage first
```

Keep the checker outside the participant workspace. Its source and expectations
stay unchanged while comparing arms. A failed first-stage contract remains a
failure; a later fix cannot retroactively make the earlier stage pass. Record
any repair separately and do not give one arm extra attempts without reporting
the changed conditions.

## Fresh follow-on change

Copy each first-stage result into a new directory. Start a new agent conversation
with that tree, the same arm's guidance and `stage-2.md` only. The next agent may
read the repository's HANDOFF.md, but receives no first-agent chat, final answer,
evaluation verdict or other-arm content.

Preserve its actual result and run its tests, then independently run:

```sh
python3 -I -B /path/to/evals/verify_artifacts.py /path/to/result --stage second
```

The checker exercises existing and added behavior through all three entry points:
eligibility, attempt limit, exact errors and precedence, permission defaults,
successful writes, requested-record selection, unrelated-record preservation,
diagnostic clearing and failed-save preservation. Expectations
come from the accepted task, not a helper in the implementation under test.
The fixture does not claim HTTP, CLI-process, concurrency or deployment coverage.

## Inspect the design and cost

Inspect actual call paths and both diffs alongside the behavior results:

- Does the preparation remove repeated policy or coordination, or only move it?
- Can the next agent find and change the relevant owner without reconstructing
  hidden rules? Trace what callers must know before and after.
- Are useful boundaries permitted even with one implementation? Are unrelated
  policies, unnecessary extension points or a god module introduced?
- Is the preparation bounded to the accepted work? Do public behavior, errors
  and material failure paths remain intact?
- Does the handoff preserve useful decisions and unresolved work without
  creating new requirements or claiming unrun checks?
- Compare total preparation, both feature changes, verification, review and
  repair effort. Record time/tokens only when observed with comparable methods.
  Fewer files, fewer tokens, a smaller diff or more refactoring is not a verdict.

Accept different sound organizations. A focused shared owner is one plausible
solution; a specific class, filename or number of files is never required.
When direct implementation wins, explain the observed trade-off. Include the
small-fix and speculative-framework response cases as restraint controls; this
fixture alone does not establish that an agent avoids unnecessary refactoring.

## Retain evidence and bound the claim

Use existing evaluation records. Retain input/task hashes, baseline and candidate
revisions, participant guidance hashes, model/settings and environment, original
dispatches and tool traces when available, both stage outputs or complete patches,
handoffs, commands/exit statuses and review findings. Record missing traces or
unmeasured costs explicitly. Confirm that each next-stage input matches the
previous output and that its checks imported the intended project.

Report behavior and design observations separately. A passing contract checker
proves only the exercised fixture behavior; it cannot prove better design.
One paired rehearsal is not evidence of general productivity improvement.
Repeat representative cases before drawing broad conclusions. A manual agent
rehearsal also does not prove native OpenCode skill discovery, deployed agent
permissions, independent Loom context controls or runtime enforcement.

Provider-free integrity checks from the skills repository root:

```sh
python3 -I -B scripts/tests/test_strategic_fixture.py
```

These establish that the seed meets its original contract, lacks the requested
feature, and that the checker rejects a broken attempt-limit comparison and an
implementation that ignores the requested job ID. They
are not agent behavior results.
