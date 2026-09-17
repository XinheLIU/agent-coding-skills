# Output Examples

Last updated: 2026-09-17

Load only the example linked by the active step. These are templates, not additional sources of requirements or design authority.

## Example 1

Used by: Step 3: Generate Visual Variants. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

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

## Example 2

Used by: Step 6: Document Visual Decision. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

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

**Variant [X]:** [Why it didn't work]\
**Variant [Y]:** [Why it didn't work]

### Key Visual Decisions

**Decision 1:** [Specific choice, e.g., "Bold color on CTA vs subtle"]\
**Rationale:** [Why this serves user goals better]

**Decision 2:** [...]

### Implementation Notes

**For `/acs-design-implement`:**
- The styled section in the canonical prototype is ready to convert to production code
- All 5 states are defined and approved
- Structure is unchanged (section stayed locked)
- DESIGN.md tokens were followed

**Files:**
- Canonical: `docs/design/prototype.html` — section `[data-surface]` now at styled fidelity
- Source variants: `$EFFORT_DIR/visual/variants/*.html`
```
