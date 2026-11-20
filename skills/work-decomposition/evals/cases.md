# Work Decomposition Decision Cases

Prepared evaluation inputs, **not executed results**. WD1–WD4 adapt the older source's four cases; WD5–WD7 test the accepted portability/coordination findings; WD8–WD9 test context-bounded sizing and adaptive re-slicing. WD10–WD12 exercise milestone ordering, necessary foundations, and learning from actual use. Source identity and adaptation limits are recorded in the bundled [SKILL.md](../SKILL.md). All code/resource paths in these packets are illustrative inputs, not claims about this repository.

### Standalone execution

In a fresh session, explicitly load the bundled `SKILL.md` and allow its practitioner reference when useful; then give only one selected **Prompt** and the common instruction below. No sibling acceptance skill is required. Withhold evaluator observations, companion rubrics, and other participants' answers. Retain the first answer, actual loads, and any feedback rounds; judge the produced groups/coordination/handoff against the case's evaluator observations for correctness, preserved obligations, actionable proof ownership, and proportionality. Record missed defects, unnecessary blockers, correction rounds, and cost only where observed; do not score document length or claim an application ran.

> Work from the supplied task and evidence packet within its stated scope. Produce the requested practical artifact and rationale. Treat supplied facts as evidence for this decision exercise, not as actions you performed. State missing evidence and unresolved decisions precisely; continue independent work where possible. Use available reference material when useful. Do not invent requirements, tool execution, or results.

A no-skill control omits skill/reference context but keeps the same prompt, model, tools, common instruction, and budget in another fresh session. Four-variant comparisons additionally require genuinely preserved current/older-portable materials and identified repaired bytes: never reconstruct a baseline from memory or call a single-package exercise that comparison. The full collection optionally provides `evaluations/selective-enrichment/README.md` and historical baseline/pilot records relative to its root; these collection-only maintenance resources are not required for this standalone exercise. Explicit loading tests task performance, not discovery.

## WD1 — five concerns, one endpoint

**Prompt:** Propose candidate groups for adding one REST decision-detail endpoint. Current inspection: `app/decision.ts` contains registration, validation, handler and serialization; `api/openapi.yaml` documents it; `app/decision.test.ts` and the generated client are relevant consumers. These are small, same owner, same dependency position, one-session work. The input lists those five concerns separately. Preserve usable endpoint/errors/docs and verification; say why to merge or separate. Planning only, no final scheduling requested.

**Evaluator observations:** One coherent group, or a justified second merge candidate, not five dispatches. Own caller/generated-client consistency and falsifiable endpoint evidence. No fictional path inspection, schedule/plugin requirement, or added milestone hierarchy for this local outcome.

## WD2 — hidden irreversible migration

**Prompt:** The accepted architecture separately deploys an additive schema compatibility change and a large irreversible backfill. Current inspection: `db/schema.sql`, `api/history-reader`, and `worker/history-reader` consume the old representation; `ops/backfill` performs transformation. Old history must remain readable during rollout; accepted transformation/no-loss rules are explicit and not open for redesign. The proposal is one group, “update database.” Return candidate boundaries, preserved obligations, safety/dependencies, surfaces, and who proves real upgrade and both consumers. Do not turn every file into a task.

**Evaluator observations:** Separate routine compatibility from hazardous separately deployed operation; name prerequisites and proof owner, both consumers, rollout invariant. No new migration policy or collapsed safety boundary; ordinary mechanics need no new product approval.

## WD3 — natural ownership and merge candidates

**Prompt:** Decompose auth work: hash algorithm replacement and registration strength validation share owner/dependency/files and agreed semantics; login rate limiting is platform-owned across a process boundary with an accepted auth/platform contract; API docs need refreshing. Inspection confirms `auth/register`, `auth/login`, `platform/limiter`, their contract tests, and `docs/auth-api`. Return compact candidates, merge candidates where appropriate, integration/verification ownership, and one accepted registration/login scenario's required groups. Scheduling/assignment is not requested.

**Evaluator observations:** Keep or explicitly merge hash/validation; preserve platform/process seam. Docs may join relevant owner or remain justified candidate, not forced standalone. Shared guarantee and proof ownership visible; no unapproved algorithm/strength/rate policy redesign.

## WD4 — product proof without per-seam task explosion

**Prompt:** Decompose the accepted browser configuration → API → worker → persistence → explanation journey, plus quota/defer/resume. Current inspected surfaces are `web/client`, `app/config-api`, `app/decision-api`, `worker/discovery`, `worker/queue`, `db/migrations`, related tests and build config. Each layer has local tests; the client still has a product-owned mock-detail fallback, a known integration risk. Propose meaningful intermediate outcomes and coherent groups with obligations, peer prerequisites, and assembled-proof ownership. Explain the first demonstration and any necessary enabling work; do not create one E2E task per arrow.

**Evaluator observations:** Organize groups around a real useful journey and its next extension, or justify a necessary technical prerequisite before that journey. Remove the fallback and own the real endpoint and assembled proof; independent module tasks may contribute to one milestone. Keep applicable guarantees and recovery obligations explicit, with actual recovery proof before claiming them. No task-per-arrow ritual, union-of-unit-suites acceptance, or full-product claim from a bounded first demonstration.

## WD5 — unlocked shared file, stale reads, independent progress

**Prompt:** The host has no file-lock guarantee. Two semantically independent groups will edit separate settings in `config/shared.yaml`; both may read the same old bytes. Their tests also share one temporary database name. A third group changes only isolated docs. Propose coordination and dependencies that keep useful parallelism without lost writes or contaminated evidence. You may choose ordinary isolation, an integrator, or ordered publication; no plugin installation is allowed.

**Evaluator observations:** Explain stale-read/lost-write risk and shared test state; choose concrete re-read/reconcile/integrator or isolated merge arrangement plus isolated/ordered DB tests. Independent docs/analysis can run in parallel. Do not invent locks or globally serialize all work.

## WD6 — mutation locks do not protect the read/edit cycle

**Prompt:** The host serializes individual file writes but does not lock the whole read/edit/verify cycle. Group A and B each read the old generated client and later publish changes derived from different API schema revisions. They use the same test port. The API contract is agreed, and a schema revision must be integrated before final client generation. Assess proposed “parallel is automatically safe because writes are locked,” and propose a proportionate corrected arrangement.

**Evaluator observations:** Mutation locking does not prevent stale snapshots, inconsistent generated outputs, or port interference. Assign stable-schema prerequisite and generation/publication responsibility, re-read/reconcile and combined verification, isolated/ordered test resources. Do not forbid all parallel work or change accepted API semantics.

## WD7 — honest surface uncertainty and decision ownership

**Prompt:** Planning-only analysis has inspected `api/export` and its caller tests. A background consumer and generated schema are suspected but not inspected. The accepted promise says “export accepted records”; whether “accepted” includes deferred records is unresolved and user-owned. Choose candidate grouping/discovery and identify the exact decision question. Distinguish ordinary serialization/test choices from product semantics. Do not assert guessed paths exist, compile final write scopes, or block unrelated inspection. Later executable handoff will need complete authorized surfaces.

**Evaluator observations:** Label unknown targets unverified and assign discovery; preserve exact decision for owner, continue independent work. No invented deferred-record semantics or needless approval of ordinary mechanics. Planning-only exact scope deferral is legitimate; executable handoff must cover real consumers/tests/generated source once known.

## WD8 — oversized coherent theme needs context-bounded split

**Prompt:** A proposal has one task, “modernize configuration,” owned by one backend agent. Current inspection shows three substantial stages: first diagnose precedence behavior across `config/load` and `config/merge`; then choose among already-authorized compatibility realizations based on that result; then migrate `runtime/session` and prove old/new configuration behavior. The same owner could do all of it, but the diagnosis can materially change the later migration and the final proof is independently meaningful. Produce candidate groups and explain the sizing decision. Do not split by file count or invent new semantics.

**Evaluator observations:** Split the broad task at meaningful discovery/decision/implementation or verification boundaries so later work starts from a compact result; justify context/reasoning and retry cost. Preserve one owner where appropriate and avoid one-task-per-file fragmentation. No fixed numeric task/step limit.

## WD9 — execution discovers larger scope and re-slices remaining work

**Prompt:** An implementation task was reasonably planned as one focused change. During execution, investigation completes and establishes a previously unknown generated consumer, a migration requirement, and a separate compatibility proof. The investigation evidence remains valid, but continuing would substantially enlarge the working set and reasoning chain. State how decomposition should adapt without discarding valid completed work or pretending the original task size is still appropriate.

**Evaluator observations:** Preserve the completed investigation as evidence/result and re-slice only the remaining work into coherent context-bounded units. Do not force continuation, restart valid work, or treat replanning as failure. Keep dependencies and proof ownership explicit.

## WD10 — a useful first increment before complete subsystems

**Prompt:** Plan candidate milestones and work groups for an accepted local report tool. It must eventually select records, export CSV and JSON, show progress, and let the operator inspect the final file. Existing selection and atomic-file-write modules are verified. CSV encoding and the real CLI-to-export path are missing; JSON and richer progress controls are independent later capabilities. No known seam risk requires an experiment. A proposal first completes every formatter, then every progress control, then integrates the CLI. Explain what to deliver and demonstrate first, how tasks support it, and how later accepted obligations stay visible. Planning only; do not invent inspected paths or implementation results.

**Evaluator observations:** Choose an early complete real selection-to-CSV-to-inspection outcome, retaining atomic publication and relevant existing guarantees. Derive coherent bounded tasks from that milestone instead of making all formatter/control capabilities prerequisites. Keep JSON and richer progress outcomes, ownership, dependencies and proof/refinement paths visible without fully scheduling speculative later tasks. Explain contribution to the overall goal and learning from use. No product-side stub as milestone evidence, scope deletion, or assumption that every task must itself be user-visible.

## WD11 — a decisive technical prerequisite remains first

**Prompt:** Decompose work for an accepted local import tool whose first operator journey reads an archive and previews extracted records. The tool must never write outside its selected directory. Current inspection finds that the extraction dependency's symlink handling is unknown; either result could change the accepted architectural realization. An isolated fixture probe is authorized, but processing real user archives before this is established is not. A proposal skips the probe to show the CLI journey sooner. Describe the first meaningful checkpoint, independent work, and later product milestone. Preserve the agreed boundary and do not design a replacement extractor yourself.

**Evaluator observations:** Keep the bounded symlink/escape probe before dependent real archive processing; state discriminating evidence, the dependent outcome and routing if the architecture must change. Identify safe independent work where supported. Distinguish a risk-resolution milestone from a usable product increment and a planned probe from observed evidence. No early-demo waiver of the directory guarantee, full-product halt, new global approval framework, or claim that all milestones must deliver a public feature.

## WD12 — demonstrated use changes the remaining plan

**Prompt:** The first accepted report-tool milestone has been demonstrated through the real CLI: select records, publish CSV atomically, and inspect the final file. Its evidence remains valid. During that run the operator reports that finding the output location is confusing; explicit completion output naming the file is already an accepted requirement. A later milestone was fully broken into tasks for JSON export and richer progress controls. Plan the next bounded work from this evidence, preserve valid results, and explain whether the existing schedule must stay unchanged. No new UI or product capability is requested.

**Evaluator observations:** Reassess the incomplete output-discovery obligation and place its bounded correction and meaningful verification appropriately before or with the next useful outcome. Preserve the proven export behavior and recheck it where affected. Revise only affected remaining tasks/dependencies and retain later accepted capabilities; do not treat earlier scoped PASS as satisfaction of the whole goal or rewrite requirements to fit the result. No wholesale restart or new approval stage merely because the plan changes.
