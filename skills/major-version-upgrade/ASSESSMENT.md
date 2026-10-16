# Major Version Upgrade — Reviewer Assessment

Review a major upgrade as a migration across a breaking contract. The question is not whether the new version is present or whether CI is green; it is whether the repository has correctly absorbed the relevant compatibility changes and has honest evidence for rollout and recovery.

## Review criteria

1. **The transition is explicit.** The work identifies the old and target versions, the reason for the upgrade, affected environments, and any compatibility, rollout, persistence, or rollback obligations that materially shape the change.
2. **Every crossed breaking boundary was considered.** For skipped majors, the review can trace relevant migration/release guidance across each intervening major rather than only the destination version. Unsupported or uncertain vendor guidance is called out instead of guessed.
3. **The real coupling surface was inventoried.** Check more than imports: configuration, defaults, plugins, generated code, tests, CI/build tooling, schemas, serialized data, protocols, deployment files, observability, and external consumers where relevant.
4. **Baseline evidence exists and is interpreted correctly.** Pre-upgrade failures are distinguished from regressions. The upgrade does not hide unrelated red state or claim before/after improvement without comparable evidence.
5. **Breaking behavior was migrated deliberately.** Removed APIs, changed defaults, new runtime requirements, persistence/protocol changes, and new failure semantics are either adapted, intentionally accepted, or explicitly shown irrelevant.
6. **Transitive drift is understood.** Lockfile/dependency graph, plugins, runtime/toolchain, generated artifacts, and forced adjacent upgrades are reviewed. Unexpected resolver churn is not waved through merely because installation succeeds.
7. **Tests preserve the requirement.** Tests were not weakened to match the new implementation. They still discriminate accepted behavior from plausible regressions introduced by the major release.
8. **System-level proof matches the risk.** Build/type checks are not accepted as proof for runtime, data, protocol, mixed-version, or operational compatibility. The strongest claims have evidence at the boundary where failure would be observed.
9. **Rollout and rollback are truthful.** For non-atomic deployment or persistent/shared state, mixed-version behavior and rollback/restore obligations are addressed. A source revert is not described as recovery if new state or messages can make the old version incompatible.
10. **The migration is focused and finished.** Unrelated modernization is excluded; temporary shims and obsolete config are removed when no longer needed; required docs/CI/runtime declarations are updated; mandatory work is not deferred as optional follow-up.
11. **Evidence is bounded.** The PR or completion record says what was actually tested and what remains unverified. It does not generalize local green checks into universal compatibility.

## Evidence boundaries

- Release notes establish expected breaking changes; they do not prove this repository is compatible.
- A successful package resolution proves only that the resolver found a graph.
- Compilation proves only the compiled surface.
- Unit tests prove only the paths they exercise.
- A clean deploy in an atomic test environment does not establish rolling mixed-version safety.
- A reversible code diff does not establish reversible data or protocol state.
- A codemod completing successfully is not evidence that its semantic choices are correct.

## False-confidence patterns

Flag these when material:

- only the target release notes were read despite skipping multiple majors;
- lockfile churn is treated as noise rather than migration surface;
- changed defaults are left implicit, causing behavior to drift silently;
- tests were rewritten around new output without checking whether old accepted behavior should remain;
- a compatibility shim has no named consumer or removal condition;
- a rolling deployment is planned but only all-old and all-new states were tested;
- rollback assumes old code can read state produced by the new version without evidence;
- a new runtime/compiler floor is discovered after the code migration and treated as unrelated;
- an automated migration rewrote broad areas with little semantic review;
- the upgrade bundles cleanup or adjacent upgrades that are not required by the target.

Do not require ceremony for its own sake. Review the actual compatibility risks created by this specific major transition.
