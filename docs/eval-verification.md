# Evaluation tooling verification — 2026-10-13

Producer verification, **not independent review or live behavioral acceptance**.
Changes are uncommitted. No staging, commits, pushes, host dependency installs,
clones, or provider/live-model calls were performed. The initial image gap was
subsequently resolved by an **explicitly authorized** OpenCode-only container
build, including its required base-image/npm/apt prerequisites. This did not
enable automatic acquisition in the eval CLI. Existing skill
enrichment, the learning rename, historical baselines, manifests and pilot were
preserved. See [usage and boundaries](evaluations.md).

## Observed environment and source

* Python `3.12.3`; Bun `1.3.14`; Podman available at `/usr/bin/podman`.
* External runner HEAD:
  `1262ac8c2eebbd10af572e3e3560318f6113233b`.
  `git status --porcelain --ignored --untracked-files=all` returned no entries
  before and after the tests. Imports did not create dependency bytecode.
* Loom methodology was read with `git show` from
  `c16e2c793b8faa8d21cf2ca9833606676e461e79:scripts/run-evals.py`, not from its
  different current working-tree HEAD. No Loom runtime/source was edited.
* V2 config/agent/permission/skill/read schemas were inspected at OpenCode
  `v2.0.23`, Git object `0fd7e2829449b052abf0078666669302923d77af`:
  `packages/schema/src/config.ts`, `config/agent.ts`, `config/provider.ts`,
  `permission.ts`, and the core config-agent, skill-tool and read/file-access
  consumers. Ordered rules use last-match precedence; read resources are
  location-relative. Follow-up inspected `packages/plugin-browser/src/connection.ts`
  and core `plugin/skill.ts` plus `config/plugin/source.ts` to resolve the concrete
  runtime findings below. Source inspection is distinct from the real-image
  effective-config and observer proof subsequently recorded.
* The load-bearing runner `opencode run --auto` consumer was also traced through
  the pinned CLI's `run/run.ts` and `run/noninteractive.ts`: `--auto` replies
  `once` to permission **asks**, without rewriting configured deny rules. Core
  `Permission.assert` rejects a deny before raising an ask. This source trace
  does not claim an executed negative model-tool test.

## Commands and observed results

| Command | Observed result |
| --- | --- |
| `bun run eval:harness-test` | **44 tests, OK**, exit 0; follow-up run 3.853 seconds; original 40 retained |
| `bun run eval:validate` | `valid`, **235 cases / 50 skills**, provider calls 0 |
| `bun run eval:list -- --skills product-acceptance` | PA1–PA9 printed with canonical and qualified IDs |
| `bun run eval:list -- --skills work-decomposition` | WD1–WD7 printed with canonical and qualified IDs |
| `git diff --check` | No whitespace errors |
| `python3 -I -B scripts/tests/test_preservation.py --snapshot` | Incoming content digest below |

The preservation test rechecks all incoming files beneath `skills/` and
`evaluations/selective-enrichment/`, excluding only the intentionally appended
skill README and two newly added JSON copies. Its pre-edit digest is:

```text
abee72b9b30cf09ca7106fbd053239214949ad98c5738c842ca98b1989a3ba1f
```

The original 48 JSON fixture files still produce 219 cases. Adding the exact
Markdown-field copies adds acceptance 9 + decomposition 7 = **235**, not a new
interpretation of the historical pilot scores.

### Exact provider-free test inventory

All names below passed in the final harness run. Test files are under
`scripts/tests/`.

**`test_eval_cases.py`**

* `test_existing_corpus_has_219_cases_without_changing_source_ids`
* `test_markdown_conversion_preserves_all_reviewed_fields_exactly`
* `test_mismatched_skill_empty_rules_bad_ids_and_duplicate_ids_rejected`
* `test_three_loom_formats`

**`test_eval_cli.py`**

* `test_empty_unknown_selectors_and_no_model_fail_before_invocation`
* `test_native_target_only_cross_judge_explicit_model_reasoning_timeout_bounds`
* `test_real_cli_provider_free_alias_modes_and_live_safeguards`
* `test_selection_intersection_and_call_caps`

**`test_eval_integration.py` — actual pinned runner APIs, injected invocation I/O**

* `test_actual_comparison_material_policy_uses_boolean_fraction_delta`
* `test_actual_runner_command_uses_generated_config_readonly_project_no_loom_and_never_pull`
* `test_actual_runner_owned_storage_reread_tamper_and_summary`
* `test_complete_native_absence_is_failure_not_diagnostic_success`
* `test_completed_negative_exit_one_independent_of_relative_value`
* `test_copilot_judge_unsupported_runtime_is_allowed_only_for_text_judgment`
* `test_driver_negative_non_evidence_and_orchestration_exit_codes`
* `test_driver_persists_four_call_summary_from_verified_artifacts`
* `test_empty_output_and_invalid_judge_are_non_evidence_not_semantic_false`
* `test_exact_required_input_or_result_unavailable_never_backfilled`
* `test_four_calls_real_profile_fresh_projects_same_budget_blind_judges`
* `test_incomplete_candidate_skips_judge_and_blocks_comparison`
* `test_judge_tools_or_incomplete_capture_cannot_authorize_a_grade`
* `test_missing_runtime_object_is_non_evidence_and_no_judge`
* `test_observed_invocation_cannot_retry_even_on_matching_provider_error`
* `test_parallel_pairs_have_distinct_projects_and_preserve_side_order`
* `test_product_timeout_and_unsupported_boundary_are_non_evidence_no_retry`
* `test_reference_read_must_start_after_successful_native_load_terminal`
* `test_retries_only_runner_replay_safe_signature_and_attempts_persisted`
* `test_unknown_actor_and_baseline_contamination_prevent_attribution`

**`test_eval_judgment.py`**

* `test_10pp_policy_trap_fixed_regression_and_absolute_verdict_independent`
* `test_boolean_scores_include_negative_rule_compliance_and_declared_trap`
* `test_rule_fractions_represent_exact_threshold_not_float_subtraction`
* `test_strict_json_rule_ids_order_independent_exactly_once`

**`test_eval_runner.py`**

* `test_adapter_hash_and_cli_version_required_no_pull_or_network`
* `test_all_authored_python_and_embedded_provider_free_probes_compile`
* `test_mutable_tags_and_missing_local_image_fail_before_execution`

**`test_eval_security.py`**

* `test_all_treatments_disable_stock_skill_content_but_keep_native_loader`
* `test_current_v2_effective_config_has_deny_default_and_narrow_allow`
* `test_environment_drops_control_injection_but_keeps_credentials`
* `test_practitioner_copy_filters_evaluator_resources_and_rejects_symlink_escape`
* `test_provider_config_rejects_runtime_contamination`

**`test_preservation.py`**

* `test_incoming_enrichment_rename_history_and_original_fixtures_unchanged`

**`test_eval_probe.py` — follow-up regressions**

* `test_probe_manifest_retains_failure_observation_and_private_permissions`
* `test_real_runner_probe_builder_excludes_all_credential_mounts_and_environment`
* `test_stock_browser_deny_extension_is_not_a_permission_mismatch_or_allow_exception`

These tests run the real project normalizer/profile, runner plan/paired lifecycle,
canonical evidence validator/builders, replay-safe retry policy, classification,
paired storage/integrity, and reread-derived driver summary. They substitute the
actual invocation boundary with deterministic result/event inputs. Image command
tests substitute engine I/O, not a real compatible image. None is evidence that
a live model loaded a skill, obeyed permissions, or improved its practical answer.

### Self-review defects found and fixed

* Binary floating-point score subtraction can misclassify exactly 10pp. The
  comparison now derives the delta from exact Boolean fractions; policy tests
  cover both exact 10pp and a smaller positive delta.
* Aggregate observations sorted by start order do not prove completion order.
  A load starting at sequence 1 and completing at 3 must not authorize a read
  starting at 2. The new regression first failed (`pass` instead of expected
  `fail`), then passed after requiring available successful load terminal
  sequence strictly before the reference-read start. A read starting at 4
  remains valid. This lesson is retained in the regression, not elevated into
  new product authority or claimed as a live-runtime finding.

## Initial image-availability failure (superseded by explicit setup below)

Read-only inventory commands:

```sh
podman images --no-trunc --filter reference='*opencode*' \
  --format '{{.ID}} {{.Repository}}:{{.Tag}} {{.Digest}}'
podman images --no-trunc --filter reference='*eval*' \
  --format '{{.ID}} {{.Repository}}:{{.Tag}} {{.Digest}}'
podman image inspect ghcr.io/bateau84/opencode-eval-runner:opencode-edge
```

The filtered inventories were empty; the named-image inspection returned
`image not known`. Other named images were unrelated application/base images;
unidentified dangling images were **not attested** as compatible runner images.
This does not prove that every conceivable local image is incompatible.

A zero-inference harness probe was attempted against the immutable digest found
in the historical Loom wrapper, solely to test local availability:

```sh
bun run eval:live -- --probe --engine podman \
  --image ghcr.io/bateau84/opencode-eval-runner@sha256:68ef7322c75aede0e8cc76d0e3531e8b82dd417bbb5e5100264a89eab7fe8627 \
  --cases product-acceptance:PA3
```

Observed process result: **exit 2**, stdout empty, error:

```text
immutable image is not available locally; acquisition/build is explicit and never automatic
```

That digest is **not asserted to match the new runner pin**. Inspection failed
before image launch, config-server startup, inference, or provider contact. The
host `opencode --version` returned **1.19.0**, not 2.0.23, and was not substituted.

## Explicit OpenCode-only build and real proof

The coordinator supplied new explicit permission for a bounded build of the
needed OpenCode target and its prerequisites. Parent directories were verified
with `ls`; the runner was still clean at the pinned revision. The exact build:

```sh
podman build --jobs 1 --skip-unused-stages=true --platform linux/amd64 \
  --target opencode --tag localhost/skills-eval-opencode:1262ac8 \
  --file /home/bateau/git/bateau84/opencode-eval-runner/Containerfile \
  /home/bateau/git/bateau84/opencode-eval-runner
```

Observed: build succeeded, both version checks printed `opencode v2.0.23`.
The unrelated Copilot builder was skipped. Only the required pinned Node/Python
base images, OpenCode npm/native packages and Containerfile apt prerequisites
were acquired inside engine/build storage; nothing was installed into the host.
No image pruning, external repository writes or credential mounts were used.

| Identity | Observed value |
| --- | --- |
| Runner source | `1262ac8c2eebbd10af572e3e3560318f6113233b`, clean before/after |
| OpenCode version | `opencode v2.0.23` |
| Platform | `linux/amd64` |
| Runtime user | `1000:1000` |
| Immutable image ID | `sha256:819172b91c14b61dd289ec11647518713d5f24b3bc7eb60e87cfd6a937e47236` |
| Local manifest digest | `sha256:461031b5a3f8ba6aa14bfb031d86e037c28ea12b16469745e6f7419cdc781ef4` |
| Local tag (not used for eval execution) | `localhost/skills-eval-opencode:1262ac8` |

This local receipt does not establish a published registry digest or signed
build attestation. The harness still rejects tags, verifies local identity and
adapter bytes/version, and executes with `--pull=never`.

### Concrete real-runtime defects resolved

1. The first effective-policy check failed despite an exact system match:
   stock's `opencode.browser` appends `{action: "browser", resource: "*",
   effect: "deny"}` after generated rules. Source at the exact OpenCode pin
   confirmed the behavior. The checker now accepts only that exact known deny
   extension when the browser plugin is present; other extensions/allow rules
   still fail. A regression covers the observed shape and important near-misses.
2. After that correction, baseline catalog isolation failed: the real skill
   inventory contained **`opencode` and `report`** in an otherwise empty workspace.
   Retained failed manifest:
   `.skill-evals/probe-486b2a476c404225aff04caff5326e5a/run.json`.
   Source confirmed the built-in `opencode.skill` content plugin owns them, and
   the current config parser supports `-<plugin-id>` removal directives. Every
   treatment now removes only that plugin, leaving the native skill tool and
   directory discovery active. The new regression first failed on the missing
   directive, then passed after the project profile fix. No skill methodology
   or historical fixture was rewritten to accommodate the runtime.

### Final real provider-free commands

```sh
bun run eval:live -- --probe --engine podman \
  --image sha256:819172b91c14b61dd289ec11647518713d5f24b3bc7eb60e87cfd6a937e47236 \
  --cases product-acceptance:PA3
bun run eval:live -- --probe --engine podman \
  --image sha256:819172b91c14b61dd289ec11647518713d5f24b3bc7eb60e87cfd6a937e47236 \
  --cases work-decomposition:WD5
```

Both observed `image-and-effective-config-verified`, exit 0. These use the
**actual installed OpenCode server**, its current API catalogs/effective agents,
and the runner's real stock observer over its runner-owned loopback stream.
No fake OpenCode executable, fake model endpoint, hand-injected observer result,
or paid model was used in these real-image probes.

Retained private mode-0600 manifests, written through the runner's owned store
and reread before console success:

* PA3: `.skill-evals/probe-fc3a844d67334d35954043fd3504cd65/run.json`
* WD5: `.skill-evals/probe-a1496799cb1040aa859914214f88348e/run.json`

Each includes image/version/platform/adapter hashes, project implementation
hashes, actual/expected agent system and permission rules, skill/plugin catalogs,
visible workspace files, exact in-container practitioner/reference hashes,
kernel read-only mount status, and the actual empty runtime-evidence capture.
They contain no auth/provider secrets. They are gitignored operational artifacts,
not additions to the historical comparison or behavioral trial results.

Observed in **both** probes:

* baseline and judge skill IDs: **empty**;
* candidate: **only `product-acceptance` / only `work-decomposition`**, respectively;
* candidate files: `SKILL.md` plus `references/proof-and-example.md` /
  `references/boundaries-and-example.md`, respectively; exact hashes match the
  copied working-tree provenance after real file reads inside the container;
* all three workspaces: kernel read-only, exact permitted file sets, no symlinks,
  no eval/rubric/ASSESSMENT/QA/AGENTS resources, no inherited Loom config-root or
  external plugin inventory;
* actual effective systems and final permission rules match the generated
  target/judge configs plus the known stock browser deny;
* in-image collector → canonical `runtime_evidence/v1` → pinned host validation:
  **complete** native and Code Mode execution boundaries, closure available/true,
  0 starts, 0 terminals, 0 missing terminals, 0 observer/callback failures, no
  losses; Code Mode finality remains explicitly unsupported;
* networking `none`; no auth/catalogue/database/config-root seed mounts and no
  provider credential variables forwarded; activation prompt `resume: false`.

The empty captures prove instrumentation/schema interoperability and absence of
tool execution during this **activation/shutdown probe**, not a model's native
skill load or its answer behavior. Effective permission-rule evidence is not an
executed negative tool-operation test.

### Remaining boundaries declared before independent review

1. **Live target skill-tool loading, live answer/judge behavior and paired live
   artifacts remain unproved.** No model/spend selection is authorized for this
   work. The matching OpenCode image prerequisite and selected-package real
   config/observer proof are now satisfied; synthetic invocation adapters still
   test model-result gating/lifecycle without asserting live behavior.
2. **Copilot image/runtime interoperability was not built/probed.** It was not
   needed for the authorized OpenCode proof. Cross-transport judge mechanics are
   provider-free unit-tested, not certified against a real Copilot image here.
3. **Skill improvement, statistical significance, discovery and application E2E
   remain unclaimed.** No paid/live pair ran; discovery is a separate unimplemented
   experiment. Historical four-variant records remain unchanged and distinct.
4. **Lint/type-check and independent review success remain unclaimed.** All
   authored Python and embedded probes compile and all 44 provider-free tests
   pass, but this is not a Ruff/mypy or independent-review verdict.

The implementation has no placeholder model transport or pending design choice:
real execution/judging is delegated to the pinned runner's actual `invoke_once`.
The initial real-image gap is resolved. Remaining live proof requires explicit
authorization, not user design of an unfinished wrapper.

## Independent security review repair — reviewer `ses_ec8c2c3aeffec04tjgv7oSXHPe`

The earlier 44-test/config-probe success above remains historical evidence, not
a security approval. Independent review found two HIGH defects in the adapter:
late raw env substitution could manufacture runtime configuration, and an
arbitrary extra credential env name could be missed by the pinned inventory.
Both were reproduced and repaired without external source/image changes,
provider/model calls, staging, commits, pulls, builds or host installs.

### Before: independently reproduced inputs and observations

The config input was `providers.reviewonly.name = "{env:PROVIDER_LABEL}"` and
an explicitly forwarded quote-bearing `PROVIDER_LABEL` value. The exact public
fictional payload is retained in `scripts/tests/test_provider_security.py` as
`POISON`. It closes the provider-name string and inserts a duplicate top-level
`agents.eval-target` containing system `REVIEW-POISONED` and wildcard allow.

Before production edits, this command used the existing actual OpenCode image,
private server, `resume:false`, network:none and no credential seed mounts:

```sh
python3 -I -B scripts/tests/test_provider_security.py --native-raw \
  --image sha256:819172b91c14b61dd289ec11647518713d5f24b3bc7eb60e87cfd6a937e47236
```

Observed `policy_matches: false`, system **`REVIEW-POISONED`**, wildcard allow
followed by the stock browser deny, complete empty runtime evidence, provider
calls 0. Retained private trace:
`.skill-evals/provider-native-raw/run.json`. It includes source implementation
hashes, image/source/version identity and actual/expected agent data. The opt-in
`--native-raw` fixture deliberately supplies the historical raw-seed vector to
characterize upstream substitution; it is **not** the repaired adapter path or
a claim that the current live CLI accepts that input.

The credential input was `--env PROVIDER_AUTH` and
`headers.Authorization = "Bearer {env:PROVIDER_AUTH}"`, using only the public
fictional `SECRET` in that same test file. This pre-repair command exercised the
**actual pinned** `Sanitizer.from_runtime`, observer credential configuration,
canonical evidence builder, result pre-sink sanitation, paired lifecycle/store,
and artifact reread, substituting only invocation I/O:

```sh
python3 -I -B scripts/tests/test_provider_security.py --sanitizer-before \
  --output .skill-evals/provider-storage-before
```

Observed: `exit: 0`, `all_pass: true`; all four inventories complete but missing
the fictional credential, and the observer credential list also missing it.
The fictional value remained in canonical capture and paired artifacts/summary.
The private `run.json`, paired JSON and `security-check.json` are retained in
`.skill-evals/provider-storage-before/`. This is a sanitizer/storage reproduction
with injected I/O, **not an observed real provider leaking a credential**. The
command was executed against the pre-repair adapter; rerunning it now reaches
the new unsupported-representation guard rather than reproducing acceptance.

### Repair before startup, not verdict masking

* Added `compile_provider_settings`: validate provider-only JSON, resolve only
  permitted env references as parsed JSON string values, then revalidate and
  serialize with escaping. OpenCode receives literal values, not raw substitution
  tokens. Quote-bearing values remain one provider string and cannot create
  agents/permissions/plugins/instructions/body configuration.
* Every final generated config is checked for remaining native env/file markers,
  including keys and generated resource paths. File refs, variable keys,
  undeclared/missing references and env values containing further native markers
  fail closed. No required value is silently dropped or changed to empty.
* `--env` and native provider-env bindings must use names recognized by the
  **actual pinned runner** `sensitive_key` predicate. Unsupported `PROVIDER_AUTH`
  fails before image/model invocation; `PROVIDER_AUTH_TOKEN` is supported and
  its original value is passed to the existing runner inventory. The adapter
  does not implement a substitute sanitizer or relax role permissions.
* CLI validation runs after environment isolation/runner compatibility loading
  but before image/container startup. Profile construction enforces the same
  boundary for programmatic paired-driver callers. Header refs remain usable
  without hardcoding a user secret; see the supported env example in usage docs.

### After: actual observed checks

```sh
python3 -I -B scripts/tests/test_provider_security.py ProviderSecurityTests
python3 -I -B scripts/tests/test_provider_security.py --native-safe \
  --image sha256:819172b91c14b61dd289ec11647518713d5f24b3bc7eb60e87cfd6a937e47236
python3 -I -B scripts/tests/test_provider_security.py --sanitizer-safe \
  --output .skill-evals/provider-storage-safe
bun run eval:harness-test
bun run eval:validate
git diff --check
```

Observed native-safe: **policy matches true**, original practical-artifact system
unchanged, generated deny rules preserved, complete empty capture and zero
provider/model/tool actions. The same quote-bearing payload is compiled as a
literal provider name using the supported `PROVIDER_LABEL_TOKEN` env path.
Retained trace: `.skill-evals/provider-native-safe/run.json`.

Observed sanitizer-safe: **exit 0/all-pass remains true**, with all four actual
inventories complete **and containing** the fictional raw credential; the actual
observer credential configuration also contains it. The pinned pre-sink APIs
remove it from reflected text/stdout/stderr and canonical tool-result capture,
and it is absent from reread paired artifacts and summaries. No summary-only
masking or artificial negative verdict was used to obtain absence. Retained
private trace: `.skill-evals/provider-storage-safe/`.

The in-process capture inputs for this sanitizer test are synthetic invocation
boundary data; its actual inventory/evidence/sanitation/storage implementations
are external pinned APIs. It does not claim a model-driven native tool event or
live provider result. The real-image config test is separate and uses stock
OpenCode, not a substituted executable or test-only config parser.

The full provider-free suite now has **50 passing tests**, including all prior
44 plus these six named regressions in `test_provider_security.py`:

* `test_quote_payload_cannot_rewrite_generated_config`
* `test_noninventoried_forwarding_and_unsafe_or_missing_references_fail_before_startup`
* `test_actual_inventory_canonical_capture_result_and_paired_storage_hide_supported_env_credential`
* `test_unsupported_env_cli_stops_before_any_image_or_model_invocation_without_logging_secret`
* `test_every_generated_seed_rejects_residual_native_variables`
* `test_effective_config_rejects_non_provider_overrides_even_without_variables`

The ordinary real-image PA3 and WD5 probes were also rerun after this repair:
both returned `image-and-effective-config-verified` with complete empty evidence,
unchanged isolated skill catalogs and read-only exact practitioner files. Their
new private manifests are:

* `.skill-evals/probe-d0c50a83e3fa427f9d3719345812af92/run.json`
* `.skill-evals/probe-f2b6d223496e4f14ab3f673fabbd2cd2/run.json`

Fixture validation remains **235 cases / 50 skills**, the preservation checksum
passes, and whitespace checks pass. Source pin remains
`1262ac8c2eebbd10af572e3e3560318f6113233b`; existing image remains OpenCode 2.0.23,
linux/amd64, immutable ID `sha256:819172b91c14b61dd289ec11647518713d5f24b3bc7eb60e87cfd6a937e47236`.
No live model/provider leakage or successful live paired trial is claimed.
Independent rereview has not yet occurred; the previous FAIL is not overwritten
by this producer repair evidence.
