# SQLite Quality Assurance

Assume the SQL is plausible, migrations have been reviewed and normal tests pass. Probe SQLite-specific assumptions that the implementation and its tests may share. Choose probes that matter to the claimed behavior.

## QA criteria

- **Pool substitution:** expand or recycle the real connection pool after successful initialization. Attempt an invalid child insert through a different physical connection; check whether enforcement disappears or a plain in-memory database unexpectedly becomes empty.
- **Snapshot and retry interleaving:** hold a read transaction, commit a conflicting write through another connection, then attempt the first transaction's write. Check fresh-read retry behavior and whether a side effect or import batch is repeated.
- **Long-reader WAL growth:** keep an application cursor open while writes continue, then release it. Observe checkpoint progress and disk use before and after release. A single-connection benchmark cannot establish this behavior; do not delete recovery files or force unbounded blocking as a test remedy.
- **Backup truth:** take a backup while the application has committed recent data in WAL mode. Restore it separately and check that newest committed data and dependent schema objects are present. Process shutdown alone does not exercise a power-loss durability promise.
- **Migration interruption:** interrupt a disposable rebuild at a relevant boundary and reopen through the real migration runner. Check that the schema/version marker agree, required objects remain, and connection enforcement is restored rather than inferred from a successful happy path.
- **Environment mismatch:** repeat the relevant probe with the application's bundled library, filesystem behavior and connection model. A system CLI, in-memory fixture or different mount can conceal an unsupported feature or locking assumption.
- **Integrity false confidence:** deliberately distinguish a structurally valid file from bad domain data or orphaned rows in a disposable fixture. Verify the claimed checker actually detects the property attributed to it.

## Evidence and limits

Record the initial state, interleaving or interruption, observed database state and what the observation falsifies. Missing access to the real driver or deployment limits the claim; it does not justify inventing a failure or redesign requirement. Ordinary rollback tests do not prove crash recovery, and crash tests do not by themselves prove power-loss durability.
