# GitHub Issue — Reviewer Assessment

Review a GitHub issue operation for correctness of **tracking state**, not merely the quality of its wording.

## Review criteria

1. **Correct target and record:** Owner/repo, issue identity and actual current body/state were verified, and likely duplicate or completed work was checked before creating a new issue.
2. **Intent preserved:** A provided work handoff or existing issue contract was represented without inventing acceptance, owner, priority or required architecture.
3. **Right tracking construct:** Local Markdown checkboxes, independent sub-issues, blockers, issue type, labels, projects and milestones are distinguished by their actual semantics; parent-child is not mistaken for prerequisite order.
4. **Meaningful granularity:** Children have their own outcome and acceptance; trivial task bullets have not been turned into a swarm of issues or a hierarchy for its own sake.
5. **Metadata grounded:** Labels, types, assignees, milestones and projects exist and are legitimately intended; no arbitrary user/bot assignment or fake `agent:ready`-style approval.
6. **State preservation:** Existing checked boxes, discussion, manually edited criteria and concurrent updates are retained when the body changes.
7. **Lifecycle truthful:** Progress, closure and reopening follow evidence and project rules; a linked PR or a closed parent does not silently certify unfinished child work.
8. **Side-effect and security discipline:** Mutations were actually requested and permitted; no sensitive information was published; unsupported native relationships were not represented as successfully applied.
9. **Verification:** Published body, metadata and relationship changes were re-read; URLs and success claims are based on tool results rather than intent to mutate.

## Evidence limits

An issue that is correctly labeled, linked and closed may still contain the wrong requirements. Use `work-handoff` assessment if the issue was constructed from a conversation and intent fidelity is in doubt.
