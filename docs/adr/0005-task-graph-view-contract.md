# One view contract for every task graph

Last updated: 2026-10-01

Change: task-graph rendering unification
Status: accepted
Basis: review of `acs-draw-portfolio-dag`, its callers, and `scripts/gen-roadmap.py`, 2026-10-01
affects: `system/skills-src/authoring/acs-draw-portfolio-dag/**`, `system/skills-src/authoring/scripts/validate-report-html.py`, `system/skills-src/build/acs-implement/SKILL.md`, `system/skills-src/build/acs-plan-delivery/references/delivery-report.md`, `system/protocols/**`, `scripts/gen-roadmap.py`

Two renderers drew task graphs and disagreed about what the drawing meant. `render_dag.py` — called by `acs-plan-delivery`, `acs-implement`, and `acs-explore-unknowns` — used blue for "blocked" and orange for "ready". `scripts/gen-roadmap.py` used blue for "ready" and red for "blocked". Four status vocabularies described the same tickets (`pending | in_progress | done | failed | superseded` on the ticket, `blocked | ready | in_progress | done | failed` in the scheduler, `done | inprogress | frontier | todo` in the view, and seven more in the old roadmap). The palette existed in three places: hard-coded in the script, then restated in prose in two `SKILL.md` files. `failed` and `superseded` had no colour and fell into "blocked". The legend said "Finished" while the ticket cards said "Complete". The Mermaid output styled only `done`, so a Mermaid reader saw a graph with one status.

The suite now has one contract, [`task-graph.md`](../../system/protocols/task-graph.md), registered as `protocol:acs:task-graph` v1.0.0. It owns the view-status vocabulary, the palette, the layout, the critical path, and the legend. The skills link to it instead of restating it, and `render_dag.py` implements it.

- **Seven view statuses** are derived from the canonical ticket, first match wins: `done`, `superseded`, `failed`, `in_progress`, `needs_design`, `ready`, `waiting`. This covers the states the four-source vocabulary was approximating and gives `failed` and `superseded` their own meaning.
- **Layout is a waves × lanes grid.** Columns are dependency waves — `wave(n) = 1 + max(wave(prerequisite))` — so a column is what can run in parallel once the columns to its left finish. Rows stay workstream lanes. Edges are orthogonal elbows instead of Bézier curves.
- **The remaining critical path is computed and drawn.** Longest chain of tickets that are neither done nor superseded, counted in tickets because tickets carry no duration estimate. Its edges are thick; the legend footer states the chain.
- **Colour is defined once**, as CSS custom properties under `:root` with a `prefers-color-scheme: dark` override. The graph had no dark mode before.
- **Tag pills are neutral**, and the scanner's own type/readiness/status tags no longer render as pills. Purple "DATA" and brown "DEPLOY" pills competed with status colours, which is the same defect as the two palettes.

## Considered options

- **Keep both renderers and align their palettes.** Rejected. `gen-roadmap.py` has no caller — only `CHANGELOG.md` mentioned it — and a second implementation is how the two palettes diverged in the first place.
- **Keep the flat "one row per workstream" layout and only restyle.** Rejected. Node order within a row was the order the scanner found files, so the graph showed no parallelism: two tickets in the same workstream looked sequential whether or not either depended on the other. Waves make the parallel set readable, which is the question a delivery plan is asked.
- **Draw the critical path in the accent orange-red of the reference design.** Rejected in favour of ink. Red already means `failed`, and a fourth colour meaning would recreate exactly the ambiguity this contract removes.
- **Keep type/readiness/status as pills on the node.** Rejected. All three are already carried by the node colour and stated on the tooltip; as pills they clipped against a 190px node and competed with the overlay tags that carry information the colour does not.
- **Version the status vocabulary but keep the old view statuses as aliases.** Rejected. Aliases mean two names for one state, which is the drift being removed. `frontier` is not a synonym for `ready`, because `ready` now also requires `Type: implementation`.

## Consequences

- `scripts/gen-roadmap.py` is deleted with no replacement. The `CHANGELOG.md` entry that described it is annotated rather than rewritten.
- `layout` gains a version token in the storage key (`dag_<name>_grid-v1`), so drag positions saved against the old row layout do not apply to the grid.
- `tag_styles` in the overlay loses its `bg` and `fg` fields and keeps `label`. Existing overlays carrying colours still load; the extra keys are ignored.
- The delivery plan's `frontier` section is renamed to `ready`, and `--plan` mode renders ticket cards using the same label map as the legend.
- A test asserts that the rendered HTML contains no colour literal outside the palette token block, so the "defined once" rule is enforced rather than documented.
- `render_dag.py` keeps its single `computeStatus` function in the emitted JavaScript so the test harness can run it under Node and compare the graph's statuses against the ticket cards' statuses.
- `validate-report-html.py` decodes an internal link's fragment before matching it against the page's ids. It previously compared the raw text, so the delivery plan — whose ticket links percent-encode the `/` in a qualified id — failed its own `--version-only` gate on every ticket. The renderer's own test had decoded all along; only the validator had not.
