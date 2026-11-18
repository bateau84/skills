---
name: visual-art-direction
description: Shape distinctive, beautiful, coherent interfaces through product-specific visual intent, references, composition, typography, and rendered critique. Use for a new visual direction, a generic-looking UI, visual polish, expressive product design, or adapting an identity across web, mobile, desktop, and terminal surfaces. Not for defining product scope, interaction contracts, or implementing production UI.
---

# Visual Art Direction

Make the product feel deliberately designed for its people, content, and setting. Beauty, clarity, and useful functionality are related goals; none proves the others. An interface can be expressive or restrained and still be excellent.

Use `experience-design` for an unsettled human problem or useful-innovation hypothesis, `visual-interface-design` for visual semantics, the relevant surface and accessibility skills for constraints, `prototyping` for unresolved questions, and `design-specification` for the handoff. Load only what the task needs. This skill supplies visual judgment; it does not expand product scope or authorize implementation.

## Choose the depth

For a bounded refinement within an accepted language, inspect the surrounding interface and improve the affected detail. Do not reopen the brand, produce alternatives, request new approval, or create a design-system document by default.

For an open visual direction, use the following method as an iterative loop. Start with the uncertainty that matters most; visual exploration can reveal an information or interaction problem. Do not defer all visual thinking until behavior is frozen, or let a beautiful mockup settle unresolved behavior.

## Establish the direction

1. **Read the product.** Inspect existing screens or outputs, accepted design guidance, realistic content, audience, main tasks, devices, and constraints. Distinguish observation from assumptions. Preserve a coherent existing language unless changing it is in scope.
2. **Write a compact visual brief.** Connect the desired character to the experience: what should the person feel, notice, and understand here? Translate words such as calm, precise, warm, playful, or editorial into concrete choices about hierarchy, density, type, color, imagery, and motion. Record what would undermine the intent. A few sentences can be enough.
3. **Use references critically.** When helpful and available, inspect a small, varied set of relevant examples, including the current product. Explain the mechanism worth learning from: a readable dense table, a distinctive type rhythm, a useful native interaction, or an appropriate emotional tone. Keep source links and identify what to borrow in principle and what does not fit. Do not copy a whole competitor layout or claim to have inspected unavailable examples.
4. **Explore meaningful alternatives when direction is open.** Compare a small set that changes the consequential choices: composition, hierarchy, density, interaction model, or character. Recoloring the same template is weak exploration. A familiar conventional option can be the strongest answer. Use the same content and comparable states so polish or invented data does not bias the choice.
5. **Choose and explain.** Select against the task, intended character, accessibility, platform fit, feasibility evidence, and accepted constraints. State the trade-off. Use delegated design authority for ordinary craft decisions; surface only unresolved decisions that actually belong to the user or another owner.

## Give craft concrete form

Treat the following as lenses for judgment, not a checklist that prescribes one style.

| Lens | Make deliberate choices about |
| --- | --- |
| Composition | A clear attention order, useful grouping, alignment, balance, and the relationship between the whole view and its parts. Use asymmetry or symmetry when it serves the intent. |
| Typography | Family and fallback, roles, weight, size, line height, measure, wrapping, numerals, and optical alignment. One well-used family may be enough. Inspect real labels, long text, localization, and target sizes. |
| Rhythm and density | Spacing within and between groups, repeated proportions, reading pace, and how much information a task needs in view. Dense expert tools and relaxed reading surfaces need different treatment. |
| Color and material | Semantic roles plus the product's emotional and identifying character. Decorative color, texture, gradients, depth, and illustration are allowed when they support intent and preserve readability and state meaning. |
| Content and imagery | Actual product vocabulary and credible content. Use imagery with a clear role and consistent treatment; distinguish illustrative sample data from real metrics, testimonials, and capabilities. |
| Interaction and motion | Feedback, continuity, responsiveness, and appropriate moments of delight. Check repeated-use cost, interruption, user control, and reduced-motion alternatives. A still image cannot establish these. |
| Coherence | A recognizable language across views, components, states, themes, and supported surfaces, with reasoned exceptions rather than compulsory uniformity. |

Use token scales as a shared vocabulary, not a ban on optical corrections. Do not invent universal rules such as a minimum four-pixel type step, mandatory monospace for every numeric table, a fixed font pairing, or a required amount of whitespace. Legibility, meaning, platform requirements, and rendered results decide whether a choice works.

## Diagnose generic output

Translate “AI slop” into a concrete observation and its consequence. The label alone is not a design finding.

- **Interchangeable structure:** Could the logo and nouns change while the same composition purportedly serves an unrelated product? Inspect whether task hierarchy, data shape, and content have affected the design. Shared conventions can still be appropriate.
- **Template-driven hierarchy:** Are all sections equal-sized cards despite different importance or information relationships? Does an oversized heading displace the information people need?
- **Unmotivated effects:** Do gradients, glass, badges, shadows, icons, or animations compete with the task or contradict the intended character?
- **Impersonal content:** Do generic slogans, stock illustrations, fabricated numbers, or repeated placeholder text conceal the product's actual value?
- **Polished fragment:** Does only the hero or empty state look considered while dense content, errors, navigation, and narrow layouts fall apart?

Cards, gradients, popular fonts, rounded corners, and minimalism are not defects by themselves. Keep an effect that earns its place. Correct the observed mismatch; do not replace one fashionable recipe with another or force novelty into familiar controls.

## Adapt the language to the surface

Preserve meaningful identity, vocabulary, states, and outcomes. Adapt the expression to the person's task and the surface's capabilities. Design only the surfaces the product needs.

| Surface | Craft and interaction priorities | Useful direct evidence |
| --- | --- | --- |
| Web | Responsive composition, content flow, browser navigation, zoom, keyboard and touch; no hover-only essential action. | Rendered views at representative widths and zoom, plus browser task interaction. |
| Mobile | Reach, touch, readable scaling, safe areas, keyboard occlusion, interruptions, orientation and available space; adapt the task rather than shrink desktop. | Target-device or simulator views and task interaction; real-device evidence for ergonomic claims. |
| Desktop | Window resizing, multiple panes/documents, keyboard efficiency, native conventions, focus, menus, and system appearance. | Running native views and representative window/input conditions; browser mockups have limited native fidelity. |
| TUI | Character-grid alignment, useful density, stable focus/selection, discoverable keys, resize behavior, terminal palettes and glyph fallbacks. | Actual terminal captures and interaction at supported sizes/themes; include no-color or limited-color conditions as applicable. |
| CLI | Wording, grouping, scannable human output, concise help and errors, progress, quiet operation, and composable streams. | Real transcripts, stderr/stdout and exit status, redirected/non-interactive output; visual ornament must not corrupt machine output. |
| Conversation or voice | Clear turns, concise language, understandable state, repair, interruption, and a usable way to inspect or correct consequential actions. | Representative transcripts and actual interaction; audio/timing evidence for spoken claims. A screenshot cannot prove conversational quality. |

Use current platform guidance when its exact behavior matters. These priorities are a starting point, not a complete platform specification. If a task crosses surfaces, preserve the needed context and progress while adapting navigation and controls.

## Render, inspect, refine

1. Identify what the available tools can actually show. Render or capture the candidate on the target surface when possible. Record whether the evidence is a static mockup, interactive prototype, or real implementation, and its revision, size, state, and content.
2. Inspect the whole composition and a representative task, then the type, spacing, alignment, controls, imagery, and motion that matter. Check realistic content volume and applicable narrow, dense, empty, error, focus, and theme states. Choose coverage by risk, not an exhaustive screenshot quota.
3. Compare with the visual brief and accepted references. Name the specific observation, why it matters, and the smallest useful refinement. Separate a functional or accessibility defect, drift from accepted visual intent, a craft opportunity, and personal preference.
4. Refine the strongest direction and inspect the changed result. Stop when the material questions are resolved and the agreed quality bar is supported. Do not invent mandatory iteration counts or keep redesigning because another style is possible.
5. Report the evidence boundary. Expert critique can judge an observed composition; it is not proof of user preference, task success, emotional response, accessibility conformance, or implemented capability. Without rendered access, provide a provisional direction and identify the checks that remain.

For evaluating an existing implementation, use `design-validation` and report findings; correction needs the task's existing authority. Do not silently redesign during validation.

## Preserve the intent

Hand off the chosen character and rationale, the consequential visual choices, representative examples, supported surface adaptations, relevant states, and the observed/unverified checks. Separate accepted decisions from illustrative references and open choices. Behavior must stand without images; visual intent must also be specific enough that implementation does not have to invent the identity.

Use an existing `DESIGN.md` or equivalent for product-wide language when that is within scope: type/color/spacing roles, content and imagery treatment, motion principles, examples, and justified exceptions. Keep feature behavior in its existing design artifact. Do not create a new artifact or approval stage for every refinement.

## Deeper guidance

- Read [Design methodology and evidence](references/design-methodology.md) for the research synthesis, source limitations, cross-surface trade-offs, and an evaluation approach. The practical method above does not depend on reading it.
- Use [ASSESSMENT.md](ASSESSMENT.md) for reviewing art-direction work and [QA.md](QA.md) for challenging apparently strong evidence. These are optional review perspectives, not permissions or independent review by themselves.
