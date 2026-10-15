# Proof Record and Worked Example

Use this as a project-adaptable record, not a required report format or approval gate. It illustrates the decisions in [SKILL.md](../SKILL.md); filling out a template is not proof of execution.

## Proof record template

```markdown
### <scenario identifier> — <externally meaningful outcome>

- Accepted claim / criterion / exclusions:
- Entry point and consumer or stimulus:
- Ordered product-owned path (implementation at every stage; all mandatory stages real):
- External dependencies (real/sandbox/fake; why; semantics preserved; compatibility limits):
- Static prerequisites (why outside the behavior under proof):
- Produced-state provenance (producer → storage/transport → consumer; run identity):
- Reset / isolation / cache and asynchronous-work handling:
- Shipping fidelity (build/package/image identity; command; configuration/flags/schema;
  claim-relevant differences or equivalence):
- Action / reproduction steps:
- Externally meaningful expected result:
- Failure/recovery/idempotency assertion, if promised:
- Implemented-experience evidence, if accepted design materially constrains this journey:
- Observed result and evidence locations (logs/assertions/transcript/screenshots; secrets redacted):
- Status: PASS | FAIL | UNPROVEN, scoped to this claim
- Remaining gaps / narrower claims supported / relevant later changes requiring revalidation:
```

Use identifiers already present or plain-language references. If only planning, leave observed result explicitly **not executed** and status **UNPROVEN**; record the runnable strategy and unavailable prerequisites.

## Local-green/product-broken example

Adapted from the older source's YuHaul regression pattern. This is an illustrative mechanism, not a new execution result.

**Accepted promise:** A user configures discovery, runs it, and can later inspect why each item was accepted or rejected. On quota exhaustion, eligible work is retained and a later run resumes it. The accepted mobile design requires comprehensible interruption status and visible recovery controls.

**Available evidence:** Backend integration tests pass for routing. Frontend component tests pass with mock decision details. The built frontend still has a mock fallback because the decision-detail endpoint is absent. A routing test inserts a discovered-item row and asserts an action. Another test starts a real request and checks `202`.

| Evidence | What it supports | What it does not support |
| --- | --- | --- |
| Backend routing tests | Routing logic for their supplied inputs | Browser configuration, discovery provenance, later explanation |
| Frontend mock-detail tests | Rendering for supplied details | Real details endpoint or real UI/backend composition |
| Insert row → route → action | Narrow routing/action path | Discovery → routing path |
| Real request → `202` | Request initiation | Completion, durable later explanation, or resume after quota |

The observed missing endpoint/product-side fallback is a full-journey defect: **FAIL** for that composition. Unexecuted recovery and mobile experience remain **UNPROVEN**. The local tests remain useful; their union is not an assembled proof.

### A corrected proof plan (not claimed executed)

1. Identify the built frontend and server package/configuration intended to ship; remove or fix the missing real endpoint through the authorized implementation work. A test must not patch in the endpoint.
2. Map the path: built browser UI → real app API/auth → real persisted configuration → real discovery/scheduler → real worker/routing → real product-side provider adapter → external provider fake → real durable decision store → real details API → built UI.
3. Use a temporary database running real migrations. An existing account may be a static prerequisite if registration is outside the claim. Do not insert discovered items or decisions: the product must produce them in this run.
4. Use an external provider fake for safety. Give it claim-relevant payloads, pagination and quota responses; keep the product adapter real. State that live-provider compatibility is not established by this fake.
5. Configure through the browser, trigger the real run, and wait on observable completion using bounded tools rather than assertions on initiation. Reload/read through the real UI and inspect persisted reasons for representative accepted and rejected items.
6. Run the agreed quota scenario: trigger exhaustion, observe retained eligible work and understandable interruption status, then resume through the supported product entry and observe the later external outcome and no-loss promise. Check duplicate-action semantics only if explicitly agreed; do not infer exactly-once behavior. Validate mobile controls/status against accepted design using available experience-validation methods.
7. Store run identity, commands, build/configuration, assertions, external-fake behavior, experience observations, and gaps. Until run, both records stay UNPROVEN.

### Claim-dependent setup decisions

- Pre-seeded account: allowed for routing/explanation; not proof of registration.
- Historical pre-upgrade data: allowed as upgrade input; pre-migrated output is not proof of migration.
- Direct API entry: appropriate for an API claim; insufficient for the same promise expressed as a browser journey.
- Provider fake: allowed beyond the product boundary with relevant semantics; insufficient for a claim of compatibility with the live provider.
- Temporary storage: allowed when exercising real migrations/persistence; bypassing those stages is not equivalent merely because rows look realistic.
