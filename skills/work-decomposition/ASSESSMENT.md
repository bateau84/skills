# Work Decomposition Assessment

Review whether the proposed tasks can be implemented and integrated against accepted outcomes without losing shared meaning.

## Review criteria

- Boundaries follow coherent capabilities/modules, not file counts.
- Shared requirements and interface semantics are accepted or explicit unresolved blockers before dependent parallel work.
- Dependencies reflect actual build, meaning, safety and integration order; independent work is not serialized artificially.
- Overlapping files and shared documentation have an explicit coordination owner; never assume automatic runtime locking.
- Cross-boundary integration and end-to-end verification have assigned responsibility.
- Each task communicates its expected outcome, relevant authority, constraints and testable acceptance without inventing semantic decisions.
- No required work or acceptance responsibility remains unowned between tasks.
- Implementation tasks cannot silently rewrite accepted authority; necessary documentation changes have an authorized owner.
- In a planning-only review, precise executable file scopes may be deferred, but ownership and shared contracts must be sufficiently clear.

## Review depth

Scale with coupling, parallelism, material risk, and how costly integration failure would be.
