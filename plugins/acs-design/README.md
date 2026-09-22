# acs-design

Design phase plugin for the Agent Coding Skills (ACS) system. Covers requirements, UX design, and technical architecture across 12 skills and 8 specialist agents.

## Installation

```bash
npx skills add acs-design
```

Requires `acs-context` (direct) and `acs-plan` (peer).

## Design Workflow

The design phase runs in three tracks that feed each other:

1. **Requirements** — lock functional requirements and acceptance criteria before any design work begins
2. **UX Design** — establish design authority, define interaction structure, explore visual directions, validate with prototypes, and implement
3. **Technical Architecture** — audit existing structure (brownfield), design architecture and foundations, specify modules, validate the codebase

See `shared/workflows/design.md` for the full sequenced workflow.

## Skill Inventory

### Requirements (1 skill)

| Skill | What it does |
|-------|-------------|
| `acs-settle-requirements` | Defines functional requirements and testable acceptance criteria from accepted product intent |

### Technical Architecture (5 skills)

| Skill | What it does |
|-------|-------------|
| `acs-audit-architecture` | Reconstructs current module boundaries and coupling before brownfield design |
| `acs-design-architecture` | Maps features to modules, compares current/ideal/feasible architectures, records the selected evolution |
| `acs-design-foundation` | Designs reusable technical foundations — libraries, SDKs, middleware, infrastructure adapters |
| `acs-design-modules` | Turns a selected architecture into implementable code modules, interfaces, and dependency rules |
| `acs-validate-codebase` | Validates design and implementation reachability across routes, modules, and dependencies |

### UX Design (6 skills)

| Skill | What it does |
|-------|-------------|
| `acs-design-context` | Establishes or refreshes the root DESIGN.md — the project's design authority. Run first before any other UX skill |
| `acs-design-system-create` | Builds design authority from scratch when no DESIGN.md or reference brand exists |
| `acs-design-interaction-flow` | Defines information architecture, user flows, and the five interaction states as locked wireframes |
| `acs-visual-design-variants` | Explores three visual directions on locked interaction structure |
| `acs-validate-prototype` | Builds throwaway code to answer one design question |
| `acs-design-implement` | Turns an approved visual design into production code with design tokens wired up and WCAG AA met |

## Bundled Specialist Agents

Eight architecture review agents in `shared/agents/`:

- `adr-explorer.md` / `adr-reviewer.md` — architectural decision records
- `application-explorer.md` / `application-reviewer.md` — application structure
- `data-architecture-explorer.md` / `data-architecture-reviewer.md` — data layer
- `technology-explorer.md` / `technology-reviewer.md` — technology choices

Each explorer/reviewer pair follows the standard ACS pattern: the explorer reconstructs the current state; the reviewer evaluates it against the target design.

## Typical Sequences

**Greenfield from PRD:**
`acs-settle-requirements` → `acs-design-context` (or `acs-design-system-create`) → `acs-design-interaction-flow` → `acs-visual-design-variants` → `acs-design-architecture` → `acs-design-foundation` → `acs-design-modules`

**Brownfield change:**
`acs-audit-architecture` → `acs-settle-requirements` → `acs-design-architecture` → `acs-design-modules` → `acs-validate-codebase`

**UX-only feature:**
`acs-design-context` → `acs-design-interaction-flow` → `acs-visual-design-variants` → `acs-validate-prototype` → `acs-design-implement`
