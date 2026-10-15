# python-testing Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic randomizes/reverses order, reruns, parallelizes where supported, removes injected postcondition state, changes timing, and replaces a mock with the real boundary when the claim requires it. Probe session fixture contamination and xfail/skip false greens.

### Mutation probes

Within the task's permissions and budget, follow the baseline/isolation/restoration procedure in `SKILL.md`:

- change an inclusive boundary, swallow a required exception, or omit a state update and look for a contract-specific failing assertion;
- check whether monkeypatching the function under test, a fixture-provided answer, or a different installed package hides the mutant;
- inspect collection, markers, non-strict xfail, and skip behavior before accepting an all-green result;
- challenge cached mutmut evidence after dependency/configuration/fixture changes and distinguish actual reruns from reused results;
- try to explain a survivor without assuming it is equivalent; inspect inputs, imported source, and the assertion before choosing a new test;
- verify that an applied mutant was removed after failure/interruption and that unrelated files and wanted test improvements survive restoration.

A mutation tool error is not a killed mutant, and a high score does not waive a real missing behavior. Prefer a narrow manual probe to unsupported tool configuration or an unbounded run.

Block when cited tests can systematically pass despite the claimed mandatory behavior being broken. Test-style preferences are non-blocking when stronger evidence proves the same invariant.

## QA depth

Increase depth with shared fixtures/global state, async/concurrency, integration/product-acceptance claims, timing, external resources, and reliance on skips/mocks.
