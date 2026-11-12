# Evaluation integrity triage — 2026-11-11

## Evidence and limits

The maintainer reported an exploratory Claude Code comparison of all **392 cases / 59 skills** at base commit `67794eb`: baseline 257/392, with-skill 362/392, with 108 baseline-fail/candidate-pass, 3 regressions, 254 both-pass and 27 both-fail. These are **reported**, not independently reproduced in this PR. The original `grades.json` outputs were not available for inspection here.

The exploratory procedure reused one answerer context per skill, always answered baseline first, then loaded the skill; one grader per skill saw both outputs, with short answer caps. This is useful for triage but does not establish a causal effect size or a production readiness score. Do not compare it as a controlled result to the pinned OpenCode harness or treat the 254 both-pass cases as proof of zero marginal value. The narrative for `architectural-design` also disagreed with its per-skill table (2/5 versus 3/5 candidate); reconcile grades before aggregating.

## Corrections in this change

- **Design deliverables:** Require concrete applicable state/action/feedback/focus/recovery decisions, distinguish validation/server/network and TUI startup failures; prototype actual requested states and partial-effect CLI transcripts; make architecture crash/effect boundaries and real alternative trade-offs explicit.
- **Misgraded scenarios:** Fix the contradictory typed-nil criterion; make the variable-shadowing example actually swallow an error; distinguish GC concurrent marking from STW pauses; remove mandatory telemetry from a path-confinement fix; make `time.After` evaluation Go-version-aware.
- **Contract-dependent obligations:** Audit integrity, loss tolerance, retention and synchronous durability must be derived from the actual audit requirement, not imposed as universal WORM/synchronous rules. Transaction ownership cannot be presumed when the caller contract is missing.
- **Incorrect API assumptions:** A dynamic `map[string]bool` Swagger response is not automatically unsupported; verify the generator's emitted schema. Preserve the meaning of a dynamic map rather than replacing it with arbitrary fixed fields.
- **Fixture clarity:** Fix the web-component eight-state count and give the prototype-transition case the artifact it asks the model to inspect, without revealing the missing transition as the answer.

This changes existing fixtures in place; source IDs and case population are preserved. These are corrections to the *test contracts*, not evidence of improvement in a rerun. Changes to a skill and its development fixtures are **not independent holdout evidence**; evaluate generalization with separate unchanged scenarios and actual work outcomes.

## Follow-up evaluation discipline

1. **Validate fixtures before model calls:** `bun run eval:validate` and `bun run eval:harness-test` using the repository's pinned clean runner. If runner/OCI is absent, report those checks as unrun rather than substituting a different result.
2. **Isolate paired conditions:** Fresh, independent answerer contexts for baseline and candidate, same task/model/tool constraints, independent rubric grader, and evidence of actual skill content loaded. Randomize A/B presentation where the harness permits, and review disagreements/borderline criteria.
3. **Measure substance:** Judge actual code/tests, design artifacts, or authorized tool effects when that is what the task requests. Avoid scoring headings and checklist vocabulary unless the accepted output format specifically requires them. Check for invented facts, unsafe behavior and reduced usefulness.
4. **Maintain two suites:** Preserve easy safety/regression guards, but add a bounded set of harder discriminating cases drawn from real incidents and cold reviews, with untouched holdouts. Do not repeatedly optimize skill wording against these same fixtures.
5. **Report meaningful denominators:** Paired fixed/regressed/both-pass/both-fail, case selection, sample and grader variation, tool/model/environment version, observed first-pass correctness, eventual corrections, cost and failure severity. A corrected fixture invalidates direct comparison to older scores.

## Not covered

This PR does **not** replace the external runner, resolve Claude credential isolation/billing, certify any live provider run, or repair every both-fail/both-pass case. Existing draft [skills PR #28](https://github.com/bateau84/skills/pull/28) owns the separate Claude Agent transport integration. Broader architecture, SQLite and suite-strengthening work remains follow-up scope after the corrected baseline is rerun.
