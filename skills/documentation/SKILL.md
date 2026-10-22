---
name: documentation
description: Maintain truthful documentation of current implemented behavior and user-facing operation. Use for application overview, setup, developer/user guides, API usage and release/migration explanations; not for deciding product requirements, architecture authority or OKF serialization.
---

# Documentation

This skill governs **truthful content** about the implemented application and published use. It does not grant authority to redefine intended product behavior.

## Explain before detailing

Lead with what the reader needs to know or do, one concrete example when useful, and the important limits. Use everyday words and short sentences where they preserve meaning. Explain necessary technical terms when they first appear; keep exact commands, identifiers, and guarantees in the detailed sections. A friendly summary must not overstate what works or hide an important failure. Don't add a separate glossary or document just to satisfy this guidance.

## Improve existing documentation

When a document needed for the current work makes the actual behavior, usage, or important limit hard to understand, **rewrite the affected content**, not just prepend a friendly introduction to otherwise opaque text. Keep supported commands, error cases, warnings, links, and current-versus-planned distinctions accurate. Validate changed factual claims against available source or observed operation. Keep the existing document and navigation structure unless changing it clearly improves use.

A wording problem alone is not a reason to stop unrelated delivery or rewrite a repository's whole documentation history. Correct a meaning or usage ambiguity before someone relies on it; improve minor prose while touching relevant sections, or leave unrelated cleanup for a separate, explicitly scoped task. Do not rewrite accepted product or architecture decisions under the guise of documentation cleanup.

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
