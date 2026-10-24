# GitHub Issue — Reviewer Assessment

Review the **authored issue**, not the quality of the conversation it came from. Can a capable agent start from the issue without the original chat and pursue the correct outcome?

## Review criteria

1. **Ownership and unit of work:** The target repository and coherent outcome are grounded; unrelated ideas were not silently bundled, and connected dependent work was not separated without a contract.
2. **Decision fidelity:** Compare the issue to accepted user intent and durable sources. Rejected ideas, tentative proposals, optional examples, and agent recommendations were not promoted into MUST behavior.
3. **Current-state accuracy:** Asserted paths, behavior, dependencies, existing fixes, and related issues/PRs are verified where accessible, or clearly marked unverified.
4. **Cold-start completeness:** Problem, reason, outcome, relevant context, accepted scope/exclusions, constraints, and accessible source references let a fresh agent work without asking for the old transcript.
5. **Readiness and uncertainty:** Implementation, investigation or decision work is correctly distinguished. Blocking choices have an explicit owner/next decision, not false implementation acceptance criteria.
6. **Testable completion:** Acceptance checks reflect observable behavior or bounded findings, including regression/cross-boundary proof when material; they do not require one unapproved internal design.
7. **Proportionate detail:** The issue is self-contained without becoming an implementation plan, transcript dump, guessed file inventory, or new workflow policy.
8. **Publication discipline:** Sensitive information is removed; requested publication/metadata is grounded; duplication is checked where possible; published title/body/URL are verified, with failures stated honestly.

## Evidence boundary

A clear issue can still describe the wrong task. Readability alone is not evidence that decisions were preserved. A linked artifact is not enough if the future reader cannot access it. A checked acceptance box is not proof that implementation succeeded; this skill concerns issue authoring only.
