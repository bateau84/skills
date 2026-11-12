# PR #29 cold-review remediation — 2026-11-12

The independent review examined `c035f215db8bf84dabe1aa63d50666bd1aa3d0c6` against `569222093f8c13b1c35714e70eddda53d87511a4`. It found two blocking guide defects and several smaller gaps, while confirming the evaluator's tool-call path and preservation of merged upstream work. This record distinguishes those review observations from the follow-up changes; it is not an independent approval of the new revision.

## Disposition

| Finding | Correction / boundary |
| --- | --- |
| F1 — SDK docs select the wrong major | All SDK README links in the MCP practitioner package now select `v1.x`, matching the examples. A package-wide consistency check prevents drifting back to `main`; the v2 migration guide remains deliberately labelled as migration material. |
| F2 — TypeScript guide errors appear successful | The actual user-search catch returns `isError: true`, and the description states that contract. A TypeScript test extracts and executes this guide example through real SDK in-memory transport, substituting only its upstream API/error-formatting dependencies. It checks the error flag at the client, not just the wording. |
| F3 — Python lifespan attribute | The guide uses `request_context.lifespan_context`. Structural and installed-SDK checks cover the field used by the guide. |
| F4 — Go example mutates on build | The module declares Go 1.25.0 and includes a generated `go.sum` and tidy requirements. Generation used the default Go checksum database without mirror replacements or `GOSUMDB=off`. CI selects the toolchain from `go.mod`, verifies modules, requires `go mod tidy -diff`, builds with `-mod=readonly`, and fails on tracked module-file changes. |
| F5 — dash-leading server arguments | CLI help and the evaluation guide explicitly require `-a=--flag` / `-a=-y`. Parser tests cover both the valid equals form and rejection of the ambiguous space-separated form. No custom parser that might reinterpret evaluator flags was introduced. |
| F6 — duplicate payload and false error | Text is forwarded once. Structured content is a fallback when no nonempty text is present. Unsupported modalities produce explicit placeholders without changing the server's `isError`, avoiding a false failure/retry signal. These tasks remain outside this text-only evaluator's supported coverage. |
| F7 — model-call cancellation | `AsyncAnthropic` replaces the synchronous client offloaded to a thread. Calls are awaited directly and the client is owned by an async context manager. Tests check cancellation reaches the pending model transport and closes the owner. This cannot guarantee a provider stopped remote computation or billing. |
| F8 — partial-repair residue | Replaced all five remaining `promql-cli` references, removed the stale `go tool golangci-lint` command, corrected the Cobra directive, aligned workspace command/output and aligned the Grafana metrics skeleton's cluster/authentication instructions. No unused Secret is presented as connected to the chart. |
| F9 — provider rewrite coverage | Added one action-schema/registration case and one resource-Read absence-versus-auth/timeout case. These are development regression guards, not measured evidence of agent uplift or cloud acceptance. |
| F10 — case accounting and uplift | Independently reproduced the distinction: of the 446 base cases, **432 are unchanged and 14 were corrected in place**, including two substantive replacements. Identity preservation is not semantic equivalence. None of the 475 previously reviewed cases changes in this follow-up; the two new cases bring the total to 477 across 105 skills. No live model evaluation was run. |
| F11 — reference reproducibility | Commit the npm lockfile and use `npm ci`; commit Go module sums and prohibit build-time rewrites; select Node/Python/Go explicitly; cap Anthropic's major range and constrain the tested direct SDK versions. Python transitive dependencies still resolve within their package constraints: this is not a claim of a fully hashed, platform-independent Python lock. |

An additional inspected concern was confirmed: stripping the value after `KEY=` changed intentional environment whitespace. The parser now preserves it, with a regression for spaces, empty values and embedded `=`.

## Evidence and limits

The exact source tree and generated Go/npm dependency files were retrieved from a read-only, revision-pinned GitHub job. Go module generation and verification retained `sum.golang.org`; no checksum bypass or source substitutions were used. The two relevant workflow logs and final-head status belong in the PR body rather than immutable completion claims here.

Local documentation checks reproduced the old SDK-link, lifespan-field, dead-reference, Cobra-directive and workspace mismatches before correction. Runtime tests reproduced duplicate content, erroneous non-text error flags and environment-value trimming. Async model/client tests now define direct cancellation rather than a detached thread contract. Actual installed-SDK tests are required by the reference CI job and may be skipped only in a dependency-free local harness.

The TypeScript test reads the guide itself; it does not hand-copy the corrected result into a fake. The real-Python-SDK tests use a fake remote HTTP service, not a fake serializer. No paid API request, authenticated cloud deployment, Terraform apply or merge is part of this remediation.

Current upstream references: [Python SDK v1](https://github.com/modelcontextprotocol/python-sdk/tree/v1.x), [TypeScript SDK v1](https://github.com/modelcontextprotocol/typescript-sdk/tree/v1.x), [Anthropic async client exports](https://github.com/anthropics/anthropic-sdk-python/blob/v2.8.0/src/anthropic/__init__.py), [Plugin Framework Go requirement](https://github.com/hashicorp/terraform-plugin-framework/blob/v1.19.0/go.mod).
