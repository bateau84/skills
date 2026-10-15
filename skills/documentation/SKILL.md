---
name: documentation
description: Maintain truthful documentation of current implemented behavior and user-facing operation. Use for application overview, setup, developer/user guides, API usage and release/migration explanations; not for deciding product requirements, architecture authority or OKF serialization.
---

# Documentation

This skill governs **truthful content** about the implemented application and published use. It does not grant authority to redefine intended product behavior.

Use the repository's `AGENTS.md` for document locations and update obligations. Use `okf-authoring`, maintained in `nrkno/okf-mcp`, when document metadata, index/log, or relationship maintenance is required; do not duplicate those formatting rules here.

## Current implementation and operation

1. Discover the accepted requirements/decisions and existing user or developer documentation.
2. Inspect source code, tests and real commands or configuration relevant to each changed claim.
3. Distinguish current, planned, unsupported and deprecated behavior; do not describe intent as already implemented.
4. Keep application/system overviews concise and navigational, with meaningful components, flows, boundaries, and known operational limits.
5. Update only documentation affected by the behavior or interface change; avoid ceremony-driven rewrites.
6. Verify important examples against available implementation evidence. Record what was not verified.

If implementation conflicts with accepted requirements, **surface the mismatch** instead of rewriting normative documents to bless the implementation.

## User-facing publication

For README, user/admin/developer instructions, migrations, releases and API usage:
- Describe only supported behavior; use reproducible examples where possible.
- Name prerequisites, compatibility and consequences where material.
- Do not invent release dates, versions, security guarantees, removal timelines or migration support.
- Preserve links to actual authoritative sources and current interfaces when available.

## Boundary

Substantive Anchors, requirements, user journeys, architectural designs and decisions belong to their specialized skills. This skill describes verified reality and usage, not new requirements.
