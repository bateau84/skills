# terraform-module-testing Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic breaks the intended invariant while preserving the current assertion, injects a different expected failure, replaces real provider behavior with permissive mock values, and runs tests in parallel/reordered. Ask whether a green test can exist while the module’s accepted behavior is wrong.

Block when cited module-test evidence is non-discriminating or plan/mock evidence is used to claim real infrastructure behavior. More apply tests are not inherently better when plan tests prove the intended contract safely.

## QA depth

Increase depth with real-resource apply tests, state sharing/cross-run dependencies, provider mocks, destructive/costly infrastructure, version-specific features, and breadth of the module contract.
