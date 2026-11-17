# Review integration: previously unevaluated skills

## Scope and provenance

The user supplied a review of 63 skills at the earlier PR head, not measured model results. Its counts (180 labelled VERIFIED, 250 SUSPECTED, 303 draft cases) remain **reviewer-reported**, not 430 independently reproduced defects. The archive of all draft cases was not supplied to this execution. We do not claim to have imported it.

During recovery, `main` advanced through #30–#32 to `569222093f8c13b1c35714e70eddda53d87511a4`. Those PRs already implemented corrections and curated regression cases. This change is reconciled on that exact main, preserving every one of its 446 case IDs and all merged source fixes. The earlier 392/59 and recovered 425/85 inventories are historical, not current acceptance counts.

The abandoned drafts were not safe to publish verbatim: a Terraform heading still said `docs/`, a later logging edit lost the newline fix, and the MCP connection stripped the error flag before the new normalizer could see it. The Terraform correction was already in main; the other two were repaired together with consistency checks of their callers and examples.

## Disposition of the 63 skill packages

The table records the bounded concerns inspected and addressed here or preserved from main. It is **not** a statement that every speculative sub-finding in the original report is proven. Unsupported generic mandates were qualified or removed instead of turning them into permanent skill rules. Companion files remain optional context, not automatically loaded production instructions.

| Skill | Disposition |
| --- | --- |
| `accessibility-design` | Correct target geometry, authentication exceptions, focus levels and terminal-accessibility claims; remove unsupported fixed cognitive limits. |
| `accessibility-implementation` | Specify an actual safe initial dialog focus target; align the declared WCAG target. |
| `anchor-authoring` | Make optional review companions discoverable; keep external OKF integration optional, not a missing mandatory local service. |
| `cli-design` | Separate POSIX shell statuses from CLI conventions; remove default credential-in-env advice and contradictory syntax claims. |
| `design-implementation` | Clarify the implementation boundary and use applicable accessibility verification rather than invented universal thresholds. |
| `desktop-ui-design` | Correct Electron accessibility activation, platform shortcuts, persistence terminology and focus-appearance level. |
| `documentation` | Provide a repository-native fallback when an optional OKF integration is unavailable. |
| `experience-design` | Respect bounded requests and user-approved product meaning; separate scenario ownership. |
| `git-commit-discipline` | Distinguish index/worktree restore and require a captured expected SHA for authorized force-with-lease rewrites. |
| `git-conflicts` | Repair conflictStyle, abort semantics, staged-state caveats and implicit lease claims. |
| `github-action` | Document current Node24 targeting without falsely claiming every old-runtime action stopped working. |
| `github-workflow` | Make checkout credentials, environment-file injection, cache producer trust and explicit permissions concrete. |
| `golang-benchmark` | Correct cob ratios, gobenchdata schema/JSON inputs, redirects, Elapsed and pprof filtering/heap interpretation. |
| `golang-cli` | Remove layout mandates and make returned error printing explicit with SilenceErrors. |
| `golang-code-style` | Allow nil slices where appropriate; preserve short-circuit guards, stdlib-first choices and caller formatting intent. |
| `golang-common-practice` | State what build, test and ./... actually cover; do not conflate package checks with tagged/nested-module coverage. |
| `golang-concurrency` | Qualify sync.Map and timer semantics instead of imposing one universal implementation rule. |
| `golang-context` | WithoutCancel drops deadlines too; transfer cancel cleanup explicitly and distinguish timeout from a bounded work owner. |
| `golang-continuous-integration` | Use immutable action references and avoid asserting absent workflow implementations exist. |
| `golang-data-structures` | Version map internals, correct shallow aggregate copies and unsafe/weak-pointer API provenance. |
| `golang-dependency-injection` | Use the pinned do/v2 executable example; remove Wire-as-default and compile-time graph/transient/lazy-init myths. |
| `golang-dependency-management` | Avoid calling broad go get -u safe or injecting lint-tool dependencies into the application graph by default. |
| `golang-design-patterns` | Align fallible option examples, observe listener failures, and distinguish sync.Pool from a bounded resource pool. |
| `golang-documentation` | Replace mandatory Javadoc boilerplate with Go prose; prohibit unauthorized publication of private source/docs. |
| `golang-error-handling` | Align error field names and avoid hiding an owned sentinel at the same boundary used to protect external errors. |
| `golang-grpc` | Correct proto include roots/package paths; identify legacy PGV instead of calling it Protovalidate. |
| `golang-how-to` | Repair missing sibling routes and missing Configure destination without adding automatic repository mutation. |
| `golang-lint` | Retain merged nolintlint settings correction and use the v2 installation path/version boundary. |
| `golang-modernize` | Fix slice range, distinguish recommended alternatives from deprecated APIs, and gate runtime defaults on module/toolchain settings. |
| `golang-naming` | Qualify local naming preferences rather than claiming universal Go suffix/bool/acronym rules. |
| `golang-observability` | Remove a forced workspace logging stack; fix slog/zap bridge construction and explicit provider/trace context. |
| `golang-performance` | Correct compiler vectorization/CPU target/preemption claims and require evidence for tuning. |
| `golang-pkg-go-dev` | Remove invented vuln flags/filter fields; distinguish catalogue vulnerability lookup from reachable-code govulncheck. |
| `golang-popular-libraries` | Stop presenting legacy/unmaintained choices as timeless defaults; include modern stdlib alternatives. |
| `golang-project-layout` | Allow root commands/libraries; fix workspace removal and binary-build output; avoid mandatory multi-module structure. |
| `golang-safety` | Align practitioner, assessment and QA with its non-adversarial safety scope. |
| `golang-security` | Use html/template, qualify constant-time length behavior, reconcile log sanitization with structured output and sensitive-data controls. |
| `golang-spf13-cobra` | Correct help/deprecation, CheckErr destination, completion constants and generator parent references. |
| `golang-spf13-viper` | Value-type error match, mapstructure/v2, default hooks, env key registration, lazy flag binding and actual watcher lifecycle. |
| `golang-stretchr-testify` | Equal compares values; Same asserts pointer identity. A pinned-package test checks both. |
| `golang-tui` | Fix focus clamps, generic constraint, ANSI helper arity, panic argument and package-qualified test/run commands. |
| `grafana-app-observability` | Preserve merged replay correction; fix metrics/job names, CORS configuration, span kind, sampling fan-out and detector names. |
| `grafana-dashboards` | Use binary calculation for the ratio and an appropriate percent display unit. |
| `grafana-infrastructure-monitoring` | Use chart-v4 maps and version-pinned rendering; fix cloud datasource fields and distinguish hosted from self-managed provisioning. |
| `grafana-loki` | Correct unwrap conversion/error filtering and glob discovery; keep cardinality and source topology explicit. |
| `grafana-mimir` | Preserve merged chart-6/Kafka changes; correct default query prefix without changing ingestion URL. |
| `intent-grilling` | Add concise decision playback without inventing a mandatory gate for every bounded task. |
| `mcp-builder` | Repair the full connection/serialization boundary and all tool-result IDs; add real SDK and TypeScript stdio checks; bound the v1 API surface. |
| `opentelemetry` | Preserve merged Python HTTP/4318 correction; fix header wrapping, JS resources, exporter protocol and Operator examples. |
| `product-discovery` | Keep bounded requests bounded and route experience/scenario work to the proper owner. |
| `product-lifecycle` | Remove the duplicated behavioral-spec step and restore the human-facing/documentation handoff. |
| `prometheus` | Replace out-of-scope query cheat sheet with scrape/relabel/retention/remote-write guidance; fix alert routing and reload prerequisites. |
| `promql` | Correct healthy-versus-missing staleness detection and qualify histogram/label pipeline diagnoses. |
| `python-database-orm` | Use an outer transaction and savepoint-joining session; explicitly require backend/driver support and test application commits. |
| `python-design-patterns` | Use current validation/ORM APIs and stdlib-compatible logger arguments; preserve the pre-refactor validation contract. |
| `risk-driven-planning` | Teach irreversibility, correlated assumptions and mechanism-exercising checks that companions already expected. |
| `synabun-memory` | Discover an authorized existing project identifier or ask; do not invent one to satisfy a tool schema. |
| `terraform-module-testing` | Preserve upstream mock fixes; fix file filters and remove plan assertions on unknown computed IDs without adding real applies. |
| `terraform-provider-actions` | Replace AWS-private/made-up APIs with public Framework interfaces and an executable version-pinned example. |
| `terraform-provider-docs` | Already corrected on main by #31/#32; retain its templates/actions paths, provider-prefixed example directories and tag semantics unchanged. |
| `terraform-provider-resources` | Replace private AWS helpers presented as generic APIs with explicit public-framework contracts and clearly project-owned collaborators. |
| `terraform-provider-testing` | Correct the no-op-after-update scenario and collection path list shape. |
| `visual-companion` | Refresh session paths on restart; distinguish clicks from selected state; fix stop path, timestamps, stale event and token cleanup guidance. |

## Verification and regression coverage

- Current corpus: **475 cases across 103 skills**; **29 new cases** beyond main. All **446 current-main IDs are preserved**. Four recovered duplicate cases were omitted because merged cases already cover the same defects. These fixtures are regression/development inputs, not independent holdouts.
- The provider-free harness uses the exact external runner `dbbbf2a0740aee7a9e9035cc14a785a9467b8fb1`. Tests that only build container arguments substitute executable discovery, while a separate test verifies a missing engine still raises the production error. No OCI executable or image is falsely claimed to have run.
- MCP tests exercise the real owned connection-to-evaluator path, including error envelopes, structured content, multiple tool calls, non-text results, cancellation and CLI parsing. The initial draft failed six of seven focused cases; the corrected path passes. Optional Python SDK tests use actual protocol/model classes and a fake HTTP network boundary, not a live provider.
- The reference-check workflow requires the optional SDK packages, compiles the pinned TypeScript example, and starts a real local stdio client/server for handshake/tool/resource/error checks. A Go reference module compiles public Terraform action/provider interfaces and tests Viper, Testify and do/v2 behavior against pinned direct dependencies.
- Current-run command output and CI conclusions belong in the PR verification section rather than a committed document that will call an old SHA “final.”

## Claim boundaries and verification sources

No model-provider calls, paid evaluations, Terraform cloud applies, authenticated Grafana deployments or user-credential operations are authorized by these tests. A successful compiler check is not a cloud acceptance test. The chart example is an explicit metrics-only skeleton; use the exact deployment's chart schema, secrets and rendered resources before any apply. SDK v1 support is a deliberate compatibility boundary, not a claimed v2 migration.

Several report conclusions need qualification: an unlinked ASSESSMENT/QA is not intrinsically unreachable when the host selects companions; external OKF integration is not a mandatory local dependency; environment variables are not a universally safe secret channel; a Go convention is not a language rule; and a Node runtime migration does not prove every old action has stopped executing. Performance, statistical and UX preferences are not universal correctness criteria.

Primary sources checked for the changed technical contracts:

- [Viper v1.20.1](https://github.com/spf13/viper/tree/v1.20.1), [Testify assertions](https://pkg.go.dev/github.com/stretchr/testify/assert), [do/v2](https://pkg.go.dev/github.com/samber/do/v2), [Cobra v1.10.1](https://github.com/spf13/cobra/tree/v1.10.1).
- [Go module layout](https://go.dev/doc/modules/layout), [Swiss maps](https://go.dev/blog/swisstable), [testing](https://pkg.go.dev/testing), [pprof filtering](https://go.dev/src/cmd/vendor/github.com/google/pprof/internal/driver/commands.go), [golangci-lint installation](https://golangci-lint.run/docs/welcome/install/local/), [gobenchdata](https://github.com/bobheadxi/gobenchdata).
- [WCAG target size](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html), [authentication](https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html), [Electron accessibility](https://www.electronjs.org/docs/latest/tutorial/accessibility), [CLI Guidelines](https://clig.dev/).
- [MCP Python SDK migration](https://py.sdk.modelcontextprotocol.io/migration/), [SDK-v1 TypeScript example](https://github.com/modelcontextprotocol/typescript-sdk/blob/v1.x/src/examples/server/simpleStatelessStreamableHttp.ts), [MCP elicitation](https://modelcontextprotocol.io/specification/latest/client/elicitation).
- [Terraform tests](https://developer.hashicorp.com/terraform/cli/commands/test), [mocking](https://developer.hashicorp.com/terraform/language/tests/mocking), [public action implementation](https://developer.hashicorp.com/terraform/plugin/framework/actions/implementation), [SQLAlchemy external transactions](https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites).
- [Grafana chart 4.1.4 values](https://github.com/grafana/k8s-monitoring-helm/blob/k8s-monitoring-4.1.4/charts/k8s-monitoring/values.yaml), [span metrics](https://grafana.com/docs/alloy/latest/reference/components/otelcol/otelcol.connector.spanmetrics/), [Faro replay](https://grafana.com/docs/grafana-cloud/observe-and-act/monitor-applications/session-replay/instrument/), [Prometheus config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/), [Operator instrumentation](https://opentelemetry.io/docs/platforms/kubernetes/operator/automatic/).
