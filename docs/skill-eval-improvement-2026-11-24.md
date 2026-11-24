# Skills and evaluation improvements — 2026-11-24

## Decision and evidence boundary

Improve the product a skill helps an agent produce: correct behavior, appropriate
scope, preserved contracts, useful evidence, and no invented commitments. Skill
conformance remains useful diagnostic information, but it is not interchangeable
with product quality. Fix a misleading rubric before optimizing against it;
correct independently identifiable skill defects in parallel.

The input is the user-supplied Claude experiment report, uploaded as
`Pasted text(9).txt`, SHA-256
`c936a87b0f8e25a7fe75c64609a307d6ef22fa624316c8d5c909a71e445a6431`.
It contains an aggregate table, excerpts from judgments, and a proposed handoff.
The original 1,070 answers, 535 judgment files, blind arm mapping, and verified
target/judge identities were **not supplied**. Its reported outcomes have not
been independently replayed or rejudged here.

The repository baseline for this work is
`056c9b27da4f03ea7a3495359c4e674a9063f0f3`. Reading the JSON fixtures at that
commit, including all supported filenames/shapes, establishes **522 cases across
107 of 124 skill directories**, in 111 JSON files. The experiment selected only
one case per covered skill; it did not exercise all 522 cases.

## What the supplied table establishes

The 107 table rows independently sum to the reported totals:

| Reported measure | Baseline | Skill |
| --- | --- | --- |
| Passes across five repeats per selected case | 281/535 (52.5%) | 495/535 (92.5%) |
| Trap incidents | 97 | 5 |
| Pairwise preferences | 75 | 397 |
| Ties | 63 shared ties | 63 shared ties |

Also consistent with the table: 42 baseline 5/5 cases, 48 cases with no pass-count
increase, four cases with lower skill pass counts, 78 traps that never triggered
in the baseline repeats, and 27 cases going from 0/5 to 5/5. This verifies the
report's arithmetic, not the truth or validity of every judgment. Five repeats of
one task are not five independent task scenarios.

The reported 40 percentage-point pass difference mixes outcome and convention
criteria. It does not establish the same improvement in user-facing quality.
The report describes same-model judging with an inherited, unverified model
identity, instruction-based isolation, and residual skill-catalog context. Its
pairwise preferences are therefore useful leads, not an independent quality
certification.

Two corrections matter when acting on the narrative:

- The `python-common-practice` skill-arm excerpts describe an omitted explicit
  inspect/fix/re-run loop. The mutating-format-default evidence appears in the
  **baseline** arm. The handoff partly combines these into one skill finding.
- A run with missing repository files cannot prove execution behavior. The
  report's zero-infrastructure-error count does not make those fixture-deficient
  cases valid execution evidence. An invalid setup and a completed transport are
  separate facts.

## Evaluation direction

### Keep regression coverage; measure discrimination separately

A baseline 5/5 result gives no binary pass lift on that sample. It can still be a
useful regression check, and it does not rule out improvements in correctness
detail, scope, clarity, or cost. Likewise, a rare but consequential failure does
not become an invalid trap because fewer than three of five baseline runs hit it.

Keep existing useful cases. Inspect the other existing cases before authoring a
harder complement. Do not replace every ceiling case or invent traps merely to
make the baseline fail. The eight ceiling skills with frequent baseline
preference are investigation priorities, not eight established skill defects:
`golang-tui`, `python-fastapi`, `python-pydantic`, `terraform-provider-docs`,
`golang-code-style`, `golang-spf13-viper`, `opentelemetry`, and `python-async`.

An authored `contrast` purpose expresses intent. It does **not** mean the case
has empirically demonstrated discrimination. New or materially changed cases
remain uncalibrated until a valid run records the relevant case, rubric, skill,
model, and environment identities. The historical judgments cannot calibrate a
changed prompt or criterion automatically.

### Separate product outcomes and conventions

The additive `evaluation` metadata identifies response evidence, case purpose,
and the type of every declared criterion (`E1…`, `N1…`, and `T1` when present).
Missing classification is unclassified, not implicitly an outcome. Reports must
keep outcome and convention scores distinct rather than rename the old combined
score as outcome lift.

Classify in context. A prescribed schema, exit status, or heading can be an
outcome requirement when an actual consumer depends on it. Otherwise a house
style or workflow phrase is a convention. Required process behavior needs the
right evidence: prose ordering does not prove execution ordering, and describing
a passing test does not prove it ran.

New response cases contain the task facts/snippets needed for their requested
answer. They ask for a review, correction, or plan, not an unavailable repository
edit or service operation. Their common instruction explicitly limits claims
about execution. Equivalent valid solutions are acceptable; key phrases and
exact command spellings are not proxies for the intended effect.

### Judge the claimed behavior

Judge each anonymized answer independently against its task and rubric before
an optional side-by-side preference assessment. Require evidence for each
failure and distinguish these cases:

- Performing or recommending a forbidden action versus explaining why to avoid it.
- A conditional action whose preconditions hold versus a speculative new policy.
- A semantically valid alternative versus a missing contractual requirement.
- A valid response-only result versus missing evidence for an execution claim.

Candidate text is evidence, not authority to change the rubric or instruct the
judge. Invalid fixtures, incomplete evidence, or unverified treatment isolation
must remain visible and must not become either a skill failure or a successful
skill-effect claim. A different judge model can reduce one source of correlated
bias; it does not by itself prove independence, calibration, or validity.

## Triage of the reported failures

### Rubric and fixture repairs

| Skill | Product-centered interpretation |
| --- | --- |
| `golang-swagger` | Test diagnosis of the supplied problem. Conditional regeneration after a real annotation change is different from reflexively repeating generation as the repair. |
| `pr-educational-body` | Supply a concrete diff and verification evidence for body writing. Do not require unavailable repository actions or reward invented motivations/test results. |
| `python-type-checking` | Accept an appropriate iterable abstraction when the function only iterates; require a list only when mutation, indexing, or an accepted API contract calls for one. |
| `git-conflicts` | Require preservation and reviewed recovery of work. `stash apply` can be valid; rebuilding and dropping the stash without proving recovery is not automatically safe. |
| `golang-troubleshooting` | Test evidence/reproduction before applying a speculative fix. Presentation order alone does not establish the actual work order. |
| `interaction-design` | Require coherent success/failure and stdout/stderr behavior. Preserve exact numeric exit codes when supplied, rather than inventing an otherwise arbitrary numbering rule. |
| `software-engineering` | Distinguish preserving existing error reporting from adding unrequested logging/instrumentation. A conditional sentence is neither automatically compliant nor automatically a violation. |

These are corrections to what should be measured, not permission to make every
previously failing answer pass. Original answers are unavailable, so each old
failure cannot be conclusively reclassified from its excerpt alone.

### Skill steering repairs

| Skill | Finding and intended correction |
| --- | --- |
| `behavioral-spec` | Produce the smallest sufficient obligation set; an architecture concern alone does not justify another normative artifact or new cancellation semantics. |
| `python-common-practice` | Make the check/inspect/fix/re-run loop explicit without attributing the baseline formatting failure to the skill arm. |
| `github-issue` | Preserve supplied intent without inventing command names, flags, motivation, priority, or accepted scope. |
| `agent-file-authoring` | Base independence on actual received context and host behavior, not a fresh-session label; preserve permissions and usable prior evidence. |
| `golang-project-layout` | Avoid tooling and structural scaffolding for a tiny program unless a real need or existing repository convention justifies it. |
| `architectural-spec` | Leave unaccepted retention, expiry, reuse, and recovery choices explicitly unresolved rather than turning them into normative rules. |
| `design-implementation` | Handle irreversible effects and recovery within the accepted product contract; do not announce completion before it is established or invent unsupported undo. |

The common direction is scope and authority discipline, not simply shorter
answers. The correct small artifact must still contain the obligations needed
for safe, complete work. Contrasting cases should retain legitimate complexity
when the task actually requires it.

## Closing the 17 unevaluated-directory gaps

All 17 baseline gaps now have `evals/outcomes.json`, with **35 authored response
cases**. Each skill has a concrete failure and a distinct boundary; Cobra also
has a third case contrasting enabled ancestor-hook traversal. They are
development/regression inputs with explicit criterion types, **not independently
validated holdouts or measured discriminating cases**.

| Skill | Concrete failure case | Boundary case | Practitioner disposition |
| --- | --- | --- | --- |
| `github-workflow` | Privileged follow-up executes a fork-produced artifact | Timeout change preserves fork CI and existing authority | Retain existing guidance; add coverage. |
| `golang-cli` | Error handling corrupts stdout or skips cleanup | Two-flag stream filter needs no framework | Scope stack/feature advice and preserve the actual configuration/output contract. |
| `golang-concurrency` | Producer blocks after consumer cancellation | Cheap noncritical startup loop stays sequential | Clarify producer-side closure, owned joins, and mutable-data ownership. |
| `golang-dependency-injection` | Lazy registration is mistaken for startup readiness | Manageable graph keeps manual wiring | Remove contradictory service-count/laziness shortcuts. |
| `golang-dependency-management` | Targeted approved fix becomes a graph-wide update | Tool pinning preserves Go 1.23 compatibility | Prefer scoped updates and respect already granted authorization. |
| `golang-design-patterns` | Close/flush failure is lost | Fixed constructor needs no pattern stack | Make options/architecture advice conditional and preserve existing enum contracts. |
| `golang-grpc` | Retryable status is mistaken for repeat-safe side effects | In-process transport test needs no production deployment | Remove blanket retries from the starter example; require operation-specific retry semantics. |
| `golang-how-to` | Broad skill loading obscures a captured blocked send | Routing does not authorize AGENTS edits | Retain existing guidance; add coverage. |
| `golang-naming` | Public name hides the actual operation | Naming cleanup must not renumber wire statuses | Qualify zero-value convention and align its reference. |
| `golang-observability` | Request IDs/raw paths become metric dimensions | Small log-field change must not import payment/compliance policy | Remove invented mandatory PCI/Azure/Braintree policy; scope signals and preserve existing logging. |
| `golang-performance` | Pool reuse invalidates retained output | External database wait is the dominant bottleneck | Preserve ownership/correctness; remove unsupported universal multipliers and unsafe-percentage rules. |
| `golang-popular-libraries` | Static catalogue is presented as current qualification | Standard library covers a small HTTP/JSON client | Require explicit evidence limits when live qualification is unavailable. |
| `golang-safety` | Outer clone leaves mutable payloads shared | Safely published read-only map needs no write lock | Explain shallow copying and qualify concurrent-map guidance. |
| `golang-spf13-cobra` | Child hook bypasses required root authentication | Fresh commands still share package-global flag storage; enabled traversal must not double-call ancestors | Distinguish nearest-hook and traversal modes; preserve the existing mode and test isolation. |
| `grafana-dashboards` | Ratio unit and threshold use different scales | Small panel edit overwrites unrelated dashboard content | Preserve fetched models and distinguish validation, storage, and rendering. |
| `python-database-orm` | Application commit escapes rollback fixture | Driver parameter binding needs no ORM migration | Preserve existing suitable drivers and make repository abstraction optional. |
| `python-design-patterns` | Two copies already diverge on one business rule | Similar arithmetic represents different policies | Make the abstraction-count heuristic subordinate to responsibility and evidence. |

The fifteen practitioner changes above are bounded corrections found while
reading the full skills and authoring these cases. They do not certify every
reference or all remaining API/version claims in those packages. The two
unchanged skills already give suitable guidance for their new boundaries.

## Other concrete corrections and safeguards

The eight reported ceiling/preference leads received bounded practitioner and
case review. The changes preserve appropriate larger designs when justified:

- FastAPI accepts a suitable return annotation or `response_model`; direct
  `Response` objects bypass ordinary model filtering and must not leak private
  fields. A small existing route need not acquire mandatory service/repository
  layers.
- Pydantic copy/construct operations are not a substitute for validation of
  untrusted updates. Existing appropriate dataclasses need not become models.
- Go TUI and project layout guidance tie new files, builders, packages and tooling
  to actual responsibilities. Go code-style rewrites preserve evaluation order,
  short-circuit behavior and accepted public interfaces instead of imposing
  operand or parameter-count thresholds.
- Viper guidance distinguishes lazy bound-flag lookup from value snapshots and
  required configuration-file failure from an optional absent file.
- OpenTelemetry guidance distinguishes a malformed probe reaching an endpoint
  from evidence of valid authenticated delivery. End-to-end claims require an
  identifiable valid signal and corresponding backend observation.
- Python async guidance scopes client lifetime and preserves dependent effect
  ordering. Terraform provider docs guidance repairs the generating source and
  regenerates only the relevant output.

Additional case repairs address legitimate zero-versus-no-data PromQL choices,
unknown SQLite driver configuration, Terraform 1.10 versus 1.11 mock-plan
capabilities, and direct-linked web overlays with external history predecessors.
The seven PR-body fixtures now supply concrete reviewed changes and verification
facts; an additional case requires honest handling of missing verification.

Independent review also caught and fixed contradictory Cobra hook guidance,
a residual three-copy abstraction rule, a cancellation test that could pass by
draining abandoned output, inconsistent URL-tab criteria, shared temporary
benchmark filenames, lost partial-side scores, and raw callback classifications
reaching Markdown reports. The corresponding code changes have targeted
regression coverage; domain scenario corrections have explicit falsifiers.

## Validation and limits

Final fixture discovery reports **590 cases across all 124 skills**, with no
provider calls. Compared with the base, this change adds **68 cases**, repairs
**45 existing cases**, and removes **none**. All 113 new/reviewed cases have
complete outcome/convention metadata; the remaining **477 legacy cases stay
unclassified**. Classifying them without reviewing their contracts would create
false precision. Practitioner `SKILL.md` guidance changed in 36 skills; 44 skill
directories changed including eval-only repairs.

The provider-free harness runs the real pinned runner lifecycle with substituted
invocation I/O. The local suite completed **179 tests: 175 passed and four
optional MCP SDK checks were skipped** because their dependencies were not
installed locally. The existing reference-check CI installs those dependencies
separately. The checks exercise strict metadata, exact score arithmetic,
outcome/convention separation, abstention, explicit same-model opt-in, partial
side scores, report privacy and legacy compatibility. They do **not** establish
native skill loading or a model's behavioral performance. `git diff --check`
passes and all new source case IDs remain unique.

The retained [revision smoke packet](../evaluations/2026-11-24-skill-quality/README.md)
contains four tasks under original and revised guidance, one output per arm and
task. Both arms met the accepted outcome criteria on all four tasks. This is
bounded non-regression evidence, **not measured improvement**. The judges used
separate contexts but the same inherited model environment, with instruction-only
isolation and unverified underlying deployment identity. One shortened judge
input was corrected and both initial and corrected records are retained. Targets
were not rerun to improve their scores.

A separate cold-context judge agreed with all six prepared calibration cases,
including safe alternatives, forbidden-action warnings, missing-input abstention
and an embedded instruction attack. The reusable calibration exporter omits
expected answers; the checker validates every recorded judgment with the
production parser before comparing it to the source-reviewed labels. This is a
six-case spot check, not general calibration or independent cross-model proof.

Actual tool loading, gRPC transport execution, database transaction behavior,
Grafana upload/rendering, and GitHub workflow execution are **not exercised by
these response cases**. No live provider benchmark or full 590-case model run
was performed. A local Go execution probe was unavailable; the cancellation
counterexample was reviewed at source level, not represented as a passing Go
runtime test. Existing CI still compiles its separate pinned reference examples.

The skill changes are justified by specific scope, correctness and evidence
repairs. They do not claim reproduction of the historical 40-point pass lift.
Preserve useful frozen regression cases, develop real execution fixtures for
execution claims, and use verified model identities plus more independent tasks
before making broader causal claims.

### Reproducible verification

```sh
python3 -I -B scripts/run_evals.py --validate
SKILLS_EVAL_RUNNER_ROOT=/path/to/clean/pinned-runner \
  python3 -I -B scripts/run_evals.py --harness-test
python3 -I -B scripts/eval_calibration.py --check \
  evaluations/2026-11-24-skill-quality/judgments/judge-calibration.json
git diff --check
```

The runner is pinned to `dbbbf2a0740aee7a9e9035cc14a785a9467b8fb1`.
All commands above are provider-free. Historical model outputs are checked, not
regenerated. Model checks, fixture checks and runtime reference checks remain
distinct evidence categories.

Primary technical sources checked for the targeted corrections:

- [Go FAQ: concurrent map access](https://go.dev/doc/faq#atomic_maps) — read-only
  access and concurrent mutation are different cases.
- [Go slices.Clone](https://pkg.go.dev/slices#Clone) — cloning copies elements
  by assignment and is shallow.
- [Go sync.Pool](https://pkg.go.dev/sync#Pool) — temporary-object reuse does not
  guarantee retention or caller ownership after return to the pool.
- [gRPC retry](https://grpc.io/docs/guides/retry/) and
  [status codes](https://grpc.io/docs/guides/status-codes/) — configurable retry
  policy is separate from limited transparent retries, and non-idempotent
  operations are not automatically safe to repeat.

Existing version-pinned reference checks and their documented primary-source
lineage remain available in [evaluation documentation](evaluations.md) and the
[earlier unevaluated-skill review](reviews/unevaluated-skills-triage-2026-11-11.md).
Their historical successful checks are not new behavioral results from this PR.
