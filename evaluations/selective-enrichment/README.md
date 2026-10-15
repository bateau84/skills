# Portable Selective-Enrichment Evaluation

**Status: limited two-case pilot executed and independently assessed; full comparison remains incomplete.** The main host supplied eight fresh-worker first-attempt representations for PA3 and WD5 across four variants; the independent assessment scored every supplied representation 8/8. This ceiling result does not establish repaired superiority, equivalence, or general effectiveness. The remaining 14 of 16 cases, discovery, companion experiments, and application E2E were not run; cost was not observed. See the retained evidence and its controls/representation limits below. Fixtures and local structural checks are not behavioral evaluation results. This protocol needs only a model/session, supplied files, and a human or available evaluator; no private host tools, named agents, package installation, or mandatory harness.

## Question and cases

Does selectively restored methodology improve first-attempt acceptance/decomposition decisions, without new blockers or lost portability?

- [Acceptance cases PA1–PA9](../../skills/product-acceptance/evals/cases.md)
- [Decomposition cases WD1–WD7](../../skills/work-decomposition/evals/cases.md)
- [Baseline identities and adaptation provenance](PROVENANCE.md)
- [Limited pilot results](PILOT-RESULTS-2026-10-13.md) and [received artifact representations](PILOT-ARTIFACTS-2026-10-13.md): historical assessed inputs/results, not complete raw child transcripts.
- [Prior capability assessment](CAPABILITY-ASSESSMENT-2026-10-13.md): preserved earlier session limitation, superseded only as to the later availability of pilot artifacts.

The standalone skill packages contain their own short case-execution instructions and source lineage. This collection-level protocol and preserved baselines are optional maintenance/comparison resources, not dependencies of copying either skill directory alone.

These are realistic decision/artifact tasks with supplied evidence packets. Assess the produced proof plans/findings/work groups, not whether the participant recites the skill. They are not executable application E2E fixtures. A participant may assess supplied run facts but must not claim to have run that product. Additional application execution requires a real product, authorized isolated environment, and recorded observations.

## Four matched variants

| Variant | Explicit practitioner context |
| --- | --- |
| no-skill | No acceptance/decomposition skill or companion text. |
| current | Frozen pre-enrichment `baselines/current/<skill>/SKILL.md`. |
| older-portable | `baselines/older-portable/<skill>/SKILL.md`: a documented portable adaptation, not the original runtime-bound source. |
| repaired | Current project `skills/<skill>/SKILL.md` and its directly linked practitioner references as requested. |

Freeze and hash repaired files before trials. Baseline hashes are recorded in provenance; never silently refresh `current` from repaired text. Keep baseline copies out of installed/discovery skill catalogs. Baseline source identity is not the current repository's HEAD alone: the starting skills already contained uncommitted portability work.

The historical `SOURCE-IDENTITIES-2026-10-13.sha256` identifies the pilot-era bytes. Later packaging repairs change active SKILL/case/protocol identities, **not** those historical pilot inputs/results. Preserve that manifest and all baselines unchanged; record later revision identities separately rather than overwriting the historical freeze or applying its pilot scores to the new revision. A full historical-manifest check against the repaired checkout will report these intentional differences.

## Explicit loading is not discovery

The primary test measures behavior **after explicit loading**. Supply the chosen SKILL body before the same case prompt (or read it into a fresh session and record that load). Permit practitioner references for that variant only. Do not supply companions in the primary trial: it must test whether essential decisions exist in practitioner guidance. Allow the same read/tool capability and same instruction for reference loading in every variant; differing authored reference availability is part of the skill treatment. Log actual loads and their cost where observed.

For manual sessions, provide the selected body and requested reference contents as messages; this avoids accidental repository-wide exposure. The no-skill session receives no such material. With tool-capable runners, isolate or restrict visible materials to the packet and selected variant. Never expose other variants, evaluator observations, examples of expected answers from other trials, eval files, or this protocol's rubric to the participant. Practitioner links to evaluation/provenance are for maintainers, **not trial input**.

Optionally test companion activities separately: use identical produced candidate artifacts in fresh sessions, supply the variant's SKILL plus ASSESSMENT for conformance; then, separately, SKILL plus QA for residual-confidence work. Record these as different experiments, not evidence of first-attempt practitioner performance. The older source combined those activities; its adaptation explicitly separates them.

Discovery is an optional **different** experiment: show a fixed mixed skill catalog containing only descriptions (one variant at a time) and realistic requests/paraphrases, ask which skill if any to load, and record selections and false positives/negatives. Do not force the intended skill to load and call that successful discovery. If following selection with task execution, report both stages separately. No-skill has no candidate skill; compare it for task performance, not retrieval recall.

## Controlled execution

1. Verify preserved baseline hashes; record repaired hashes, model exact identifier/version, tools and permissions, common instructions, sampling settings when available, context limits, and correction budget. Set these before looking at results. Record any unavailable controls.
2. Extract only one case's **Prompt** verbatim and the common instruction below. Keep its evaluator observations withheld. Each variant gets identical prompt/evidence, model, tools, permissions, common instructions and budget; only skill context differs. Do not include case names/traps or previous outputs unless they are part of the agreed identical input.
3. Start a fresh session per case/variant/repetition. No carry-over memory, cached answers, or correction history. Randomize/counterbalance variant order; record it. Use the same repetition count for each variant (prefer multiple runs if resources allow; a single run is exploratory).
4. Capture first submitted artifact and tool/load trace before feedback. For these packets, a text proof record or group table is the artifact; for added repository trials inspect actual output bytes/actions, not statements that edits/checks happened.
5. Judge blind to variant where possible using case-specific observations plus the rubric below. Cite artifact passages/actions. Accept alternative valid groupings/proofs, not a required template or exact wording.
6. If measuring correction effort, use the same predeclared budget (e.g. up to two rounds) and feedback policy: state each missed case-fact defect without providing a rewritten solution. Preserve all rounds. Score first attempt and final separately; if still wrong at budget exhaustion, report that. Do not repeatedly coach one variant while leaving others uncorrected.
7. Record limits, counts and observed cost; summarize matched per-case differences before any aggregate. Report “not run” for absent trials and “not observed” for cost/control data you lack. Do not extrapolate from a few cases to universal quality.

**Common instruction (same for all variants):**

> Work from the supplied task and evidence packet within its stated scope. Produce the requested practical artifact and rationale. Treat supplied facts as evidence for this decision exercise, not as actions you performed. State missing evidence and unresolved decisions precisely; continue independent work where possible. Use available reference material when useful. Do not invent requirements, tool execution, or results.

## Outcome scoring, not document-length scoring

For each case, score four dimensions **0 / 1 / 2** (0 = wrong/missing, 1 = partial/actionable gaps, 2 = sufficient first-attempt work):

| Dimension | Observable basis |
| --- | --- |
| Decision/outcome correctness | Correct claim verdict or coherent merge/separate/coordination choice, grounded in case facts. |
| Preserved obligations and defect detection | Identifies the case's load-bearing defect/guarantee and preserves narrower legitimate evidence or work. |
| Actionable proof/handoff | Concrete path, provenance, fidelity, assertion or group surface/dependency/proof ownership as relevant; not merely advice to “test/integrate.” |
| Proportionality and authority | Avoids unnecessary live providers, E2E ceremony, all-work serialization, invented semantics, named-role/plugin dependence or blocked ordinary realization. |

Alongside the 0–8 profile, record **missed load-bearing defects** and **unnecessary blockers** by type/count, **correction rounds to acceptable artifact**, unresolved failures, and **cost where observed** (input/output/cached tokens, monetary cost, wall time, reference/tool calls; identify which were available). Do not score word count or length as quality. Token cost can be a trade-off, not proof that shorter text is better.

A total does not wash out a fatal error: separately flag full-journey PASS through a product-owned mock or injected upstream state; an unexecuted proof called PASS; a materially lost obligation/safety boundary; invented product meaning; or unsafe automatic overlap assumptions. Also flag overblocking near misses: rejecting legitimate external fakes/static prerequisites/API-only proof, demanding new E2E for a local patch, or forbidding all parallelism.

## Minimal result record

```text
Case / activity / variant / repetition / order:
Model/settings/tools/common-instruction identity:
Skill + reference hashes and actual loads (or none):
Input/evidence packet identity; permissions and budget:
First artifact and trace location:
Dimension scores + cited artifact evidence:
Missed defects; unnecessary blockers; fatal errors:
Correction feedback/artifacts; rounds used; final scores/unresolved gaps:
Observed token/cost/time/tool data (or not observed):
Judge/blinding; limitations/deviations; status (executed/not run):
```

Store outputs under a project-selected results directory or outside the checkout as authorized; this protocol does not authorize writes to other people's files, staging, commits, or provider usage. A blank record or fixture inventory is never a run result.
