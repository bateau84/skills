# prometheus Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer checks instrumentation/storage/query assumptions around Prometheus’s pull/counter/staleness model:

- metric type/name/unit follows semantics: counters only increase/reset, gauges represent current values, histograms/summaries are chosen according to aggregation needs;
- labels are bounded stable dimensions; IDs/raw paths/errors/user input cannot explode series cardinality;
- scrape target/service discovery/relabeling retains intended targets/labels and cannot silently drop an environment/tenant;
- scrape interval/timeout/staleness and application update rate support the claimed detection/window;
- histogram buckets are useful for target latency ranges and aggregation uses the correct `le` dimensions; summaries are not incorrectly aggregated across instances;
- recording/alert rules preserve units/labels/denominators and evaluate often enough for `for` semantics;
- HA/remote-write duplicate/out-of-order behavior is understood where multiple replicas/backends exist;
- missing target/series is distinguishable from a healthy zero.
