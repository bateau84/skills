# SQL Quality Assurance

Assume the SQL is readable and passed ordinary review. Attack shared assumptions that could make both the author and reviewer accept the wrong answer.

## QA criteria

- **Correlated fixture blindness:** replace one-to-one sample data with two independent child collections, repeated amounts, missing children, and a second owner reusing the same local IDs. Look for multiplication and cross-owner leakage hidden by tidy fixtures.
- **Oracle blindness:** a rewrite and its test both copy the original formula. Hand-calculate one result from business facts; compare full values and multiplicities. Inject one duplicate and one offsetting error to expose count/checksum-only comparisons.
- **NULL and peer blindness:** introduce NULL into an anti-join input and ties into window/pagination order. Check whether missing rows or changed cumulative totals pass existing tests.
- **Temporal composition:** traverse pages while a permitted writer inserts, deletes, or changes a sort key. Check the promised consistency model; do not demand a fixed snapshot when the product explicitly accepts live traversal.
- **Concurrent correctness:** interleave two read-then-write attempts or interrupt a batch between effects and progress recording. Probe lost updates, invariant violations, duplicate external effects, and an incorrect claim of atomicity.
- **Dialect substitution:** run relevant edge cases through the actual engine/runtime rather than an apparently equivalent test database. Probe type coercion, collation, NULL ordering, and feature support where the query relies on them.
- **Cost moved out of sight:** execute the full export/result consumption or a wide-row case. Determine whether a fast first row masks unbounded client memory, extra queries, or expensive sorting later.

Use a small counterexample before a large workload. Report the violated contract, reproducible input/interleaving, and observed output; distinguish a demonstrated defect from a proposed probe that was not executed.
