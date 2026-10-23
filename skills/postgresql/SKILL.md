---
name: postgresql
description: "Design, implement, and troubleshoot PostgreSQL schemas, queries, transactions, constraints, migrations, and application connections. Use when working with Postgres SQL, MVCC, isolation, COPY, RLS, or concurrent index changes. Pair with sql for relational query semantics and sql-performance for measured query or workload tuning; not a cluster administration or sharding runbook."
license: MIT
metadata:
  author: Bateau
  version: "1.0.0"
---

# PostgreSQL

Build correct, maintainable PostgreSQL data access before adding complexity. The ordinary target is roughly 100 MB–1 GB of data; concurrency, access patterns, and recovery needs matter more than a size label.

Use [sql](../sql/SKILL.md) for shared relational semantics and [sql-performance](../sql-performance/SKILL.md) for the measurement and optimization loop. Language database skills own driver APIs and resource cleanup. This skill owns PostgreSQL behavior and changes to its schema and data access.

## Establish the database contract

Read the existing schema, migrations, query callers, and operational constraints. Determine:

- deployed server major, extensions, driver/ORM, migration runner, and pool mode;
- domain invariants, transaction boundaries, tenant/owner boundaries, and expected results;
- relevant row counts, data distribution, table/index sizes, read/write mix, and concurrency;
- target environment, connection role, available tools, recovery route, and allowed interruption.

Use an available SQL client or application connection; do not assume `psql`, containers, extensions, or administrator access exist. `SHOW server_version` identifies the server; a local client version does not. For consequential syntax or operational behavior, open the official documentation for that deployed major. The `/current/` links below are discovery links, not a minimum supported version.

## Model data and enforce invariants

- Choose primary keys and data types from the domain and expected range. Preserve established ID formats; do not replace keys solely for a hypothetical distributed future.
- Use exact numeric representation when exact arithmetic is required. Use JSON/JSONB for document-shaped values where appropriate, while keeping relationships and frequently constrained fields explicit. Consult [data types](https://www.postgresql.org/docs/current/datatype.html).
- Distinguish an instant from a local calendar time. `timestamptz` represents an instant and displays it in the session time zone; store an originating zone separately if the domain needs it. Check conversions, daylight-saving boundaries, and precision against [date/time behavior](https://www.postgresql.org/docs/current/datatype-datetime.html).
- Encode required values, uniqueness, ranges, and relationships using `NOT NULL`, `UNIQUE`, `CHECK`, and foreign keys. `CHECK` accepting a null result does not replace `NOT NULL`; define the intended null behavior of uniqueness.
- A foreign key protects a relationship; it does not automatically add an index on its referencing columns. Inspect joins, parent deletes/updates, existing indexes, and write cost before adding one. Do not duplicate the index already supporting a primary/unique key.
- Make delete/update actions deliberate. A cascade changes domain behavior; it is not a generic performance fix. For tenant-scoped identities, ensure constraints enforce the intended tenant relationship as well as query predicates.

Constraint rules and index implications: [Constraints](https://www.postgresql.org/docs/current/ddl-constraints.html).

## Make transactions preserve the intended result

1. Identify which reads and writes must agree, and keep all statements on the same transaction connection.
2. Choose the smallest sound mechanism: an atomic conditional update, constraint, explicit row lock, or stronger isolation. A read followed by a write is not automatically protected by a transaction alone.
3. Keep the transaction short. Avoid network calls or unbounded work while holding locks; acquire multiple locks consistently where possible.
4. Handle errors by SQLSTATE and ensure rollback/release on failure. A transaction left aborted cannot simply continue with its next statement.
5. For retryable failures, retry the whole decision and transaction with bounded attempts/backoff. Protect external side effects from duplication; an unknown commit result needs reconciliation or an idempotency design, not blind replay.

At Read Committed, statements can see different committed snapshots. Repeatable Read and Serializable have different guarantees and can require transaction retries. Inspect the actual configured isolation rather than assuming the default. See [isolation](https://www.postgresql.org/docs/current/transaction-iso.html).

Serialization failures use `40001`; deadlocks use `40P01`. Retry policy must distinguish these from persistent constraint errors. A retry repeats the reads and application decisions, not just the failed SQL statement. See [serialization failure handling](https://www.postgresql.org/docs/current/mvcc-serialization-failure-handling.html).

## Integrate queries and connection state

- Bind values with the driver's parameter API. Validate and quote dynamic identifiers separately; placeholders do not stand for table names or sort directions.
- Preserve nulls, duplicate multiplicity, ordering, and transaction visibility when changing SQL. Use explicit selected columns and bounded result handling when callers do not need the whole relation.
- Size a bounded pool against measured concurrency and the server budget across application instances. Distinguish pool wait from server execution; propagate deadlines/cancellation and release rows and transactions promptly.
- Check what the pool preserves. Session settings, temporary tables, and prepared statements must not be assumed to follow a request through a transaction-pooling setup. Prefer transaction-local settings when the setting and pool support them.
- Keep object resolution and privileges explicit. A writable schema in `search_path` can allow another role to influence unqualified object lookup; security-definer functions need particular care. See [schemas and search paths](https://www.postgresql.org/docs/current/ddl-schemas.html).
- If row-level security is part of the design, test with the actual application role and both permitted and denied rows. Superusers and `BYPASSRLS` roles bypass RLS; owners normally do too. Do not treat an owner-run test as proof of tenant isolation. See [row security](https://www.postgresql.org/docs/current/ddl-rowsecurity.html).

For query-plan inspection, plain `EXPLAIN` does not run the executor; `EXPLAIN ANALYZE` does. Inspect functions, triggers, and data-modifying CTEs before executing diagnostics. Rollback does not reverse every effect, including sequence increments. Use a disposable representative database for uncertain or mutating experiments. See [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html) and [transaction exceptions](https://www.postgresql.org/docs/current/transaction-iso.html).

## Change schemas with a recoverable path

Use the project's migration mechanism. Schema SQL is part of the deliverable when the task requires it; a migration framework does not decide its correctness.

1. Inspect dependent queries, constraints, indexes, views/functions, and old/new application compatibility. Identify expected locks, scans/rewrites, temporary disk demand, and long-running transactions.
2. Rehearse the forward migration on representative existing data, including invalid legacy rows. Confirm a usable restore or forward-repair path for irreversible transformations; an empty reverse script is not recovery.
3. Use suitable lock/statement timeouts and bounded backfills. Choose ordinary transactional DDL when its lock window fits; use staged changes when availability requires them.
4. For `CREATE INDEX CONCURRENTLY`, run outside a transaction block. Inspect validity after success or failure; an interrupted build can leave an invalid index that still costs writes. Recover through an appropriate drop/rebuild, accounting for dependencies and any uniqueness enforcement already active.
5. For supported constraint kinds, `NOT VALID` followed by `VALIDATE CONSTRAINT` can separate installation from checking old rows. Verify the deployed major and constraint kind; this is not a universal mechanism for adding uniqueness.
6. Verify the resulting schema and representative reads/writes before considering the migration complete. A matching name or `IF NOT EXISTS` does not prove the existing definition matches the intended one.

Sources: [ALTER TABLE](https://www.postgresql.org/docs/current/sql-altertable.html), [concurrent index builds](https://www.postgresql.org/docs/current/sql-createindex.html), and [timeouts](https://www.postgresql.org/docs/current/runtime-config-client.html).

## Load, maintain, and recover data

Use `COPY` for suitable bulk ingestion, with a bounded staging/validation path when input needs checking. Choose transaction size from atomicity, retry, WAL, and lock requirements. Loading a new empty table can justify building indexes afterward; a live import does not justify silently removing uniqueness or foreign-key protection. Refresh relevant statistics after a major distribution change. See [populating a database](https://www.postgresql.org/docs/current/populate.html).

Keep autovacuum working and inspect long transactions when dead tuples accumulate. Normal vacuum reuses dead-row space and updates visibility information; `VACUUM FULL` rewrites the table, needs extra space, and takes an exclusive lock. Do not schedule it as a routine response to slow SQL. See [routine vacuuming](https://www.postgresql.org/docs/current/routine-vacuuming.html).

For material data changes, identify the actual recovery artifact and a way to restore it. A successful `pg_dump` is not a successful restore test; account for required roles, extensions, ownership, and application checks. Choose logical or other existing backup methods from recovery needs rather than database size alone. See [backup and restore](https://www.postgresql.org/docs/current/backup.html).

## Keep growth options inexpensive

Prefer stable keys, useful access-path indexes, bounded queries, resumable backfills, and visible query/connection metrics. Add ownership or retention fields when they are domain facts, not as speculative shard plumbing.

Record a measured trigger for revisiting the design: writer contention, an unmet latency budget at expected concurrency, maintenance time, or an excessive working set. Partitioning and sharding address different problems; neither is required by a 1 GB size threshold. Use [sql-performance](../sql-performance/SKILL.md) to compare simpler changes before proposing either. Partitioning decisions need pruning/retention benefits and their constraint costs: [table partitioning](https://www.postgresql.org/docs/current/ddl-partitioning.html).

## Verify and report the change

Use the actual PostgreSQL major for behavior-dependent checks; SQLite or SQL mocks do not prove PostgreSQL constraints, isolation, or migrations.

- Exercise relevant success and failure paths: null/duplicate/foreign-key violations, affected-row counts, commit/rollback, and concurrency where the invariant depends on it.
- Verify migrations from an existing schema/data state as well as fresh setup when both paths are shipped; check partial-failure recovery for staged operations.
- Compare query results under the same data and visibility assumptions. If claiming better performance, retain representative before/after measurements through `sql-performance`; syntax success or an index scan alone is insufficient.
- State changed SQL/schema, server assumptions, executed checks, remaining limits, and operational/recovery implications. Distinguish proposed tests from observed results.
