# python-observability Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic runs concurrent requests/tasks, executor hops, worker restart/shutdown, exporter failure, and a known error containing sensitive input. Probe duplicate events, context bleed between requests, orphan spans, cardinality explosion, and lost flush.

Block when required diagnostic/security evidence is materially false/missing or telemetry can leak sensitive data/cause serious runtime failure. Cosmetic naming is non-blocking.

## QA depth

Increase depth with async/thread/process concurrency, framework middleware, high volume/cardinality, audit/security use, exporter lifecycle, and SLO dependence.
