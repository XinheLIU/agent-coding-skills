# Design Workflow

Last updated: 2026-09-25

Transform accepted product intent into settled requirements, a unified UX design, and an engineering design. Three sequential sub-phases with clear boundaries: requirements define WHAT, UX defines HOW (delivery), technical defines HOW (engineering).

```
entry_artifact: docs/product/<product>/product.html (accepted intent)
exit_artifact:  canonical spec + accepted prototype/contracts/decisions + applicable DESIGN.md
approval_gate:  Necessary decisions accepted per slice before execution; existing approvals persist
```

## Overview

```
accepted intent → [1] requirements → [2] UX design → [3] technical design → acs-plan-delivery
                      WHAT                HOW delivery    HOW engineering
                  acs-settle-requirements  acs-design-context    acs-audit-architecture
                                       acs-validate-prototype acs-design-architecture
                                       acs-design-interaction-flow acs-design-foundation
                                       acs-visual-design-variants acs-design-modules
                                       acs-design-implement  acs-validate-codebase
```

## Sub-phase 1: Requirements (WHAT)

**Goal:** Define what capabilities the product provides. No screens, no components, no algorithms — only observable behavior and testable acceptance criteria.

**Entry:** Accepted intent records in `product.html`.

**Skills:**
- `/acs-settle-requirements` — functional requirements, acceptance criteria, scope boundary

**Exit:** `specs/<spec>.md` with complete functional requirements and testable criteria.

**Gate:** Requirements must be reviewed before UX begins. Unresolved blocking questions stay in the spec as explicit gaps, not silent assumptions.

## Sub-phase 2: UX (HOW delivery)

**Goal:** Define how capabilities are delivered — interaction, flow, and visual design. Produces one unified design document inspecting the whole product, not per-page fragments.

**Entry:** `specs/<spec>.md` from sub-phase 1.

**Skills:**
- `/acs-design-context` — inspect whole product vision, establish design authority, produce root `DESIGN.md`
- `/acs-validate-prototype` — validate whether a design approach is worth building (problem space)
- `/acs-design-interaction-flow` — user journeys, state transitions, interaction model
- `/acs-visual-design-variants` — visual layer, typography, color, spacing based on `DESIGN.md`
- `/acs-design-system-create` — reusable design patterns when duplication is visible (3+ uses)
- `/acs-design-implement` — final prototype/design doc; merges all prior design work

**Exit:** the configured canonical prototype (default `docs/design/prototype.html`) with sections transitioning from wireframe → styled → implemented as gates are passed. Accepted visual content and consequential rationale are Persistent Memory, preserved at their reviewed revisions.

**Note:** UX skills operate on the whole product, not individual pages. The prototype is the durable what — every approval gate is a section transition in one file, not scattered artifacts.

## Sub-phase 3: Technical (HOW engineering)

**Goal:** Map accepted features to an implementable architecture, shared technical foundations, code modules, and verified wiring.

**Entry:** canonical spec/criteria and relevant accepted prototype sections or existing technical inputs.

**Skills:**
- `/acs-audit-architecture` — reconstruct current structure when brownfield evidence is unclear
- `/acs-design-architecture` — map features to business modules and compare current, ideal, and feasible designs
- `/acs-design-foundation` — design libraries, SDKs, components, middleware, and infrastructure adapters for named consumers
- `/acs-design-modules` — specify code interfaces, types, directories, wiring, dependency rules, and migration
- `/acs-validate-codebase` — verify design and implementation reachability across routes, menus, exports, interfaces, and modules

The handoff is `requirement → capability/module → contract → code entry → verification evidence`. Greenfield uses a minimum real end-to-end path; brownfield includes migration and preservation evidence.

**Exit:** technical design with architecture options, capability contracts, module contracts, wiring, gaps, and validation evidence.

**Gate:** Relevant technical decisions must be accepted before dependent slices execute. Their tickets may be planned earlier.

## Entry Criteria

- `docs/product/<product>/product.html` has at least one accepted intent record.
- Canonical paths resolve from explicit inputs, existing homes, or `docs/agents/memory.md`; configuration is needed only when routing remains ambiguous.

## Exit Criteria

- `specs/<spec>.md`: complete functional requirements with testable acceptance criteria.
- Configured prototype: accepted design intent for the assessed surfaces, with retained exact visual versions.
- `DESIGN.md`: applicable visual tokens, design rationale and rules. Technical contracts, domain terminology, and ADRs retain their separate canonical homes.
- Relevant layers reviewed and accepted for the scope being handed off; existing substantive decisions satisfy the gate. Remaining questions identify the slices they block.

## Handoff

Persist formal proposals before review. Use the [Presenter](../protocols/presenter.md) to compare their referenced revisions; keep product HTML and prototypes as canonical artifacts. Record feedback against the exact decision scope and content revision. A report is a derived reading view, and acceptance is distinct from permission to implement.

Pass the canonical change ID, spec/criterion references, relevant UX and technical decisions/contracts, consumed revisions, migration/preservation constraints, and remaining blockers to [acs-plan-delivery](../skills-src/build/acs-plan-delivery/SKILL.md) (reference procedure; capability not installed). It generates or refreshes the same `delivery-plan.html` with the plan and embedded DAG, then opens it. Link authoritative artifacts rather than copying them into tickets.

A request from `acs-plan-delivery` can target one missing decision. Resolve it with accepted artifact/evidence references and return to the existing graph; the planner reassesses affected slices. Independent ready slices can proceed while this design work remains open.

Shared context coordination: [context-coordination.md](../protocols/context-coordination.md)
