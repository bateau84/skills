# golang-testing Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer checks whether tests prove the claimed behavior under Go’s execution model:

- table/subtests copy/capture loop variables correctly and use `t.Parallel` only with isolated state; package/global env/process state is restored with `t.Cleanup`;
- assertions target observable behavior/invariants and failure paths, not implementation trivia;
- temp files/dirs, clocks/randomness/network/database dependencies are deterministic enough without bypassing the behavior under proof;
- race-sensitive code has `-race`/stress or targeted concurrency evidence when applicable; sleeps are not the only synchronization proof;
- mocks/fakes sit beyond the intended test boundary; state is produced by the real upstream product behavior for integration/acceptance claims;
- `t.Fatal`/helper behavior, cleanup, goroutine failures, and error assertions cannot hide failures in background goroutines;
- skips/xfails/build tags are honest and do not remove the changed hard path from CI evidence.

### Targeted mutation testing

When mutation evidence is used, verify that:

- source/package scope, build tags, Go/tool versions, selected tests, and time/concurrency bounds are recorded; the baseline ran real tests rather than reporting no test files or a stale result;
- the mutated source is built and executed, with cache reuse understood; a manual probe can use `go test -count=1` and an explicit timeout;
- Gremlins package-local selection does not stand in for cross-package/integration proof; unsupported language constructs or tool failures are disclosed;
- boundary, error-return, and state-change survivors are traced to the accepted behavior, not dismissed solely on coverage or score;
- compile failures, timeouts, and uncovered mutants are separate from assertion-based kills; required race/integration evidence is not replaced by a mutation score;
- only deliberate mutations are restored, the final diff and relevant suite are checked, and justified new tests are retained.

Use the mutation section in `SKILL.md`. Optional automation is not a new gate; a real unverified mandatory behavior remains a finding.
