# Persistence test maintenance: DONE

The focused persistence suite now has two tests instead of four. It preserves
the public creation, duplicate-ID, and row-count assertions, and checks that a
second distinct ID is accepted. The real process-death recovery test remains
unchanged and runs in the required full suite.

## Changes and protection

- Removed `test_existing_order_id_is_rejected`: it repeated the retained
  `test_duplicate_order_is_rejected` assertions exactly.
- Removed `test_create_uses_insert_once` and its mock import: README.md explicitly
  excludes private helper call counts from the public contract. Real SQLite
  state and public return values remain tested.
- Extended the creation test with `order-2`, preventing a store that incorrectly
  rejects every ID after the first from satisfying the examples.
- Left production code, recovery coverage, test selection, and domain tests
  unchanged. No dependency or README change was needed.

## Checks actually run

- Before editing: `python3 -B -m unittest discover -s tests -p test_orders.py -v`
  → `Ran 4 tests in 0.002s`, `OK`.
- After editing: the same focused command → `Ran 2 tests in 0.001s`, `OK`.
- Final required gate: `python3 -B -m unittest discover -s tests -v`
  → `Ran 4 tests in 0.022s`, `OK`, including
  `test_committed_order_survives_process_death ... ok`.
- `git diff --check -- .` → exit 0, no diagnostics, after removing an extra
  trailing blank line. Inspected the final scoped diff.

An inline standard-library harness (`python3 -B -`) tested three deliberate
production defects in a disposable copy containing the candidate tests.
Candidate: baseline `a1ec464` plus the test edit; Python 3.12.14. The isolated
baseline ran all four tests successfully. Imports were verified to resolve to
the copied source. Probes ran sequentially with a 40-second timeout per command.

| Deliberate defect | Observed assertion failure |
| --- | --- |
| Return `created` for an existing ID | Duplicate and recovery tests expected `duplicate`. |
| Reject every ID after the first | Distinct-ID creation expected `created`. |
| Omit the create transaction commit | Duplicate test counted zero rows after rollback; recovery expected `duplicate` after process death. |

All three probes failed on the intended assertions, without setup errors or
timeouts. Candidate source/test checksums were unchanged; the disposable copy
was removed before the final required gate.

## Remaining limitations

These probes establish detection of three sampled regressions, not exhaustive
mutation coverage. Verification used the current environment only. No separate
build, linter, or type-check gate is configured. Domain quantity behavior was
outside this assignment and was not changed or expanded. No local obligations
remain; no commit or publication was made.

## Skills used

- test-driven-development
- python-testing
- software-engineering
- python-common-practice
