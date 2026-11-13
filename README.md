# Portable Agent Skills

Reusable engineering, design, product, and documentation guidance for any AI agent or human practitioner. No plugin, agent hierarchy, orchestration framework, or MCP server is required to use the library.

## License and provenance

Original contributions are available under the [Apache License, Version 2.0](LICENSE),
to the extent their authors have rights to license them. Third-party materials
retain their original copyright and applicable licensing obligations.
See [NOTICE](NOTICE) and [LICENSING.md](LICENSING.md) for confirmed attribution,
including the Anthropic-derived `mcp-builder` skill.

## Use a skill

1. Browse [`skills/`](skills/) and select the smallest set relevant to the task.
2. Read the selected directory's `SKILL.md`, or load it through your agent's native skill loader when available.
3. Resolve `references/`, `scripts/`, and other relative paths from that skill's directory. Bare skill names refer to siblings in this library; use ordinary file reads if no loader is available.
4. For review or adversarial validation, optionally read `ASSESSMENT.md` or `QA.md` in the same directory.

Copy a complete skill directory when installing elsewhere so its references and bundled resources travel with it. Installation paths and discovery conventions depend on the host; the content can also be read directly without installation.

Skills provide methodology. The user's request, host instructions, repository conventions, and actual tool permissions determine scope and execution. Terms such as designer, reviewer, or implementer describe activities, not required agents. Artifact templates and example paths can be adapted to local conventions.

Some technical skills explain particular external tools or services. Those dependencies apply only when using that integration; check availability and use documented alternatives where provided. Evaluation files are scenario fixtures, not a required execution harness.

Browse [`skills/`](skills/) for the catalogue; see [LICENSING.md](LICENSING.md) for confirmed source lineage.

## Optional runnable evaluations

`bun run eval:list`, `bun run eval:validate`, and `bun run eval:harness-test` provide
provider-free maintainer checks. Explicitly selected live trials use
`bun run eval:live -- ...` with a chosen model and a pinned external runner plus
verified immutable local image. No eval tooling is required to load a skill.
Live runs print the run artifact directory at startup and completion and publish
the latest report at **[`EVAL-RESULTS.md`](EVAL-RESULTS.md)** beside this README.
Each `.skill-evals/<run-id>` (or explicit `--artifact-dir`) retains its own
`results.md` and detailed JSON history. Generated reports are private (0600),
gitignored operational output, not automatically committed.
Relative `--artifact-dir`/`--output` paths are repository-rooted, independent of
the caller's working directory. Report delivery failures remain exit 2 but show
any independently verified evaluation aggregate and retained manifest location.
For an experimental, subscription-backed Claude Agent path, see [Claude Agent evaluation](docs/claude-agent-evals.md). This is an opt-in profile; no real model run is automatically authorized.\nSee [evaluation setup, controls, evidence and exit semantics](docs/evaluations.md)
and [observed verification/gaps](docs/eval-verification.md). The historical
four-variant pilot remains a separate record, not a new Boolean-score run.
