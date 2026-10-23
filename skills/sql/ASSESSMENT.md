# SQL Assessment

Assess the resulting SQL/schema work against its accepted result contract. Use the criteria relevant to the change; this is not a requirement to redesign every query.

## Review criteria

- **Row grain and cardinality:** identify what one result row represents and verify every join against keys and one-to-many relationships. Aggregates do not count multiplied inputs; `DISTINCT` is justified by the contract.
- **Missing data:** empty groups, NULLs, outer joins, `COUNT`, and absence checks produce the intended values. Predicate placement preserves required unmatched rows.
- **Domain boundaries:** joins, uniqueness and affected-key predicates preserve tenant/owner scope. Numeric units, precision, timezones, and calendar boundaries match the caller's contract.
- **Ordering and windows:** output ordering is explicit when promised; windows use the correct partition, tie-breaker, and frame. Pagination includes the complete sort tuple and a stated consistency model.
- **Safe composition:** values are bound; dynamic identifiers/directions are validated separately. The emitted SQL matches the deployed dialect/version and real schema.
- **Write integrity:** constraints and transaction boundaries enforce the invariant under concurrency. Retry behavior, affected rows, migration compatibility, and recovery are considered when changed.
- **Bounded work:** result projection, page/export behavior, batching, and client materialization respect actual limits without truncating the promised result or breaking atomicity.
- **Evidence quality:** expected values and duplicate multiplicities were checked on discriminating cases, not only counts or a duplicate-erasing set comparison. Speed claims refer to measured work, not query appearance.

## Review result

Point to the SQL, relevant schema constraints, and observed result/transaction evidence. Separate a wrong result from a performance hypothesis and from unavailable execution evidence. Do not block a sound query because it lacks speculative sharding or an unrelated engine feature.
