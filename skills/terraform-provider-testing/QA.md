# terraform-provider-testing Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic breaks Read/update/import/destroy while leaving Create intact, returns unrelated expected error, leaves remote resource after test, introduces perpetual plan diff, and runs tests in parallel/reordered. Ask what provider defect could survive every cited check.

Block when acceptance tests can systematically false-pass on state convergence/lifecycle or cleanup is unsafe. Test helper style is non-blocking.

## QA depth

Increase depth with stateful/destructive resources, import/disappears, eventual consistency, replacement, parallel test execution, sweepers, ephemeral resources, and cost/privilege of real provider accounts.
