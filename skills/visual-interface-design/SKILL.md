---
name: visual-interface-design
description: "Surface-independent visual design reasoning: use type, color, spacing, and visual hierarchy to communicate meaning and express an accepted product character. Use for visual decisions in web apps, mobile and desktop GUIs, TUIs, or CLI output. For a new aesthetic direction, compose with visual-art-direction. Not for surface rendering mechanics, interaction behavior (use interaction-design), or accessibility implementation (use accessibility-implementation)."
metadata:
  version: "1.1.0"
---

# Visual Interface Design

## What this skill is for

Use type, color, spacing, size, weight, contrast, and position to communicate meaning, guide attention, and create a coherent, attractive interface with the intended character. Judge these goals together: beauty does not establish usability, and correct semantics alone do not establish visual quality.

**The foundational test:** What does this choice contribute to the task, visual coherence, or intended character, and what does it cost in legibility, attention, or consistency? Aesthetic purpose is legitimate. Make it concrete against the brief and rendered composition; do not require every decorative detail to encode information.

**Load this skill when:**
- Making visual decisions that communicate meaning: hierarchy, status, state, type, category, action affordance
- Designing visual systems for application interfaces: dashboards, forms, tools, data tables, monitoring views
- Specifying the visual semantics section of a Design Spec
- Evaluating whether a described visual design correctly communicates its intended meaning

**Compose with project-specific visual guidance when useful:**
- For products with application and marketing surfaces, preserve a coherent design language while respecting their different user goals. No external design skill is required.
- Use `visual-art-direction` when defining a visual direction, diagnosing generic output, or making consequential craft choices. For a bounded refinement, preserve the accepted language and improve the affected detail without reopening the identity or requiring alternatives.

**Do NOT load this skill when:**
- Producing framework-specific marketing-page layouts: use the project's design system and implementation conventions; this skill focuses on visual reasoning.
- Choosing surface rendering mechanics: ANSI color codes, CSS layout engines, rendering APIs (→ `tui-design`, `web-ui-design`)
- Specifying interaction states or behavior (→ `interaction-design`)

**Reasoning and implementation boundary:**
This skill teaches how to reason about visual hierarchy, semantic color, typography, spacing, iconography, data visualization, motion, dark mode, and surface constraints. Concrete themes, component catalogs, CSS frameworks, and token formats follow the project's design system. Use `design-implementation` to translate an agreed design into UI.

Keep portable visual principles here; put framework-specific rendering recipes in implementation or surface guidance.

---

## Visual hierarchy as attention management

Visual hierarchy is the designed order in which the eye processes elements. It is not decoration — it is the interface's answer to: **what should the user look at first, second, third?**

A hierarchy that serves the system's organizational model rather than the user's attention priorities is a design failure. Structure in code (feature categories, module boundaries) has no obligation to match reading priority. Design must override code organization to produce reading order that serves the user's task.

### The five hierarchy signals

These signals work in combination. Any single signal used alone is fragile; combining two or more creates unambiguous hierarchy.

| Signal | How it works | Use for |
|--------|-------------|---------|
| **Scale** | Larger elements claim more attention. Use a coherent set of levels that fits the content. | Primary vs secondary vs tertiary content |
| **Weight** | Bold draws more attention than regular. Heavy weight signals primary content. | Emphasis within body copy, primary labels |
| **Contrast** | High contrast (dark on light, light on dark) claims attention; low contrast recedes. | Focus indicators, primary actions, critical state |
| **Position** | Top-left is the primary reading-entry point in LTR interfaces. | Primary actions in predictable positions |
| **Color saturation** | Saturated colors attract attention; desaturated colors recede. | Separating primary from supporting information |

**The grayscale test:** Remove all color. Does the hierarchy survive? If the hierarchy depends entirely on color, it will fail for colorblind users and in monochrome contexts (some terminal environments, printed output). Any hierarchy that only exists in color is a design gap.

### Failure: hierarchy that matches code structure

The most common visual hierarchy failure in application interfaces: the visual layout mirrors the system's internal organization (feature categories, module boundaries, database schemas) rather than the user's task priorities. A settings page organized as "Authentication / Authorization / Audit" mirrors the code modules. A user who needs to change their password has no way to predict which module contains it. Redesigning around user tasks ("Account & Security / Notifications / Appearance") requires visual hierarchy that matches what users are looking for, not what the system calls things.

### Gestalt principles applied operationally

Gestalt principles are not aesthetic guidelines — they describe how human visual processing groups elements without conscious reasoning.

**Proximity:** Elements closer together appear related. Cluster form fields for the same concept. Separate groups with whitespace, not just visual dividers. A label 24px below its input field will appear to belong to the input above it, not to the input it labels.

**Similarity:** Elements that look the same belong to the same category. Consistent button shape means "all buttons behave like buttons." Consistent tag styling means "all tags are the same kind of thing." Breaking similarity inadvertently creates false category distinctions.

**Common region:** Elements inside a visible container belong together. Cards, panels, and dialogs exploit this. Overlapping containers create ambiguity — an element visually inside two containers belongs to neither clearly.

**Figure/ground:** Interactive elements must read as figure (foreground, attended-to), not as ground (background, ignored). A button that blends into its container background reads as ground and will not be clicked.

---

## Color as information encoding

Color can encode meaning and establish identity, atmosphere, and visual appeal. Distinguish those purposes so expressive surfaces do not obscure status, content, or actions. Evaluate the palette as a composition, including the visibility of its semantic signals.

### Color roles for application UI

**Foreground / Background:** The surfaces on which content appears, whether neutral or expressive. The relevant text and controls must meet applicable contrast requirements against their actual backgrounds, including gradients and images.

**Brand / Accent:** A coherent palette that identifies the product and supports its character. If an accent also marks interactive affordances, preserve other cues that distinguish controls from decoration.

**Status colors:** Preserve stable, understandable meanings. The following are common starting conventions; use the accepted product and domain language rather than treating the table as a universal palette.

| Status | Convention | What it communicates |
|--------|-----------|---------------------|
| Error | Red (adjusted for medium) | Something is wrong and requires user action |
| Warning | Yellow / Amber | Something may become wrong; user should be aware |
| Success | Green | An action completed correctly |
| Info | Blue | Neutral information, no action required |

Do not casually reverse established status meanings for novelty. A brand color may also appear decoratively when context, labels, and other visual cues keep it distinguishable from status. Check the actual composition for ambiguity.

**Interactive states:** Separate visual treatment for hover, focus, active, and disabled states. See §Interactive state colors below.

### Semantic clarity and expressive color

Ask what each treatment contributes: information, grouping, identity, mood, or visual balance. Decorative color, gradients, texture, and imagery can serve the accepted direction. Refine or remove them when they compete with task priority, reduce readability, resemble misleading status signals, or fragment the design language. A popular effect is neither automatically generic nor automatically appropriate.

### Color accessibility: designing for color blindness

Color blindness affects approximately 8% of males and 0.5% of females. The three common forms each affect different parts of the spectrum:

| Form | Affects | What is lost |
|------|---------|-------------|
| Protanopia | Red receptors | Red appears dark; red-green distinction lost |
| Deuteranopia | Green receptors | Green appears dark; red-green distinction lost (most common) |
| Tritanopia | Blue receptors | Blue-yellow distinction lost |

**The design rule:** Never use color as the only visual means of conveying information, identifying an action, or prompting a response. WCAG 1.4.1 (Level A) requires an additional visual distinction where color conveys meaning; decorative color need not carry information. Useful redundant signals include:
- Status indicators: color + icon (✓, ✗, !, ℹ) + text label
- Chart series: color + line style (solid, dashed, dotted) + data point shape
- Validation state: color + border change + explanatory text

### Contrast ratios

WCAG 2.2 contrast requirements are design minimums, not targets:

| Context | Minimum ratio | Applies to |
|---------|--------------|-----------|
| Text other than large text | 4.5:1 | Text and images of text under 1.4.3 |
| Large text (≥ 18pt, or ≥ 14pt bold) | 3:1 | Large-scale text under 1.4.3 |
| Required non-text visual information | 3:1 | Cues needed to identify controls/states or understand graphics, against adjacent colors, under 1.4.11 |
| Author-supplied focus indicators | 3:1 | Required focus cues against adjacent colors under 1.4.11; this is not the complete set of focus requirements |

**Design practice:** Check contrast before finalizing colors. Apply the criteria to the information they cover: 1.4.3 has exceptions for incidental text and logotypes; 1.4.11 excludes inactive controls and unmodified user-agent appearance. A decorative border is not automatically a required control boundary. Do not use these exceptions to excuse unreadable task content. A body-text pair subject to 1.4.3 must meet 4.5:1 regardless of aesthetic intent.

### Interactive state colors

Make meaningful interactive states distinguishable with appropriate visual cues. The following are possible treatments, not a compulsory appearance recipe for every control:

| State | What to change | Secondary signal |
|-------|---------------|-----------------|
| Default | Baseline | Label, border |
| Hover | Subtle background shift | Cursor change |
| Focus | Visible focus ring (3:1 minimum) | Ring, not just color change |
| Active | Pressed state (shadow inward, slight scale) | Visual compression |
| Disabled | Recognizably unavailable while preserving needed context | Explanation where the reason is otherwise unclear |
| Loading | Progress indicator or loading content | Text/status that remains understandable without motion |
| Error | Red / status-error token | Icon + text |
| Success | Green / status-success token | Icon + text |

### TUI color model

Terminal color support is a design constraint, not just a technical one. Design choices must fall within what the target terminal supports.

**16-color ANSI / 8-color ANSI (VT100 basic):**
8 foreground + 8 background colors with bright variants. Cannot control saturation or lightness — only predefined color names. Design hierarchy using combinations:
- Primary content: default foreground on default background
- Emphasis: bright/bold variants
- Status: reserved semantic colors (red for error, green for success, yellow for warning, cyan for info)
- Structural: use box-drawing characters (─, │, ┌, ┐, └, ┘) for containment rather than color-filled backgrounds

**256-color (xterm-256color):**
Adds a 6×6×6 color cube plus 24-step grayscale ramp. Enables subtle tonal variation for depth, but terminal color rendering varies by terminal emulator — test in both light and dark terminal themes.

**Truecolor (24-bit):**
Full RGB. Most modern terminal emulators support this. Check `$COLORTERM` before assuming truecolor is available; design a 256-color fallback.

**CLI output color principle:** Color in CLI output must be optional. Terminal pagers (`less`), log aggregators, and some CI environments strip ANSI codes; others display them as escape sequences. Honor the `NO_COLOR` environment variable (no-color.org standard). Use color for emphasis only, never as the sole structural signal. Output must be readable without color.

---

## Typography for interfaces

Typography combines family selection, proportion, rhythm, and hierarchy. Choose a voice that fits the product while keeping real content legible and easy to scan at its rendered size.

### Legibility vs readability

**Legibility** is whether individual characters can be distinguished — a font-level property. A font with poorly differentiated letterforms (`1`, `l`, `I` all looking the same) has poor legibility even at large sizes.

**Readability** is whether text can be read comfortably at speed — affected by size, line length, line height, contrast, and spacing. A font that is legible character-by-character may be unreadable in long passages due to tight line height or excessive line length.

Both must be addressed. Legibility is the floor (can they read it at all?); readability determines whether they will sustain reading.

### Type scale for application UI

A type scale is a coherent set of roles and sizes that supports the information hierarchy. Reuse accepted roles where they work; add a level only when the content needs it. The number of sizes is not a quality score.

**Scale design principle:** Judge distinctions through the combination of size, weight, family, spacing, and position in the actual rendering. There is no universal minimum pixel difference between levels. A small size step can work with weight and placement; a larger step can still fail if the composition is confused.

**Common named scale levels for application UI:**

| Level | Typical use | Visual signal |
|-------|-------------|--------------|
| Display / Hero | Empty states, major headlines | Largest; sparing use |
| Heading | Section titles, panel headers | Clearly distinguished from body in the composition |
| Subheading | Group labels, secondary structure | Supporting level distinguished through size, weight, or placement |
| Body | Primary content, descriptions | Regular weight; most content lives here |
| Caption / Label | Metadata, timestamps, helper text | Smaller, often muted color |
| Monospace | Code, paths, terminal output, data | Fixed-width; distinct family |

### Information hierarchy through type

Use type attributes in combination to create unambiguous hierarchy within a component:

- **Weight**: use emphasis to support reading priority. Each additional weight should have a clear role rather than adding arbitrary variation.
- **Size**: distinguish structural levels and consequential content without overwhelming the task.
- **Color**: supporting information may recede, but timestamps or identifiers can be task-critical. Preserve their legibility and appropriate prominence.
- **Style**: italics or other forms can distinguish emphasis, definitions, or a product voice. Inspect legibility in the actual font and context rather than banning a style category.

**Practical example — a data table row:**
- Column header: caption weight bold, muted foreground
- Primary cell content: body weight regular, full foreground
- Secondary cell content (e.g., "updated 3 min ago"): caption size, muted foreground
- Status cell: body size with status icon + color token

### Interface-specific typography decisions

**Table column headers:** Choose case, size, and weight that keep labels readable and distinct from values. Sentence case is a useful default; compact uppercase or other accepted treatments need rendered checking. Left-align text columns; right-align consistently formatted numbers or align decimal separators when comparison needs it. Headers need not be smaller than body text.

**Label/value pairs:** Label above or to the left of value. Label uses caption size and muted foreground. Value uses body size and full foreground. Gap between label and value must be less than gap between pairs (gestalt proximity).

**Error messages:** Full contrast. Do not use muted foreground for errors — urgency must be visually present. Pair with the status-error color token.

**Tooltips:** Small size (caption level), high contrast background, generous padding. Tooltips are transient; their text is secondary. Do not put critical information only in tooltips.

### Monospace for code, data, and terminal output

Use monospace where character-position alignment carries information, such as terminal transcripts and preformatted code. It is also a useful convention for commands and paths; check ambiguous glyphs and long strings at their actual size.

Numeric columns do not require a wholly monospaced typeface. A proportional family with supported tabular numerals can keep digits at equal widths; CSS exposes this through `font-variant-numeric: tabular-nums`. Column layout and consistent number formatting still matter. Tabular numerals do not make letters or arbitrary strings fixed-width, and a requested font feature must be supported by the chosen font.

For structured logs or tables, compare monospace with aligned fields using suitable type and numeral treatments. Preserve scanability, exact values, and readable messages; do not demote useful identifiers merely because they are metadata.

---

## Spacing and rhythm as structure

Spacing is the primary gestalt proximity signal. It groups and separates — without any visual divider — based purely on physical distance between elements.

### Spacing scale

Use an intentional spacing system to create rhythm and grouping. Existing product tokens are the starting point. Common scales include:

**4px base:** 4, 8, 12, 16, 24, 32, 48, 64
**8px base:** 8, 16, 24, 32, 48, 64, 96

These are examples, not required units. Optical alignment, type metrics, borders, and constrained content may justify other values. Inspect whether an exception improves the rendered result while preserving grouping and repeated relationships. Record a reusable exception where needed; avoid both arbitrary drift and mechanically snapping a good optical adjustment back to a grid.

**Internal vs external spacing:** Padding *inside* a container signals "these belong together." Margin *between* containers signals "these are separate groups." The ratio of internal-to-external spacing determines whether the grouping reads clearly. Rule: the space between siblings within a group should be less than the space between different groups.

### Density decisions

Density is a deliberate design decision — not a failure mode and not an automatic success.

**High-density (appropriate for):**
- Data tables with many columns
- Monitoring dashboards with simultaneous metrics
- Code editors and terminal applications
- Expert users who need maximum information per viewport

**Low-density (appropriate for):**
- Onboarding flows where cognitive load reduction matters
- Mobile contexts where touch targets must be larger
- Settings dialogs where users need to read carefully before acting

**Anti-pattern:** Applying low-density spacing conventions from marketing pages to data-dense application interfaces. A monitoring dashboard that uses 48px vertical rhythm for every row wastes screen space and forces scrolling that makes the full picture invisible.

### Vertical rhythm and baseline grid

For text-heavy interfaces, consistent line-height values tied to the spacing scale create vertical rhythm — a predictable cadence that makes sustained reading easier. Text at 16px with 24px line height (1.5×) on a 24px baseline grid aligns with component spacing values at the same multiple.

Vertical rhythm matters more for editorial and form-heavy interfaces than for data-dense dashboard views, where cell height is driven by data density requirements.

---

## Iconography: when it works and when it fails

Icons work only within specific conditions. Outside those conditions, they increase cognitive load rather than reducing it.

### When icons work

1. **With text labels** — always better than icon alone. The icon provides quick visual recognition after learning; the label provides meaning on first encounter.

2. **For universal symbols** — a small set of icons have near-universal recognition: magnifying glass (search), gear (settings), X (close), hamburger (navigation menu), floppy disk (save — legacy but established), play/pause/stop (media), trash (delete). Universal symbols can be used without labels in space-constrained contexts.

3. **In expert interfaces** — users who work in the interface daily develop icon vocabulary over time. A code editor's toolbar can use icon-only controls because users invest in learning them. A consumer onboarding flow cannot.

4. **For status and state** — icons communicate state more efficiently than color alone. A ✓ icon alongside green conveys success to colorblind users. A ⚠ icon alongside yellow conveys warning. Never use status icons without accompanying text for novel states.

### When icons fail

1. **Without labels in novel interfaces** — first-time users cannot infer icon meaning. NN/g research: navigation labels significantly improve task completion rates over icon-only navigation. "Cleaner" icon-only navigation trades discoverability for aesthetics — a bad trade.

2. **For metaphorically clever icons** — an icon requires immediate recognition, not inference. A "collaboration" icon might make sense in retrospect but will not be recognized without prior experience.

3. **At small sizes without sufficient weight** — fine-line icons at 16px collapse into illegible shapes. Icons for interactive use need adequate stroke weight and sufficient size (minimum 24×24px touch target; 16×16px minimum for decorative/read-only icons).

4. **When relying on color alone for meaning** — an icon that is red to mean "error" and the same icon shape that is green to mean "success" will confuse colorblind users. Use distinct icon shapes for distinct states.

### Icon design criteria

When assessing iconography quality:
- Clear, recognizable silhouette at the smallest rendered size
- Distinguishable from adjacent icons in the same context
- Adequate stroke weight — not so fine that it collapses at small sizes
- Not reliant on color alone for its meaning
- Culturally neutral where the application has a diverse international audience (thumbs-up is ambiguous in some regions; check marks are safer)

---

## Data visualization design

Data visualization must preserve truthful comparisons and readable values. Supporting structure and visual character can help, but effects that distort quantities or compete with the data undermine the task.

### Choosing chart types

The chart type must match the comparison the user needs to make:

| Comparison | Chart type | Why |
|-----------|-----------|-----|
| Ranking or comparison of distinct values | Bar chart | Length encodes quantity unambiguously |
| Change over time for continuous data | Line chart | Slope encodes rate of change |
| Correlation between two variables | Scatter plot | Position encodes both variables simultaneously |
| Part-of-whole relationships | Pie chart (≤ 5 segments) | Area encodes proportion |
| Distribution of values | Histogram | Bars show frequency across ranges |
| Many metrics at a glance | Small multiples | Same structure repeated, easy comparison |

**Pie chart limit:** Pie charts are only useful with 5 or fewer segments. With more segments, individual slice sizes become impossible to compare accurately. Prefer a bar chart when segments exceed 5.

**Avoid:** Dual Y-axis charts (implies a relationship between series that may not exist); 3D charts of any kind (perspective distortion misrepresents values); area charts on non-zero baselines (exaggerates differences).

### Data tables

When to use tables vs charts:
- Use **tables** when users need to look up specific values, not just observe overall patterns
- Use **charts** when users need to observe trends, comparisons, or distributions across many data points

**Scannable table design:**
- Align comparable numeric fields consistently; align decimal separators where needed and use tabular digits when stable digit width helps
- Left-align text columns
- Use consistent date/time formatting within a column (ISO 8601 for machine-readable; locale-formatted for human reading)
- Row striping (alternating light/very-light background) aids row tracking in wide tables — use subtle contrast, not high-contrast stripes
- Column headers: legible and distinct from values, using the accepted type roles rather than a compulsory size or case
- Sortable columns: visual indicator of sort state (▲/▼), not just which column sorts

### The chartjunk principle (Tufte)

**Data-ink ratio:** Maximize the proportion of ink that represents data; minimize ink that does not represent data. The following are candidates for removal:

- 3D perspective on bars and pies (adds ink, distorts data)
- Excessive grid lines (thin, light grid lines are acceptable; heavy grids dominate the data)
- Decorative backgrounds and fills on chart areas
- Unnecessary borders around chart components
- Legends that repeat information already labeled on the chart

**Small multiples:** When the same chart structure applied across many datasets needs comparison, arrange the same chart at small scale in a grid. Users can compare across multiples faster than interpreting a single animated chart with toggleable series.

**Sparklines:** "Intense, simple, word-sized graphics" (Tufte) — tiny trend lines embedded alongside data in tables, showing the shape of change without axes, labels, or interactive elements. Appropriate for showing directionality in a data-dense monitoring view without consuming layout space.

### Color for data

**Categorical data:** Assign distinct colors to categories. The colors must be distinguishable for colorblind users — test with protanopia and deuteranopia simulators. Do not use more categories than can be clearly distinguished (practical limit: 8–10 colors maximum).

**Quantitative magnitude:** Use a sequential palette (light→dark within a single hue) that progresses monotonically. A darker shade should always encode a higher value. Avoid rainbow palettes for quantitative data — they imply categorical boundaries that do not exist in the data.

**Bipolar data (positive/negative, hot/cold):** Use a diverging palette (blue→white→red for negative/neutral/positive) where the midpoint is visually neutral and the two poles are perceptually distinct.

---

## Motion as communication

Motion can clarify change, maintain orientation, and express appropriate product character. Give it a purpose and inspect its attention, repetition, accessibility, and interaction costs. An expressive flourish can fit the brief; it must not obscure state or make routine work wait.

### What motion should communicate

**State change:** An element appearing signals it has entered the visible state. Disappearing signals it has left. Collapsing/expanding signals a density change. Without motion, abrupt appearance can disorient; with motion, the user knows something happened.

**Causality:** A shared-element transition (an element moves from one location to another across a navigation) connects cause and effect in the user's mental model. The user sees that the card they tapped became the detail view they are now seeing.

**Direction:** Slides in from the right = navigating forward. Slides in from the left = navigating back. This directional language must be consistent across the application or the spatial model collapses.

**System status:** A spinner communicates "something is happening." A progress bar communicates "something specific is happening and here is how much remains." A completion animation communicates "the action is done." Preserve truthful status independently of its animation.

**Character:** A brief transition or celebratory detail can support an accepted expressive direction. Judge where it appears, how often it repeats, and whether it fits the person's task. Do not turn delight into a quota or ban it for lacking a separate information payload.

### What motion must not do

**Slow task completion:** Do not make users wait for nonessential animation before their next action. Keep feedback prompt and routine transitions brief, interruptible where appropriate, and coherent under repeated input. Choose timing for the distance, input, task, and platform; verify it through interaction rather than treating a universal millisecond limit as proof of quality.

**Disregard motion sensitivity:** Large movement, zoom, and parallax can trigger vestibular symptoms. WCAG 2.3.3 (Animation from Interactions, Level AAA) requires that interaction-triggered motion animation can be disabled unless essential to the functionality or information conveyed. It is not a ban on all animation. Honor reduced-motion preferences as a design practice even when the agreed conformance target is AA.

**Distract from content:** Continuous peripheral effects can compete with reading and concentrated work. Avoid animating dashboard metrics merely to make them appear live; a clear value/update state may suffice. WCAG 2.2.2 (Level A) requires pause/stop/hide controls for nonessential automatically moving, blinking, or scrolling information that lasts over five seconds alongside other content. Automatic updates alongside other content need pause/stop/hide or frequency control unless essential; they have no five-second exception.

### Designing for prefers-reduced-motion

`prefers-reduced-motion: reduce` is a user OS setting that should be honored. The behavior must not be: "all animations are removed, the interface breaks." The correct design is:

- Remove or replace nonessential movement with a stable treatment; simply shortening it is not always an adequate alternative.
- Preserve state, progress, and outcomes through visible content and suitable non-color cues when motion is removed.
- Stop nonessential ambient motion and preserve the applicable controls for moving or auto-updating content.
- If motion is essential to the actual function, such as previewing an animation being edited, explain that dependence and provide appropriate controls instead of falsely promising an equivalent static experience.

**Design rule:** For ordinary navigation and status feedback, make the stationary states understandable first. Specify the motion and reduced-motion treatments together, then inspect them with actual interaction when available.

---

## Dark mode as a distinct visual design

Dark mode is not color inversion. Programmatically inverting a light-mode color palette produces: shadows on dark surfaces (which look wrong — shadows recede from light, not from dark), semantic colors that are illegible (pure red on pure black), and text contrast that is overwhelming (pure white on pure black causes halation and eye strain). Each of these requires deliberate redesign.

### Surface layering in dark mode

In **light mode**, elevation (Z-axis depth) is expressed through shadows on a light surface. Shadows darken the surface beneath a raised element, simulating depth.

In **dark mode**, shadows are barely perceptible on dark surfaces. Elevation must instead be expressed through **surface lightness**: the elevated element's background is lighter than the surface below it. A card on a dark-mode background is lighter than the background. A modal or popover is lighter still. The hierarchy inverts: lighter surfaces are closer in dark mode.

This is the Material Design "surface tonal overlay" approach and is also reflected in macOS dark mode — the system background is darker; elevated panels are lighter.

### Text on dark backgrounds

**Avoid pure white on pure black:** The maximum-contrast combination (white #FFFFFF on black #000000) produces halation — the text appears to blur at its edges due to the extreme contrast. This causes eye strain on extended reading.

**Use off-white on off-dark:** White text at 87–95% opacity on a very dark gray background (not black) reduces halation while maintaining sufficient contrast. Material Design's recommendation: #FAFAFA text on #121212 surface. macOS uses system-defined semantic text colors that are slightly off-white in dark mode.

### Status colors in dark mode

Status colors designed for white backgrounds (the conventional fully-saturated red #CC0000, green #00AA00) appear harsh on dark backgrounds and may fail contrast requirements. Dark mode requires desaturated, lightened status colors — the same hue family, but shifted toward higher lightness and lower saturation.

**Design requirement:** Dark mode is not a toggle instruction in the Design Spec. It is a complete second color specification. Every semantic color (foreground, background, brand/accent, status-error, status-warning, status-success, status-info, muted foreground, surface, elevated surface) must have both a light-mode and a dark-mode value. This is a design deliverable.

### Design tokens enable dark mode

A design token is a named design decision: `color.status.error = #D32F2F`. Tokens make dark mode structurally possible:

```
color.status.error.light = #D32F2F  (fully saturated, for white backgrounds)
color.status.error.dark = #EF9A9A   (desaturated/lightened, for dark surfaces)
```

Without token-level dark mode specification, developers must guess which colors to adjust and by how much. The token vocabulary is the interface between design reasoning and implementation. In the Visual Semantics section of a Design Spec, express visual decisions as token references, not as raw color values. The implementation resolves the tokens — the design specifies the intent.

---

## Surface-specific visual constraints

### TUI: character grid forces visual discipline

The terminal character grid imposes constraints that web and desktop interfaces do not have:

**Grid alignment is absolute:** Every visual element is one or more character cells wide and tall. There is no sub-pixel positioning, no fractional units, no pixel-precise layout. Visual alignment must be designed in character columns and rows.

**Box-drawing characters for structure:** Borders, panels, and containment are expressed using Unicode box-drawing characters (─ │ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼). These are visual structure without color — they work in 1-color terminals and degrade gracefully when box-drawing Unicode is unavailable (falls back to ASCII `+-|`).

**Focus through cursor and highlight:** TUI focus is expressed through cursor position (visible blinking cursor) and cell highlighting (inverted colors or bold weight on the focused row or cell). There is no `:focus` ring equivalent — the entire focused element or row changes visual treatment. Design focus states as complete cell-level inversions, not subtle border additions.

**Color depth must be treated as a design constraint, not assumed:** Design the primary visual hierarchy in the 16-color (ANSI basic) model. Test the design at that constraint before assuming xterm-256color or truecolor is available. A TUI that requires 256 colors to be readable excludes users on older terminals, remote SSH connections, and some CI environments.

**No sub-pixel rendering, no antialiasing:** Text in terminals renders at the character level — each character occupies exactly its cell. Fine-line icons from icon fonts do not render reliably in terminals; Unicode block characters (█ ▌ ▎ ▏) and Braille patterns are the TUI designer's alternative for non-character graphical elements.

### Desktop: platform design language is the foundation

Desktop applications exist within a platform design language that users have internalized. Visual design that fights the platform creates cognitive friction and accessibility failures (platform accessibility APIs expect platform controls).

**Platform typography defaults:**
- macOS: SF Pro (text), SF Mono (monospace). System fonts provide automatic dark mode adaptation, optical size variants, and Dynamic Type support.
- Windows: Segoe UI Variable (text), Cascadia Code (monospace). WinUI controls use these automatically.
- GNOME Linux: Cantarell (text), Monospace (monospace).

**When to use system fonts vs custom fonts:** System fonts signal "this is a native application." Custom fonts signal "this has its own visual identity." For utilities, tools, and developer-facing applications, system fonts are almost always preferable — they integrate with platform accessibility, scale with system font size preferences, and require no font loading. For branded consumer applications on hybrid frameworks (Electron, Tauri), custom fonts may be appropriate but must be carefully tested for legibility at system font size settings.

**Semantic color from the platform:** macOS defines system colors with light/dark mode equivalents (NSColor.label, NSColor.secondaryLabel, NSColor.systemRed, etc.). Windows Fluent Design defines system accent colors. Prefer platform semantic colors for text, backgrounds, and status indicators — they inherit dark mode automatically and match the OS's visual language.

### Web application: pixel-precise but context-variable

Web application interfaces are not the same design problem as web marketing pages. The constraints differ:

**Zoom changes proportions:** Browser zoom (Ctrl/Cmd +) scales all text and layout proportionally. A design that depends on exact pixel relationships will reflow when zoomed. Use relative units (rem, em, %) for sizing rather than fixed pixel values wherever the design must zoom gracefully.

**Font loading introduces rendering variance:** Web fonts load after initial render, causing FOUT (flash of unstyled text) or FOIT (flash of invisible text) without explicit management. This is not purely a CSS problem — it is a design decision: which fonts are critical enough to warrant blocking render, and which can fall back to system fonts during load?

**System dark mode requires explicit support:** Unlike desktop native applications where platform controls automatically adapt, web applications must explicitly implement dark mode via CSS `prefers-color-scheme` or equivalent. A web application with no dark mode implementation will have system UI (scrollbars, form controls on some browsers) in dark mode while the application itself remains light — visually incoherent.

**Data-dense web application design:** Monitoring dashboards, data tables, and analytics views often need compact spacing to preserve the global picture. Choose padding for the actual type, content, input targets, and scanning task. Do not copy generous marketing-page spacing into every row when it forces avoidable scrolling and hides relationships.

---

## Anti-patterns

These are predictable failures in application visual design. Each has a diagnostic question you can ask of any design.

**1. Color as the only differentiator between states**
Diagnostic: does the design remain understandable with all color removed?
Fix: pair color with shape, text, icon, or weight as a secondary signal.

**2. Visual hierarchy that mirrors code structure**
Diagnostic: does the layout organization map to developer-facing categories (modules, features, database tables) rather than user-facing tasks?
Fix: reorganize around what users are looking for, not how the system is built.

**3. Inconsistent spacing creating false groupings**
Diagnostic: can you identify which elements belong together by proximity alone, without reading the content?
Fix: restore intentional spacing relationships — elements in the same group use smaller gaps than gaps between groups. Preserve optical corrections that improve the rendered grouping.

**4. Decorative icons without labels in non-expert interfaces**
Diagnostic: would a first-time user recognize every icon without its label?
Fix: add text labels to navigation and command icons; rely on icon-only only for truly universal symbols after confirming users have learned the vocabulary.

**5. Motion that competes with the task**
Diagnostic: does movement distract from reading, block the next action, obscure state, or ignore motion preferences?
Fix: reduce or remove the competing effect, preserve meaningful feedback, and provide the applicable reduced-motion and pause/update controls. Judge timing through the actual interaction.

**6. Dense data applications using marketing-page spacing**
Diagnostic: does repeated padding hide the context needed for scanning or comparison merely because "it looks clean"?
Fix: fit density to the task while preserving legibility and input targets; inspect realistic data instead of prescribing one padding value.

**7. Dark mode as color inversion**
Diagnostic: were the dark mode colors produced by inverting light mode values, or designed independently?
Fix: design a separate color specification for dark mode; elevation through lightness, not shadow; desaturated status colors.

**8. Chartjunk obscuring data**
Diagnostic: which effects obscure comparison, distort values, or compete with meaningful labels and data?
Fix: remove misleading perspective and distracting fills or grids while retaining useful context and coherent visual character.

**9. Typography decoration over legibility**
Diagnostic: has this font been tested at its actual rendered size on the target display at actual user distance?
Fix: test type at the precise pixel size it will render at, on a representative screen; choose legibility over brand expression.

**10. Type hierarchy that mirrors code hierarchy, not reading priority**
Diagnostic: does the most important information for the user's immediate task have the highest visual weight?
Fix: visual weight must match task-relevance, not system-organizational-level.

---

## AI-Agent Adaptation

Use the tools actually available. Screenshots, browser automation, terminal captures, and color sampling can support rendered checks when provided by the host. Expert critique of an observed composition is legitimate design evidence; it does not establish actual user preference, emotional response, task success, or complete accessibility conformance. Record the surface, state, size, and observation method. Without rendered access, keep visual judgments provisional. Do not assume access to target hardware or real-user observations.

**Analytical checks available without rendered access:**
- **Contrast ratio verification:** Given resolved foreground/background colors, calculate the ratio against the applicable threshold. Unknown layering, gradients, or theme values remain evidence gaps; a passing pair does not establish whole-interface conformance.
- **Grayscale test (analytical):** Given a described layout, reason about whether the hierarchy survives without color — if only color distinguishes elements, the hierarchy fails the test.
- **Spacing system audit:** Check whether recurring relationships use accepted tokens or justified exceptions. A non-multiple alone is not a defect; optical quality requires rendering.
- **Color role audit:** Check semantic distinctions and whether expressive uses fit the brief without competing with them. Do not require every color to encode information.
- **Type role analysis:** Check whether size, weight, family, and placement have coherent roles. Numeric sizes alone cannot prove perceptible hierarchy or legibility.
- **Iconography criteria check:** Verify that specified icons meet the when-to-use conditions.
- **Gestalt reasoning from layout descriptions:** If told "the form label is 32px below the input field," apply gestalt proximity: the label reads as belonging to the input *above* it, not the input it labels. Spatial relationships described in text are sufficient to apply proximity and common-region principles.
- **Risk identification from specification:** Icon-only navigation or automatic motion warrants checking recognition, control, and task fit. Do not infer a rendered defect solely from the name of a style or technique.

**Checks requiring rendered or interactive evidence:**
- Assessing whether a color palette "feels right" or has the intended emotional register
- Evaluating visual tension, figure/ground quality, or gestalt grouping in rendered output
- Evaluating hierarchy, type, optical alignment, density, and craft at the inspected viewport, zoom, content, and theme; do not generalize to untested target conditions
- Inspecting motion, interruption, repeated input, and reduced-motion behavior through actual interaction rather than a still image
- Sampling rendered colors when a capture/color tool is available; otherwise calculate from specified RGB/hex values and disclose that boundary.

Treat palette character and composition assessments as expert judgments against the accepted brief. Claims about what users prefer, feel, or notice in use need relevant user evidence; a designer's judgment or attractive render does not establish them.

**Design decision scope:** Record consequential visual choices and their rationale in the existing handoff, with named roles/tokens and precise values where implementation needs them. Preserve accepted character as well as semantic meaning. Distinguish inspected results, expert interpretation, assumptions, and unverified checks. Use `visual-art-direction` for developing the direction and `design-validation` for judging its real implementation; neither tool access nor visual polish expands product or implementation authority.

---

## Sources

- Nielsen Norman Group — 5 Principles of Visual Design in UX (Kelley Gordon, 2020) [nngroup.com/articles/principles-visual-design/]
- Nielsen Norman Group — 10 Usability Heuristics for User Interface Design (Nielsen, 1994; reviewed 2024) [nngroup.com/articles/ten-usability-heuristics/]
- Tufte, E.R. — *The Visual Display of Quantitative Information* (1983, 2nd ed. 2001) — data-ink ratio, chartjunk, small multiples, sparklines
- Material Design 3 [m3.material.io] — color roles, tonal palette system, surface elevation in dark mode
- Apple Human Interface Guidelines [developer.apple.com/design/human-interface-guidelines/] — SF Pro type system, semantic color system, dark mode surface layering
- GOV.UK Design System [design-system.service.gov.uk] — color-as-functional-signal only, baseline spacing system, line length guidance
- W3C [WCAG 2.2](https://www.w3.org/TR/WCAG22/) and its Understanding documents: [1.4.1 Use of Color, Level A](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html), [1.4.3 Contrast (Minimum), Level AA](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [1.4.11 Non-text Contrast, Level AA](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), [2.2.2 Pause, Stop, Hide, Level A](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html), and [2.3.3 Animation from Interactions, Level AAA](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html). Apply each criterion's scope and exceptions; these are not universal style rules.
- W3C [CSS Fonts Module Level 3, numerical formatting](https://www.w3.org/TR/css-fonts-3/#font-variant-numeric-prop) — supported tabular numerals can align digits without requiring a wholly monospaced family.
- Wathan, A. & Schoger, S. — *Refactoring UI* (2018) [refactoringui.com] — type scale systems, hierarchy without color, spacing as design tool [partially verified — established professional reference]
- no-color.org — NO_COLOR convention for CLI environments

---
