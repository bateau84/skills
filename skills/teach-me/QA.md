# Teach Me — Quality Assurance

Challenge explanations that passed ordinary assessment. A concise, engaging tutorial can still leave the learner with a rule that fails in real work. Probe the **learner's likely inference**, not only the literal wording.

## Adversarial probes

1. **Analogy breaks at a consequential boundary.** Take an apparently good analogy and construct the nearest realistic case where it stops working. For a mutex, test lock ordering and fairness; for an event loop, test blocking synchronous work; for a cache, test stale state and invalidation. Did the answer imply a guarantee the system does not provide?
2. **A hidden prerequisite survives the checkpoint.** Have the learner apply the explanation to a slightly different example. Can they do so without a prerequisite the tutor never named? A plausible "yes, that makes sense" is not proof that the concept transferred.
3. **Version-specific example fails outside the toy case.** Cross-check a consequential API, release feature, or command against primary documentation and actual platform assumptions. A correct generic explanation does not verify a claimed new-version behavior.
4. **Session and authority confusion.** Start a lesson, pause it, resume with changed context, then end it. Look for fabricated memory continuity, unintended memory writes, accidental global slash-command assumptions, or a tutor persona that overrides a later implementation request.
5. **Risk concealed by pedagogy.** Apply an oversimplified tutorial to a production or security-sensitive setting. Look for an example that teaches a safe intuition while quietly omitting a necessary constraint or encourages a destructive action as if it were a harmless learning exercise.

## How to report

Choose one realistic probe relevant to the user's topic and check the response or executable example when possible. Distinguish **observed misinformation**, **plausible untested learner confusion**, and **verified correctness within stated scope**. Report the smallest counterexample, why the learner could infer the wrong rule, and the minimal clarification that repairs the lesson.

Do not demand extra jargon, a longer lecture, mandatory research tools, or independent reviewer personas as a substitute for testing the mental model. A QA file alone is not an independent review.
