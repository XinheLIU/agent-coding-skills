# Technical Design View

Last updated: 2026-10-11

One HTML view, `docs/design/technical-design.html`, renders the whole technical record. It replaces per-skill report files. Apply the display and Writing rules in [the visual report contract](../../../../../skills/acs-map-current-product/references/visual-report.md) and the tab mechanics in [the tabbed report protocol](../../../authoring/references/tabbed-discovery-report.md); this file adds only the technical-design content requirements.

The view is derived. Every fact, ID and verdict comes from `technical-design.md` at a named revision, which the header shows. It is a *living view*: keep the fixed path, and set `view-kind="living"` and the `generated` and `source-revision` meta tags (see the visual contract's date-and-version rule). On refresh, rebuild the whole file. Never edit it by hand, and never let it hold a conclusion that the record lacks.

## Tabs

Render one tab per record section that is not `not assessed`. Show each unassessed section as a disabled tab, so omissions are visible.

| Tab | Required content |
| --- | --- |
| Overview | Card scorecard (card · status · mode · P0/P1/P2 open counts), consumed revisions, and one anchored top recommendation |
| Architecture | Current / ideal / feasible diagram; one card per option with trade-offs; capability → owner map; decision ledger |
| Modules | One card per structural change: before/after ownership, seam placement, dependency direction, interface depth, migration step |
| Contracts | Invariant table (ID · statement · enforced at · verified by); failure-modes matrix (path × failure × handled × tested × visible) with silent-and-untested rows in red |
| Test Strategy | Critical path × layer grid (unit / integration / contract / e2e / characterization); doubles and fixtures policy; CI gates |
| Traceability | Status matrix (requirement · entry · module · contract · test · status) with status pills; unexpected code list |
| Ledger | All findings, filterable by card, severity, and status; each row links to its target item's anchor in its tab |

## Rules

- Every target item and finding keeps its record ID as its HTML `id`, so links from other records resolve.
- Structural cards (Architecture options, Modules changes) use `data-visual="compare"`: Before and After panes.
- Table-shaped tabs still get a visual, with `data-visual="single"` beside the table. A tab of tables with no diagram fails the validator.
  - Contracts: draw the call path, mark each invariant's enforcement point, and draw silent failure paths in red.
  - Test Strategy: draw the layer grid, with critical paths as rows.
  - Traceability: draw requirement → module → test chains, with breaks in red.
- Severity colors follow the visual contract: red for P0 and silent failures, amber for P1, neutral for P2.
- Put long evidence in `<details>`. The first viewport of each tab shows the status and what to act on.
- End the Overview tab with exactly one next action naming the card that owns it.
