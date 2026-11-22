# GitHub Actions Lockfile — Conformance Assessment

Assess whether the requested repository's lockfile lifecycle was correctly carried out. This is a **review** of observed work, not a fresh repair procedure or an authorization to modify the repository. Use `SKILL.md` for normal practice, `QA.md` for adversarial attempts to falsify confidence.

## Confirm evidence and scope

1. Identify exact repository, host, ref/branch, worktree baseline, requested scope, installed extension version, and commands actually executed. Distinguish a local run from CI proof; don't infer either from files merely existing.
2. Confirm the source workflow tree was complete, and whether any command was scoped to a subset. Check that deleted-workflow entries were pruned by a full-directory run where applicable; a path-scoped success is not repository-wide proof.
3. Verify the lockfile was machine-generated rather than hand-authored, that workflow edits and lockfile reflect one coherent change, and that no unrelated edits, staged secrets, or unauthorized repairs were made.
4. Require a successful full `gh actions-lock --verify` under the intended host/authentication context. `--verify-local`, `--no-fix`, syntax validation, and a `.valid` JSON field from an unknown command mode cannot substitute for this. Report tool failure, network/rate limits, and unexecuted verification separately.
5. Inspect findings, warnings, and their remediation/doc URLs. A check that exits 0 with warnings can still need explicit risk decisions.

## Examine executable changes and coverage

- Inspect every changed dependency `commit`; compare with intended version and upstream history. Check `ref`, `owner_id`, `repo_id`, dependency removals, and suspicious downgrades. Green provenance checks do not prove code safety.
- Confirm changed full semver tags were reviewed as security-relevant events; record any branch/major-tag changes deliberately re-locked.
- Confirm there was **no** automated `--accept-moved` and no unexplained `--relock`; moved/replaced/reachable-only pins were investigated rather than normalized.
- Find `jobs.<id>.uses` in other repositories and assess their separate full-SHA/source-lock coverage. The caller's lockfile doesn't protect them.
- Find `uses: ./…`, `uses: $/…`, and any nested remote dependencies. Review whether migration altered execution semantics; a local-action warning downgrade is not proof of complete coverage.
- Account for Docker images not locked by the tool, particularly mutable tags or expressions not protected by digest references.
- Check that default-branch and PR verification are enabled as intended, the extension bootstrap version is controlled, tokens are scoped/read-only, and verification workflow/lockfile edits require review. Check whether repository policy enforcement is merely suggested, piloted, or actually active.

## Outcome

State one of:

- **PASS (defined scope):** full applicable verification succeeded, change provenance and diff reviewed, and uncovered surfaces/risks are explicitly documented.
- **BLOCKED:** security-significant moved/replaced identity, changed pin without acceptable explanation, invalid provenance, corrupt file with unknown cause, missing authoritative verification, or a bypassed required control.
- **LIMITED:** run was partial/offline, warnings or unsupported surfaces remain, or CI enforcement was not tested; name precisely what is and isn't proven.

Include direct command output/CI links and changed SHA evidence where available. Do not call an agent's self-review independent.
