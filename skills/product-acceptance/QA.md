# Product Acceptance — Residual-Confidence QA

Adversarial validation for any agent. Assume competent production and conformance review; attack residual false confidence without inventing new requirements.

## QA criteria

- Construct the easiest broken product that could still pass the apparently sound scenario set: disconnected write/read paths, a demo fallback, or a worker that never resumes. Identify the accepted claim it would violate.
- Challenge shared assumptions: all proofs may use the same forgiving external fake, authenticated session, initialized database, dev proxy, or cached asset. Change one claim-relevant assumption and seek independent evidence.
- Probe provenance that looks legitimate but is correlated: a prior run may have populated the read result; a reset may leave queue or cache state; a fixture may already contain the expected migration output.
- Seek semantic mismatches hidden by a reasonable fake: quota at a later page, duplicate delivery after a timeout, or a failure after an external side effect. Use only perturbations relevant to accepted promises; do not invent provider guarantees.
- Ask whether final shipping packaging/flags select a different adapter, route, schema, or fallback than the reviewed proof. Seek a representative run of that composition rather than trusting labels.
- Inspect whether assertions could remain green when the human cannot understand the result or resume the agreed journey. Functional and experience evidence can share the same blind spot.

Report the counterexample, affected claim, evidence, and remaining uncertainty. Extra adversarial cases do not become new product requirements by being suggested.

## QA depth

Increase QA depth where a shared wrong assumption could survive both competent production and normal review.
