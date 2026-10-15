# python-testing Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer checks pytest/unittest evidence for state isolation and claim fidelity:

- fixture scope matches resource/state ownership; mutable session/module fixtures cannot leak order-dependent state into supposedly isolated tests;
- `yield` fixture teardown runs under failure and does not mask the primary exception; monkeypatch/env/cwd/sys.path/global configuration is restored;
- parametrization spans semantic boundary cases rather than multiplying equivalent examples; IDs make failures diagnosable;
- async tests use the intended event-loop/backend/lifecycle and do not leave tasks pending across tests;
- `tmp_path`, frozen clocks/random seeds, network/DB fakes, and dependency overrides preserve the behavior under proof rather than bypass it;
- `xfail`/skip markers are specific/honest and unexpected pass/failure policy cannot turn regressions green;
- mocks use autospec/spec where helpful but do not overfit implementation or replace a product boundary in integration/acceptance claims;
- caplog/warnings/exceptions assert meaningful semantics, not only that “something happened”.

### Targeted mutation testing

When mutation evidence is used, verify that:

- mutmut/Python versions, source paths, pytest selection/configuration, and runtime bounds are recorded; flags/configuration match the installed version;
- the baseline collects and passes the intended tests, not only skipped or expected-failure cases;
- imports resolve to the mutated candidate rather than another installed package; fixtures, dependencies, and cached/incremental results match this run;
- exceptions, boundary values, and state-update survivors are explained by actual assertions and the accepted contract;
- import/setup/type-check errors, timeouts, and untested mutants are not runtime assertion kills; exclusions and equivalence claims are justified;
- `mutmut apply` or a manual edit cannot overwrite unrelated work; restoration and the final relevant pytest suite are verified.

Use the mutation section in `SKILL.md`. Tool availability and a score target are not additional mandatory gates.
