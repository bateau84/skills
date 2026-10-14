# Product Acceptance — Older Portable QA

The original assessment's adversarial subsection, separated without changing its methodological intent:

Try to create false-green acceptance: replace upstream state with fixtures, run stale builds, mock product services, assert only HTTP 200, bypass the human surface, weaken an external fake, or choose only happy paths.

Do not accept mandatory product-owned mocks/fallbacks, skipped upstream surfaces, hand-injected behavior state, backend-only human-journey evidence, frontend mock composition evidence, stale/non-shipping composition, shallow assertions, or missing promised failure/recovery evidence.

Do not reject deterministic external fakes or narrower local mock tests solely because they are simulated. Representative composition proof is not exhaustive duplication of all lower-level tests.
