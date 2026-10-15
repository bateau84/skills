# golang-testing Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic seeks false positives: reverse test order, run repeatedly/parallel/race, remove hand-injected state, make timing slower/faster, and swap mocks for the real boundary where the claim requires it. Ask what defect could exist while every cited test still passes.

### Mutation probes

Within the task's permissions and budget, use the baseline/isolation/restoration procedure in `SKILL.md` to probe one meaningful defect:

- change an inclusive comparison or return `nil` where an error must propagate; confirm the test fails on the contract, not compilation;
- omit a required persistence/state update behind a mock and check whether assertions still pass;
- inspect whether package filters or build tags missed the test that would detect the mutant; rerun the relevant boundary test rather than accepting package-local green as system proof;
- challenge a reported timeout kill against the original baseline and intended liveness bound; a goroutine hang or tool timeout is not automatically assertion evidence;
- inspect restoration after an interrupted probe, including unrelated edits and generated binaries that could mask the final source.

Document actual outcomes and justified equivalent mutants. Do not turn a narrow probe into mandatory whole-repository mutation testing or replace race/leak checks with it.

Block when tests cited for a mandatory verification claim do not exercise that behavior or can systematically false-pass. Missing optional unit-test style preference is non-blocking if stronger evidence exists.

## QA depth

Increase depth with concurrency/races, persistence/network/process boundaries, integration/product-acceptance claims, global state, timing sensitivity, and consequence of false-green evidence.
