# `k8s-monitoring` Helm values reference

## Values for `grafana/k8s-monitoring` 4.x

**Do not reuse the old v1 `externalServices`, `metrics.*`, or `logs.pod_logs` values:** chart 4.x expects named destination and collector **maps** with independently enabled features. This is a minimal **metrics-only skeleton**, not a complete production deployment or an example of secure credential provisioning. Derive the complete values (including logs, traces and collection routing) from the **exact installed version** and [Grafana's chart upgrade documentation](https://github.com/grafana/k8s-monitoring-helm/tree/main/charts/k8s-monitoring). Never commit real access-policy tokens in a values file.

```yaml
cluster:
  name: example-cluster

destinations:
  grafanaMetrics:
    type: prometheus
    url: https://prometheus-prod-<region>.grafana.net/api/prom/push
    auth:
      type: basic
      username: "<metrics-instance-id>"
      password: "<substitute-securely-before-apply>"

clusterMetrics:
  enabled: true

collectors:
  alloy-metrics:
    presets: [clustered, statefulset]
```

The `<...>` placeholders are **not** valid production configuration. Supply real endpoints and credentials through an approved secret-injection mechanism and validate the chart schema and generated resource manifests before installing:

```bash
helm show values grafana/k8s-monitoring --version 4.1.4 > chart-4.1.4.defaults.yaml
helm template k8s-monitoring grafana/k8s-monitoring --version 4.1.4 \
  -n monitoring -f values.yaml > rendered.yaml
# Review rendered destinations, collectors, permissions and receiver ports.
```

For pod logs and events, use the matching v4 feature names (`podLogsViaLoki`, `clusterEvents`); for traces configure `applicationObservability` and its receiver ports. Confirm support and required collector settings in the version-pinned chart rather than assuming this metrics skeleton enables all signals.

## Useful Kubernetes PromQL

```promql
# CPU usage by pod
sum(rate(container_cpu_usage_seconds_total{namespace="$namespace", container!=""}[5m])) by (pod)

# Memory by pod
sum(container_memory_working_set_bytes{namespace="$namespace", container!=""}) by (pod)

# Node CPU pressure
1 - avg(rate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)

# Pod restarts
increase(kube_pod_container_status_restarts_total[1h])

# Deployment readiness
kube_deployment_status_replicas_ready / kube_deployment_spec_replicas

# PVC usage
kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes
```

## Pre-built dashboards (grafana.com IDs)

- Kubernetes / Cluster — **15520**
- Kubernetes / Namespace — **15521**
- Kubernetes / Pod — **15522**
- Node Exporter Full — **1860**
- cAdvisor — **14282**

## Infrastructure alert rules

```yaml
groups:
  - name: kubernetes-alerts
    rules:
      - alert: PodCrashLooping
        expr: rate(kube_pod_container_status_restarts_total[15m]) * 60 * 15 > 0
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "Pod {{ $labels.namespace }}/{{ $labels.pod }} crash looping"

      - alert: NodeMemoryPressure
        expr: (node_memory_MemAvailable_bytes / node_memory_MemTotal_bytes) < 0.1
        for: 5m
        labels: { severity: critical }
        annotations:
          summary: "Node {{ $labels.instance }} low memory (<10% free)"

      - alert: PersistentVolumeAlmostFull
        expr: kubelet_volume_stats_available_bytes / kubelet_volume_stats_capacity_bytes < 0.1
        for: 5m
        labels: { severity: warning }
        annotations:
          summary: "PVC {{ $labels.namespace }}/{{ $labels.persistentvolumeclaim }} almost full"
```
