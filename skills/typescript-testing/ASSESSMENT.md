# typescript-testing Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer verifies the suite cannot go green for TypeScript or JavaScript-specific mechanical reasons while behavior is broken:

- async tests await or return the operation and await rejection/resolution assertions so failures cannot occur after test completion;
- test doubles stop at real external boundaries rather than mocking away the parser, state machine, service, or component behavior being claimed;
- fake timers are scoped, advanced according to runner semantics, account for microtasks when needed, and are restored reliably;
- module mocks, spies, patched globals, process.env, singleton state, caches, and listeners are restored so tests pass alone and independent of order;
- the configured environment (Node, Bun, jsdom, happy-dom, browser) is capable of proving the browser/runtime behavior asserted;
- type-level API claims use an actual compile or type-test mechanism instead of runtime assertions, while runtime validation is not mistaken for type proof;
- regression tests reproduce the defining failure before relying on the fix and include important rejection, failure, or cancellation paths;
- parameterized tests remain diagnosable and snapshots are small and stable enough to review meaningfully;
- final evidence includes focused or containing tests and applicable repository typecheck and lint verification.

### Targeted mutation testing

When mutation evidence is used, verify that:

- source/test globs, tool/plugin/runtime versions, configuration, and time/concurrency limits are explicit; tests and in-source test blocks are not mutation targets;
- the selected StrykerJS runner matches the project; a custom command or Bun integration is verified locally rather than assumed supported;
- the baseline collects the intended tests and runs the mutated source through the actual transform/import path, not old build output or a mocked module;
- related-test filtering has not omitted API-driven integration tests or other indirect consumers;
- runtime assertion kills are distinguished from TypeScript checker rejection, setup failures, timeouts, and uncovered code; ordinary typechecking still runs when required;
- survivors, exclusions, and score denominator are explained; restoration preserves wanted edits and is followed by relevant tests/typecheck/lint.

Use the mutation section in `SKILL.md`. No universal score or runner migration is required merely to perform this review.
