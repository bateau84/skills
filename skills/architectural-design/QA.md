# architectural-design Quality Assurance

Adversarial validation for any agent. Assume competent production and conformance review; attack residual false confidence without inventing new requirements.

## QA criteria

- Attack interactions between individually sound components: partial failure, restart, concurrency, retry, cancellation, backpressure, stale state, and mixed old/new state.
- Search for silent false-positive/false-negative paths where the architecture reports success, safety, freshness, or authorization without the claimed invariant actually holding.
- Look for shared assumptions about ordering, time, identity, durability, ownership, or trust that no component truly enforces.
- Remove, delay, duplicate, or degrade one dependency and ask whether containment and recovery still match accepted outcomes.
- Challenge a structural option that claims to satisfy a Quality Scenario only under nominal conditions or by silently assuming an unaccepted recovery/latency target. Re-run the relevant stimulus and compare what each alternative actually proves.
- Attack incomplete inverse paths: write without reliable read, acquire without release, publish without reconcile, dispatch without cancel, create without safe removal.
- Search for authority/evidence laundering across persistence, process, network, plugin/tool/MCP, or privilege boundaries.
- Challenge whether a materially simpler architecture or omitted viable option changes the tradeoff frontier; do not demand complexity merely for hypothetical threats.
- Test whether the claimed invariant survives real assembled composition rather than only component-level verification.
- Trace a representative change through the proposed owners and callers. Could the apparent simplification hide unrelated policies in one component, transfer coordination to another caller, or depend on a future capability that may never arrive? Include the transition and migration costs before accepting the claimed improvement.

## QA depth

Increase QA depth where a shared wrong assumption could survive both competent production and normal review.
