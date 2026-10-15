# Selective enrichment: capability boundary and source evidence

**Date:** 2026-10-13. **Producer:** current Product Acceptance evaluator session.
**Behavioral verdict: UNPROVEN. No independent pilot comparisons executed.**

Purpose: hand off an honest evaluation boundary, reproducible source identities, and a small discriminating pilot to the coordinator and independent reviewer. This is a portable evaluation evidence resource, not product authority, an implementation review approval, or a Loom/OKF-registered report.

## 1. Actual capability and session provenance

- Requested comparison: no-skill / frozen current / manually adapted older-portable / repaired, using fresh isolated same-model/role/instruction/tool sessions and explicit practitioner loading.
- Actual evaluator model: `openai/gpt-6.1-sol`, as declared by this session's developer instructions. Role: Product Acceptance. Platform session ID, sampling settings, context limit, token/cached-token counts, monetary cost and wall time are not exposed/observed.
- Available callable tools: `functions.apply_patch`, `bash`, `glob`, `grep`, `read`, `skill`, `webfetch`, and `multi_tool_use.parallel`. **No Task, Agent, child-session creation, or context-reset interface is present.** Parallel tool calls do not create model participants. No external model runner was invoked, installed, or substituted.
- No grant/workflow/step/question ID was supplied, and no Loom attach/plan/status/result/evidence/complete APIs are exposed. The user explicitly permits portable evidence authority without absent host APIs. No Loom PASS or immutable Loom result is claimed.
- Host guidance actually loaded via `functions.skill`: product-acceptance, graphify, report-lifecycle. Host product-acceptance resolves under `/home/bateau/.config/opencode/skills/`, **not** the repaired project treatment. The project SKILL bodies were read by exact repository path. These were evaluator loads, not participant trials. No graph pipeline ran: no existing `graphify-out/graph.json` was found, and new graph output/install/provider use would exceed this task's permissions.
- Evaluator read the protocol, provenance, both complete fixture files including evaluator observations, all four supplied practitioner bodies, repaired practitioner references, and project report-lifecycle guidance. Baseline companions and repaired acceptance/decomposition companions were hashed, not loaded into a practitioner trial. This evaluator is unblinded and context-contaminated for subsequent participant work.
- Thus a four-answer exercise in this same context would test neither no-skill nor isolation. Child session identities, participant load traces, first artifacts, blind judges and observed correction rounds do not exist. None are fabricated below.

## 2. Evidence gathered and source identity

Repository HEAD observed: `31ad1ad06792ed6bc904fb3e8fab21cce698fe14`. Extensive dirty changes existed at entry; HEAD alone is not the treatment identity.

The [SHA-256 manifest](SOURCE-IDENTITIES-2026-10-13.sha256) records 24 observed file identities: all 12 frozen baseline files, six repaired skill/companion files, two repaired practitioner references, two fixture files, protocol and provenance. All 12 baseline hashes matched the supplied PROVENANCE tables. This validates preserved local baseline identity, not the original older checkout or behavioral efficacy. The original older checkout was not independently inspected in this session.

Key repaired identities:

| Resource | SHA-256 |
| --- | --- |
| acceptance SKILL | `8797fc3e905b81453801f8b5ea7c953e3aba7dc5b2f542f1f529b09438d74577` |
| decomposition SKILL | `7d9e464c37229354ffd0b827e44a7c83514c60bc1a97fb2af23a1b453e330352` |
| acceptance proof/example reference | `d9d9086d166ec7f30e493eedb53448c983680b276cb034c79d77f684acdf2232` |
| decomposition boundaries/example reference | `1bb7481e6e35940c30f55a6745df2512f9317c15dc895eafe648360d666fca76` |

Older-portable is explicitly a **manual adaptation**, not the exact older source. Any future difference against it must retain that qualification. No-skill has no skill-file identity and has not been executed.

### Commands/actions actually performed

From `/home/bateau/git/bateau84/skills`:

```sh
git status --short
sha256sum evaluations/selective-enrichment/baselines/{current,older-portable}/{product-acceptance,work-decomposition}/{SKILL,ASSESSMENT,QA}.md skills/{product-acceptance,work-decomposition}/{SKILL,ASSESSMENT,QA}.md skills/product-acceptance/references/proof-and-example.md skills/work-decomposition/references/boundaries-and-example.md skills/{product-acceptance,work-decomposition}/evals/cases.md evaluations/selective-enrichment/{README,PROVENANCE}.md
git rev-parse HEAD && git diff --binary | sha256sum && git diff --cached --binary | sha256sum
git diff --check -- skills/product-acceptance skills/work-decomposition
```

All commands above returned exit 0. The whitespace check had no diagnostics; it is structural supporting evidence, not usefulness evidence and not a check of every untracked file. Source reads used `functions.read`; inventory used `functions.glob`. The tool transcript is the original observation trace; the manifest preserves the hash output bytes as text.

Pre-write tracked-diff digest: `8943a2770890c0efd907fea8cf80e0122a00ea1cc1e7e3689e85a09a7d96379d`. Cached-diff digest: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty). Only this evidence resource and its manifest were added with `apply_patch`. No skill/baseline/protocol inputs were edited. No staging, commits, pushes, installs, paid API calls or application runs occurred.

Post-write verification actions:

```sh
sha256sum -c evaluations/selective-enrichment/SOURCE-IDENTITIES-2026-10-13.sha256
git diff --binary | sha256sum && git diff --cached --binary | sha256sum && git status --short -- evaluations/selective-enrichment skills/product-acceptance skills/work-decomposition
```

Both returned exit 0. All **24/24** manifest entries returned `OK`; both added evidence files were read back successfully. The cached-diff digest remained empty. The overall tracked-diff digest changed to `1bd671295856dc0db90f401f4d5a0ffdabdeeb3c2253a768a81bcb8d7b6326d4` during observation. The cause was not determined; no unchanged-whole-working-tree claim is made. This evaluator's only mutations were the two untracked evaluation evidence files, and all hashed evaluation inputs remained identical. No unrelated changes were reverted or reconciled.

## 3. Source findings, NOT behavioral scores

These compare authored guidance against supplied decision tasks. They establish explicit coverage and one known baseline instruction defect; they do not establish what a fresh model would produce, detect, miss, or unnecessarily block. Line citations refer to the hashed files.

| Discriminator | Frozen current | Older-portable adaptation | Repaired practitioner guidance |
| --- | --- | --- | --- |
| PA3: injected discovery state versus legitimate routing prerequisite | acceptance SKILL 12–16 states the real-component rule, but has no explicit state-provenance/static-prerequisite distinction | acceptance SKILL 101–109 explicitly distinguishes upstream-produced state and static prerequisites | acceptance SKILL 37–39 explicitly preserves narrow routing evidence and legitimate prerequisites |
| PA8: wrong build/configuration and bypassed upgrade migration | acceptance SKILL 12 states production implementation; no concrete build/configuration/schema fidelity record or historical-input distinction | acceptance SKILL 16 says intended-to-ship; 49 includes migrations; 101–109 covers provenance. The practitioner proof template 123–137 has no dedicated build/configuration identity fields. Provenance documents that detailed shipping fidelity stayed in its companion | acceptance SKILL 39–41 explicitly requires real migration from legitimate historical input and claim-relevant shipping fidelity; 47 includes build/configuration in the minimum record |
| WD5: unlocked writes, stale snapshots and shared database, while retaining independent work | decomposition SKILL 16 incorrectly asserts runtime file locks serialize concrete mutations. This is an actual authored baseline defect, incompatible with WD5's supplied host facts; not an observed model failure | decomposition SKILL 40 includes mutable resources; 55 identifies resource/write-safety boundaries; no lock guarantee, but no detailed stale-read/reconcile/test-isolation procedure | decomposition SKILL 20 names DB/ports/cache; 51–53 denies assumed locks, addresses stale reads, isolation/integrator/publication, re-read/reconcile and combined verification while preserving independent work |
| WD2: separately deployed irreversible migration, both consumers, upgrade proof ownership | decomposition SKILL 14 recognizes safety/ownership/dependency; 28 asks integration implications, with little operational detail | decomposition SKILL 24, 41, 47 preserves safety/invariants; 65–73 gives candidate obligations/scenarios, less explicit falsifiable seam/proof ownership | decomposition SKILL 35 names irreversible/separate rollout boundaries; 45–47 and 61–64 require guarantee/proof ownership. Reference 11–19 illustrates compatibility/backfill separation and API/worker proof without choosing new loss policy |

**Author-repair finding:** the documented unsupported lock guarantee is present in the frozen current practitioner baseline and absent from repaired practitioner guidance, which supplies concrete countermeasures. Do not repair the frozen baseline. No new concrete defect requiring active-skill repair was established by this bounded source inspection. That is not a clean bill of health: usefulness, regression/overblocking, discovery, first-attempt quality and cost remain unproven, and independent implementation review is still needed.

The repaired guidance's additional explicit decisions are plausibly useful, especially WD5 and PA8. This is a hypothesis supported by source differences, **not** measured superiority. Current already contains the central real-path rule; it must not be described as having observed failures on all acceptance cases.

## 4. Smallest useful next pilot (planned, NOT RUN)

Four supplied cases, one fresh session per case/variant, one repetition: **16 first-attempt artifacts**, versus 64 for all 16 supplied cases across four variants. This is an exploratory decision-artifact pilot, not executable application E2E or general-purpose skill validation.

| Case | Accepted evaluation concern | Artifact to inspect | Planned counterbalanced order |
| --- | --- | --- | --- |
| PA3 | Preserve real upstream provenance without rejecting legitimate prerequisites/narrower proof | Two scoped verdicts and corrected proof plan, including retained routing evidence | no-skill → current → older-portable → repaired |
| PA8 | Prove shipping-equivalent upgrade and real migration without demanding production secrets | Defect finding and corrected historical-input → migration → user-read proof | current → older-portable → repaired → no-skill |
| WD5 | Prevent lost writes/test contamination without invented locks or global serialization | Concrete settings-publication/re-read and test-DB arrangement, retaining independent docs progress | older-portable → repaired → no-skill → current |
| WD2 | Preserve hazardous rollout separation, both consumers and assembled proof responsibility without fragmentation | Candidate groups with compatibility prerequisite, safety obligations, consumers and proof owner | repaired → no-skill → current → older-portable |

This order is planned counterbalancing, not performed randomization. Selection used fixture facts/source inspection but no participant outputs. It covers provenance, fidelity, coordination and safety plus useful narrower-work/nonblocking controls. It does not cover all accepted concerns.

### Required execution controls

1. Verify the manifest before use; if repaired sources changed, freeze a new identity rather than silently treating this one as current. Use exactly the protocol's common instruction and only the selected case's Prompt verbatim. Withhold case heading/trap, evaluator observations, protocol rubric, provenance and other variants.
2. Require a fresh context for each of the 16 participants with the same exact model, role, instructions, permissions/tool capability and known settings. Record unavailable settings. A shared tool wrapper or a claimed reset inside one chat is insufficient. If the participant role auto-loads acceptance/decomposition guidance for no-skill, it invalidates the intended no-skill contrast; choose one matched practitioner role/instruction envelope and log it.
3. Load the selected supplied SKILL body by exact path/message, not the host installed skill with the same name. Only variant-appropriate practitioner references may be requested; log actual loads and hashes. Do not load ASSESSMENT/QA in this primary experiment. The repaired WD practitioner link to acceptance guidance must be handled consistently as an allowed practitioner reference if requested, and its actual load recorded. Keep evaluation/provenance links inaccessible to participants even when a SKILL body mentions them.
4. Capture the first submitted text artifact and trace before feedback. Judge those bytes against case facts; don't award points for saying a test ran or reciting the methodology. Use the protocol's four 0–2 dimensions, cite passages, and separately record missed load-bearing defects, unnecessary blockers and fatal errors. Alternative correct plans/groupings are valid.
5. Planned correction budget for this minimal pilot: **zero feedback rounds** for all variants. Thus it tests first-attempt artifacts only; rounds-to-acceptable and correction cost remain not assessed, rather than being reported as zero-to-success. A later equal-budget correction experiment would need separate preserved feedback/artifacts.
6. Blind the scorer to variant where practical; retain a sealed identity mapping and disclose any recognition from style/content. One repetition supports exploratory per-case contrasts, not reliable causal/generalized effect estimates. Record tokens/time/load calls only when genuinely exposed.

### Unrun suite and claims

All PA1–PA9 and WD1–WD7 comparisons remain **NOT RUN**, including the proposed four-case pilot. PA1/4/5/6/7/9 and WD1/3/4/6/7 are outside this proposed pilot; PA2 is also unrun and supplies a valuable external-fake/live-compatibility control for follow-up. PA6 checks local-patch overblocking, PA9 API/browser claim scope, and WD6 write-lock versus read/edit-cycle safety. These are relevant remaining concerns, not silently covered by the pilot.

Discovery testing and companion conformance/QA experiments: **NOT RUN**, separate from explicit practitioner-loading performance. No discovery success follows from evaluator file reads. No real application outcomes were executed; fixtures are supplied decision packets.

## 5. Observed outcome summary

| Activity/measure | Result |
| --- | --- |
| Baseline identity check | 12/12 hashes match supplied provenance |
| Source identity capture | 24 files recorded; not behavioral evidence |
| Behavioral first attempts | 0 executed; all variants/cases unproven |
| 0–8 scores, missed model defects, model blockers, fatal model errors | Not assessable: no participant artifacts |
| Correction rounds to acceptable / correction cost | Not observed; no rounds or acceptable artifacts |
| Token/monetary/wall-time comparison | Not observed; no comparative claim |
| Discovery / full suite / companion activities | Not run |
| Active-skill deficiency needing author repair | None newly established by bounded source inspection; behavioral efficacy and review remain open |

The exact blocker is missing fresh isolated model-session capability, not unavailable Loom infrastructure, missing fixtures, JSON syntax or lack of permission to perform ordinary evaluation. The next honest step is running the matched pilot on a host exposing suitable isolated sessions, then scoring actual first artifacts independently.
