---
name: design-implementation
description: Implement accessible, state-complete UI from a design specification. Use when building or modifying components or pages from agreed interaction, responsive, visual, and content requirements.
license: MIT
metadata:
  author: Bateau
  version: "2.0.0"
---

# Design Implementation

Translate the agreed design into working UI using the project's components, tokens, and framework conventions. No external design cookbook or theme plugin is required.

## Establish the contract

Read the relevant design and existing implementation patterns. Identify user goals, interactions, states, responsive behavior, accessibility, copy, and capability dependencies. Resolve material ambiguity before inventing user-visible behavior. Use `design-specification` for an incomplete handoff and `accessibility` for implementation mechanics.

## State completeness

Consider each reachable state; implement the ones meaningful to the component rather than forcing every element into a fixed quota:

| State | Treatment |
| --- | --- |
| Default | Clear purpose, label, and affordance |
| Hover | Additional feedback only where hover is available |
| Focus | Visible keyboard focus and sensible focus order |
| Active | Truthful pressed/selected feedback |
| Disabled | Explain unavailability when needed; native semantics or correctly enforced ARIA behavior |
| Loading | Prevent accidental duplicates, expose progress, and retain a readable label |
| Error | Identify the problem and recovery action; associate field errors with their inputs |
| Success | Confirm hidden effects where needed; avoid redundant or prematurely dismissed feedback |
| Empty/interrupted/stale | Explain what happened, what remains, and how to continue |

Do not rely on color alone. Use native controls where possible. Preserve user input and focus appropriately through async transitions.

## Responsive behavior

- Test at narrow widths, zoom, long content, and alternate input modes.
- Use content-driven breakpoints and flexible sizing rather than fixed device assumptions.
- Avoid accidental horizontal overflow; fix its cause instead of globally clipping meaningful content or focus indicators.
- Allow labels and controls to wrap when needed for localization or zoom.
- Use dynamic/small viewport units and safe-area insets when the surface requires them.
- Verify layout changes preserve task completion and reading/focus order.

Use `web-ui-design` or the relevant surface skill for deeper guidance.

## Motion and asynchronous feedback

Motion should clarify, guide, or confirm, and respect reduced-motion preferences. Every hover affordance needs a keyboard equivalent. Use optimistic updates only when failure can be detected and state truthfully restored; define pending, rollback, retry, and cancellation behavior. Destructive or irreversible actions may need confirmed completion rather than optimism.

## Components, tokens, and copy

Reuse existing components and documented design tokens. If a component catalog is present, load only relevant examples. Add or adjust tokens through project conventions; do not assume append-only themes or mandatory source-file stamps.

Use specific action labels and self-contained link text. Errors should state what happened and what the user can do without blaming them. Never fabricate product capabilities or metrics; use agreed content or explicit placeholders.

## Verify the implemented experience

Exercise the real interaction path, keyboard navigation, focus transitions, error/recovery states, and relevant responsive conditions. Use available browser, terminal, or desktop tools; record actual observations and unverified limits. Compare the result with the design, not just a screenshot. Use `design-validation` for a fuller experience check.
