---
name: github-actions-lockfile
description: Generate, maintain, troubleshoot, and security-review .github/workflows/actions.lock with gh actions-lock. Use when onboarding GitHub Actions workflows, changing uses dependencies, relocking moved tags, investigating invalid or corrupt lockfiles, setting up CI verification, or diagnosing missing pins, local-action coverage, and provenance findings. Not for general workflow trigger, runner, or permissions design (use github-workflow).
---

# GitHub Actions Lockfile

Use `gh actions-lock` to generate the repository's `.github/workflows/actions.lock` and verify its provenance. **Treat the file as generated security state, not editable configuration.** A passing command proves only the checks that command performs; it does not establish that the action code is benign or that unrelated workflow trust boundaries are sound.

The extension is a pre-1.0 external dependency. Check the installed version and `gh actions-lock --help` before relying on flags, output shape, or exit semantics. If a flag or behavior differs from this skill, follow the installed CLI and current upstream documentation; do not invent an equivalent flag or claim verification happened.

## Security invariants

- Never hand-edit, synthetically reconstruct, or blindly replace `actions.lock`. Diagnose unexpected content or diffs, correct source workflows as needed, then regenerate using the CLI. Preserve evidence of suspicious changes before repair.
- Never automatically use `--accept-moved`, and never use it in CI. `unreachable-pin`, `repo-replaced`, `misleading-sha`, or unexplained `owner_id`/`repo_id` changes are security investigations, not routine maintenance.
- Do not run `--relock` just to make a failing check green. It can change executable commits; review the proposed update and upstream history/release notes first.
- Do not ignore the exit code, discard diagnostics, or confuse `--verify-local` with `--verify`. Do not treat warnings as resolved because `.valid` is true. `--no-onboard` intentionally excludes new workflows/actions and must never be used to claim full coverage.
- Never weaken a workflow, drop lock coverage, disable enforcement, or use `--ignore-local-actions` merely to silence a failure. Document and obtain acceptance for a real exception.
- Limit edits to requested repositories and authorized files. Preserve unrelated worktree changes; don't stage unrelated changes or commit/push without authorization. Host tool/approval policies still apply.

## Preflight: establish target and trust context

1. Confirm the repository root (`git rev-parse --show-toplevel` where `.git` exists), remote host, target branch, and `.github/workflows` directory. Inspect `git status --short` and existing workflow/lockfile diffs before any write. Distinguish pre-existing edits from your own; stop before overwriting an unclear change.
2. Confirm `gh` and extension availability (`gh --version`, `gh extension list`, `gh actions-lock --version`, `gh actions-lock --help`). If absent, install only when authorized: `gh extension install github/gh-actions-lock`. On a `*.ghe.com` tenant, use the full `https://github.com/github/gh-actions-lock` URL when the short name resolves against the tenant. Record the tested extension version for reproducibility.
3. Verify host and authentication with `gh auth status --hostname HOST`, not by printing tokens. Host selection is `--hostname` > `GH_HOST` > repo context (`GH_REPO`/known remote) > github.com. `GH_TOKEN` overrides `GITHUB_TOKEN` and saved credentials on the selected host. Investigate unintended overrides without displaying secrets (for example, `env -u GH_TOKEN -u GITHUB_TOKEN gh auth status --hostname HOST`).
4. Support github.com and GitHub Enterprise Cloud data residency (`*.ghe.com`); **do not claim GitHub Enterprise Server support**. For `*.ghe.com`, public github.com action reads use `GH_ACTIONS_LOCK_GITHUB_COM_TOKEN`, then saved github.com login, then anonymous access—not the tenant token. In CI, configure separate minimal read credentials if needed; never echo or embed them in files.
5. For a partial checkout without `.git`, set `GH_ACTIONS_LOCK_REPO_ROOT` only to the confirmed repository root containing workflows. Confirm that its `$/` paths resolve to the intended repository. A missing workflow tree or wrong root is a blocker, not an empty success.
6. Identify local composite actions, remote reusable workflows (`jobs.<id>.uses`), Docker/container images, private dependency repositories, and repository/organization pinning or allowed-action policies. These affect coverage and runtime acceptance.

## Select the least-risk command

| Intent | Command | Meaning |
| --- | --- | --- |
| Offline local coverage check | `gh actions-lock --verify-local` | No network/writes. Does **not** establish provenance. |
| Read-only diagnosis | `gh actions-lock --no-fix --json=valid,findings` | Reports findings without writing; examine status and stderr. |
| Frozen authoritative check | `gh actions-lock --verify` | Network verification; suitable for required CI check. |
| Onboard/fix all workflows | `gh actions-lock` | Mutates workflows and lockfile when fixable. |
| Onboard/fix one workflow | `gh actions-lock .github/workflows/ci.yml` | Scoped mutation; not a complete repository audit. |
| Advance refs intentionally | `gh actions-lock --relock` | Resolves currently upstream commits; requires dependency update review. |
| Approve exceptional history movement | `gh actions-lock --accept-moved` | Human-authorized only, after investigating why the locked pin is unreachable. |

`--json` selects output format; it **does not** make a command read-only. To keep versions parseable, use `--json=valid,findings,workflows,dependencies,pins` only if the installed CLI supports those fields. Machine-readable output is on stdout, progress/errors on stderr. Preserve the process exit status (avoid masking it with `| jq`). A retryable API/rate-limit error is not grounds to regenerate or accept a moved ref. Failed runs normally print a cache log path containing their complete JSON report, target repository and error; inspect those logs for diagnosis, but check for sensitive details before sharing, and do not assume they are retained indefinitely. Use `--no-interactive` for unattended operations when supported, without weakening failure handling.

## Onboard or repair a repository

1. Run `gh actions-lock --no-fix --json=valid,findings` and inspect every error/warning and its `remediation`/`doc_url`. First reconcile unexpected pre-existing edits and suspicious pins; do not start with a destructive rewrite.
2. Review each workflow's `uses:` and action provenance. Check intended upstream owner, intended version/ref, and remote reusable workflow calls. Correct unsupported/misconfigured workflow sources first.
3. Run `gh actions-lock` from the verified root. A default run covers the complete workflow directory and can prune entries for deleted workflows. A path-scoped run **does not** perform whole-repository pruning.
4. Expect newly pinned partial semver tags (`v4`, `v3.2`) to be narrowed to the highest matching full semver tag. It may change workflow YAML as well as `actions.lock`. Use `--no-narrow` only for a deliberate mutable-ref policy exception; never assume it makes a ref immutable. Already locked dependencies are not automatically advanced by a plain run.
5. Examine `git diff -- .github/workflows/` and any affected `action.yml`/`action.yaml`, not just the lockfile. For each changed SHA, compare with the intended upstream release/history; investigate changed `owner_id` or `repo_id` as a potential repository replacement. Confirm there are no unrelated edits, unexpected downgrades, missing workflows, or edited token/permission settings. Never automatically approve a green but unexpected diff.
6. Run a full-directory `gh actions-lock --verify` and `gh actions-lock --verify-local`. Inspect reported warnings, then check `git status --short` / diff again to confirm verification performed no writes. Report unresolved coverage gaps explicitly.
7. Propose staging **only** reviewed workflow, local action, and lockfile files together. Never stage an entire `.github/` tree without inspecting it. Leave committing, pushing, or merging to the user's authorization and repository policy.

If a lockfile is malformed or apparently tampered with, preserve its diff and compare with Git history; do **not** patch the YAML manually. Resolve the cause (misconfiguration, tool compatibility, or malicious edit), regenerate with the trusted CLI, review the changed executable commits, and re-verify. If the cause cannot be established, stop and report the unresolved security concern.

## Maintain pins without accepting an attack

- Run the full frozen verification after **every** workflow `uses:` or local action change, on PRs, and periodically against the protected default branch. Dependabot can update existing onboarded entries but does not onboard newly introduced workflows for you.
- For a new or stale dependency, run plain `gh actions-lock` and inspect the diff. For intentional updates of already-locked moving refs, inspect the upstream change and run `--relock`; review all changed commits, including transitive composite dependencies, then verify.
- Classify a moved version tag separately from a moved branch/major tag: a full semver tag unexpectedly moving is high signal. If a pin is no longer reachable, halt; compare repository identity and upstream history (including force-push/takeover), identify the intended safe commit, and require an explicit human decision **before** `--accept-moved`. It is never an automatic recovery option.
- If an upstream repository is renamed, deleted, replaced, or unreadable, distinguish access failure from identity substitution. Do not work around `repo-replaced` or `misleading-sha` with `--relock` or accepting moves.
- If JSON reports `retryable: true`, verify connectivity, host/token selection, and rate limits, then retry without writes. Distinguish tool execution errors from blocking dependency findings; neither is a clean verification.
- If installed CLI supports `--fail-on-warning`, consider it for read-only policy checks when *all* warnings should block. Its absence from an older `--help` is not permission to claim warning-free verification.

## Coverage that needs separate decisions

- **Remote reusable workflows:** `jobs.<id>.uses` references to another repository are not locked by the caller's `actions.lock`; pin the called workflow to its full commit SHA and verify that the source repository is locked when applicable.
- **Local actions:** `uses: ./…` executes against the checkout workspace and is not traversed by the lock tool. If it uses remote actions, the CLI may fail for missing coverage. Prefer a reviewed `--migrate-local-actions` change to `uses: $/…` when the action must execute at the workflow commit. This changes semantics; inspect workflows and action files. The CLI behavior for rewriting nested `action.yml` files has differed between versions, so inspect what actually changed. `--ignore-local-actions` is an explicitly reviewed exception only after proving any necessary remote pins are covered for that same workflow; it can otherwise fail at runtime after earlier steps executed.
- **Images:** Docker/container references are not locked. Review/pin relevant images by digest (`@sha256:...`) and keep this outside the lockfile integrity claim.
- **Trust beyond dependency resolution:** The lockfile cannot validate a publisher's source code, event triggers, job permissions, tokens, secrets, runner isolation, or artifact/cache trust. Apply `github-workflow` for those concerns.
- **Rollback inside reachable history:** A floating ref can be pinned to an older but reachable commit without failing verification. Read every changed SHA and intended release/version; verification is not a substitute for reviewing the diff.

## Enforce it in CI and review

- Use the upstream `verify-lockfile.yml` as a reference, or adapt `examples/verify-lockfile.yml` from this skill. Pin a reviewed **extension release** for reproducible CI bootstrap, use `permissions: contents: read`, keep checkout credentials nonpersistent, and run `gh actions-lock --verify` as a required, **non-mutating** PR check. Do not auto-repair from an untrusted PR job.
- Run a scheduled verification against the protected default branch if upstream ref movement should trigger an alert between PRs. When the verification workflow itself is introduced or changed, run `gh actions-lock` to include its action dependencies.
- Protect the check with branch rules; add `.github/workflows/actions.lock` and verification workflow(s) to `CODEOWNERS`, requiring appropriate review of executable pin changes. A PR that can simply disable the checker is not protected by the checker.
- On supported GitHub Enterprise Cloud installations, consider piloting the **Require lockfile** policy in Evaluate mode before activating enforcement. Ensure every targeted workflow is onboarded, including workflows with no `uses:` entries. Confirm compatibility with allowed-actions and full-SHA pinning policies, which evaluate the locked commit.
- Use least-privilege read access for private/internal action repositories; for `*.ghe.com`, keep tenant and public github.com credentials separate. Never use `--accept-moved` in automated checks.

## Deliver evidence, not a green assertion

Report the repository/ref and host, installed extension version, mode(s) run and status, workflows scanned, `actions.lock` and workflow diffs, added/changed commit SHAs and repository identities, outstanding warnings, uncovered reusable workflows/local actions/images, and whether CI/protection is active. Distinguish **verified**, **fixed but unverified**, **blocked/suspicious**, and **not assessed**. Do not claim a command ran if the agent cannot execute it in its host.

Current authoritative references: [extension and CLI](https://github.com/github/gh-actions-lock), [GitHub lockfile semantics](https://docs.github.com/en/actions/concepts/security/workflow-dependency-lockfiles), [onboarding and moved refs](https://docs.github.com/en/actions/how-tos/secure-your-work/lock-workflow-dependencies), [enforcement](https://docs.github.com/en/actions/how-tos/administer/enforce-workflow-lockfiles). The upstream skill is available via `gh skill install github/gh-actions-lock`; this companion provides stricter operator judgment and review boundaries without replacing the official CLI.

Optional independent perspectives: [conformance assessment](ASSESSMENT.md), [adversarial validation](QA.md). They do not grant extra privileges.
