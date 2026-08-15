# Design

Last updated: 2026-08-10

How the product should work, at two levels: how users experience it, and how the system is structured under the hood.

| Sub-phase | Concerns | Directory |
| --- | --- | --- |
| UX | User flows, interaction patterns, navigation, UI system | `ux/` |
| Technical | Domain model, system architecture, ADRs, structural decisions | `technical/` |

UX design feeds `engineering/frontend`. Technical design feeds `engineering/feature` and `engineering/frontend` both.

## When to enter — and when to skip

This phase is optional. It is entered from the design gate in `product/definition/write-prd`, which routes by the largest open question the PRD leaves behind:

- **Enter `ux/`** when what the user sees or navigates is undecided — layout, information hierarchy, or the visual system (`ui-ux-pro-max`), or a foggy route of interdependent decisions (`wayfinder`).
- **Enter `technical/`** when the system's shape is undecided — vague or conflicting terms and hard-to-reverse trade-offs (`domain-modeling`), strained module boundaries (`codebase-design`), an agent system (`design-agent-architecture`), or an operational decision loop (`design-operational-ontology`).
- **Skip to `engineering/feature/spec`** when the PRD's Part 2 flowchart and Part 3 five-state blocks are complete, vocabulary is settled, and the change fits the existing architecture.

Both branches may run for the same effort. A design question conversation can't settle goes to `product/definition/prototype`: throwaway variants, decision recorded, control returns to the skill that raised it.

Upstream input for every design skill is the effort PRD (`docs/product/<slug>/prd.md`) when one exists; each skill also runs standalone.
