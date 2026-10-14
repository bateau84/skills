# Baseline and Adaptation Provenance

Captured during selective enrichment on 2026-10-13. **No behavioral comparisons have been executed here.** Baselines are evaluation resources, not installed skills or updated product guidance.

## Frozen current baseline

Source checkout: `/home/bateau/git/bateau84/skills`, HEAD `31ad1ad06792ed6bc904fb3e8fab21cce698fe14`. The working tree already contained extensive uncommitted agent-neutral portability edits and the `skills/loom-learning` → `skills/learning` rename. HEAD is therefore not the pre-enrichment baseline content.

Before modifying either skill, all six starting working-tree files were copied using a file patch into `baselines/current/`. `diff -ru` against each starting directory returned no differences, and SHA-256 hashes matched. No original guidance was repaired inside this frozen baseline; the two incorrect file-lock claims intentionally remain as comparison inputs.

| Relative path under `baselines/current/` | SHA-256 |
| --- | --- |
| product-acceptance/SKILL.md | `2c337b2a76a9da9441534b3830cc7a33e6cea4b25384acac737187127e83be96` |
| product-acceptance/ASSESSMENT.md | `2f3a806e9ed07186a1d8c9266f7f86bc2f86f1a940f470693779415a78f7cbf4` |
| product-acceptance/QA.md | `0b6b9a8fd28e32f0d47b5bad497318b353294aaa28fca57c551c2462df0b6f07` |
| work-decomposition/SKILL.md | `c59d8f92911aa076543fa80b3356245e32dbdd8fcad2a492a858b735b11bcd11` |
| work-decomposition/ASSESSMENT.md | `989d6162c1a4bf8f65a5d222d4112b5ab414e4fc9892eaf934a3ecb080b19bd8` |
| work-decomposition/QA.md | `495a93c5e99d6266e1f4961ff7d47a9346fd6a4026b95ee5aeecf13fe91d51b7` |

## Original older source (read only, not the portable treatment)

Source checkout: `/home/bateau/git/Sea-Shell/mats-opencode-setup`; lineage `nrkno/mats-opencode-setup`; HEAD `3f26d834d84e4f24e14366864a9319f81201e6cb`. `git status --short -- skills/product-acceptance skills/work-decomposition` was empty at capture. Product-acceptance declared `license: MIT`, author Bateau, version 1.0.0. Work-decomposition declared version 1.2.0 and no separate license field; do not infer a new license for it.

| Original path (relative to old checkout) | SHA-256 |
| --- | --- |
| skills/product-acceptance/SKILL.md | `88a202e543b9b6967c76eadd77f94fa892ec8c25f671d0cdfa26047373fd504c` |
| skills/product-acceptance/ASSESSMENT.md | `1d4c084a3bdd6730000fa660cfba12f7ef5e20b546bc33c0b0554326f672fb32` |
| skills/product-acceptance/evals/evals.json | `f285046b3c8eabaf582f5024b638bcbc92921039a061ffbef1618a9443846d96` |
| skills/work-decomposition/SKILL.md | `2c9e7b190e1863a937e302dc1593fe19b578bb184db52a73893ba3e1681c64d2` |
| skills/work-decomposition/ASSESSMENT.md | `df1a64e24352b0dc43e8d8358f3185189f6ccc7e78996266494191a71450d3c4` |
| skills/work-decomposition/evals/evals.json | `862ffbaad6ad60b06df2a48214ab92bdb82f7eafb78d02f6062e7698d09f6718` |

The originals are not copied as active guidance and were not modified. The source revision/path/hash permits optional recovery and inspection; the comparison itself is portable without access to that checkout because the adapted baseline is included below. Do not describe its results as measurements of the verbatim original runtime-bound files.

## Included older-portable treatment

`baselines/older-portable/` is a manually adapted, self-contained comparison resource. It is **not a byte-for-byte original** and not merely a literal string-stripping operation. Runtime labels were replaced with accepted outcome/shared obligation/activity terms; paragraphs/lists were condensed without intentionally adding the repaired decisions. This editing is a comparison limitation, not evidence of improvement. Inspect the mapping when attributing a difference.

| Source sections | Adaptation |
| --- | --- |
| Acceptance SKILL modes and plan/prove/audit sections | Retained as task activities and portable proof/audit methods; removed named-role routing and shipping gate choreography. |
| Acceptance local evidence, product boundary, external fakes, scenario selection, provenance, failure semantics, template and YuHaul pattern | Retained, with lists/wording condensed and Anchor changed to accepted outcome. Removed unavailable `includes/aos-coherence.md` and fixed repository cross-links. |
| Acceptance ASSESSMENT review/adjudication/scaling | Review/scaling retained in ASSESSMENT; adversarial subsection separated into QA; no original standalone QA existed. Shipping fidelity remains in its original companion location. |
| Decomposition core/lenses/grouping/separation/output/failure boundaries | Retained, replacing fixed authority artifact names with portable terms. |
| Decomposition composition/task-manager seam | Recast as candidate analysis → risk/planning/acceptance relationship; removed mandatory load order, named task-manager, spoke/wave assignment and private policy dependencies. Preserved candidate-vs-final-plan distinction. |
| Decomposition ASSESSMENT review/adjudication/scaling | Review/scaling retained; adversarial subsection separated into QA; reader-aid rules condensed to underlying material-vs-editorial distinction. No original standalone QA existed. |

No host file-lock guarantee was added to the older-portable baseline. Nor were repaired stale-read procedures, detailed shipping/proof record additions, or the new cases injected into it. Practitioner-only trials deliberately do not load either version's assessment/QA; companion tests are separate.

| Relative path under `baselines/older-portable/` | SHA-256 |
| --- | --- |
| product-acceptance/SKILL.md | `2ed91e0f0477f848f30a117e750320c2d094f62c8a15a8696d91815fe33fd0ab` |
| product-acceptance/ASSESSMENT.md | `6198942a7f8fd5545055ccac7a36a40ff241ce9ed018e6114f9bbc71b1be9048` |
| product-acceptance/QA.md | `46d8742ff61c5629f92f70ff6bc5732f5d8d55525153cebc9e03bc698bbcc91d` |
| work-decomposition/SKILL.md | `0a59de929b04c0377a68d5a6d8f3601965dcdd9e084df95b95a157355dee95b1` |
| work-decomposition/ASSESSMENT.md | `226b5091195728a46dc5ceb60c650a74255ac966de1bddb4e7a1c6ab6d5f5a7f` |
| work-decomposition/QA.md | `f79c0ef3e782410be5383bc19b7b7245c44c66b53f1cd0c5c93139bf675ff167` |

## Repaired guidance and cases

Repaired practitioner guidance selectively brings the older boundary/provenance/external-fake/template/grouping methodology into the normal path, adds shipping fidelity from the older acceptance assessment, and corrects both unsupported lock guarantees. Examples remain directly linked depth, not hidden essential rules. Conformance and residual-confidence companions remain distinct and agent-neutral.

Case lineage:

- PA1–PA7 adapt old acceptance cases 1–7; PA7 also incorporates old case 8's quota/resume promise. Named agents and runtime authority labels were removed; supplied evidence packets and scoped statuses make observations assessable.
- PA8 extends the old shipping-fidelity/migration assessment finding. PA9 adds a paired boundary-scope control. PA2/PA3 include paired external-compatibility and static-prerequisite controls.
- WD1–WD4 adapt old decomposition cases 1–4. WD5/WD6 directly test the accepted unsupported-lock/stale-read/shared-state finding. WD7 tests grounded surface discovery and product-decision ownership.

These are adapted/synthetic cases grounded in source findings and user-accepted gaps, not new production incidents or baseline failures observed in this session. Repaired file hashes must be frozen at actual evaluation time; no performance claim follows from their presence.

## Local preparation evidence

The implementation session ran these structural checks, not model comparisons:

- Before enrichment, `diff -ru` of each starting skill directory against `baselines/current/<skill>` exited 0, and SHA-256 outputs matched all six current-baseline entries above.
- `git diff --check -- skills/product-acceptance skills/work-decomposition` exited 0. All 18 new evaluation/baseline/reference/case files were separately checked with `git diff --no-index --check /dev/null <file>`: no diagnostics; exit 1 represents the expected new-file difference, not a whitespace finding. The checking loop explicitly handled this exit convention and completed all 18 files.
- `rg -c` counts for case headings, `**Prompt:**`, and `**Evaluator observations:**` matched: acceptance 9 of each, decomposition 7 of each.
- Local Markdown links were enumerated with content search and manually resolved against the file inventory: practitioner examples/companions, sibling acceptance skill, case files, protocol, and provenance targets exist. This is a manual link check, not a Markdown-renderer or runtime test.
- Read-only repository search found the two incorrect lock claims in decomposition practitioner/assessment guidance; both were replaced in active guidance. Their unchanged frozen copies are intentionally retained for evaluation.

No staging, commit, push, package installation, old-source mutation, application execution, or behavioral evaluation was performed. The original older-source status/hash check is independent of the included manual portable adaptation. Outcome effectiveness, discovery performance, correction effort, and cost remain to be measured by the subsequent evaluator.
