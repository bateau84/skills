---
name: sql
description: "Design and verify relational schemas and SQL queries. Use when writing, reviewing, or debugging joins, aggregates, CTEs, window functions, NULL handling, pagination, constraints, or SQL rewrites. Add sqlite or postgresql for engine behavior; use sql-performance for measured slow-query tuning. Not for driver or ORM API details."
---

# SQL

Make the result correct and the amount of work deliberate. A shorter query, fewer joins, or an index scan does not by itself make a query better.

## Establish the query's contract

Inspect the schema, existing SQL, migrations, and callers before proposing a change. Establish only the facts that affect this task:

- Actual engine/version and driver placeholder syntax; do not assume SQLite and PostgreSQL accept the same SQL or enforce the same types.
- What one output row represents, required columns, allowed duplicates, NULL meaning, and the expected result for no matches.
- Keys, relationship cardinality, tenant/owner scope, uniqueness and foreign-key constraints, and relevant indexes.
- Required order, pagination/navigation behavior, and whether results need one consistent snapshot while data changes.
- Representative row counts, row widths, distribution/skew, query frequency, and the application's result/memory limits.

Read available evidence first. Ask only when a missing fact would change the result or a consequential operation. State assumptions on proposals; do not invent schema or production measurements.

Use `sqlite` or `postgresql` for engine-specific schema and transaction work. Add a language database skill for driver calls and resource lifetimes; it does not replace SQL reasoning. Authorized schema work belongs in the project's existing migration process.

## Model the data rules

Choose stable keys, appropriate types and units, and database constraints for required values, uniqueness, valid ranges, and relationships. Keep ownership keys in joins and constraints when identifiers are only unique within an owner. Normalize the ordinary model; denormalize only for a concrete access pattern with a clear update/consistency strategy.

Treat NULL as a domain choice. A nullable uniqueness rule or `CHECK` is not automatically a non-null requirement; verify engine semantics and add `NOT NULL` when required. Decide precision and rounding for numeric data, and distinguish an instant from a local calendar date. Do not use floating point for an exact monetary contract. See the engine's [constraint documentation](https://www.postgresql.org/docs/current/ddl-constraints.html).

## Build complex queries in meaningful steps

1. Identify the required row grain at each step: for example, one order line, one order, then one customer. Use explicit joins and clear aliases.
2. Check which joins can multiply rows. Aggregate independent one-to-many relationships separately before joining their results when that matches the requested grain. `DISTINCT` and `SUM(DISTINCT amount)` do not repair an unexplained fan-out.
3. Use `EXISTS` when the question is whether a match exists, rather than joining every match. For absence checks, choose `NOT EXISTS` or another expression with deliberate NULL behavior; `NOT IN` with a nullable subquery is a different contract.
4. Place predicates deliberately. Filtering the nullable side of a left join in `WHERE` can remove unmatched parents. `COUNT(*)` counts its null-extended row; `COUNT(child.non_null_key)` counts matches.
5. Choose aggregates, window functions, and CTEs for the result semantics. Window functions preserve row grain. Specify tie-breaking and the window frame when peer handling matters; the window's order does not establish final output order.
6. Keep understandable CTE boundaries. Whether a CTE is folded or materialized depends on the engine, version, and query; neither flattening all CTEs nor forcing materialization is a general optimization.

Verify these rules against the actual engine: [joins and grouping](https://www.postgresql.org/docs/current/queries-table-expressions.html), [subqueries and NULL](https://www.postgresql.org/docs/current/functions-subquery.html), [aggregates](https://www.postgresql.org/docs/current/functions-aggregate.html), and [window frames](https://www.postgresql.org/docs/current/tutorial-window.html). PostgreSQL documentation describes its dialect, not a guarantee for every SQL implementation.

## Keep access bounded and usable

- Bind values through the driver. Parameters do not safely substitute table/column names or sort direction; map dynamic identifiers to an allowlist and use the driver's identifier-quoting facility where needed.
- Select the columns needed by the caller. Filter and aggregate in the database where it preserves the contract and reduces transfer or repeated work. Avoid creating one remote query per returned row; measure the trade-off for embedded SQLite rather than treating all query counts as equal network costs.
- Use comparison predicates that can match the intended access path. For time ranges, consider explicit half-open bounds (`>= start`, `< end`) in the correct timezone/units rather than wrapping every stored value in a function. Verify expression indexes and casts when functions are required.
- Use a total, deterministic `ORDER BY` for bounded pages. Offset pagination is valid for suitable small or random-access workloads; deep offsets may require increasing work.
- For sequential traversal, consider keyset pagination with the full sort tuple and a unique tie-breaker. Cursor predicates must match directions, collation, NULL handling, filters, and tenant scope. A cursor alone does not provide snapshot consistency across concurrent inserts, deletes, or sort-key changes.
- Stream/chunk exports and batch writes within application memory, bind-parameter, lock-duration, and recovery limits. Releasing one batch must not silently weaken an all-or-nothing requirement.

[LIMIT/OFFSET](https://www.postgresql.org/docs/current/queries-limit.html) and [SQLite row-value pagination](https://www.sqlite.org/rowvalue.html) explain the relevant mechanics. Read [query patterns](references/query-patterns.md) for concrete aggregation and cursor examples.

## Preserve write and concurrency semantics

For updates/deletes, identify the affected key set and expected row count. Use transactions for the actual invariant; an application check followed by a write can race. Choose a constraint, atomic conditional update, suitable locking, or isolation level supported by the engine. Do not copy PostgreSQL row-locking syntax into SQLite.

Keep transactions short without splitting required atomic work. Define retryable failures and whether the whole transaction must restart. Protect external effects from duplicated retries. Use the project's migration and restore procedure for persistent schema/data changes; inspect old/new application compatibility and deployed-version support.

Diagnostic SQL can execute work too. Read the statement, including CTEs/functions/triggers, before running it. PostgreSQL `EXPLAIN ANALYZE` executes the statement; a rollback is not a universal undo for external effects or sequences. Use estimated plans or a disposable representative environment when execution is outside the task's scope. See [EXPLAIN](https://www.postgresql.org/docs/current/sql-explain.html).

## Verify meaning before claiming improvement

Compare outputs against accepted behavior on cases that exercise the relationships: empty inputs, missing children, multiple children on both sides, duplicate values, NULLs, equal sort keys, owner boundaries, and numeric/time boundaries. Select cases relevant to the changed query rather than building an unrelated test suite.

Check values and duplicate multiplicities, plus order when promised. Equal row counts, a checksum alone, or set comparison that discards duplicates is insufficient. When fixing an existing bug, use independently derived expected results rather than treating the old query as the oracle. Exercise retry/rollback behavior if write semantics changed.

For performance work, use `sql-performance` to compare representative full execution and application consumption, including write/storage costs. If the database is unavailable, provide reviewable SQL, assumptions, expected results, and a concrete verification procedure; mark execution and speed claims as unverified.

Return the SQL/schema change, its meaning, the evidence checked, and any material limitation. Do not present a suggested rewrite as a measured optimization.
