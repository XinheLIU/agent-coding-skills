# System Specification Details

Last updated: 2026-10-23

Load only for the active artifact. The [skill procedure](../SKILL.md) and domain contracts govern; examples do not create authority.

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

- Tokens created from scratch via acs-design-system-create, YYYY-MM-DD
- Product context: configured product document persona/problem records
- Component specs: docs/design/components/
