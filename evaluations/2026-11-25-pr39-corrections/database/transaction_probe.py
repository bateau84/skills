"""Bounded SQLAlchemy API check on SQLite; not PostgreSQL qualification.

Uses a task-owned file database, NullPool for fresh physical connections, and
explicit BEGIN events because SQLite legacy transaction mode can otherwise
invalidate a savepoint/outer-rollback probe. No server or provider calls.
"""
import asyncio
import importlib.metadata
import json
import platform
import sqlite3
import tempfile
from pathlib import Path

from sqlalchemy import delete, event, func, select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    pass


class Record(Base):
    __tablename__ = "records"
    id: Mapped[int] = mapped_column(primary_key=True)
    label: Mapped[str]


async def probe(database):
    engine = create_async_engine("sqlite+aiosqlite:///" + str(database), poolclass=NullPool)

    @event.listens_for(engine.sync_engine, "connect")
    def disable_driver_begin(connection, _):
        connection.isolation_level = None

    @event.listens_for(engine.sync_engine, "begin")
    def explicit_begin(connection):
        connection.exec_driver_sql("BEGIN")

    async def fresh_count():
        async with engine.connect() as connection:
            return await connection.scalar(select(func.count()).select_from(Record))

    def sync_insert(session, label):
        session.add(Record(label=label))
        session.flush()

    def sync_insert_and_commit(session, label):
        sync_insert(session, label)
        session.commit()

    try:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

        ordinary = async_sessionmaker(engine, expire_on_commit=False)
        async with ordinary() as session:
            async with session.begin():
                await session.run_sync(sync_insert, "committed-by-normal-exit")
            await session.rollback()  # Too late to undo the prior completed commit.
        ordinary_count = await fresh_count()
        assert ordinary_count == 1, ordinary_count

        async with engine.begin() as connection:
            await connection.execute(delete(Record))

        # Calling the sync bridge alone does not add a commit/rollback contract.
        async with ordinary() as session:
            await session.run_sync(sync_insert, "uncommitted")
        uncommitted_count = await fresh_count()
        assert uncommitted_count == 0, uncommitted_count

        async with engine.connect() as connection:
            outer = await connection.begin()
            joined = async_sessionmaker(bind=connection, expire_on_commit=False,
                                        join_transaction_mode="create_savepoint")
            try:
                async with joined() as session:
                    session.add(Record(label="async-application-commit"))
                    await session.commit()
                    assert outer.is_active
                    await session.run_sync(sync_insert_and_commit, "sync-application-commit")
                    assert outer.is_active
                    within_fixture = await session.scalar(select(func.count()).select_from(Record))
                    assert within_fixture == 2, within_fixture
            finally:
                await outer.rollback()
        after_teardown = await fresh_count()
        assert after_teardown == 0, after_teardown
        return {
            "schema": "portable-skills/sqlalchemy-transaction-probe/v1",
            "status": "pass",
            "environment": {"python": platform.python_version(),
                            "sqlalchemy": importlib.metadata.version("sqlalchemy"),
                            "aiosqlite": importlib.metadata.version("aiosqlite"),
                            "sqlite": sqlite3.sqlite_version,
                            "pool": "NullPool", "transaction_control": "explicit BEGIN events"},
            "observations": {
                "normal_begin_exit_then_late_rollback_rows": ordinary_count,
                "run_sync_without_commit_then_session_close_rows": uncommitted_count,
                "joined_fixture_rows_after_async_and_sync_application_commits": within_fixture,
                "fresh_connection_rows_after_outer_teardown": after_teardown,
                "outer_transaction_remained_active_after_each_application_commit": True,
            },
            "limits": "SQLite-only SQLAlchemy API check; no PostgreSQL/asyncpg, pytest fixture lifecycle, or agent behavior was executed."
        }
    finally:
        await engine.dispose()


if __name__ == "__main__":
    with tempfile.TemporaryDirectory(prefix="sqlite-", dir=Path(__file__).parent) as workspace:
        result = asyncio.run(probe(Path(workspace) / "probe.sqlite"))
    print(json.dumps(result, indent=2))
