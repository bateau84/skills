# Optional runnable skill evaluations

The skill directories still load without Bun, Python, OCI images, Loom, or an
evaluation runtime. Root tooling is an optional maintainer workflow:

```sh
bun run eval:list
bun run eval:list -- --skills product-acceptance
bun run eval:validate
bun run eval:harness-test
```

No npm dependencies or installation step are needed. Bun only supplies script
aliases; Python 3.11+ and its standard library implement the project profile. The
equivalent direct commands are `python3 -I -B scripts/run_evals.py --list`,
`--validate`, and `--harness-test`. Non-isolated Python launches are rejected.
Listing and fixture validation do not require the external runner or models.
Harness integration tests require the pinned runner but substitute only its
invocation I/O; **they never call a provider or prove real native skill loading**.

## Dependency and image identity

The execution dependency is the **clean checkout**, not an arbitrary executable
found on PATH:

- Runner: [`bateau84/opencode-eval-runner`](https://github.com/bateau84/opencode-eval-runner)
  at `1262ac8c2eebbd10af572e3e3560318f6113233b`.
- Resolution: `--runner-root /path/to/opencode-eval-runner`, then
  `SKILLS_EVAL_RUNNER_ROOT`, then the local sibling `../opencode-eval-runner`
  relative to this repository (not the current shell directory).
- The checkout must have no modified, untracked, or ignored files, including
  bytecode. Imports do not write bytecode there. Use a dedicated clean checkout
  rather than a dependency tree carrying unrelated experiments or cache files.
- Its pinned Containerfile specifies OpenCode **2.0.23** and Copilot **1.0.83** in
  separate transport images. Changing only the Python host code is insufficient.

There is **no established current published immutable digest in this project**.
The runner's floating `*-edge` defaults and historical Loom digests are not used
as substitutes. Every live/probe invocation requires an explicit full local
image ID (`sha256:` plus 64 hex digits), or `repository@sha256:<64 hex digits>`.
Tags—even tags containing a source SHA—are rejected. Local inspection must find
the image. A zero-inference, no-network probe verifies its container adapter
file hashes against the pinned host checkout and checks the CLI version before
spend. Execution uses the resolved image ID. All runner OCI commands add
`--pull=never`; nothing is automatically installed, cloned, pulled, or built.
This is byte/version compatibility in a trusted-checkout regime, not signed
build attestation or resistance to hostile custom images.

If you **explicitly choose to acquire/build dependencies**, do so separately.
For a new dedicated checkout, clone the repository and check out the exact
revision above, then inspect its status. From that checkout, the runner's
documented explicit build procedure is, for example:

```sh
# Explicit acquisition/build operations; NOT performed by this harness.
podman build -f /path/to/opencode-eval-runner/Containerfile \
  --target opencode -t skills-eval-opencode:1262ac8 \
  /path/to/opencode-eval-runner
podman image inspect skills-eval-opencode:1262ac8 --format '{{.Id}}'

# Only if a Copilot judge is intentionally needed:
podman build -f /path/to/opencode-eval-runner/Containerfile \
  --target copilot -t skills-eval-copilot:1262ac8 \
  /path/to/opencode-eval-runner
podman image inspect skills-eval-copilot:1262ac8 --format '{{.Id}}'
```

Keep the full printed IDs. A host OpenCode installation of a different version
is not a substitute. These commands can acquire base images and CLI binaries;
they require your explicit operational authorization and network access.

## Provider-free runtime probe

After a matching image is already present, select a case and run:

```sh
bun run eval:live -- --probe --engine podman \
  --image "$OPENCODE_IMAGE_ID" --cases product-acceptance:PA3
```

The probe checks adapter/version compatibility, then starts isolated stock
OpenCode servers through the runner's preflight helpers. Its activation prompt
uses `resume: false`, so no model inference runs. Networking is `none`, and no
credentials are forwarded. It checks the effective agent system/permission
suffix, baseline/judge skill absence, the candidate's selected skill catalog,
readable/read-only practitioner files, excluded eval directories, and absence
of external/Loom plugins/config-root inheritance. It does **not** assert that a
model called the native skill tool. An unavailable or incompatible image exits
2, not PASS. See [observed verification and gaps](eval-verification.md).

The probe additionally reads and hashes every copied file inside the container,
checks the exact visible file set and absence of symlinks, and verifies the
kernel's read-only workspace mount flag. It enables the runner's actual stock
observer for the non-resuming activation/shutdown cycle; the resulting empty
capture is built in-image and validated by the pinned host runtime-evidence
schema/readiness APIs. This is schema/observer interoperability for that cycle,
not native model-tool execution or behavioral acceptance. Probe runs retain
private mode-0600 `run.json` manifests under `.skill-evals/probe-<id>` (or the
explicit `--artifact-dir`), including observed effective policy, catalogs,
container file hashes and evidence. Failed checks retain their observations and
failure status. Console results derive from a reread of that manifest.
Once the probe directory is owned and its manifest exists, launch announces
`Probe artifacts: <absolute-directory>` on stderr, before probe callbacks run.
Its final JSON still includes the manifest path; probes do not replace the latest
paired-evaluation report at the repository root.
No auth, model-catalogue, credential-database or config-root seeds are mounted,
and no provider credential variables are forwarded. Copilot runtime proof is
separate; `--probe` currently accepts only the OpenCode judge configuration.

## Live selection and spend controls

Live calls are never made by list/validate/test/probe. A live run requires both
explicit selection and an explicitly chosen model. A small first trial is:

```sh
# Paid/live example: only run after explicitly choosing model and spend.
bun run eval:live -- \
  --cases product-acceptance:PA3 --model "$CHOSEN_MODEL" \
  --engine podman --image "$OPENCODE_IMAGE_ID" \
  --artifact-dir /path/to/new-single-run-directory
```

`--cases` accepts the printed canonical ID (`SKILL-product-acceptance-PA3`) or
qualified source ID (`product-acceptance:PA3`). Numeric IDs are qualified, e.g.
`python-testing:1`; bare `1` is not a global alias. `--target` and `--skills` are
aliases selecting comma-separated skill names. With `--cases`, they restrict
the selectable cases to those targets. Unknown and empty selectors fail before
execution. `--all` is an explicit whole-suite choice (or all cases of selected
targets); **do not blindly run the entire case corpus**. Merely passing
`--target-kind skill` does not authorize selecting everything.

| Control                                   | Default / semantics                                                                                                                                                                                        |
| ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--iterations N`                          | 1 repetition per selected case; positive integer                                                                                                                                                           |
| `--parallel N`                            | 1 concurrent pair; positive bounded number, not “unlimited”                                                                                                                                                |
| `--model`                                 | Required; native OpenCode target only                                                                                                                                                                      |
| `--judge-model`                           | Target model by default for OpenCode; explicit when using a cross-transport judge                                                                                                                          |
| `--judge-transport`                       | `opencode`, or `github-copilot-cli` with explicit model and `--copilot-image`                                                                                                                              |
| `--reasoning LEVEL`                       | Common target/judge reasoning; omitted means provider default                                                                                                                                              |
| `--target-reasoning`, `--judge-reasoning` | Phase overrides; target control is identical in baseline and candidate                                                                                                                                     |
| `--engine`                                | `auto` (Podman then Docker), or explicit `podman`/`docker`                                                                                                                                                 |
| `--network MODE`                          | Engine default, **live**, not an offline evaluation; `host` prints an isolation warning                                                                                                                    |
| `--image`, `--opencode-image`             | Aliases for the immutable OpenCode identity; no implicit image                                                                                                                                             |
| `--copilot-image`                         | Immutable Copilot judge identity if needed                                                                                                                                                                 |
| `--timeout-seconds`, `--inner-timeout`    | 240 seconds per actual target/judge invocation                                                                                                                                                             |
| `--container-timeout`, `--outer-timeout`  | 300 seconds; at least 300 and inner +60                                                                                                                                                                    |
| `--transport-retries N`                   | 0, range 0–5; only the runner's replay-safe transient routing policy                                                                                                                                       |
| `--artifact-dir`, `--output`              | Aliases for a fresh single-run directory; default `.skill-evals/<generated-run-id>`; explicit relative paths are anchored to the repository root, not the shell cwd; absolute external paths are preserved |

At **one case, one repetition, no retries**, nominal and maximum spend are
**2 target calls + 2 judge calls**. With `C` cases, `I` repetitions and `R` retries,
nominal counts are `2*C*I` for each phase and maximum counts are
`2*C*I*(R+1)` for each. The harness prints these counts before execution. A
failed/unusable target can suppress its judge, so actual counts can be lower.
No correction/feedback rounds or model-backed delegation are added. Counts are
not a monetary/token estimate; sampling, token caps, provider cache behavior and
actual prices are not independently controlled here.
These are **runner invocation/attempt counts**, not an upper bound on underlying
provider HTTP requests: one native target invocation can have several model/tool
steps while loading guidance, reading references and producing its answer.

Retries are not generic transport replay. The external runner requires the
exact `provider.no-route`/`Model unavailable` host-failure signature **and**
authoritative proof that no invocation was observed. Timeouts, tools already
observed, malformed evidence, parse failures, and unavailable fields are not
silently retried. Each attempt/failure/retry decision remains in the artifacts.

## Terminal output and machine compatibility

Live runs default to concise human-readable output: planned invocation bounds,
run/model information, case/iteration + baseline/candidate target/judge attempt
progress, then verified side statuses and available behavior scores. Results
appear as each pair completes, including with `--parallel N`; each result block
is kept together. An `attempt ...` line means entry into the runner invocation
boundary, **not** a completed model call, observed provider HTTP request, or PASS.
Each entry is followed by an accurately timed **attempt return** update, before
the next phase starts: `returned`, `returned (reported error)`, `returned
(unrecognized response)`, or `raised (host error)`, with case/iteration, side,
phase and attempt number. The elapsed time measures the actual invocation-adapter
call. These updates explicitly say **verification pending**: an adapter returning
success does not establish evidence readiness, a valid judgment, or PASS. Error
updates expose only generic state from protocol scalars, never exception text or
raw response/log payloads. Retry attempts each receive their own entry/return
updates. Human progress updates are suppressed entirely in `--json` mode.
Verdicts/rationale are printed only after durable paired-artifact reread and
integrity validation. The final summary separately rereads all successful jobs.

Output choices (append to the same explicitly authorized live command):

| Choice       | Behavior                                                                                                                                                                               |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Neither flag | Human progress/results; no full pair/summary JSON dump                                                                                                                                 |
| `--verbose`  | Same human results plus bounded per-attempt duration, host exit, failure code, and retry/replay-safety diagnostics                                                                     |
| `--json`     | JSONL `live-spend-plan`, `run-started`, `verified-pair`, `verified-summary` events; final event adds `report_path` and `latest_report_path`; human live/isolation notices go to stderr |
| Both flags   | Rejected by argument parsing (exit 2), before execution                                                                                                                                |

`--json` preserves existing machine event IDs/fields, including the detailed
`pairs` array in the final summary, with the intentional diagnostic privacy
substitutions below, the additive location fields and `run-started` event described below.
Pair results and durable JSON evidence (including the saved PA3 runs) are not
regraded or rewritten. Pair events arrive in **completion order**; the
summary's pairs remain in plan order. Consumers must associate events using
`case` and `iteration`, not their line position. Scripts parsing the former
default live JSON output must now opt in with `--json`. These two formatting
flags affect **live reporting only**: `--list` stays TSV, `--validate` stays its
provider-free JSON object, `--harness-test` stays stdlib test output, and `--probe`
stays its existing verified JSON report. No broad script/pipeline compatibility
is promised across those different modes.

Human results preserve the distinction between **FAIL** (behavioral negative)
and **NON-EVIDENCE** (unusable or missing proof); an unavailable score is not
printed as zero. Failed judgments show criterion counts and up to three bounded
criterion rationales per side. A zero score on one conjunctive criterion does
not mean every part of the answer was wrong. For example, this excerpt was
generated by **replaying an existing, verified PA3 artifact**, not a new model
run or a regrade:

```text
SKILL-product-acceptance-PA3#1 baseline PASS 100% -> candidate FAIL 0%
  Paired observation: observed regression (-100.0 pp); policy, not statistical significance.
  candidate: 1/1 positive criteria unmet.
  candidate E1: The response correctly identifies the missing discovery provenance and preserves B’s narrower claim, but says A did not run the real router/adapter or observe the action and therefore discards A’s routing/action evidence. The scenario says those stages were run after the inserted row.
  Zero is a criterion-level score (criteria can be compound), not a claim every statement was wrong.
```

Improvement/regression labels describe the observed pair using the unchanged
10pp/trap policy, **not statistical significance or general superiority**.
Failed treatment integrity yields an unattributed comparison, even when answer
scores exist. For non-evidence, reporting selects a bounded actual runtime error
message from the **verified, runner-redacted final result fields** (structured
error events first, otherwise only the first stderr diagnostic line). The saved
malformed-model PA3 artifact, for example, replays as NON-EVIDENCE with
`Invalid model reference: gpt-6-luna`, not as a behavioral FAIL. Raw stdout,
assistant text, prompts, tool payloads, observer traces and arbitrary host
exception messages are not dumped. If no safe result detail is available, only
the failure code is shown. Diagnostic text is flattened, length-bounded and
stripped of terminal/control/bidi sequences, including in verbose mode.

**Integrity-verified does not mean redacted.** The pinned engine constructs some
check, judge-contract and comparison-callback diagnostics on the host, after
container result sanitization. Reporting never treats those exception strings as
safe rationale. In default **and verbose** output, only known literal project
check rationale is copied; dynamic tool identities, arbitrary callback reason or
metadata payloads, and callback exception messages are withheld. Safe check and
contract codes remain visible. Runtime error and legitimate judged-criterion
rationale still come from the verified, runner-redacted result path.

The same privacy policy applies to **JSON events**, including checks nested in
the summary: unsafe check `reason` and comparison failure `message` strings are
replaced by canonical withholding text; arbitrary check metadata is omitted
(the metadata object remains), and unrecognized check names/codes use a generic
identifier. Classification, status, score/delta, attempt counts and field types
are not changed. IDs still reference the **original durable artifact**, not a
hash of the privacy-projected console event. Callback failures are not regraded.
This intentionally changes unsafe diagnostic content relative to the former
machine output; consumers must not require raw host exception payloads.

Configuration/malformed-input exceptions and failed probe callbacks likewise
cannot forward arbitrary exception text to the CLI. Canonical configuration
guidance is retained where known; supplied values and unknown host diagnostics
are withheld. A failed probe prints its retained manifest path separately. Its
status/observations and raw failure remain in the unchanged private manifest.
Upstream private artifacts can still contain **unredacted host diagnostics**;
this presentation repair does not sanitize or rewrite those artifacts. Do not
publish them or assume their integrity IDs certify credential privacy.

Completion reports observed target/judge **attempt counts from verified
artifacts**, distinct from the planned nominal/maximum budget. If orchestration
fails, those counts are explicitly partial: failed jobs may have additional
unrecorded attempts. Provider request counts, tokens and monetary cost remain
unobserved; the output does not invent them. Completion points to the durable
`run.json`, the per-run Markdown report, and ends with the latest root report path.
Full paired JSON artifacts, judgments, checks, attempts, timing, provenance and
integrity IDs remain unchanged in the private run directory in
**every** output mode. Console brevity does not weaken evidence or loading gates.

### Automatic Markdown results

Every future live evaluation run automatically publishes **`results.md`** beside
`run.json`, inside its fresh `.skill-evals/<run-id>` or explicit `--artifact-dir`.
It also publishes the full latest report at **`EVAL-RESULTS.md` beside the root
`README.md`**, regardless of the shell's current directory. The default history
directory `.skill-evals/` is hidden, but its absolute run directory is explicitly
announced at startup and completion. The root file appears only after a future
report-producing evaluation invocation, not by retroactively regrading history.
Explicit relative `--artifact-dir`/`--output` paths are also repository-rooted:
`--output reports/run` means `<repository>/reports/run`, even when launched from
another directory. Absolute artifact paths outside the repository remain valid
and retain appropriately rebased evidence links.
No new flag, model call, regrade, summary model or extra inference spend is added.
Existing historical run directories are **not** retroactively modified. Root Bun
aliases are unchanged. List/validate/harness-test/probe retain their existing
mode-specific output; the new report is for paired evaluation runs.

The report includes observed run creation time, model/reasoning and execution
settings, selection/repetition coverage, candidate absolute results **separate**
from relative paired observations, plan-ordered case/iteration statuses and
available scores, decisive bounded failed-criterion rationale or safe runtime
reasons, observed target/judge attempts versus the planned budget, and relative
links to actual paired JSON and the run manifest. The root view uses links relative
to the repository root, including `../...` links when `--artifact-dir` is outside
the repository; the per-run view uses links relative to its own directory. Link
targets are checked against actual run-owned files, not manufactured by replacing
prefixes in arbitrary Markdown text. Source identifiers/hashes and
paired artifact integrity IDs support provenance without duplicating prompts,
responses, provider configuration or full JSON. Only recorded timestamps/durations
are shown; finish times and provider requests/tokens/prices are not invented.

Publication independently rereads the manifest and paired artifacts through the
pinned runner's ownership/integrity APIs and checks the summary against those
artifacts. It uses the same origin-aware diagnostic privacy projection as the
terminal, plus the runner's credential inventory for metadata, before bounding
and escaping Markdown/control characters. Raw host callback exceptions never
become report rationale. A criterion-level zero can represent a compound rule;
NON-EVIDENCE is not a behavioral FAIL or an invented zero.

Completed negatives, non-evidence and partial orchestration-error runs receive
reports too. Missing jobs are visibly unavailable, not empty PASS rows. If an
owned run fails before finalization, a report may recover verified saved pairs
but explicitly says **INCOMPLETE**, with partial attempt accounting and no
complete run claim. Malformed arguments/preflight before ownership create no
fake execution report. Unverifiable/tampered artifacts or unsafe/unwritable storage
fail closed (exit 2): there is no substitute false summary/report when safe
publication cannot be established.

Both Markdown views are private **0600**, with file/directory fsync on the
supported Linux filesystem. The per-run `results.md` is atomically created only
when absent; existing run history is never overwritten. The root `EVAL-RESULTS.md`
is atomically **replaced** only if absent or identifiable as an unmodified
generated report. A versioned checksum header identifies generated bytes; it is
not a signature or stronger evidence authority. Manual content, edited generated
content, symlinks, non-regular files and hardlinks are refused with a safe, precise
diagnostic. Move your manual file explicitly before retrying; the harness does
not silently adopt or overwrite it. The destination is checked before inference
and again during publication. A late root conflict or failure before replacement
retains the immutable per-run report and JSON, leaves prior root content intact,
and exits 2. A durability error after atomic replacement can leave the complete
new root file visible, but still exits 2 and does not claim successful publication.

A stable private `.EVAL-RESULTS.lock` serializes publication across whole commands,
not inference or individual pairs. **Latest means the most recently report-published
run**, including behavioral negatives, non-evidence and partial orchestration
failures—not the run started most recently, an all-PASS verdict, or a chronological
claim based on inferred timestamps. Updating the root view never deletes previous
per-run reports. Root report/lock/temporary files and `.skill-evals/` are gitignored
operational output; no automatic staging or commit is performed. Live artifact-directory
paths traversing symlinks are rejected. Metadata and even redacted rationale can
still be private. **Linked upstream raw JSON can contain unredacted host
diagnostics**; do not publish it or treat integrity IDs as privacy certification.

Default and `--verbose` startup print `Run artifacts: <absolute-directory>` and
`Latest report after completion: <absolute-root-report>`, only after the run has
valid ownership and an existing manifest, before the first long invocation.
Completion prints the run directory once in the summary, its manifest and one
`Report: <per-run-path>` line, then ends with one `Latest report: <root-path>` line.

`--json` emits no human path lines on stdout. The additive **`run-started`** event
contains `run_id`, an absolute `artifact_dir`, and `latest_report_path` (the planned
destination, not a published result at startup). Its existing `verified-summary`
event gains additive string **`report_path`** and **`latest_report_path`**, while its
previous IDs, result fields, detailed `pairs` and durable `run.json` summary remain
unchanged. Consumers must tolerate these added fields/events. On an exceptional
orchestration exit _before_ a final summary,
successful recovery publication instead emits a JSONL
`{"event":"results-report","artifact_dir":"<directory>","report_path":"<per-run-path>","latest_report_path":"<root-path>"}` event; this is a report
location, **not** a `verified-summary` or a success verdict. Existing preceding
pair events keep their original evidence IDs and completion-order semantics.
If the per-run report was retained but root publication failed, the
success path must not claim that the root view was updated. Publication errors
have a separate safe **operation code**, such as `per_run_report_collision`,
`per_run_report_write_failed`, `per_run_report_durability_failed`,
`latest_report_write_failed` or `latest_report_durability_failed`; arbitrary caught
host exception text is never forwarded. The wrapper still exits **2**, without
overwriting collisions or falsely advertising a published report.

A failed report must not hide valid evaluation results. Before presenting an
aggregate after a publication error, the driver independently rereads ownership,
paired identities/hashes and the manifest/summary again. If these checks pass,
human output includes the verified aggregate, artifact directory and `run.json`
location, then separate per-run/latest publication statuses and the safe failure
explanation. JSON emits `verified-summary` with unchanged result fields/IDs plus:

- `report_publication`: `per_run` and `latest` statuses (`published`, `failed`, or
  `not-written`) and a safe `failure` object containing `code` and `message`;
- `evaluation_finalized`: whether the durable evaluation summary was finalized;
- `evaluation_exit_code`: the unchanged evaluation exit (0/1/2) when finalized,
  otherwise `null` for a still-running/incomplete owned run.

`report_path` is included only for a confirmed per-run publication;
`latest_report_path` is omitted when latest publication failed or was not
attempted, even if a complete file became visible before a durability error.
A complete PASS evaluation can therefore have `all_pass: true` and
`evaluation_exit_code: 0` while the process exits 2 for report delivery failure.
Partial or non-evidence aggregates are not promoted into complete proof. If
ownership, artifacts or the summary were tampered with, no verified aggregate is
emitted; the integrity failure remains exit 2 with no complete run claim.

Consumers should tolerate additive events/fields rather than assume
every JSONL line is a pair result. CLI errors before ownership produce no
`run-started` event or fake report and leave an existing latest report unchanged.

### Bounded Loom interface overlap

The historical Loom wrapper at the recorded revision printed phase progress,
PASS/FAIL/error results, ablation scores/deltas, failure rationale and a final
pass count. The current sibling Loom checkout no longer contains that wrapper;
the historical source/package/README, not an assumed current implementation,
were the reference for this presentation change.

Existing conveniences remain: comma-separated `--cases`/`--target`, qualified
case IDs, `--skills`, target/judge model and reasoning controls, bounded
iterations/concurrency, and image/timeout/artifact-path aliases. Safety deviations
are intentional: `--parallel` requires a positive number (no unlimited shorthand),
`--target-kind skill` alone is not selection/spend authorization, retries default
to zero and require authoritative replay safety, and images must be explicit
immutable local identities. The harness does not port arbitrary Loom `--suite`,
agent/runtime evaluations, Copilot targets, `--runtime-parallel`, `--keep-temp`,
automatic dependency/image acquisition, or `eval:system`/`eval:stress` aliases.
The existing root Bun aliases are unchanged. Model syntax/preflight behavior,
fixture meaning, grading and historical evidence are not changed by reporting.

## Treatment and config boundaries

Each pair runs sequentially: baseline target → its judge → candidate target →
its judge. Different pairs may run concurrently. All four invocation workspaces
are disposable and distinct; the real checkout is never mounted writable or
used as the invocation workspace.

- Baseline: no skill files, no skill/reference tool allowance.
- Candidate: just the selected skill directory's practitioner bytes. `evals/`,
  ASSESSMENT, QA, evaluator resources, hidden config, AGENTS instructions and
  agent directories are excluded. All symlinks are rejected, including internal
  ones. The native `skill` tool is allowed only for the selected ID; `read` only
  for exact copied files. Reads must follow the successful native load.
- Judges: empty workspaces, all tools denied. Each sees only its own response,
  scenario/common instruction, and rubric, never the other treatment's answer,
  loading trace or practitioner guidance. The response might still reveal style
  clues; this is not a claim of perfect experimental blinding.

The temporary `eval-target`/`eval-judge` agents are generated evaluation inputs,
not required library agents. Instructions and policy use the **current V2**
`agents.<id>.system` and ordered `permissions` array of
`{action, resource, effect}` rules with last-match precedence—not legacy Loom
frontmatter/tool declarations. The OpenCode transport ignores system-file
content, so it is not used to inject OpenCode instructions. Copilot uses the
runner's tool-disabled transport and an explicit judge system message.

Stock OpenCode 2.0.23 registers built-in `opencode` and `report` skills even in an
empty workspace. The generated config therefore uses the native plugin-remove
directive `plugins: ["-opencode.skill"]` in every treatment. This disables only
that built-in content plugin; `opencode.tool.skill` and `opencode.config.skill`
remain active for the candidate's native loading and directory discovery.
Provider-config files still cannot supply plugin directives. Stock's separate
browser plugin appends an exact `browser/*/deny` rule after config; the real
probe recognizes only that source-backed restriction, never arbitrary trailing
permission changes or allow rules.

Before runner imports or parallel work, the driver sanitizes the host environment.
Inherited runner config/config-root/image and OpenCode/Python runtime controls
cannot import Loom or override these policies. Known credential variables are
forwarded intentionally; extra provider variables require `--env NAME` and
cannot be runtime-control names. Extra names must also be recognized by the
**pinned runner's actual credential-inventory predicate** (for example
`PROVIDER_AUTH_TOKEN` or `CUSTOM_API_KEY`), and explicitly forwarded values must
be present/nonempty. An unsupported name such as `PROVIDER_AUTH` fails before
any container startup rather than being forwarded without credential coverage.
Values are not logged.

OpenCode's normal auth/database/model catalog seeds may be discovered by the
runner, or chosen using `--auth`, `--database`, `--models-catalog` and the
corresponding `OPENCODE_EVAL_RUNNER_AUTH`, `_DB`, `_MODELS` variables. Database
sanitization, credential scanning, observer capture and result redaction remain
owned by the external runner. A **provider-only V2** file may be passed with
`--provider-config`: top-level `providers`, recognized provider/model settings
and headers, no runtime configuration, arbitrary package loading, or request
`body` overlays. Legacy `provider` configs are rejected rather than silently
migrated. No host plugin/MCP/agent/instruction tree or config-root is inherited.

Provider config `{env:NAME}` references are supported only in string **values**,
using the three default OpenCode API-key variables or explicitly forwarded,
runner-inventoried credential names. The adapter resolves them in the parsed
JSON tree and serializes with JSON escaping; it does not leave raw-text
substitutions for OpenCode to perform. It revalidates the provider-only shape
and rejects native env/file markers in every final generated seed. Variable
keys, `{file:...}` references, undeclared/missing env references, and substitution
values containing further `{env:...}`/`{file:...}` markers are rejected before
startup. This prevents quote-bearing env values from manufacturing agent,
permission, plugin, instruction or request-body configuration.

For example, a custom header can keep its credential outside the config file:

```json
{
  "providers": {
    "private-provider": {
      "canonical": "openai",
      "headers": { "Authorization": "Bearer {env:PROVIDER_AUTH_TOKEN}" }
    }
  }
}
```

Set `PROVIDER_AUTH_TOKEN` through your normal secret/environment mechanism and
pass `--env PROVIDER_AUTH_TOKEN --provider-config /path/to/provider.json` with
the explicitly selected live run. The original credential value is inventoried
by the real runner from the forwarded env, including when the resolved header
adds a `Bearer ` prefix. No hardcoded user credential or replacement sanitizer
is required. Existing auth/database/catalogue seed handling remains runner-owned.

## Evidence, scoring and exit status

The project requires canonical `runtime_evidence` with complete native and Code
Mode execution boundaries. Every exact tool/actor/input field needed for the
treatment assertion must be available; a successful native load additionally
requires available result evidence. Complete absence of the selected native
load is a behavioral treatment failure; incomplete/unsupported/redacted/omitted
required facts are **non-evidence**. `skills_loaded`, text, tool convenience
arrays, or collector-shaped prose never backfill an authoritative gap. An
OpenCode judge additionally requires complete no-tool evidence. Copilot's
unsupported native boundary is permissible only for its text-only judge role.
Unsupported Code Mode _finality_ does not invalidate unrelated native evidence.

Targets must produce nonempty text. Judges return strict `judgment/v1` JSON with
one result for every exact positive (`E1…`) and forbidden (`N1…`) rule ID, strict
Booleans, cited evidence, trap assessment, and a consistent overall `passed`.
Missing, duplicate, conflicting, unknown or malformed results are non-evidence,
not a successful grade or an invented zero score.

Behavior score is the fraction of satisfied positive rules, avoided forbidden
rules, and—when declared—avoided trap. Candidate absolute PASS requires every
rule plus treatment integrity. Relative skill value is separate:

- regression if a trap regresses or score delta is negative;
- material improvement if a trap is fixed or the delta is at least **10pp**;
- smaller positive delta: improvement; zero: neutral.

The threshold uses exact Boolean fractions, not floating-point rounding. It is
a **policy**, not statistical significance. Treatment integrity failure prevents
attributed improvement even if answer scores are available; a higher score is
not candidate absolute PASS.

| Exit | Meaning                                                                      |
| ---- | ---------------------------------------------------------------------------- |
| 0    | Every selected pair has complete usable evidence and every candidate passes  |
| 1    | Completed behavioral negative or non-evidence                                |
| 2    | Configuration/orchestration/storage/integrity failure; no complete run proof |

The runner owns run-directory claims, paired artifacts, integrity IDs, atomic
storage, and reread/verification. `run.json` summaries and console verdicts are
derived from **reread, verified paired artifacts**, not just in-memory grades.
Versioned project metadata records working-tree fixture/rubric/practitioner
hashes, effective config hashes, controls, runner revision, immutable image proof,
and implementation hashes. Root SKILL/reference provenance is exact working-tree
bytes, **not HEAD alone**. Default result directories are gitignored; treat the
runner's artifacts as sensitive operational evidence, not public credentials or
a skill-loading prerequisite.

## Corpus, history and source lineage

The original 48 JSON fixture files produced 219 normalized cases. Later
consolidation merged several skills' fixtures (moving their cases unchanged)
and removed `report-lifecycle`'s single case, leaving 218. Three Loom-style
source shapes are accepted: arrays, `{skill, cases}`,
and `{skill_name, evals}`. Normalized IDs are `SKILL-<skill>-<source-id>`; source
IDs and expectation text are preserved.

The reviewed PA1–PA9 and WD1–WD7 Markdown packets now have runnable JSON copies.
Their prompts, common instruction, observations and IDs match exactly; each
original evaluator-observation paragraph remains one conjunctive positive rule,
not an invented breakdown into new criteria. JSON does not claim the scenario's
application ran. Discovery is **not implemented**: explicit loading measures
performance after loading, not retrieval quality.

The historical [four-variant protocol and limited pilot](../evaluations/selective-enrichment/README.md)
remain separate and unchanged. Its 0/1/2 dimensions and 0–8 pilot results are
**not converted into Boolean results or attached to new runs**. No current
superiority, discovery success, or application E2E claim follows from the pilot
or from these provider-free harness tests.

Normalization, Boolean scoring and 10pp/trap comparison methodology were informed
by Loom `scripts/run-evals.py` at
`c16e2c793b8faa8d21cf2ca9833606676e461e79`. No Loom agent/plugin/OCI/observer/storage
runtime was copied. The external runner's `eval_plan`, `eval_paired`,
`eval_artifacts`, `eval_execute`, and EvalProfile v1 hooks implement the actual
execution/judging lifecycle. This source lineage/pin is **not a blanket MIT
license grant**; existing skill/source attribution and licenses remain intact.
