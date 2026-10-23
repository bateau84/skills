# postgresql Quality Assurance

Assume the SQL, schema, and migration have passed normal review. Attack shared assumptions that can make PostgreSQL evidence look stronger than it is. Select probes for the changed behavior and execute them on a suitable test target; report unexecuted probes as limits.

## QA criteria

- **Role substitution:** repeat a claimed tenant-isolation path as the real application role with two tenants and denied writes. Compare owner/superuser behavior; a privileged fixture can hide an inactive or overly broad RLS policy. Probe pooled requests for leaked tenant/session state when that state supplies isolation.
- **Snapshot mismatch:** interleave two sessions around a read-then-write invariant. Try the configured isolation with concurrent updates and retries; serial tests can agree while a production race loses an update or makes an invalid decision.
- **Retry duplication:** force a serialization failure and, separately, a connection loss around commit. Check persisted rows and external-effect/idempotency records. A successful retry test must not conceal duplication when the first commit actually succeeded.
- **Migration half-success:** interrupt a concurrent index build or staged backfill and resume through the real migration runner. Inspect validity, duplicate enforcement, completion markers, and old/new application behavior; a clean-database rerun can miss a stranded invalid index or skipped data range.
- **Definition mismatch:** pre-create an index or constraint with the expected name but a different definition. Verify migration checks detect the difference instead of accepting `IF NOT EXISTS` as proof that the intended contract is installed.
- **Time and collation mismatch:** replay boundary values under the deployed session zone/collation, including ambiguous local times where relevant. Compare ordering, uniqueness, and serialized output; UTC-only or default-locale tests can share the wrong assumption.
- **Recovery illusion:** restore the chosen backup into a separate database with realistic role/extension requirements, then exercise the changed application path. An archive listing or a successful dump alone does not prove recoverability.
- **Diagnostic side effects:** challenge a supposedly read-only plan probe with a data-modifying CTE, sequence, or side-effecting function. Verify target selection and actual execution mode; rollback does not erase every effect of `EXPLAIN ANALYZE`.

## QA depth

Prioritize the boundary whose failure would survive the existing tests: two-session races, pooled role/state transitions, interrupted DDL, or recovery from the actual prior schema. Reuse existing realistic fixtures where possible. Additional personas, proposed probes, and static inspection do not by themselves establish independent or executed validation.
