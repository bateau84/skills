# postgresql Reviewer Assessment

Review whether the PostgreSQL change satisfies its accepted data, application, and deployment contract. Use the artifacts and database evidence relevant to the change; this perspective does not impose a separate approval stage.

## Review criteria

- **Engine and version:** SQL, extensions, migration syntax, isolation assumptions, and verification match the deployed PostgreSQL major. A SQLite fixture or client-version string does not establish PostgreSQL behavior.
- **Schema meaning:** types represent the domain's precision/range/time meaning; nullability, unique/check constraints, foreign keys, and cascade actions preserve accepted invariants. Tenant-scoped relationships are enforced where required.
- **Index ownership:** primary/unique enforcement is not duplicated by redundant indexes. Referencing-side foreign-key indexes are considered from joins and parent changes; neither automatic creation nor universal necessity is assumed.
- **Atomicity and concurrency:** relevant statements share a transaction connection; the chosen conditional write, locking, constraint, or isolation level protects the actual race. Commit/rollback and whole-transaction retry behavior are explicit where required.
- **Application boundary:** values are bound, dynamic identifiers are controlled, resource cleanup and cancellation exist, and pool/session behavior fits the deployed connection mode. An ambiguous commit outcome is not handled as an ordinary failed transaction.
- **Role and lookup behavior:** schema qualification/search-path choices fit role privileges. RLS evidence uses the application role and covers permitted and denied data where isolation is claimed.
- **Migration mechanics:** expected locks, rewrite/scan cost, backfill bounds, data compatibility, and recovery are addressed. Concurrent index builds are outside transaction blocks and checked for validity; staged constraint validation uses a supported kind and server version.
- **Data operations:** bulk ingestion preserves accepted constraints and atomicity. Statistics/maintenance actions address actual state; a routine `VACUUM FULL` or disabled autovacuum is not treated as a free optimization.
- **Verification coverage:** changed constraints, writes, result semantics, existing-data migration, and relevant rollback/concurrency paths have appropriate checks. Destructive diagnostics have an appropriate target and side-effect analysis.
- **Claims and scale:** measured gains are distinguishable from proposals; no assumption that 1 GB requires partitioning/sharding substitutes for workload evidence. Restore claims identify what was restored and checked.

## Review depth

Increase depth for isolation changes, data conversions, cascades, RLS/security-definer code, concurrent/staged migrations, backfills, or claims about recoverability. For a query-only edit, focus on its actual PostgreSQL behavior and callers rather than requiring an unrelated operations redesign. Use `sql` for shared result semantics and `sql-performance` for the tuning evidence.
