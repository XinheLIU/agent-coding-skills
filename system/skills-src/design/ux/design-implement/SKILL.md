---
name: design-implement
description: "Turn an approved visual design into production code in the project's own stack and conventions, with design tokens wired up, WCAG AA met, and the component documented in docs/design/components/. Requires a styled section in docs/design/prototype.html and DESIGN.md. Use to implement or build a design that is already settled, not to explore one."
---

Last updated: 2026-09-09

# Design Implementation

Convert approved design into production code that matches the project's tech stack.

## When to Use

- Design is approved (a `styled`, `locked` section exists in `docs/design/prototype.html`)
- Design authority is defined (`DESIGN.md` at project root)
- Ready to implement actual production code (not exploring options)
- User asks: "implement this design", "turn this into code", "build the component"

Do NOT use when:
- No design authority exists yet (run `/design-context` or `/design-system-create` first)
- Still exploring options (use `/visual-design-variants`)
- The target section is still at `wireframe` fidelity (finish variant selection first)

## Inputs and Handoffs

**Upstream:**
- `docs/design/prototype.html` — the target section at `styled` fidelity, `data-structure="locked"`, all five state blocks (REQUIRED)
- `DESIGN.md` at project root (tokens/patterns — REQUIRED; legacy `docs/design/system.md` readable until migrated)
- `<work-root>/<effort>/interaction/state-table.md` (state semantics, when the effort is still live)
- Project tech stack (auto-detected)

**Downstream:**
- Production component code in project's source directory
- `docs/design/components/<name>.md` (Human layer component documentation)
- The prototype section marked `data-fidelity="implemented"` with `data-component` / `data-component-doc` pointers

## Workflow

### Step 0: Verify Prerequisites

Resolve the product document from explicit user paths, `docs/agents/memory.md`, and active `state.md`. New product memory uses `product.html#prd`; follow its persona, capability, scope, and question links. Legacy `prd.md` remains readable when canonical. Do not pick the first file found across products.

Resolve the work root from the same `docs/agents/memory.md`; with none configured, or no such file, it is `.scratch/`.

```bash
WORK_ROOT=<the path resolved above>

# Effort directory (optional working context)
EFFORT_DIR=$(find "$WORK_ROOT" -maxdepth 1 -type d -name "[0-9]*-*" 2>/dev/null | sort -r | head -1)

# Check for the canonical prototype
if [ -f docs/design/prototype.html ]; then
  echo "PROTOTYPE: found"
else
  echo "PROTOTYPE: missing"
fi

# Check for design authority
if [ -f DESIGN.md ] || [ -f docs/design/system.md ]; then
  echo "DESIGN_AUTHORITY: found"
else
  echo "DESIGN_AUTHORITY: missing"
fi
```

Then read the prototype and verify the target section: it must carry `data-fidelity="styled"` and `data-structure="locked"` with all five state blocks. 

If any prerequisite missing:
- STOP and report which is missing
- Guide user to run appropriate skill:
  - No prototype or section still at wireframe fidelity → run `/visual-design-variants`
  - No section for this surface at all → run `/interaction-design`
  - No design authority → run `/design-context` (or `/design-system-create` for from-scratch)

### Step 1: Read Context

**Load design inputs:**

1. The styled section of the canonical prototype:
```bash
cat docs/design/prototype.html
```

2. Design authority:
```bash
cat DESIGN.md 2>/dev/null || cat docs/design/system.md
```

3. Working context, when the effort is still live:
```bash
cat $EFFORT_DIR/interaction/state-table.md 2>/dev/null || echo "NO_STATE_TABLE (read state semantics from the section's data-state blocks)"
cat $EFFORT_DIR/visual/decision.md 2>/dev/null || echo "NO_DECISION"
cat $EFFORT_DIR/interaction/decisions.md 2>/dev/null || echo "NO_INTERACTION_DECISIONS"
```

**Extract key information:**
- **Styled section:** HTML structure, CSS rules, component patterns, the `data-capability` link back to the why
- **State blocks:** All 5 states rendered in the section (LOADING/EMPTY/ERROR/SUCCESS/PARTIAL)
- **Design authority:** Tokens (colors, fonts, spacing), component foundations
- **Decisions:** Rationale for design choices (informs implementation comments)

### Step 2: Detect Tech Stack

Inspect project files to determine the tech stack:

```bash
# Check for package.json (Node.js ecosystem)
if [ -f package.json ]; then
  echo "PACKAGE_MANAGER: npm/yarn/pnpm"
  cat package.json | grep -A 20 '"dependencies"'
fi

# Check for requirements.txt or pyproject.toml (Python)
if [ -f requirements.txt ] || [ -f pyproject.toml ]; then
  echo "PACKAGE_MANAGER: pip/uv"
  [ -f requirements.txt ] && head -20 requirements.txt
  [ -f pyproject.toml ] && head -40 pyproject.toml
fi

# Check for go.mod (Go)
if [ -f go.mod ]; then
  echo "LANGUAGE: go"
fi

# Check for Cargo.toml (Rust)
if [ -f Cargo.toml ]; then
  echo "LANGUAGE: rust"
fi
```

**Detect framework from package.json dependencies:**
- `"react"` → React (check for Next.js, look for CSS approach)
- `"vue"` → Vue (SFC with scoped styles)
- `"svelte"` → Svelte (SFC with scoped styles)
- `"@angular/core"` → Angular
- None of above + HTML project → Vanilla HTML/CSS

**Detect CSS approach:**
- `"tailwindcss"` → Tailwind utility classes
- `"@emotion/react"` or `"styled-components"` → CSS-in-JS
- CSS Modules pattern in imports → CSS Modules
- None → Plain CSS or inline styles

**Python web frameworks:**
- `"fastapi"` or `"flask"` or `"django"` → Jinja2 templates
- `"streamlit"` → Streamlit components

**Summarize detected stack:**
```
Stack: React 18 with Next.js 14
CSS: Tailwind CSS v3
Package manager: npm
```

### Step 3: Extract Design Tokens

From `DESIGN.md` frontmatter, extract tokens into stack-appropriate format.

**For CSS/Tailwind projects**, generate `styles/design-tokens.css`:
```css
:root {
  /* Typography */
  --font-heading: 'Inter', system-ui, sans-serif;
  --font-body: 'Inter', system-ui, sans-serif;
  
  /* Type scale */
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;
  
  /* Colors - Light mode */
  --surface-page: #ffffff;
  --surface-raised: #f9fafb;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --accent: #3b82f6;
  --accent-hover: #2563eb;
  
  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-12: 3rem;
  --space-16: 4rem;
  
  /* Border radius */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 20px;
  --radius-full: 9999px;
}

@media (prefers-color-scheme: dark) {
  :root {
    /* Dark mode overrides */
    --surface-page: #111827;
    --surface-raised: #1f2937;
    --text-primary: #f9fafb;
    --text-secondary: #d1d5db;
  }
}
```

**For Tailwind**, generate `tailwind.config.js` extensions:
```js
module.exports = {
  theme: {
    extend: {
      colors: {
        surface: {
          page: 'var(--surface-page)',
          raised: 'var(--surface-raised)',
        },
        accent: {
          DEFAULT: 'var(--accent)',
          hover: 'var(--accent-hover)',
        },
      },
      fontFamily: {
        heading: ['Inter', 'system-ui', 'sans-serif'],
        body: ['Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
}
```

**For React/CSS-in-JS**, generate `styles/tokens.ts`:
```typescript
export const tokens = {
  fonts: {
    heading: "'Inter', system-ui, sans-serif",
    body: "'Inter', system-ui, sans-serif",
  },
  colors: {
    surface: {
      page: '#ffffff',
      raised: '#f9fafb',
    },
    text: {
      primary: '#111827',
      secondary: '#6b7280',
    },
    accent: {
      default: '#3b82f6',
      hover: '#2563eb',
    },
  },
  spacing: {
    1: '0.25rem',
    2: '0.5rem',
    3: '0.75rem',
    4: '1rem',
    6: '1.5rem',
    8: '2rem',
  },
  radius: {
    sm: '6px',
    md: '10px',
    lg: '20px',
    full: '9999px',
  },
} as const;
```

Ask where to write tokens if location is ambiguous:
- "Where should I write the design tokens file? (e.g., `src/styles/tokens.css`, `styles/design-tokens.css`)"

### Step 4: Generate Component Code

Analyze the styled section's structure and generate production components.

**Ask for component details:**

Present what you found in the styled section (main elements, structure) and ask:

**What component(s) should I create?**
- Component name(s): e.g., "Hero", "FeatureCard", "ProductDashboard"
- Target directory: e.g., `src/components/`, `components/ui/`
- Standalone or composed: Single component or multiple sub-components?

**Generation principles:**

1. **Extract semantic structure** from the styled section
2. **Apply tech stack conventions:**
   - React: Functional components with TypeScript, props interface
   - Vue: SFCs with script setup and scoped styles
   - Svelte: SFCs with reactive declarations
   - HTML: Semantic markup with BEM-style classes
3. **Use design tokens** literally (reference token variables, don't hardcode values)
4. **Ensure accessibility:**
   - Semantic HTML (header, nav, main, section, article, footer)
   - Proper heading hierarchy (h1 → h2 → h3, no skips)
   - ARIA labels for icon buttons
   - Alt text for meaningful images
   - Form labels with `for` attribute
   - Focus styles visible (3px outline in accent color)
5. **Make responsive:**
   - Mobile-first breakpoints
   - Flexible layouts (flex/grid with fr/auto)
   - Touch targets 44x44px minimum
   - No horizontal scroll on small screens
6. **Component API:**
   - Props/attributes for dynamic content
   - Variants for different states (if applicable)
   - Sensible defaults

**Example React component:**

```typescript
// components/Hero.tsx
import React from 'react';
import styles from './Hero.module.css';

interface HeroProps {
  title: string;
  subtitle?: string;
  ctaText?: string;
  ctaHref?: string;
  imageSrc?: string;
  imageAlt?: string;
}

export function Hero({
  title,
  subtitle,
  ctaText = 'Get Started',
  ctaHref = '#',
  imageSrc,
  imageAlt = '',
}: HeroProps) {
  return (
    <section className={styles.hero}>
      <div className={styles.content}>
        <h1 className={styles.title}>{title}</h1>
        {subtitle && <p className={styles.subtitle}>{subtitle}</p>}
        <a href={ctaHref} className={styles.cta}>
          {ctaText}
        </a>
      </div>
      {imageSrc && (
        <div className={styles.image}>
          <img src={imageSrc} alt={imageAlt} loading="lazy" />
        </div>
      )}
    </section>
  );
}
```

```css
/* components/Hero.module.css */
.hero {
  display: flex;
  flex-direction: column;
  gap: var(--space-8);
  padding: var(--space-8);
  background: var(--surface-page);
}

.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

.title {
  font-family: var(--font-heading);
  font-size: var(--text-4xl);
  font-weight: 700;
  line-height: 1.2;
  color: var(--text-primary);
}

.subtitle {
  font-size: var(--text-lg);
  line-height: 1.6;
  color: var(--text-secondary);
}

.cta {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 44px;
  padding: var(--space-3) var(--space-6);
  background: var(--accent);
  color: white;
  font-weight: 600;
  border-radius: var(--radius-md);
  text-decoration: none;
  transition: background 0.2s;
}

.cta:hover {
  background: var(--accent-hover);
}

.cta:focus-visible {
  outline: 3px solid var(--accent);
  outline-offset: 2px;
}

.image {
  flex: 1;
}

.image img {
  width: 100%;
  height: auto;
  border-radius: var(--radius-lg);
}

@media (min-width: 768px) {
  .hero {
    flex-direction: row;
    align-items: center;
    padding: var(--space-12);
  }
  
  .content {
    max-width: 50%;
  }
}
```

Write the generated files to the target directory.

### Step 4.5: Polish Pass (optional)

Read `<work-root>/<effort>/design/capabilities.md`. If it carries a `③ method` row, follow that row's decision and continue at Step 5.

Otherwise scan the skills available in this session for one whose stated job is a named pass over UI code that already exists:

- **Craft and motion** — spring versus ease, hover behavior, transition timing
- **Optical refinement** — alignment, concentric radii, hit areas, shadow treatment
- **Accessibility** — contrast, focus order, ARIA coverage beyond the built-in gates

Append one row to `capabilities.md` recording what was found, or `none`. Rows are `| slot | found or none | decision | this skill |`; create the file with that header when absent. With `none`, continue at Step 5 — the Step 7 quality gates already enforce the baseline.

With something found, name it and what it would change, then **AskUserQuestion**:

> A polish capability is available: **[name]** — it would [what it changes, one clause].
>
> **A)** Skip it — the Step 7 quality gates already enforce the baseline (Recommended)
> **B)** Run it over the generated code before documenting

Three limits bound what a polish pass may change:

1. Visual values come from `DESIGN.md`. A polish pass may not introduce off-system colors or fonts.
2. Structure is locked. Anything requiring a layout, navigation, or state-transition change routes back to `/interaction-design` — it does not go into the code here.
3. Every applied fix gets one line in the component doc's `## Implementation Notes` (Step 6), naming what changed and why.

Done when `capabilities.md` carries a `③ method` row and the pass either ran within the three limits or was declined.

### Step 5: Generate Usage Example

Create a simple example showing how to use the component:

```typescript
// examples/hero-example.tsx (or in Storybook, or in README)
import { Hero } from '../components/Hero';

export function HeroExample() {
  return (
    <Hero
      title="Build faster with our platform"
      subtitle="The complete solution for modern development teams"
      ctaText="Start free trial"
      ctaHref="/signup"
      imageSrc="/hero-image.jpg"
      imageAlt="Platform dashboard screenshot"
    />
  );
}
```

### Step 6: Document Component

Write component documentation to `docs/design/components/<name>.md`:

```markdown
# [Component Name]

Last updated: YYYY-MM-DD

## Description

[1-2 sentences describing what this component does and when to use it]

## Preview

![Component preview](/path/to/screenshot)

*Design reference: `docs/design/prototype.html` section `[data-surface]`*

## Usage

\`\`\`[language]
[Usage example code]
\`\`\`

## API / Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `title` | `string` | required | Main heading text |
| `subtitle` | `string` | optional | Supporting text below title |
| `ctaText` | `string` | `"Get Started"` | Call-to-action button text |
| `ctaHref` | `string` | `"#"` | Button destination URL |

## Accessibility

- Semantic HTML: Uses `<section>` and proper heading hierarchy
- ARIA: Button has accessible label from `ctaText`
- Keyboard: CTA button is keyboard-focusable with visible focus ring
- Screen readers: Image has descriptive alt text via `imageAlt` prop
- Touch targets: CTA button is 44x44px minimum

## Responsive Behavior

- **Mobile (< 768px)**: Stacked layout, image below content
- **Tablet/Desktop (≥ 768px)**: Side-by-side layout, content left, image right

## Design System Mappings

Uses tokens from `DESIGN.md`:

- **Typography**: `--font-heading` (title), `--font-body` (subtitle)
- **Colors**: `--text-primary` (title), `--text-secondary` (subtitle), `--accent` (CTA)
- **Spacing**: `--space-8` (section padding), `--space-4` (content gap)
- **Radius**: `--radius-md` (button), `--radius-lg` (image)

## Variants

[If applicable, document different variants/states]

- Default
- With image
- Without image
- Dark mode (inherits from token dark mode)

## Related Components

[Links to related component docs]

## Implementation Notes

[Any technical details, gotchas, or future improvements]
```

Confirm directory exists:
```bash
mkdir -p docs/design/components
```

**Mark the prototype section implemented.** Update the section in `docs/design/prototype.html`: `data-fidelity="implemented"`, `data-component="<source-path>"`, `data-component-doc="docs/design/components/<name>.md"`, `data-updated`. Content stays as the approved design — the section is now canonical intent; the shipped code is canonical behavior. If implementation deviated from the section (a spacing fix, a responsive compromise), reconcile: fold the deviation back into the section if it is the better design, or note it as drift in the component doc. Never leave the divergence unstated.

### Step 7: Summary

Report what was created:

**Production code:**
- `[path]/[ComponentName].[ext]` — component implementation
- `[path]/[ComponentName].module.css` or styles — component styles (if separate)
- `[path]/tokens.[ext]` — design token definitions (if created)

**Documentation:**
- `docs/design/components/[name].md` — Human layer, component documentation

**Memory classification:**
- Component code → Project source (tracked by project's git rules)
- Component docs → Human layer (git-tracked, outlives effort)
- Prototype section → Human layer, marked implemented with component pointers
- Working exploration (variants, drafts) → Working layer (can be archived or deleted after implementation)

Next steps:
- Component is ready to use in the project
- Refer to component docs for API and usage examples
- DESIGN.md remains source of truth for tokens; the prototype section for design intent

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).

```text
Triad role:  WHAT (implemented) — ships the styled section as code and marks it implemented
Layer:       human (component docs + prototype section markers) + project source (code)
Owns:        docs/design/components/<name>.md; the implemented transition of in-scope prototype sections
Contributes: <work-root>/<effort>/design/capabilities.md — the `③ method` row only
Coordinates: state.md — records the component as shipped and closes the design stage
Promotes:    reusable component conventions → docs/conventions, via sync-context
```

Resolve the work root and active effort as in Step 0. The component code follows the project's own git rules; this skill does not decide those.

Durability test: the component doc yes — it carries the API, the states, and the reasons behind implementation choices that the code cannot show. The prototype section yes — it stays canonical intent, now with pointers to the code that realizes it. The working variants no; the merged section superseded them at approval.

After shipping, the shipped component is canonical **behavior** and the section canonical **intent**; when they diverge later, report the divergence — regenerate the section from the component for small drift, reopen it through the pipeline for deliberate redesign.

A convention discovered while building — how this codebase handles compound components, where token overrides are permitted, what the focus-ring pattern is — binds the next contributor and does not belong in one component's doc. Route it to `docs/conventions` via `sync-context`.

**Update `state.md` when the component lands** — component path, doc path, the implemented `data-surface` anchor, design stage complete. This is the pipeline's last stage, so the pointer closes it rather than naming a successor.

## Quality Gates

Before finalizing:
- [ ] Component uses design tokens (no hardcoded colors/spacing)
- [ ] WCAG AA contrast validated (4.5:1 for text, 3:1 for large text)
- [ ] Semantic HTML (proper tags, heading hierarchy)
- [ ] ARIA labels for icon-only buttons
- [ ] Keyboard accessible (focusable, visible focus rings)
- [ ] Touch targets 44x44px minimum on mobile
- [ ] Responsive tested (375px, 768px, 1024px breakpoints)
- [ ] Component API documented with prop types
- [ ] Usage example provided
- [ ] Matches tech stack conventions (file naming, folder structure)

## Integration Points

**Reads from:**
- `docs/design/prototype.html` (styled section — REQUIRED)
- `DESIGN.md` (design tokens — REQUIRED)
- Project files (package.json, etc.) for stack detection

**Writes to:**
- Project source directory (component code)
- `docs/design/components/<name>.md` (Human layer documentation)
- `docs/design/prototype.html` (section markers: implemented + component pointers)
- Token files (styles/tokens.css or equivalent)

**Feeds:**
- Component docs feed `spec` (reference for implementation)
- Tokens feed all future component work (consistent styling)

**Optional polish pass:** an external craft, motion, or accessibility reviewer may run in Step 4.5 within the three limits stated there. The native quality gates run either way.
