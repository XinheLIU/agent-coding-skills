# Design Workflow

Last updated: 2026-08-10

This workflow transforms design ideas into implemented components through **interaction design → visual design → implementation**, separating user flows from visual aesthetics.

## Overview

```
User idea → interaction design → visual design → implement code → shipped component
            (user flows, states)  (visual polish)  (production)
            ↓                      ↓                ↓
            Working layer          Working layer    Project + Human docs
```

**Key principle:** Interaction structure (what/where/when) is designed before visual treatment (colors/fonts/polish).

## The Four Skills

### 0. `/design-system-create` — Foundation (Optional but Recommended)

**Purpose**: Establish the canonical design system (typography, colors, spacing).

**When**: Starting a project, no design system exists, or needs formalization.

**Process**:
- Gathers product context (persona, platform from PRD Part 1)
- Proposes typography, color palette, spacing, layout principles
- Validates accessibility (WCAG AA contrast)
- Writes `docs/design/system.md` (Human layer, git-tracked)

**Outputs**:
- `docs/design/system.md` — canonical design system

**Handoff**: Design system feeds both interaction and visual design.

---

### 1. `/interaction-design` — User Flows & States (CORE)

**Purpose**: Define HOW users interact before HOW it looks. Structure over style.

**When**: Starting a new feature, unclear user flows, before any visual work.

**Process**:
- Reads PRD Part 1 (user context) and Part 3 (five-state blocks if exists)
- Designs information architecture (what user sees first/second/third)
- Fills **interaction state table** (LOADING/EMPTY/ERROR/SUCCESS/PARTIAL for every feature)
- Maps user journey with emotional arc
- Generates **low-fidelity wireframes** (gray boxes, no colors/fonts)
- Documents responsive and accessibility requirements
- Identifies unresolved interaction decisions

**Outputs** (Working layer):
- `.scratch/<effort>/interaction/wireframes/*.html` — structure baseline
- `.scratch/<effort>/interaction/state-table.md` — five-state coverage (CORE)
- `.scratch/<effort>/interaction/journey-map.md` — user journey
- `.scratch/<effort>/interaction/decisions.md` — interaction rationale
- `.scratch/<effort>/interaction/responsive-a11y.md` — specs

**Critical constraint**: Wireframes have NO visual styling — only structure.

**Handoff**: Wireframes + state table feed visual design. Structure is locked after approval.

---

### 2. `/visual-design-variants` — Visual Exploration

**Purpose**: Explore visual directions (colors, typography, visual weight) on the locked interaction structure.

**When**: After interaction design approved, design system exists.

**Process**:
- **Requires wireframes** from `/interaction-design` (MANDATORY)
- Reads design system tokens
- Generates 3 visual variants with **SAME structure, DIFFERENT visuals**:
  - Different color saturation
  - Different font personalities
  - Different visual weight distribution
  - Different decorative elements
- Collects feedback, iterates
- Writes approved visual design

**Outputs** (Working layer):
- `.scratch/<effort>/visual/variants/*.html` — 3 visual options
- `.scratch/<effort>/visual/approved.html` — selected design (CORE)
- `.scratch/<effort>/visual/decision.md` — visual rationale

**Critical constraint**: CANNOT change button positions, navigation hierarchy, or state transitions. Only visual properties vary.

**Handoff**: Approved visual design feeds implementation.

---

### 3. `/design-implement` — Production Code

**Purpose**: Convert approved visual design into production code matching tech stack.

**When**: Visual design approved, ready to build components.

**Process**:
- Reads approved.html + state-table.md + design system
- Detects tech stack (React/Vue/Svelte/HTML, CSS approach)
- Generates semantic, accessible, responsive code
- **Implements all 5 states** from state table
- Documents component

**Outputs**:
- Component code in project source directory (project-tracked)
- `docs/design/components/<name>.md` — component docs (Human layer)

**Handoff**: Component ready for use.

## Memory Layers

| Artifact | Layer | Tracked | Lifetime | Why |
|----------|-------|---------|----------|-----|
| `docs/design/system.md` | Human | Yes | Project | Design system outlives features |
| `docs/design/components/*.md` | Human | Yes | Project | Component docs are reference |
| `.scratch/<effort>/interaction/*` | Working | No | Effort | Exploration, disposable after implementation |
| `.scratch/<effort>/visual/*` | Working | No | Effort | Exploration, disposable after implementation |
| Component source code | Project | Per project | Project | Production code |

**Promotion path**: 
- PRD Part 3 ← state-table.md (optional, if user approves sync)
- Component docs (Human layer) ← implementation
- Production code ← approved visual design

## Workflow Patterns

### Pattern 1: Complete Flow (New Feature)

Starting with unclear flows and no visual work done.

```
1. /design-system-create (if no system exists)
   → Output: docs/design/system.md

2. /interaction-design
   → Input: PRD Part 1 + Part 3
   → Output: wireframes + state-table.md
   → Decision gate: user approves interaction structure

3. /visual-design-variants  
   → Input: wireframes (REQUIRED) + state-table.md + system.md
   → Output: approved.html
   → Decision gate: user approves visual direction

4. /design-implement
   → Input: approved.html + state-table.md + system.md
   → Output: Component code + docs/design/components/<name>.md
```

**Time**: ~1-2 hours (interaction takes longest, visual and implementation faster)

### Pattern 2: Visual Iteration Only

Interaction structure is correct, just need different visual treatment.

```
1. /visual-design-variants (reads existing wireframes)
   → Input: wireframes (already exist) + system.md
   → Output: new approved.html

2. /design-implement
   → Output: New component code
```

**Time**: ~30 minutes

### Pattern 3: Interaction Revision

Visual is wrong because interaction structure needs changes.

```
1. /interaction-design (revise existing)
   → Update wireframes and state-table.md
   → Decision gate: user approves new structure

2. /visual-design-variants (regenerate on new structure)
   → Generate new variants on revised wireframes

3. /design-implement
```

**Time**: ~1 hour

### Pattern 4: Quick Implementation (Design Already Approved)

HTML mockup provided, just need production code.

```
1. Place HTML in .scratch/<effort>/visual/approved.html
2. Create state-table.md manually or extract from mockup
3. /design-implement
```

**Time**: <30 minutes

## Key Differentiators from Previous Version

### What Changed

**Before:**
- `design-explore-variants` generated layouts + visuals together
- No explicit interaction design phase
- State coverage optional, often skipped
- Structure and visuals changed simultaneously

**After:**
- **Interaction design first** — wireframes with NO visual styling
- **Five-state table MANDATORY** — every feature × 5 states
- **Visual design locked to structure** — can't move buttons/nav
- **Clear handoff** — interaction → visual → implementation

### Why This Matters

1. **Can reuse interaction** — same wireframe, multiple visual explorations
2. **State coverage enforced** — loading/empty/error never forgotten
3. **Faster iteration** — visual tweaks don't require rethinking flows
4. **Clearer responsibilities** — interaction designer ≠ visual designer
5. **PRD integration** — Part 3 (five-state blocks) ↔ state-table.md sync

## Integration Points

### Upstream (Design reads from)

**Product definition:**
- `docs/product/<slug>/prd.md` Part 1 (persona, platform, product type)
- `docs/product/<slug>/prd.md` Part 3 (five-state blocks — optional seed)

**Project constraints:**
- `CONTEXT.md` (design principles or constraints if any)

**Task context:**
- `.scratch/<effort>/state.md` (what feature is being built)

### Downstream (Design feeds)

**Implementation:**
- `frontend-design` skill (reads design system and component docs)
- `spec` skill Part 3 (references design system for component specs)

**Product:**
- PRD Part 3 ← state-table.md (optional promotion if user approves)

**Testing:**
- `test-component` skill (accessibility and visual regression tests)

## Skill Boundaries

| Decision Type | Skill | Artifact |
|--------------|-------|----------|
| User sees what first | interaction-design | architecture.md, wireframe |
| Button goes where | interaction-design | wireframe layout |
| Click triggers what | interaction-design | state table, journey map |
| Loading shows what | interaction-design | state table (LOADING column) |
| Empty state warmth | interaction-design | state table (EMPTY column) |
| Error feedback location | interaction-design | state table (ERROR column) |
| Mobile nav collapses how | interaction-design | responsive-a11y.md |
| Keyboard navigation | interaction-design | responsive-a11y.md |
| What color to use | visual-design-variants | approved.html |
| What font to use | design-system-create | system.md |
| Border radius size | visual-design-variants | approved.html |
| Shadow depth | visual-design-variants | approved.html |
| Button visual style | visual-design-variants | approved.html (structure locked) |

## Quality Standards

All design skills enforce:

### Accessibility (WCAG AA)
- Text contrast: 4.5:1 for normal, 3:1 for large (≥18pt)
- Touch targets: 44x44px minimum
- Semantic HTML: proper heading hierarchy, landmarks
- Keyboard navigation: focusable elements, visible focus rings
- ARIA: labels for icon-only buttons
- Form labels: explicit `<label for="...">`, not placeholder-only

### Five-State Coverage
- **LOADING**: Skeleton UI matching success layout
- **EMPTY**: Warm message + primary action (not just "No data")
- **ERROR**: Specific message + recovery action
- **SUCCESS**: Full data display
- **PARTIAL**: Mixed state or degraded mode

### Responsive Design
- Mobile-first breakpoints: 640px, 768px, 1024px, 1280px
- No horizontal scroll
- Touch-friendly spacing

### Design System Adherence
- Use design tokens literally (no arbitrary values)
- Follow component foundations

## Hard Rules (Enforced)

From G-Stack's proven standards:

### Font Blacklist
**Never use**: Papyrus, Comic Sans, Lobster, Impact, Jokerman

### Generic Font Caution
**Requires justification**: Inter, Roboto, Poppins, system-ui

### Color Discipline
- ONE decisive accent color (not three equal-weight)
- Surface colors: 2-3 levels only (not long tonal ramp)

### Anti-Patterns (AI Slop)
- Purple gradients on white
- Centered everything
- Decorative blobs
- Three-column grid by default

## Relationship to ui-ux-pro-max

The existing `ui-ux-pro-max` skill is a **knowledge base** queried during design:

**What it provides:**
- 67 styles catalog
- 96 color palettes by product type
- 57 font pairings
- 99 UX guidelines (8 priority tiers)
- 25 chart types
- Stack-specific guidance (13 frameworks)

**How new skills use it:**

1. **interaction-design** queries for:
   - UX guidelines (state design, flow patterns)
   - Chart types (data visualization interactions)

2. **design-system-create** queries for:
   - Font pairings
   - Color palettes by product type
   - Style directions

3. **design-implement** enforces:
   - Priority 1-4 rules (accessibility, touch, performance)
   - Pre-delivery checklist

**Search interface:**
```bash
python3 system/skills-src/design/ux/ui-ux-pro-max/scripts/search.py [domain] --query "[terms]"
```

## Comparison to G-Stack

### Preserved
- ✓ Consultative approach (not form wizards)
- ✓ Multi-variant exploration with feedback loop
- ✓ Clear handoffs between phases
- ✓ Accessibility-first (WCAG gates)
- ✓ Five-state coverage (loading/empty/error/success/partial)
- ✓ Design hard rules (font blacklist, contrast, touch targets)

### Adapted
- ✓ **Interaction ↔ Visual separation** (G-Stack's `plan-design-review` split)
- ✓ **Mandatory state table** (G-Stack's Pass 2)
- ✓ **User journey mapping** (G-Stack's Pass 3)
- ✓ **Wireframe-first** (G-Stack's office-hours wireframe pattern)

### Simplified
- No taste-profile.json (cross-session memory)
- No browse/design binaries (standard tools only)
- No Pretext-native layout
- No 10-category design review (basic quality in implement)
- Three-phase flow instead of four separate skills

**Result**: G-Stack's interaction-first methodology + simpler tooling + memory-protocol aligned.

## Troubleshooting

**"No wireframes found"**
→ Run `/interaction-design` first to define user flows and structure

**"No design system found"**
→ Run `/design-system-create` first to establish typography, colors, spacing

**"No approved visual design found"**
→ Run `/visual-design-variants` after interaction design is approved

**"Visual design changes button positions"**
→ That's an interaction change — go back to `/interaction-design` to revise structure

**"State table incomplete"**
→ `/interaction-design` enforces five-state coverage — every feature must define all 5 states

**"Need different aesthetic"**
→ Update system.md first (re-run `/design-system-create`), then regenerate visual variants

**"PRD Part 3 out of sync with state table"**
→ `/interaction-design` offers to sync — run it in update mode or manually copy states

## Examples

See test projects in `.scratch/design-workflow-tests/` (if created) for worked examples.

---

**Key workflow summary:**
1. Define flows (interaction-design) → wireframes + state table
2. Explore visuals (visual-design-variants) → approved.html
3. Implement (design-implement) → production code + docs

### 1. `/design-system-create` — Foundation

**Purpose**: Establish the canonical design system that grounds all visual work.

**When**: Starting a project, no design system exists, or existing system needs formalization.

**Process**:
- Gathers product context (persona, platform from PRD Part 1)
- Proposes typography, color palette, spacing, layout principles
- Validates accessibility (WCAG AA contrast)
- Generates preview HTML for approval
- Writes `docs/design/system.md` (Human layer, git-tracked)

**Outputs**:
- `docs/design/system.md` — canonical design system
- `.scratch/design-system/system-preview.html` — approval preview (disposable)

**Handoff**: Design system feeds both variant exploration and implementation.

### 2. `/design-explore-variants` — Options

**Purpose**: Generate multiple design directions, collect feedback, iterate to approval.

**When**: Design system exists, specific feature/page needs layout, want to see options.

**Process**:
- Reads design system tokens (typography, colors, spacing)
- Generates 3 variants with different layout approaches:
  - Balanced: standard hierarchy, even emphasis
  - Focal: one element dominates
  - Dense: information-rich, compact
- Collects structured feedback via AskUserQuestion
- Iterates based on adjustments (max 3 rounds)
- Writes approved design and decision rationale

**Outputs**:
- `.scratch/<effort>/designs/approved.html` — selected design (Working layer)
- `.scratch/<effort>/designs/decision.md` — why this was chosen (Working layer)
- `.scratch/<effort>/designs/variants/*.html` — exploration history (Working layer)

**Handoff**: Approved design feeds implementation.

### 3. `/design-implement` — Production Code

**Purpose**: Convert approved design into production code matching the project's tech stack.

**When**: Design approved, ready to build real components.

**Process**:
- Reads approved.html and design system
- Detects tech stack (React/Vue/Svelte/HTML, CSS approach)
- Extracts design tokens into stack-appropriate format
- Generates semantic, accessible, responsive component code
- Creates usage example
- Documents component with API, accessibility notes, design mappings

**Outputs**:
- Component code in project source directory (project-tracked)
- Design tokens file if needed (styles/tokens.css or equivalent)
- `docs/design/components/<name>.md` — component docs (Human layer, git-tracked)

**Handoff**: Component ready for use, docs feed spec and frontend-design skills.

## Memory Layers

The design workflow follows the durability test: *if the work root were deleted, would the project lose a fact it still needs?*

| Artifact | Layer | Tracked | Lifetime | Why |
|----------|-------|---------|----------|-----|
| `docs/design/system.md` | Human | Yes | Project | Design system outlives any single feature |
| `docs/design/components/*.md` | Human | Yes | Project | Component docs are reference material |
| `.scratch/<effort>/designs/approved.html` | Working | No | Effort | Scaffolding; real code supersedes it |
| `.scratch/<effort>/designs/variants/*.html` | Working | No | Effort | Exploration history, disposable after selection |
| `.scratch/<effort>/designs/decision.md` | Working | No | Effort | Decision context, disposable after implementation |
| Component source code | Project | Per project | Project | Production code, tracked by project rules |

**Promotion path**: Exploration (Working) → Approved design (Working) → Implemented code (Project source) + Docs (Human layer)

## Workflow Patterns

### Pattern 1: New Project Design

Starting from scratch with no design work done yet.

```
1. /design-system-create
   → Input: PRD Part 1, user preferences
   → Output: docs/design/system.md

2. /design-explore-variants  
   → Input: docs/design/system.md, feature description
   → Output: .scratch/<effort>/designs/approved.html

3. /design-implement
   → Input: approved.html, system.md
   → Output: Component code + docs/design/components/<name>.md
```

**Time**: ~1-2 sessions (system creation takes longest, variants and implementation are faster)

### Pattern 2: Existing Design System

Design system already exists, just need to design and implement a new feature.

```
1. /design-explore-variants (skip design-system-create)
   → Input: docs/design/system.md (existing), feature description
   → Output: .scratch/<effort>/designs/approved.html

2. /design-implement
   → Input: approved.html, system.md
   → Output: Component code + docs/design/components/<name>.md
```

**Time**: ~1 session

### Pattern 3: Quick Implementation

Design already approved (HTML mockup provided), just need production code.

```
1. Place approved design in .scratch/<effort>/designs/approved.html manually

2. /design-implement (skip exploration)
   → Input: approved.html, system.md
   → Output: Component code + docs/design/components/<name>.md
```

**Time**: <1 hour

### Pattern 4: System Update

Existing design system needs updates (new components, token changes).

```
1. /design-system-create with update flag
   → Input: existing docs/design/system.md, requested changes
   → Output: updated docs/design/system.md

2. Update affected components if token changes impact them
```

**Time**: Varies by scope

## Integration Points

### Upstream (Design reads from)

**Product definition:**
- `docs/product/<slug>/prd.md` Part 1 (persona, platform, product type)
- Informs aesthetic direction, platform constraints, user needs

**Project constraints:**
- `CONTEXT.md` (design principles or constraints if any)
- Binding rules that design must respect

**Task context:**
- `.scratch/<effort>/state.md` (what feature is being built)
- Guides variant generation focus

### Downstream (Design feeds)

**Implementation:**
- `frontend-design` skill (reads design system and component docs)
- `spec` skill Part 3 (references design system for component specs)

**Testing:**
- `test-component` skill (accessibility and visual regression tests)

**Reference:**
- All visual work refers to `docs/design/system.md` as source of truth

## Quality Standards

All design skills enforce these standards:

### Accessibility (WCAG AA)
- Text contrast: 4.5:1 for normal text, 3:1 for large text (≥18pt)
- Touch targets: 44x44px minimum on mobile
- Semantic HTML: proper heading hierarchy, landmarks, labels
- Keyboard navigation: focusable elements, visible focus rings (3px outline)
- ARIA: labels for icon-only buttons, descriptions where needed
- Form labels: explicit `<label for="...">`, not placeholder-only

### Responsive Design
- Mobile-first breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)
- Flexible layouts: flex/grid with relative units
- No horizontal scroll on any screen size
- Touch-friendly on mobile (spacing, target sizes)

### Design System Adherence
- Use design tokens literally (no arbitrary colors/spacing)
- Follow component foundations from system.md
- Respect established patterns

### Code Quality
- Semantic markup (header, nav, main, section, article, footer)
- Match tech stack conventions (file naming, folder structure)
- Self-documenting component APIs
- Sensible defaults for optional props

## Hard Rules (Enforced)

These are non-negotiable gates from G-Stack's proven design standards:

### Font Blacklist
**Never use**: Papyrus, Comic Sans, Lobster, Impact, Jokerman

These fonts signal unprofessional design and are rejected automatically.

### Generic Font Caution
**Requires justification**: Inter, Roboto, Poppins, system-ui

These are overused. If proposing one of these, must state why it's the right choice for this specific product (e.g., "system-ui for internal tool performance" is valid; "Inter because it's popular" is not).

### Color Discipline
- ONE decisive accent color (not three equal-weight brand colors)
- Surface colors: 2-3 levels only (page, raised, overlay) — not a long tonal ramp
- All text/background pairs validated before writing system.md

### Anti-Patterns (AI Slop)
Avoid generic AI design patterns:
- Purple gradients on white background
- Centered everything with no hierarchy
- Decorative geometric blobs
- Three-column grid by default
- Stock "hero with form on right" layout (unless genuinely appropriate)

## Skill Discovery

Skills are symlinked for flat discovery:

```bash
# From system/skills/ (flat discovery layer)
ls -la skills/ | grep design
lrwxr-xr-x  design-system-create -> ../skills-src/design/ux/design-system-create
lrwxr-xr-x  design-explore-variants -> ../skills-src/design/ux/design-explore-variants
lrwxr-xr-x  design-implement -> ../skills-src/design/ux/design-implement
```

Invoke with:
- `/agent-coding-skills:design-system-create`
- `/agent-coding-skills:design-explore-variants`
- `/agent-coding-skills:design-implement`

Or use short names if skill discovery is configured.

## Relationship to ui-ux-pro-max

The existing `ui-ux-pro-max` skill becomes a **reference resource** rather than a workflow skill:

**What ui-ux-pro-max provides:**
- 67 styles catalog (glassmorphism, brutalism, minimalism, etc.)
- 96 color palettes by product type
- 57 font pairings with personality matching
- 99 UX guidelines in 8 priority categories
- 25 chart types with library recommendations
- Stack-specific guidance (13 frameworks)

**How the new skills use it:**

1. **design-system-create** queries it for:
   - Font pairing recommendations (typography search)
   - Color palette suggestions (color search by product type)
   - Style direction (style search by category)

2. **design-implement** enforces its:
   - Priority 1-4 rules (accessibility, touch, performance, layout)
   - Pre-delivery checklist (no emoji icons, cursor-pointer, contrast)

3. **All skills** follow its:
   - WCAG AA standards
   - Touch target minimums
   - Responsive breakpoints

**Search interface:**
```bash
python3 system/skills-src/design/ux/ui-ux-pro-max/scripts/search.py [domain] --query "[terms]"
```

Domains: product, style, typography, color, landing, chart, ux, react, web

## Comparison to G-Stack

What we preserved:
- ✓ Consultative design system creation (not a form wizard)
- ✓ Multi-variant exploration with feedback loop
- ✓ Clear handoff: system → variants → implementation
- ✓ Accessibility-first (WCAG gates, semantic HTML)
- ✓ Design hard rules (font blacklist, contrast, touch targets)
- ✓ Durability principle (system outlives effort, exploration doesn't)

What we simplified:
- No taste-profile.json (cross-session preference memory)
- No browse/design binaries (works with standard tools only)
- No Pretext-native layout (standard CSS is simpler)
- No 10-category design review (basic quality in design-implement)
- No GStack-specific telemetry/routing
- Three skills instead of four (consultation + shotgun combined concept)

**Result**: Same workflow clarity, simpler tooling, memory-protocol aligned.

## Troubleshooting

**"No design system found"**
→ Run `/design-system-create` first to establish typography, colors, spacing

**"No approved design found"**
→ Run `/design-explore-variants` to generate and select a design

**"Component already exists"**
→ Choose different name or explicitly state you want to overwrite

**"Can't detect tech stack"**
→ Manually specify stack in design-implement (e.g., "React with Tailwind")

**"Design doesn't match system"**
→ Variants should use system tokens; if they don't, that's a bug — report it

**"Need different aesthetic"**
→ Update system.md first (re-run design-system-create with update flag), then regenerate variants

## Examples

See test projects in `.scratch/design-workflow-tests/` (if created) for worked examples.
