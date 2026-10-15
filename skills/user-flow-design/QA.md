# user-flow-design Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic starts from awkward but plausible states: missing permission, stale state, invalid input after partial progress, cancellation between steps, repeated retry, role/surface handoff, and failure during recovery. Search for orphan states, cycles without progress, dead-end errors, and implicit jumps.

Block when a required scenario has no complete realizable path, an error/recovery branch cannot reach a valid exit/rejoin, entry assumptions are unsupported and load-bearing, or completion depends on undefined product semantics/capability.

Do not block merely for absent branches that cannot occur in the accepted system.

## QA depth

Increase depth with branch/state count, asynchronous steps, retries, role/surface handoffs, persistence across time, destructive consequence, and uncertainty of entry conditions.
