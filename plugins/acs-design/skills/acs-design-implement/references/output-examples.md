# Output Examples

Last updated: 2026-09-10

Load only the example linked by the active step. These are templates, not additional sources of requirements or design authority.

## Example 1

Used by: Step 3: Extract Design Tokens. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

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

## Example 2

Used by: Step 3: Extract Design Tokens. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

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

## Example 3

Used by: Step 4: Generate Component Code. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

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

## Example 4

Used by: Step 4: Generate Component Code. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

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

## Example 5

Used by: Step 6: Document Component. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

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
