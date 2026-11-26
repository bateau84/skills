# Definition of Done: focused work samples

These three fresh-context tasks exercised candidate completion guidance on small synthetic assignments. The observations support the particular behaviors below. They do not establish an improvement over the prior instructions, lower cost, or performance in OpenCode/Loom.

Each subagent received the named instruction file and its task's `REQUEST.md`, with no parent conversation, evaluator rubric, or expected verdict. It could use tools within the disposable task directory. The parent inspected the actual files and reran the Python checks. The full subagent tool traces were not exported; retained evidence consists of task inputs, produced artifacts, and the parent's verification output.

## Observations

| Sample | Observed behavior | Evidence boundary |
| --- | --- | --- |
| [Architecture handoff](architecture/design-handoff.md) | Finished the design-only assignment, named the integration proof owner, kept real runtime conformance unproven, and treated distributed-worker benchmarking as advisory. | A generated design artifact checked against supplied scenario facts. The prior source review and formatter probe were fixture facts, not product checks executed in this trial. |
| [CSV implementation](export/RESULT.md) | Fixed quoting with the standard library; retained header, order and plain output; passed all three existing tests; left the unrelated cache file alone; returned DONE at the local boundary. | Actual source edit and passing tests, independently rerun in [verification.txt](export/verification.txt). The [initial source](export/report.before.py) failed the special-character test before the change. No application integration or release was claimed. |
| [Required proof unavailable](required-proof/RESULT.md) | Left the already passing implementation and tests unchanged; distinguished three passing local tests from the skipped mandatory deployment probe; returned BLOCKED with the missing proof and its owner. | Actual inspection and test execution, independently rerun in [verification.txt](required-proof/verification.txt). `OK (skipped=1)` did not become acceptance. The synthetic deployment placeholder cannot produce real deployment evidence. |

The architecture sample used the candidate `architectural-design` skill. The first coder sample used the candidate Coder charter and resolved supporting skills from the installed session catalog; their versions were not pinned. The required-proof sample received the candidate Coder charter and candidate `software-engineering` skill explicitly. [manifest.json](manifest.json) records source-file hashes, repository bases, retained-file hashes and limits. These distinguish the instruction inputs even though no exact model build is exposed by the collaboration API.

## Reproduce and extend

For each task, copy its inputs into a separate temporary directory, excluding the result file and verification output. For the CSV task, use `report.before.py` as `report.py`. Supply the matching instruction files and `REQUEST.md` to a fresh agent without the produced artifact, this README, or the fixture's evaluation expectations. Inspect the resulting artifact and tool actions; do not score the presence of the words “done” or “blocked” alone.

Run `python3 -B -m unittest -v` inside each Python sample directory. In the unavailable-proof sample, a successful process exit with one skip remains insufficient evidence for the required deployment claim. Only the integration owner can supply that real proof.

The broader regression fixtures add 18 skill cases and nine agent cases. Fixture validation succeeded for 608 cases across 124 skills and parsing succeeded for 66 unique agent cases. Those counts describe valid fixtures, not executed model passes. A controlled comparison should pin both repository revisions, installed skills, model, permissions and tool context, and include real defects beyond a narrow checklist as well as adequate evidence that warrants stopping.
