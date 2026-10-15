# loki Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic creates a high-cardinality label, malformed log line, missing stream, empty tenant, retention boundary, and broad long-range query. Ask whether the query returns plausible numbers even when parsing failed or logs stopped arriving.

Block when load-bearing diagnosis/alerting materially lies, tenant/security/retention boundaries fail, or label/query design can cause serious availability/cost impact. Minor query style is non-blocking.

## QA depth

Increase depth with ingest volume/cardinality, tenant count, retention, broad query ranges, parser diversity, alert/SLO use, sensitive logs, and distributed Loki architecture.
