---
name: design-system-create
description: "Create the canonical design system document. Gathers product context, proposes typography/color/layout system grounded in user needs, generates preview, writes docs/design/system.md after approval. Consultative process that ties aesthetic choices to product goals and user constraints."
---

Last updated: 2026-08-10

# Design System Creation

Create the canonical design system that grounds all design work in this project.

## When to Use

- Starting design work on a new project with no existing design system
- Product context exists (PRD Part 1) but visual direction is undefined
- Existing design has drifted and needs formal documentation
- User asks: "create a design system", "define visual style", "what should this look like"

Do NOT use when:
- `docs/design/system.md` already exists and is current (validate and use it)
- Only exploring variants without defining the system (use `/design-explore-variants`)
- Implementing an already-approved design (use `/design-implement`)

## Inputs and Handoffs

**Upstream:**
- `docs/product/<slug>/prd.md` Part 1 (persona, platform, product type)
- `CONTEXT.md` (design principles or constraints if any)
- User's stated design direction or preferences

**Downstream:**
- `docs/design/system.md` → feeds `design-explore-variants` and `design-implement`
- System preview HTML → user approval gate

## Workflow

### Step 0: Check for Existing Design System

```bash
if [ -f docs/design/system.md ]; then
  echo "EXISTING_DESIGN_SYSTEM: yes"
  cat docs/design/system.md
else
  echo "EXISTING_DESIGN_SYSTEM: no"
fi
```

If `EXISTING_DESIGN_SYSTEM: yes`:
- Read the file and summarize its current state
- Ask: "This project has a design system at docs/design/system.md. Do you want to: (A) Validate and use it, (B) Update it, or (C) Replace it?"
- If A: STOP. No changes needed.
- If B: Continue to Step 1 but pre-fill from existing
- If C: Continue to Step 1 as if creating fresh

### Step 1: Gather Product Context

Read existing context sources first, then fill gaps with one comprehensive question.

**Auto-gather from:**

1. PRD Part 1 if it exists:
```bash
find docs/product -name "prd.md" -type f | head -1 | xargs cat 2>/dev/null || echo "NO_PRD"
```
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

Do NOT ask these as separate questions. Present all in one AskUserQuestion with:
- Pre-filled defaults from auto-gather
- Only ask for genuine gaps
- Include context about where each pre-fill came from

### Step 2: Design System Proposal

Generate a complete design system grounded in the product context. This is a consultative process — propose with rationale, not a form.

#### 2.1 Aesthetic Direction

Tie the aesthetic to product goals and user needs. Examples:

- **SaaS/productivity**: Clean, efficient, doesn't compete with user's content → minimalist with one accent
- **Marketing/portfolio**: Memorable, differentiating → bold typography, distinctive palette
- **Dashboard/analytics**: Scannable, hierarchical → clear type scale, muted palette with accent for alerts
- **Editorial/content**: Readable, comfortable → serif body text, generous line-height, warm palette
- **Internal tools**: Functional, fast to parse → system fonts, obvious states, high contrast

State the direction in 2-3 sentences with the "why" explicit.

#### 2.2 Typography

Query `ui-ux-pro-max` for font pairing recommendations:

```bash
python3 /Users/xhl/GitHub/learning-infra/agent-skill-projects/agent-coding-skills/system/skills-src/design/ux/ui-ux-pro-max/scripts/search.py typography --query "<category>" 2>/dev/null
```

Categories: modern, elegant, playful, professional, minimal, bold, editorial, technical

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

Query `ui-ux-pro-max` for palette recommendations:

```bash
python3 /Users/xhl/GitHub/learning-infra/agent-skill-projects/agent-coding-skills/system/skills-src/design/ux/ui-ux-pro-max/scripts/search.py color --query "<product-type>" 2>/dev/null
```

Product types: saas, ecommerce, healthcare, fintech, portfolio, editorial, dashboard

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

Create a simple preview showing the design system elements. This is Working-layer (disposable after approval), so write to:

```bash
mkdir -p .scratch/design-system/
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

Use AskUserQuestion with options:
- A) Approve this design system (write to docs/design/system.md)
- B) Adjust [specific element] — specify what to change
- C) Start over with different direction

If B: Make the requested changes and present again (max 3 iterations)
If C: Return to Step 1 with new direction

### Step 5: Write Design System Document

After approval, write to `docs/design/system.md`:

```markdown
# Design System

Last updated: YYYY-MM-DD

## Aesthetic Direction

[2-3 sentences: what this design communicates and why it fits the product/users]

## Typography

### Fonts
- **Heading**: [Font Name] — [rationale]
- **Body**: [Font Name] — [rationale]

### Font Stacks
```css
--font-heading: '[Font]', [fallbacks];
--font-body: '[Font]', [fallbacks];
```

### Type Scale
Base: 16px, Scale: 1.25

| Element | Size | Weight | Line Height |
|---------|------|--------|-------------|
| h1 | 2.441rem (39px) | 700 | 1.2 |
| h2 | 1.953rem (31px) | 700 | 1.3 |
| h3 | 1.563rem (25px) | 600 | 1.3 |
| h4 | 1.25rem (20px) | 600 | 1.4 |
| body | 1rem (16px) | 400 | 1.6 |
| small | 0.8rem (13px) | 400 | 1.5 |

## Color Palette

### Light Mode

**Surfaces:**
```css
--surface-page: #FFFFFF;
--surface-raised: #F9FAFB;
--surface-overlay: #FFFFFF;
```

**Text:**
```css
--text-primary: #111827;    /* Contrast: 15.3:1 ✓ */
--text-secondary: #6B7280;  /* Contrast: 4.6:1 ✓ */
--text-tertiary: #9CA3AF;   /* Contrast: 3.2:1 (large text only) */
```

**Accent:**
```css
--accent: #3B82F6;          /* Contrast: 4.5:1 on white ✓ */
--accent-hover: #2563EB;
--accent-active: #1D4ED8;
```

**Semantic:**
```css
--success: #10B981;
--warning: #F59E0B;
--error: #EF4444;
--info: #3B82F6;
```

**Borders:**
```css
--border-default: #E5E7EB;
--border-subtle: #F3F4F6;
```

### Dark Mode
[Same structure, dark variants]

## Spacing Scale

```css
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
```

## Layout

- **Primary approach**: Flex-based composition
- **Grid usage**: Card galleries, stat rows (genuinely 2D layouts)
- **Max width**: 1280px for app layouts, 65ch for text content
- **Breakpoints**: 640px (sm), 768px (md), 1024px (lg), 1280px (xl)

## Border Radius

```css
--radius-sm: 6px;     /* inputs, tags */
--radius-md: 10px;    /* cards, buttons */
--radius-lg: 20px;    /* feature panels */
--radius-full: 9999px; /* pills, avatars */
```

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

- Product context: docs/product/[slug]/prd.md Part 1
- Component specs: docs/design/components/
```

Confirm `docs/design/` directory exists, create if needed:

```bash
mkdir -p docs/design
```

### Step 6: Summary

Report what was created:
- `docs/design/system.md` — Human layer, git-tracked canonical design system
- `.scratch/design-system/system-preview.html` — Working layer, preview (can be deleted)

Next steps:
- Use `/design-explore-variants` to generate design options for specific features
- Use `/design-implement` to convert approved designs into production code
- Design system is now the source of truth; refer to it in all visual work

## Memory Layer Classification

**Human layer (git-tracked, outlives effort):**
- `docs/design/system.md` — canonical design system

**Working layer (gitignored, disposable):**
- `.scratch/design-system/system-preview.html` — approval preview

Apply the durability test: if the work root were deleted, would the project lose a fact it still needs? Design system YES (Human layer), preview NO (Working layer).

## Quality Gates

Before writing `docs/design/system.md`:
- [ ] All text/background pairs validated against WCAG AA
- [ ] Font choices avoid blacklist (no Papyrus, Comic Sans, Lobster, Impact, Jokerman)
- [ ] Generic fonts (Inter, Roboto, Poppins) have strong justification stated
- [ ] Type scale tested (readable at all sizes)
- [ ] Touch targets confirmed 44x44px minimum
- [ ] ONE decisive accent color (not three equal-weight brand colors)
- [ ] Rationale ties aesthetic to product/user needs (not arbitrary choices)

## Integration Points

**Reads from:**
- `docs/product/<slug>/prd.md` Part 1 (persona, platform)
- `CONTEXT.md` (design principles if any)
- `ui-ux-pro-max` typography and color catalogs

**Writes to:**
- `docs/design/system.md` (Human layer)

**Feeds:**
- `design-explore-variants` (uses system.md as constraint)
- `design-implement` (uses system.md for tokens/patterns)
- `spec` Part 3 (references design system for component specs)
