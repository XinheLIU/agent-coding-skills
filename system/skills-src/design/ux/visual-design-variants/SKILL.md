---
name: visual-design-variants
description: "Explore three genuinely different visual directions — color, typography, weight — on interaction structure that is already locked. Requires locked wireframe sections in docs/design/prototype.html plus DESIGN.md; cannot move buttons, navigation, or state transitions. The approved direction merges into the canonical prototype as its styled section. Use to compare visual options or design variants before committing to one."
---

Last updated: 2026-09-09

# Visual Design Variants

Explore **visual directions** (colors, typography, visual weight) on an already-defined **interaction structure**. This skill generates 3 variants that share the same layout but differ in visual treatment.

## Critical Constraint

**This skill CANNOT change interaction structure.** Button positions, navigation hierarchy, state transitions, and user flows are locked in the prototype section by `/interaction-design` (`data-structure="locked"`). Only visual properties vary.

## When to Use

- After `/interaction-design` has locked wireframe sections in `docs/design/prototype.html`
- Design authority exists (`DESIGN.md` at project root)
- User wants to see visual options before committing
- Exploring visual hierarchy without changing interaction structure

Do NOT use when:
- No locked wireframe sections exist yet (run `/interaction-design` first)
- Interaction structure needs changes (go back to `/interaction-design`)
- No design authority exists yet (run `/design-context` or `/design-system-create` first)

## Inputs and Handoffs

**Upstream (REQUIRED):**
- `docs/design/prototype.html` — sections with `data-structure="locked"` at `wireframe` fidelity (structure baseline + all five state blocks)
- `DESIGN.md` at project root (visual tokens; legacy `docs/design/system.md` readable until migrated)

**Upstream (OPTIONAL):**
- `<work-root>/<effort>/interaction/journey-map.md` (emotional intent)
- `<work-root>/<effort>/interaction/state-table.md` (state semantics behind the rendered blocks)

**Downstream:**
- Working exploration in `<work-root>/<effort>/visual/`: `variants/variant-{a,b,c}.html`, `decision.md`, `constraints.md`
- On approval: the winning treatment merges into the surface's section in `docs/design/prototype.html`, `wireframe → styled` (feeds `design-implement`)

## Workflow

### Step 0: Verify Prerequisites

Resolve the product document from explicit user paths, `docs/agents/memory.md`, and active `state.md`. New product memory uses `product.html#prd`; follow its persona, capability, scope, and question links. Legacy `prd.md` remains readable when canonical. Do not pick the first file found across products.

Resolve the work root from the same `docs/agents/memory.md`; with none configured, or no such file, it is `.scratch/`. Then check all required inputs exist:

```bash
WORK_ROOT=<the path resolved above>

# Effort directory for working exploration (create one if none is active)
EFFORT_DIR=$(find "$WORK_ROOT" -maxdepth 1 -type d -name "[0-9]*-*" 2>/dev/null | sort -r | head -1)

# Check the canonical prototype
if [ ! -f docs/design/prototype.html ]; then
  echo "ERROR: No canonical prototype - run /interaction-design first"
  exit 1
fi

# Check design authority
if [ ! -f DESIGN.md ] && [ ! -f docs/design/system.md ]; then
  echo "ERROR: No design authority - run /design-context or /design-system-create first"
  exit 1
fi

echo "Prerequisites verified"
```

Then read the prototype and verify the target surfaces are ready: each section this effort styles must carry `data-structure="locked"`. A section still `open` goes back to `/interaction-design`. Note the in-scope `data-surface` slugs and confirm all five `data-state` blocks are present in each.

If any check fails, **STOP** and report what's missing with the correct skill to run.

### Step 1: Read Interaction Structure

Load the locked sections and understand the locked structure:

```bash
# Read the canonical prototype (locked sections + state blocks)
cat docs/design/prototype.html

# Read design authority
cat DESIGN.md 2>/dev/null || cat docs/design/system.md

# Optional working context from the interaction effort
cat $EFFORT_DIR/interaction/state-table.md 2>/dev/null
```

**Extract and document:**

1. **Structural elements from the locked sections** (these CANNOT change):
   - Header layout (logo position, nav structure, actions)
   - Main content zones (sidebar yes/no, columns, sections)
   - Component placement (where buttons/forms/data appears)
   - Footer structure
   - Mobile layout differences (if specified)

2. **States to visualize** (from the sections' `data-state` blocks):
   - All 5 states × N surfaces = M total states to design
   - Note which states need visual attention (empty/error especially)

3. **Design tokens available** (from `DESIGN.md` frontmatter):
   - Typography: font families, size scale, weights
   - Colors: primary, accent, neutral scale, semantic colors
   - Spacing: base unit, scale
   - Component foundations: buttons, inputs, cards

Write structural constraints to `$EFFORT_DIR/visual/constraints.md`:

```markdown
## Visual Design Constraints

### Locked Structure (from the canonical prototype)

**Cannot change:**
- [List all structural elements - header layout, main zones, component positions]
- [Navigation hierarchy - what's primary/secondary]
- [Button locations - where CTAs appear]
- [Form flow - field order and grouping]

**Can change:**
- Typography: font selection, size adjustments within scale, weight distribution
- Colors: palette choices within system, saturation, contrast levels
- Spacing: tightness/looseness within scale (but not layout structure)
- Visual weight: which elements feel heavier via size/color/boldness
- Decorative elements: shadows, borders, icons, illustrations
- Motion: transitions, animations (respecting structure)

### States to Design

[List from the sections' state blocks]
- Surface A: LOADING, EMPTY, ERROR, SUCCESS, PARTIAL
- Surface B: ...

### Design Tokens (DESIGN.md)

[Extract key tokens]
- Fonts: [list]
- Colors: [list]
- Spacing scale: [list]
```

### Step 2: Define Visual Directions

Create 3 distinct **visual personalities** that fit the interaction structure:

**AskUserQuestion** to understand intent:

> The interaction structure is locked. Now exploring visual directions on top of it.
>
> **What feeling should this interface evoke?**
> (Examples: Trustworthy & professional, Playful & energetic, Calm & focused, Bold & confident)
>
> [Text input expected]

Based on response, propose 3 visual directions:

```markdown
## Visual Direction A — [Personality A]

**Visual strategy:**
- Typography: [font pairing, weight distribution]
- Color saturation: [High/Medium/Low]
- Visual weight: [Which elements feel heaviest]
- Decorative approach: [Minimal shadows / Bold borders / Gradient accents / etc]

**Example adjustments on the locked structure:**
- Primary CTA: [Bold color, large size, heavy weight]
- Secondary content: [Lighter color, smaller size]
- Backgrounds: [Flat / Subtle gradient / Pattern]

---

## Visual Direction B — [Personality B]

[Different strategy...]

---

## Visual Direction C — [Personality C]

[Different strategy...]
```

**Anti-convergence rule:** The 3 directions MUST use different visual strategies. Not just slight color tweaks — genuinely different visual treatments.

**AskUserQuestion** to confirm directions before generating:

> Proposed visual directions:
>
> **A: [Name]** — [1 sentence strategy]  
> **B: [Name]** — [1 sentence strategy]  
> **C: [Name]** — [1 sentence strategy]
>
> **Options:**
> **A)** Generate these 3 variants  
> **B)** Adjust directions — [specify which and how]  
> **C)** Show me the locked structure first

If C, open the prototype section in browser before continuing.

### Step 2.5: External Production (optional)

Read `<work-root>/<effort>/design/capabilities.md`. If it carries `① taste` and `⑥ production` rows, follow their decisions and continue at Step 3.

Otherwise scan the skills available in this session for either:

- **① taste** — a skill that argues for or vetoes a design direction and produces no palette, template, or code as its own artifact. It sharpens the three direction strategies from Step 2; it never chooses among them.
- **⑥ production** — a skill that renders high-fidelity mockups, prototypes, or decks from a brief that is already settled. It decides nothing.

Append one row per slot recording what was found, or `none`. Rows are `| slot | found or none | decision | this skill |`; create the file with that header when absent. With `none` for both, continue at Step 3 — the default path.

With something found, name it and what it would change, then **AskUserQuestion**:

> A [taste / production] capability is available: **[name]** — it would [what it changes, one clause].
>
> **A)** Generate the variants inline per Step 3 (Recommended)
> **B)** Use **[name]**, reconciled into this skill's contract below

Whatever produces them, the output must satisfy this skill's contract:

1. The locked section structure survives intact (Step 1 constraints).
2. Every visual value traces to `DESIGN.md` — no invented colors or fonts.
3. Files land at `$EFFORT_DIR/visual/variants/variant-{a,b,c}.html` with the Step 3 state switcher present. Copy or rename if the tool writes elsewhere.
4. All five states from the locked section appear in each variant.

If the output cannot meet these four, generate inline per Step 3 — the default path.

Done when `capabilities.md` carries `① taste` and `⑥ production` rows and three variants exist at the canonical paths.

### Step 3: Generate Visual Variants

For each direction (A, B, C), generate full HTML that:

1. **Preserves exact structure** from the locked section
2. **Applies visual treatment** per direction strategy
3. **Shows all states** from the section's state blocks
4. **Uses DESIGN.md tokens**

**Generation process per variant:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Visual Variant [A/B/C] — [Feature Name]</title>
<style>
/* Design tokens */
:root {
  /* Extract from DESIGN.md frontmatter */
  --font-display: [from system];
  --font-body: [from system];
  --color-primary: [from system];
  --color-accent: [from system];
  /* etc */
  
  /* Variant-specific visual adjustments */
  --visual-weight-primary: [based on direction];
  --visual-saturation: [based on direction];
  /* etc */
}

/* Base structure from the locked section (LOCKED) */
[Copy exact layout structure from the prototype section]

/* Visual treatment (VARIABLE per direction) */
.primary-cta {
  /* Direction A: bold color, heavy weight */
  /* Direction B: subtle color, large size */
  /* Direction C: gradient background, medium weight */
}

/* State-specific styles */
.state-loading { /* skeleton UI */ }
.state-empty { /* warm empty state */ }
.state-error { /* error display */ }
.state-success { /* full data */ }
.state-partial { /* mixed state */ }
</style>
</head>
<body>

<!-- State: SUCCESS (default view) -->
<div class="state-success">
  [Full implementation preserving the locked structure]
</div>

<!-- State: LOADING -->
<div class="state-loading" style="display:none;">
  [Skeleton UI matching success structure]
</div>

<!-- State: EMPTY -->
<div class="state-empty" style="display:none;">
  [Warm empty state with icon, message, CTA]
</div>

<!-- State: ERROR -->
<div class="state-error" style="display:none;">
  [Error message with recovery action]
</div>

<!-- State: PARTIAL -->
<div class="state-partial" style="display:none;">
  [Partial data + loading indicator]
</div>

<script>
// State switcher for preview
function showState(state) {
  document.querySelectorAll('[class^="state-"]').forEach(el => {
    el.style.display = 'none';
  });
  document.querySelector('.state-' + state).style.display = 'block';
}

// Controls
document.body.insertAdjacentHTML('beforeend', `
  <div style="position:fixed;bottom:20px;right:20px;background:white;padding:10px;border:2px solid #333;border-radius:8px;">
    <strong>State:</strong>
    <button onclick="showState('success')">Success</button>
    <button onclick="showState('loading')">Loading</button>
    <button onclick="showState('empty')">Empty</button>
    <button onclick="showState('error')">Error</button>
    <button onclick="showState('partial')">Partial</button>
  </div>
`);
</script>

</body>
</html>
```

Save to:
- `$EFFORT_DIR/visual/variants/variant-a.html`
- `$EFFORT_DIR/visual/variants/variant-b.html`
- `$EFFORT_DIR/visual/variants/variant-c.html`

### Step 4: Present Side-by-Side Comparison

Open all 3 variants in browser for side-by-side comparison:

```bash
open $EFFORT_DIR/visual/variants/variant-a.html
open $EFFORT_DIR/visual/variants/variant-b.html
open $EFFORT_DIR/visual/variants/variant-c.html
```

**AskUserQuestion** for feedback:

> Visual variants generated. Opening in browser...
>
> **Variant A ([Name]):** [Path]  
> **Variant B ([Name]):** [Path]  
> **Variant C ([Name]):** [Path]
>
> Each variant has state switcher (bottom-right controls) to see all 5 states.
>
> **Feedback:**
> **A)** Approve one variant — [specify A/B/C]  
> **B)** Iterate on one — [specify which + what to change]  
> **C)** Hybrid — [take elements from multiple]  
> **D)** None work — try different visual directions

### Step 5: Iterate or Approve

Based on feedback:

**If A (approve one):**
- Merge the chosen treatment into the surface's section in `docs/design/prototype.html`: apply the winning CSS through the shared `:root` token block plus section-scoped rules, keep the section's markup, markers, and state blocks intact, set `data-fidelity="styled"` and `data-updated`
- Structure markers are untouched — the section stays `locked`
- Document decision (next step)
- Done

**If B (iterate):**
- Read the variant HTML
- Apply requested changes **without changing structure**
- Regenerate that variant
- Return to Step 4 (present again)
- **Max 3 iterations** — if not converging, suggest going back to interaction design

**If C (hybrid):**
- Identify which visual elements from which variants
- Create new variant combining them **while preserving structure**
- Present hybrid for approval
- If approved, merge it as in A

**If D (none work):**
- **AskUserQuestion**: "What's missing visually?" or "What feeling isn't captured?"
- Define 3 NEW visual directions
- Regenerate from Step 3

### Step 6: Document Visual Decision

Once variant approved, write decision rationale:

```markdown
## Visual Design Decision

**Date:** [timestamp]

**Chosen Direction:** Variant [A/B/C] — [Name]

### Why This Direction

**Visual strategy that won:**
- Typography: [what worked]
- Color treatment: [what worked]
- Visual weight distribution: [what worked]
- Emotional resonance: [why this feels right for the product]

### What Was Tried and Rejected

**Variant [X]:** [Why it didn't work]  
**Variant [Y]:** [Why it didn't work]

### Key Visual Decisions

**Decision 1:** [Specific choice, e.g., "Bold color on CTA vs subtle"]  
**Rationale:** [Why this serves user goals better]

**Decision 2:** [...]

### Implementation Notes

**For `/design-implement`:**
- The styled section in the canonical prototype is ready to convert to production code
- All 5 states are defined and approved
- Structure is unchanged (section stayed locked)
- DESIGN.md tokens were followed

**Files:**
- Canonical: `docs/design/prototype.html` — section `[data-surface]` now at styled fidelity
- Source variants: `$EFFORT_DIR/visual/variants/*.html`
```

Write to `$EFFORT_DIR/visual/decision.md`.

### Step 7: Completion Summary

```markdown
## Visual Design — Complete

**Effort:** $EFFORT_DIR

**Artifacts Created:**
- ✅ Visual constraints documented (`visual/constraints.md`)
- ✅ 3 visual variants generated (`visual/variants/`)
- ✅ Approved treatment merged into `docs/design/prototype.html` (section at styled fidelity)
- ✅ Decision rationale (`visual/decision.md`)

**Structure Preservation:**
- ✅ Locked section structure maintained
- ✅ All 5 state blocks styled
- ✅ DESIGN.md tokens applied

**Ready for Next Step:**
The styled section in the canonical prototype is ready for `/design-implement`.
Implementation will convert it to production code.

**Files to reference in next step:**
- `docs/design/prototype.html` (styled section — the what)
- `DESIGN.md` (design tokens — the how)
- `$EFFORT_DIR/interaction/state-table.md` (state semantics, while the effort lives)
```

**AskUserQuestion** for next step:

> Visual design complete. Approved variant ready.
>
> **Next step:**
>
> **A)** Run `/design-implement` now (convert to production code)  
> **B)** Review interaction structure first — visual revealed UX issues  
> **C)** Update design system based on learnings  
> **D)** Done — I'll handle implementation manually

## Quality Checklist

Before marking visual design complete:

- [ ] All 3 variants share exact structure from the locked section
- [ ] All 5 states styled in the merged section
- [ ] DESIGN.md tokens used (not arbitrary values)
- [ ] Visual directions genuinely differ (not just color swaps)
- [ ] Merged section matches interaction intent from journey map
- [ ] State switcher works (user can preview all states)
- [ ] Mobile responsive if the section specified mobile behavior
- [ ] Accessibility contrast meets WCAG AA (check with browser tools)
- [ ] Section markers intact: still locked, fidelity styled, data-updated current

## Common Pitfalls

**Don't:**
- Change button positions or navigation hierarchy — that's interaction structure
- Generate variants with different layouts — structure is locked
- Skip empty/error states — all 5 states must be visualized
- Use colors outside DESIGN.md
- Make all 3 variants look similar — they need visual contrast

**Do:**
- Reference the locked section continuously to maintain structure
- Use state switcher to verify all 5 states work
- Apply DESIGN.md tokens consistently
- Make visual differences bold enough to compare
- Document why the chosen direction works better

## Integration with Other Skills

**Reads from:**
- `docs/design/prototype.html` — locked wireframe sections (structure baseline + states)
- `DESIGN.md` — visual tokens (via `/design-context` or `/design-system-create`)

**Feeds into:**
- `/design-implement` — the styled section (final visual to implement)

**Cannot be used without:**
- Locked sections must exist first
- Design authority must exist first

## Files Created

```
docs/design/prototype.html   # Section updated in place: wireframe → styled (CORE DELIVERABLE)

<work-root>/<effort>/
  visual/
    constraints.md         # Structural constraints from the locked section
    variants/              # 3 visual directions (working exploration)
      variant-a.html
      variant-b.html
      variant-c.html
    decision.md            # Visual decision rationale
```

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).

```text
Triad role:  WHAT (visuals) — raises locked sections from wireframe to styled fidelity
Layer:       human (the merged section) + working (variants and rationale)
Owns:        <work-root>/<effort>/visual/; the fidelity transition of in-scope prototype sections
Contributes: <work-root>/<effort>/design/capabilities.md — the `① taste` and `⑥ production` rows only
Coordinates: state.md — records the approved direction, the data-surface anchors, and the next stage
Promotes:    none beyond the merge — the styled section plus DESIGN.md are the durable record
```

Resolve the work root and active effort as in Step 0.

`Promotes: none` beyond the merge is deliberate. This skill picks among directions that `DESIGN.md` already permits; it does not create token authority. If choosing a variant reveals that the authority itself is wrong — a token missing, an accent that cannot carry the hierarchy — that is a change to `DESIGN.md` and routes back to `/design-context`, not a local override.

Durability test: the losing variants no — they were the argument. The winning treatment yes — it merges into the canonical section. `decision.md` explains a choice the merged section cannot show, so keep it until the component ships and its rationale is folded into the component doc.

**Update `state.md` at the approval gate** — approved direction, the styled `data-surface` anchors, next stage `/design-implement`.
