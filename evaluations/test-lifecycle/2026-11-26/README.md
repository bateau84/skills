# Test lifecycle forward exercises — 2026-11-26

Two fresh-context subagents performed bounded code tasks with the candidate
Coder instructions plus the candidate TDD/Python methodology. Both received only
their task, their fixture, the instruction paths, and boundaries prohibiting
changes elsewhere, dependencies, commits, or publication. They were not given
expected edits, evaluator rubrics, prior diagnoses, or the sibling result.

The maintainer inspected the resulting diffs and reports. The first task extended
an existing table and observed Red before the fix. The second consolidated two
redundant or incidental checks, retained real process-death recovery, and challenged
the retained assertions with three isolated defects. These are observed small
samples, not proof of general improvement or savings in existing product suites.

## Artifacts

- [Manifest](manifest.json): tasks, candidate content hashes, observed outcomes, and limits.
- [Baseline fixture](fixture/README.md): standard-library Python source and six existing tests.
- [Boundary correction](boundary-fix.patch) and [execution report](boundary-fix-result.md).
- [Persistence maintenance](suite-maintenance.patch) and [execution report](suite-maintenance-result.md).

The fixture and patches are historical evaluation artifacts. They do not add a
new required product or skill CI stage. The boundary bug is intentionally present
in the baseline; it belongs to the first task. The second task leaves it alone.
The real recovery test uses POSIX process signaling and `select`; this record
claims execution only in the current Linux/Python environment.

## Inspect or reproduce

Copy `fixture/` to a disposable working directory. Run
`python3 -B -m unittest discover -s tests -v` there for the six-test baseline.
Apply one selected patch with `git apply /absolute/path/to/<case>.patch` from the
copy and repeat that command. Use separate baseline copies for the two patches.
To reproduce the first Red, apply its test change before its production change.
The reports distinguish executed actions from broader evidence not established.

Independent instruction review found no blocking policy issues. Its one advisory
was to deliver the evidence-reuse corpus case as two separately revealed stages;
the authored case was corrected. That staged scenario and the whole-objective
cost cases remain unexecuted. No new runtime or maintenance benefit is inferred
from JSON validation or from merely adding those scenarios.
