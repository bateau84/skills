# architectural-decision Quality Assurance

Adversarial validation for any agent. Assume competent production and conformance review; attack residual false confidence without inventing new requirements.

## QA criteria

- Identify the strongest assumption shared by all compared alternatives and test whether it is actually true.
- Search for an omitted genuinely viable alternative that changes the tradeoff frontier rather than cosmetically renaming an option.
- Detect post-hoc option construction: signs that the selected choice was fixed first and alternatives were written only to justify it.
- Attack irreversible, migration-heavy, operational, or security consequences hidden by short-term implementation convenience.
- Ask what concrete evidence would make the chosen decision wrong, then check whether the proposed confirmation can actually observe it.
- Re-evaluate the choice under realistic scale, restart, partial failure, concurrency, compatibility, and adversarial conditions that fall inside accepted scope.
- Check whether the winning option depends on stronger product semantics, threat assumptions, or guarantees than accepted authority actually provides.
- Challenge new machinery that solves only hypothetical risk while a simpler option still satisfies accepted obligations.
- Remove or delay the future capability assumed to repay a refactor. Does the decision still acknowledge its actual costs and conditional value, or does a speculative forecast make every option appear to require the same investment? Challenge a claimed payoff measured only after preparation costs were excluded.

## QA depth

Increase QA depth where a shared wrong assumption could survive both competent production and normal review.
