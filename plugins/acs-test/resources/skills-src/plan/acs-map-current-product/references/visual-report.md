# Visual Report Contract

Last updated: 2026-09-30

Use this display template when [Presenter](../../../../protocols/presenter.md) renders a complex Human Review View. Domain records already supply findings, options, recommendations, evidence, and blockers; organize that content without inventing conclusions. Simple results use text. The release builder bundles this shared source and its references for standalone consumers.

## When to use tabbed layout

For complex multi-dimensional analysis with 3+ major architectural concerns, substantial revision history, nested options requiring sub-navigation, or before/after comparisons across multiple dimensions, use a tabbed layout instead of the flat card structure. See [tabbed-discovery-report.md](../../../authoring/references/tabbed-discovery-report.md) for the complete protocol.

Simple findings (1-5 cards, single dimension) remain card-based without tabs.

## Reading order

- Header: a title that names the subject (not a sentence, at most 2rem), one meta line `YYYY-MM-DD · <revision> · <scope>`, review status, and a compact legend. No lede paragraph.
- Overview: status/count pills and the top recommendation or decision.
- Cards: one card per finding or capability.
- Evidence: source paths and detailed rationale inside `<details>` where possible.
- Footer: provenance, source artifact, and generation information.

Do not lead with an essay. The first viewport should tell the reader what matters and where to look next.

## Card contract

Each finding, candidate, capability, option, or module is one `<article class="card">` in this order, every time:

1. short title and status badge;
2. involved files or records in monospace;
3. a dominant current/target (before/after) visual;
4. one-sentence problem;
5. one-sentence solution or observed behavior;
6. up to four short wins, each naming the concrete gain;
7. an adjacent one-sentence visual takeaway;
8. an optional decision, ADR, or uncertainty callout;
9. collapsed evidence with file/line or record anchors.

```html
<article class="card" id="FND-CON-3" data-visual="compare">
  <h3>Short title naming the change</h3>
  <div class="badges"><span class="badge">P1</span><span class="tag">in-process</span></div>
  <pre class="files">src/a.ts:26  ← what this line is
src/b.ts:129 ← what this line is</pre>
  <div class="grid">
    <div class="pane"><h4>Before</h4><svg role="img" viewBox="0 0 400 300"><title>…</title>…</svg></div>
    <div class="pane"><h4>After</h4><svg role="img" viewBox="0 0 400 300"><title>…</title>…</svg></div>
  </div>
  <p class="takeaway">One sentence: what the picture shows.</p>
  <div class="two">
    <div><p><strong>Problem.</strong> …</p><p><strong>Solution.</strong> …</p></div>
    <ul class="wins"><li>…</li></ul>
  </div>
  <div class="callout">Optional decision or ADR line.</div>
  <details><summary>Evidence</summary>…</details>
</article>
```

The card body is never collapsed: only evidence goes inside `<details>`, never the title or the visual.

**Every card has a visual.** `data-visual` states which kind:

| Value | Use for | Requires |
| --- | --- | --- |
| `compare` (default) | Structural change: modules, seams, ownership, options, refactors | two `.pane` elements, Before and After |
| `single` | Table-shaped content: contracts, gates, test layers, traceability | one schematic beside the table, e.g. the path with the enforcement point marked, a failure path, a layer grid |
| `none` | A pure ledger row that only links to a card elsewhere | nothing |

A table never replaces the visual; it sits beside it.

**Diagrams are schematics, not prose.** Labels are names and short phrases: at most 14 words per `<text>` and 90 words per SVG. A sentence belongs in the takeaway or the problem/solution line. If the diagram needs a paragraph, redraw it. Keep diagrams roughly 320–360px tall and vary patterns: Mermaid flow/sequence graphs for relationships, hand-built boxes and arrows for seams, cross-sections for shallow layers, mass diagrams for interface versus implementation, and call-graph collapse for repeated delegation.

## Visual and runtime rules

- Use inline CSS and inline SVG as the portability baseline. Mermaid is optional progressive enhancement for graph-shaped diagrams when the generated report environment permits network access.
- Keep labels and basic structure in ordinary HTML so the report remains readable if a CDN or Mermaid render fails.
- Use one accent color, red only for leakage/problems, amber only for warnings, and dark emphasis for deep modules or recommendations.
- Editorial, not dashboard: shadows at most `0 1px 2px`, radius at most 12px, serif headings allowed, no hero-sized headline.
- Define colors once as CSS custom properties, with a `prefers-color-scheme: dark` override. SVG `fill`, `stroke`, and `stop-color` use `var(--token)`, `none`, `currentColor`, or `url(#id)`, never raw hex, so diagrams follow the theme.
- Put long evidence, open questions, and implementation detail behind native `<details>` elements.
- Every diagram has an adjacent one-sentence takeaway.
- Every report ends with one anchored top recommendation or next decision.
- Keep roadmap and implementation sequencing artifacts distinct from finding reports; do not use a roadmap as an audit companion.

## Date and version

Agents and readers must be able to tell which snapshot a view shows without opening its sources. Every view carries, in `<head>`:

```html
<meta name="generated" content="YYYY-MM-DD">
<meta name="source-revision" content="<commit sha or record revision>">
```

and shows the same date and revision on the header meta line.

- **One-off report** (review, audit, refactor report, discovery pass): the filename is `<slug>-YYYY-MM-DD.html`. A later run writes a new file; the older one stays as dated evidence.
- **Living view** rebuilt at a fixed path that other records link to (for example `technical-design.html`): keep the path and add `<meta name="view-kind" content="living">`. The date and revision tags are still required.

The same date and version rule covers every other human-readable HTML file (canonical records, roadmaps, delivery plans, prototypes); see [Presenter date and version](../../../../protocols/presenter.md#date-and-version). Those files validate with `--version-only`, because this contract's card rules apply only to finding reports.

## Validate before handover

Run [the report validator](../../../authoring/scripts/validate-report-html.py) on every generated view and fix each error before handing it over:

```bash
python3 <path of the validator link above> path/to/view.html
```

It checks each card's `data-visual` against its panes and SVGs, SVG label density, raw hex colors, accessible titles, collapsed cards, internal links, the top recommendation, the `generated` and `source-revision` tags, and the dated filename for one-off reports. A view that fails is not finished.

## Portability

Consumer `references/visual-report.md` aliases resolve to this single source in the repository. Packaging materializes the reference closure with working local links. Keep domain-specific content requirements in the consumer's report reference; display rules live here. No separately installed Presenter skill is required.

## Quality gates

- The report validator passes with no errors.
- Internal card and recommendation links resolve.
- Visible prose stays concise; detailed evidence remains reachable.
- Domain sources remain authoritative, including canonical product HTML and prototype artifacts. Deleting this derived report loses no unique fact or decision.
- Visible source revisions match the requested snapshot; refresh and feedback processing recheck the sources under Presenter.
- Persist review feedback in the canonical record, never browser localStorage; localStorage is only for display preferences.
- Inline SVG includes accessible `<title>` and `<desc>` elements; ordinary HTML labels preserve meaning if scripts or CDNs fail.
- Changed Markdown files carry a current `Last updated` line near the top.
