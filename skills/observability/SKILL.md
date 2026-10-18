---
name: observability
description: "Logs, metrics, and traces written into code as a first-class deliverable — structured logging, log levels, metrics cardinality, request-flow tracing, and correlation. Use when deciding what to log, choosing between a log / metric / trace, separating operational vs audit vs diagnostic logs, instrumenting a feature or boundary, or judging whether code is observable enough to ship. Not for language or APM mechanics (→ See `golang-observability`, `python-observability`, `grafana-app-observability`)."
license: MIT
metadata:
  author: Bateau
  version: "1.2.0"
---

> Language-agnostic observability guidance for implementation, review, and diagnosis. Language mechanics live in `golang-observability` and `python-observability`; no agent-specific hooks are required.

**Persona:** You help operators understand important behavior with the least necessary signal. Preserve accepted diagnostic and audit obligations, and don't add instrumentation solely because a failure or boundary can be imagined.

## The first principle

Observability is the ability to understand system behavior from external outputs. Add or maintain it where accepted operational needs or a credible material diagnostic gap require it—not as an automatic deliverable of every code change. Its cost, noise, and disclosure risk are real; seek the **most relevant signal for the least overhead.**

## Three pillars — reach for the right one

The reflex "I want to see how the code is processing" usually wants a **trace**, not a log. Pick the signal that answers the question:

| Pillar | Question it answers | Reach for it when |
| --- | --- | --- |
| **Logs** | _What exactly happened in this one event?_ | A discrete event, decision, or error whose details you'll want after the fact. |
| **Metrics** | _How much / how often / how bad, in aggregate?_ | Rates, counts, latencies, saturation — anything you alert on or watch trend over time. |
| **Traces** | _Where did this request go, and where did the time go?_ | Following one request across functions/services, finding the slow or failing hop. **This is the tool for "watch it process."** |

The mistake to avoid: fossilizing print-debugging as **narration logs** ("entering X", "got here", "value=5"). That play-by-play is what a trace (or a diagnostic session) gives you for free, and it becomes pure noise in production. Log _decisions and outcomes_; trace _flow_; measure _aggregates_.

On a material cross-service diagnostic path, a span tree can show causality better than scattered logs. Add tracing where that visibility is needed and supported by the deployment; do not instrument every method, query, and external call by default.

## Log categories — they are not one thing

Split logs by audience and purpose; they have different levels, retention, and security rules. Lumping them produces logs that serve none well.

| Category | Purpose / audience | Typical level | Retention & handling |
| --- | --- | --- | --- |
| **Operational** | What the system did, for the operators running it (request handled, job ran, dependency degraded). | Info / Warn | Short-to-medium; the bulk of your volume — keep it lean. |
| **Audit** | Who did what, for compliance and security (authn, authz decisions, data access, config change). | Info (dedicated stream) | Long, often regulated; **immutable, access-controlled, never mixed into ops logs**. |
| **Diagnostic** | Why something happened, for the developer debugging it (branch taken, computed value, intermediate state). | Debug | Off or sampled in prod; on-demand. Must be cheap to disable. |

A single event can warrant entries in more than one stream — an auth failure is an _audit_ record _and_ an _operational_ warning — but write them deliberately to their stream; do not conflate them.

### Audit logging when required

Security and compliance audit behavior must follow the **actual accepted contract, regulations, and threat model**. Identify which actions require audit events, who must consume them, and what loss, retention, access, and integrity guarantees apply. For genuinely required durable audit records, protect against unauthorized alteration or loss with mechanisms suited to that contract.

A dedicated, immutable, unsampled pipeline or synchronous write may be necessary for high-assurance auditing, but none is a universal obligation for every application log. Do not introduce WORM storage, hash chains, GDPR pseudonymization machinery, or separate log infrastructure solely because the task adds an ordinary operational event. Missing mandatory audit guarantees are material findings; optional stronger ones are advisory.

## The discipline (what turns expensive spray into cheap signal)

- **Log material outcomes at useful boundaries, not in hot loops** — capture decisions and failure context that operators actually need. An external call or possible error path does not automatically deserve its own log.
- **Log an error exactly once, at the handler.** Below the handler, wrap and propagate (`fmt.Errorf("get user %s: %w", id, err)` / raise with context). Do not log _and_ return — every layer that does creates a duplicate. The single log at the top handler carries the full chain plus the request context. This is the difference between a useful error trail and a wall of repeated noise.
- **Structured over freeform.** Emit key/value fields rather than interpolated prose. A structured field is greppable, aggregatable, and _assertable in a test_. Use JSON in production (shipped to the aggregator) and a human-readable format (logfmt / colourised) on the developer terminal — one logger, two handlers.
- **Canonical fields.** Every record carries at minimum: `timestamp` (UTC, ISO 8601 or ns-epoch), `level`, `message`, `service.name`. Add when in scope: `trace_id` + `span_id` (correlation), `service.version` (tie incidents to releases), `environment` (never mix prod/staging), `error.type` + `error.message` (on error paths), `caller` (file:line, on Error/Debug). Put data in named fields, never baked into the message string — `"user 12345 paid $99"` is unqueryable; `user_id=u_12345 amount=99.99` is searchable.
- **Right level, every time.** The deciding question is _whose fault is it?_
  - **Error** — *your system* failed and could not recover without intervention (DB down, unhandled exception, 5xx returned).
  - **Warn** — something unexpected happened but the system recovered (retry succeeded, approaching a quota, deprecated path hit).
  - **Info** — a normal business event at a boundary (request handled, job completed, config loaded). If the caller sent bad input and you returned a clean 4xx, that is Info or Debug — your system worked as designed.
  - **Debug** — diagnostic detail that is off in production by default.
  
  The most common noise source is logging every user-error (HTTP 400) as an Error. Resist it: the system is not broken, the input was.
- **Correlate the pillars.** Thread a request/trace id through logs, metric exemplars, and spans so all three line up for a single request. An uncorrelated log is archaeology.
- **Respect the transport.** Never write logs to a channel the protocol owns — for a stdio server, stdout is the wire, so logs go to stderr or a file.
- **Never log secrets or PII.** Tokens, passwords, keys, personal data. A careless log is a breach sitting in storage waiting to be grepped, and a compliance liability under GDPR/CCPA.

## The honest economics — cheap when disciplined, expensive when sprayed

"It costs nothing when dormant" is a myth. A log you never read still costs:

- **Compute** — an unguarded `debug(expensiveFormat(x))` pays the formatting/allocation even when the level is off. Guard hot-path logs, or pass structured fields the handler formats lazily.
- **Money** — ingestion, indexing, and retention are often the single biggest observability line item. Over-logging is the bill that gets budgets cut, taking the _good_ logs with it.
- **Attention** — every line is something a future reader must triage. Over-logging buries the one line that matters; noise is _negative_ value.
- **Risk** — every log is a potential PII/secret leak and an attack surface in storage.
- **Cardinality** — putting unbounded high-cardinality values (user IDs, request IDs) as *metric label keys* rather than *log field values* creates a time-series explosion that kills Prometheus-style systems. Fine in a log record's fields; catastrophic as a dimension on a counter or histogram.

So: more logging is not more observability. Deliberate signal is.

**The canonical log line pattern.** Instead of N fine-grained INFO lines scattered through a request, emit **one rich record at the request boundary** that collects everything worth knowing (method, path, status, latency, user, key IDs, trace_id). This collapses noise into a single searchable, alertable line — reinforcing both boundary-logging and cost discipline. Extend the pattern to background jobs, queue messages, and cron runs: anywhere there is a logical unit of work with a clear entry and exit.

## Observability is not prevention

Logging makes a failure _detectable_; it does not make it _not happen_. Keep it strictly **below** "make illegal states unrepresentable" (types, assertions, validate-at-the-boundary). The trap is _"we'll see it in the logs"_ becoming the excuse a weak invariant ships behind. The strongest code makes the error impossible; the next best makes it loud. Observability is the second tier — invaluable, but not a substitute for a guarantee. (This is the runtime counterpart to the silent-wrong-output defect: instrumentation _surfaces_ a confidently-wrong value; a real invariant _prevents_ it.)

## Observability is testable behavior

When a diagnostic or audit signal is part of the **accepted behavior**, assert on its externally useful property (see `test-driven-development`). Don't add logging tests or instrumentation requirements for every possible failure. Never emit secrets or raw sensitive inputs merely to make a test inspectable.

Observable output can support human and agent verification: running the real path and inspecting its results provides evidence that source read-back alone cannot. Swallowed errors or missing operational signals can obscure failures. Use telemetry where operators need it, alongside assertions on returned values, state, or other relevant outcomes; a feature does not need a log line merely to be testable. Missing telemetry is a gap when the required diagnostic or audit behavior depends on it, not proof that only a human can verify the feature.

## Completion and proportionate visibility

Before calling an operationally significant change done, ask:

1. Does the accepted outcome require operator-visible diagnostics or audit evidence, and is that signal available?
2. Are newly affected **material** failures distinguishable without exposing secrets or creating excessive noise?
3. Does the signal match the repository's existing observability practice rather than add a second logging or tracing system?

A change with no new operational diagnostic obligation can finish with its existing logs and behavior-level tests. Missing evidence of a **required** audit or diagnostic promise is a gap; a hypothetical stronger observability guarantee is not an automatic blocker.

## Cross-references

- The project's observability conventions — signal ownership, operational needs, and verification expectations.
- `golang-observability` — Go mechanics: logger choice, `zap`/`otelzap` wiring, `context.Context` propagation rules, Loki label strategy, RabbitMQ `traceparent` propagation, audit storage decisions, HTTP status level conventions, Prometheus, pprof.
- `python-observability` — Python mechanics: `logging` / `structlog`, metrics, OpenTelemetry.
- `test-driven-development` — asserting on logs/metrics/spans as observable behavior.

---

This skill covers signal design. Load the language-specific skill when the task actually needs those implementation mechanics.
