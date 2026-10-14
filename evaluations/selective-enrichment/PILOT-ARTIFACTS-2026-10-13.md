# Two-case pilot: supplied inputs and response representations

Date: 2026-10-13. Source: coordinator's continuation message to this Product Acceptance evaluator. This file reproduces the supplied answer representations, not independently retrieved child transcripts. The coordinator initially described responses as verbatim apart from layout, then explicitly clarified that some long responses were condensed. **All response blocks below are therefore labeled coordinator-provided representations, potentially condensed.** Wording within these blocks is preserved from the supplied packet; table whitespace is formatted for readability. No block is asserted to be a complete raw participant response or tool trace.

Full host Task outputs reportedly remain available to the coordinator. This evaluator has no raw child-output/trace API. Sessions, launch controls and reads are coordinator reports; artifact contents below are the actual received evidence assessed in [the results](PILOT-RESULTS-2026-10-13.md). Do not feed this evidence file to later participants.

## Input identity

The [existing source manifest](SOURCE-IDENTITIES-2026-10-13.sha256) was reverified before assessment: 24/24 entries OK. It identifies both fixture files and the protocol. The coordinator reports identical prompts/instructions for each variant within each case, fresh worker sessions, one repetition, maximum 350 words, no mutation or tools other than selected practitioner-file reads, and no feedback rounds. Actual launch messages, hidden Worker directive and complete tool traces were not supplied.

### Common instruction

From protocol README line 48, reported supplied identically to all eight workers:

> Work from the supplied task and evidence packet within its stated scope. Produce the requested practical artifact and rationale. Treat supplied facts as evidence for this decision exercise, not as actions you performed. State missing evidence and unresolved decisions precisely; continue independent work where possible. Use available reference material when useful. Do not invent requirements, tool execution, or results.

### PA3 prompt

From `skills/product-acceptance/evals/cases.md` line 19; fixture-file SHA-256 `f4f065f7d9a409ae354b454b574b9a9f8ccc93bdb047f6fd1234d9a52eab903e`:

> Classify two proofs. A claims discovery → routing → action, but inserts a discovered-item row before running the real router/adapter and observing the action. B claims routing → action only; it uses an existing account and supplied item as prerequisites and runs the real routing/action path. Write the supported claim and gap for each, and a corrected plan for A. Do not discard useful narrower evidence.

### WD5 prompt

From `skills/work-decomposition/evals/cases.md` line 31; fixture-file SHA-256 `14c4081aa978c04c1516a01e7cd6d0ef825d7b7b032bf3172340f1f7715d1b97`:

> The host has no file-lock guarantee. Two semantically independent groups will edit separate settings in `config/shared.yaml`; both may read the same old bytes. Their tests also share one temporary database name. A third group changes only isolated docs. Propose coordination and dependencies that keep useful parallelism without lost writes or contaminated evidence. You may choose ordinary isolation, an integrator, or ordered publication; no plugin installation is allowed.

## PA3 no-skill

Reported worker Task/session ID: `ses_ec927e297ffeU4pfLuKbwUC1sS`. PA3 launch position 1, repetition 1. Reported practitioner reads: none. Coordinator-provided representation, potentially condensed:

| Proof | Supported claim | Gap / limit |
| --- | --- | --- |
| A | Routing → action, for the manually inserted discovered-item row, through the real router/adapter and observed action. This is useful downstream integration evidence. | It does not establish discovery → routing → action. Inserting the row bypasses discovery and its handoff to routing. The proof cannot show that real discovery produces an eligible item with the fields/state needed for the downstream path. |
| B | Routing → action, conditional on the existing account and supplied item being valid prerequisites. Using prerequisites does not invalidate a proof whose claim starts at routing. | Discovery and account creation are outside its claim, not missing steps within it. The packet supplies no concrete trace or assertion artifacts for independent verification; those would be needed to audit the claimed routing/action result. |

```text
Corrected plan for A: 1 Keep the current proof relabeled routing → action with manually inserted row explicit. 2 Prepare account and item at input boundary of real discovery rather than inserting discovery output. 3 Run real discovery path, capture production output consumed by routing. 4 Let output proceed through real routing/adapter/action without manual bridge. 5 Correlate input/discovered item/routing decision/observed action one continuous chain. Unresolved setup: packet does not identify discovery input source/trigger/output contract/action-success observable; identify before executable test. Narrower evidence remains useful.
```

## PA3 current

Reported worker Task/session ID: `ses_ec927e26cffe4iVZ1MYOd2tHSI`. PA3 launch position 2, repetition 1. Reported read: `evaluations/selective-enrichment/baselines/current/product-acceptance/SKILL.md`. Coordinator-provided representation, potentially condensed:

```text
A supported given inserted row real router/adapter reaches action, supports routing → action. Gap bypasses discovery/handoff; cannot prove discovery creates required state; full remains unproven, retain downstream. B supported existing account/item real routing/action; legitimate prerequisites. Gaps account setup/discovery integration outside scope not defects. Correct A: identify agreed criterion/meaningful entry exact expected action unresolved; retain seeded routing proof; prepare account/source without inserting discovery result, controlled external fixture only if not replacing behavior; enter real discovery boundary exercising discovery/handoff/router/adapter/action; link discovered and routed item to meaningful action, observe failure behavior required by criterion; full proven only with evidence. Ref reported read baselines/current/product-acceptance/SKILL.md.
```

## PA3 older-portable

Reported worker Task/session ID: `ses_ec927e229ffem4fdeGVYY7mCpu`. PA3 launch position 3, repetition 1. Reported read: `evaluations/selective-enrichment/baselines/older-portable/product-acceptance/SKILL.md`. Coordinator-provided representation, potentially condensed:

```text
A given inserted discovered row real router/adapter process and produce observed action, retain routing-action. Gap inserted output substitutes discovery/handoff, discovery behavior/provenance/output compatibility unproven. 'The broader claim fails; the narrower evidence remains useful.' B existing account/item legitimate for routing-action; creation/discovery outside claim, broader needs evidence. Formal acceptance linked to action criteria not supplied. Correct A boundary identify actual discovery entry and mandatory stages; prerequisites account/config but not produced output; real entry/discovery-produced state/router/adapter without injection; assert same-item input/state/decision/action, not internal success; retain downstream diagnosis test. Missing exact discovery path/action criteria/promised recovery resolve before assertions. Ref reported baselines/older-portable/product-acceptance/SKILL.md.
```

## PA3 repaired

Reported worker Task/session ID: `ses_ec927e20dffe1dXMWBJDRXoNRT`. PA3 launch position 4, repetition 1. Reported reads: `skills/product-acceptance/SKILL.md` and `skills/product-acceptance/references/proof-and-example.md`. Coordinator-provided representation, potentially condensed:

```text
A real routing/adapter observed action retain narrower, full UNPROVEN 'not necessarily failed', fixture supplied output discovery should produce, downstream cannot fix provenance. B real routing-action prerequisite legit, supplied account supports narrow PASS. No creation/discovery proof required, generalization unsupported, missing build/config/run-links/external dependency details proof-record gaps not demonstrated defects. Correct A plan not executed: supported entry→real discovery→real persistence/transport→router→adapter→observed action; isolated state/static prerequisites no discovered rows; representative discovery inputs true external service may substitute preserving semantics not product-owned; real entry trace same-run item and expected action not queued row; record build/config/run/provenance/expected-observed/evidence, recovery only agreed. Keep narrower evidence full UNPROVEN, exact entry/action/substitutions specification needed. Ref reported current skills/product-acceptance/SKILL.md AND references/proof-and-example.md.
```

## WD5 repaired

Reported worker Task/session ID: `ses_ec9272528ffee2sRjC67liICAc`. WD5 launch position 1, repetition 1. Reported read: `skills/work-decomposition/SKILL.md` only. Coordinator-provided representation, potentially condensed:

```text
Parallel preparation one integrator; separate independent settings groups. A/B private worktree patches base tested revision, no direct common writes, no semantic dependency. Docs independent no settings dependency established. Integrator sole publisher common configuration depends both patches, owns combined proof, may belong existing group. Re-read current shared file reconcile both narrow patches preserve intervening changes not replace stale full snapshots. Combined diff both settings unrelated preservation; stale-base tests insufficient. Single-publisher protocol not host lock. Prefer per-group/run DB names if supported else serialize setup/reset→tests→cleanup including all lifecycle. Record revision/database/results and combined verified publication. Worktree/naming/commands unverified; if isolation unavailable parallel analysis ordered edits with re-read; serialize tests unless isolation confirmed, no plugins. Ref reported only repaired SKILL.md.
```

## WD5 older-portable

Reported worker Task/session ID: `ses_ec9272508ffetSUgbchTbUho4W`. WD5 launch position 2, repetition 1. Reported read: `evaluations/selective-enrichment/baselines/older-portable/work-decomposition/SKILL.md`. Coordinator-provided representation, potentially condensed:

```text
Parallel prep single writer serialized DB tests. A/B separate semantically independent, isolate checkout/private draft deliver baseline setting patch no shared publication. Integrator sole publisher after ready patches combines. DB tests sequential combined config exclusive setup/execution/teardown; prior releases database then next. Docs independent. Integrator current read setting changes not stale whole-file snapshots, reconcile changed baseline preserve unrelated; both survive. Single writer coordination not lock all writers honor else unresolved. Test serialize all consumers including cleanup baseline reset exact revision evidence; DB-independent checks concurrent. Need settings/commands/additional writers/database consumers/reset, unique names may later permit parallel not established. Ref older-portable SKILL.md.
```

## WD5 current

Reported worker Task/session ID: `ses_ec92724f0ffeH4FBl9N5BuzKBi`. WD5 launch position 3, repetition 1. Reported read: `evaluations/selective-enrichment/baselines/current/work-decomposition/SKILL.md`. Coordinator-provided representation, potentially condensed:

```text
Explicitly says reference parallel advice assumes runtime locks but host lacks guarantee. A/B isolated config copies focused patches base, development alongside docs; tests exclusive DB. Docs independent local checks final delivery. Integrator sole canonical publisher waits patches validates combined before publish. Sole writer no plugin/implicit lock, read current check baseline apply both no full snapshots preserve unrelated; if changes re-read reconcile. Exclusive DB windows include setup/execution/background/cleanup baseline reset log config/revision/DB lifecycle. Combined tests separate passing insufficient. Need isolation/control writers/users/reset/tests, unique names could remove serialization not established; independent development/docs can continue. Ref current baseline SKILL.md.
```

## WD5 no-skill

Reported worker Task/session ID: `ses_ec92724aaffe30Qopbo2Lby1AD`. WD5 launch position 4, repetition 1. Reported practitioner reads: none. Coordinator-provided representation, potentially condensed:

```text
Parallel three groups preparation/publication distinct no canonical competing writes. A/B isolated checkout/workspace base intended setting delta no dependencies. Docs isolated publish independently no conflict. One integrator applies both to latest canonical validates combined waits patches. Combined verification waits integration. Setting deltas not stale whole-file replacements integrator sole rereads preserves unrelated explicit key/semantic interactions textual clean insufficient. Without workspace A/B proposals parallel only integrator edits. Per-group/run temporary DB names ownership setup/cleanup log revision/database. If naming fixed serialize DB tests reset baseline before next; docs/preparation parallel integrated proof needed. Need isolation, naming, reset, cross-field constraints despite stated independence, doesn't block isolated preparation/docs. No plugin.
```
