# Visual Report Contract

Last updated: 2026-09-25

Use this display template when [Presenter](../../../../protocols/presenter.md) renders a complex Human Review View. Domain records already supply findings, options, recommendations, evidence, and blockers; organize that content without inventing conclusions. Simple results use text. The release builder bundles this shared source and its references for standalone consumers.

## When to use tabbed layout

For complex multi-dimensional analysis with 3+ major architectural concerns, substantial revision history, nested options requiring sub-navigation, or before/after comparisons across multiple dimensions, use a tabbed layout instead of the flat card structure. See [tabbed-discovery-report.md](../../../authoring/references/tabbed-discovery-report.md) for the complete protocol.

Simple findings (1-5 cards, single dimension) remain card-based without tabs.

## Reading order

- Header: title, date, scope, source record IDs/revisions, review status, and a compact legend.
- Overview: status/count pills and the top recommendation or decision.
- Cards: one card per finding or capability.
- Evidence: source paths and detailed rationale inside `<details>` where possible.
- Footer: provenance, source artifact, and generation information.

Do not lead with an essay. The first viewport should tell the reader what matters and where to look next.

## Card contract

Each finding, candidate, capability, option, or module card contains:

1. short title and status badge;
2. involved files or records in monospace;
3. a dominant current/target (before/after) visual;
4. one-sentence problem;
5. one-sentence solution or observed behavior;
6. up to four short wins, each naming the concrete gain;
7. an adjacent one-sentence visual takeaway;
8. an optional decision, ADR, or uncertainty callout;
9. collapsed evidence with file/line or record anchors.

The visual carries the explanation. If the diagram needs a paragraph, redraw it. Keep diagrams roughly 320–360px tall and vary patterns: Mermaid flow/sequence graphs for relationships, hand-built boxes and arrows for seams, cross-sections for shallow layers, mass diagrams for interface versus implementation, and call-graph collapse for repeated delegation.

## Visual and runtime rules

- Use inline CSS and inline SVG as the portability baseline. Mermaid is optional progressive enhancement for graph-shaped diagrams when the generated report environment permits network access.
- Keep labels and basic structure in ordinary HTML so the report remains readable if a CDN or Mermaid render fails.
- Use one accent color, red only for leakage/problems, amber only for warnings, and dark emphasis for deep modules or recommendations.
- Put long evidence, open questions, and implementation detail behind native `<details>` elements.
- Every diagram has an adjacent one-sentence takeaway.
- Every report ends with one anchored top recommendation or next decision.
- Every structural card has a current/target comparison. If comparison is not meaningful, state why on the card.
- Keep roadmap and implementation sequencing artifacts distinct from finding reports; do not use a roadmap as an audit companion.

## Portability

Consumer `references/visual-report.md` aliases resolve to this single source in the repository. Packaging materializes the reference closure with working local links. Keep domain-specific content requirements in the consumer's report reference; display rules live here. No separately installed Presenter skill is required.

## Quality gates

- Every card has a before/after visual or an explicit reason why a comparison does not apply.
- Internal card and recommendation links resolve.
- Visible prose stays concise; detailed evidence remains reachable.
- Domain sources remain authoritative, including canonical product HTML and prototype artifacts. Deleting this derived report loses no unique fact or decision.
- Visible source revisions match the requested snapshot; refresh and feedback processing recheck the sources under Presenter.
- Persist review feedback in the canonical record, never browser localStorage; localStorage is only for display preferences.
- Inline SVG includes accessible `<title>` and `<desc>` elements; ordinary HTML labels preserve meaning if scripts or CDNs fail.
- Changed Markdown files carry a current `Last updated` line near the top.
