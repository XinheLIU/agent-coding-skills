# Output Examples

Last updated: 2026-09-09

Load only the example linked by the active step. These are templates, not additional sources of requirements or design authority.

## Example 1

Used by: Step 5: Write DESIGN.md. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

```markdown
---
colors:
  surface-page: "#FFFFFF"
  surface-raised: "#F9FAFB"
  surface-overlay: "#FFFFFF"
  text-primary: "#111827"
  text-secondary: "#6B7280"
  text-tertiary: "#9CA3AF"
  accent: "#3B82F6"
  accent-hover: "#2563EB"
  accent-active: "#1D4ED8"
  success: "#10B981"
  warning: "#F59E0B"
  error: "#EF4444"
  info: "#3B82F6"
  border-default: "#E5E7EB"
  border-subtle: "#F3F4F6"
typography:
  font-heading: "'[Font]', [fallbacks]"
  font-body: "'[Font]', [fallbacks]"
  scale-base: 16px
  scale-ratio: 1.25
spacing: [4, 8, 12, 16, 24, 32, 48, 64]
radius:
  sm: 6px
  md: 10px
  lg: 20px
  full: 9999px
---

# Design Authority

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
