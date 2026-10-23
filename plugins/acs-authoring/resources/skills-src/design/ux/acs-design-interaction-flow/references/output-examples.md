# Output Examples

Last updated: 2026-09-17

Load only the example linked by the active step. These are templates, not additional sources of requirements or design authority.

## Example 1

Used by: Step 3: Design Interaction State Table. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

```markdown
## Interaction State Table

For each user-facing feature, specify what the user **SEES** (not backend behavior).

| FEATURE | LOADING | EMPTY | ERROR | SUCCESS | PARTIAL |
|---------|---------|-------|-------|---------|---------|
| [Feature 1] | [Skeleton UI with pulse animation] | [Warm empty state: icon, message, primary action] | [Error icon, specific message, retry button, support link] | [Full data display] | [Partial data + "Loading more..." indicator] |
| [Feature 2] | ... | ... | ... | ... | ... |

### State Design Guidelines

**LOADING:**
- Show skeleton UI matching success layout
- Never generic spinner alone — show structure
- Indicate progress if measurable

**EMPTY:**
- Warmth required — not just "No items"
- Explain why empty
- Provide primary action (e.g., "Create your first project")
- Optional: onboarding context

**ERROR:**
- Specific error message (not "Something went wrong")
- What happened, why it might have happened
- Clear recovery action (Retry, Contact Support, etc.)
- Preserve user's unsaved work when possible

**SUCCESS:**
- Full data display
- All interactions enabled
- Clear next actions

**PARTIAL:**
- Mixed state — some data loaded, some still loading
- OR degraded mode — core function works, secondary features unavailable
- Clear indication of what's missing and why
```

## Example 2

Used by: Step 5: Generate Low-Fidelity Wireframe Sections. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

```html
<!DOCTYPE html>
<html>
<head>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: -apple-system, system-ui, sans-serif;
  background: #f5f5f5;
  color: #333;
  padding: 20px;
}
.wireframe-label {
  background: #ffeb3b;
  padding: 2px 6px;
  font-size: 11px;
  text-transform: uppercase;
  font-weight: bold;
}
.box {
  background: white;
  border: 2px solid #e0e0e0;
  padding: 20px;
  margin: 10px 0;
}
button {
  background: #e0e0e0;
  border: 2px solid #999;
  padding: 10px 20px;
  font-family: inherit;
  cursor: pointer;
}
</style>
</head>
<body>
<span class="wireframe-label">Wireframe: [Screen Name]</span>

<!-- Structure here -->
<div class="box">
  <h1>[PRIMARY HEADLINE]</h1>
  <p>[Supporting text - 1-2 sentences]</p>
  <button>[PRIMARY ACTION]</button>
</div>

<!-- Show all 5 states if applicable -->
<h2>State: LOADING</h2>
<div class="box">
  [Skeleton structure]
</div>

<h2>State: EMPTY</h2>
<div class="box">
  [Empty state structure]
</div>

<!-- etc -->

</body>
</html>
```

## Example 3

Used by: Step 6: Document Interaction Decisions. Adapt to the active scope; the skill and shared domain contract govern authority and lifecycle.

```markdown
## Interaction Decisions

### Decision 1: [Topic]

**What we decided:** [Specific choice]

**Why:** [Rationale — user need, constraint, best practice]

**Alternatives considered:**
- Option A: [why rejected]
- Option B: [why rejected]

**Implications:**
- Engineering: [what this means for implementation]
- Visual design: [constraints for acs-visual-design-variants]
- Accessibility: [a11y requirements]

---

### Decision 2: Mobile Navigation Pattern

**What we decided:** Collapsible sidebar (slide-in drawer)

**Why:** Primary nav has 6 items — too many for bottom tabs, hamburger hides context

**Alternatives considered:**
- Bottom tabs: Rejected — only fits 5 items, our 6th is important
- Hamburger: Rejected — users need to see nav context while working

**Implications:**
- Engineering: Need drawer component with gesture support
- Visual design: Drawer must be visually distinct from main content
- Accessibility: Focus trap when open, Escape to close, ARIA labels

---

[Continue for each major decision]
```
