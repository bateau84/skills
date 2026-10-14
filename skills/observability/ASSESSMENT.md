# observability Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer starts from the operational questions/invariants that must be answerable, then checks signals:

- each load-bearing failure/state transition has enough metrics/logs/traces/events to distinguish cause classes rather than merely prove “something failed”;
- correlation identity survives service/async boundaries and timestamps/timezones/sampling do not make evidence impossible to join;
- metrics use appropriate type/unit/denominator/window/cardinality; logs preserve structured context; traces sample/propagate in a way compatible with the diagnosis claim;
- dashboards/alerts distinguish absence/staleness/telemetry outage from healthy zero values;
- SLI/SLO measurements correspond to user/product outcomes or explicitly state the proxy and its blind spots;
- telemetry volume/cardinality/sampling/retention has a bounded cost and cannot itself overload the system;
- secrets/PII/audit data are governed and access/retention match sensitivity;
- observability failure degrades diagnosis, not product correctness, unless explicitly designed otherwise.
