---
name: git-commit-discipline
description: Small coherent commits, explanatory messages, shared-working-tree discipline, and safe undo/recovery. Use when asked to commit, when a diff mixes concerns, when agents share a working tree, or when undoing or recovering Git changes. Not for content conflicts (use git-conflicts).
license: MIT
metadata:
  author: Bateau
  version: "3.0.0"
---

# Git Commit Discipline

Commits serve as recovery checkpoints and explanations for future maintainers. This method grew from an incident in which a destructive reset erased a long session's uncommitted work. It does not authorize commits, publication, history rewrites, or hook bypasses by itself.

## Scope and checkpoints

When commits are requested, commit at coherent verified checkpoints rather than accumulating unrelated work. When commits are not requested, keep the diff coherent and report completed work without making a commit.

Before committing, inspect status, the working and staged diffs, and recent history. Match repository message conventions; never stage unrelated work, secrets, or temporary reports.

```bash
git status --short
git diff --stat
git diff
git diff --cached
git log --oneline -10
git add -- path/to/fileA path/to/fileB
git diff --cached --check
git diff --cached
git commit -m "<subject>" -m "<why and verification>"
```

Preserve repository hooks. If a hook fails, inspect the outcome, fix the issue, re-verify, and follow local instructions before trying again. Do not disable hooks as a convenience.

## Split by concern

A bug fix, unrelated refactor, and new feature normally deserve separate commits. Each should be explainable and independently revertible. Stage explicit files; use interactive hunk staging only if the host supports and permits it. Inspect the staged result and verify each proposed checkpoint makes sense on its own.

Do not use broad staging when the tree contains more than one concern or another contributor's work. Generated artifacts and lockfiles follow repository policy; stage them only when they are intentional consequences of the scoped change.

## Explain why

Follow the project's existing format. Where Conventional Commits are used:

```text
<type>(<scope>)!: <subject>
```

The subject is a quick index for people and tools. For non-trivial work, add enough body to explain background, goal, reasoning/trade-offs, key changes, verification, and meaningful follow-ups. These are content prompts, not mandatory headings. A typo correction may need only a subject.

Verification should name actual checks and outcomes, including limitations. Do not invent evidence. For breaking changes, include migration impact and the project's breaking-change marker, such as `!` and `BREAKING CHANGE:`.

```text
fix(auth): reject expired refresh tokens

The refresh endpoint checked signatures but ignored expiry, allowing
stale tokens to create new sessions. Validate expiry before issuing
replacement credentials, using the same clock as the access-token path.

Verification: focused expiry and boundary tests passed; auth suite passed.
```

## Shared working trees

If multiple agents or contributors share a tree, the index and files are shared mutable state. No automatic locking or isolation is assumed.

- Prefer separate worktrees or an agreed serialized commit owner when available.
- Stage only the agreed scope; account for every staged line before committing.
- Coordinate overlapping edits and index mutation. Re-read files after another writer changes them.
- Do not delete, restore, or commit unexplained sibling changes.
- Do not delete `.git/index.lock` blindly; investigate the owning process and stop if ownership is unclear.

## Safe undo

Clarify the intended outcome when "undo" is ambiguous. Choose the narrowest operation that preserves recoverability and obeys the user's request and host permissions.

| Intended outcome | Typical operation | Important boundary |
| --- | --- | --- |
| Discard specified uncommitted files | `git restore -- <paths>` | Destroys those edits; confirm scope and ownership. |
| Preserve edits before changing context | `git stash push` | Include untracked files only intentionally; inspect before dropping. |
| Undo a shared commit | `git revert <sha>` | Adds an inverse commit without rewriting shared history. |
| Undo a local commit while keeping edits | `git reset --soft <sha>` or `--mixed` | Moves history; requires authorization for that outcome. |
| Permanently discard work/history | `git reset --hard <sha>` | Only with explicit authorization and a recoverability check. |

Before destructive operations, inspect the exact affected paths/history, record HEAD, and preserve wanted edits with an appropriate backup or checkpoint. For cleaning, preview the same scope with `git clean -n` and the intended flags. Do not chain destructive commands after failure or use them to resolve uncertainty.

Publish only when requested. For an authorized history rewrite, prefer `--force-with-lease` over plain force, and verify the expected remote state; the lease protects against unexpected remote movement, not against an incorrect local rewrite.

## Recover lost work

1. Stop further destructive operations and identify what was lost.
2. For orphaned commits, inspect `git reflog`, confirm the candidate, and create a recovery branch before deciding how to restore it:
   ```bash
   git reflog show HEAD
   git branch recovered-work <verified-sha>
   git log --oneline recovered-work
   ```
3. Reflog does not record never-committed file content. For lost uncommitted work, inspect editor local history, backups, stashes, or host snapshots **if available**. Do not assume an agent tool captured a snapshot. Previously staged objects may sometimes be recoverable, but recovery is not guaranteed.
4. Inspect candidate content before restoration, protect current edits, and restore only explicit paths. Verify the diff and applicable checks afterward.
5. If no reliable candidate exists, report what can and cannot be recovered rather than guessing or running more resets.

Use `git-conflicts` for merge/rebase/cherry-pick content conflicts and `pr-educational-body` for pull-request explanations.
