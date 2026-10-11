# Baseline HTML Presentation

Last updated: 2026-10-11

Also read [the local visual report contract](visual-report.md). It gives the compact card grammar, the standalone packaging rule, the before/after visual budget and the Writing rules. This document adds only the product-memory presentation guidance.

Read [the product memory contract](../../../resources/protocols/product-memory.md) first. The baseline enriches `discovery.html`. It does not own the document and does not produce a separate `current-product.html`. These patterns present current behavior inside shared concepts. Keep the records, IDs and styling that already exist.

Use the contract's semantic scaffold and shared navigation. Map the baseline to sections as follows:

| Baseline content | Section |
| --- | --- |
| Snapshot, candidate visions, coverage pills | `overview` |
| Roles | `users-problems` |
| Stories and flows | `capabilities-journeys` |
| Findings | `gaps-opportunities` |
| Unknowns | `questions-assumptions` |
| NFR observations | `risks-measures` |
| Aggregated `research-coverage` record with the roadmap-readiness statement | `research` |

Evidence lives in linked records or native details. A module map explains the relevant capability records; it is not a competing inventory.

## Progressive disclosure: three reading levels

The reader gets value when they stop at any level. Build every section on these levels:

1. **Overview (always visible):** header pills, snapshot, vision panel, system module map, journey chains, gap badges.
2. **Per-area detail (collapsed):** one `<details>` per functional area, with stories, boundary verdicts and the interaction diagram.
3. **Evidence (deepest):** file paths and per-story evidence, in nested `<details>` or trailing table columns.

Rules:

- `<summary>` text is informative: area name, story count and gap count. Never "click to expand".
- Every diagram gets an adjacent one-sentence takeaway ("what this shows").
- Gaps and open questions show at level 1 as badges. Their evidence lives at level 3.
- The overview and journeys link to the relevant capability records without duplicating their text.

## Baseline summary

In the shared overview, add the baseline coverage, the observation date and one row of status pills: implemented (emerald), in-progress (amber), planned (slate), gaps (red). Each pill shows its count and links to its section. Diagram labels name observable capabilities and user-flow steps. Do not write an introduction paragraph; start with the snapshot.

## Section patterns

**Snapshot.** Three labeled lines: purpose, personas, surfaces. Each is one source-backed sentence, with its evidence path in small, muted monospace text.

**Vision panel.** One bordered block per candidate vision in the overview. It holds the vision statement, an `inferred` (slate) or `confirmed` (emerald) chip, and anchor links to the story clusters that imply it. If the vision stayed inferred because confirmation was skipped, the panel links the open question.

**Product surface map.** A diagram of actors, observable capabilities and user-flow relationships, with an adjacent takeaway and source evidence.

**User journeys.** One horizontal step chain per flow: actor chip → entry point → steps → outcome. Each step links to its canonical capability or journey record. Build it as a flex row of boxes with SVG arrows. Use a journey chart only when satisfaction or effort per step matters.

**Functional areas.** Linked capability records grouped by area, with evidence in `<details>`:

- **Stories table.** Columns: story, surface need, deep need, modules (anchor-linked), evidence. Rows summarize the canonical records and link to them; layer entries live on those records.
  - A surface need carries an `evidenced` chip when code backs it.
  - A deep-need cell carries a slate `inferred` chip until someone confirms it.
  - Fundamental needs live in the per-area `<details>`, not in the table.
  - An inferred persona carries a slate `inferred` chip that names the source.
- **Constraint row.** Observed permissions, recovery, accessibility or latency, with environment, revision and evidence. Unknown expectations stay questions.
- **Interaction diagram.** A graph of this area's user-flow steps and observable outcomes. Use the offline diagram pattern below.

**In-progress and planned.** Two separate tables; never merge them with implemented. In-progress rows name the missing link ("UI without backend"). Planned rows carry a confidence chip.

**Observable constraints.** Show measured or promised user-facing behavior, with evidence and assessed coverage. Do not rate the internal architecture.

**Gaps and opportunities.** Enrich the existing shared gap and opportunity records: finding, expected versus observed behavior, evidence, affected capabilities and linked questions. Questions live in shared question records. Use badges for navigation, not duplicate cards that keep their own findings.

## Diagram patterns

Pick the pattern for the content, and vary it. Sameness reads as filler.

### Graph diagrams

For user flows and capability relationships, use a small inline SVG or a readable Mermaid source block with an adjacent explanation. If a renderer is already available, embed its SVG result. Do not add a remote runtime dependency. Link the diagram to the capabilities and evidence it explains. Diagram labels summarize records; they do not own product state.

### Nested boxes (module hierarchy)

Build modules as bordered `<div>`s, with submodules nested inside; depth equals nesting. Use this when the point is containment, which Mermaid draws poorly. Grey out internals, and give hub modules a thicker border.

### Step chain (user journeys)

A flex row of rounded boxes joined by SVG arrows, with the actor chip on the left and the outcome box highlighted. Each box links to its module section. Keep one journey per row, and allow horizontal overflow inside the chain.

## Style guidance

- Editorial, not corporate dashboard: generous whitespace, a readable maximum width, a stone or slate palette, and one accent (indigo works) for navigation and links.
- Status colors mean status only: emerald implemented, amber in-progress or opportunity, slate planned or question, red gap.
- Module labels inside diagrams: small uppercase monospace text with modest letter spacing. Schematic, not UI.
- Keep diagrams under about 360px tall. A wide diagram scrolls in its own overflow container, never the page.
- Inline the shared CSS once. Native `<details>`, anchors and tables work without JavaScript.
- Prefer Tailwind or Mermaid CDN dependencies for newly generated review-style visuals when the report environment permits. Keep ordinary HTML labels and inline visuals as the fallback. Do not change an existing product-memory document only to change its styling.

## Writing

Follow the [Writing rules](visual-report.md#writing). Keep facts and inferences visually distinct with `inferred` chips. Let diagrams and tables carry the weight. If a diagram needs a paragraph to be understood, redraw the diagram.
