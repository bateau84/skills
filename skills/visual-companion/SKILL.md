---
name: visual-companion
description: Browser-based visual brainstorming companion for showing mockups, diagrams, and interactive A/B/C choices during conversation. Use when a question would be clearer shown than described — UI mockups, wireframes, architecture diagrams, side-by-side comparisons, flowcharts.
---

# Visual Companion

Browser-based visual brainstorming companion for showing mockups, diagrams, and interactive options during conversation.

## When to Use

Decide per-question, not per-session. The test: **would the user understand this better by seeing it than reading it?**

**Use the browser** when the content IS visual:

- UI mockups, wireframes, layouts, component designs
- Architecture diagrams, data flow, relationship maps
- Side-by-side visual comparisons
- Design polish — look and feel, spacing, visual hierarchy
- State machines, flowcharts, entity relationships

**Use the terminal** when the content is text:

- Requirements and scope questions
- Conceptual A/B/C choices described in words
- Tradeoff lists, pros/cons tables
- Technical decisions — API design, data modeling
- Clarifying questions

A question _about_ a UI topic is not automatically visual. "What kind of wizard do you want?" → terminal. "Which of these wizard layouts feels right?" → browser.

## Offering the Companion

Do NOT offer it upfront. Wait until a question would genuinely be clearer shown than told. The first time that happens, offer it as its own message:

> "This next part might be easier if I show you — I can put together mockups, diagrams, and comparisons in a browser tab as we go. Want me to?"

This offer MUST be its own message — no other content. Wait for the user's response. If they decline, continue text-only.

## Starting a Session

```bash
SCRIPTS="$HOME/.config/opencode/skills/visual-companion/scripts"
$SCRIPTS/start-server.sh --project-dir /path/to/project --open
```

Returns JSON with `screen_dir`, `state_dir`, and `url`. Save all three.
Share the full URL (includes session key) with the user as a fallback.

## The Loop

1. **Check server is alive** — verify `$STATE_DIR/server-info` exists and `$STATE_DIR/server-stopped` does not. If stopped, restart with same `--project-dir` (reuses port, browser tab auto-reconnects).

2. **Write HTML** to a new file in `screen_dir`:
   - Use semantic filenames: `layout.html`, `architecture.html`, `comparison.html`
   - Never reuse filenames — each screen gets a fresh file
   - Use your file-creation tool — never cat/heredoc
   - Server automatically serves the newest file

3. **Tell user what to expect and end your turn:**
   - Remind them of the URL
   - Brief text summary of what's on screen
   - Ask them to respond: "Take a look and let me know what you think."

4. **On your next turn:**
   - Read `$STATE_DIR/events` if it exists — JSON lines of user clicks
   - Merge with their terminal text for the full picture
   - Terminal message is primary; events provide structured interaction data

5. **Iterate or advance** — if feedback changes current screen, write a new version (e.g., `layout-v2.html`). Only move on when current step is validated.

6. **Unload when returning to text** — when the next point doesn't need the browser, push a waiting screen:
   ```html
   <!-- filename: waiting.html -->
   <div
     style="display:flex;align-items:center;justify-content:center;min-height:60vh"
   >
     <p class="subtitle">Continuing in terminal...</p>
   </div>
   ```

## Writing Content Fragments

Write just the content — no `<html>`, no CSS, no `<script>`. The server wraps it in the frame template automatically.

```html
<h2>Which layout works better?</h2>
<p class="subtitle">Consider readability and visual hierarchy</p>

<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Single Column</h3>
      <p>Clean, focused reading experience</p>
    </div>
  </div>
  <div class="option" data-choice="b" onclick="toggleSelect(this)">
    <div class="letter">B</div>
    <div class="content">
      <h3>Two Column</h3>
      <p>Sidebar navigation with main content</p>
    </div>
  </div>
</div>
```

## CSS Classes Available

### Options (A/B/C choices)

```html
<div class="options">
  <div class="option" data-choice="a" onclick="toggleSelect(this)">
    <div class="letter">A</div>
    <div class="content">
      <h3>Title</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

Multi-select: Add `data-multiselect` to the container.

### Cards (visual designs)

```html
<div class="cards">
  <div class="card" data-choice="design1" onclick="toggleSelect(this)">
    <div class="card-image"><!-- mockup --></div>
    <div class="card-body">
      <h3>Name</h3>
      <p>Description</p>
    </div>
  </div>
</div>
```

### Mockup container

```html
<div class="mockup">
  <div class="mockup-header">Preview: Dashboard</div>
  <div class="mockup-body"><!-- content --></div>
</div>
```

### Split view (side-by-side)

```html
<div class="split">
  <div class="mockup"><!-- left --></div>
  <div class="mockup"><!-- right --></div>
</div>
```

### Pros/Cons

```html
<div class="pros-cons">
  <div class="pros">
    <h4>Pros</h4>
    <ul>
      <li>Benefit</li>
    </ul>
  </div>
  <div class="cons">
    <h4>Cons</h4>
    <ul>
      <li>Drawback</li>
    </ul>
  </div>
</div>
```

### Mock elements (wireframe building blocks)

```html
<div class="mock-nav">Logo | Home | About | Contact</div>
<div style="display:flex;">
  <div class="mock-sidebar">Navigation</div>
  <div class="mock-content">Main content area</div>
</div>
<button class="mock-button">Action Button</button>
<input class="mock-input" placeholder="Input field" />
<div class="placeholder">Placeholder area</div>
```

## Browser Events Format

```jsonl
{"type":"click","choice":"a","text":"Option A - Simple Layout","timestamp":1706000101}
{"type":"click","choice":"b","text":"Option B - Hybrid","timestamp":1706000115}
```

Last `choice` event is typically the final selection. The click pattern reveals hesitation.
If `$STATE_DIR/events` doesn't exist, user didn't interact with the browser.

## Design Tips

- Scale fidelity to the question — wireframes for layout, polish for polish questions
- Explain the question on each page
- 2-4 options max per screen
- Use real content when it matters (Unsplash images for visual work)
- Keep mockups simple — layout and structure, not pixel-perfect

## Cleaning Up

```bash
$SCRIPTS/stop-server.sh $SESSION_DIR
```

Project-dir sessions persist in `.brainstorm/` for reference. `/tmp` sessions are deleted on stop.
