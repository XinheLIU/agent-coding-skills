# Visual Report Contract

Last updated: 2026-09-13

Use this contract for static HTML reports that explain findings, candidates, or capabilities. The report must work when its owning skill is installed alone; packaged skills carry a local copy of this reference and must only link to it relatively.

## Reading order

- Header: title, date, scope, and a compact legend.
- Overview: status/count pills and the top recommendation or decision.
- Cards: one card per finding or capability.
- Evidence: source paths and detailed rationale inside `<details>` where possible.
- Footer: provenance, source artifact, and generation information.

Do not lead with an essay. The first viewport should tell the reader what matters and where to look next.

## Card contract

Each candidate or capability card contains:

1. short title and status badge;
2. involved files or records in monospace;
3. a dominant before/after visual;
4. one-sentence problem;
5. one-sentence solution or observed behavior;
6. up to four short wins, each naming the concrete gain;
7. an optional decision, ADR, or uncertainty callout.

The visual carries the explanation. If the diagram needs a paragraph, redraw it. Keep diagrams roughly 320–360px tall and vary patterns: Mermaid flow/sequence graphs for relationships, hand-built boxes and arrows for seams, cross-sections for shallow layers, mass diagrams for interface versus implementation, and call-graph collapse for repeated delegation.

## Visual and runtime rules

- Use Tailwind CDN for layout and Mermaid CDN for graph-shaped diagrams when the generated report environment permits network access.
- Keep labels and basic structure in ordinary HTML so the report remains readable if a CDN or Mermaid render fails.
- Use one accent color, red only for leakage/problems, amber only for warnings, and dark emphasis for deep modules or recommendations.
- Put long evidence, open questions, and implementation detail behind native `<details>` elements.
- Every diagram has an adjacent one-sentence takeaway.
- Every report ends with one anchored top recommendation or next decision.

## Portability

The owning skill must reference `references/visual-report.md`, never `/meta`, another skill, or a suite-level path. The repository may maintain a canonical copy under `craft/meta/references/`, but packaging materializes a local copy beside each consumer. A standalone install must contain every file named by the skill.

## Quality gates

- Every card has a before/after visual or an explicit reason why a comparison does not apply.
- Internal card and recommendation links resolve.
- Visible prose stays concise; detailed evidence remains reachable.
- Markdown sources and product-memory records remain authoritative.
- Changed Markdown files carry a current `Last updated` line near the top.
