---
name: design-implement
description: "Convert approved design into production code matching the project's tech stack. Extracts design tokens, builds components following stack conventions, ensures accessibility (WCAG AA), generates responsive code. Documents in docs/design/components/."
---

Last updated: 2026-08-17

# Design Implementation

Convert approved design into production code that matches the project's tech stack.

## When to Use

- Design is approved (`.scratch/<effort>/visual/approved.html` exists)
- Design system is defined (`docs/design/system.md` exists)
- Ready to implement actual production code (not exploring options)
- User asks: "implement this design", "turn this into code", "build the component"

Do NOT use when:
- No design system exists yet (run `/design-context` or `/design-system-create` first)
- Still exploring options (use `/visual-design-variants`)
- Design not yet approved (finish variant selection first)

## Inputs and Handoffs

**Upstream:**
- `.scratch/<effort>/visual/approved.html` (approved visual design - REQUIRED)
- `.scratch/<effort>/interaction/state-table.md` (state definitions - REQUIRED)
- `docs/design/system.md` (design system for tokens/patterns - REQUIRED)
- Project tech stack (auto-detected)

**Downstream:**
- Production component code in project's source directory
- `docs/design/components/<name>.md` (Human layer component documentation)

## Workflow

### Step 0: Verify Prerequisites

```bash
# Find effort directory
EFFORT_DIR=$(find .scratch -maxdepth 1 -type d -name "[0-9]*-*" 2>/dev/null | sort -r | head -1)

# Check for approved visual design
if [ -f "$EFFORT_DIR/visual/approved.html" ]; then
  echo "APPROVED_DESIGN: found"
else
  echo "APPROVED_DESIGN: missing"
fi

# Check for state table
if [ -f "$EFFORT_DIR/interaction/state-table.md" ]; then
  echo "STATE_TABLE: found"
else
  echo "STATE_TABLE: missing"
fi

# Check for design system
if [ -f docs/design/system.md ]; then
  echo "DESIGN_SYSTEM: found"
else
  echo "DESIGN_SYSTEM: missing"
fi
```

If any prerequisite missing:
- STOP and report which is missing
- Guide user to run appropriate skill:
  - No approved.html → run `/visual-design-variants`
  - No state-table.md → run `/interaction-design`
  - No system.md → run `/design-context` (or `/design-system-create` for from-scratch)

### Step 1: Read Context

**Load design inputs:**

1. Approved visual design:
```bash
cat $EFFORT_DIR/visual/approved.html
```

2. Interaction state table:
```bash
cat $EFFORT_DIR/interaction/state-table.md
```

3. Design system:
```bash
cat docs/design/system.md
```

4. Decision rationale (if exists):
```bash
cat $EFFORT_DIR/visual/decision.md 2>/dev/null || echo "NO_DECISION"
cat $EFFORT_DIR/interaction/decisions.md 2>/dev/null || echo "NO_INTERACTION_DECISIONS"
```

**Extract key information:**
- **Visual design:** HTML structure, CSS rules, component patterns
- **State table:** All 5 states per feature (LOADING/EMPTY/ERROR/SUCCESS/PARTIAL)
- **Design system:** Tokens (colors, fonts, spacing), component foundations
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

From `docs/design/system.md`, extract tokens into stack-appropriate format.

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

Analyze the approved.html structure and generate production components.

**Ask for component details:**

Present what you found in approved.html (main elements, structure) and ask:

**What component(s) should I create?**
- Component name(s): e.g., "Hero", "FeatureCard", "ProductDashboard"
- Target directory: e.g., `src/components/`, `components/ui/`
- Standalone or composed: Single component or multiple sub-components?

**Generation principles:**

1. **Extract semantic structure** from approved.html
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

### Step 4.5: External Polish Pass (optional, layer ③)

If polish/review skills are installed (see `design/ux/README.md` layer ③ — interaction-craft, motion-design, "feel-better", or a11y-review skills), run a review pass over the generated code before documenting it:

- **Interaction craft / motion** — spring vs ease decisions, hover behavior, transition timing
- **Feel-better** — optical alignment, concentric radii, hit areas, shadow treatment
- **A11y review** — contrast, focus order, ARIA coverage beyond the built-in gates

**Authority limits for the polish pass:**

- Visual token values come from `docs/design/system.md` — a polish skill may NOT introduce off-system colors/fonts
- Structure (layout, navigation, state transitions) is locked — anything requiring structural change goes back to `/interaction-design`, not into the code
- Record every applied fix in the component doc's `## Implementation Notes` (Step 6), one line per fix with the skill that suggested it

If no polish skill is installed, skip silently — the built-in quality gates (Step 7) already enforce the baseline.

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

![Component preview](/path/to/screenshot-or-figma-embed)

*Design reference: `.scratch/<effort>/visual/approved.html`*

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

Uses tokens from `docs/design/system.md`:

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
- Approved HTML → Working layer (can be archived or deleted after implementation)

Next steps:
- Component is ready to use in the project
- Refer to component docs for API and usage examples
- Design system remains source of truth for tokens at `docs/design/system.md`

## Memory Layer Classification

**Human layer (git-tracked, outlives effort):**
- `docs/design/components/<name>.md` — component documentation

**Project source (git-tracked per project conventions):**
- Component code files (in src/components or equivalent)
- Token/style files (in styles/ or equivalent)

**Working layer (gitignored, can be archived after implementation):**
- `.scratch/<effort>/visual/approved.html` — served its purpose once implemented

Apply the durability test: component docs YES (they outlive the implementation effort and serve as reference), approved HTML NO (it was scaffolding, the real code supersedes it).

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
- `.scratch/<effort>/visual/approved.html` (approved design - REQUIRED)
- `docs/design/system.md` (design system tokens - REQUIRED)
- Project files (package.json, etc.) for stack detection

**Writes to:**
- Project source directory (component code)
- `docs/design/components/<name>.md` (Human layer documentation)
- Token files (styles/tokens.css or equivalent)

**Feeds:**
- Component docs feed `spec` (reference for implementation)
- Tokens feed all future component work (consistent styling)

**External skills (optional):** layer-③ polish skills (interaction craft, motion, feel-better, a11y review) may run a review pass in Step 4.5 — see `design/ux/README.md`. Native quality gates run regardless.
