# Design Workflow Quick Start

Last updated: 2026-09-26

The short path through the UX pipeline. Full sequence and gates: [`system/workflows/design.md`](system/workflows/design.md).

## 30-Second Overview

Three skills, one durable artifact:

```
/acs-design-interaction-flow → wireframe sections + state coverage
/acs-visual-design-variants  → winning treatment merged (→ styled)
/acs-design-implement        → production code (→ implemented)
```

Each stage advances sections of one canonical prototype rather than producing its own file. Approval is a section transition, not a handoff document.

## The design triad

Three durable documents, each answering one question:

| | Document | Owns |
| --- | --- | --- |
| **Why** | `docs/product/<product>/product.html` | Product intent; every prototype surface links its capability record |
| **How** | `DESIGN.md` at the project root | Design authority: visual tokens in YAML frontmatter, rationale in prose |
| **What** | `docs/design/prototype.html` | The canonical prototype, one self-contained file |

Working exploration — journey maps, state tables, variant candidates — lives and dies in the work root.

## When to Use Each Skill

### `/acs-design-interaction-flow` — Start Here

Use when starting a feature, when user flows are unclear, or when you don't know which states to show.

**Output:** wireframe sections in the prototype, marked `data-fidelity="wireframe"` with `data-structure="locked"`, plus the five state blocks per surface.

### `/acs-visual-design-variants` — After Structure Locks

Use when wireframes are accepted and you need to see visual options.

**Requires:** locked wireframe sections and `DESIGN.md` tokens.

**Output:** the winning treatment merged into those sections, advancing them to `data-fidelity="styled"`. Candidates stay in the work root.

### `/acs-design-implement` — Final Step

Use when the visual design is accepted and you're ready for production code.

**Output:** component code, plus sections marked `data-fidelity="implemented"` with component pointers.

## First-Time Setup

`/acs-design-context` inspects the whole product and writes root `DESIGN.md` — typography, colors, spacing, and the rationale behind them. Run once per project. A legacy `docs/design/system.md` stays canonical until this skill folds it in and leaves a pointer.

`/acs-design-system-create` extracts reusable patterns once duplication is visible (3+ uses).

## Key Rules

### Five states are mandatory

Every surface defines **LOADING** (skeleton), **EMPTY** (warm, with a primary action), **ERROR** (specific, with recovery), **SUCCESS** (full data), and **PARTIAL** (degraded or incomplete).

**Why:** these get forgotten, which is how "No data" ships as an empty state. Making them mandatory and machine-checkable via `data-state` blocks prevents it.

### Structure locks after interaction design

Once wireframe sections are accepted, button positions, navigation hierarchy, and user flows are locked — recorded as `data-structure="locked"`, not as prose. Visual design may change only color, typography, spacing, and borders.

**Why:** separating structure from style makes iteration faster, and one token source prevents two authorities disagreeing.

### Shipped code is canonical behavior

The prototype section is canonical *intent*; shipped code is canonical *behavior*. Divergence is reported and reconciled, never silent.

## Common Patterns

| Situation | Sequence |
| --- | --- |
| New feature | interaction-flow → visual-design-variants → design-implement |
| Visual tweak only | visual-design-variants (reads locked sections) → design-implement |
| Interaction needs a fix | interaction-flow (revise, unlock scope) → visual-design-variants → design-implement |

## PRD Integration

If the spec carries five-state blocks, `/acs-design-interaction-flow` reads them as a seed, fills gaps, and offers to write back — so state definitions have one source of truth.

## Troubleshooting

| Symptom | Cause |
| --- | --- |
| "No wireframe sections found" | Run `/acs-design-interaction-flow` first |
| "No design system found" | Optional — run `/acs-design-context`, or the skill uses defaults |
| Visual design moved a button | A bug. Visual design cannot change locked structure — report it |
| Missing states | `/acs-design-interaction-flow` enforces all five; check the `data-state` blocks |
| Need a different aesthetic | Re-run `/acs-visual-design-variants` with a new direction, or update `DESIGN.md` |

## Full Documentation

- **Workflow and gates:** [`system/workflows/design.md`](system/workflows/design.md)
- **Design contract:** [`system/protocols/design-memory.md`](system/protocols/design-memory.md)
- **External design skills:** [`system/skills-src/design/ux/external-skills.md`](system/skills-src/design/ux/external-skills.md)
