# Evaluate the product a skill is meant to improve

## Define the claim before the score

Name the user-visible product and the failure mechanism: a correct patch,
usable requirement, coherent design, accurate diagnosis or reviewable handoff.
Then identify what evidence could establish that product. A generated plan can
demonstrate reasoning; it cannot demonstrate an applied fix or a passing test.

For each criterion distinguish:

- **Outcome:** correctness, usefulness, accepted constraints or a real consumer
  obligation, justified independently of the skill's preferred wording.
- **Convention:** a preferred template, idiom, heading, spelling or organization
  that is not itself necessary for the accepted task.

The same feature can belong to either group in different tasks. A prescribed
JSON schema used by a caller is an outcome obligation. A schema invented only
to make grading convenient is not. Split compound criteria when they mix the
two. Report outcome and convention results separately, with denominators.
Never let a formatting gain compensate for a correctness regression.

## Make the task answerable

Supply the source files, diff, accepted decisions, tool outputs and environment
facts required by the claimed evidence mode. Keep evaluator-only expectations,
answer keys and prior verdicts outside target context.

If execution is unavailable, make the task explicitly a response or planning
exercise and grade the proposal. If execution is necessary, a missing fixture,
blocked tool or unavailable observation is unusable evidence, not failed skill
behavior. Do not invent a successful run or silently turn execution into prose.

Inspect negative criteria for their actual predicate. Warning against a command
is different from recommending it. Conditional regeneration after annotation
changes is different from needless regeneration now. A safe equivalent command
is valid unless the accepted contract requires that exact command. Paragraph
order alone does not prove the order in which actions occurred.

## Build useful contrasts

Use observed failures where available. A synthetic case is a hypothesis until
exercised; record that honestly. A useful set may include:

- the defining capability or recurring failure;
- an adjacent task where the guidance should stay out of the way;
- a small task where extra scaffolding or invented decisions would harm the
  product;
- a case where more structure or a stricter boundary is actually necessary.

Choose cases for these distinctions, not a fixed quota. Review existing cases
before adding duplicates. Retain high-ceiling and rare-risk cases as regression
coverage. The baseline need not fail most runs for a serious boundary to matter.
Treat discrimination as observed for a particular case, model and setup; changed
prompts, fixtures or rubrics invalidate inherited calibration.

## Calibrate judges independently

Have a judge assess each anonymized output against the task before any paired
preference question. Do not reveal which arm used the skill, the intended fix,
the author's verdict, or the other answer during absolute grading. Require
specific output/artifact evidence; a model's own success claim is not proof.

Use a different verified underlying judge model for comparative claims where
available. A provider change, reasoning variant, new role name or fresh session
does not establish independence. Different models still share biases. Record
model identities, host context and actual restrictions; instructions to avoid
tools are not enforced isolation. If these controls are unavailable, label the
run as a limited smoke check and narrow its claims.

Check the judge itself with prepared correct alternatives, actual violations,
warnings mentioning forbidden actions, missing-input cases, and responses that
try to instruct the judge. A valid abstention identifies missing input,
conflicting criteria or an unobservable claim. It must not excuse an ordinary
wrong answer to an answerable task. Human/source-based spot checks remain useful
even when model judges agree. Keep preference and verbosity assessments separate
from correctness, and do not reward empty brevity.

## Compare revisions without optimizing to a known answer

Freeze a small set of task-local prompts and accepted outcome criteria before
running old and revised guidance under matched target conditions. Use fresh
contexts, equal capabilities and recorded instruction identities. Keep some
nearby cases unseen during editing. A no-skill baseline answers a different
question from an old-skill versus revised-skill comparison; do not conflate them.

Retain contrary outcomes and blocked runs. Do not rerun a losing sample until it
passes or count corrections to one task as independent successes. Repetitions
measure variation within a case; they do not create new task coverage. Inspect
both the output and the trajectory when claiming execution quality or cost.

Make the smallest justified method change, preserving positive practices and
scope. A sound correctness repair can be warranted without a statistically
meaningful benchmark gain. Conversely, several successful probes do not prove
general improvement. Report separately what was authored, deterministically
validated, behaviorally observed and left unmeasured.
