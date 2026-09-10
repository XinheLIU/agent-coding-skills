# Design Workflow

Last updated: 2026-09-09

This workflow transforms product intent into implemented components through **design context → interaction design → visual design → implementation**. Shared design understanding is a triad — `product.html` is **why**, root `DESIGN.md` is **how**, `docs/design/prototype.html` is **what** (contract: `skills-src/craft/context/init-context/references/design-memory.md`). Pipeline skills own design reasoning, gates, and artifact validation; the coordinator binds optional design capabilities from the six-layer catalog (`skills-src/design/ux/external-skills.md`; system overview: `skills-src/design/ux/README.md`).

## Overview

```
PRD (WHY) → design context → interaction design → visual design → implement code → shipped component
            (⑤ DESIGN.md)     (③ lock structure)   (①③⑥ style it)   (⑥+③ production)
            ↓                  ↓                     ↓                 ↓
            HOW written        WHAT: wireframe        WHAT: styled      WHAT: implemented
                               sections locked        section merged    + component docs
```

**Key principles:**

1. **Interaction before visuals** — structure (what/where/when) is locked (`data-structure="locked"` in the prototype) before color/typography/polish.
2. **One canonical token source** — root `DESIGN.md` is the only how downstream skills read for visual values; `/design-context` decides what feeds it and keeps the prototype's `:root` block in sync.
3. **The prototype is the durable what** — every approval gate lands in `docs/design/prototype.html` as a section transition (`wireframe → styled → implemented`), so shared understanding is one openable file, not scattered effort intermediates.
4. **External skills carry heavy work** — the coordinator probes available capabilities for the one or two slots requested by the stage, recognizing them by capability signature rather than vendor name, and offers what it finds; the native workflow is always the recommended fallback.

## The Five Skills

### 0. `/design-context` — Design Authority (ENTRY POINT)

**Purpose**: Decide where design authority comes from and produce the canonical root `DESIGN.md`.

**When**: Starting design work; a legacy `docs/design/system.md` needs migrating; you have a reference site/brand to import; the prototype's tokens drifted from DESIGN.md.

**Process**:
- Detects `DESIGN.md` (root), legacy `docs/design/system.md`, the prototype, PRD Part 1
- Branches: adopt existing DESIGN.md → migrate legacy system.md → extract from a reference site (⑤ extractors) → adopt a ready-made brand spec (④ catalogs) → or hand off to `/design-system-create` for from-scratch creation
- Resolves authority conflicts (default: existing DESIGN.md frontmatter wins visual values; legacy prose survives as rationale)
- Writes `DESIGN.md` after approval; pointers the legacy file; re-syncs the prototype's `:root` token block

**Outputs**: root `DESIGN.md` (Current State, git-tracked) — the triad's **how**

**External dispatch**: layers ⑤ (DESIGN.md lifecycle + extractors) and ④ (template catalogs). When an accepted ⑤ tool owns the DESIGN.md lifecycle, writes route through it and are reconciled; the file is canonical either way.

---

### 0b. `/design-system-create` — From-Scratch Fallback

**Purpose**: Consultatively create the root `DESIGN.md` when there is nothing to adopt.

**When**: Called directly, or via `/design-context` Step 3 when the user picks the native path.

**Process**: gathers product context (PRD Part 1) → proposes typography/color/spacing/layout with rationale → optional layer-② knowledge lookup for font pairings and palettes → preview HTML → approval → writes `DESIGN.md` (YAML frontmatter tokens + prose).

**Outputs**: root `DESIGN.md` (Current State); `<work-root>/<effort>/design/system-preview.html` (Run Context, disposable after reconciliation)

---

### 1. `/interaction-design` — Structure & States (CORE)

**Purpose**: Define HOW users interact before HOW it looks. Structure over style.

**When**: New feature with unclear flows; PRD Part 3 five-state blocks are thin.

**Process**:
- Reads the configured `product.html#prd` index and linked Part 1/3 records; canonical legacy PRDs remain readable
- Designs information architecture (what the user sees first/second/third)
- Fills the **interaction state table** — LOADING/EMPTY/ERROR/SUCCESS/PARTIAL for every feature (mandatory, no gaps)
- Maps user journeys with emotional arc
- Drafts **low-fidelity wireframe sections** (gray boxes, NO colors/fonts), each linking its `product.html` capability record via `data-capability`
- At approval, merges the sections into `docs/design/prototype.html` at `wireframe` fidelity with `data-structure="locked"`
- Documents responsive + accessibility requirements; surfaces unresolved decisions

**Outputs**: locked wireframe sections in `docs/design/prototype.html` (Change Context); working exploration in `<work-root>/<effort>/interaction/{state-table.md,journey-map.md,decisions.md,responsive-a11y.md,wireframes/}`

**Critical constraint**: Wireframe sections have no visual styling — only structure. Structure locks at approval; reopening a locked section is explicit and drops it back to wireframe fidelity.

**External dispatch**: optional layer-② knowledge pass for state-design and flow-pattern guidelines, cited in `decisions.md`. The five-state table itself is always native.

---

### 2. `/visual-design-variants` — Visual Exploration

**Purpose**: Explore visual directions on the locked structure, then merge the winner into the canonical prototype.

**When**: After locked wireframe sections exist and root `DESIGN.md` exists.

**Process**:
- **Requires** locked sections in `docs/design/prototype.html` and `DESIGN.md` (hard prerequisites)
- Defines 3 genuinely different visual directions (anti-convergence rule)
- Generates 3 variant HTMLs in the working layer — same structure, different visual treatment — each showing all 5 states with a state switcher
- Iterates (max 3 rounds); at approval merges the winning treatment into the surface's section, `wireframe → styled`

**Outputs**: the styled section in `docs/design/prototype.html` (Change Context); `<work-root>/<effort>/visual/{variants/variant-{a,b,c}.html,decision.md,constraints.md}` (Run Context)

**Critical constraint**: CANNOT change button positions, navigation hierarchy, or state transitions — only visual properties vary, and every value traces to `DESIGN.md`.

**External dispatch**: layer-① taste skills sharpen direction strategies; layer-⑥ production engines may render the variant HTMLs. Reconciliation contract: locked structure preserved, DESIGN.md tokens only, output lands at `visual/variants/variant-{a,b,c}.html` with the state switcher intact; only the approval gate merges into the prototype.

---

### 3. `/design-implement` — Production Code

**Purpose**: Convert the styled section into production code matching the project's tech stack.

**When**: A `styled`, locked section exists in the prototype and the user is ready to build.

**Process**:
- Reads the styled section + `DESIGN.md` (+ `state-table.md` while the effort lives)
- Detects tech stack (React/Vue/Svelte/HTML × Tailwind/CSS-in-JS/…)
- Extracts design tokens into stack-appropriate format
- Generates semantic, accessible, responsive component code implementing **all 5 states**
- Documents the component; marks the section `implemented` with `data-component` / `data-component-doc` pointers

**Outputs**: component code in project source (project-tracked); `docs/design/components/<name>.md` (Current State with linked change rationale); the section marked `implemented`

**External dispatch**: optional layer-③ polish pass (interaction craft, motion, feel-better, a11y review) over generated code — within token authority; structural changes route back to `/interaction-design`. Applied fixes are recorded in the component doc.

## External Orchestration

The six-layer model (full catalog: `skills-src/design/ux/external-skills.md`) maps to pipeline stages:

| Layer | What it provides | Consumed by | When absent |
|:---:|---|---|---|
| ① Taste / Judgment | Aesthetic direction, anti-slop stance | `visual-design-variants` Step 2.5 | Directions proposed inline |
| ② Design Knowledge | Font/palette/guideline databases | `design-system-create` Steps 2.2–2.3, `interaction-design` Step 1.5 | Proposed from first principles |
| ③ Method / Workflow | Design workflows, polish, motion, redesign | `design-implement` Step 4.5 (polish); redesign tools run before re-entering the pipeline | Built-in quality gates |
| ④ Templates & References | Ready-made brand specs | `design-context` Step 2 | Create from scratch |
| ⑤ Design Context | DESIGN.md format, extractors, lifecycle | `design-context` Steps 1–3 | Native `design-system-create` path |
| ⑥ Production Environments | High-fidelity mockup/demo engines | `visual-design-variants` Step 2.5 | Inline HTML generation |

No stage needs more than two of these slots, so none probes all six. The coordinator probes requested slots at the point of use, serializes the result into `<work-root>/<effort>/design/capabilities.md`, and reads that record on re-entry instead of asking again. The row doubles as the step's done condition — an optional step ends when its slot row exists, whether it reads `none`, `declined`, or `accepted`.

Every dispatch follows the same contract: **the pipeline skill owns the artifacts; the external skill is a producer whose output is reconciled into the canonical paths.** Skills recognize capabilities by signature, never by vendor name. The pipeline is complete with no external tools installed; `skills-src/design/ux/external-skills.md` catalogs what may optionally slot in, for a human choosing what to install — no skill reads it at runtime.

Technical design carries a lighter version: `design-agent-architecture` and `design-operational-ontology` offer a **diagramming** capability for the diagram each must produce, and fall back to drawing it directly. The coordinator binds optional diagramming; accepted technical decisions/contracts remain linked Change Context even when no run artifact is needed.

## Context and acceptance

Use [the shared protocol](../skills-src/craft/context/init-context/references/PROTOCOL.md) for lifecycle and identity; [the Design contract](../skills-src/craft/context/init-context/references/design-memory.md) defines artifact roles. The coordinator supplies paths and canonical change/spec/criterion IDs and applies transitions under [context coordination](context-coordination.md). Keep requirement text in its canonical spec; design records reference it.

At every acceptance gate retain consequential decisions with ID, rationale, alternatives, affected surfaces, and consumed requirement/token/contract revisions beside the accepted design or in Change Context. Component documentation must not be the first durable home of rationale. Return those references, delta, blockers, and next action; the coordinator updates run routing and applies scoped freshness propagation.

The prototype preserves accepted intent; shipped code establishes actual behavior. Record divergence and route reassessment to Design. Do not require a synchronized second implementation of the UI. Reopen sections only for accepted design changes. Drafts/variants are disposable only after essential rationale and evidence are retained.

## Workflow Patterns

### Pattern 1: Complete Flow (New Feature)

```
1. /design-context              → root DESIGN.md (adopt / migrate / extract / create)
2. /interaction-design          → locked wireframe sections in prototype.html → APPROVAL GATE
3. /visual-design-variants      → styled section merged → APPROVAL GATE
4. /design-implement            → component code + docs + section marked implemented
```

**Time**: ~1-2 hours (interaction takes longest).

### Pattern 2: Visual Iteration Only

Interaction structure is correct; need a different visual treatment.

```
1. /visual-design-variants  (re-styles the locked sections; they drop to wireframe treatment for exploration) → new styled section
2. /design-implement        → new component code
```

**Time**: ~30 minutes.

### Pattern 3: Interaction Revision

Visual is wrong because the structure is wrong.

```
1. /interaction-design (reopen the section)   → revised structure, re-locked → APPROVAL GATE
2. /visual-design-variants (regenerate)       → new variants on revised structure
3. /design-implement
```

**Time**: ~1 hour.

### Pattern 4: Quick Implementation (Design Already Approved)

HTML mockup in hand, need production code.

```
1. Wrap the mockup as a prototype section: data-surface, data-capability,
   data-fidelity="styled", data-structure="locked", five data-state blocks
2. Reconcile its visual values into DESIGN.md tokens (run /design-context if none exists)
3. /design-implement
```

**Time**: <30 minutes.

### Pattern 5: Redesign Existing UI

```
1. External layer-③ redesign tool (audit / redesign / polish — see README catalog)
   runs against the existing UI, OUTSIDE this pipeline
2. Re-enter at /visual-design-variants if structure is kept,
   or /interaction-design if flows change
3. /design-implement
```

### Pattern 6: Reference-Driven New Project

"Make it look like Linear."

```
1. /design-context  → extract (⑤) or adopt (④) the brand spec → root DESIGN.md
2-4. as Pattern 1
```

## Integration Points

### Upstream (design reads from)

- the configured `product.html#prd` (legacy PRDs remain readable) Part 1 (persona, platform, product type) and Part 3 (five-state seed) — the **why**; every prototype section links back to it. With no product docs, `map-current-product` infers the baseline from the repo.
- `DESIGN.md` at project root — the **how** (this pipeline's own canonical output; also maintained by ⑤ lifecycle tools)
- `CONTEXT.md` (binding design principles or constraints)
- `state.md` for the active effort (what feature is being built)

Entry gate: the Design Gate in `product/definition/write-prd` routes here when the PRD leaves experience or structure open.

### Downstream (design feeds)

- `engineering/feature/spec` — reads root `DESIGN.md` (constraints) and `docs/design/prototype.html` (the settled what)
- the configured `product.html#prd` (legacy PRDs remain readable) Part 3 ← proposed state-table amendments, reconciled via `write-prd`
- Testing skills ← component docs carry the accessibility contract

## Skill Boundaries

| Decision type | Owner skill | Artifact |
|---|---|---|
| Where design authority comes from (adopt vs migrate vs scratch) | design-context | DESIGN.md provenance |
| What font/color/radius values are | design-context / design-system-create | DESIGN.md |
| User sees what first | interaction-design | architecture.md, wireframe section |
| Button goes where | interaction-design | locked section layout |
| Click triggers what | interaction-design | state blocks, journey map |
| Loading/empty/error content | interaction-design | state table + state blocks |
| Mobile nav pattern, keyboard nav | interaction-design | responsive-a11y.md |
| Which visual personality wins | visual-design-variants | the styled section |
| Component API, code structure | design-implement | component code + docs |

## Quality Standards

All design skills enforce:

### Accessibility (WCAG AA)
- Text contrast: 4.5:1 for normal, 3:1 for large (≥18pt)
- Touch targets: 44x44px minimum
- Semantic HTML: proper heading hierarchy, landmarks
- Keyboard navigation: focusable elements, visible focus rings (3px outline)
- ARIA: labels for icon-only buttons
- Form labels: explicit `<label for="...">`, not placeholder-only

### Five-State Coverage
- **LOADING**: skeleton UI matching success layout (never a bare spinner)
- **EMPTY**: warm message + primary action
- **ERROR**: specific message + recovery action
- **SUCCESS**: full data display
- **PARTIAL**: mixed state or degraded mode, clearly indicated

### Responsive Design
- Mobile-first breakpoints: 640px, 768px, 1024px, 1280px
- No horizontal scroll; touch-friendly spacing

### Design System Adherence
- Use design tokens literally (no arbitrary values)
- External production engines must reconcile into DESIGN.md tokens — engine-invented values are rejected

## Hard Rules (Enforced)

### Font Blacklist
**Never use**: Papyrus, Comic Sans, Lobster, Impact, Jokerman

### Generic Font Caution
**Requires justification**: Inter, Roboto, Poppins, system-ui

### Color Discipline
- ONE decisive accent color (not three equal-weight)
- Surface colors: 2-3 levels only

### Anti-Patterns (AI Slop)
- Purple gradients on white
- Centered everything
- Decorative blobs
- Three-column grid by default

## Troubleshooting

**"No canonical prototype / no locked sections"** → Run `/interaction-design` first.

**"No design authority found"** → Run `/design-context` (or `/design-system-create` for from-scratch).

**"Section still at wireframe fidelity"** → Run `/visual-design-variants`; its approval gate merges the styled treatment into the section.

**"Visual design changes button positions"** → That's an interaction change — go back to `/interaction-design`, which reopens the section explicitly.

**"State blocks incomplete"** → `/interaction-design` enforces five-state coverage; every section renders all 5 `data-state` blocks.

**"Need different aesthetic"** → Update root `DESIGN.md` first (re-run `/design-context` to re-sync or import, or `/design-system-create` to re-propose), then regenerate visual variants.

**"External skill output doesn't match DESIGN.md tokens"** → The reconciliation contract was violated — regenerate inline (the native fallback) rather than accepting off-system values.

**"Legacy docs/design/system.md still canonical"** → Run `/design-context`; it folds the legacy file into `DESIGN.md` and leaves a pointer.

**"Shipped component diverged from its prototype section"** → Report it. Record the divergence and route design reassessment; reopen only for accepted design changes.

**"PRD Part 3 out of sync with state table"** → `/interaction-design` identifies affected capability records; `write-prd` reconciles authorized state changes.

**"A design question can't be settled in conversation"** → Route to `prototype`: throwaway variants, decision recorded in `prototypes/<slug>/decision.md`, control returns to the skill that raised it. Its outputs never merge into the canonical prototype directly.
