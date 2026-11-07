# Add timed-out job retry support

Implement retry support for jobs in state `timed_out` through all three existing
entry points. They follow the same attempt limit, successful state update,
diagnostic clearing and failed-save behavior as `failed` jobs.

Keep all existing signatures and behavior, including error precedence. For states
that are still ineligible, retain the existing `ValueError("job is not failed")`
message for compatibility even though it is no longer a complete description of
the allowed states. Internal restructuring is in scope. No other feature or
external dependency is requested.

Read the project requirements, make the actual code and test changes, run relevant
checks and update the accepted behavior in README.md. Leave a short HANDOFF.md
with useful decisions, evidence and remaining work. Report the observed result.
