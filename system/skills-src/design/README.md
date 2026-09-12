# Design

Last updated: 2026-09-12

How the product should work, at three levels: what capabilities it provides (requirements), how users experience it (UX), and how the system is structured under the hood (technical). Three sequential sub-phases with explicit boundaries and handoffs — run the full [`/design` workflow](../../workflows/design.md) or enter individual sub-phases directly.

| Sub-phase | Defines | Directory |
| --- | --- | --- |
| Requirements | WHAT capabilities the product provides | `requirements/` |
| UX | HOW those capabilities are delivered (interaction + visual) | `ux/` |
| Technical | HOW to engineer them (domain model, architecture, ADRs) | `technical/` |

Requirements feed UX and technical design both. UX design feeds `build/plan-implementation` (design constraints) and production code via `ux/design-implement`. Technical design feeds `build/` and the implementation loop.

## When to enter — and when to skip

Entered from [`/plan`](../../workflows/plan.md) when `product.html` has accepted intent. The three sub-phases run sequentially; each produces a durable artifact the next consumes.

### Requirements (`requirements/`)

Enter when accepted product intent exists but functional requirements and testable acceptance criteria have not been written.

- `requirements/settle-requirements` — define what capabilities the product provides: observable behavior per actor and condition, acceptance criteria in Given/When/Then form, explicit scope boundary. Output: `specs/<spec>.md`.

Skip requirements when an existing canonical spec already covers the change. Route scope changes back to `/plan`, not here.

### UX (`ux/`)

Enter when what the user sees or navigates is undecided. Prerequisite: `specs/<spec>.md` from requirements. Shared design understanding is a triad — `product.html` is why, root `DESIGN.md` is how, `docs/design/ux-design.html` is what. The pipeline runs in stages — enter at the earliest unsettled one:

- `ux/design-context` — no design authority yet (no root `DESIGN.md`; a legacy `docs/design/system.md` counts but should be migrated), or a reference site/brand to import
- `ux/validate-prototype` — validate whether a design approach is worth building; throwaway variants, decision recorded, control returns
- `ux/design-interaction-flow` — flows, layout, information hierarchy, or five-state coverage undecided; locks wireframe sections in the canonical prototype
- `ux/visual-design-variants` — structure locked, visual direction open; merges the winner as the styled section
- `ux/design-implement` — styled section approved, needs production code
- Full pipeline doc: [`workflows/design.md`](../../workflows/design.md); UX system + external dispatch: [`ux/README.md`](ux/README.md); external tool catalog: [`ux/external-skills.md`](ux/external-skills.md)

UX skills operate on the whole product, not individual pages. One design document (`docs/design/ux-design.html`) encodes the complete product vision; sections transition from wireframe → styled → implemented as gates are passed.

### Technical (`technical/`)

Enter when the system's shape is undecided. Prerequisite: `specs/<spec>.md`; `docs/design/ux-design.html` strongly recommended. Skills follow a three-phase progression:

**Prototype validation** (problem space — is it worth building?):
- `technical/explore-unknowns` — spike technical unknowns, map dependency-ordered decision tickets; run before committing to full design

**Engineering hardening** (solution space — can we maintain it long-term?):
- `technical/engineer-domain-model` — entities, value objects, aggregates, bounded contexts; resolves overloaded terms and produces `CONTEXT.md` / ADRs
- `technical/harden-architecture` — module boundaries, seams, deep modules, interface contracts; produces `DESIGN.md`
- `technical/challenge-approach` — adversarial review of design decisions; stress-test before committing

**Component extraction** (composable space — extract after 3+ proven uses):
- `technical/audit-architecture` — assess existing architecture before refactoring; identifies duplication and extraction opportunities

**Agent/LLM projects only** (outside the standard SDLC loop):
- `technical/design-agent-architecture` — LLM orchestration, tool calling, memory patterns
- `technical/design-operational-ontology` — knowledge representation, reasoning structures

Skip to `build/` when `DESIGN.md` exists with settled module boundaries and interface contracts, vocabulary is stable, and the change fits the existing architecture.

Both UX and technical branches may run for the same effort. Every design skill can read the product document resolved through `docs/agents/memory.md` and `state.md`. Each skill also runs standalone.
