# Minimum order boundary: DONE

`orders.qualifies` now accepts orders equal to the configured minimum (`>=`).
The existing domain test adds equality at 10 while retaining the below/above
cases. The README now states the inclusive rule explicitly.

## Verification

Commands ran from this fixture directory:

- **Red:** `python3 -B -m unittest discover -s tests -p test_domain.py -v`
  failed only for `amount=10`: `AssertionError: False != True`, followed by
  `FAILED (failures=1)`. Production code was unchanged at this point.
- **Green:** the same focused command passed: `Ran 1 test in 0.000s`, `OK`.
- **Required gate:** `python3 -B -m unittest discover -s tests -v` passed:
  `Ran 6 tests in 0.033s`, `OK`. This included
  `test_committed_order_survives_process_death ... ok` using real child processes.
- Reviewed the final code/documentation diff and searched this fixture for
  minimum-rule consumers; the public function owns the rule.
- `git diff --check -- .` exited 0 with no output.

## Evidence limits

Evidence covers the local suite in this environment, including values 9, 10,
and 11 at minimum 10 and the existing order creation/recovery cases. It does
not establish exhaustive input or platform coverage. No additional build or
lint gate is configured in the README. No assigned work remains.

## Skills used

test-driven-development, python-testing, software-engineering, python-how-to,
python-common-practice.
