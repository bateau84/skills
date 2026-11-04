# Ubiquitous Language — Assessment

Assess whether the produced vocabulary prevents real misunderstandings **without inventing authority or changing contracts**.

1. **Bounded context:** Are the context and intended audience explicit? If a term differs across contexts, are both meanings preserved rather than forcibly unified?
2. **Distinguishing definitions:** Can a reader use the definition and at least one example/counterexample to tell the term apart from its nearest neighbor? Flag circular definitions and synonyms presented as definitions.
3. **Evidence and status:** Can consequential claims be traced to accepted decisions, stakeholders, or observed artifacts? Are `proposed`, `accepted`, and `unresolved` meanings distinguished? Does observed implementation avoid masquerading as product intent?
4. **Conflicting meanings:** Does the work expose material collisions (same word/different meaning; different words/same meaning)? Are unsettled lifecycle, ownership, and outcome semantics left explicit instead of being silently decided?
5. **Safe application:** Are in-scope artifacts consistent with accepted terms? If APIs, storage, events, tests, or external consumers depend on a name, is any rename treated as an impact-bearing change rather than cosmetic editing?
6. **Right-sized result:** Does the work clarify the specific ambiguity without building an unnecessary universal glossary, inventing policy, or adding definitions no one needs?

**Evidence:** Inspect the glossary or clarification, affected source artifacts, and a representative example that could have been misread before the change. A self-reported 'consistent' verdict is not enough.

**Disposition:** Report semantic errors, unsupported authority claims, missing important distinctions, and breaking renames separately from optional naming preferences.