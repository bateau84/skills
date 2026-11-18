# Design methodology and evidence

This reference combines useful experiences, visual quality, and innovation.
It is an original synthesis informed by primary sources, reviewed on 2026-11-18.
The recommendations are professional
judgment, not a validated universal process or proof that an agent produces
better designs. Use the parts that resolve the task's uncertainties; this is not
a specification, additional approval gate, or required sequence of artifacts.

## Contents

- [Keep the quality dimensions distinct](#keep-the-quality-dimensions-distinct)
- [Organize work around uncertainty](#organize-work-around-uncertainty)
- [Turn intent into visual decisions](#turn-intent-into-visual-decisions)
- [Make innovation earn its complexity](#make-innovation-earn-its-complexity)
- [Adapt across surfaces](#adapt-across-surfaces)
- [Example: an operations tool](#example-an-operations-tool)
- [Evaluate the method and its outputs](#evaluate-the-method-and-its-outputs)
- [Read the evidence within its limits](#read-the-evidence-within-its-limits)

## Keep the quality dimensions distinct

A coherent design connects several dimensions without treating one as proof of
the others:

| Dimension | Question | Evidence that helps |
| --- | --- | --- |
| Value | Does this solve a worthwhile problem? | Observed work, existing research, unmet needs, outcome evidence. |
| Usability | Can people understand and complete the task? | Representative task attempts, errors, recovery, effort, and learning. |
| Accessibility | Can people with different abilities use it? | Applicable standards, implementation checks, assistive technology, and participation by disabled people. |
| Aesthetic quality | Is the composition coherent, appealing, and carefully resolved? | Rendered critique and appropriately sampled human judgments. |
| Character | Does the experience express the intended identity and feeling? | Product context, accepted direction, contextual user response. |
| Innovation | Does a different approach produce a meaningful benefit? | Comparison with the existing or conventional approach, including added costs. |

An attractive screen can hide a broken journey. A technically accessible flow
can remain confusing. Consistent tokens can produce an anonymous interface.
Conversely, a familiar component or dense layout can be exactly right. Assess
the combination in context instead of collapsing it into a single quality score.

[Apple's design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles.md)
bring purpose, agency, familiarity, flexibility, craft, and delight together.
Their practical implication here is to make the intended experience explicit:
calm during an incident, inviting during exploration, or precise during editing.
These are platform principles rather than evidence that a particular palette
will cause a particular emotion. Ask people when their response matters.

## Organize work around uncertainty

Start with what is least understood and most consequential. If the problem is
unclear, study the work before choosing a feature. If the task is established
but the interaction is unfamiliar, compare ways to perform it. If the structure
works but feels generic, investigate visual direction. A local refinement
within an accepted language usually needs inspection and correction, not a new
discovery exercise.

The [Design Council's framework](https://www.designcouncil.org.uk/resources/framework-for-innovation)
describes divergence and convergence for understanding problems and developing
solutions, and explicitly describes a nonlinear process. Apply that distinction
at the scale of the actual decision. Explore enough alternatives to escape the
first plausible answer, then choose using the task, constraints, and evidence.
Do not manufacture a fixed number of directions for a settled detail.

For an open direction, compare consequential alternatives using the same content
and equivalent states. Change the information relationship, interaction model,
density, or character. Three recolorings offer little evidence about structure.
Record why a promising alternative was rejected so it does not return merely
because its screenshot looks attractive in isolation.

Choose the prototype by the question. [Houde and Hill's model](https://hci.stanford.edu/courses/cs294h/2006/readings/houde-prototypes-97.pdf)
distinguishes a product's role, look and feel, and implementation. Visual finish
does not establish completeness. A walkthrough can expose a recovery problem;
an interactive sketch can test navigation; realistic rendered content can reveal
poor composition; a technical experiment can test a dependency. None substitutes
for the others. Label simulations and unsupported capabilities clearly.

Return to earlier decisions when evidence warrants it. Typography may expose
labels that are too long. A mobile prototype may reveal an unnecessary step.
Visual and behavioral work should inform each other while decisions are still
cheap to change.

## Turn intent into visual decisions

Write a small direction statement tied to the product. Replace vague adjectives
with consequences: a calm operational interface might use stable alignment,
limited competing emphasis, readable dense rows, and clear status language.
An exploratory collection might need larger imagery and a more varied rhythm.
Neither direction establishes a universal style or a prescribed component set.

Inspect the current product and a few useful references. For each, explain the
mechanism worth learning from, the context that makes it work, and what should
not transfer. A readable financial table can inform a monitoring view; its
commercial branding might be irrelevant. An editorial composition can suggest
hierarchy without supplying suitable navigation. References support reasoning;
they do not excuse copying an entire layout or inventing a claimed inspection.

Develop the whole composition before polishing isolated components. Identify
where attention should begin, which information belongs together, and how the
eye moves between groups. Compare the strength of headings, controls, data, and
imagery. Choose whitespace and density according to reading and task needs.
An oversized title can waste a monitoring viewport; generous space can improve
a focused reading experience. Symmetry and asymmetry are both available tools.

Treat typography as both communication and expression. Choose roles, weight,
measure, line height, wrapping, fallback behavior, and numeral treatment using
real content. Inspect long labels and target sizes. [Material's typography
guidance](https://m3.material.io/styles/typography/applying-type) distinguishes
expressive display and headline roles from longer, more utilitarian text, while
acknowledging platform and implementation constraints. This supports purposeful
variation, not a mandatory font pairing or universal pixel scale.

Use repeated proportions and spacing roles to create rhythm, allowing reasoned
optical corrections. Give color, material, imagery, and motion coherent jobs:
meaning, recognition, emphasis, character, or an appropriate sensory experience.
An effect is weak when it contradicts the task or direction, not merely because
it is fashionable. Diagnose interchangeable layouts, meaningless ornament,
generic content, and neglected states instead of maintaining a style blacklist.

Inspect rendered results from the whole view to the details, refine the observed
mismatch, and inspect the change. Include the content volume and states that
could break the direction. A beautiful empty screen says little about a full
table. A still image cannot establish motion quality, responsiveness, or the
cost of repeating an animation throughout a workday.

## Make innovation earn its complexity

State the proposed benefit relative to a familiar baseline. A useful hypothesis
names the person, difficulty, proposed mechanism, expected benefit, and evidence
that would weaken it. For example: grouping related events might reduce the work
of reconstructing an incident, but could hide a critical outlier. Test both.

Count costs as well as benefits: learning, discovery, extra decisions, errors,
latency, attention, maintenance, and reduced control. Evaluate first use and
repeated use when they differ. Retain a discoverable path when an expert shortcut
is useful. Familiar navigation and a distinctive presentation can coexist;
novelty need not be spread across every control.

For AI functionality, [Google PAIR's user-needs guidance](https://pair.withgoogle.com/guidebook-v2/chapter/user-needs/)
asks whether AI adds distinctive value and distinguishes automation from
augmentation. Compare a simpler solution. Make correction, inspection, and
recovery possible where consequences matter. State what is known about actual
capabilities and what remains proposed. A plausible generated explanation does
not prove that a system can safely perform the action it describes.

Innovation may come from better defaults, less context switching, useful
previews, direct manipulation, reversible actions, or composable operations.
If a new feature or changed product promise exceeds the assignment, present it
as a hypothesis for the appropriate owner. Visual design authority does not
authorize scope expansion.

## Adapt across surfaces

Preserve the needed outcomes, terminology, state meaning, and identity while
adapting the interaction. [Fluent's principles](https://fluent2.microsoft.design/design-principles)
combine familiar platform patterns with distinctive signature experiences.
Product coherence therefore need not mean identical controls or a desktop
layout compressed into every viewport.

The following matrix is a starting point for selecting evidence, not a complete
platform standard. Use only the surfaces relevant to the product.

| Surface | Design emphasis | Useful evidence and its limit |
| --- | --- | --- |
| Web | Content flow, responsive composition, browser navigation, meaningful URLs, zoom, keyboard and touch. | Rendered widths and task interaction; a screenshot does not prove navigation or semantic accessibility. |
| Mobile | Touch, reach, safe areas, keyboard intrusion, readable scaling, interruptions and resumed work. | Target-device or simulator journeys; simulator images alone do not establish physical ergonomics. |
| Desktop | Productive density, window resizing, keyboard efficiency, pointer behavior, native menus and focus. | Running native views and representative input/window conditions; browser mockups have limited native fidelity. |
| CLI | Discoverable commands, clear help and errors, scannable output, progress, predictable composition. | Transcripts plus stdout/stderr, exit status, piped and noninteractive behavior; decoration must not corrupt machine output. |
| TUI | Character-grid composition, stable focus, selection, keys, resizing, palettes and glyph constraints. | Terminal captures and keyboard journeys at representative sizes/configurations; snapshots do not prove assistive-technology access. |
| Conversation or voice | Clear turns, concise prompts, correction, interruption, completion and handoff. | Dialogues and actual interaction; spoken pacing and listenability require audio/timing evidence. |

[Apple's layout guidance](https://developer.apple.com/design/human-interface-guidelines/layout)
addresses available space, text-size changes, and recognizable adaptation.
[GNOME's accessibility guidance](https://developer.gnome.org/hig/guidelines/accessibility.html)
provides concrete checks for high contrast, larger text, keyboard, and screen
readers. These guide their respective platforms; do not transplant their exact
sizes or conventions into unrelated environments.

[CLI Guidelines](https://clig.dev/) supports human use and composability, but
explicitly excludes full-screen terminal applications. For TUI evidence,
[Textual's testing documentation](https://textual.textualize.io/guide/testing/)
demonstrates interaction simulation, size variation, and snapshot comparison;
those mechanisms detect behavior or change, not aesthetic excellence.
[Google's conversation guidance](https://developers.google.com/assistant/conversation-design/learn-about-conversation)
offers turn-taking and relevance principles. Its older Actions platform context
should not be mistaken for a current implementation recommendation.

When a journey crosses surfaces, specify what context must travel: the selected
object, progress, filters, draft, or pending action. Decide how stale state or
conflicting edits become visible. A shared identifier is insufficient if people
must reconstruct the task after every transition. These continuity decisions
belong in the experience and interaction design, with capability dependencies
made explicit.

## Example: an operations tool

Consider a hypothetical tool for investigating service incidents. This example
proposes design ideas; it does not describe existing or validated capabilities.

The intended experience is calm, precise investigation under time pressure. The
main question is what changed and what evidence supports a response. A visual
direction might use stable rows, aligned timestamps, readable metrics, restrained
status emphasis, and a clearly related evidence panel. Large promotional
headings or equally prominent cards would compete with this task. That judgment
comes from the scenario, not a rule against headings or cards.

Compare a familiar event list with a proposed grouped timeline. The hypothesis
is that grouping reduces reconstruction effort. Use the same realistic sample
events, including an unrelated critical event, delayed data, and a missing
source. Observe whether grouping helps and whether users can see its limits.
An optional proposed summary must remain distinguishable from source evidence.
Whether reliable grouping or summarization is technically available is a
separate question for implementation evidence.

On desktop, a list and evidence pane could support comparison. On mobile, the
same incident might open with essential status and an accessible path to the
evidence. A TUI could offer stable panes and explicit selection; a CLI could
provide a concise human summary and separately defined structured output. A
conversational surface could answer a bounded question and link back to the
relevant incident. Design only the variants justified by actual user needs.

If cross-surface handoff is proposed, specify which incident, time window, and
selection survive, and how freshness is shown. If taking action is in scope,
design its consequences, authority, and recovery explicitly. No attractive
prototype or fluent response establishes permission or operational safety.

## Evaluate the method and its outputs

For a particular product, compare the observed design with its accepted intent
and representative journeys. Separate failures, drift, craft opportunities,
preferences, and unverified assumptions. A preference for another style is not
automatically a defect. Use the smallest refinement that resolves the material
issue, and stop when evidence supports the agreed quality bar.

For evaluating changes to Designer or its skills, use a comparison designed to
isolate the changed instructions:

1. Keep briefs, model configuration, tools, source content, and time or compute
   budget comparable. Record exact instruction revisions and any deviations.
2. Use multiple briefs across relevant product types and surfaces, including
   constrained refinements and open directions. Generate multiple samples;
   retain failed and ordinary outputs, not only the best example.
3. Randomize presentation order and conceal which instruction version produced
   each candidate when gathering preference judgments. Ask about coherence,
   craft, task fit, and intended character with room for reasons and ties.
4. Assess representative task completion, recovery, accessibility, and technical
   feasibility separately. A preferred screenshot cannot compensate for an
   inaccessible critical action. Use equivalent content and state coverage.
5. Report who judged, what they observed, variation between samples, exclusions,
   and uncertainty. Distinguish agent critique from user evidence. Small samples
   can reveal issues without establishing a population-wide improvement.

[W3C guidance on involving users](https://www.w3.org/WAI/test-evaluate/involving-users/)
recommends combining participation by disabled people with standards-based
evaluation and cautions against generalizing one person's experience to all
users. Include this perspective throughout relevant work rather than treating
accessibility as a final visual inspection.

For website aesthetics, the original [VisAWI-S study](https://www.uni-muenster.de/OWMS/uploads/drafts_thielsch/pdf/moshagen_thielsch_2013.pdf)
provides a researched measure of perceived visual aesthetics. Its website and
language context matters. Adapting its concepts for a terminal or an agent rubric
does not transfer the instrument's validation. Use an informal rubric honestly
when that is sufficient.

No output benchmark, user study, or live UI evaluation was performed in creating
this reference. Stronger instruction coverage is a testable improvement
hypothesis, not an observed gain in design quality.

## Read the evidence within its limits

Research can challenge assumptions without providing a recipe. A
[Google-authored CHI 2026 study abstract](https://research.google/pubs/usability-hasnt-peaked-exploring-how-expressive-design-overcomes-the-usability-plateau/)
reports improved task performance and aesthetic ratings for Material 3
Expressive variants in a study of 48 participants and 10 mobile applications.
Only its abstract was reviewed here. It supports investigating whether expression
and usability improve together; it does not establish superiority for every
style, product, or surface.

Platform guidance expresses informed design positions. Methodology papers offer
ways to reason. Controlled studies provide findings within their tested
conditions. Actual product evidence determines whether a choice works here.
Keep these sources of confidence separate, revisit uncertain decisions, and
preserve the rationale and examples that allow the next designer or implementer
to continue the work coherently.
