# infrastructure Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic simulates partial apply, provider timeout after remote success, concurrent operator, region/AZ dependency failure, quota exhaustion, drift, rollback after state/schema changed, and destroy/recreate of a stateful resource. Probe “plan is green” assumptions that ignore control-plane runtime behavior.

Block when accepted availability/data/security/authority guarantees can be violated, irreversible destruction/migration lacks controlled path, or target/state identity is ambiguous. Cost/style optimization is proportional unless tied to an accepted budget/SLO.

## QA depth

Increase depth with destructive/stateful changes, IAM/secrets/network perimeter, cross-region/AZ design, control-plane eventual consistency, shared state/automation, cost blast radius, and rollback difficulty.
