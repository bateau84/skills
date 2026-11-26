# Completed-job report export: structural design handoff

## Readiness decision

**The design is ready for implementation. The export increment is not yet proven to work.** This design assignment is complete: the accepted structure has justified owners, coherent failure handling, and an assigned downstream proof obligation. Implementation has not been assembled, and the real query-to-download check has not run. Those facts prevent a claim of implemented conformance, but do not prevent completion of this design-only assignment.

The bounded outcome enabled by this design is a CSV download of stored terminal job outcomes for the requested time range, through the existing authenticated query path. This contributes to the parent goal of letting operators inspect completed-job outcomes offline. Product delivery remains incomplete until the export integration task assembles and verifies that path.

## Derived from

The authority for this handoff is `REQUEST.md` in this directory. It supplies the following accepted decisions and evidence:

- Reuse the existing authenticated query boundary, CSV formatter, and HTTP download adapter.
- The query owns time-range filtering and stored terminal outcomes; the formatter owns escaped CSV representation.
- The adapter returns a file only after query and formatting succeed. Otherwise, it exposes the existing error outcome.
- Relevant source review found coherent ownership and no need for a new store or service.
- A focused formatter feasibility probe confirmed the required escaping.
- The export integration task owns the required real query-to-download check, which has not run.
- Cross-region deployment and email are outside this increment.

The source review and formatter probe are supplied prior evidence. This handoff does not claim to have rerun them or inspected implementation source. No quantitative Quality Scenario or new performance target was supplied; this design does not invent one.

## Problem and selected approach

Operators need a portable representation of completed-job outcomes. The system already has the three capabilities this increment needs: an authenticated query that selects the right stored outcomes, a formatter that represents values safely in CSV, and an HTTP adapter that delivers a completed result.

Connect those capabilities in that order. Keep selection and outcome meaning in the query, CSV escaping in the formatter, and response commitment in the adapter. The supplied review supports the ownership boundaries, and the escaping probe resolves the identified formatter feasibility concern. A new service, store, scheduler, or worker lifecycle has no demonstrated obligation to satisfy in this increment.

For example, an authenticated operator requests a time range containing terminal job records with commas, quotes, or line breaks in exported text. The query selects the records using its existing range rules. The formatter escapes those values. The adapter offers the resulting file only after both operations succeed. If the query or formatting fails, the adapter exposes the existing error outcome instead of a file.

This is a structural design, not evidence of successful assembly. It also does not promise successful client receipt after a download starts, introduce automatic retry, or establish a throughput target.

## Satisfies: obligations, owners, and proof

| Accepted obligation | Architectural owner and enforcement | Decisive downstream proof |
|---|---|---|
| Use the existing authenticated access path | The existing authenticated query boundary remains the sole entry to retrieval; the export assembly must not bypass it. | A real request exercises that boundary, including its existing rejection behavior. |
| Export the selected stored terminal outcomes | The query applies its existing time-range and terminal-outcome rules. The formatter and adapter do not repeat selection policy or reinterpret outcome values. | Seeded records inside and outside the range, including terminal and nonterminal records, produce exactly the query-authorized export content. |
| Preserve values in escaped CSV representation | The existing formatter owns representation. The supplied focused probe supports feasibility. | The assembled export preserves representative commas, quotes, and line breaks when the returned CSV is parsed. |
| Return a file only after query and formatting succeed | The adapter's response-commit boundary follows successful query and formatter completion. | Integration failure injection shows that query and formatter failures expose the existing error outcome and do not commit a file response. |
| Enable offline inspection | Successful adapter output is a downloadable CSV containing the selected outcomes. | A real HTTP request produces a file that can be saved and read independently of the live query. |

The export integration task owns this proof. Supporting component checks may help diagnose failures, but they do not replace the real query-to-download check.

## Constraints, options, and decision

Correct selection, faithful representation, authenticated access, and the response-commit boundary are the load-bearing forces. Maintaining one owner for each rule avoids duplicate filtering and escaping logic. Reusing the existing adapter preserves its current HTTP and error behavior.

The structural choice is already accepted. This handoff finalizes its composition rather than reopening it. There is one authorized realization to carry forward: direct assembly of the existing query, formatter, and adapter. The supplied source review and focused probe justify that realization without a new feasibility investigation.

A separate export service or persistent export store would introduce additional access boundaries, operational ownership, and state management without a demonstrated requirement that the accepted path cannot satisfy. Distributed workers would additionally require dispatch, completion, recovery, and delivery semantics that this increment has not authorized. These are possible future architectures, not viable substitutions for this bounded handoff. Email and cross-region deployment are explicitly excluded.

**Decision:** retain the three existing owners and connect their existing seams. Preparation stops at the assembly and verification needed for this increment. No new service, durable export state, worker protocol, compatibility layer, or background lifecycle is justified.

## Structure, state, and flow

1. The request enters through the existing authenticated boundary with the requested time range and the boundary's existing request semantics.
2. The query retrieves the applicable stored terminal outcomes. Existing persistence continues to own those outcomes; this design introduces no writes to their lifecycle.
3. The formatter produces the escaped CSV representation of the query result.
4. After successful query and formatting completion, the adapter commits the file response using its existing download contract. A failure before that point follows the existing error path.

The key composition requirement is that the adapter must not commit the file response while query or formatting can still fail. The implementation must use the existing component contracts to establish that ordering. This handoff does not prescribe a new buffer, temporary store, or exact method signature.

There is no new persistent export object and no new lifecycle transition to recover. Existing job persistence, authentication, and HTTP lifecycle behavior retain their current owners. This design adds no retry, cancellation, or durable acceptance semantics.

## Invariants and falsification points

| Guarantee | Preconditions | Responsible boundary and mechanism | How it can be falsified |
|---|---|---|---|
| Export retrieval uses existing authentication | Requests reach the supported export entry point. | The assembly invokes the existing authenticated query path without a bypass. | A request rejected by that path nevertheless retrieves export data. |
| Export selection and outcome meaning match the query | The query's existing accepted semantics and stored records are authoritative. | Query-owned filtering and terminal-outcome selection; downstream components only represent and deliver. | An out-of-range or nonterminal record appears, an expected record disappears, or an outcome changes during representation. |
| CSV represents the returned values faithfully | Values are within the existing formatter's supported contract. | Formatter-owned escaping, supported by the supplied feasibility probe. | Parsing the exported CSV changes a value or shifts its row or column because of escaping. |
| A file response follows successful preparation | Query and formatter report completion through their existing contracts. | The adapter gates response commitment on both successful completions. | A file response is committed before either component succeeds, or a preparation failure is presented as a file. |

## Input and operation coverage

The integration proof must cover a populated result and an empty result, preserving the existing formatter and adapter behavior in each case. It must also cover the query's existing time-range boundaries and rejection of invalid requests, rather than creating new interpretation rules in the export assembly.

Terminal outcomes must retain their stored meaning, including distinct terminal outcome values supported by the query. The export must not silently narrow “terminal” to successful jobs. Representation coverage includes the escaping cases established by the focused probe. The paired operation is export and read: parsing the downloaded file must recover the represented values.

Concurrent source changes retain the query's existing consistency semantics. The design does not add a snapshot guarantee or synchronization mechanism. If assembly reveals that an existing guarantee cannot be preserved, that is a failed premise requiring review of the affected design, not authority to invent a stronger guarantee.

## Failure and recovery

| Failure point | Required behavior and owner | Remaining evidence |
|---|---|---|
| Authentication or request validation | Preserve the existing boundary's rejection behavior; do not deliver query data through another path. | Exercise the real boundary in integration. |
| Query failure, including unavailable persistence | Adapter exposes the existing error outcome; no file response has been committed. | Inject a query failure through the assembled path. |
| Formatter failure after retrieval | Adapter exposes the existing error outcome; no file response has been committed. | Inject a formatter failure through the assembled path. |
| Process failure before response commitment | No completed file response can have been committed. Transport behavior remains that of the existing runtime and adapter. | Inspect response-commit ordering; exercise the relevant interruption if needed to prove that ordering. |
| Transfer interruption after successful preparation and commitment | Existing HTTP behavior applies. This design establishes successful preparation, not guaranteed client receipt or automatic recovery. | Verify adapter compatibility; any stronger delivery requirement needs accepted product semantics. |

There is no durable acceptance or authorized background-effect boundary here: no scheduling gap, persisted export decision, or completion-recording state is introduced. Consequently, no new recovery owner is needed. Query and formatter failure tests remain essential because individually correct components can still be assembled with an incorrect response-commit order.

## Security and trust boundaries

Stored job outcomes cross the existing authenticated query boundary and then the HTTP boundary to the requesting operator. Authentication remains enforced by the existing boundary. The formatter receives data rather than authority; it owns CSV representation and must not become a second access-control or selection layer. The adapter owns when the prepared representation is exposed externally.

The concrete risks in this scope are bypassing the existing authenticated path, exporting records outside the query's selection, and exposing a file response before preparation succeeds. The integration evidence above addresses those risks. No new credentials, service-to-service authority, email recipient, cross-region transfer, model-visible channel, or executable effect is introduced by this design.

## Verification, composition, and remaining proof

| Evidence | Status | Owner or source | What it establishes |
|---|---|---|---|
| Relevant source review | Completed, as supplied in `REQUEST.md` | Supplied review; reviewer identity not provided | Coherent ownership and no demonstrated need for a new store or service. |
| Focused formatter feasibility probe | Completed, as supplied in `REQUEST.md` | Supplied probe; executor identity not provided | Required escaping is feasible with the existing formatter. |
| Structural handoff review | Completed in this document | Design task | Obligations have owners, the proposed flow preserves accepted boundaries, and failure paths and proof obligations are explicit. |
| Component assembly | Not completed | Export integration task | Will establish that the real interfaces compose as described. |
| Real query-to-download check | Not run; required | Export integration task | Must establish authenticated selection, escaped representation, successful download, and existing error behavior across the assembled path. |

The integration task must retain concrete results for the successful download and the decisive query/formatter failure checks. A formatter probe alone cannot prove query selection, response-commit ordering, or HTTP delivery. A design review cannot establish runtime behavior.

There is no unresolved design-blocking feasibility question in the supplied scope. If integration finds that the adapter cannot delay file commitment until formatting completes, that the formatter does not support required values, or that retrieval bypasses the accepted authenticated boundary, the corresponding design premise has failed and must be corrected before product completion.

## Consequences and advisory work

This design keeps one owner for selection, one for representation, and one for delivery. It adds assembly work without a new operational service or persistent export lifecycle. Its limits are inherited component behavior and the absence of assembled integration evidence.

The suggestion to eventually benchmark distributed export workers is **advisory future work**. There is no accepted distributed deployment requirement, measured capacity failure, or performance target that makes it necessary to finish this design. A future accepted capacity requirement or credible evidence that the direct path cannot meet an actual operating condition would justify evaluating alternatives and benchmarking them. The suggestion does not reopen the current decision or add a completion condition.

## Completion boundary

**Design handoff: complete and ready.** The agreed structure is justified, load-bearing obligations have coherent owners and enforcement, relevant failure paths fit together, and downstream work has an assigned proof plan without needing a new product or structural decision.

**Export increment and parent outcome: still pending implementation and integration proof.** Passing that proof is the export integration task's completion condition, not evidence already established by this handoff.
