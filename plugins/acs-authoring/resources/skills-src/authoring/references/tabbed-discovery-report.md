# Tabbed Discovery Report Protocol

Last updated: 2026-10-11

Use this protocol for complex analysis with real interactive tabs that hide inactive content. **Copy the markup, CSS and script from [the template](tabbed-discovery-template.html)**; this file states the requirements the template meets. The [visual report contract](visual-report.md) still applies: card skeleton, `data-visual`, diagram budgets, colors, date and version, and the Writing rules.

## When to use

| Use tabs for | Stay with cards for |
| --- | --- |
| Architecture discovery with 4 or more structural issues | Simple findings (1–5 cards, one dimension) |
| Design documents that compare 3 or more materially different options | Linear progressions without nested structure |
| Analysis with a long revision history that the reader needs | Reports that fit in 2–3 viewport heights |
| Multi-phase migrations with interdependent steps | |
| Before/after transformations across several layers | |

## Three-tab baseline

Default structure: Problems → Design → Migration.

```
┌──────────────────────────────────────┐
│ Metrics Card (header)                │
├──────────────────────────────────────┤
│ [Problems] [Design] [Migration]      │  ← Tab buttons
├──────────────────────────────────────┤
│                                      │
│  Active tab content                  │
│  (other tabs hidden)                 │
│                                      │
└──────────────────────────────────────┘
```

Name the tabs for the domain:

- Technical refactoring: Current → Target → Path
- Product analysis: Gaps → Opportunities → Roadmap
- Architecture audit: Findings → Options → Decision

## Tab interface

Structure, as in the template:

```html
<div class="tabs" role="tablist">
  <nav class="tab-nav">
    <button class="tab-btn active" role="tab" aria-selected="true"
            aria-controls="problems-panel" data-tab="problems">Problems</button>
    <!-- one button per tab -->
  </nav>
  <div class="tab-panel active" id="problems-panel" role="tabpanel" aria-labelledby="tab-problems">…</div>
  <div class="tab-panel" id="design-panel" role="tabpanel" aria-labelledby="tab-design" hidden>…</div>
</div>
```

Behavior. The template's inline vanilla script at the end of the document does all of this, with no dependencies:

- A click on a tab button activates its panel. It sets `active` and `aria-selected` on the button, and `active` and `hidden` on the panels.
- ArrowRight and ArrowLeft move to the next or previous tab and wrap around. Home and End jump to the first and last tab.
- On load, the first tab is active. Optionally, a URL hash that names a panel (`#design`) activates that tab.

## Components

All components are in the template. Copy them; do not redesign them.

- **Metrics card.** Place it before the tabs. It shows key numbers (`193 → 60` SKILL.md lines), status badges (`4 problems`, `3 decided`, `2 undecided`) and the top decision.
- **Comparison card.** Use one card per problem or refactoring delta. It is an `<article class="card comparison-card" data-visual="compare">`, with a `Current ❌` pane and a `Target ✅` pane. Each pane has an inline SVG diagram, an optional snippet, and a `Cost:` or `Gain:` line. Give each card a takeaway and an evidence `<details>` whose summary gives the count (`Evidence (3 files affected)`). Snippets have at most 5 lines. Full schemas go in `<details>`.
- **Decision history callout.** Use it for revisions: date, decision, context, rationale in `<details>`, and timing. Put it in the tab it affects. If a decision spans several concerns, duplicate the callout or use cross-tab anchor links.
- **Nested sub-tabs.** Use them when one main tab has 4 or more distinct options or layers. Sub-tabs need their own script initialization: the same pattern as main tabs, scoped to `.sub-tab-btn` and `.sub-tab-panel`.
- **Migration timeline.** Give each step a number, a title, one sentence on what it unlocks, and a readiness badge (`Ready`, `Needs API`). A horizontal flow diagram with SVG arrows is also acceptable.

### Diagram patterns

Mix diagram types. Pick the pattern that fits the content, so the cards do not all look the same:

1. **Mermaid graph** for dependencies and call flow ("X calls Y calls Z"). Use `flowchart` or `graph`. Style leakage edges red and deep modules dark with `classDef`. Sequence diagrams show "before: 6 round-trips; after: 1".
2. **Hand-built boxes and arrows** when the Mermaid layout fights you. Draw modules as bordered `<div>`s and arrows as inline SVG `<line>` or `<path>`. Use it to show one thick-bordered deep module with greyed-out internals.
3. **Cross-section** for layered shallowness. Stack horizontal bands. Before: 6 thin layers. After: 1 thick band.
4. **Mass diagram** for interface versus implementation. Draw two rectangles per module. Before: the interface is nearly as tall as the implementation (shallow). After: a short interface and a tall implementation (deep).
5. **Call-graph collapse.** Before: a tree of function calls as nested boxes. After: one box with faded internals.

Keep diagrams about 320px tall, so before and after sit side by side without scrolling. Diagram labels use `text-xs uppercase tracking-wider`: schematic, not UI.

## Progressive disclosure

1. **Tab level:** major concerns, one per tab.
2. **Card level:** one card per problem, option or finding.
3. **Evidence level:** file paths and detailed rationale in `<details>`.

Never duplicate content across levels. Evidence lives only at level 3.

## Design tokens

Use the same tokens as [visual-report.md](visual-report.md):

- **Colors:** base `--bg`, `--fg`, `--mut` (muted text), `--line` (borders); status `--problem` (red), `--warn` (amber), `--ok` (emerald), `--neutral` (slate); one accent `--acc` (indigo or orange); `--code` (slightly darker or lighter than the base). Use color sparingly: one accent, red for leakage and problems, amber for warnings.
- **Typography:** body `ui-sans-serif, -apple-system, system-ui, sans-serif`; code `ui-monospace, SFMono-Regular, Menlo, monospace`; headings in the same family at a heavier weight (serif is optional for an editorial tone); diagram module labels `text-xs uppercase tracking-wider`.
- **Spacing:** 1.5–2rem between cards; 0.5–0.75rem between elements inside a card; at most 920px wide for prose, wider for diagrams; diagrams about 320px tall.
- **Light and dark mode:** CSS custom properties with a `@media (prefers-color-scheme: dark)` override. Never put fixed colors in declarations.
- **Tone:** editorial, not corporate dashboard. Generous whitespace. A stone or slate palette works well with serif headings.

## Accessibility

- **ARIA:** tab buttons have `role="tab"`, `aria-selected` and `aria-controls`. Tab panels have `role="tabpanel"`, `aria-labelledby` and `hidden`. The container has `role="tablist"`.
- **Keyboard:** Tab focuses the tab buttons. The arrow keys switch tabs. Home and End jump to the first and last tab. Enter and Space activate a tab (implicit with `<button>`).
- **Screen reader:** focus announces "X of Y tabs", the tab name and its selected state. Content in inactive tabs is truly hidden, not only `display:none`.

## Fallback behavior

When JavaScript is disabled or fails:

- All tab panels stay visible in document order.
- Tab buttons become section headers, or stay clickable with no effect.
- The base HTML is readable; the script only adds interaction.

Implement this with a `<noscript>` style override, or with an initial state where all panels are visible.

## Portability

- Reference this file as `references/tabbed-discovery-report.md` (relative).
- Never require suite-level paths (`/authoring/...`), another skill or an external service.
- Use inline CSS and vanilla JS only. CDN dependencies (Mermaid, Tailwind) are optional and must degrade gracefully.

A packaged skill must include this reference and every template it needs.

## Writing

Follow the [Writing rules](visual-report.md#writing). Two additions apply to tabbed reports:

- **Wins:** name the concrete gain in at most 6 words: "Tests hit one interface", "Schema leak eliminated", "Batch edits now expressible", "Delete 4 shallow wrappers". Never write a vague win such as <s>"easier to maintain"</s> or <s>"cleaner code"</s>.
- **Cost and gain lines:** state the concrete impact. "Cost: Goes stale after migration, no type safety." "Gain: Single source of truth, always current."

## Quality gates

- Every tab has at least one card or other meaningful content.
- Before/after comparisons show actual diagrams, not placeholder text.
- Evidence is reachable and collapsed by default.
- Diagram labels are legible without magnification.
- Code snippets are syntax-highlighted (`<code class="language-*">` with Prism or highlight.js) or plain monospace.
- Internal links resolve, including anchors and tab switches.
- The page works on mobile: tabs stack or scroll horizontally, and content reflows.

## Related contracts

- [visual-report.md](visual-report.md): card-based reports, inline SVG patterns and the Writing rules. Use it when all findings fit in one scrollable page.
- [html-report.md](../../plan/acs-map-current-product/references/html-report.md): progressive disclosure for product mapping.
