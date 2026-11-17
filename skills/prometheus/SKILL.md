---
name: prometheus
license: Apache-2.0
description: "Prometheus metrics collection, scraping, TSDB, alerting rules, recording rules, and Grafana Cloud Metrics integration. Use when configuring scrape targets, designing alerting/recording rules, or discussing metrics architecture. Not for PromQL queries (→ See `promql`)."
---

# Metrics with Prometheus and Grafana

> **Docs**: https://prometheus.io/docs/ | **Grafana Cloud Metrics**: https://grafana.com/docs/grafana-cloud/send-data/metrics/

## Collection and storage contract

Own plain Prometheus server configuration here; use `promql` for query derivation, `grafana-mimir` for Mimir topology, and `grafana-infrastructure-monitoring` for Alloy/Helm deployment. Start with the actual scrape targets, authentication, interval, retention, cardinality budget and remote-storage destination.

A minimal local scrape example (replace illustrative targets with the deployment's actual service discovery):

```yaml
global:
  scrape_interval: 30s
  scrape_timeout: 10s
rule_files:
  - rules/*.yml
scrape_configs:
  - job_name: api
    static_configs:
      - targets: ["127.0.0.1:8080"]
    metric_relabel_configs:
      - source_labels: [__name__]
        regex: 'unneeded_debug_.*'
        action: drop
```

`relabel_configs` changes or drops discovered **targets before scraping**; `metric_relabel_configs` filters scraped samples before ingestion. They are not interchangeable. A target dropped before scraping never gets an `up=0` series. Bound labels to stable dimensions: request IDs, emails, trace IDs and arbitrary paths belong in logs/traces or exemplars, not metric labels. Counter rates require a range rate/increase; averaging a raw CPU counter is not utilization.

For remote write, use the endpoint supplied for the exact tenant, and load secrets from an approved mounted file instead of committing tokens:

```yaml
# Merge into the Prometheus server configuration after supplying real values.
remote_write:
  - url: https://prometheus-<region>.grafana.net/api/prom/push
    basic_auth:
      username: "<metrics-instance-id>"
      password_file: /run/secrets/metrics-write-token
```

Set the accepted TSDB retention deliberately using `--storage.tsdb.retention.time` and/or `--storage.tsdb.retention.size`; monitor disk headroom, WAL and remote-write queue failures. Remote write is not proof the destination is receiving current data or an automatic replacement for local retention. Confirm ingestion on the actual downstream datasource.

Use `up{job="api"} == 0` for discovered targets whose scrape fails, and a separate `absent(up{job="api"})` check when the **whole expected job** disappears. Per-instance disappearance requires an expected inventory; do not equate absent data with a healthy zero. Validate a rule with representative fixtures, missing-data cases and `promtool test rules` before publishing.

Sources: [Prometheus configuration](https://prometheus.io/docs/prometheus/latest/configuration/configuration/), [storage](https://prometheus.io/docs/prometheus/latest/storage/).

## Alerting Rules

### Prometheus Alerting Rule

```yaml
groups:
  - name: api_alerts
    rules:
      - alert: HighErrorRate
        expr: |
          sum by (job) (rate(http_requests_total{status=~"5.."}[5m]))
            / sum by (job) (rate(http_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High 5xx error rate ({{ $value | humanizePercentage }})"
```

### Alertmanager Routing

```yaml
# alertmanager.yml
route:
  receiver: default
  group_by: [alertname, job]
  group_wait: 30s
  group_interval: 5m
  routes:
    - matchers: ['severity="critical"']
      receiver: pagerduty
    - matchers: ['severity="warning"']
      receiver: slack

receivers:
  - name: pagerduty
    pagerduty_configs:
      - routing_key: "<pagerduty-events-v2-routing-key>"
  - name: slack
    slack_configs:
      - channel: "#alerts"
        api_url: "<webhook_url>"
  - name: default
    email_configs:
      - to: "oncall@example.com"
```

### Validate Alerting Configuration

```bash
promtool check rules rules.yml
amtool check-config alertmanager.yml
amtool config routes test --config.file=alertmanager.yml severity=critical
```

## Recording Rules

Pre-compute expensive PromQL for dashboard performance:

```yaml
groups:
  - name: api_rules
    interval: 1m
    rules:
      - record: job:http_requests:rate5m
        expr: sum by (job) (rate(http_requests_total[5m]))
      - record: job:http_request_duration_seconds:p99
        expr: histogram_quantile(0.99, sum by (job, le) (rate(http_request_duration_seconds_bucket[5m])))
```

### Deploy and Verify Recording Rules

```bash
# 1. Validate rule syntax
promtool check rules rules/recording.yml

# 2. Reload Prometheus (after adding to rule_files in prometheus.yml)
promtool check config prometheus.yml
# The HTTP reload endpoint requires --web.enable-lifecycle (disabled by default):
curl -X POST http://localhost:9090/-/reload
# Alternatively, signal the Prometheus process with SIGHUP via the service manager.

# 3. Verify rules are active
curl -s http://localhost:9090/api/v1/rules | jq '.data.groups[].rules[] | {name, health}'
```

## Metrics Drilldown (Grafana 12+)

Queryless Prometheus exploration — browse metrics without writing PromQL. Navigate to
**Drilldown > Metrics** or use `<grafana-url>/a/grafana-metricsdrilldown-app`.
Provides metric search with label breakdown, smart segmentation for anomaly detection,
auto-visualization, and telemetry pivoting from metrics to related logs and traces.

## Resources

- [PromQL Reference](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Grafana Cloud Metrics](https://grafana.com/docs/grafana-cloud/send-data/metrics/)
- [Metrics Drilldown App](https://github.com/grafana/metrics-drilldown)
- [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)
- [Grafana Mimir](https://grafana.com/docs/mimir/latest/)
