---
protocol: acs:task-graph
version: 1.0.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/task-graph.md
---

# Task Graph View Contract

Last updated: 2026-10-01

One rendering contract for every task graph the suite draws: the delivery plan DAG, the roadmap view, and the live progress view an implement run refreshes. It fixes the vocabulary, the palette, the layout, and the legend so two graphs from two skills read the same way.

The renderer is [`acs-draw-portfolio-dag`](../../skills/acs-draw-portfolio-dag/SKILL.md). Canonical tickets own status and dependencies; this protocol owns only how they are displayed. Derived views remain [Presenter](../skills-src/design/technical/acs-trace-requirements/references/visual-report.md) output and are rebuilt, never hand-edited.

## View status

Canonical tickets carry `Status` (`pending`, `in_progress`, `done`, `failed`, `superseded`), `Type` (`implementation`, `design`), and `Readiness` (`ready`, `needs-design`, `needs-criteria`, `needs-review`). The graph shows exactly one **view status** per ticket, derived in this order — first match wins:

| View status | Rule | Meaning |
| --- | --- | --- |
| `done` | the ticket is done | Complete, and its evidence counts for dependents |
| `superseded` | `Status: superseded` | Replaced by another ticket; not remaining work |
| `failed` | `Status: failed` | Attempted and failed; stays visible with its dependents blocked |
| `in_progress` | `Status: in_progress` | Claimed and running now |
| `needs_design` | not execution-ready — design ticket, readiness other than `ready`, or unready inputs | Cannot be dispatched until design or criteria land |
| `ready` | implementation, readiness `ready`, every prerequisite `done` | On the frontier: dispatchable now |
| `waiting` | otherwise — a prerequisite is not `done` | Blocked on dependencies |

`waiting` is the default, not a fallback error: a ticket with an unfinished prerequisite has no other truthful label. `superseded` overrides `waiting`, because a dead ticket is not waiting on anything.

Legacy manifests without `Type` or `Readiness` are treated as execution-ready implementations; their raw status text still separates done, in-progress, failed, and superseded.

## Palette

Colour carries **view status only**. Workstream is shown by lane position, tags are neutral outline pills, and no other element may use a status hue.

| View status | Fill | Border | Text | Legend label |
| --- | --- | --- | --- | --- |
| `done` | `#e6f5ec` | `#4a9d6e` | `#1e6b45` | Done |
| `in_progress` | `#fdf2df` | `#cf9a35` | `#7c5510` | In progress |
| `failed` | `#fbe8e5` | `#c85a49` | `#8a2f22` | Failed |
| `ready` | `#e8f1fc` | `#4b82c9` | `#1e4a8a` | Ready now |
| `needs_design` | `#efecfb` | `#7766cd` | `#443789` | Needs design or review |
| `waiting` | `#f2f3f6` | `#a9b0bb` | `#4c5361` | Waiting on prerequisites |
| `superseded` | `#f2f3f6` | `#a9b0bb` | `#6b7280` | Superseded |

`superseded` uses the `waiting` palette with a dashed border and 55% opacity, so it reads as retired rather than pending. Dark mode redefines these as tokens; the hues keep their identity and their relative contrast against the dark page.

Edges:

| Edge | Stroke | Meaning |
| --- | --- | --- |
| Critical | `#343b48`, 2.5px | This hop is on the remaining critical path |
| Satisfied | `#9ecbb1`, 1.2px | The prerequisite is done |
| Dependency | `#c3c8d1`, 1.2px | The prerequisite is not done |

Edges are orthogonal elbows from the right edge of the prerequisite to the left edge of the dependent. The critical path is drawn last, so it stays on top.

Tokens are CSS custom properties declared once in a single `:root` block, redefined under `prefers-color-scheme: dark`. No rule, script, or inline style may use a raw colour value; markup carries `var(--token)`. This is the [visual report contract](../skills-src/design/technical/acs-trace-requirements/references/visual-report.md#visual-and-runtime-rules) rule applied to task graphs, and it is what keeps the light and dark views from drifting apart.

## Layout

Columns are **waves**, rows are **workstream lanes**.

- `wave(ticket) = 1 + max(wave(prerequisite))`, and a ticket with no prerequisites is in wave 1. Wave _n_ holds the tickets whose longest prerequisite chain is _n_ — everything in a column can proceed in parallel once the columns to its left finish.
- Lanes keep the manifest's workstream order, so a workstream's tickets stay on one row and cross-workstream dependencies read as vertical hops.
- A lane with several tickets in one wave stacks them within that cell.
- Wave headers name each column, lane labels name each row with its ticket count, and a dashed rule separates the columns.
- A node shows the ticket's short id and title. Type, readiness, and status are already carried by the node colour and stated in full on the node tooltip, so they are not repeated as pills; only overlay tags such as `data` or `deploy`, which say something the colour does not, render as pills.

Layout is the default; the HTML view lets a user drag nodes, and those positions persist in `localStorage` under the `--storage-key` prefix. Changing the layout algorithm changes what stored positions mean, so the renderer's storage key carries a layout version: positions saved by an older layout do not apply to a newer one.

## Critical path

The critical path is the longest chain of **remaining** tickets, counted in tickets because tickets carry no duration estimate. Remaining means neither `done` nor `superseded` — a failed or unready ticket is still work the chain must traverse.

The chain's edges are drawn as critical edges, and the legend footer states it:

```
Remaining critical path: profile/D1 → profile/T2 → profile/T5 · 4 waves · 3/12 done
```

When no ticket remains, the footer says so instead (`All 12 tickets done · 4 waves`). Longer chains wrap rather than truncate; the summary is the one place the sequence is written out, so it is never abbreviated.

## Legend

One legend panel sits directly under the graph — not in the toolbar — and holds three rows in this order:

1. every view status present in the graph, as a fill-and-border swatch plus its legend label;
2. the three edge types, drawn as line samples;
3. the critical-path summary line.

Legend labels come from the palette table above. A ticket card, a node tooltip, or a toolbar badge that names a view status uses the same label as the legend — one vocabulary, no synonyms (`Complete` beside `Finished` beside `Done` is exactly the drift this contract removes).

## Parity between formats

HTML is the primary view. The Mermaid output is a secondary, text-diffable form and mirrors the same contract: `flowchart LR`, one `classDef` per view status with the palette above, a `subgraph` per workstream, critical edges styled by `linkStyle`, and the same critical-path summary line under the fence. A Mermaid file that styles only `done` misrepresents the graph and is out of contract.

Mermaid cannot read CSS custom properties, so it restates the palette hex. Both forms are generated from the same palette definition in the renderer, so they cannot drift.
