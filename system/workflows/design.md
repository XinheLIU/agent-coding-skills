# Design Workflow

Last updated: 2026-09-13

Transform accepted product intent into settled requirements, a unified UX design, and an engineering design. Three sequential sub-phases with clear boundaries: requirements define WHAT, UX defines HOW (delivery), technical defines HOW (engineering).

```
entry_artifact: docs/product/<product>/product.html (accepted intent)
exit_artifact:  specs/<spec>.md + docs/design/ux-design.html + DESIGN.md
approval_gate:  User must approve all three layers before handoff to /build
```

## Overview

```
accepted intent → [1] requirements → [2] UX design → [3] technical design → /build
                      WHAT                HOW delivery    HOW engineering
                  settle-requirements  design-context    explore-unknowns
                                       validate-prototype engineer-domain-model
                                       design-interaction-flow harden-architecture
                                       visual-design-variants
                                       design-implement
```

## Sub-phase 1: Requirements (WHAT)

**Goal:** Define what capabilities the product provides. No screens, no components, no algorithms — only observable behavior and testable acceptance criteria.

**Entry:** Accepted intent records in `product.html`.

**Skills:**
- `/settle-requirements` — functional requirements, acceptance criteria, scope boundary
  
**Exit:** `specs/<spec>.md` with complete functional requirements and testable criteria.

**Gate:** Requirements must be reviewed before UX begins. Unresolved blocking questions stay in the spec as explicit gaps, not silent assumptions.

## Sub-phase 2: UX (HOW delivery)

**Goal:** Define how capabilities are delivered — interaction, flow, and visual design. Produces one unified design document inspecting the whole product, not per-page fragments.

**Entry:** `specs/<spec>.md` from sub-phase 1.

**Skills:**
- `/design-context` — inspect whole product vision, establish design authority, produce root `DESIGN.md`
- `/validate-prototype` — validate whether a design approach is worth building (problem space)
- `/design-interaction-flow` — user journeys, state transitions, interaction model
- `/visual-design-variants` — visual layer, typography, color, spacing based on `DESIGN.md`
- `/design-system-create` — reusable design patterns when duplication is visible (3+ uses)
- `/design-implement` — final prototype/design doc; merges all prior design work

**Exit:** `docs/design/ux-design.html` — a single openable document encoding the whole product design, with sections transitioning from wireframe → styled → implemented as gates are passed.

**Note:** UX skills operate on the whole product, not individual pages. The prototype is the durable what — every approval gate is a section transition in one file, not scattered artifacts.

## Sub-phase 3: Technical (HOW engineering)

**Goal:** Map accepted features to an implementable architecture, shared technical foundations, code modules, and verified wiring.

**Entry:** `specs/<spec>.md` + `docs/design/ux-design.html`.

**Skills:**
- `/audit-architecture` — reconstruct current structure when brownfield evidence is unclear
- `/design-architecture` — map features to business modules and compare current, ideal, and feasible designs
- `/design-foundation` — design libraries, SDKs, components, middleware, and infrastructure adapters for named consumers
- `/design-modules` — specify code interfaces, types, directories, wiring, dependency rules, and migration
- `/validate-codebase` — verify design and implementation reachability across routes, menus, exports, interfaces, and modules

The handoff is `requirement → capability/module → contract → code entry → verification evidence`. Greenfield uses a minimum real end-to-end path; brownfield includes migration and preservation evidence.

**Exit:** technical design with architecture options, capability contracts, module contracts, wiring, gaps, and validation evidence.

**Gate:** User approves DESIGN.md before handoff to /build.

## Entry Criteria

- `docs/product/<product>/product.html` has at least one accepted intent record.
- `docs/agents/memory.md` exists.

## Exit Criteria

- `specs/<spec>.md`: complete functional requirements with testable acceptance criteria.
- `docs/design/ux-design.html`: unified design doc encoding whole product vision.
- `DESIGN.md`: ADRs, domain model, module boundaries, interface specs.
- All three layers reviewed and approved by user.

## Handoff

Passes specs + UX design + DESIGN.md to `/build`. The build workflow reads DESIGN.md for engineering decisions and specs for acceptance criteria.

Shared context coordination: [context-coordination.md](context-coordination.md)
