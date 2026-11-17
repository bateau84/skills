# Licensing and provenance

## Repository licence

Original material contributed to `bateau84/skills` is made available under the
[Apache License, Version 2.0](LICENSE), except where a file or directory states
otherwise. This covers only rights held by the respective authors or contributors.
A repository-wide licence does **not** remove third-party copyright, override
separate terms, or grant rights that contributors do not own.

Apache-2.0 permits reuse, modification, and commercial distribution, subject to
its conditions, including required attribution and modification notices.
See [NOTICE](NOTICE) for confirmed upstream attribution.

## Confirmed upstream adaptation: `mcp-builder`

- **Source:** Anthropic's
  [`mcp-builder` skill](https://github.com/anthropics/skills/tree/main/skills/mcp-builder).
- **Original rights holder:** Anthropic, PBC (copyright notice: 2026).
- **Upstream licence:** Apache-2.0. The original
  [per-skill licence](skills/mcp-builder/LICENSE.txt) is retained unmodified.
- **Material inherited:** `SKILL.md`, MCP reference guides, evaluation guidance,
  and bundled Python scripts and sample input.
- **Modifications here:** SDK-version compatibility guidance, MCP tool-scope
  advice, reference and evaluator correctness, dependency bounds, and additional
  assessments, QA scenarios, tests, and examples. Modified inherited files
  carry modification notices.

A source comparison on 2026-11-12 confirmed that most of the text in corresponding
`mcp-builder` files was retained from Anthropic, including substantial verbatim
passages. These are **adaptations**, not independently authored substitutes for
Anthropic's materials. Project-specific additions may have their own authorship,
but the upstream licence and notices continue to apply to inherited content.

## Distribution and further source checks

When copying, packaging, or publishing a skill, include its applicable licence
and attribution files, preserve upstream copyright statements, and identify
changes to inherited files. A bundled skill may contain multiple separately
authored components; do not present all of them as solely original work.

This document records **confirmed** provenance, not a completed rights audit of
every skill in the repository. Other externally derived content requires its own
source and licensing review before independent commercial redistribution. The
absence of a per-skill licence does not prove that all content is original or
free of third-party conditions.
