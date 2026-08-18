# Design

Last updated: 2026-08-17

How the product should work, at two levels: how users experience it, and how the system is structured under the hood.

| Sub-phase | Concerns | Directory |
| --- | --- | --- |
| UX | Design context, user flows, interaction patterns, visual system, implementation | `ux/` |
| Technical | Domain model, system architecture, ADRs, structural decisions | `technical/` |

UX design feeds `engineering/feature/spec` (design constraints) and production code via `ux/design-implement`. Technical design feeds `engineering/feature` and frontend implementation both.

## When to enter — and when to skip

This phase is optional. It is entered from the design gate in `product/definition/write-prd`, which routes by the largest open question the PRD leaves behind:

- **Enter `ux/`** when what the user sees or navigates is undecided. The UX pipeline runs in stages — enter at the earliest unsettled one:
  - `ux/design-context` — no design token source yet (no `DESIGN.md`, no `docs/design/system.md`), or a reference site/brand to import
  - `ux/interaction-design` — flows, layout, information hierarchy, or five-state coverage undecided
  - `ux/visual-design-variants` — structure settled, visual direction open
  - `ux/design-implement` — visual approved, needs production code
  - Full pipeline doc: [`workflows/design.md`](../../workflows/design.md); external tool catalog: [`ux/README.md`](ux/README.md)
- **Enter `technical/`** when the system's shape is undecided — vague or conflicting terms and hard-to-reverse trade-offs (`domain-modeling`), strained module boundaries (`codebase-design`), an agent system (`design-agent-architecture`), or an operational decision loop (`design-operational-ontology`).
- **Enter `craft/meta/wayfinder`** when the destination is known but the route is foggy — multiple interdependent decisions, larger than one session.
- **Skip to `engineering/feature/spec`** when the PRD's Part 2 flowchart and Part 3 five-state blocks are complete, vocabulary is settled, and the change fits the existing architecture.

Both branches may run for the same effort. A design question conversation can't settle goes to `prototype`: throwaway variants, decision recorded, control returns to the skill that raised it.

Upstream input for every design skill is the effort PRD (`docs/product/<slug>/prd.md`) when one exists; each skill also runs standalone.
