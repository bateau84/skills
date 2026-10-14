# report-to-keep QA Contract

Attack false confidence around durable retention.

## QA criteria

- a failed or provisional gate report being described as approved because it was promoted;
- useful conclusions being used to justify keeping an otherwise disposable raw report instead of updating the correct governed artifact;
- path traversal, symlink escape, or alternate-path tricks that replace an unintended destination;
- collision or overwrite behavior that can replace unrelated durable evidence;
- crash/interruption between audit state and filesystem publication leaving partial, unrecoverable, or contradictory durable state;
- cross-process promotion/recovery races that can misclassify an in-flight promotion as abandoned;
- partial copies being represented as verified preservation;
- ambiguous source material being retained as if provenance were established;
- producer identity or context being relabeled during retention;
- transformations, summaries, metadata rewrites, or redactions silently changing the retained evidence;
- retention that contradicts the user's request or repository conventions.

Promotion should survive these attacks without increasing the report's authority.
