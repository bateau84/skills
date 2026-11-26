# Order sample

Use Python 3 standard library only. `orders.qualifies` is the public minimum-order rule.
`OrderStore.create` returns `created` once per ID and `duplicate` thereafter,
including after process death following a successful commit. Internal helpers
and their call counts are not public contracts.

Run focused tests while editing. Before handing off changes, run
`python3 -B -m unittest discover -s tests -v`. This includes the real process-recovery
check, which is required. Do not add packages or change test selection.
