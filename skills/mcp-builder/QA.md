# mcp-builder Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic treats every tool argument and returned resource text as attacker-controlled. Attempt tool confusion, arbitrary URL/path access, cross-tenant ID substitution, retry after timeout with unknown remote outcome, pagination truncation, prompt-injected tool/resource content, and oversized result/error leakage.

Block when model-visible affordances can cause authority escalation, secret leakage, cross-tenant access, duplicate/destructive side effects, or systematically misleading partial results. Coverage breadth alone is never proof of MCP quality.

## QA depth

Increase depth with mutation/destructive tools, credentials, arbitrary URLs/files, multi-tenancy, open-world APIs, retry uncertainty, result volume, and autonomous model use.
