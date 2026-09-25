# Baseline HTML Presentation

Last updated: 2026-09-17

For the compact card grammar, standalone packaging rule, and before/after visual budget, also read [the local visual report contract](../../../../../skills/acs-refactor-code/references/visual-report.md). This document remains the product-memory-specific presentation guidance; the local contract supplies the portable visual rules.

Read [the product memory contract](../../../../protocols/product-memory.md) first. The baseline enriches `discovery.html`; it does not own the document or produce a separate `current-product.html`. These patterns guide presentation of current behavior inside shared concepts. Preserve records, IDs, and styling already present.

Use the contract's semantic scaffold and shared navigation. Map the snapshot and candidate visions to `overview`, roles to `users-problems`, stories and flows to `capabilities-journeys`, findings to `gaps-opportunities`, unknowns to `questions-assumptions`, and NFR observations to `risks-measures`. The baseline summary's coverage pills stay in the overview; the aggregated `research-coverage` record with the roadmap-readiness statement lives in the `research` section. Evidence lives in linked records or native details. A module map is explanatory material attached to relevant capability records, not a competing inventory.

## Progressive disclosure — three reading levels

The reader gets value stopping at any level. Structure every section around this:

1. **Overview (always visible):** header pills, snapshot, vision panel, system module map, journey chains, gap badges.
2. **Per-area detail (collapsed):** one `<details>` per functional area — stories, boundary verdicts, interaction diagram.
3. **Evidence (deepest):** file paths and per-story evidence in nested `<details>` or trailing table columns.

Rules:

- `<summary>` text is informative — area name + story count + gap count — never "click to expand".
- Every diagram gets an adjacent one-sentence takeaway ("what this shows").
- Gaps and unanswered questions surface at level 1 as badges; the evidence for them lives at level 3.
- Relevant capability records are reachable from the overview and journeys without duplicating their text.

## Baseline summary

Within the shared overview, add baseline coverage, observation date, and one row of status pills — implemented (emerald), in-progress (amber), planned (slate), gaps (red) — each with its count, anchor-linked to its section. Diagram labels identify observable capabilities and user-flow steps. No introduction paragraph — straight into the snapshot.

## Section patterns

**Snapshot** — three labeled lines (purpose, personas, surfaces), each one source-backed sentence with its evidence path in small, muted monospace text.

**Vision panel** — one bordered block per candidate vision in the overview: the vision statement, an `inferred` (slate) or `confirmed` (emerald) chip, and anchor links to the implying story clusters. When skipped confirmation left it inferred, the panel links the open question.

**Product surface map** — a diagram of actors, observable capabilities, and user-flow relationships, with an adjacent takeaway and source evidence.

**User journeys** — one horizontal step chain per flow: actor chip → entry point → steps → outcome. Each step links to its canonical capability or journey record. Hand-built flex row of boxes with SVG arrows; a journey chart only when satisfaction/effort per step genuinely matters.

**Functional areas** — linked capability records grouped by area, with evidence in `<details>`:

- **Stories table** — story, surface need, deep need, modules (anchor-linked), evidence. Rows summarize and anchor-link the canonical records; layer entries live on those records. Surface needs carry an `evidenced` chip when code-backed; deep-need cells carry a slate `inferred` chip until confirmed; fundamental needs live in the per-area `<details>`, not the table. Inferred personas marked with a slate `inferred` chip naming the source.
- **Constraint row** — observed permissions, recovery, accessibility, or latency, with environment/revision and evidence; unknown expectations stay questions.
- **Interaction diagram** — graph of this area's user-flow steps and observable outcomes, using the offline diagram pattern below.

**In-progress / planned** — two separate tables. In-progress rows name the missing link ("UI without backend"); planned rows carry a confidence chip. Never merged with implemented.

**Observable constraints** — show measured or promised user-facing behavior with evidence and assessed coverage; do not rate internal architecture.

**Gaps and opportunities** — enrich existing shared gap/opportunity records: finding, expected versus observed behavior, evidence, affected capabilities, and linked questions. Questions live in shared question records. Use badges for navigation, not duplicate cards with independently maintained findings.

## Diagram patterns

Pick per content; vary them — sameness reads as filler.

### Graph diagrams

For user flows and capability relationships, use a small inline SVG or a readable Mermaid source block with an adjacent explanation. If a renderer is already available, embed its SVG result; do not add a remote runtime dependency. Link the diagram to the capabilities and evidence it explains. Diagram labels summarize records; they do not own product state.

### Nested boxes (module hierarchy)

Hand-built: modules as bordered `<div>`s, submodules nested inside, depth = nesting. Use when the point is containment, which Mermaid draws poorly. Grey out internals; give hub modules a thicker border.

### Step chain (user journeys)

Flex row: rounded boxes joined by SVG arrows, actor chip on the left, outcome box highlighted. Each box anchor-links to its module section. Keep one journey per row; allow horizontal overflow within the chain.

## Style guidance

- Editorial, not corporate-dashboard: generous whitespace, a readable maximum width, stone/slate palette, one accent (indigo works) for navigation and links.
- Status colors mean status only: emerald implemented, amber in-progress/opportunity, slate planned/question, red gap.
- Module labels inside diagrams: small uppercase monospace text with modest letter spacing — schematic, not UI.
- Keep diagrams under ~360px tall; wide ones scroll in their own overflow container, never the page.
- Inline shared CSS once. Native `<details>`, anchors, and tables work without JavaScript. Prefer Tailwind/Mermaid CDN dependencies for newly generated review-style visuals when the report environment permits. Preserve ordinary HTML labels and inline visuals as the fallback, and do not retrofit existing product-memory documents solely to change their styling.

## Tone

Plain, concise, evidence-first. Facts and inferences stay visually distinct (inferred chips). No hedging, no "it's worth noting". If a sentence could be a bullet, make it a bullet. Prose stays sparse — the diagrams and tables carry the weight; if a diagram needs a paragraph to be understood, redraw the diagram.
