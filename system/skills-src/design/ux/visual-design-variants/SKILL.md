---
name: visual-design-variants
description: "Explore three genuinely different visual directions — color, typography, weight — on interaction structure that is already locked. Requires locked wireframe sections in docs/design/prototype.html plus DESIGN.md; cannot move buttons, navigation, or state transitions. The approved direction merges into the canonical prototype as its styled section. Use to compare visual options or design variants before committing to one."
---

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [design.locked_structure, design.applicable_rules]
  retrieves: [change.requirements, design.relevant_decisions]
  produces: [design.visual_decision]
  updates: [design.prototype_intent, design.accepted_decisions]
  invalidates: [implementation.visual_dependents, verification.visual_evidence]
  handoff_to: [implementation]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


# Visual Design Variants

Explore **visual directions** (colors, typography, visual weight) on an already-defined **interaction structure**. This skill generates 3 variants that share the same layout but differ in visual treatment.

## Critical Constraint

**This skill CANNOT change interaction structure.** Button positions, navigation hierarchy, state transitions, and user flows are locked in the prototype section by `/design-interaction-flow` (`data-structure="locked"`). Only visual properties vary.

## When to Use

- After `/design-interaction-flow` has locked wireframe sections in `docs/design/prototype.html`
- Design authority exists (`DESIGN.md` at project root)
- User wants to see visual options before committing
- Exploring visual hierarchy without changing interaction structure

Do NOT use when:
- No locked wireframe sections exist yet (run `/design-interaction-flow` first)
- Interaction structure needs changes (go back to `/design-interaction-flow`)
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

Use the coordinator-resolved product/spec and relevant records. Preserve canonical requirement/criterion IDs and distinguish observed behavior from accepted intent.

Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

The coordinator supplies the configured work root and exact active effort; never select the newest directory as identity.

Then read the prototype and verify the target surfaces are ready: each section this effort styles must carry `data-structure="locked"`. A section still `open` goes back to `/design-interaction-flow`. Note the in-scope `data-surface` slugs and confirm all five `data-state` blocks are present in each.

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

**Ask through the coordinator** to understand intent:

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

**Ask through the coordinator** to confirm directions before generating:

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

Request optional ① taste and ⑥ production results through the coordinator. Native direction/HTML generation is the fallback.

Whatever produces them, the output must satisfy this skill's contract:

1. The locked section structure survives intact (Step 1 constraints).
2. Every visual value traces to `DESIGN.md` — no invented colors or fonts.
3. Files land at `$EFFORT_DIR/visual/variants/variant-{a,b,c}.html` with the Step 3 state switcher present. Copy or rename if the tool writes elsewhere.
4. All five states from the locked section appear in each variant.

If the output cannot meet these four, generate inline per Step 3 — the default path.

Done when the three variants satisfy the domain checks; return capability outcomes to the coordinator.

### Step 3: Generate Visual Variants

For each direction (A, B, C), generate full HTML that:

1. **Preserves exact structure** from the locked section
2. **Applies visual treatment** per direction strategy
3. **Shows all states** from the section's state blocks
4. **Uses DESIGN.md tokens**

**Generation process per variant:**

Read [Example 1](references/output-examples.md#example-1) when producing this artifact.

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

**Ask through the coordinator** for feedback:

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
- **Ask through the coordinator**: "What's missing visually?" or "What feeling isn't captured?"
- Define 3 NEW visual directions
- Regenerate from Step 3

### Step 6: Document Visual Decision

Once variant approved, write decision rationale:

Read [Example 2](references/output-examples.md#example-2) when producing this artifact.

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

**Ask through the coordinator** for next step:

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

## Accepted decision handoff

At acceptance, retain consequential decision IDs, rationale, alternatives, affected surfaces/criteria, and consumed requirement/token/contract revisions beside the accepted design or in linked Change Context, following [the Design contract](references/design-memory.md). Do not wait for component documentation. Draft notes and rejected variant files may remain in Run Context after this reconciliation. Return accepted references, delta, unresolved questions/blocking effects, and next action to the coordinator.

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).


Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

This skill picks among directions that `DESIGN.md` already permits; it does not create token authority. Retain consequential selection rationale with the accepted decision before implementation. If choosing a variant reveals that the authority itself is wrong — a token missing, an accent that cannot carry the hierarchy — that is a change to `DESIGN.md` and routes back to `/design-context`, not a local override.

Durability test: the losing variants no — they were the argument. The winning treatment yes — it merges into the canonical section. `decision.md` explains a choice the merged section cannot show, so keep it until the component ships and its rationale is folded into the component doc.

**Return the transition to the coordinator at the approval gate** — approved direction, the styled `data-surface` anchors, next stage `/design-implement`.
