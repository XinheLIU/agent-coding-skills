# Design Workflow

Last updated: 2026-08-17

This workflow transforms product intent into implemented components through **design context → interaction design → visual design → implementation**. The pipeline skills stay thin — routing, approval gates, and artifact conventions — and dispatch heavy design work to installed external skills from the six-layer catalog (`skills-src/design/ux/README.md`).

## Overview

```
PRD Part 1/3 → design context → interaction design → visual design → implement code → shipped component
               (⑤ tokens)        (③ flows, states)    (①③⑥ visuals)   (⑥+③ production)
               ↓                  ↓                     ↓                 ↓
               Human layer        Working layer         Working layer     Project + Human docs
```

**Key principles:**

1. **Interaction before visuals** — structure (what/where/when) is designed and locked before color/typography/polish.
2. **One canonical token source** — `docs/design/system.md` is the only file downstream skills read for visual values; `/design-context` decides what feeds it.
3. **External skills carry heavy work** — each stage checks the catalog for an installed capability (taste, knowledge, method, templates, DESIGN.md, production) and dispatches; the native workflow is always the fallback.

## The Five Skills

### 0. `/design-context` — Token Source (ENTRY POINT)

**Purpose**: Decide where design tokens come from and produce the canonical `docs/design/system.md`.

**When**: Starting design work; a `DESIGN.md` exists but nothing consumes it; you have a reference site/brand to import.

**Process**:
- Detects `DESIGN.md` (root), existing `docs/design/system.md`, PRD Part 1
- Branches: adopt existing DESIGN.md → extract from a reference site (⑤ extractors) → adopt a ready-made brand spec (④ catalogs) → or hand off to `/design-system-create` for from-scratch creation
- Resolves token authority conflicts (default: DESIGN.md wins visual values; system.md keeps component foundations)
- Writes `docs/design/system.md` after approval

**Outputs**: `docs/design/system.md` (Human layer, git-tracked)

**External dispatch**: layers ⑤ (DESIGN.md lifecycle + extractors) and ④ (template catalogs). Never modifies `DESIGN.md` at root — that's an input, owned by external lifecycle tools.

---

### 0b. `/design-system-create` — From-Scratch Fallback

**Purpose**: Consultatively create `docs/design/system.md` when there is no DESIGN.md and no reference to import.

**When**: Called directly, or via `/design-context` Step 3 when the user picks the native path.

**Process**: gathers product context (PRD Part 1) → proposes typography/color/spacing/layout with rationale → optional layer-② knowledge lookup for font pairings and palettes → preview HTML → approval → writes `docs/design/system.md`.

**Outputs**: `docs/design/system.md` (Human layer); `.scratch/design-system/system-preview.html` (Working, disposable)

---

### 1. `/interaction-design` — User Flows & States (CORE)

**Purpose**: Define HOW users interact before HOW it looks. Structure over style.

**When**: New feature with unclear flows; PRD Part 3 five-state blocks are thin.

**Process**:
- Reads PRD Part 1 (`docs/product/<slug>/prd.md`) and Part 3
- Designs information architecture (what the user sees first/second/third)
- Fills the **interaction state table** — LOADING/EMPTY/ERROR/SUCCESS/PARTIAL for every feature (mandatory, no gaps)
- Maps user journeys with emotional arc
- Generates **low-fidelity wireframes** (gray boxes, NO colors/fonts)
- Documents responsive + accessibility requirements; surfaces unresolved decisions

**Outputs** (Working layer): `.scratch/<effort>/interaction/{wireframes/,state-table.md,journey-map.md,decisions.md,responsive-a11y.md}`

**Critical constraint**: Wireframes have no visual styling — only structure. Structure locks at approval.

**External dispatch**: optional layer-② knowledge pass for state-design and flow-pattern guidelines, cited in `decisions.md`. The five-state table itself is always native.

---

### 2. `/visual-design-variants` — Visual Exploration

**Purpose**: Explore visual directions on the locked interaction structure.

**When**: After interaction design is approved and `docs/design/system.md` exists.

**Process**:
- **Requires** `interaction/wireframes/`, `interaction/state-table.md`, and `docs/design/system.md` (hard prerequisites)
- Defines 3 genuinely different visual directions (anti-convergence rule)
- Generates 3 variant HTMLs — same structure, different visual treatment — each showing all 5 states with a state switcher
- Iterates (max 3 rounds) to an approved variant

**Outputs** (Working layer): `.scratch/<effort>/visual/{variants/variant-{a,b,c}.html,approved.html,decision.md,constraints.md}`

**Critical constraint**: CANNOT change button positions, navigation hierarchy, or state transitions — only visual properties vary.

**External dispatch**: layer-① taste skills sharpen direction strategies; layer-⑥ production engines may render the variant HTMLs. Reconciliation contract: locked structure preserved, system.md tokens only, output lands at `visual/variants/variant-{a,b,c}.html` with the state switcher intact.

---

### 3. `/design-implement` — Production Code

**Purpose**: Convert the approved visual design into production code matching the project's tech stack.

**When**: `visual/approved.html` exists and the user is ready to build.

**Process**:
- Reads `visual/approved.html` + `interaction/state-table.md` + `docs/design/system.md`
- Detects tech stack (React/Vue/Svelte/HTML × Tailwind/CSS-in-JS/…)
- Extracts design tokens into stack-appropriate format
- Generates semantic, accessible, responsive component code implementing **all 5 states**
- Documents the component

**Outputs**: component code in project source (project-tracked); `docs/design/components/<name>.md` (Human layer)

**External dispatch**: optional layer-③ polish pass (interaction craft, motion, feel-better, a11y review) over generated code — within token authority; structural changes route back to `/interaction-design`. Applied fixes are recorded in the component doc.

## External Orchestration

The six-layer model (full catalog: `skills-src/design/ux/README.md`) maps to pipeline stages:

| Layer | What it provides | Consumed by | When absent |
|:---:|---|---|---|
| ① Taste / Judgment | Aesthetic direction, anti-slop stance | `visual-design-variants` Step 2.5 | Directions proposed inline |
| ② Design Knowledge | Font/palette/guideline databases | `design-system-create` Steps 2.2–2.3, `interaction-design` Step 1.5 | Proposed from first principles |
| ③ Method / Workflow | Design workflows, polish, motion, redesign | `design-implement` Step 4.5 (polish); redesign tools run before re-entering the pipeline | Built-in quality gates |
| ④ Templates & References | Ready-made brand specs | `design-context` Step 2 | Create from scratch |
| ⑤ Design Context | DESIGN.md format, extractors, lifecycle | `design-context` Steps 1–3 | Native `design-system-create` path |
| ⑥ Production Environments | High-fidelity mockup/demo engines | `visual-design-variants` Step 2.5 | Inline HTML generation |

Every dispatch follows the same contract: **the pipeline skill owns the artifacts; the external skill is a producer whose output is reconciled into the canonical paths.** Skills name layers and capabilities, never hardcoded vendors — the README catalog is the detailed reference.

## Memory Layers

| Artifact | Layer | Tracked | Lifetime | Why |
|----------|-------|---------|----------|-----|
| `DESIGN.md` (root) | Human (external owner) | Yes | Project | Design context source; written by lifecycle tools, read by pipeline |
| `docs/design/system.md` | Human | Yes | Project | Canonical design system outlives features |
| `docs/design/components/*.md` | Human | Yes | Project | Component docs are reference |
| `.scratch/<effort>/interaction/*` | Working | No | Effort | Exploration, disposable after implementation |
| `.scratch/<effort>/visual/*` | Working | No | Effort | Exploration, disposable after implementation |
| Component source code | Project | Per project | Project | Production code |

**Promotion path**:
- PRD Part 3 ← `state-table.md` (optional, if user approves sync in `/interaction-design`)
- `docs/design/system.md` ← DESIGN.md merge or from-scratch creation
- Component docs (Human layer) ← implementation
- Production code ← approved visual design

## Workflow Patterns

### Pattern 1: Complete Flow (New Feature)

```
1. /design-context              → docs/design/system.md (adopt / extract / create)
2. /interaction-design          → wireframes + state-table.md → APPROVAL GATE
3. /visual-design-variants      → visual/approved.html → APPROVAL GATE
4. /design-implement            → component code + docs/design/components/<name>.md
```

**Time**: ~1-2 hours (interaction takes longest).

### Pattern 2: Visual Iteration Only

Interaction structure is correct; need a different visual treatment.

```
1. /visual-design-variants  (reads existing wireframes + system.md) → new approved.html
2. /design-implement        → new component code
```

**Time**: ~30 minutes.

### Pattern 3: Interaction Revision

Visual is wrong because the structure is wrong.

```
1. /interaction-design (revise)         → updated wireframes + state table → APPROVAL GATE
2. /visual-design-variants (regenerate) → new variants on revised structure
3. /design-implement
```

**Time**: ~1 hour.

### Pattern 4: Quick Implementation (Design Already Approved)

HTML mockup in hand, need production code.

```
1. Place HTML at .scratch/<effort>/visual/approved.html
2. Create interaction/state-table.md manually or extract from the mockup
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
1. /design-context  → extract (⑤) or adopt (④) the brand spec → docs/design/system.md
2-4. as Pattern 1
```

## Integration Points

### Upstream (design reads from)

- `docs/product/<slug>/prd.md` Part 1 (persona, platform, product type) and Part 3 (five-state seed)
- `DESIGN.md` at project root (layer-⑤ design context, when present)
- `CONTEXT.md` (binding design principles or constraints)
- `.scratch/<effort>/state.md` (what feature is being built)

Entry gate: the Design Gate in `product/definition/write-prd` routes here when the PRD leaves experience or structure open.

### Downstream (design feeds)

- `engineering/feature/spec` — reads `docs/design/system.md` and `DESIGN.md` as design constraints
- `docs/product/<slug>/prd.md` Part 3 ← optional state-table sync
- Testing skills ← component docs carry the accessibility contract

## Skill Boundaries

| Decision type | Owner skill | Artifact |
|---|---|---|
| Where tokens come from (DESIGN.md vs scratch) | design-context | system.md provenance |
| What font/color/radius values are | design-context / design-system-create | system.md |
| User sees what first | interaction-design | architecture.md, wireframe |
| Button goes where | interaction-design | wireframe layout |
| Click triggers what | interaction-design | state table, journey map |
| Loading/empty/error content | interaction-design | state table |
| Mobile nav pattern, keyboard nav | interaction-design | responsive-a11y.md |
| Which visual personality wins | visual-design-variants | approved.html |
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
- External production engines must reconcile into system.md tokens — engine-invented values are rejected

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

**"No wireframes found"** → Run `/interaction-design` first.

**"No design system found"** → Run `/design-context` (or `/design-system-create` for from-scratch).

**"No approved visual design found"** → Run `/visual-design-variants` after interaction design is approved; it writes `visual/approved.html`.

**"Visual design changes button positions"** → That's an interaction change — go back to `/interaction-design`.

**"State table incomplete"** → `/interaction-design` enforces five-state coverage; every feature defines all 5 states.

**"Need different aesthetic"** → Update `docs/design/system.md` first (re-run `/design-context` to re-sync from DESIGN.md, or `/design-system-create` to re-propose), then regenerate visual variants.

**"External skill output doesn't match system tokens"** → The reconciliation contract was violated — regenerate inline (the native fallback) rather than accepting off-system values.

**"PRD Part 3 out of sync with state table"** → `/interaction-design` offers to sync — run it in update mode.

**"A design question can't be settled in conversation"** → Route to `prototype`: throwaway variants, decision recorded in `prototypes/<slug>/decision.md`, control returns to the skill that raised it.
