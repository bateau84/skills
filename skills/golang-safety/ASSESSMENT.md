# golang-safety Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Review expected runtime/data/process correctness failures in the accepted usage and threat boundary. Do not expand a non-adversarial safety task into an unsolicited security audit; route adversarial exploitation/threat modeling to `golang-security` when relevant:

- untrusted sizes/counts/depths are bounded before allocation/iteration/recursion; integer conversion/overflow cannot turn validation into bypass/resource exhaustion;
- nil/index/type assertions/panics cannot be triggered by expected external data without controlled error handling;
- file/path/temp/process/network operations preserve intended root/permissions and avoid traversal/symlink/race/command-injection hazards;
- parsing/serialization limits protect against oversized/malformed/decompression-bomb input;
- `unsafe`, cgo, memory aliasing, atomics, and zero-copy techniques have an explicit necessity/invariant and targeted tests;
- resources/goroutines are bounded under the accepted workload and failure model;
- destructive operations identify target and fail safely under partial error/retry.
