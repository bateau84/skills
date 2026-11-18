# Designer craft: verification record

Date: 2026-11-18. This record covers the methodology revision introducing
`visual-art-direction` and connecting it to experience, prototyping, handoff,
and validation. It records checks actually performed, not a design-quality
benchmark.

## Deterministic checks

- `python3 -I -B scripts/run_evals.py --validate` — valid: 507 cases across 106
  skills; the validator made zero provider calls.
- Changed Markdown frontmatter parsed, fenced blocks were balanced, local
  Markdown destinations resolved, and changed JSON files had unique case IDs.
- `git diff --check` — clean in both the skills and companion agents repositories.
- The affected skill fixtures contain 35 cases, including 19 new cases. The
  companion Designer fixture adds four synthetic cases. Fixture existence and
  schema validity do not mean those cases were behaviorally passed.

## Fresh-context task probes

Three separate hosted-agent sessions received one candidate practitioner file
and the task below. They did not inherit the author's conversation, diagnoses,
expected answers, or previous verdicts. They were instructed not to read eval,
assessment, or QA files, not to edit files or use external services, and to use
only direct practitioner references if needed. Their textual responses were
inspected by the author against the task. This is a limited forward test, not
an independently scored performance comparison.

### Expressive visual direction

Practitioner: `skills/visual-art-direction/SKILL.md`.

Task:

> Refine the visual direction for a playful music discovery app. Accepted brand
> decisions are saturated gradients, rounded controls, and a widely used
> sans-serif family. People browse cover art, preview tracks, and save albums;
> no new features are requested. We want it to feel crafted rather than generic,
> on phone and desktop. Routine design choices are delegated to you. Available
> design evidence is this brief only; no screenshots, rendering, or user research
> are provided. Produce a useful concise direction and implementation handoff,
> with evidence limits.

Observed response: retained the accepted expressive ingredients; made cover art,
album metadata, preview, and save form a consistent hierarchy; adapted phone and
desktop density; treated proposed colors and dimensions as initial settings; and
explicitly left rendered quality, contrast, usability, accessibility, and audience
response unverified. It did not reject the brand through a style blacklist or
claim to have rendered a screen.

### Early visual prototype

Practitioner: `skills/prototyping/SKILL.md`.

Task:

> We are choosing a visual direction for a mobile reading app. The question is
> whether an editorial layout with generous type and imagery or a compact
> library-led layout makes the collection inviting while preserving readable
> long titles. Search behavior is still being discussed separately. We can render
> static phone-sized views now; no native prototype or user study is available.
> Recommend the smallest useful prototype exercise and concrete output/evidence
> boundaries so we can decide this visual question now.

Observed response: recommended a comparable pair of static views with the same
content and conditions; did not block visual work on unsettled search; included
long-title cases; distinguished team aesthetic judgment from user preference;
and limited conclusions to sampled appearance. It proposed an exercise, as
requested, rather than claiming that rendering or a native test had occurred.

### Accepted craft versus pixel differences

Practitioner: `skills/design-validation/SKILL.md`.

Task:

> Validate from these supplied observation notes; do not claim you personally
> opened the app. Accepted visual design for an incident timeline: chronological
> reading spine, compact timestamp alignment, readable long notes, restrained
> severity emphasis, secondary notes region on wide screens. Observed build
> abc123 at 1440x900 with representative long notes: all tokens match, but
> implementation puts each event in an equally prominent large card; chronology
> is split across alternating columns and the notes region dominates the first
> view. Observed at 390px: all notes remain reachable in chronological order.
> A secondary icon is 2px larger than the reference without affecting meaning
> or alignment. Keyboard and screen-reader use were not exercised. Report
> concrete findings and evidence limits.

Observed response: identified chronological composition and notes prominence as
accepted-design drift despite token consistency; accepted the harmless icon
variation; treated the narrow observation as partial positive evidence; and left
keyboard, assistive technology, readability, and other unobserved assertions
unverified. It attributed observations to the supplied notes and did not claim
direct product inspection or measured task slowdown.

## Candidate content identifiers

These SHA-256 values identify the practitioner content supplied for the probes.
They are not native skill-load instrumentation or a tool-execution attestation.

| Practitioner | SHA-256 |
| --- | --- |
| `visual-art-direction` | `cc3dcae4a78a40d259df6e57b241dd3cc10c38b5eea43569132b839160fb1f2a` |
| `prototyping` | `0081c99c2314978d3342e1b5ece4015d8b9e71ef5be5744750a6ab444799d279` |
| `design-validation` | `a816064b8ec0c7b751a2240ffec336e7900d03068ab76a45e8ac3293bacbfc7c` |

## Independent review

A separate fresh-context reviewer examined the changed source, companions,
fixtures, and research reference without earlier reviewer opinions or these
probe outputs. It found no material issues in the changed scope, checked the
relevant W3C corrections, and confirmed the 35 skill cases plus four Designer
cases parsed. It did not render products or run a design-quality benchmark.
The author reviewed this verification record separately.

## What remains unverified

No baseline-versus-revision experiment, rendered UI comparison, representative
user study, native OpenCode skill-loading trial, or broad behavioral fixture run
was performed. The probes involved one response per task with no repetitions and
no blinded external scoring. They support only the described instruction-following
observations. They do not establish that people prefer the revised designs or
complete tasks more effectively.

The [methodology reference](../skills/visual-art-direction/references/design-methodology.md#evaluate-the-method-and-its-outputs)
describes how to evaluate those broader claims. The PR should be judged as a
research-grounded instruction and coverage improvement with explicit remaining
empirical questions.
