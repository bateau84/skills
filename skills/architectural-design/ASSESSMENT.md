# architectural-design Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

- Accepted obligations map to explicit components/boundaries without inventing product behavior; unresolved semantics remain unresolved.
- New machinery earns its total cost against a named obligation, demonstrated material risk, or concrete maintenance burden, and an adequate existing/simpler seam was not ignored.
- Genuine alternatives were developed before selection and compared on the same material forces; rejected options are not ceremonial strawmen.
- Data, control, authority, evidence, state ownership, lifecycle, and failure flows are coherent across boundaries.
- Load-bearing guarantees identify their preconditions, responsible boundary, enforcement mechanism, and verification point.
- Relevant input/state and operation coverage includes inverse paths and failure cases rather than only the happy path.
- Relevant failure lenses are covered, including silent wrong results, stale/corrupt state, interruption/retry/cancellation, concurrency, and dependency failure.
- Trust/security boundaries are explicit where authority, credentials, untrusted input, sensitive state, processes, or networks cross.
- Composition proof tests assembled behavior rather than only locally plausible components, and load-bearing verification is persisted when required.
- Public seams remain small enough that downstream implementation does not have to rediscover architecture.
- Structural preparation addresses an inspected difficulty or accepted upcoming change, with a direct baseline, bounded stopping point, whole-change cost, and preservation evidence. The claimed improvement names knowledge or coordination callers no longer need; conditional future value is not presented as an observed result.

## Review depth

Scale review depth with consequence, uncertainty, boundary count, and blast radius.
