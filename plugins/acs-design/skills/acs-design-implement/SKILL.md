---
name: acs-design-implement
description: "Turn an approved visual design into production code in the project's own stack and conventions, with design tokens wired up, WCAG AA met, and the component documented in docs/design/components/. Requires a styled section in docs/design/prototype.html and DESIGN.md. Use to implement or build a design that is already settled, not to explore one."
---

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [change.requirements, design.accepted_prototype, design.applicable_rules]
  retrieves: [system.affected_source, design.relevant_decisions, operations.checks]
  produces: [change.implementation_evidence]
  updates: [source.components, design.component_records]
  invalidates: [verification.for_changed_code]
  handoff_to: [testing, code_review]
```

Shared semantics: [shared protocol](../../protocols/skill-declarations.md); shared execution: [Coordination](../../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


# Design Implementation

Convert approved design into production code that matches the project's tech stack.

## When to Use

- Design is approved (a `styled`, `locked` section exists in `docs/design/prototype.html`)
- Design authority is defined (`DESIGN.md` at project root)
- Ready to implement actual production code (not exploring options)
- User asks: "implement this design", "turn this into code", "build the component"

Do NOT use when:
- No design authority exists yet (run `/acs-design-context` or `/acs-design-system-create` first)
- Still exploring options (use `/acs-visual-design-variants`)
- The target section is still at `wireframe` fidelity (finish variant selection first)

## Inputs and Handoffs

**Upstream:**
- `docs/design/prototype.html` — the target section at `styled` fidelity, `data-structure="locked"`, all five state blocks (REQUIRED)
- `DESIGN.md` at project root (tokens/patterns — REQUIRED; legacy `docs/design/system.md` readable until migrated)
- `<work-root>/<effort>/interaction/state-table.md` (state semantics, when the effort is still live)
- Canonical change/spec/criterion IDs and accepted design/contract references with consumed revisions
- Project tech stack (auto-detected)

**Downstream:**
- Production component code in project's source directory
- `docs/design/components/<name>.md` (Current State component documentation with linked Change Context rationale)
- The prototype section marked `data-fidelity="implemented"` with `data-component` / `data-component-doc` pointers

## Workflow

### Step 0: Verify Prerequisites

Use the coordinator-resolved product/spec and relevant records. Preserve canonical requirement/criterion IDs and distinguish observed behavior from accepted intent.

Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

The coordinator supplies the configured work root and exact active effort; never select the newest directory as identity.

Then read the prototype and verify the target section: it must carry `data-fidelity="styled"` and `data-structure="locked"` with all five state blocks. 

If any prerequisite missing:
- STOP and report which is missing
- Guide user to run appropriate skill:
  - No prototype or section still at wireframe fidelity → run `/acs-visual-design-variants`
  - No section for this surface at all → run `/acs-design-interaction-flow`
  - No design authority → run `/acs-design-context` (or `/acs-design-system-create` for from-scratch)

### Step 1: Read Context

Read only the target prototype sections and their state blocks, applicable DESIGN.md rules, and linked accepted decisions/contracts with consumed revisions. Read relevant scratch state tables or draft notes only when they add unresolved context; accepted rationale must already have a durable reference and remain understandable after scratch cleanup.

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
Read [Example 1](references/output-examples.md#example-1) when producing this artifact.

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
Read [Example 2](references/output-examples.md#example-2) when producing this artifact.

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

Read [Example 3](references/output-examples.md#example-3) when producing this artifact.

Read [Example 4](references/output-examples.md#example-4) when producing this artifact.

Write the generated files to the target directory.

### Step 4.5: Polish Pass (optional)

Request an optional ③ method polish pass through the coordinator when it would improve craft, optical refinement, or accessibility. The built-in gates are the native fallback.

Three limits bound what a polish pass may change:

1. Visual values come from `DESIGN.md`. A polish pass may not introduce off-system colors or fonts.
2. Structure is locked. Anything requiring a layout, navigation, or state-transition change routes back to `/acs-design-interaction-flow` — it does not go into the code here.
3. Every applied fix gets one line in the component doc's `## Implementation Notes` (Step 6), naming what changed and why.

Done when the pass, if selected, satisfies these limits; return the outcome to the coordinator.

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

Read [Example 5](references/output-examples.md#example-5) when producing this artifact.

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
- `docs/design/components/[name].md` — Current State, component documentation

**Memory classification:**
- Component code → Project source (tracked by project's git rules)
- Component docs → Current State (git-tracked, outlives effort)
- Prototype section → Change Context, marked implemented with component pointers
- Working exploration (variants, drafts) → Run Context (can be archived or deleted after implementation)

Next steps:
- Component is ready to use in the project
- Refer to component docs for API and usage examples
- DESIGN.md remains source of truth for tokens; the prototype section for design intent

## Accepted decision handoff

At acceptance, retain consequential decision IDs, rationale, alternatives, affected surfaces/criteria, and consumed requirement/token/contract revisions beside the accepted design or in linked Change Context, following [the Design contract](../../protocols/design-memory.md). Do not wait for component documentation. Draft notes and rejected variant files may remain in Run Context after this reconciliation. Return accepted references, delta, unresolved questions/blocking effects, and next action to the coordinator.

## Shared Memory Contract

Full contract: [../../protocols/design-memory.md](../../protocols/design-memory.md).


Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

Durability test: the component doc yes — it carries the API, the states, and the reasons behind implementation choices that the code cannot show. The prototype section yes — it stays canonical intent, now with pointers to the code that realizes it. The working variants no; the merged section superseded them at approval.

After shipping, the shipped component is canonical **behavior** and the section canonical **intent**; when they diverge later, report the divergence — record the affected intent/behavior and route reassessment to Design. Reopen only for accepted design changes; do not maintain a synchronized second UI implementation.

A convention discovered while building — how this codebase handles compound components, where token overrides are permitted, what the focus-ring pattern is — binds the next contributor and does not belong in one component's doc. Route it to `docs/conventions` via `acs-sync-context`.

**Return the transition to the coordinator when the component lands** — component path, doc path, the implemented `data-surface` anchor, design stage complete. This is the pipeline's last stage, so the pointer closes it rather than naming a successor.

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
- `docs/design/components/<name>.md` (Current State documentation)
- `docs/design/prototype.html` (section markers: implemented + component pointers)
- Token files (styles/tokens.css or equivalent)

**Feeds:**
- Component docs feed `spec` (reference for implementation)
- Tokens feed all future component work (consistent styling)

**Optional polish pass:** an external craft, motion, or accessibility reviewer may run in Step 4.5 within the three limits stated there. The native quality gates run either way.
