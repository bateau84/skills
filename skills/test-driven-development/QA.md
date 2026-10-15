# test-driven-development Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic tries to falsify the claim that the tests meaningfully drove and prove the accepted behavior.

### Construct the simplest wrong implementation

For each load-bearing requirement, ask:

> What is the simplest incorrect implementation that would still make these tests pass?

Try examples such as:

- returning the first expected constant;
- special-casing only the tested inputs;
- ignoring one branch or state transition;
- implementing both sides of a round trip with the same wrong convention;
- satisfying interaction assertions without producing the required outcome;
- bypassing persistence, ordering, authorization, retry, or error semantics hidden by a double.

If a materially wrong implementation survives, the suite is under-specified.

### Challenge mutation-testing claims

When valuable and permitted, turn one plausible wrong implementation into a bounded manual mutation or inspect a narrow automated run. Follow [targeted mutation testing](./references/mutation-testing.md) for isolation, baseline, budget, classification, and restoration.

- change an inclusive boundary, remove a guard, or suppress a required effect; verify the test notices the broken contract rather than merely touching the line;
- check whether a reported kill is only a compile/setup error, flaky test, or unexplained timeout;
- trace a survivor through test selection, mocks, generated output, and imported code before accepting a claim of equivalent behavior;
- inspect exclusions and the score denominator for high-risk code hidden from the report;
- challenge a high score with a realistic defect outside the generated operator set; do not interpret a sampled or partial run as whole-system proof;
- inspect the restored candidate and final diff so a probe cannot leave broken production code or erase unrelated work.

A known equivalent mutation need not be killed. A real missing mandatory behavior cannot be waived merely because the overall score is high. Do not broaden QA into a full-repository mutation campaign by default.

### Attack RED evidence

Check whether the claimed Red could have failed before the intended behavioral assertion because of:

- setup or fixture defects;
- compile/type/import failures unrelated to the behavior;
- environment or dependency failures;
- an exception on the wrong path;
- an assertion that was never reached.

A ceremonial Red is not discriminating evidence.

### Attack GREEN evidence

Look for:

- a Fake It implementation that was never forced to generalize;
- tests that merely repeat implementation logic;
- mocks/fakes that return the final answer rather than model a boundary;
- assertions against values planted by the test itself;
- weak examples that permit over-fitting;
- test helpers that silently encode the same bug as production.

### Attack composition

Unit TDD can leave integration gaps. Where the claim crosses a process, protocol, persistence, filesystem, database, CLI, browser, or external-service boundary, verify that some higher-level evidence actually exercises that composition.

Do not accept mocked unit evidence as proof of a boundary the mock replaces.

### Attack refactoring confidence

Check that refactoring did not:

- weaken or delete the discriminating assertion;
- move production decision logic into shared test helpers;
- silently change behavior while tests stayed green;
- preserve green only because tests are coupled to the old implementation shape.

### Attack test ordering and design feedback

Inspect whether the sequence of tests forced useful design progress or merely accumulated examples after implementation. Where tests require excessive setup, many mocks, or broad internal knowledge, consider whether the suite hides a design/locality problem that can make future autonomous maintenance unsafe.

## Blocking guidance

Block when TDD evidence is used to claim mandatory behavior that the tests do not discriminate, when doubles bypass the product boundary under proof, when a temporary Fake It implementation is presented as complete behavior, or when load-bearing cross-boundary behavior lacks evidence at the boundary.

Exact red/green commit ritual is non-blocking unless repository policy requires it. Behavioral and evidence quality matter more than theater.

## QA depth

Increase depth with correctness/security consequence, state machines, boundary integration, mock density, persistence/recovery semantics, regression risk, and ease of writing a trivial implementation that fools the tests.
