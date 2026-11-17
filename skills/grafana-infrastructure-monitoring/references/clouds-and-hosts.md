# Cloud-provider + host / container collection

Local YAML provisioning applies to **self-hosted Grafana**. For hosted Grafana Cloud, use its UI/API or the Grafana Terraform provider; there is no host filesystem to edit or Grafana process to restart. Cloud-hosted Grafana cannot use the customer VM's EC2/GCE metadata identity. Select an explicitly supported hosted authentication/assume-role method.

## AWS CloudWatch

Scrape via the CloudWatch exporter:

```alloy
prometheus.scrape "cloudwatch" {
  targets    = [{__address__ = "cloudwatch-exporter:9106"}]
  forward_to = [prometheus.remote_write.cloud.receiver]
}
```

Or use the CloudWatch datasource directly:

```yaml
# provisioning/datasources/cloudwatch.yaml
apiVersion: 1
datasources:
  - name: CloudWatch
    type: cloudwatch
    jsonData:
      defaultRegion: us-east-1
      authType: keys             # inline credentials supplied securely below
      # Or explicit creds:
      # authType: credentials   # means a shared credentials file, not inline keys
    secureJsonData:
      accessKey: <injected-access-key>
      secretKey: <injected-secret-key>
```

## Azure Monitor

```yaml
# provisioning/datasources/azure.yaml
apiVersion: 1
datasources:
  - name: Azure Monitor
    type: grafana-azure-monitor-datasource
    jsonData:
      azureAuthType: clientsecret
      cloudName: azuremonitor
      subscriptionId: your-subscription-id
      tenantId:  your-tenant-id
      clientId:  your-client-id
    secureJsonData:
      clientSecret: your-client-secret
```

## Google Cloud Monitoring

```yaml
# provisioning/datasources/google.yaml
apiVersion: 1
datasources:
  - name: Google Cloud Monitoring
    type: stackdriver
    jsonData:
      authenticationType: jwt
      clientEmail: service-account@project.iam.gserviceaccount.com
      tokenUri: https://oauth2.googleapis.com/token
      defaultProject: your-project
      # Or JWT:
      # authenticationType: jwt
    secureJsonData:
      privateKey: |
        -----BEGIN PRIVATE KEY-----
        <injected PEM key, not the full service-account JSON>
        -----END PRIVATE KEY-----
```

## Node Exporter (Linux host) via Alloy

```alloy
prometheus.exporter.unix "host" {
  rootfs_path = "/"
  enable_collectors = ["cpu", "diskstats", "filesystem", "loadavg", "meminfo", "netdev", "stat", "time", "uname"]
}

prometheus.scrape "node" {
  targets         = prometheus.exporter.unix.host.targets
  forward_to      = [prometheus.remote_write.cloud.receiver]
  scrape_interval = "60s"
}
```

## Docker / cAdvisor via Alloy

```alloy
prometheus.scrape "cadvisor" {
  targets      = [{"__address__" = "localhost:8080"}]
  metrics_path = "/metrics"
  forward_to   = [prometheus.remote_write.cloud.receiver]
}

discovery.docker "containers" {
  host = "unix:///var/run/docker.sock"
}

loki.source.docker "containers" {
  host       = "unix:///var/run/docker.sock"
  targets    = discovery.docker.containers.targets
  forward_to = [loki.write.cloud.receiver]
}
```

## Forwarding components required by the host snippets

The scrape/source fragments above reference these writers; include them in the same Alloy configuration. Their endpoints/tenant IDs are signal-specific, and secrets below must come from an approved deployment secret mechanism.

```alloy
prometheus.remote_write "cloud" {
  endpoint {
    url = sys.env("PROMETHEUS_REMOTE_WRITE_URL")
    basic_auth {
      username = sys.env("METRICS_TENANT_ID")
      password = sys.env("METRICS_WRITE_TOKEN")
    }
  }
}
loki.write "cloud" {
  endpoint {
    url = sys.env("LOKI_PUSH_URL")
    basic_auth {
      username = sys.env("LOGS_TENANT_ID")
      password = sys.env("LOGS_WRITE_TOKEN")
    }
  }
}
```

Validate the assembled Alloy configuration and inspect actual exported telemetry; references to undefined components are not a complete deployment. Sources: Grafana [CloudWatch](https://grafana.com/docs/grafana/latest/datasources/aws-cloudwatch/configure/), [Azure Monitor](https://grafana.com/docs/grafana/latest/datasources/azure-monitor/configure/) and the installed plugin's GCP authentication schema.
