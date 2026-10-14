---
name: skill-authoring
description: Author and maintain reusable, agent-neutral skills. Use when creating, porting, editing, auditing, or packaging SKILL.md files and supporting references. Not for agent role policy (use agent-file-authoring).
---

# Skill Authoring

Skills are on-demand methodology. They do not create permissions, orchestration, approval stages, or evidence merely by being loaded. Any agent may use them within the task and host instructions.

## Three-layer skill contract

A skill directory may contain three distinct context layers:

- `SKILL.md` — **required** practitioner methodology: how to do the work well.
- `ASSESSMENT.md` — **optional** review methodology: how to check conformance and domain correctness.
- `QA.md` — **optional** adversarial-validation methodology: how to falsify confidence after competent production and review.

The three files must not become increasingly severe copies of the same checklist.

### SKILL.md ownership

Keep producer/practitioner method here.

Keep optional conformance rubrics and adversarial attack plans in their companions rather than mixing them into practitioner guidance. Keep the checks and failure handling needed to produce sound ordinary work in `SKILL.md`; moving them into an optional companion would make the practitioner path incomplete.

### ASSESSMENT.md ownership

Create it only when the domain has meaningful skill-specific review expertise.

It must answer: **Did this work satisfy its accepted inputs and domain obligations?**

Keep it bounded and evidence-oriented. Put broad red-teaming and systemic confidence attacks in `QA.md`.

### QA.md ownership

Create it only when apparently competent reviewed work can still be materially wrong because of hidden, correlated, systemic, compositional, adversarial, recovery, security, or false-confidence failure modes.

It must answer: **How could this still be wrong even though it looks correct and passed normal review?**

QA may attack assumptions and evidence quality; it does not establish new product or architecture decisions or require redesign as a substitute for validation.

Absence of either companion file is valid. Do not generate boilerplate merely for symmetry.

The same agent may use these perspectives, but doing so is self-review, not automatically independent review. Independence depends on the actual reviewer, context, and evidence, not the filename or a change of persona.

## Create or port a skill

When discovery, structure, behavioral guidance, or eval design is load-bearing, read [Portable authoring principles](references/authoring-principles.md) before editing. Evaluation scenarios may be exercised manually or through available host tooling; no particular harness is required.

1. **Start from the job, not the document.** Define what the skill enables, the concrete situations that should retrieve it, nearby sibling territory, and what observable failure or quality gap justifies the skill.
2. **Treat the description as a retrieval contract.** Lead with the capability; include concrete `Use when` verbs, filenames, tools, symptoms, or situations; add a narrow `Not for ...` sibling pointer where territory overlaps. Do not turn the description into a miniature workflow. When editing a proven description, dropped trigger anchors are a reason to re-test discovery, not proof of causality.
3. **Choose a shape that fits the work.** Technique, reference, pattern-recognition, and discipline/governance skills need different bodies. Do not force every skill into one universal section template.
4. **Keep the load-bearing normal path in `SKILL.md`.** Move bulky schemas, API tables, examples, or specialized variants to direct references only when the core method remains understandable without loading them. Avoid reference chains whose real answer is several hops away.
5. **Match instruction specificity to risk.** Low-risk work with many valid approaches should state goals, constraints, and quality bars. Preferred patterns may use ordered guidance. Fragile, destructive, security-sensitive, or protocol-bound work should use exact sequences and fail-closed conditions where needed.
6. **Prefer durable method over volatile facts.** Encode procedures, heuristics, interpretation rules, invariants, and decision structure. Fast-changing environment facts such as current deployments, owners, incidents, endpoints, versions, or live metrics should come from authoritative runtime sources unless the skill is explicitly a maintained reference and freshness is part of its contract.
7. **Design for composition.** A skill should be independently useful while avoiding ownership that belongs to siblings. Split monoliths when several reusable capabilities can be selected separately; do not duplicate shared methodology merely to make one skill self-contained.
8. **Ground behavioral rules in observed failure.** For a new discipline-enforcing skill, obtain realistic RED evidence before drafting when practical: show the concrete failure without the candidate. For updates, a user counterexample, review finding, production incident, or prior eval failure can supply the RED input. Never invent a baseline result.
9. Put reusable practitioner method in `SKILL.md`; decide independently whether domain-specific assessment and adversarial validation add real discriminating value.
10. Keep terminology agent-neutral. Use activity names such as design, implementation, review, and validation rather than assuming named agents.
11. Treat companion files as optional perspectives any agent can use, not role-exclusive permissions.
12. Keep orchestration and execution policy in the host or project instructions rather than embedding a workflow engine in a skill.
13. Replace framework-specific routing, tool calls, fixed namespaces, and approval choreography with portable methods. State real external dependencies and provide a file-based fallback when appropriate. Audit what a practitioner must actually do, not just vocabulary: trace linked references and adjacent guidance for hidden loader, service, lock, snapshot, or agent assumptions.
14. Make verification concrete. Evals should resemble real work, name the trap being prevented, include positive and negative expectations, and prefer produced artifacts or observed actions over transcript self-report when those are the claimed outputs.
15. Preserve licenses and attribution for copied third-party material. Curate sources deliberately: keep the generalizable principle, record meaningful lineage, and discard obsolete workflow mechanics rather than copying them for historical symmetry.
16. Keep external dependencies explicit; do not assume a CLI/service is installed.
17. If a skill changes behavioral decisions rather than merely technical method, add or update a realistic eval for that decision boundary. Prefer real incidents and observed work as scenario sources. Record what was actually exercised; do not imply an evaluation ran because a fixture exists.

## Companion quality tests

A useful `ASSESSMENT.md` should fail the Rename Test: renaming the skill should make the criteria obviously wrong for another domain. It should contain domain-specific evidence, boundary, negative-space, and false-confidence checks rather than "check correctness/tests/edge cases."

A useful `QA.md` should expose failure modes that a competent author **and** competent reviewer could plausibly share. If it merely repeats `ASSESSMENT.md` with harsher wording, delete it.

## Port classification

- **Copy/adapt:** reusable domain methodology independent of the source runtime.
- **Rewrite:** useful methodology entangled with old agent/routing/gate semantics.
- **Defer:** niche package/persona/external integration that is not part of the trusted baseline.
- **Reject:** content whose primary purpose bypasses host permissions or duplicates a private runtime rather than teaching reusable method.

A good skill answers: "How should a practitioner do this work well?"
Its companions explain normal review and attacks on residual confidence. None requires a particular agent hierarchy or grants permission to bypass host constraints.

## Portable references

- [Portable authoring principles](references/authoring-principles.md) — discovery/retrieval, progressive disclosure, skill shapes, risk-matched specificity, composability, durable-vs-volatile knowledge, RED grounding, source curation, and eval design.
- Local `evals/` fixtures, when present, describe realistic requests and expected observations; adapt execution to the available environment.
