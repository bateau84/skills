# Query patterns

These examples explain decisions, not universal replacements. Confirm the real schema and accepted results first. The named parameters below use SQLite syntax; PostgreSQL drivers typically use positional placeholders such as `$1` and `$2`. Bind through the driver rather than substituting strings.

## Aggregate independent child collections

Assume `customers(id)`, `orders(id, customer_id, amount_cents NOT NULL)`, and `tickets(id, customer_id)`, with globally unique IDs. The report needs every customer, total order amount, and ticket count, with zero totals/counts when there are no corresponding children. Directly joining both child tables multiplies orders by tickets.

```sql
WITH order_totals AS (
    SELECT customer_id, SUM(amount_cents) AS total_cents
    FROM orders
    GROUP BY customer_id
), ticket_totals AS (
    SELECT customer_id, COUNT(*) AS ticket_count
    FROM tickets
    GROUP BY customer_id
)
SELECT c.id,
       COALESCE(o.total_cents, 0) AS total_cents,
       COALESCE(t.ticket_count, 0) AS ticket_count
FROM customers AS c
LEFT JOIN order_totals AS o ON o.customer_id = c.id
LEFT JOIN ticket_totals AS t ON t.customer_id = c.id
ORDER BY c.id;
```

Two orders of 100 cents and two tickets must produce 200 cents and two tickets. `SUM(DISTINCT amount_cents)` would incorrectly produce 100 cents. A customer without children produces zeros because this report explicitly requires that meaning; do not universally turn unknown amounts into zero.

If IDs are scoped to a tenant, carry the tenant key through grouping and joins. For a narrowly filtered report, investigate pushing equivalent restrictions into the child aggregates so unrelated rows are not processed. That is a measured engine-specific decision, not a reason to change the report's meaning. See [join/grouping semantics](https://www.postgresql.org/docs/current/queries-table-expressions.html).

## Traverse a stable ordered result

Assume `events(id PRIMARY KEY, tenant_id, created_at NOT NULL, summary)`. Timestamps use one consistent representation, the order keys are immutable during this traversal, and the request wants the next page in descending timestamp/ID order.

```sql
-- First page: omit the cursor predicate entirely.
SELECT id, created_at, summary
FROM events
WHERE tenant_id = :tenant_id
ORDER BY created_at DESC, id DESC
LIMIT :page_size;

-- Following pages: bind the final row's complete sort tuple.
SELECT id, created_at, summary
FROM events
WHERE tenant_id = :tenant_id
  AND (created_at, id) < (:last_created_at, :last_id)
ORDER BY created_at DESC, id DESC
LIMIT :page_size;
```

A candidate index is `(tenant_id, created_at DESC, id DESC)`; verify its plan, measured benefit, and write/storage costs. Enforce a positive bounded page size in the application.

The ID avoids skipping other events with the same timestamp. This example is not sufficient for nullable keys, mixed ascending/descending ordering, a different collation, or mutable sort values. Define their cursor comparison deliberately. For a snapshot export while writes continue, use a suitable snapshot or other explicitly bounded consistency design, accounting for long-transaction costs. See [row-value scrolling](https://www.sqlite.org/rowvalue.html) and [deterministic ordering](https://www.postgresql.org/docs/current/queries-limit.html).

## Check result equivalence

For an unordered result with meaningful duplicates, compare a multiset of typed rows, not just a set or row count. For promised order, compare the sequence. When precision is approximate by design, choose a domain-justified tolerance rather than hiding an error behind arbitrary rounding.

Use independently calculated expectations for the two-order/two-ticket case and a full traversal across repeated timestamps. A correct result on those cases is semantic evidence only; it is not a benchmark for a 1 GB workload.
