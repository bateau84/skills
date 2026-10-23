# SQLite Assessment

Assess whether the work satisfies its accepted SQLite data, deployment and operation contracts. Apply criteria relevant to the change; a small query edit does not require a recovery project.

## Review criteria

- **Runtime evidence:** feature and patch claims refer to the embedded application library, driver and relevant compile options. A different CLI version does not establish compatibility.
- **Schema semantics:** types and conversions fit SQLite affinity or STRICT rules; keys, checks, uniqueness and foreign keys express the intended data contract. Rebuilds account for existing invalid values and dependent schema objects.
- **Connection scope:** foreign-key enforcement and other connection-local settings are applied to every physical connection at the right time and read back. Pool initialization evidence reaches connections created after startup.
- **Write semantics:** the atomic unit uses one connection; conflict handling preserves identity, child rows and intended trigger effects. REPLACE is not accepted as equivalent to an update without explicit justification.
- **Concurrency and errors:** transaction mode, busy handling, snapshot retries, cancellation and commit failures match the driver and journal mode. Replays are bounded and preserve external side-effect behavior.
- **Deployment and durability:** storage location supports the chosen journal mode. WAL claims retain the single-writer constraint; synchronization changes preserve or explicitly identify changes to the accepted durability requirement.
- **Migration and recovery:** the ordered migration preserves required tables, indexes, triggers and views; foreign-key state is restored on success and failure. Backup/restore evidence includes data needed for the chosen journal mode.
- **Bounded work:** import, RETURNING and result-consumption choices account for parameter count, transaction duration, memory and restart semantics relevant to the workload.
- **Verification limits:** relevant file and connection lifecycles were exercised on real SQLite. Integrity checks are not presented as proof of application or foreign-key correctness; timing claims have measured support.

## Review output

For a defect, identify the affected invariant, concrete SQL/configuration path and evidence of the mismatch. Distinguish a demonstrated defect from an untested deployment assumption. Route detailed plan/benchmark review to sql-performance when tuning is the claimed result.
