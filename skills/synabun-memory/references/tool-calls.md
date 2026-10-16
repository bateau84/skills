# Memory tool calls

Load the relevant section when needed. These are tool argument objects, not shell commands. Names below omit host-specific prefixes. The installed schema and permissions control what can actually be called; do not probe by making blind writes.

## Compatibility

The public documentation mixes the consolidated `category` tool with older split `category_*` examples. The inspected source also has fields/actions not listed on that page. For example, its `remember` schema requires both `project` and `category`, and its `memories` tool supports exact-ID reads. Always inspect the connected version.

Substitute a confirmed project identifier, an existing category, real content, and returned full UUIDs for every placeholder. Never send angle-bracket placeholders literally. Synabun calls may report failures as plain text rather than a transport error: read the response.

## Find and read

Start with a specific, project-scoped query. Leave ranking/count settings at their configured values unless the task or user calls for a different setting.

`recall`
```json
{"query":"duplicate completion notifications after resuming a delegated task","project":"<existing-project>"}
```

When supported, add `format: "compact"` for discovery. Optional `include_sessions: false` excludes transcript chunks when only curated memories are relevant. Do not pass unsupported fields on older servers. Omitting `project` can search other projects; it is not a safe substitute for an unknown identifier. Tags default to any-match in the inspected source; do not assume that several tags mean all must match.

`memories` — fetch a full original, if this action is exposed:
```json
{"action":"get","id":"<full-uuid-from-result>"}
```

Note `id`, not `memory_id`. Newer results include a revision usable for guarded edits. Listing and compact-search excerpts may be truncated. On an older server without exact-ID reads, retrieve the complete original through a supported memory read. If completeness cannot be established, do not merge or delete based on a preview.

`memories` — limited project browsing:
```json
{"action":"by-project","project":"<existing-project>","limit":10}
```

`memories` with `action: "stats"` returns store-wide statistics in the inspected implementation; adding `project` does not scope them. Do not request them when an all-project inventory is outside scope. Likewise, `by-category` does not combine the project filter in that implementation. Use `by-project` and inspect categories, or a confirmed combination supported by the installed version. A limited listing is not a complete audit.

## Choose a category

`category` — inspect existing names and descriptions:
```json
{"action":"list"}
```

On a server exposing split tools instead, use its actual `category_list` schema. Do not call both variants. Prefer a suitable existing leaf category. Only create a category when nothing fits and taxonomy changes are in scope:

`category`
```json
{"action":"create","name":"engineering-lessons","description":"Evidence-backed engineering lessons with context and applicability limits."}
```

The name above is an example, not a required category. Do not pre-create separate buckets for every agent, task, repository, or lifecycle stage. Category rename/delete can affect other memories; ordinary lesson capture does not authorize taxonomy cleanup. In the inspected `remember` implementation, an unknown category can be remapped to a fallback rather than rejected—check where a write actually landed.

## Store a distinct lesson

`remember`
```json
{
  "content":"<concise lesson with scope, mechanism, evidence, limits, and observation date>",
  "project":"<existing-project>",
  "category":"<existing-category>",
  "importance":8,
  "tags":["implementation-lesson","concurrency"],
  "source":"self-discovered",
  "related_files":["<verified-project-file>"]
}
```

Remove `related_files` when no real applicable file is known. Paths must be meaningful to the memory server's registered project root, not merely exist in the caller's working directory. Do not invent paths or copy large code blocks into memory.

`source` is `user-told`, `self-discovered`, or `auto-saved`; it records origin, not truth. Importance is 1–10. A significant reusable lesson may be 7; evidenced architecture choices and hard-won fixes fit 8; reserve 9–10 for unusually consequential knowledge. A routine event does not become valuable merely by assigning it a high score.

Newer schemas expose `idempotency_key` and `source_ref`. Use a stable key for retries of the same logical write, scoped to the same project/category; do not reuse it for different content. `source_ref` can carry a stable source pointer, but keep enough provenance in the content for readers. Semantic duplicate checks still matter.

## Correct, consolidate, or supersede

Fetch the complete current record first. `reflect` changes only supplied fields, but supplied collection fields replace their collections.

`reflect`
```json
{
  "memory_id":"<full-uuid-from-result>",
  "content":"<updated lesson, retaining still-valid evidence and the reason for correction>",
  "add_tags":["revalidated"]
}
```

Use `add_tags` to preserve unrelated tags. `tags`, `related_files`, and `related_memory_ids` replace their existing arrays when supplied: merge intentionally. Leave `project` and `category` unchanged unless correcting a confirmed misfiling. Updating content can regenerate file checksums; do not refresh a stale baseline without checking its source.

When exposed, add `expected_revision` using the revision just read. A conflict means fetch again and reconcile, not retry with a guessed revision. Without revision support, re-read just before editing and keep updates narrow; this reduces but does not remove race risk. Stop a destructive merge if concurrent changes cannot be reconciled safely.

For a distinct replacement decision, newer `reflect` schemas expose `supersedes`: call it on the replacement memory with the old memory's UUID. Fetch and verify both records and their project first. `related_memory_ids` alone is only a link, not a supersession relation. On older versions, preserve the relationship and scope in the content rather than inventing an unsupported argument. Do not equate superseded with worthless.

## Find cleanup candidates

`sync` — use supported filters and a modest output limit:
```json
{"project":"<existing-project>","categories":["<existing-category>"],"limit":10}
```

Some versions expose only `project`; use only supported fields. In the inspected implementation, `project` scopes the scan, but `categories` and `limit` filter/bound output after scanning. They are not a guarantee of cheap execution.

The scan compares stored checksums against accessible files. Memories without checksums and missing/unreadable files can be skipped. No flagged result does not mean all memories are valid. A changed file can leave a lesson correct. If optional judgment is configured, `sync` may invoke it and record advisory verdicts; it is not guaranteed to be a purely read-only operation. Do not enable services, paid analysis, or settings changes as part of this skill.

`memories` — newer versions offer candidate triage:
```json
{"action":"triage","project":"<existing-project>","limit":10}
```

Triage suggests records and does not itself delete them. It can use configured judgment. Neither its ranking nor access-count/age signals authorize deletion. Fetch full originals, preserve rare important lessons, and state the limits of any partial cleanup.

## Forget and restore

For an explicit forget request or authorized cleanup, verify the target's full content and project immediately before soft deletion. When consolidating, first confirm that the survivor contains every distinct useful lesson and evidence pointer.

`forget`
```json
{"memory_id":"<full-uuid-from-result>"}
```

`restore` — reverse a soft deletion when the record is still recoverable:
```json
{"memory_id":"<full-uuid-from-result>"}
```

These tools operate on returned full UUIDs, not title matches or shortened IDs. Record the returned outcome; a successful transport alone is insufficient. Do not automatically purge trash. Restoring trash is different from undoing a content edit. Newer `memories` schemas have `history` and `undo`; inspect those schemas and the exact revision before using them in an explicitly requested correction.

## Source basis

Checked 2026-10-15. Public guide: `https://synabun.ai/docs#section-mcp-tools`.

Source files were read from `danilokhury/Synabun` main; its observed head was `9393942ba8013e6cfd6b5ac2515b14cf51f15139`. Recorded file identities, rather than the mutable branch name, identify the exact excerpts inspected:

| File under `mcp-server/src/tools/` | Inspected lines | Git blob SHA |
| --- | --- | --- |
| `remember.ts` | 1–170 | `dc7c266c0edc5048e2c8400f4fb3a0bc02ce14b7` |
| `recall.ts` | 1–190 | `2eae602844ef36ca038ded8fab7b06c97e8d4e48` |
| `reflect.ts` | 1–165 | `9049804d91f99155b85970ee87876f821445277e` |
| `memories.ts` | 1–165 | `7ce6d4d56f6748c17625a9d70950b93613162c20` |
| `sync.ts` | 1–195 | `39f580451a74d36f9b35d536d7df0401c900fef4` |
| `category.ts` | 1–125 | `8a3d5e562e022bf2d7a89dd901187e5d26fd0d0f` |

Source directory: `https://github.com/danilokhury/Synabun/tree/9393942ba8013e6cfd6b5ac2515b14cf51f15139/mcp-server/src/tools`.

The public guide supplies the basic `forget`/`restore` contract. This is source/schema verification, not a live test against the user's installed server. No browser, profile, scheduling, or other non-memory tool guide is included.
