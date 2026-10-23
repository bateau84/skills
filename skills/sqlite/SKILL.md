---
name: sqlite
description: "Build and maintain reliable SQLite databases. Use when writing SQLite schema or migrations, configuring embedded connections or PRAGMAs, handling SQLITE_BUSY or WAL files, importing data, or implementing backup and recovery. For relational query semantics use sql; for measured query and workload optimization use sql-performance."
license: MIT
metadata:
  author: Bateau
  version: "1.0.0"
---

# SQLite

Own SQLite's storage, connection, transaction and migration behavior. Use [sql](../sql/SKILL.md) for shared relational/query design and [sql-performance](../sql-performance/SKILL.md) for measured tuning. Language database skills cover driver APIs; the actual SQLite runtime and application contract determine engine behavior.

The normal target is roughly 100 MB–1 GB, with room to grow. File size alone does not determine engine suitability or justify sharding. Preserve a simple deployment while measuring the write concurrency, working set and recovery needs that could change it.

## Establish the actual environment

Inspect the application's database connection, not only the developer's SQLite CLI:

- Record `SELECT sqlite_version(), sqlite_source_id();`, the driver and relevant `PRAGMA compile_options;` output. Check runtime feature support before using version-dependent syntax.
- Identify file-backed versus in-memory storage, filesystem/mount location, number of processes, connection pool, journal mode, write volume and required durability.
- Inspect existing tables, constraints, indexes, triggers, views and migration history before changing them. Keep the repository's existing migration mechanism.
- Identify the accepted result or invariant, representative data, rollback/recovery approach and operation budget. Use available evidence; make missing assumptions explicit instead of inventing deployment facts.

For concurrent WAL use, compare the embedded build and any vendor backports with current [SQLite release notes](https://www.sqlite.org/changes.html) and [WAL correctness notices](https://www.sqlite.org/wal.html#walresetbug). A recent CLI does not prove the deployed library contains a fix.

## Define data and connection rules

### Data representation

- Declare keys, `NOT NULL`, uniqueness, checks and foreign keys to express the accepted data rules. Add child-key indexes when parent changes would otherwise require expensive child-table searches; foreign keys do not create those indexes automatically. [Foreign-key indexes](https://www.sqlite.org/foreignkeys.html#fk_indexes)
- Ordinary SQLite tables can allow NULL in a non-integer primary key unless it is explicitly `NOT NULL`; do not import another engine's implicit rule. STRICT and WITHOUT ROWID tables have different guarantees. [Primary-key constraints](https://www.sqlite.org/lang_createtable.html#the_primary_key)
- SQLite's ordinary type affinity is not rigid type enforcement. Choose one documented representation for timestamps, booleans and exact amounts; do not rely on a `DECIMAL` declaration to create exact decimal arithmetic. [Data types](https://www.sqlite.org/datatype3.html)
- Consider `STRICT` tables for a typed schema when every supported runtime is SQLite 3.37.0 or newer. Check its accepted type names and conversion behavior; inspect existing values before converting a table. [STRICT tables](https://www.sqlite.org/stricttables.html)
- Use an explicit stable primary key for application identity. `INTEGER PRIMARY KEY` already allocates integer IDs; add `AUTOINCREMENT` only when its committed-ID non-reuse behavior is required. It is not a gapless sequence. [Integer keys](https://www.sqlite.org/autoinc.html)
- Consider `WITHOUT ROWID` for suitable compact composite-key tables after measuring the trade-off. It changes key/storage behavior and is not a universal upgrade. [WITHOUT ROWID](https://www.sqlite.org/withoutrowid.html)

### Connection initialization

Initialize every physical application connection, including connections opened later by a pool. For a schema using foreign keys, run and verify this outside an active transaction:

```sql
PRAGMA foreign_keys = ON;
PRAGMA foreign_keys; -- verify 1 on the connection that will perform the work
```

Changing foreign-key enforcement within a transaction has no effect. Test actual pooled connections, not only startup code. [Foreign-key activation](https://www.sqlite.org/foreignkeys.html#fk_enable)

Give lock waits a bounded busy-handler/timeout policy that fits the caller's deadline. A timeout handles some contention; it does not add write capacity. Read back consequential settings: unknown PRAGMAs can be silently ignored. Do not assume all PRAGMAs share the same connection/database persistence. [PRAGMA semantics](https://www.sqlite.org/pragma.html)

Use the driver's parameter binding and deterministic statement/cursor cleanup. Check iteration, commit and close errors where the driver exposes them. Do not share connections across concurrent tasks unless the driver's documented usage and the application's transaction ownership support it.

Each plain `:memory:` connection creates a separate database. Verify connection lifetime and database identity before pooling it; closing the final connection to a shared in-memory database removes its contents. Shared cache is not a general performance remedy. [In-memory databases](https://www.sqlite.org/inmemorydb.html), [shared-cache caveats](https://www.sqlite.org/sharedcache.html)

## Keep write units correct and bounded

1. Define the atomic unit and its failure behavior. Bind values, reuse prepared statements when useful, and keep all statements in the unit on the same connection.
2. Keep transactions short; prepare input before acquiring a write transaction. Avoid network calls or unrelated processing while holding it.
3. For a known read-then-write unit, consider `BEGIN IMMEDIATE` to acquire the write transaction before reading. It can itself return busy and reserves write access early, so do not apply it to every read. Use savepoints for nested units. [Transactions](https://www.sqlite.org/lang_transaction.html)
4. Distinguish an invalid read snapshot from ordinary contention. On a failed snapshot upgrade, restart the whole transaction with fresh reads; retry only a bounded, replay-safe unit. Do not retry every error or repeat external side effects. A busy commit can leave a transaction active; inspect its state before deciding what to retry. [Isolation](https://www.sqlite.org/isolation.html), [commit behavior](https://www.sqlite.org/lang_transaction.html)
5. Verify the expected affected rows and commit outcome; roll back or clean up on error. Exercise cancellation through the actual driver, including whether the connection is reusable afterward. [Interrupt semantics](https://www.sqlite.org/c3ref/interrupt.html)

Choose the conflict action from the data contract. `INSERT OR REPLACE` can delete an existing conflicting row, affecting foreign-key actions and identity; use an explicit `ON CONFLICT ... DO UPDATE` when the intended operation is an update. Do not hide invalid input behind broad `OR IGNORE`. [Conflict handling](https://www.sqlite.org/lang_conflict.html), [UPSERT](https://www.sqlite.org/lang_upsert.html)

Batch imports and backfills within measured transaction and memory budgets. Respect the runtime's parameter limits; use prepared executions or bounded statements rather than one enormous generated SQL string. Commit separate batches only when partial progress and restart behavior are part of the contract. [SQLite limits](https://www.sqlite.org/limits.html)

Return only needed columns and bound result consumption. Large write statements with `RETURNING` can buffer their output internally; application-side streaming alone does not remove that memory cost. [RETURNING processing](https://www.sqlite.org/lang_returning.html#processing_order)

## Choose journal and durability behavior deliberately

WAL allows readers alongside a writer, but still permits only one writer at a time. Standard WAL requires all database users on the same host and is unsuitable for a database directly shared across hosts over a network filesystem. Verify `PRAGMA journal_mode` after changing it. [WAL deployment](https://www.sqlite.org/wal.html), [write isolation](https://www.sqlite.org/isolation.html)

Long read transactions can prevent checkpoints from completing. Close finished cursors/transactions and observe WAL growth and checkpoint progress. A checkpoint performs work; it is not a free status query. Never delete a live WAL file to reclaim space. [WAL lifecycle](https://www.sqlite.org/wal.html), [checkpoint modes](https://www.sqlite.org/c3ref/wal_checkpoint_v2.html)

Preserve the accepted durability contract when tuning. In WAL mode, `synchronous=NORMAL` can lose recently committed transactions after power loss even though it protects consistency; `FULL` adds commit synchronization. Do not disable journaling or synchronization as a routine import optimization. [Synchronous settings](https://www.sqlite.org/pragma.html#pragma_synchronous)

## Migrate and recover without losing hidden state

Use a tested SQLite-aware backup path before a consequential migration: the [online backup API](https://www.sqlite.org/backup.html) or a suitable [VACUUM INTO](https://www.sqlite.org/lang_vacuum.html#vacuuminto) operation. A copy of only a live `.db` file is not sufficient when committed data remains in its WAL. Restore to a separate location and verify the required data and schema.

Prefer supported `ALTER TABLE` operations for the deployed version. When rebuilding a table is necessary, follow the current documented sequence and adapt it to the migration runner's transaction behavior. In particular:

1. Inventory dependent indexes, triggers and views; decide how existing data will satisfy the new definition.
2. If the rebuild requires foreign-key enforcement disabled, do that before the migration transaction on its connection. Do not change the setting inside a transaction and assume it worked.
3. Create the replacement table, copy with explicit columns and conversions, replace the old table, and recreate required dependent objects. Do not rename the old table first as a shortcut that can retarget dependencies.
4. Run `foreign_key_check` and validate data/invariants before commit. Roll back failures, restore the prior enforcement setting after ending the transaction, and verify it even on error paths.

The [ALTER TABLE rebuild procedure](https://www.sqlite.org/lang_altertable.html#otheralter) supplies the exact version-relevant details. Avoid direct `sqlite_schema` edits or `writable_schema` shortcuts for ordinary migrations.

Plan migration lock time and temporary disk headroom. SQLite `VACUUM` rebuilds the database and can need substantial extra space; it is not PostgreSQL's routine vacuum and is not a default fix for a slow query. [VACUUM behavior](https://www.sqlite.org/lang_vacuum.html)

## Verify the behavior that changed

Use the actual application runtime and a real disposable database. For file, WAL, backup or multi-connection behavior, an isolated in-memory test is insufficient.

- Check result values, types, row counts, constraints and affected-row semantics relevant to the change.
- Check failure/rollback and reopen behavior for changed writes or migrations; confirm dependent objects and connection initialization survive the real lifecycle.
- Use `PRAGMA foreign_key_check` for referential violations. `integrity_check` or `quick_check` checks database consistency but does not replace foreign-key or application-level checks. [Integrity checks](https://www.sqlite.org/pragma.html#pragma_integrity_check)
- For performance claims, retain comparable measurements; use [sql-performance](../sql-performance/SKILL.md) and its [SQLite reference](../sql-performance/references/sqlite.md).

Report what changed, the runtime and workload used, what was verified, and any remaining limitation. If execution is unavailable, deliver the concrete SQL/configuration and verification steps as unexecuted proposals.

## Leave useful room for growth

Keep migrations reproducible, IDs stable, data types consistent, queries bounded and access patterns visible. Preserve existing tenant boundaries when they exist; do not add tenant/shard routing for a hypothetical deployment.

Reconsider the engine when measured writer contention, shared network access, operating requirements or capacity exceed this design. A client/server database may solve those needs before partitioning or sharding is warranted. State the evidence that would trigger that decision. [Engine-selection guidance](https://www.sqlite.org/whentouse.html)
