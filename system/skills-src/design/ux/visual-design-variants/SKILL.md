---
name: visual-design-variants
description: "Explore visual directions (color, typography, spacing) on top of established interaction structure. Requires wireframes from /interaction-design. Generates 3 variants with SAME structure but different visual treatments."
category: Design · Visual
triggers:
  - visual design
  - design variants
  - explore visuals
  - design options
---

Last updated: 2026-08-10

# Visual Design Variants

Explore **visual directions** (colors, typography, visual weight) on an already-defined **interaction structure**. This skill generates 3 variants that share the same layout but differ in visual treatment.

## Critical Constraint

**This skill CANNOT change interaction structure.** Button positions, navigation hierarchy, state transitions, and user flows are locked by the wireframe from `/interaction-design`. Only visual properties vary.

## When to Use

- After `/interaction-design` has defined wireframes and state table
- Design system exists (`docs/design/system.md`) 
- User wants to see visual options before committing
- Exploring visual hierarchy without changing interaction structure

Do NOT use when:
- No wireframes exist yet (run `/interaction-design` first)
- Interaction structure needs changes (go back to `/interaction-design`)
- No design system exists yet (run `/design-system-create` first)

## Inputs and Handoffs

**Upstream (REQUIRED):**
- `.scratch/<effort>/interaction/wireframes/*.html` (structure baseline - REQUIRED)
- `.scratch/<effort>/interaction/state-table.md` (all states to visualize - REQUIRED)
- `docs/design/system.md` (design system tokens - REQUIRED)

**Upstream (OPTIONAL):**
- `.scratch/<effort>/state.md` (current task context)
- `.scratch/<effort>/interaction/journey-map.md` (emotional intent)

**Upstream (OPTIONAL):**
- `.scratch/<effort>/state.md` (current task context)
- `.scratch/<effort>/interaction/journey-map.md` (emotional intent)

**Downstream:**
- `.scratch/<effort>/visual/variants/variant-a.html` → visual option A
- `.scratch/<effort>/visual/variants/variant-b.html` → visual option B
- `.scratch/<effort>/visual/variants/variant-c.html` → visual option C
- `.scratch/<effort>/visual/approved.html` → chosen variant (feeds `design-implement`)
- `.scratch/<effort>/visual/decision.md` → rationale for chosen visual direction

## Workflow

### Step 0: Verify Prerequisites

Check all required inputs exist:

```bash
# Find effort directory
EFFORT_DIR=$(find .scratch -maxdepth 1 -type d -name "[0-9]*-*" 2>/dev/null | sort -r | head -1)

if [ -z "$EFFORT_DIR" ]; then
  echo "ERROR: No effort directory found"
  exit 1
fi

# Check wireframes
if [ ! -d "$EFFORT_DIR/interaction/wireframes" ]; then
  echo "ERROR: No wireframes found - run /interaction-design first"
  exit 1
fi

# Check state table
if [ ! -f "$EFFORT_DIR/interaction/state-table.md" ]; then
  echo "ERROR: No state table found - run /interaction-design first"
  exit 1
fi

# Check design system
if [ ! -f "docs/design/system.md" ]; then
  echo "ERROR: No design system found - run /design-system-create first"
  exit 1
fi

echo "Prerequisites verified:"
echo "- Wireframes: $(ls -1 $EFFORT_DIR/interaction/wireframes/*.html 2>/dev/null | wc -l) files"
echo "- State table: found"
echo "- Design system: found"
```

If any check fails, **STOP** and report what's missing with the correct skill to run.

### Step 1: Read Interaction Structure

Load the wireframes and understand the locked structure:

```bash
# Read all wireframes
for wf in $EFFORT_DIR/interaction/wireframes/*.html; do
  echo "=== $(basename $wf) ==="
  cat "$wf"
done

# Read state table
cat $EFFORT_DIR/interaction/state-table.md

# Read design system
cat docs/design/system.md
```

**Extract and document:**

1. **Structural elements from wireframes** (these CANNOT change):
   - Header layout (logo position, nav structure, actions)
   - Main content zones (sidebar yes/no, columns, sections)
   - Component placement (where buttons/forms/data appears)
   - Footer structure
   - Mobile layout differences (if specified)

2. **States to visualize** (from state table):
   - All 5 states × N features = M total states to design
   - Note which states need visual attention (empty/error especially)

3. **Design tokens available** (from design system):
   - Typography: font families, size scale, weights
   - Colors: primary, accent, neutral scale, semantic colors
   - Spacing: base unit, scale
   - Component foundations: buttons, inputs, cards

Write structural constraints to `$EFFORT_DIR/visual/constraints.md`:

```markdown
## Visual Design Constraints

### Locked Structure (from wireframes)

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

[List from state table]
- Feature A: LOADING, EMPTY, ERROR, SUCCESS, PARTIAL
- Feature B: ...

### Design System Tokens

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

**Example adjustments on wireframe structure:**
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
> **C)** Show me the wireframe structure first

If C, open wireframe in browser before continuing.

### Step 3: Generate Visual Variants

For each direction (A, B, C), generate full HTML that:

1. **Preserves exact structure** from wireframe
2. **Applies visual treatment** per direction strategy
3. **Shows all states** from state table
4. **Uses design system tokens**

**Generation process per variant:**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Visual Variant [A/B/C] — [Feature Name]</title>
<style>
/* Design system tokens */
:root {
  /* Extract from docs/design/system.md */
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

/* Base structure from wireframe (LOCKED) */
[Copy exact layout structure from wireframe]

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
  [Full implementation preserving wireframe structure]
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
- Copy chosen variant to `$EFFORT_DIR/visual/approved.html`
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
- If approved, that becomes approved.html

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
- This visual design is ready to convert to production code
- All 5 states are defined and approved
- Structure matches wireframe (no interaction changes)
- Design system tokens were followed

**Files:**
- Approved visual: `$EFFORT_DIR/visual/approved.html`
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
- ✅ Approved visual design (`visual/approved.html`)
- ✅ Decision rationale (`visual/decision.md`)

**Structure Preservation:**
- ✅ Interaction structure from wireframes maintained
- ✅ All 5 states from state table visualized
- ✅ Design system tokens applied

**Ready for Next Step:**
This visual design is ready to feed into `/design-implement`.
The approved.html shows the final visual treatment on the locked interaction structure. Implementation will convert this to production code.

**Files to reference in next step:**
- `$EFFORT_DIR/visual/approved.html` (approved visual design)
- `$EFFORT_DIR/interaction/state-table.md` (state definitions)
- `docs/design/system.md` (design tokens)
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

- [ ] All 3 variants share exact structure from wireframe
- [ ] All 5 states visualized in approved variant
- [ ] Design system tokens used (not arbitrary values)
- [ ] Visual directions genuinely differ (not just color swaps)
- [ ] Approved variant matches interaction intent from journey map
- [ ] State switcher works (user can preview all states)
- [ ] Mobile responsive if wireframe specified mobile behavior
- [ ] Accessibility contrast meets WCAG AA (check with browser tools)

## Common Pitfalls

**Don't:**
- Change button positions or navigation hierarchy — that's interaction structure
- Generate variants with different layouts — structure is locked
- Skip empty/error states — all 5 states must be visualized
- Use colors outside the design system
- Make all 3 variants look similar — they need visual contrast

**Do:**
- Reference the wireframe continuously to maintain structure
- Use state switcher to verify all 5 states work
- Apply design system tokens consistently
- Make visual differences bold enough to compare
- Document why the chosen direction works better

## Integration with Other Skills

**Reads from:**
- `/interaction-design` — wireframes (structure baseline)
- `/interaction-design` — state-table.md (states to visualize)
- `/design-system-create` — system.md (visual tokens)

**Feeds into:**
- `/design-implement` — approved.html (final visual to implement)

**Cannot be used without:**
- Wireframes must exist first
- Design system must exist first

## Files Created

```
.scratch/<timestamp>-<effort>/
  visual/
    constraints.md         # Structural constraints from wireframe
    variants/              # 3 visual directions
      variant-a.html
      variant-b.html
      variant-c.html
    approved.html          # Chosen variant (CORE DELIVERABLE)
    decision.md            # Visual decision rationale
```

All files stay in Working layer (`.scratch/`) — they're exploration artifacts.

The approved visual design feeds into `/design-implement` which produces the Human layer docs and production code.

---

**Last updated:** 2026-08-10

**Variant C — Dense**: More information visible, compact spacing, efficient scanning
- Example: Multi-column layout, smaller hero, list-based features
- Example: Dashboard with many small panels, table-heavy

Adjust these principles based on the page type, but ensure the three are genuinely different approaches, not minor tweaks.

**Generation process:**

For each variant:
1. Design the HTML structure (semantic markup)
2. Apply design system tokens literally (copy from system.md)
3. Implement responsive breakpoints (mobile-first)
4. Ensure accessibility (WCAG AA, semantic HTML, ARIA labels)
5. Keep self-contained (inline styles or embedded CSS)

Write to working directory:
```bash
mkdir -p .scratch/$(basename $(pwd))/designs/variants
```

Files:
- `.scratch/<effort>/designs/variants/variant-a.html`
- `.scratch/<effort>/designs/variants/variant-b.html`
- `.scratch/<effort>/designs/variants/variant-c.html`

### Step 3: Present Variants for Comparison

Display all three variants with brief descriptions of their approach:

**Variant A: Balanced**
- Layout: [brief description]
- Emphasis: [what stands out]
- Best for: [type of user/goal]

[Inline render or code block of variant-a.html]

---

**Variant B: Focal**
- Layout: [brief description]
- Emphasis: [what stands out]
- Best for: [type of user/goal]

[Inline render or code block of variant-b.html]

---

**Variant C: Dense**
- Layout: [brief description]
- Emphasis: [what stands out]
- Best for: [type of user/goal]

[Inline render or code block of variant-c.html]

### Step 4: Collect Feedback

Use AskUserQuestion with structured options:

**Which variant is closest to what you want?**

Options:
- **A) Variant A (Balanced)** — approve as-is or specify adjustments
- **B) Variant B (Focal)** — approve as-is or specify adjustments  
- **C) Variant C (Dense)** — approve as-is or specify adjustments
- **D) None are right** — describe what's missing or what direction to try

For options A/B/C, include a text field: "Approve as-is or list specific changes (leave blank to approve)"

### Step 5: Iterate or Finalize

**If user approves a variant as-is:**
- Copy chosen variant to `.scratch/<effort>/designs/approved.html`
- Write decision rationale to `.scratch/<effort>/designs/decision.md`
- Go to Step 6

**If user requests adjustments:**
- Apply the requested changes to the chosen variant
- Generate 2 new alternatives exploring different approaches to the same goal
- Present the adjusted variant + 2 new options (total 3 again)
- Return to Step 4
- Max 3 iteration rounds; after that, recommend approval of closest option

**If user says "none are right":**
- Ask for more specific direction: "What's missing or what direction should we explore?"
- Generate 3 new variants based on that direction
- Return to Step 3
- Max 2 full regeneration rounds

### Step 6: Write Decision Record

After approval, document why this design was chosen:

```bash
cat > .scratch/$(basename $(pwd))/designs/decision.md << 'EOF'
# Design Decision

Last updated: YYYY-MM-DD

## Chosen Design

Variant: [A/B/C or description]
File: approved.html

## Rationale

[Why this design was chosen - from user feedback and context]

## Key Characteristics

- Layout approach: [description]
- Information hierarchy: [what's emphasized]
- Component choices: [notable decisions]
- User goal alignment: [how this serves the user]

## Alternatives Considered

- Variant [other]: [why not chosen]
- Variant [other]: [why not chosen]

## Next Steps

- Use /design-implement to convert to production code
- Design system tokens in: docs/design/system.md
EOF
```

Copy approved variant:
```bash
cp .scratch/$(basename $(pwd))/designs/variants/variant-[chosen].html .scratch/$(basename $(pwd))/designs/approved.html
```

### Step 7: Summary

Report what was created:
- `.scratch/<effort>/designs/approved.html` — Working layer, approved design ready for implementation
- `.scratch/<effort>/designs/decision.md` — Working layer, rationale and decision record
- `.scratch/<effort>/designs/variants/` — Working layer, exploration history (3+ HTML files)

Next steps:
- Run `/design-implement` to convert approved.html into production code
- Approved design follows the design system at `docs/design/system.md`
- Decision rationale captured in decision.md

## Memory Layer Classification

**Working layer (gitignored, disposable after implementation):**
- `.scratch/<effort>/designs/approved.html` — approved design
- `.scratch/<effort>/designs/decision.md` — decision record
- `.scratch/<effort>/designs/variants/*.html` — exploration history

All design exploration artifacts are Working-layer because they're scaffolding toward the final implementation. Once code is shipped, the HTML variants become obsolete — the shipped code is the source of truth.

Apply the durability test: if the work root were deleted, would the project lose a fact it still needs? The design system (system.md) YES, but specific variant HTMLs NO — they were exploration, not the building.

## Quality Gates

Before finalizing:
- [ ] All variants use design system tokens literally (no arbitrary colors/spacing)
- [ ] All variants pass WCAG AA contrast checks
- [ ] All variants are responsive (test at 375px, 768px, 1024px)
- [ ] Touch targets minimum 44x44px on mobile
- [ ] Semantic HTML (proper heading hierarchy, landmarks, labels)
- [ ] Variants are genuinely different approaches (not minor tweaks)
- [ ] User feedback incorporated accurately
- [ ] Decision rationale captures "why this one"

## Integration Points

**Reads from:**
- `docs/design/system.md` (design system - REQUIRED)
- `.scratch/<effort>/state.md` (task context)

**Writes to:**
- `.scratch/<effort>/designs/approved.html` (Working layer)
- `.scratch/<effort>/designs/decision.md` (Working layer)
- `.scratch/<effort>/designs/variants/*.html` (Working layer)

**Feeds:**
- `design-implement` (reads approved.html and system.md)

## Variant Generation Guidelines

When creating variants, balance these competing goals:

**Consistency** (across all variants):
- Same font families, type scale, weights
- Same color palette and semantic tokens
- Same spacing scale values
- Same component patterns (button styles, form treatments)
- Same accessibility standards

**Differentiation** (between variants):
- Layout structure (grid vs stack vs sidebar)
- Visual hierarchy (what dominates vs supports)
- Content density (generous whitespace vs information-rich)
- Component emphasis (large hero vs small header)
- Information flow (top-down vs scattered vs focal)

**Never vary** (anti-patterns):
- Don't introduce colors outside the design system
- Don't use different fonts or type scales between variants
- Don't violate accessibility standards to create distinction
- Don't sacrifice mobile usability for desktop drama
- Don't add gratuitous decoration or "AI slop" patterns

Good variants feel like they're from the same design system but serve different user modes or goals.
