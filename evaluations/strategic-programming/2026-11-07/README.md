# Strategic programming: one manual rehearsal

Both the existing and revised guidance produced working changes through two
successive tasks. Both first-stage implementations put the repeated retry policy
in one shared function; both fresh follow-on agents extended that function for
the second task. **This run does not show that the revised guidance is better or
faster.** It provides inspectable implementation outputs and a working exercise
for further comparisons.

## What was compared

This was one combined comparison of the `coder` role and `software-engineering`
practitioner guidance. Both changed together, so effects cannot be attributed to
either file separately. No assessment or QA companion was supplied to the
implementers.

| Input | Existing guidance | Revised guidance |
| --- | --- | --- |
| `agents/coder.md` | `bateau84/agents@372e4ece9af2deabcf05f8225cacd08b08c23215` | `bateau84/agents@894214f3e6b6c3e23931f98145c6d9655f8ecf21` |
| `skills/software-engineering/SKILL.md` | `bateau84/skills@1ec91b64265026a0c94a92fe1be449a566d9b240` | `bateau84/skills@490d1800298403a40ef8e12dc68dbfe8d2b12435` |

The seed, both tasks and final checker are also pinned to the revised skills
commit above. [The manifest](manifest.json) records their SHA-256 identities,
the exact supplied guidance hashes, and every retained output file's hash.
The supplied guidance and task bytes were checked against their source files.

The coordinator used a fresh agent conversation for each stage: four
implementers in total. First-stage agents received the seed, their arm's two
guidance files and the timed-out retry task. Second-stage agents received a copy
of their predecessor's output, the same guidance and the retry-permission task.
They could read `HANDOFF.md`, but received no first-agent chat or evaluation
verdict. They were instructed to stay within their project, use local tools and
the Python standard library, and avoid sibling projects, delegation and external
services.

This was instructed context isolation in a shared workspace. It was not an OS
sandbox or blinded comparison; arm names were visible in paths. The inherited
model build, sampling settings and comparable time/token costs were not
independently captured. The stage-to-stage copies are coordinator-reported;
pre-run snapshots and original orchestration/tool traces were not exported, so
this record cannot independently attest the exact initial second-stage trees.

## Observed results

These are independent post-run checks of the preserved outputs, not copied
claims from the participants' handoffs. All commands exited zero. Counts below
are test methods, including methods that exercise multiple entry points and
scenarios; they are not a quality or efficiency score.

| Preserved output | Its project tests | External contract checker | Patch reconstruction |
| --- | --- | --- | --- |
| Existing guidance, first task | 3 passed | 5 passed | All 9 file hashes matched; checker passed |
| Existing guidance, second task | 5 passed | 6 passed | All 9 file hashes matched; checker passed |
| Revised guidance, first task | 5 passed | 5 passed | All 9 file hashes matched; checker passed |
| Revised guidance, second task | 7 passed | 6 passed | All 9 file hashes matched; checker passed |

The final checker covers eligibility, exact errors, attempt limits, permission
defaults and precedence, diagnostic clearing, successful writes, failed-save
preservation, requested-record selection and unrelated-record preservation
through all three public Python entry points. The last two checks were added
after the participant runs, following independent review, and applied equally
to all frozen outputs. No participant output was repaired for these checks.
The checker source hash stayed fixed throughout the retained verification.

Source inspection supports these bounded design observations:

- Both first-stage outputs replace three copies of the policy with one function.
  The existing-guidance arm uses `jobqueue/_retry.py`; the revised arm uses
  `jobqueue/retry.py`. Each caller module re-exports the function and requires no
  extra coordination from its caller.
- Both second-stage outputs add the defaulted permission field and its check to
  the model and shared policy. The three caller modules remain unchanged from
  the first stage. No additional abstraction or extension mechanism appears.
- The revised first-stage handoff reports a behavior-preserving extraction check
  before adding the feature. That intermediate check is **self-reported**: the
  intermediate tree and original tool trace are not retained here. Final-state
  checks cannot independently establish that sequence.

## Retained evidence and replay

- [Manifest](manifest.json): source revisions and input/output content identities.
- [Verification log](verification.json): exact commands, working directories,
  exit statuses, stdout/stderr and environment for the independent reruns.
- [Existing, first](outputs/baseline-first.patch),
  [existing, second](outputs/baseline-second.patch),
  [revised, first](outputs/candidate-first.patch), and
  [revised, second](outputs/candidate-second.patch): complete changes from the
  **original seed**, including each stage's `HANDOFF.md`. Do not apply the two
  stages' patches sequentially.

Each patch was applied to a fresh seed copy with `git apply --whitespace=error`.
Every reconstructed file hash matched its preserved output, and the external
checker passed again. Only Python bytecode caches are excluded. Participant
handoffs are retained verbatim; their original execution claims remain distinct
from the independent checks in `verification.json`.

For example, from the skills repository at the pinned source commit plus this
evidence record, replay the revised second-stage output:

```sh
evidence_root="$PWD/evaluations/strategic-programming/2026-11-07"
packet_root="$PWD/skills/software-engineering/evals"
replay_root=$(mktemp -d)
cp -R "$packet_root/fixture" "$replay_root/project"
git -C "$replay_root/project" apply --whitespace=error "$evidence_root/outputs/candidate-second.patch"
(cd "$replay_root/project" && python3 -B -m unittest discover -s tests -v)
python3 -I -B "$packet_root/verify_artifacts.py" "$replay_root/project" --stage second
```

Use `--stage first` with a first-stage patch. Compare the reconstructed files to
the corresponding `output_files_sha256` map in the manifest if checking content
identity. The temporary directories shown in the retained log no longer exist;
the patches and pinned seed reconstruct their contents.

## What remains unproven

This was a manual agent exercise with actual model work. Its subsequent Python
checks make no provider calls. It does not exercise native OpenCode skill
discovery, deployed role permissions, Loom context controls or runtime
enforcement. It covers a trusted in-process fixture, without real HTTP/CLI
processes, durable storage, concurrency or production deployment.

One small paired run cannot establish a productivity advantage, reliable
long-term maintenance improvement, or restraint on unrelated small fixes. The
separate response cases cover those decisions, but their presence is not a
behavioral result. Repeated, controlled runs with retained original traces and
comparable cost measurements would be needed for broader claims.
