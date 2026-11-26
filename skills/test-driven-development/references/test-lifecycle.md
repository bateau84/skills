# Test lifecycle: framework basis and examples

Use this reference when deciding whether tests should be added, consolidated,
replaced, retired, or run at a different feedback boundary. The normal decisions
remain in `SKILL.md`; this reference explains their basis.

## Established foundations

| Source | Principle used here |
| --- | --- |
| Kent Beck, [Canon TDD](https://newsletter.kentbeck.com/p/canon-tdd) | Analyze behavior in a Test List, implement one concrete test at a time, make it pass honestly, and refactor when useful. Speculatively implementing the whole list creates avoidable rework. |
| Ham Vocke, [The Practical Test Pyramid](https://martinfowler.com/articles/practical-test-pyramid.html#AvoidTestDuplication) | Maintain a responsive test portfolio. Higher-level tests should earn their extra cost through confidence unavailable below; redundant protection can be removed or replaced. Stage verification by its feedback needs. |
| Adam Bender, [Testing Overview, Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch11.html) | Distinguish scope from size: what a test verifies is different from its resources, processes, and execution constraints. Reliability and fast feedback contribute to the suite's value. |
| Erik Kuefler, [Unit Testing, Software Engineering at Google](https://abseil.io/resources/swe-book/html/ch12.html) | Behavior-focused tests should survive harmless implementation changes. Prefer descriptive, meaningful tests; some repeated setup is clearer than excessive abstraction. |
| Vaughn Vernon, [Effective Aggregate Design, Part I](https://www.dddcommunity.org/wp-content/uploads/files/pdf_articles/Vernon_2011_1.pdf) | Model consistency boundaries around actual business invariants rather than convenient object graphs. Applying this to testing means exercising an accepted rule at its owning boundary. |
| Martin Fowler, [Test Coverage](https://martinfowler.com/bliki/TestCoverage.html) | Coverage helps locate untested code; it does not establish assertion quality. Maintenance friction and runtime warrant investigation, not arbitrary numeric targets. |

The lifecycle guidance is a synthesis of these practices, not a new named TDD or
DDD framework. DDD supplies domain language and boundaries where the project uses
them; it does not prescribe test quotas, fixed layer ratios, or runtime limits.

## Example: one rule, distinct boundaries

A reservation domain rejects quantities above available stock. Its existing
domain tests cover valid quantities and the upper boundary. A newly discovered
zero-quantity bug can become another focused case in that table, observed failing
before the fix. Copying the entire quantity matrix into browser tests adds no
automatic value.

A real database test that races two reservations protects a different mechanism:
the persistence transaction must uphold the rule under concurrent access. A
browser scenario may separately protect correct input serialization and visible
rejection. Keep those boundaries where required even if all tests mention the
same domain rule. Conversely, consolidate duplicate browser cases when a retained
scenario proves the same wiring and the domain matrix preserves the examples.

## Example: a slow suite

A recorded 18-minute qualification run is a reason to inspect its slow groups,
matrix, retries, and repeat frequency. It is not evidence that a particular test
is wasteful. An unchanged, applicable run can support later independent review;
a changed schema, adapter, or shipping configuration may require new proof.

Separate measurements from estimates. For a material optimization, compare the
affected commands under comparable conditions and identify the protection kept.
Do not claim a faster product suite from instruction changes alone. Preserve
required final qualification even when the normal editing loop becomes cheaper.
