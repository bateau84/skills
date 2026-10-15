# typescript-testing Quality Assurance

Adversarial validation for any agent. Assume competent test writing and normal review; attack false greens and suite coupling.

## QA criteria

Critic tries to make the implementation wrong while leaving the test green:

- delay a Promise until after the test body would ordinarily return and confirm the assertion still owns it;
- reject the operation instead of resolving and look for un-awaited matchers or swallowed rejections;
- run tests individually, reversed or shuffled, and repeatedly to expose leaked module, global, timer, or singleton state;
- remove or alter behavior behind a heavily mocked collaborator and see whether the test still passes because the mock supplied the answer;
- change scheduler order with deferred Promises or fake time rather than real sleeps;
- run the test under the actual production-like browser or runtime when a shim may omit the behavior being claimed;
- mutate a public TypeScript signature in an invalid way and confirm type-level tests fail when such compatibility is part of the claim;
- inspect giant snapshots and loose matchers for changes the assertion would ignore.

### Mutation probes

Use the bounded baseline/isolation/restoration procedure in `SKILL.md` when executing these probes:

- alter a guard, falsy-value boundary, rejection path, or required state effect and check for a meaningful runtime assertion failure;
- confirm the source StrykerJS mutates is the module the tests actually import; stale transpiled output or module mocks can keep tests green;
- inspect related-test filtering for a survivor whose real consumer calls through HTTP or another indirect boundary;
- challenge apparent kills caused only by typechecking, startup errors, or a detached asynchronous assertion; keep type-contract evidence separate from runtime evidence;
- inspect excluded lines, in-source test blocks, and incomplete runs before accepting a score as evidence;
- verify no temporary source mutation, mock, timer, or configuration change remains in the delivered diff.

Do not change the project's runner just to obtain a mutation score. A manual sample or explicit tooling limitation is preferable to invented compatibility or unsupported success claims.

Block when test evidence is materially false or cannot fail for the regression it claims to guard. Do not demand browser E2E for pure logic that a faster lower-level test proves completely.

## QA depth

Increase depth for async code, singleton/module state, global API mocking, fake timers, browser storage, navigation or focus, flaky suites, public type APIs, and security-sensitive parsing or validation.
