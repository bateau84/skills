# Ubiquitous Language — Quality Assurance

Adversarially challenge a vocabulary that has passed ordinary `ASSESSMENT.md` review. Assume the definitions are clear, correctly scoped, and traceable on their own. Ask whether **shared assumptions, relationships, and real consumers** could still make the vocabulary misleading. This is not another glossary checklist, a product decision gate, or permission to rename contracts.

## Residual-confidence attacks

1. **Correlated evidence mistaken for consensus.** Trace several agreeing glossaries, requirements, or agent summaries back to their original sources. Were they independently accepted, or copied from one unverified interpretation? Challenge a claimed agreement with an independently sourced domain example or accepted decision. Agreement among copies is not additional evidence.
2. **Meaning lost at a bounded-context crossing.** Follow a real entity or event across at least two contexts. Test one-to-many, missing, and ambiguous mappings rather than assuming equal names imply equal identities. Verify that translation preserves each context's meaning; do not force either context to adopt the other's term.
3. **Transitive contradiction between individually sound terms.** Combine lifecycle terms, qualifiers, and rules into one realistic end-to-end example. Test whether the resulting classification violates an accepted invariant even though each local definition passed review. Follow relationships and implications, not just each glossary entry.
4. **Stale consumers behind a clean vocabulary.** Start with an accepted change in meaning, then trace a representative normal path and failure path through a downstream consumer (such as a service, API client, event handler, stored record, report, or agent instruction). Look for decisions still made using the old meaning. Distinguish intentional compatibility aliases from consumers that misclassify behavior.
5. **Historical meaning hidden by current labels.** When the vocabulary has changed, sample an old persisted record or event. Can a current reader correctly interpret its meaning at the time it was written? A consistent current glossary does not prove historical data or replay is safe.

## Concrete adversarial scenarios

Use a small subset relevant to the work, with actual source and consumer evidence where available:

- **False consensus:** Three design documents call a deployment `ready` after CI passes, but all three copied a draft note. An accepted release decision also requires security approval. Trace source lineage and test a CI-green build with missing approval. Do not treat repeated wording as independent acceptance.
- **Cross-context identity:** Identity defines `account` as an authenticated principal; Billing defines `account` as the invoice recipient. Walk through one principal managing two billing accounts and a transferred account. Check that IDs and events crossing the boundary identify the intended entity rather than assuming a one-to-one mapping.
- **Composed lifecycle rule:** `Completed` means execution ended, including failure; `Chargeable` is defined as completed; an accepted billing rule says failed executions must not be charged. Exercise a completed-but-failed run to expose the contradiction. Do not resolve the product rule by silently changing either definition.
- **Correct glossary, wrong behavior:** The approved meaning of `completed` is now “goal achieved,” while an event consumer still treats every terminal outcome as completed. Feed it a failed terminal event and inspect the actual classification. A glossary-only change must not be reported as an implemented migration.
- **Past and present conflict:** `Active` now means entitled to access, while an older stored `active=true` meant only “not suspended.” Replay an old record and inspect a current access check. Seek explicit versioning or translation evidence before asserting compatibility.

## Probe and evidence discipline

- Select **one high-consequence term or relationship** and one counterexample that the producer's own examples did not already exercise. Expand only if that probe exposes a broader failure mechanism.
- Trace the term from its accepted source through the relevant boundary to an observable consumer action or artifact. Where the original decision or consumer is unavailable, say exactly what remains unverified; do not manufacture a failure.
- Separate **confirmed semantic failure**, **plausible but untested risk**, and **unresolved domain decision**. Report the smallest reproducible counterexample, affected contexts/consumers, source evidence, and the impact on the confidence claim.
- Do not require global vocabulary uniformity, a repo-wide rename, or a new decision authority as the remedy. Compatibility or behavior changes belong to separately authorized work.

A QA finding is material when an apparently sound vocabulary causes, conceals, or cannot substantiate a consequential incorrect interpretation across boundaries, rules, consumers, or time. If the probes find no such counterexample, report the scoped evidence and its limits—not universal proof of consistency.
