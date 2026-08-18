---
name: interaction-design
description: Design user flows, information architecture, and interaction states before visual design
category: Design · UX
triggers:
  - interaction design
  - user flow
  - wireframe
  - state design
  - UX flow
---

# Interaction Design

Design the **how users interact** before the **how it looks**. Define information architecture, user flows, and all interaction states (loading, empty, error, success, partial) through low-fidelity wireframes.

## When to Use

- Starting a new feature with unclear user flows
- Before visual design exploration (feeds into `/visual-design-variants`)
- When PRD Part 3 (Five-State Blocks) is incomplete
- Restructuring existing flows with UX issues

## What This Produces

**Working Layer** (`.scratch/<effort>/interaction/`):
- `wireframes/*.html` — Low-fidelity structure (gray boxes + labels, no colors/fonts)
- `state-table.md` — Five-state coverage table (LOADING/EMPTY/ERROR/SUCCESS/PARTIAL)
- `journey-map.md` — User journey with emotional arc
- `decisions.md` — Interaction decisions and rationale
- `architecture.md` — Information architecture (what user sees first/second/third)

## Workflow

### Step 0: Detect Context

Read existing artifacts:

```bash
# Detect PRD (canonical location first, legacy flat path as fallback)
PRD_PATH=$(find docs/product -name "prd.md" -type f 2>/dev/null | head -1)
if [ -z "$PRD_PATH" ] && [ -f "docs/prd.md" ]; then
  PRD_PATH="docs/prd.md"
fi
if [ -n "$PRD_PATH" ]; then
  echo "PRD found: $PRD_PATH"
fi

# Detect existing interaction designs
EFFORT_DIR=$(find .scratch -maxdepth 1 -type d -name "[0-9]*-*" 2>/dev/null | sort -r | head -1)
if [ -n "$EFFORT_DIR" ] && [ -d "$EFFORT_DIR/interaction" ]; then
  echo "Existing interaction design: $EFFORT_DIR/interaction"
fi

# Detect design system
if [ -f "docs/design/system.md" ]; then
  echo "Design system exists"
fi
```

**AskUserQuestion** if existing interaction design found:

> Found existing interaction design from [date]. 
>
> **A)** Review and iterate on existing design  
> **B)** Start fresh (archive old design)  
> **C)** Cancel — I'll handle this manually

If starting fresh, create effort directory:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
EFFORT_NAME="interaction-$(echo "$USER_TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | head -c 30)"
EFFORT_DIR=".scratch/${TIMESTAMP}-${EFFORT_NAME}"
mkdir -p "$EFFORT_DIR/interaction/wireframes"
```

### Step 1: Gather Product Context

Read from these sources (auto-gather, don't ask if present):

1. **PRD Part 1** (`$PRD_PATH` ## Part 1: Problem & Solution)
   - Who: target users, persona
   - What: product type, core value proposition
   - Platform: web app, mobile, dashboard, etc.

2. **PRD Part 3** (`$PRD_PATH` ## Part 3: Five-State Blocks)
   - Existing state definitions (if present)
   - This is what we'll expand/refine

3. **User Stories** (if separate from PRD)
   - Key user tasks
   - Entry/exit points

If PRD missing or incomplete, **AskUserQuestion** (single comprehensive question):

> I need context to design the interaction flows:
>
> 1. **Who are the users?** (role, expertise, context of use)
> 2. **What are they trying to do?** (1-3 core tasks)
> 3. **What type of interface?** (dashboard, form-heavy, data visualization, content-focused, etc.)
> 4. **Key user flows?** (e.g., "create project → invite team → deploy")
> 5. **Edge cases you're worried about?** (slow network, empty data, errors)

Record answers in `$EFFORT_DIR/interaction/context.md`.

### Step 1.5: External Knowledge Pass (optional, layer ②)

If a UX-knowledge skill is installed (see `design/ux/README.md` layer ② — design-guideline databases, design-specialist libraries), query it before filling the state table:

- **State-design guidelines** relevant to the feature list (loading/empty/error patterns for this product type)
- **Flow patterns** for the identified user tasks (onboarding, CRUD, search/filter, etc.)

Fold what you use into `decisions.md` with a citation line (`Source: <skill name>, <query>`). If no such skill is installed, skip silently — the five-state table below is self-sufficient.

### Step 2: Define Information Architecture

**Goal:** What does the user see first, second, third?

Generate ASCII diagram of screen structure:

```
+--------------------------------------------------+
| Header: [Brand] [Primary Nav] [User Actions]    |
+--------------------------------------------------+
| Sidebar (if needed)  | Main Content Area        |
|                      |                           |
| [Nav items]          | 1. PRIMARY: [Hero/Title] |
|                      | 2. SECONDARY: [Key Info] |
|                      | 3. TERTIARY: [Actions]   |
|                      |                           |
+--------------------------------------------------+
| Footer (if needed)                               |
+--------------------------------------------------+
```

**Navigation flow diagram:**

```
Landing → [Action A] → Screen 2 → [Action B] → Screen 3
             ↓                         ↓
          [Cancel] → Back          [Error] → Error State
```

**Apply "Constraint Worship":** If you can only show 3 things on first screen, which 3?

Write to `$EFFORT_DIR/interaction/architecture.md`:

```markdown
## Information Architecture

### Screen Hierarchy

[ASCII diagram]

### Navigation Flow

[Flow diagram with entry/exit points]

### Priority Hierarchy

**PRIMARY (must see immediately):**
- [Item 1]
- [Item 2]

**SECONDARY (important but not immediate):**
- [Item 3]

**TERTIARY (available but not prominent):**
- [Item 4]

### Constraint Worship

If forced to show only 3 elements: [which 3 and why]
```

**AskUserQuestion** to confirm architecture:

> Here's the information architecture I'm proposing:
>
> [Show ASCII diagram inline]
>
> **Primary hierarchy:** [list]  
> **Navigation flow:** [describe]
>
> **A)** Approved — continue to state design  
> **B)** Revise — [specify what to change]  
> **C)** Show wireframe first — I need to see it visually

If C chosen, generate low-fi HTML wireframe (gray boxes only) and show screenshot before continuing.

### Step 3: Design Interaction State Table

**CORE DELIVERABLE** — Every feature must define all 5 states.

**Read PRD Part 3** if exists. If complete, use it as foundation. If missing/incomplete, you'll fill gaps and **offer to write back to PRD Part 3**.

Create table structure:

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

**Identify features** from PRD/context. Common categories:
- Data lists/tables
- Forms/input flows
- Search/filter
- File uploads
- Real-time updates
- User-generated content sections

For EACH feature, fill the 5 states.

**AskUserQuestion** once per feature (NOT batched):

> **Feature: [Name]**
>
> Proposed states:
> - **LOADING:** [description]
> - **EMPTY:** [description]  
> - **ERROR:** [description]
> - **SUCCESS:** [description]
> - **PARTIAL:** [description]
>
> **A)** Approved  
> **B)** Revise [which state needs change]

Write completed table to `$EFFORT_DIR/interaction/state-table.md`.

**Sync with PRD Part 3:**

If PRD exists and Part 3 is incomplete, **AskUserQuestion**:

> The interaction state table is now complete. PRD Part 3 (Five-State Blocks) should match this.
>
> **A)** Update PRD Part 3 with these states (recommended)  
> **B)** Keep PRD and interaction design separate

If A: Write back to `$PRD_PATH` Part 3.

### Step 4: Map User Journey

Pick 2-3 **critical user flows** (the "happy paths" that define product value).

For each flow, create storyboard:

```markdown
## User Journey: [Flow Name]

| STEP | USER DOES | USER SEES | USER FEELS | DESIGN SUPPORTS |
|------|-----------|-----------|------------|-----------------|
| 1 | Lands on page | [Screen state] | Curious / Uncertain | Clear headline, obvious starting point |
| 2 | Clicks [Action] | [Transition + new state] | Confident / In control | Immediate feedback, progress indicator |
| 3 | Encounters [blocker] | [Error state] | Frustrated | Helpful error message, clear recovery |
| 4 | Completes [goal] | [Success state] | Accomplished | Success confirmation, next steps |

### Emotional Arc

- **5-second (visceral):** First impression — [what user feels]
- **5-minute (behavioral):** Task completion — [what user feels]  
- **5-year (reflective):** Long-term memory — [what user remembers]

### Critical Moments

Where does this flow succeed or fail?
- [Moment 1]: [why critical]
- [Moment 2]: [why critical]
```

Write to `$EFFORT_DIR/interaction/journey-map.md`.

**AskUserQuestion** to validate journeys:

> Mapped [N] critical user journeys. Key emotional moments:
>
> [Summarize 1-2 critical moments per journey]
>
> **A)** Accurate — continue to wireframes  
> **B)** Missing a critical flow — [describe]  
> **C)** Emotional arc is wrong — [correct]

### Step 5: Generate Low-Fidelity Wireframes

**Output:** HTML wireframes with **no visual styling** — structure only.

**Styling constraints (enforced):**
- Grayscale only: `#f5f5f5` (background), `#e0e0e0` (boxes), `#333` (text)
- System font: `-apple-system, system-ui`
- No colors except grays
- No shadows, gradients, decorative elements
- Boxes labeled with `[Component Type]` annotations
- All interactions shown as gray `<button>` elements with labels

**Generate one wireframe per key screen:**

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

Save to `$EFFORT_DIR/interaction/wireframes/[screen-name].html`.

Generate wireframes for:
1. Main screen (all 5 states)
2. Each critical flow screen
3. Mobile breakpoint version if responsive behavior differs significantly

**AskUserQuestion** after generating wireframes:

> Generated [N] wireframes. Opening in browser...
>
> [Open wireframes in browser or show paths]
>
> **A)** Structure approved — document decisions  
> **B)** Revise [which screen, what change]  
> **C)** Need to see visual mockups — skip to /visual-design-variants

### Step 6: Document Interaction Decisions

Record **why** you made each interaction choice:

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
- Visual design: [constraints for visual-design-variants]
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

Write to `$EFFORT_DIR/interaction/decisions.md`.

### Step 7: Identify Responsive & Accessibility Requirements

**Responsive behavior** (not just "stacks on mobile" — specific intentional changes):

```markdown
## Responsive Specifications

### Breakpoints

- **Desktop (1024px+):** [Layout description]
- **Tablet (768px - 1023px):** [What changes]  
- **Mobile (< 768px):** [What changes]

### Key Responsive Decisions

**Navigation:** [How nav pattern changes across breakpoints]

**Data tables:** [Horizontal scroll vs. card transformation vs. priority columns]

**Forms:** [Single column on mobile, stacked labels]

**Images/media:** [Scaling behavior, art direction changes]
```

**Accessibility requirements:**

```markdown
## Accessibility Specifications

### Keyboard Navigation

- Tab order: [Logical order description]
- Focus indicators: [All interactive elements must have visible focus ring]
- Escape key: [Closes modals/drawers]
- Arrow keys: [Navigation in lists/trees if applicable]

### Screen Reader Support

- Page landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`
- ARIA labels on icon-only buttons
- Live regions for dynamic updates (loading → success state changes)
- Error announcements

### Touch Targets

- Minimum 44×44px on all interactive elements
- Adequate spacing between adjacent buttons

### Color Contrast

- Body text: Minimum 4.5:1 contrast (WCAG AA)
- Large text (18pt+): Minimum 3:1
- Interactive elements: 3:1 against background

### Motion

- Respect `prefers-reduced-motion` for animations
- Loading indicators must work without animation
```

Write to `$EFFORT_DIR/interaction/responsive-a11y.md`.

### Step 8: Surface Unresolved Decisions

**Critical:** Flag ambiguities that will block implementation.

```markdown
## Unresolved Interaction Decisions

| DECISION NEEDED | IF DEFERRED, WHAT HAPPENS | RECOMMENDATION |
|-----------------|---------------------------|----------------|
| What does "partial success" state show when API returns 50% of data? | Engineer ships all-or-nothing (no partial state) | Define partial state now — show loaded data + "Loading more..." |
| Mobile nav: drawer or bottom sheet? | Engineer defaults to hamburger | Test with users OR pick drawer (more context visible) |
| Form validation: inline or on submit? | Engineer does on-submit only (poor UX) | Inline validation after blur, final check on submit |
```

For each unresolved decision, **AskUserQuestion** individually (NOT batched):

> **Decision: [Topic]**
>
> **Recommendation:** [Your suggestion]  
> **Why:** [Rationale]  
> **If we defer:** [What implementation does by default]
>
> **A)** [Accept recommendation]  
> **B)** [Alternative option]  
> **C)** Defer — document as TODO

Write final list to `$EFFORT_DIR/interaction/unresolved.md`.

### Step 9: Summary & Handoff

Generate completion summary:

```markdown
## Interaction Design — Complete

**Effort:** $EFFORT_DIR

**Artifacts Created:**
- ✅ Information architecture (`architecture.md`)
- ✅ Interaction state table (`state-table.md`)  
  - [N] features × 5 states = [N×5] states defined
- ✅ User journey maps (`journey-map.md`)  
  - [N] critical flows mapped
- ✅ Low-fidelity wireframes (`wireframes/*.html`)  
  - [N] screens
- ✅ Interaction decisions documented (`decisions.md`)
- ✅ Responsive & accessibility specs (`responsive-a11y.md`)
- ✅ Unresolved decisions: [N resolved, M deferred]

**PRD Integration:**
- [✅/❌] PRD Part 3 updated with five-state blocks

**Ready for Next Step:**
This interaction design is ready to feed into `/visual-design-variants`.
The wireframes define structure (what goes where), state table defines all UI states, journey maps define emotional flow. Visual design will add colors, typography, and visual polish WITHOUT changing interaction structure.

**Files to reference in next step:**
- `$EFFORT_DIR/interaction/wireframes/*.html` (structure baseline)
- `$EFFORT_DIR/interaction/state-table.md` (all states to visualize)
- `docs/design/system.md` (design tokens, if exists)
```

**AskUserQuestion** for next step:

> Interaction design complete. [N] features, [M] states, [P] flows defined.
>
> **Next step:**
>
> **A)** Run `/visual-design-variants` now (explore visual directions based on this structure)  
> **B)** Review interaction design first — I need to see it working  
> **C)** Update PRD/docs before continuing  
> **D)** Done — I'll handle next steps manually

## Quality Checklist

Before marking interaction design complete, verify:

- [ ] Every feature has all 5 states defined (no gaps in state table)
- [ ] Empty states include warmth (not just "No data")
- [ ] Error states include recovery actions (not just error messages)
- [ ] At least 2 critical user journeys mapped
- [ ] Wireframes show structure without visual styling
- [ ] Mobile behavior is intentional (not just "it stacks")
- [ ] Keyboard navigation patterns specified
- [ ] Touch targets meet 44px minimum
- [ ] Major interaction decisions documented with rationale

## Common Pitfalls

**Don't:**
- Add colors/fonts to wireframes — that's visual design's job
- Skip empty/error states — "we'll handle it later" = it gets forgotten
- Assume responsive = auto-stack — specify intentional mobile changes
- Defer "obvious" decisions — what's obvious to you isn't to the engineer

**Do:**
- Force yourself to fill every cell in the state table
- Show wireframes to user before locking structure
- Document WHY you made each interaction choice
- Think about keyboard users and screen readers upfront

## Integration with Other Skills

**Feeds into:**
- `/visual-design-variants` — uses wireframes as structure baseline
- `/design-implement` — uses state table to generate all states in code

**Reads from:**
- PRD Part 1 (user context)
- PRD Part 3 (five-state blocks, if exists)
- `docs/design/system.md` (constraints, if exists)
- External layer-② knowledge skills, when installed (state/flow guidelines — see `design/ux/README.md`)

**Writes to (optional):**
- PRD Part 3 — if user approves sync

## Files Created

```
.scratch/<timestamp>-<effort>/
  interaction/
    context.md              # User context gathered
    architecture.md         # Information architecture + nav flow
    state-table.md         # Five-state table (CORE DELIVERABLE)
    journey-map.md         # User journey storyboards
    wireframes/            # Low-fi HTML wireframes
      screen-1.html
      screen-2.html
      ...
    decisions.md           # Interaction decisions + rationale
    responsive-a11y.md     # Responsive & accessibility specs
    unresolved.md          # Deferred decisions (if any)
```

All files stay in Working layer (`.scratch/`) — they're exploration artifacts that feed into implementation but don't become project documentation themselves.

The state definitions MAY be promoted to PRD Part 3 (Human layer) if user approves sync.

---

**Last updated:** 2026-08-17
