# Major Version Upgrade — Quality Assurance

Adversarially test a reviewed major upgrade for failures that normal migration work can still miss. Focus on semantic drift, hidden coupling, mixed-version states, irreversible state changes, transitive surprises, and false rollback confidence.

## QA criteria

1. **Attack changed defaults that escaped source review.** Compare behavior-sensitive defaults before and after: timeouts, retries, auth/security posture, serialization, concurrency, resource limits, connection handling, feature enablement, error policy, and generated output where relevant.
2. **Attack cold and optional paths.** Exercise lazy initialization, rarely used features, optional plugins, alternate configuration, error paths, shutdown/restart, scheduled work, migrations, and code that is not reached by the normal smoke test.
3. **Attack mixed-version composition.** If old and new processes, clients, workers, or services can coexist even briefly, test both directions of interaction. Look for incompatible messages, schemas, caches, locks, leases, or coordination semantics.
4. **Attack rollback after state has changed.** Let the new version write representative durable state or emit its new protocol form, then test the real rollback/restore path. Identify the precise point where rollback ceases to be safe.
5. **Attack transitive and plugin drift.** Inspect unexpected graph changes, duplicate major versions, peer/plugin compatibility, removed optional dependencies, changed native components, and runtime/toolchain floors that may differ across development and production.
6. **Attack tests that migrated with the bug.** Check whether expected outputs were updated simply because the new version produced them. Reconstruct the accepted behavior independently and compare both old and new implementations when possible.
7. **Attack environment skew.** Exercise material differences such as OS/architecture, runtime version, container base, filesystem, locale/timezone, database/server version, browser/client, or feature flags when the upgraded component is sensitive to them.
8. **Attack performance and resource assumptions.** Major releases can change pooling, caching, concurrency, allocation, batching, indexes, query plans, startup cost, or defaults without breaking correctness. Probe the limits that matter to this system rather than benchmarking everything.
9. **Attack external consumers.** Look for callers outside the obvious repository path: generated clients, scripts, plugins, cron jobs, stored payloads, operators, dashboards, or sibling services that may depend on old names, formats, status codes, timing, or failure behavior.
10. **Attack generated and cached artifacts.** Ensure old generated clients, schemas, compiled assets, container layers, caches, or vendored outputs cannot survive the upgrade and create a mixed old/new state that ordinary source tests miss.
11. **Attack recovery under interruption.** Stop the process during migration, restart after partial progress, repeat idempotent steps, and test cleanup after failure when the component owns stateful transitions.
12. **Attack confidence claims.** Match every strong claim such as "backward compatible", "safe rollback", "no behavior change", or "drop-in replacement" to observed evidence at that exact boundary.

## Adversarial probes

Use the probes that fit the upgrade:

- diff effective configuration, not only configuration files;
- run the same representative input through old and new versions and compare observable behavior;
- run old and new peers at the same time;
- write state with the new version and attempt rollback with the old version;
- start from stale caches, generated output, or persisted fixtures created by the old version;
- disable a compatibility shim to discover hidden consumers;
- inspect the complete dependency/plugin graph before and after;
- force the primary dependency to fail slowly, partially, or during shutdown/restart;
- exercise one low-frequency feature or alternate code path not covered by the main test suite;
- run a representative workload long enough to expose changed pooling, leaks, retries, or resource ceilings when those are plausible release risks.

## Confidence rule

Do not invent exotic failure modes merely because the upgrade is large. Raise a finding when a plausible hidden incompatibility can violate accepted behavior, corrupt or strand state, defeat rollout or rollback, create a security/operational regression, or make the supplied evidence materially weaker than the upgrade claims.
