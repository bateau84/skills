# promql Quality Assurance

Adversarial validation for any agent. Assume competent production and normal review; attack residual false confidence without inventing new requirements.

## QA criteria

Critic tests no traffic, missing target, counter reset, one missing region, new label dimension, zero denominator, histogram bucket mismatch, and duplicate vector keys. Ask whether a plausible wrong system state yields the same scalar/graph.

Block when a load-bearing alert/SLI/dashboard query can materially misclassify health. Equivalent query style is non-blocking.

## QA depth

Increase depth with SLO/alert consequence, multi-dimensional joins, histograms, recording-rule chains, no-data semantics, large cardinality, and complex time/subquery logic.
