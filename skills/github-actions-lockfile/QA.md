# GitHub Actions Lockfile — Adversarial Validation

After ordinary production and conformance review, try to disprove the assurance claim. Use isolated fixtures or read-only repository inspection unless an authorized test workspace permits mutation. A passing `gh actions-lock --verify` is an important signal but not a proof that the pinned executable is desirable.

## False-green attacks to exercise

1. **Reachable-history rollback:** Replace a floating-ref locked commit with an older commit still in the same ref's ancestry in an isolated fixture. Verification may accept this. Does review identify the unexplained rollback through base-to-head diff and version/history evidence?
2. **Identity substitution:** Test an apparent same-name action after repository replacement, or alter `owner_id`/`repo_id` in an isolated lockfile. Does the operator stop, retain evidence, and investigate rather than regenerate until the error disappears?
3. **Forced history movement:** Simulate an `unreachable-pin` / repointed full semver tag. Verify no unattended `--accept-moved` or mechanical `--relock` clears it. Require a human-understood upstream explanation.
4. **Coverage illusion:** Make offline coverage pass while online provenance verification fails. Does the report distinguish modes and retain stderr/exit status (including pipeline failures)?
5. **Path-scoping and no-onboard trap:** Verify only one workflow, or re-pin with `--no-onboard`, while another newly added workflow or deleted-workflow lock entry remains. Does the operator refrain from calling it repository-wide verification?
6. **Local-action blind spot:** Insert a `./` composite that invokes a remote action absent from the workflow lockfile. Does the operator catch the runtime failure risk instead of uncritically using `--ignore-local-actions`? For a `$/` migration, verify a changed checkout-workspace assumption is considered.
7. **Unprotected dependency class:** Reference a remote reusable workflow by a mutable tag or container image by tag while all normal action entries verify. Does the final security claim explicitly exclude these surfaces and propose proper controls?
8. **Checker self-bypass:** In a PR, modify the verify workflow to skip verification or give the job write rights, together with a lockfile change. Does branch protection/CODEOWNERS and review catch a bypass even if current CI is green?
9. **Enterprise auth confusion:** Configure a tenant `GITHUB_TOKEN` plus public github.com action lookup on `*.ghe.com`. Does the operator avoid leaking the tenant token to github.com, distinguish rate limits from corruption, and request the separate public-read token only where necessary?
10. **Tool/format drift:** Use a version lacking `--fail-on-warning` or with changed JSON/finding categories. Does the operator check `--help`, avoid making up output, and report uncertainty instead of implying the newer behavior ran?

## Challenge the evidence

For each test, state the fixture/repository and host, actual command or inspection, observed exit/status and diff, what the ordinary process would have concluded, and whether the risky state was detected. If a scenario was only reasoned about, mark it **not executed**. Do not change the real lockfile to stage an attack without explicit authorization.

QA is successful when the implementation/report narrows its claims or blocks a false-green state; it is not measured by forcing every fixture to produce CLI exit 1. Residual limits (malicious code in an authorized commit, compromised reviewer, weak organizational controls) remain out of scope for the lockfile alone.
