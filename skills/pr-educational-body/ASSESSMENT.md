# pr-educational-body Reviewer Assessment

Domain-specific review guidance for any agent performing assessment. It does not establish product decisions or prove correctness by itself.

## Review criteria

Reviewer reads the PR body as a cold reviewer and verifies it teaches the **actual conceptual delta** without becoming a second commit log:

- PR title follows Conventional Commits syntax with a meaningful type, optional scope, `!` only for a breaking change, and a non-empty description summarizing the whole PR; new, edited, trivial, and draft PRs all comply;
- “why” describes the prior problem/outcome rather than invented retrospective rationale; commit history plus diff support the narrative;
- before→after conceptual delta matches the complete branch diff, including removals/behavioral changes not highlighted by commit titles;
- repository-specific terminology is introduced after the underlying concept so an external reviewer can build the right mental model;
- “what changed” groups by behavior/concern, not file inventory, and exposes security/migration/compatibility/state/authority changes proportional to risk;
- review notes point to genuinely load-bearing or risky areas rather than flattering summaries;
- verification lists exact checks/commands and observed status only when actually run; unverified areas remain explicit;
- breaking changes/follow-ups/deferred risk are visible when material;
- PR body does not claim normative authority over source specs/architecture or duplicate every commit message verbatim.
