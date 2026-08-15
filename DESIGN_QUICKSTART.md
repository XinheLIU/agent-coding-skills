# Design Workflow Quick Start

Last updated: 2026-08-10

## 30-Second Overview

**Three skills, clear handoffs:**

```
/interaction-design → wireframes + state table
/visual-design-variants → approved.html  
/design-implement → production code
```

## When to Use Each Skill

### `/interaction-design` — Start Here

Use when:
- Starting a new feature
- User flows unclear
- Don't know what states to show (loading/empty/error)

**Output:** Low-fi wireframes (gray boxes), state table (5 states × N features)

**Time:** 30-45 min

---

### `/visual-design-variants` — After Interaction Approved

Use when:
- Wireframes exist and approved
- Need to see visual options
- Want to explore colors/fonts/styling

**Requires:** Wireframes from `/interaction-design`

**Output:** 3 visual variants, user picks one

**Time:** 15-30 min

---

### `/design-implement` — Final Step

Use when:
- Visual design approved
- Ready for production code

**Requires:** Approved visual + state table

**Output:** Component code + docs

**Time:** 20-30 min

## First-Time Setup

### Optional: Create Design System

```bash
/design-system-create
```

Defines typography, colors, spacing. Run once per project.

**Output:** `docs/design/system.md`

**Time:** 15-20 min

## Example Session

```bash
# 1. Define user flows and states
/interaction-design

# You'll be asked:
# - Who are the users? What are they doing?
# - Key features to design?
# - Edge cases you're worried about?

# Skill generates:
# - Wireframes (.scratch/.../interaction/wireframes/*.html)
# - State table with 5 states per feature
# - User journey map

# 2. Explore visual directions
/visual-design-variants

# Skill automatically:
# - Reads your wireframes
# - Generates 3 visual variants (same structure, different visuals)
# - Opens in browser for comparison

# You pick one variant

# 3. Generate production code
/design-implement

# Skill automatically:
# - Converts approved visual to React/Vue/HTML code
# - Implements all 5 states from state table
# - Writes component docs
```

## Key Rules

### Five States Are Mandatory

Every feature MUST define:
- **LOADING** — Skeleton UI
- **EMPTY** — Warm empty state with action
- **ERROR** — Specific error + recovery
- **SUCCESS** — Full data display
- **PARTIAL** — Degraded or incomplete data

**Why:** These states get forgotten. Making them mandatory prevents "No data" shipped as empty state.

### Structure Locks After Interaction Design

Once wireframes approved:
- Button positions LOCKED
- Navigation hierarchy LOCKED
- User flows LOCKED

Visual design can only change:
- Colors
- Fonts
- Spacing
- Shadows/borders

**Why:** Separating structure from style makes iteration faster.

## Common Patterns

### Pattern 1: Full Flow (New Feature)

```
/interaction-design → /visual-design-variants → /design-implement
```

**Time:** ~1.5 hours total

### Pattern 2: Visual Tweak Only

```
/visual-design-variants (reads existing wireframes) → /design-implement
```

**Time:** ~45 min

### Pattern 3: Interaction Needs Fix

```
/interaction-design (revise) → /visual-design-variants (regenerate) → /design-implement
```

**Time:** ~1 hour

## What Gets Created

### Working Layer (`.scratch/<effort>/`)

**Not git-tracked, disposable after implementation:**

```
.scratch/20261010-143022-feature-name/
  interaction/
    wireframes/
      main-screen.html
      flow-screen-2.html
    state-table.md          ← CORE: 5 states × N features
    journey-map.md
    decisions.md
    responsive-a11y.md
  visual/
    variants/
      variant-a.html
      variant-b.html
      variant-c.html
    approved.html           ← CORE: chosen visual
    decision.md
```

### Human Layer (`docs/design/`)

**Git-tracked, permanent documentation:**

```
docs/
  design/
    system.md              ← Design system (if created)
    components/
      feature-name.md      ← Component docs from /design-implement
```

### Project Source

**Git-tracked, production code:**

```
src/components/FeatureName.tsx   ← From /design-implement
```

## PRD Integration

**PRD Part 3 (Five-State Blocks) ↔ Interaction State Table**

If your PRD has Part 3:
- `/interaction-design` reads it as seed
- Fills gaps
- Offers to write back (syncs PRD ← state table)

**Why:** Single source of truth for state definitions.

## Troubleshooting

**"No wireframes found"**
→ Run `/interaction-design` first

**"No design system found"**
→ Optional. Create with `/design-system-create` or skill will use defaults

**"Visual design changed button positions"**
→ That's a bug — visual design CANNOT change structure. Report it.

**"Missing states in state table"**
→ `/interaction-design` enforces all 5 states. Check the generated state-table.md

**"Need different aesthetic"**
→ Run `/visual-design-variants` again with new direction, or update design system

## Tips

1. **Don't skip interaction design** — even if you "know what it looks like," defining states upfront saves debugging later

2. **Wireframes are intentionally ugly** — gray boxes force focus on structure, not colors

3. **Empty states need love** — "No items" is lazy. Explain why empty + offer primary action

4. **Error states need recovery** — "Something went wrong" is useless. Say what happened + how to fix

5. **Partial states are real** — APIs return partial data. Plan for it.

## What Makes This Different

### vs. Traditional Design Tools

- **State-first:** Forces you to think about loading/empty/error upfront
- **Interaction-visual split:** Can iterate visuals without redoing flows
- **Code generation:** Approved design → production code automatically

### vs. Old design-explore-variants

- **Before:** Structure + visuals changed together
- **After:** Structure locked first, then explore visuals
- **Result:** Faster iteration, fewer surprises

## Quick Reference

| Want to... | Run... | Needs... |
|-----------|--------|----------|
| Define user flows | `/interaction-design` | PRD (optional) |
| See visual options | `/visual-design-variants` | Wireframes |
| Get production code | `/design-implement` | Approved visual + state table |
| Create design system | `/design-system-create` | Product context |

## Full Documentation

- **Architecture:** `DESIGN_SEPARATION_PROPOSAL.md`
- **Implementation:** `DESIGN_SEPARATION_COMPLETE.md`
- **Workflow details:** `system/workflows/design.md`

## Ready to Start?

```bash
/interaction-design
```

That's it. The skill will guide you through the rest.
