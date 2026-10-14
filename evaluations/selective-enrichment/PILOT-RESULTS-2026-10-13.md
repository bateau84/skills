# Selective enrichment: two-case exploratory pilot assessment

Date: 2026-10-13. Producing assessor: current Product Acceptance session, model `openai/gpt-6.1-sol`. Assessment source: eight coordinator-supplied response representations from fresh worker Task sessions. **Current status: two cases assessed across four variants; all eight supplied representations sufficient under the bounded rubric. Repaired superiority remains UNPROVEN.** This is not a full-suite result or an application Product Acceptance PASS.

This continuation supersedes the earlier *no available behavioral artifacts* state, not the historical facts in [the capability assessment](CAPABILITY-ASSESSMENT-2026-10-13.md). That file is preserved unchanged: this evaluator still cannot launch fresh Task sessions, but the coordinator's host reportedly did. The initial four-case plan was not executed as written. Actual supplied subset: PA3 and WD5 only.

## Evidence, source identity and controls

- [Retained input and answer representations](PILOT-ARTIFACTS-2026-10-13.md) include exact fixture prompts/common instruction, all eight IDs, reported reads and received answer text. Some answers were condensed by the coordinator. Quotes/findings below refer to these **received representations**, not purported complete verbatim child transcripts. Full raw outputs are available to the coordinator, not independently accessed here.
- The [24-file source freeze](SOURCE-IDENTITIES-2026-10-13.sha256) was checked again before assessment with `sha256sum -c evaluations/selective-enrichment/SOURCE-IDENTITIES-2026-10-13.sha256`: exit 0, 24/24 OK. It binds all treatment/practitioner/reference/fixture inputs. HEAD alone is insufficient. The original older-source checkout was not revalidated; **older-portable remains the documented manual adaptation**.
- Coordinator reports eight fresh sessions, same `worker` subagent type, environment model `openai/gpt-6.1-sol`, common protocol instruction and per-case prompt, maximum 350 words, read-only behavior, selected practitioner reads only, no no-skill reads, no rubric/companions/other-variant context, no feedback rounds. Actual raw launch/hidden instructions, read traces and completed-output word counts were not inspected here.
- Reference access was instruction-restricted, **not hard sandboxed**. Source paths reveal treatment. Assessor knows variant mapping and is **not blind**; independent assessment means applying the rubric to supplied artifacts, not a blinded or separately hosted judge.
- Same hidden Worker directive is a shared instruction confound. **No-skill means no task-specific SKILL context, not an instruction-free base model.** Its success cannot be attributed solely to the model without that directive.
- Launch order: PA3 no-skill/current/older-portable/repaired; WD5 repaired/older-portable/current/no-skill. Parallel batches, one repetition, counterbalanced exploratory subset, **no controlled randomization**. Actual arrival/completion order and timings unavailable.
- Sampling, context limits, token/cached-token counts, monetary cost and wall time unavailable. Reported read counts: PA3 0/1/1/2 files for no-skill/current/older-portable/repaired; WD5 0/1/1/1. These are reported file loads, not verified tool-call counts or measured cost. Repaired PA3 reportedly read its proof/example reference; repaired WD5 reportedly read only its SKILL.
- No feedback/correction rounds were reported. Scores assess first submitted representations; no corrected/final-after-feedback artifacts exist. This is not a correction-effort experiment.

### Treatment hashes for the reported reads

Paths are relative to repository root; full paths also appear in the artifact record/manifest.

| Treatment | PA3 SKILL SHA-256 | WD5 SKILL SHA-256 |
| --- | --- | --- |
| no-skill | none | none |
| current | `2c337b2a76a9da9441534b3830cc7a33e6cea4b25384acac737187127e83be96` | `c59d8f92911aa076543fa80b3356245e32dbdd8fcad2a492a858b735b11bcd11` |
| older-portable | `2ed91e0f0477f848f30a117e750320c2d094f62c8a15a8696d91815fe33fd0ab` | `0a59de929b04c0377a68d5a6d8f3601965dcdd9e084df95b95a157355dee95b1` |
| repaired | `8797fc3e905b81453801f8b5ea7c953e3aba7dc5b2f542f1f529b09438d74577` | `7d9e464c37229354ffd0b827e44a7c83514c60bc1a97fb2af23a1b453e330352` |

Reported repaired PA3 reference `skills/product-acceptance/references/proof-and-example.md`: `d9d9086d166ec7f30e493eedb53448c983680b276cb034c79d77f684acdf2232`. Hash verification proves local source identity, not which bytes a child actually read.

## Rubric and case mapping

Protocol rubric: **D** decision/outcome correctness; **O** preserved obligations/defect detection; **H** actionable proof/handoff; **P** proportionality/authority. Each 0–2: wrong/missing, partial/actionable gaps, sufficient first attempt. Totals do not excuse fatal errors. No word-count or verbosity bonus.

- PA3 criterion: identify discovery provenance bypass, retain routing/action evidence, allow static prerequisites for B, correct A through real discovery-produced state and the meaningful action without claiming the plan ran. Fixture observations: acceptance cases line 21.
- WD5 criterion: address stale-read/lost-write and shared DB contamination, choose concrete publication/re-read/isolation or ordered-test arrangements, preserve independent docs/analysis, avoid assumed locks/global serialization/plugins. Fixture observations: decomposition cases line 33.

## PA3: matched first-attempt results

| Variant / supplied session ID | D/O/H/P | Total | Artifact-grounded rationale |
| --- | --- | --- | --- |
| [no-skill](PILOT-ARTIFACTS-2026-10-13.md#pa3-no-skill) — `ses_ec927e297ffeU4pfLuKbwUC1sS` | 2/2/2/2 | 8/8 | D: A “does not establish discovery → routing → action”; B supports routing conditional on valid prerequisites. O: preserves “useful downstream integration evidence” and excludes account creation/discovery from B's scope. H: steps 3–5 capture real discovery output, avoid a manual bridge and correlate input/item/decision/action. P: asks for missing executable trigger/observable without discarding narrower evidence or demanding upstream account creation. |
| [current](PILOT-ARTIFACTS-2026-10-13.md#pa3-current) — `ses_ec927e26cffe4iVZ1MYOd2tHSI` | 2/2/2/2 | 8/8 | D: full remains unproven; B prerequisites legitimate. O: explicitly retains downstream evidence and calls B's out-of-scope discovery/account setup “not defects.” H: real discovery/handoff/router/adapter/action with linked item and meaningful action. P: permits a controlled external fixture only outside behavior under proof, requires failure behavior only when the criterion does, and does not call its plan executed. |
| [older-portable](PILOT-ARTIFACTS-2026-10-13.md#pa3-older-portable) — `ses_ec927e229ffem4fdeGVYY7mCpu` | 2/2/2/2 | 8/8 | D: inserted output leaves discovery behavior/provenance/compatibility unproven; B legitimate. O: “the narrower evidence remains useful.” H: real entry/discovery-produced state/router/adapter, same-item input/state/decision/action assertions rather than internal success. P: asks only for missing path/action/accepted recovery specification, does not prohibit static setup or require invented recovery. |
| [repaired](PILOT-ARTIFACTS-2026-10-13.md#pa3-repaired) — `ses_ec927e20dffe1dXMWBJDRXoNRT` | 2/2/2/2 | 8/8 | D: full UNPROVEN “not necessarily failed”; B narrow support. O: explains why downstream reality cannot fix injected discovery provenance and retains narrower evidence. H: real discovery/persistence/transport/router/adapter/action, same-run tracing and expected versus observed action, plus build/config/run record. P: legitimate static prerequisites/external substitution, recovery only if agreed; missing record fields are gaps, not demonstrated implementation defects. |

Detected missed load-bearing defects: **0 per representation**. Detected unnecessary blockers: **0 per representation**. Detected fatal errors: **0 per representation**.

Status-wording judgment: older-portable's “The broader claim fails” is read in its stated context as rejection of an unsupported proof claim; surrounding text says discovery is unproven. It does not establish or assert an observed broken product. Repaired's narrow PASS is conditional assessment of B's supplied real-path facts, not a claim that the participant ran it; its corrected A plan is explicitly not executed. Neither is a detected fatal error. No-skill's request for concrete trace artifacts limits a later independent audit; it does not reject the supplied narrower decision evidence.

**Matched finding:** no scored separation. Repaired supplies more explicit proof-record/fidelity detail; no-skill/current/older-portable already satisfy PA3's material decisions and corrected path. Additional detail is not itself superiority.

## WD5: matched first-attempt results

| Variant / supplied session ID | D/O/H/P | Total | Artifact-grounded rationale |
| --- | --- | --- | --- |
| [no-skill](PILOT-ARTIFACTS-2026-10-13.md#wd5-no-skill) — `ses_ec92724aaffe30Qopbo2Lby1AD` | 2/2/2/2 | 8/8 | D: independent preparation with one integrator and combined verification dependencies. O: rejects stale whole-file replacements, preserves unrelated keys and addresses both source and DB hazards. H: latest-canonical setting deltas, sole-publisher re-read; per-run DB ownership or serialized/reset tests if names fixed. P: no-workspace fallback preserves parallel proposals/docs; no plugin or global block. Cross-field checks are combined verification, not an invented semantic dependency. |
| [current](PILOT-ARTIFACTS-2026-10-13.md#wd5-current) — `ses_ec92724f0ffeH4FBl9N5BuzKBi` | 2/2/2/2 | 8/8 | D: explicitly rejects reference's lock assumption because supplied host lacks the guarantee. O: independent docs/development retained; separate tests insufficient for the combined change. H: sole canonical publisher, baseline/current re-read/reconcile, no full snapshots; exclusive DB setup/execution/background/cleanup/reset with revision evidence. P: no implicit lock/plugin; resource serialization only, unique names may remove that constraint. |
| [older-portable](PILOT-ARTIFACTS-2026-10-13.md#wd5-older-portable) — `ses_ec9272508ffetSUgbchTbUho4W` | 2/2/2/2 | 8/8 | D: parallel preparation, integrator after patches, sequential DB lifecycle. O: latest-file reconciliation preserves both settings/unrelated data; all database consumers and cleanup included. H: private drafts/patches, current-read setting publication, reset/exclusive setup-through-teardown and exact revision evidence. P: single-writer protocol not a host lock, docs/DB-independent checks concurrent, unknown writers/resources are flagged rather than silently assumed. |
| [repaired](PILOT-ARTIFACTS-2026-10-13.md#wd5-repaired) — `ses_ec9272528ffee2sRjC67liICAc` | 2/2/2/2 | 8/8 | D: independent A/B with integrator depending on both, owns combined proof. O: re-read/reconcile against current file, preserve intervening changes, stale-base tests insufficient; DB contamination addressed. H: narrow isolated patches, sole publisher, per-run names or ordered full DB lifecycle, revision/database/results record. P: integrator may live in existing group, host lock not assumed; unavailable isolation falls back to parallel analysis and ordered edits/tests, no plugins. |

Detected missed load-bearing defects: **0 per representation**. Detected unnecessary blockers: **0 per representation**. Detected fatal errors: **0 per representation**.

**Matched finding:** no scored separation. Repaired and no-skill prefer DB isolation when available with serialization fallback; current and older-portable choose immediately safe serialization of a shared DB while preserving independent preparation/docs. Both arrangements are allowed by WD5. Penalizing serialized conflicting DB tests would mistake proportionate coordination for globally serialized work.

**Current baseline is not a participant fatal:** its authored lock guarantee remains a real baseline source defect, but this response explicitly overrides it using the host facts and gives a safe arrangement. Do not report a behavioral lock failure where this artifact did not make one; do not infer the source defect harmless on other cases.

## Outcome and author-review handoff

- **Bounded artifact adequacy:** all eight received first-attempt representations sufficient (8/8 each). No detected load-bearing misses, unnecessary blockers or fatal errors in this evidence. Because some responses were condensed, absence findings are limited to the received text; omitted raw content/tool violations cannot be excluded independently.
- **Comparative improvement:** no observed rubric advantage for repaired; PA3 and WD5 are at ceiling for all four treatments. One observation per cell cannot demonstrate equivalence, causal benefit, universal robustness or absence of regression. Shared Worker instructions may explain some baseline/no-skill strength; no mechanism can be identified from this pilot.
- **Correction effort:** zero feedback rounds reported; no correction exercise, time-to-acceptable or comparative correction cost measured. Supplied first attempts satisfy this rubric without reviewer-requested corrections; that is not a measured efficiency advantage.
- **Concrete active-skill author repair:** none required by the received artifacts. No current artifact fatal to notify before review. Independent implementation review can proceed with this bounded evidence; it must not interpret it as a full acceptance gate or efficacy proof.
- **Unrun coverage:** PA1, PA2, PA4, PA5, PA6, PA7, PA8, PA9; WD1, WD2, WD3, WD4, WD6, WD7. Thus 14/16 supplied cases, 56/64 case/variant cells unrun. The earlier four-case plan still lacks PA8 and WD2, and WD5 launch order differs from that plan. This is only the two-case subset, not its completion.
- **Discovery, ASSESSMENT/QA companion experiments and real application E2E:** not run. Explicit reads do not prove discovery. PA8 shipping/upgrade, WD2 hazardous rollout, local-patch/API overblocking and lock-cycle/generated-output behavior remain open discriminators.
- A modest useful next comparison is PA8 plus WD6 (shipping fidelity and mutation-lock/read-cycle separation), or PA8 plus WD2 to finish the earlier planned case set, with identical fresh controls. This is a recommendation, not new required scope or an executed result. Repeating ceiling cases alone is unlikely to resolve the current comparison question.

## Evaluator actions and evidence limits

This continuation read the historical report, protocol, manifest and fixture files with `functions.read`, and ran:

```sh
sha256sum -c evaluations/selective-enrichment/SOURCE-IDENTITIES-2026-10-13.sha256
git status --short -- evaluations/selective-enrichment && git diff --cached --binary | sha256sum
```

Both commands exited 0. Manifest 24/24 OK; index-diff digest remained empty (`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`). Assessment judged actual received answer content, not candidate claims of having executed products. This evaluator launched no child sessions and observed no child file-read tools directly.

Only these new pilot artifacts/results resources were authored with `apply_patch` under `evaluations/selective-enrichment/`. Historical report, protocol, freeze manifest, skills and baselines were not rewritten. Protocol's original prepared-status line remains its historical preparation status; this separate linked update is the current result record. No staging/commits/push/install/external paid API usage or unrelated-change restoration. No absent Loom/host evidence APIs or PASS claims are invented.
