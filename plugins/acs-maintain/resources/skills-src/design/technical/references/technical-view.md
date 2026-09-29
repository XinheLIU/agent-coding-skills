# Technical Design View

Last updated: 2026-09-29

One HTML view, `docs/design/technical-design.html`, renders the whole technical record. It replaces per-skill report files. Apply the display rules in [the visual report contract](../../../authoring/references/visual-report.md) and the tab mechanics in [the tabbed report protocol](../../../authoring/references/tabbed-discovery-report.md); this file adds only the technical-design content requirements.

The view is derived. Every fact, ID, and verdict comes from `technical-design.md` at a named revision, shown in the header. Rebuild the whole file on refresh; never edit it by hand and never let it hold a conclusion the record lacks.

## Tabs

Render one tab per record section that is not `not assessed`. Unassessed sections appear as a disabled tab so omissions are visible.

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
- Structural cards (Architecture options, Modules changes) carry a current/target visual; tables (Contracts, Test Strategy, Traceability) do not need one.
- Severity colors follow the visual contract: red for P0 and silent failures, amber for P1, neutral for P2.
- Long evidence sits in `<details>`; the first viewport of each tab shows status and what to act on.
- End the Overview tab with exactly one next action naming the card that owns it.
