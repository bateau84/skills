# product-acceptance Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

- Scenarios materially cover accepted outcomes rather than merely convenient implemented paths.
- Every PASS enters through a meaningful product boundary and exercises mandatory product-owned components.
- External fixtures/mocks do not replace the behavior under proof.
- Evidence is observed, current, scenario-specific, and supports the claimed outcome.
- Unexecuted/inconclusive scenarios remain unproven.
- Hard failure/recovery paths required by accepted behavior are represented.

## Review depth

Scale review depth with consequence, uncertainty, boundary count, and blast radius.
