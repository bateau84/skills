# Ubiquitous Language — Assessment

Assess whether the produced vocabulary prevents real misunderstandings **without inventing authority or changing contracts**.

1. **Bounded context:** Are the context and intended audience explicit? If a term differs across contexts, are both meanings preserved rather than forcibly unified?
2. **Distinguishing definitions:** Can a reader use the definition and at least one example/counterexample to tell the term apart from its nearest neighbor? Flag circular definitions and synonyms presented as definitions.
3. **Evidence and status:** Can consequential claims be traced to accepted decisions, stakeholders, or observed artifacts? Are `proposed`, `accepted`, and `unresolved` meanings distinguished? Does observed implementation avoid masquerading as product intent?
4. **Conflicting meanings:** Does the work expose material collisions (same word/different meaning; different words/same meaning)? Are unsettled lifecycle, ownership, and outcome semantics left explicit instead of being silently decided?
5. **Safe application:** Are in-scope artifacts consistent with accepted terms? If APIs, storage, events, tests, or external consumers depend on a name, is any rename treated as an impact-bearing change rather than cosmetic editing?
6. **Durable, right-sized result:** Was the existing vocabulary found and reused, including relevant definitions embedded in other documents? If none existed and consequential terms recur across artifacts, was a small vocabulary created when writing was in scope and linked from affected documents? Review-only work may propose edits instead. Flag competing dictionaries, unnecessary glossaries for trivial questions, and waiting for agreement before recording an unresolved term.
7. **Finding continuity:** Can the next reader recover each material unresolved collision's sources, distinguishing example, consequence, decision needed, and known or unknown owner without the original chat? Are verified corrections distinguished from open decisions and out-of-scope work, without treating a handoff as resolution or claiming unchecked consumers are aligned?

**Evidence:** Inspect the resulting vocabulary or clarification, affected source artifacts, links, and a representative example that could have been misread before the change. For claimed file changes, inspect the actual files or diff; for a handoff, inspect what the recipient can access. A self-reported 'consistent' verdict or promise to create a file is not enough.

**Disposition:** Report semantic errors, unsupported authority claims, missing important distinctions, and breaking renames separately from optional naming preferences.
