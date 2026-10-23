---
name: python-database
description: "Python database access with stdlib sqlite3 — bound queries, connection context managers, sqlite3.Row, transaction control, repositories and per-connection setup. Use when writing, reviewing or debugging Python sqlite3/aiosqlite call sites or Python migration integration. Use sqlite for engine/WAL/file behavior, sql for query/schema design, and sql-performance for measured tuning. Not for SQLAlchemy, Django ORM or server database drivers (use python-database-orm)."
license: MIT
metadata:
  author: Bateau
  version: "1.1.0"
---

> Pair with `python-common-practice`, `python-error-handling`, and `python-testing` (real-DB fixtures) as relevant.

**Persona:** You are a Python engineer who keeps SQL at the edge. The rest of the app talks to a repository, never to a cursor.

# SQLite with `sqlite3`

The stdlib `sqlite3` module is enough for an embedded DB — no ORM required. Keep all SQL behind a repository so the rest of the code depends on methods, not on the schema. This is sortarr's `db/{connection,migrations,repository}` layout.

Use `sqlite` for engine semantics and lifecycle, `sql` for query/schema meaning, and `sql-performance` for measured tuning. This skill supplies Python integration rather than a separate engine policy.

## Parameterize every query — never format SQL

String-formatting user input into SQL is the classic injection vulnerability. Pass parameters with `?` placeholders; the driver escapes them safely.

```python
# ✗ Bad — SQL injection; an attacker controls the query
cur.execute(f"SELECT * FROM tracks WHERE id = '{track_id}'")

# ✓ Good — parameterized; value can never alter the query
cur.execute("SELECT * FROM tracks WHERE id = ?", (track_id,))
cur.execute("INSERT INTO tracks (id, title) VALUES (?, ?)", (tid, title))
```

Use `?` (qmark) placeholders, or `:name` with a dict. **Identifiers** (table/column names) can't be parameterized — if they're dynamic, validate them against an allow-list, never interpolate raw input.

## Connections via a context manager

Open and close connections deterministically with a context manager — leaked connections lock the file. sortarr's `get_connection` is the model: `sqlite3.Row` factory, error logged-and-re-raised, `close()` in `finally`.

```python
from contextlib import contextmanager
import sqlite3

@contextmanager
def get_connection(db_path: str):
    con = sqlite3.connect(db_path, autocommit=True)  # Python 3.12+
    con.row_factory = sqlite3.Row     # rows behave like dicts: row["title"]
    try:
        con.execute("PRAGMA foreign_keys = ON")   # before a transaction exists
        if con.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
            raise RuntimeError("SQLite foreign-key enforcement unavailable")
        con.autocommit = False                   # explicit transaction handling
        yield con
    finally:
        con.close()
```

`row_factory = sqlite3.Row` lets you access columns by name (`row["title"]`) instead of brittle positional indexing (`row[1]`) — adding a column won't silently shift your fields.

## Transactions — commit or roll back as a unit

Transaction behavior depends on Python's `autocommit`/legacy `isolation_level` settings; do not assume all connections open implicit transactions. With the explicit `autocommit=False` setup above, wrap related writes so a failure rolls back. The connection used as a context manager commits on success and rolls back on exception:

```python
with get_connection(db_path) as con:
    with con:                                  # commit on success, rollback on exception
        con.execute("INSERT INTO runs (started) VALUES (?)", (now,))
        con.execute("UPDATE state SET last_run = ?", (now,))
```

Note the two `with`s do different jobs: the outer closes the connection; the inner (`with con:`) is the transaction boundary.

With `autocommit=True`, `with con:` does not create a multi-statement transaction. For Python before 3.12, use a documented explicit-SQL or legacy transaction mode with foreign-key setup outside any transaction. Check the deployed [sqlite3 transaction-control documentation](https://docs.python.org/3/library/sqlite3.html#transaction-control).

## Repository pattern

Expose intent-named methods, not SQL, so callers (and the FastAPI layer) never touch a cursor. Type the repository against a `Protocol` so tests can substitute a fake (→ See `python-type-checking`).

```python
class Repository:
    def __init__(self, con: sqlite3.Connection):
        self._con = con

    def save_decision(self, d: MatchDecision) -> None:
        self._con.execute(
            "INSERT INTO decisions (video_id, verdict) VALUES (?, ?) "
            "ON CONFLICT(video_id) DO UPDATE SET verdict = excluded.verdict",
            (d.video_id, d.verdict),
        )

    def decision_for(self, video_id: str) -> MatchDecision | None:
        row = self._con.execute(
            "SELECT video_id, verdict FROM decisions WHERE video_id = ?", (video_id,)
        ).fetchone()
        return MatchDecision(**row) if row else None
```

Return `None` for "not found" — that's expected absence, not an error (→ See `python-error-handling`).

The save example assumes `video_id` has a primary-key/unique constraint and the SQLite runtime supports UPSERT (3.24.0+). It updates the existing row; `INSERT OR REPLACE` can delete it and trigger cascading child deletion. See [SQLite UPSERT](https://www.sqlite.org/lang_upsert.html) and the `sqlite` skill.

## Migrations

Use the project's versioned migration process; a small embedded application may use `PRAGMA user_version`. Choose startup or a separate migration step from deployment/concurrency needs. `IF NOT EXISTS` does not verify an existing schema matches the desired one. Follow `sqlite` for supported ALTER/rebuild procedures, dependent objects, transaction and foreign-key sequencing, failure recovery and backup checks.

## Connection settings and WAL

```python
# Apply to every actual connection before its first transaction, as above.
con.execute("PRAGMA foreign_keys = ON")
if con.execute("PRAGMA foreign_keys").fetchone()[0] != 1:
    raise RuntimeError("SQLite foreign-key enforcement unavailable")
```

Verify foreign-key enforcement per connection rather than relying on defaults. Changing it inside a transaction has no effect. Choose WAL only after checking deployment/filesystem, durability and checkpoint needs with `sqlite`; it is a persistent database-mode choice, not an unconditional connection initializer.

## Sync `sqlite3` on an async event loop

The stdlib `sqlite3` API is **blocking**. Calling it directly inside an `async def` FastAPI handler stalls the event loop for the whole query — every other in-flight request waits. SQLite is also single-writer: concurrent writers serialize on a file lock, so one slow write blocks the rest. Keep DB work off the loop one of two ways:

```python
# ✓ A plain `def` handler — FastAPI runs it in a threadpool, off the loop
@router.get("/stats")
def get_stats(repo: Repository = Depends(get_repo)) -> StatsOut:
    return repo.stats()                       # blocking sqlite is fine here

# ✓ Inside an async handler, offload the blocking call
from starlette.concurrency import run_in_threadpool

@router.get("/decisions/{vid}")
async def get_decision(vid: str, repo=Depends(get_repo)) -> DecisionOut:
    row = await run_in_threadpool(repo.decision_for, vid)   # or asyncio.to_thread
    ...
```

Don't share one connection across tasks or threads — `sqlite3` connections aren't safe for concurrent use. Open per request (or per job), or use a thread-aware pool. In an APScheduler job, open the connection **inside** the job, not once at import time (→ See `python-async`).

## Common mistakes

| Mistake | Fix |
| --- | --- |
| f-string / `%`-format SQL with input | Use `?` placeholders; never interpolate values. |
| Forgetting `commit()` | Use `with con:` for the transaction, or commit explicitly. |
| Positional `row[1]` access | `con.row_factory = sqlite3.Row`; access by name. |
| Connection never closed | Open via a context manager; close in `finally`. |
| Assuming FK constraints enforced | `PRAGMA foreign_keys = ON` per connection. |
| SQL scattered across the app | Confine it to a repository; callers use methods. |
| Blocking `sqlite3` call inside an `async def` handler | Use a `def` handler (threadpool) or `await run_in_threadpool(...)` / `asyncio.to_thread`. |
| Sharing one connection across tasks/threads | Open per request or per job; `sqlite3` connections aren't concurrency-safe. |
| Mocking the DB in tests | Use a real `tmp_path` SQLite DB — it's fast and catches SQL errors. |

**Diagnose:** use configured lint/security checks for unsafe SQL construction and a real `tmp_path` SQLite database for SQL/transaction checks. Use `EXPLAIN QUERY PLAN` plus representative full-result timings through `sql-performance`; a scan may be appropriate, and an index being used does not prove improvement.

## References

- [sqlite3 — DB-API 2.0 interface for SQLite](https://docs.python.org/3/library/sqlite3.html)
- [PEP 249 — Python Database API 2.0](https://peps.python.org/pep-0249/)
- [SQLite — Write-Ahead Logging](https://www.sqlite.org/wal.html)
- [Starlette — run_in_threadpool](https://www.starlette.io/concurrency/)
