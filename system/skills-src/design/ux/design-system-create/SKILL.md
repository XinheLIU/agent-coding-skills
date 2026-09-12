---
name: design-system-create
description: "Build design authority from scratch when there is nothing to adopt — no DESIGN.md, no reference brand. Proposes typography, color, and layout tied to the product's persona and constraints, previews it, and writes a root DESIGN.md on approval. Use when asked to create a design system or define visual style; if a reference or DESIGN.md exists, run /design-context instead."
---

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [product.relevant_context]
  retrieves: [design.existing_authority, operations.constraints]
  produces: [design.tokens, design.rationale]
  updates: [design.applicable_rules, design.accepted_decisions]
  invalidates: [design.token_dependents]
  handoff_to: [interaction_design, visual_design]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


# Design System Creation

Create the canonical design authority that grounds all design work in this project: `DESIGN.md` at the project root — the **how** of the shared design triad ([references/design-memory.md](references/design-memory.md)).

## When to Use

- Starting design work on a new project with no existing design system
- Product context exists (PRD Part 1) but visual direction is undefined
- Existing design has drifted and needs formal documentation
- User asks: "create a design system", "define visual style", "what should this look like"

Do NOT use when:
- `DESIGN.md` already exists and is current (validate and use it; `/design-context` re-syncs it)
- Only exploring variants without defining the system (use `/visual-design-variants`)
- Implementing an already-approved design (use `/design-implement`)

## Inputs and Handoffs

**Upstream:**
- the configured product document (`product.html#prd`, or a canonical legacy PRD) Part 1 (persona, platform, product type)
- `CONTEXT.md` (design principles or constraints if any)
- User's stated design direction or preferences

**Downstream:**
- `DESIGN.md` at project root → feeds `design-interaction-flow`, `visual-design-variants`, and `design-implement`
- System preview HTML → user approval gate

## Workflow

### Step 0: Check for Existing Design Authority

Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

The coordinator supplies the configured work root and exact active effort; never select the newest directory as identity.

This skill does not require an active effort — with no effort directory, write the preview to `$WORK_ROOT/design/` instead.

```bash
if [ -f DESIGN.md ]; then
  echo "EXISTING_DESIGN_AUTHORITY: yes"
  cat DESIGN.md
elif [ -f docs/design/system.md ]; then
  echo "LEGACY_SYSTEM_MD: yes — route to /design-context to migrate"
else
  echo "EXISTING_DESIGN_AUTHORITY: no"
fi
```

A legacy `docs/design/system.md` with no `DESIGN.md` is a migration, not a creation — hand off to `/design-context` Step 1.

If `EXISTING_DESIGN_AUTHORITY: yes`:
- Read the file and summarize its current state
- Ask: "This project has design authority at DESIGN.md. Do you want to: (A) Validate and use it, (B) Update it, or (C) Replace it?"
- If A: STOP. No changes needed.
- If B: Continue to Step 1 but pre-fill from existing
- If C: Continue to Step 1 as if creating fresh

### Step 1: Gather Product Context

Read existing context sources first, then fill gaps with one comprehensive question.

**Auto-gather from:**

1. Resolve the active product document from explicit user paths, `docs/agents/memory.md`, and `state.md`. Read its persona/problem and platform records through the PRD reading index; use a legacy PRD if it remains canonical. Do not select the first product found on disk.
Extract: persona (who), platform (web/mobile/desktop), product type (SaaS/marketing/dashboard/etc.)

2. CONTEXT.md if it exists:
```bash
[ -f CONTEXT.md ] && cat CONTEXT.md || echo "NO_CONTEXT"
```
Extract: any stated design principles or constraints

3. README.md for product overview:
```bash
[ -f README.md ] && head -50 README.md || echo "NO_README"
```

**Then ask ONE comprehensive question** for anything not auto-gathered:

Present what you found (persona, platform, type) and ask for:
- **What**: What does this product do? (1 sentence)
- **Who**: Who uses it? (persona if not in PRD)
- **Platform**: web app | mobile app | desktop | marketing site | dashboard
- **Category**: SaaS | e-commerce | portfolio | editorial | internal tool | other
- **Memorable thing**: What should users remember about this experience? (forces unique direction)
- **Design direction**: Any specific aesthetic, references, or constraints?

Do NOT ask these as separate questions. Present all in one question through the coordinator with:
- Pre-filled defaults from auto-gather
- Only ask for genuine gaps
- Include context about where each pre-fill came from

### Step 2: Design System Proposal

Generate a complete design system grounded in the product context. This is a consultative process — propose with rationale, not a form.

Request optional ② type/color knowledge through the coordinator. Use it as evidence for palette/type choices; this skill owns the decision and native fallback.

### 2.1 Aesthetic Direction

Tie the aesthetic to product goals and user needs. Examples:

- **SaaS/productivity**: Clean, efficient, doesn't compete with user's content → minimalist with one accent
- **Marketing/portfolio**: Memorable, differentiating → bold typography, distinctive palette
- **Dashboard/analytics**: Scannable, hierarchical → clear type scale, muted palette with accent for alerts
- **Editorial/content**: Readable, comfortable → serif body text, generous line-height, warm palette
- **Internal tools**: Functional, fast to parse → system fonts, obvious states, high contrast

State the direction in 2-3 sentences with the "why" explicit.

#### 2.2 Typography

When the `② knowledge — type/color` row says to consult a reference, look up pairings that suit this product category and cite what came from where. Otherwise propose from first principles below — the default path.

**Shortcut worth offering:** if a published spec already fits this product type closely, adopting it wholesale via `/design-context` beats composing one from scratch. Offer it; proceed only on approval.

Choose ONE pairing (heading + body) that matches the aesthetic direction. Provide:
- Heading font with rationale
- Body font with rationale
- Font stack (primary + fallbacks)
- Type scale (base 16px, scale factor 1.25 or 1.333)
  - h1, h2, h3, body, small sizes
- Line height (1.5-1.75 for body, 1.2-1.4 for headings)
- Font weights (which weights are used and where)

**Hard rules** (from G-Stack, enforced):
- NO: Papyrus, Comic Sans, Lobster, Impact, Jokerman
- CAUTION: Inter, Roboto, Poppins, system-ui (generic; need strong justification)

#### 2.3 Color Palette

When that same row says to consult a reference, look up the palette for the product type (saas, ecommerce, healthcare, fintech, portfolio, editorial, dashboard). Otherwise propose from first principles — the default path.

Choose ONE palette. Provide semantic color tokens:

**Surface colors** (2-3 levels only, not a long tonal ramp):
- `--surface-page`: page background
- `--surface-raised`: card/panel background
- `--surface-overlay`: modal/dropdown background

**Text colors**:
- `--text-primary`: body text
- `--text-secondary`: muted text
- `--text-tertiary`: placeholder text

**Accent color** (ONE decisive accent, not three equal-weight brand colors):
- `--accent`: primary interactive color
- `--accent-hover`: hover state
- `--accent-active`: pressed state

**Semantic colors**:
- `--success`, `--warning`, `--error`, `--info`

**Borders**:
- `--border-default`, `--border-subtle`

**WCAG AA validation**: All text/background combinations MUST pass 4.5:1 contrast for normal text, 3:1 for large text (18pt+). State this explicitly.

#### 2.4 Layout & Spacing

**Spacing scale** (geometric progression):
```
--space-1: 0.25rem (4px)
--space-2: 0.5rem (8px)
--space-3: 0.75rem (12px)
--space-4: 1rem (16px)
--space-6: 1.5rem (24px)
--space-8: 2rem (32px)
--space-12: 3rem (48px)
--space-16: 4rem (64px)
```

**Layout approach**:
- Primary: flex-based composition
- Grid: only for genuinely 2D layouts (card galleries, stat rows)
- Max content width (if applicable): 65ch for text, 1200-1400px for app layouts
- Breakpoints: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)

**Border radius**:
- Small: 3-6px (inputs, tags)
- Medium: 8-12px (cards, buttons)
- Large: 16-20px (feature panels)
- Full: 9999px (pills, avatars)

#### 2.5 Component Foundations

Define the core patterns (don't build components yet):

**Buttons**:
- Primary, secondary, ghost variants
- States: default, hover, active, disabled, loading
- Size: touch-safe minimum 44x44px

**Forms**:
- Input states: default, focus, error, disabled
- Label positioning: above (recommended) or inline
- Error messages: below field, specific

**Cards**:
- Padding, shadow/border treatment
- Interactive vs static
- Hover states if clickable

State these as principles, not code.

### Step 3: Generate Preview HTML

Create a simple preview showing the design system elements. This is Run Context (disposable after approval), so write to:

```bash
mkdir -p "$WORK_ROOT/$EFFORT/design"
```

Generate `system-preview.html` with:
- Typography scale demonstrated (h1-h4, body, small)
- Color palette swatches with hex codes
- Spacing scale visual ruler
- Button states (primary, secondary, ghost × default, hover, disabled)
- Form inputs (default, focus, error states)
- Card example

Keep it simple — one self-contained HTML file with inline styles using the proposed tokens.

### Step 4: Present for Approval

Show the design system proposal:

1. **Aesthetic direction** (2-3 sentences with rationale)
2. **Typography** (heading + body fonts, type scale, rationale)
3. **Color palette** (semantic tokens with hex codes, WCAG contrast confirmation)
4. **Layout & spacing** (scale, approach, radii)
5. **Component foundations** (button/form/card patterns)

Then display the preview HTML inline so the user can see it rendered.

Use the coordinator’s question interface with options:
- A) Approve this design system (write DESIGN.md at the project root)
- B) Adjust [specific element] — specify what to change
- C) Start over with different direction

If B: Make the requested changes and present again (max 3 iterations)
If C: Return to Step 1 with new direction

### Step 5: Write DESIGN.md

After approval, write `DESIGN.md` at the project root. Machine-readable tokens go in YAML frontmatter; judgment stays in prose. This is the shape external ⑤ lifecycle tools maintain, so the native path and the tool path produce the same file.

Read [Example 1](references/output-examples.md#example-1) when producing this artifact.

### Type Scale
Base and ratio per frontmatter.

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| h1 | 2.441rem (39px) | 700 | 1.2 |
| h2 | 1.953rem (31px) | 700 | 1.3 |
| h3 | 1.563rem (25px) | 600 | 1.3 |
| h4 | 1.25rem (20px) | 600 | 1.4 |
| body | 1rem (16px) | 400 | 1.6 |
| small | 0.8rem (13px) | 400 | 1.5 |

## Color Palette

Token values live in the frontmatter — one source, no duplication in prose. Record here only the judgment: contrast validations (`--text-primary` on `--surface-page`: 15.3:1 ✓), what each accent state is for, and dark-mode variants when defined.

## Spacing Scale

Values per frontmatter `spacing`. Record here only usage guidance (component padding uses 24/32; section rhythm uses 48/64).

## Layout

- **Primary approach**: Flex-based composition
- **Grid usage**: Card galleries, stat rows (genuinely 2D layouts)
- **Max width**: 1280px for app layouts, 65ch for text content
- **Breakpoints**: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)

## Border Radius

Values per frontmatter `radius`: sm for inputs and tags, md for cards and buttons, lg for feature panels, full for pills and avatars.

## Component Foundations

### Buttons
- **Sizes**: 44x44px minimum (touch-safe)
- **Variants**: primary (filled accent), secondary (outlined), ghost (text only)
- **States**: default, hover (-10% lightness), active (-20% lightness), disabled (50% opacity), loading (spinner + disabled)

### Forms
- **Labels**: Above input (preferred), 14px, semibold
- **Inputs**: 44px height, --radius-sm, --border-default
- **States**: 
  - Default: border-default
  - Focus: accent border, 3px outline
  - Error: error border, error message below
  - Disabled: 60% opacity, cursor-not-allowed
- **Error messages**: Below field, error color, 14px

### Cards
- **Padding**: var(--space-6) or var(--space-8)
- **Border**: 1px solid var(--border-default) or shadow-sm
- **Interactive**: Add hover state (shadow-md), cursor-pointer
- **Static**: No hover state

## Accessibility

- All text/background pairs pass WCAG AA (4.5:1 for normal text, 3:1 for large text ≥18pt)
- Touch targets minimum 44x44px
- Focus states visible with 3px outline
- Form labels explicit (not placeholder-only)
- Semantic HTML structure

## References

- Tokens created from scratch via design-system-create, YYYY-MM-DD
- Product context: configured product document persona/problem records
- Component specs: docs/design/components/
```

If `docs/design/prototype.html` exists, re-sync its `:root` token block from the new frontmatter (see `/design-context` Step 4).

### Step 6: Summary

Report what was created:
- `DESIGN.md` — Current State, git-tracked canonical design authority (the triad's **how**)
- `<work-root>/<effort>/design/system-preview.html` — Run Context, preview (can be deleted)

Next steps:
- Use `/design-interaction-flow` to define structure and states in the canonical prototype, then `/visual-design-variants` for visual options
- Use `/design-implement` to convert approved designs into production code
- DESIGN.md is now the source of truth; refer to it in all visual work

## Accepted decision handoff

At acceptance, retain consequential decision IDs, rationale, alternatives, affected surfaces/criteria, and consumed requirement/token/contract revisions beside the accepted design or in linked Change Context, following [the Design contract](references/design-memory.md). Do not wait for component documentation. Draft notes and rejected variant files may remain in Run Context after this reconciliation. Return accepted references, delta, unresolved questions/blocking effects, and next action to the coordinator.

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).


Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

Durability test: `DESIGN.md` yes — every later component reads it. The preview no; once the authority is written, the authority is the answer.

Most aesthetic choices are settled by `DESIGN.md` itself and promote nowhere. The exception is a choice that constrains engineering — a type scale that forces a layout system, a token structure that dictates how theming works. Route that rationale to an ADR; leave taste in `DESIGN.md`.

## Quality Gates

Before writing `DESIGN.md`:
- [ ] All text/background pairs validated against WCAG AA
- [ ] Font choices avoid blacklist (no Papyrus, Comic Sans, Lobster, Impact, Jokerman)
- [ ] Generic fonts (Inter, Roboto, Poppins) have strong justification stated
- [ ] Type scale tested (readable at all sizes)
- [ ] Touch targets confirmed 44x44px minimum
- [ ] ONE decisive accent color (not three equal-weight brand colors)
- [ ] Rationale ties aesthetic to product/user needs (not arbitrary choices)
- [ ] Frontmatter tokens and prose sections both present; provenance line in `## References`

## Integration Points

**Reads from:**
- the configured product document (`product.html#prd`, or a canonical legacy PRD) Part 1 (persona, platform)
- `CONTEXT.md` (design principles if any)

**Writes to:**
- `DESIGN.md` at project root (Current State)
- `docs/design/prototype.html` `:root` token block (sync only, when a prototype exists)

**Feeds:**
- `visual-design-variants` (uses DESIGN.md as constraint)
- `design-implement` (uses DESIGN.md for tokens/patterns)
- `spec` (references design authority for component specs)

**When a reference exists instead:** `/design-context` imports it rather than proposing from scratch. This skill is the no-reference path.
