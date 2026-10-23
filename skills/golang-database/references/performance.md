# Go Database Performance Integration

Use this reference for Go pool observations and batch APIs. Use `sql` for query/pagination semantics and `sql-performance` plus its relevant engine reference for plans, indexes, statistics and resource tuning. Follow the task and repository authority for execution; this reference neither grants permission nor forbids already authorized changes.

## Connection Pool Sizing

### Configuration

Values below illustrate the API. Choose them from engine capacity, request concurrency and measured pool behavior; they are not defaults for every application. See [Go connection management](https://go.dev/doc/database/manage-connections).

```go
db, err := sqlx.Connect("postgres", dsn)
if err != nil {
    return fmt.Errorf("connecting to database: %w", err)
}

db.SetMaxOpenConns(25)                  // total connections (match your DB capacity)
db.SetMaxIdleConns(10)                  // keep connections warm, reduce handshake overhead
db.SetConnMaxLifetime(5 * time.Minute)  // recycle connections (DNS changes, server restarts)
db.SetConnMaxIdleTime(1 * time.Minute)  // release idle connections back to the pool
```

| Setting           | Too low                         | Too high                         |
| ----------------- | ------------------------------- | -------------------------------- |
| `MaxOpenConns`    | Requests queue waiting for conn | DB overwhelmed, context switches |
| `MaxIdleConns`    | Cold connections, slow queries  | Wasted memory holding idle conns |
| `ConnMaxLifetime` | Frequent reconnection overhead  | Stale connections after failover |
| `ConnMaxIdleTime` | Same as MaxIdleConns too low    | Idle conns consume server memory |

### Monitoring

Check pool stats in production to detect exhaustion:

```go
stats := db.Stats()
slog.Info("db pool",
    "open", stats.OpenConnections,
    "in_use", stats.InUse,
    "idle", stats.Idle,
    "wait_count", stats.WaitCount,        // total waits for a connection
    "wait_duration", stats.WaitDuration,  // total wait time
)
```

`WaitCount` and `WaitDuration` are cumulative. Compare deltas over an interval with request rate and latency. Investigate held transactions, unclosed results, slow work and server contention before changing capacity; raising `MaxOpenConns` can overload the database.

### Prometheus Metrics

Use a custom Prometheus collector to export pool metrics on-demand (scales to multiple pools automatically):

```go
type DBCollector struct {
    pools map[string]*sqlx.DB
}

func NewDBCollector(pools map[string]*sqlx.DB) *DBCollector {
    return &DBCollector{pools: pools}
}

func (c *DBCollector) Describe(ch chan<- *prometheus.Desc) {
    ch <- prometheus.NewDesc("db_open_connections", "Number of open connections", []string{"pool"}, nil)
    ch <- prometheus.NewDesc("db_in_use_connections", "Connections currently in use", []string{"pool"}, nil)
    ch <- prometheus.NewDesc("db_idle_connections", "Idle connections in pool", []string{"pool"}, nil)
    ch <- prometheus.NewDesc("db_total_latency_seconds", "Total latency for a connection", []string{"pool"}, nil)
}

func (c *DBCollector) Collect(ch chan<- prometheus.Metric) {
    for poolName, db := range c.pools {
        stats := db.Stats()

        ch <- prometheus.MustNewConstMetric(
            prometheus.NewDesc("db_open_connections", "Number of open connections", []string{"pool"}, nil),
            prometheus.GaugeValue, float64(stats.OpenConnections), poolName)

        ch <- prometheus.MustNewConstMetric(
            prometheus.NewDesc("db_in_use_connections", "Connections currently in use", []string{"pool"}, nil),
            prometheus.GaugeValue, float64(stats.InUse), poolName)

        ch <- prometheus.MustNewConstMetric(
            prometheus.NewDesc("db_idle_connections", "Idle connections in pool", []string{"pool"}, nil),
            prometheus.GaugeValue, float64(stats.Idle), poolName)

        ch <- prometheus.MustNewConstMetric(
            prometheus.NewDesc("db_wait_duration_seconds_total", "Total connection wait duration", []string{"pool"}, nil),
            prometheus.CounterValue, stats.WaitDuration.Seconds(), poolName)
    }
}

func init() {
    pools := map[string]*sqlx.DB{
        "primary": mainDB,
        "replica": replicaDB,
    }
    prometheus.MustRegister(NewDBCollector(pools))
}
```

**Collector advantages:**

- Metrics are collected on-demand during scrapes (no background goroutine)
- Always returns current state (no stale data between scrapes)
- Scales to multiple pools automatically
- Lower memory footprint (no metric state in memory)

**Alert thresholds:**

- Open connections approaching `MaxOpenConns` → risk of request queuing
- Increasing wait rate/duration → investigate held connections, slow queries and engine capacity before resizing
- Idle connections too high → reduce `MaxIdleConns` or lower `ConnMaxIdleTime`

## Batch Processing

Avoid two extremes:

- **Row-by-row** — can incur avoidable network/commit overhead; embedded SQLite has different round-trip costs
- **One giant batch** — can consume memory, hold locks or exceed parameter/time limits

### Choose a bounded batch size

Measure batches against row width, bind-parameter limits, lock duration, memory and recovery needs. The 500-row example is illustrative. It commits statements separately; use an appropriate transaction when the accepted operation must be all-or-nothing, or design restart/idempotency for partial progress.

### Batch INSERT with sqlx

```go
func insertUsersBatch(ctx context.Context, db *sqlx.DB, users []User) error {
    const batchSize = 500
    for i := 0; i < len(users); i += batchSize {
        end := min(i+batchSize, len(users))
        batch := users[i:end]

        _, err := db.NamedExecContext(ctx, `INSERT INTO users (name, email) VALUES (:name, :email)`, batch)
        if err != nil {
            return fmt.Errorf("inserting users batch %d-%d: %w", i, end, err)
        }
    }
    return nil
}
```

### Bulk INSERT with pgx (PostgreSQL COPY protocol)

For suitable PostgreSQL bulk loads, consider `pgx.CopyFrom` and compare it against the actual workload. This example materializes input rows; use a bounded/streaming source for large input and preserve required transaction/constraint behavior:

```go
rows := make([][]any, len(users))
for i, u := range users {
    rows[i] = []any{u.Name, u.Email}
}
_, err := pool.CopyFrom(ctx,
    pgx.Identifier{"users"},
    []string{"name", "email"},
    pgx.CopyFromRows(rows),
)
```

## Query and index work

Use `sql` for a complete pagination order and cursor tuple, including a unique tie-breaker and explicit snapshot/live-result semantics. An offset is valid for suitable workloads; do not promise constant-time cursor traversal without measuring its access path.

Use `sql-performance` for the measured query → plan → change → comparison loop. Inspect the real schema and existing indexes through available database tooling; no particular MCP service is required. Choose an index from predicates, ordering and workload costs rather than a universal most-selective-first rule. Do not remove an index from low scan counts alone: check constraint ownership, rare/critical uses and the observation window.

Estimated plans and executed plans are different operations. `EXPLAIN ANALYZE` executes SQL and can have side effects; use the engine reference to choose a suitable environment and measurement method. Keep Go context deadlines, result cleanup, bind/prepared behavior and full result consumption representative in before/after measurements.

Use `golang-observability` for Go database metrics and `promql` for interpreting exported pool measurements.
