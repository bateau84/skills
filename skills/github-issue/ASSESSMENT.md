# GitHub Issue — Reviewer Assessment

Review a GitHub issue operation for correctness of **tracking state**, not merely the quality of its wording.

## Review criteria

1. **Correct target and record:** Owner/repo, issue identity and actual current body/state were verified, and likely duplicate or completed work was checked before creating a new issue.
2. **Intent preserved:** A provided work handoff or existing issue contract was represented without inventing acceptance, owner, priority or required architecture.
3. **Human-readable issue:** Title and body explain the need, desired result, limits and observable checks in everyday words. A person can compare these against the accepted request without deciphering internal jargon. Exact technical details remain correct throughout the body, not just in its summary.
4. **Right tracking construct:** Checkboxes, sub-issues, blockers, organization issue type, repository labels/milestones, organization issue fields, Project membership and local Project fields remain distinct; hierarchy is not treated as sequencing.
5. **Meaningful granularity:** Children have their own outcome and acceptance; trivial task bullets have not been turned into a swarm of issues or a hierarchy for its own sake.
6. **Metadata grounded:** Types, labels, assignees, milestones, Projects and fields exist, have an agreed purpose, a supported write path and correct audience visibility. No invented owner, priority, deadline, effort, or `agent:ready`-style approval.
7. **Scope and state integrity:** Shared organization issue fields are not confused with similarly named Project custom fields. Project Status is distinct from issue state, and configured automation is considered. Existing checked boxes, discussion and concurrent edits survive body changes.
8. **Lifecycle truthful:** Progress, closure and reopening follow evidence and project rules; a linked PR or a closed parent does not silently certify unfinished child work.
9. **Side-effect and security discipline:** Mutations were actually requested and permitted; no sensitive information was published; unsupported native relationships were not represented as successfully applied.
10. **Verification:** Changed issue fields, type, milestone, Project membership, Project-local values, body, and relationships were re-read where supported; partial results are not presented as complete.

## Evidence limits

An issue that is correctly labeled, linked and closed may still contain the wrong requirements. Use `work-handoff` assessment if the issue was constructed from a conversation and intent fidelity is in doubt.
