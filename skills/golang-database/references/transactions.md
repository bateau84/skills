# Transactions, Isolation Levels, and Locking

The SQL/isolation examples below use PostgreSQL semantics. Confirm the actual database and driver support; use `sqlite` for SQLite transactions, which do not support `SELECT FOR UPDATE`. Use `sql`/`postgresql` to select the invariant and retry strategy, then apply these Go resource-lifetime patterns.

## Basic transaction pattern

```go
tx, err := db.BeginTxx(ctx, nil) // database/driver default; verify effective isolation
if err != nil {
    return fmt.Errorf("beginning transaction: %w", err)
}
defer tx.Rollback() // no-op if already committed

// ... execute queries using tx ...

if err := tx.Commit(); err != nil {
    return fmt.Errorf("committing transaction: %w", err)
}
```

## Custom isolation level

```go
tx, err := db.BeginTxx(ctx, &sql.TxOptions{
    Isolation: sql.LevelSerializable, // requires engine/driver support and retry handling
})
```

| Level | Use when |
| --- | --- |
| `LevelReadCommitted` | PostgreSQL's usual default; statements can observe different snapshots |
| `LevelRepeatableRead` | A stable PostgreSQL transaction snapshot; not every invariant is protected |
| `LevelSerializable` | Serializable execution where required; handle whole-transaction retries |

## SELECT FOR UPDATE — prevent race conditions

```go
var balance int
err := tx.GetContext(ctx, &balance, "SELECT balance FROM accounts WHERE id = $1 FOR UPDATE", accountID)
// Row is locked until tx.Commit() or tx.Rollback()
```

Use PostgreSQL `FOR UPDATE` when locking these selected rows protects the read-modify-write invariant. An atomic conditional update or constraint can be simpler. A lock on existing rows does not automatically protect an invariant involving absent rows or unrelated predicates; choose the engine's suitable isolation/constraint strategy. Keep all statements on `tx` and handle retryable failures across the whole transaction.

## Locking variants

| Clause | Effect |
| --- | --- |
| `FOR UPDATE` | Locks rows for write — other transactions block on same rows |
| `FOR UPDATE NOWAIT` | Same, but fails immediately instead of waiting |
| `FOR SHARE` | Locks rows for read — prevents writes but allows other reads |
