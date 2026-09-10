---
name: interaction-design
description: "Decide how a feature behaves before deciding how it looks — information architecture, user flows, and the five interaction states (empty, loading, ideal, error, partial), locked as wireframe sections of the canonical prototype (docs/design/prototype.html). Requires product context; produces the structure that /visual-design-variants is forbidden to change. Use for UX flow, wireframe, state design, or interaction design work on a feature whose behavior is unsettled."
---

# Interaction Design

Last updated: 2026-09-09

## Context contract

```yaml
context:
  requires: [change.requirements]
  retrieves: [product.relevant_context, design.applicable_rules, design.relevant_decisions]
  produces: [design.interaction_contract]
  updates: [design.prototype_intent, design.accepted_decisions]
  invalidates: [design.visual_dependents, verification.interaction_evidence]
  handoff_to: [visual_design, product, implementation]
```

Shared semantics: [shared protocol](../../../craft/context/init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../../../workflows/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Design the **how users interact** before the **how it looks**. Define information architecture, user flows, and all interaction states (loading, empty, error, success, partial) through low-fidelity wireframes.

## When to Use

- Starting a new feature with unclear user flows
- Before visual design exploration (feeds into `/visual-design-variants`)
- When PRD Part 3 (Five-State Blocks) is incomplete
- Restructuring existing flows with UX issues

## Inputs and Handoffs

**Upstream (REQUIRED):**
- the configured product document (`product.html#prd`, or a canonical legacy PRD) Parts 1+3 — the **why**; each surface designed here links back to a capability or journey record

**Upstream (OPTIONAL):**
- `DESIGN.md` at project root (visual constraints, if it exists — this skill does not need it to design structure; legacy `docs/design/system.md` readable until migrated)
- `CONTEXT.md` (project constraints or terminology)
- `docs/design/prototype.html` (existing canonical prototype — the **what**; sections may be reopened here)

**Downstream:**
- `docs/design/prototype.html` — wireframe-fidelity sections, one per surface, all five states rendered, `data-structure="locked"` at approval (Change Context; the hard prerequisite of `/visual-design-variants`)
- Working exploration in `<work-root>/<effort>/interaction/`:
  - `context.md` — product context gathered in Step 1
  - `state-table.md` — five-state coverage analysis (LOADING / EMPTY / ERROR / SUCCESS / PARTIAL) that the prototype's state blocks render
  - `journey-map.md` — user journey with emotional arc
  - `architecture.md` — information architecture (what the user sees first, second, third)
  - `decisions.md` — interaction decisions and rationale
  - `responsive-a11y.md` — responsive and accessibility specifications
  - `unresolved.md` — deferred decisions, when any remain

The locked wireframe sections in the prototype are what `/visual-design-variants` styles; `state-table.md` remains the analysis `/design-implement` reads for state semantics.

## Workflow

### Step 0: Detect Context

Use the coordinator-resolved product/spec and relevant records. Preserve canonical requirement/criterion IDs and distinguish observed behavior from accepted intent.

Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

The coordinator supplies the configured work root and exact active effort; never select the newest directory as identity.

When the prototype exists, list its sections and their `data-surface` / `data-structure` / `data-fidelity` markers. A surface this effort touches that is `locked` must be explicitly reopened — that is a structure change, surfaced to the user, never silent.

**Ask through the coordinator** if existing interaction design found:

> Found existing interaction design from [date]. 
>
> **A)** Review and iterate on existing design  
> **B)** Start fresh (archive old design)  
> **C)** Cancel — I'll handle this manually

If starting fresh, create effort directory:

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
EFFORT_NAME="interaction-$(echo "$USER_TOPIC" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | head -c 30)"
EFFORT_DIR="$WORK_ROOT/${TIMESTAMP}-${EFFORT_NAME}"
mkdir -p "$EFFORT_DIR/interaction/wireframes"
```

### Step 1: Gather Product Context

Read from these sources (auto-gather, don't ask if present):

1. **PRD Part 1** (configured product document: linked persona/problem/scope records)
   - Who: target users, persona
   - What: product type, core value proposition
   - Platform: web app, mobile, dashboard, etc.

2. **PRD Part 3** (configured product document: linked capability/acceptance records)
   - Existing state definitions (if present)
   - This is what we'll expand/refine

3. **User Stories** (if separate from PRD)
   - Key user tasks
   - Entry/exit points

If PRD missing or incomplete, **Ask through the coordinator** (single comprehensive question):

> I need context to design the interaction flows:
>
> 1. **Who are the users?** (role, expertise, context of use)
> 2. **What are they trying to do?** (1-3 core tasks)
> 3. **What type of interface?** (dashboard, form-heavy, data visualization, content-focused, etc.)
> 4. **Key user flows?** (e.g., "create project → invite team → deploy")
> 5. **Edge cases you're worried about?** (slow network, empty data, errors)

Record answers in `$EFFORT_DIR/interaction/context.md`.

### Step 1.5: Consult Prior Art (optional)

Request optional ② knowledge for UX guidelines through the coordinator. Interpret relevant state/flow guidance and cite consulted sources in decision rationale. The five-state table remains native; absent an optional capability, continue directly.

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

**Ask through the coordinator** to confirm architecture:

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

**Read PRD Part 3** if exists. If complete, use it as foundation. If missing/incomplete, record the proposed interaction states and link the affected capability/question IDs for reconciliation via `write-prd`.

Create table structure:

Read [Example 1](references/output-examples.md#example-1) when producing this artifact.

**Identify features** from PRD/context. Common categories:
- Data lists/tables
- Forms/input flows
- Search/filter
- File uploads
- Real-time updates
- User-generated content sections

For EACH feature, fill the 5 states.

**Ask through the coordinator** once per feature (NOT batched):

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

If PRD exists and Part 3 is incomplete, **Ask through the coordinator**:

> The interaction state table is now complete. PRD Part 3 (Five-State Blocks) should match this.
>
> **A)** Update PRD Part 3 with these states (recommended)  
> **B)** Keep PRD and interaction design separate

If A: hand the accepted state-table changes and affected capability IDs to `write-prd` for minimal reconciliation into canonical records. Preserve unrelated requirements; do not create a second normative five-state copy.

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

**Ask through the coordinator** to validate journeys:

> Mapped [N] critical user journeys. Key emotional moments:
>
> [Summarize 1-2 critical moments per journey]
>
> **A)** Accurate — continue to wireframes  
> **B)** Missing a critical flow — [describe]  
> **C)** Emotional arc is wrong — [correct]

### Step 5: Generate Low-Fidelity Wireframe Sections

**Output:** wireframe-fidelity sections drafted for the canonical prototype — structure only, **no visual styling**.

Draft in the working layer first (`$EFFORT_DIR/interaction/wireframes/*.html`), one file per surface, so iteration stays cheap; they merge into `docs/design/prototype.html` only at the approval gate (Step 9).

**Styling constraints (enforced):**
- Grayscale only: `#f5f5f5` (background), `#e0e0e0` (boxes), `#333` (text)
- System font: `-apple-system, system-ui`
- No colors except grays
- No shadows, gradients, decorative elements
- Boxes labeled with `[Component Type]` annotations
- All interactions shown as gray `<button>` elements with labels

**Generate one wireframe per key screen:**

Read [Example 2](references/output-examples.md#example-2) when producing this artifact.

Save drafts to `$EFFORT_DIR/interaction/wireframes/[surface-slug].html`.

Each draft is one prototype `<section>` in the making. Give it its markers now so the merge is mechanical:

```html
<section data-surface="[surface-slug]"
         data-capability="[relative-path/product.html]#[record-id]"
         data-fidelity="wireframe" data-structure="open"
         data-updated="YYYY-MM-DD">
  <!-- structure + all five data-state blocks -->
</section>
```

The `data-capability` link is mandatory — a surface that serves no capability or journey record is scope nobody asked for; raise it rather than inventing the link. Render all five states from the state table as `data-state` blocks inside the section.

Generate wireframes for:
1. Main screen (all 5 states)
2. Each critical flow screen
3. Mobile breakpoint version if responsive behavior differs significantly

**Ask through the coordinator** after generating wireframes:

> Generated [N] wireframes. Opening in browser...
>
> [Open wireframes in browser or show paths]
>
> **A)** Structure approved — document decisions  
> **B)** Revise [which screen, what change]  
> **C)** Need to see visual mockups — skip to /visual-design-variants

### Step 6: Document Interaction Decisions

Record **why** you made each interaction choice:

Read [Example 3](references/output-examples.md#example-3) when producing this artifact.

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

For each unresolved decision, **Ask through the coordinator** individually (NOT batched):

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

**Merge into the canonical prototype.** On structure approval, merge each approved wireframe section into `docs/design/prototype.html`, setting `data-structure="locked"`:

- Create the file from scratch when absent: self-contained HTML, no build step, one shared keyboard-accessible state switcher driving the `data-state` blocks, and a `:root` block — grayscale wireframe values now, `DESIGN.md` tokens synced in later by `/design-context` or applied by `/visual-design-variants`.
- A section whose `data-surface` already exists is updated in place, preserving the slug; new surfaces append. Never touch sections this effort did not reopen.
- Reopened sections that were `styled` or `implemented` drop back to `wireframe` fidelity — their old visuals are stale against new structure. Say so in the summary.

Generate completion summary:

```markdown
## Interaction Design — Complete

**Effort:** $EFFORT_DIR

**Canonical prototype:** docs/design/prototype.html
- [N] surfaces at wireframe fidelity, structure LOCKED
- Each linked to its capability record (data-capability)
- All 5 states rendered per surface, switchable

**Working exploration:**
- ✅ Information architecture (`architecture.md`)
- ✅ Interaction state table (`state-table.md`) — [N] features × 5 states
- ✅ User journey maps (`journey-map.md`) — [N] critical flows
- ✅ Interaction decisions documented (`decisions.md`)
- ✅ Responsive & accessibility specs (`responsive-a11y.md`)
- ✅ Unresolved decisions: [N resolved, M deferred]

**PRD Integration:**
- [✅/❌] Accepted state definitions handed to write-prd

**Ready for Next Step:**
Structure is locked in the canonical prototype. `/visual-design-variants` will
style the locked sections — colors, typography, polish — WITHOUT changing them.
```

**Ask through the coordinator** for next step:

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
- [ ] Every prototype section renders all 5 states and links a capability record
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
- `/visual-design-variants` — styles the locked wireframe sections in the canonical prototype
- `/design-implement` — uses state table to generate all states in code

**Reads from:**
- PRD Part 1 (user context)
- PRD Part 3 (five-state blocks, if exists)
- `DESIGN.md` (constraints, if exists)

**Writes to (optional):**
- Product capability/acceptance records — via `write-prd` when sync is authorized

## Files Created

```
docs/design/prototype.html      # Canonical prototype — wireframe sections, locked at approval

<work-root>/<effort>/
  interaction/
    context.md              # User context gathered
    architecture.md         # Information architecture + nav flow
    state-table.md         # Five-state analysis rendered by the prototype's state blocks
    journey-map.md         # User journey storyboards
    wireframes/            # Section drafts, merged into the prototype at approval
      surface-1.html
      surface-2.html
      ...
    decisions.md           # Interaction decisions + rationale
    responsive-a11y.md     # Responsive & accessibility specs
    unresolved.md          # Deferred decisions (if any)
```

## Accepted decision handoff

At acceptance, retain consequential decision IDs, rationale, alternatives, affected surfaces/criteria, and consumed requirement/token/contract revisions beside the accepted design or in linked Change Context, following [the Design contract](references/design-memory.md). Do not wait for component documentation. Draft notes and rejected variant files may remain in Run Context after this reconciliation. Return accepted references, delta, unresolved questions/blocking effects, and next action to the coordinator.

## Shared Memory Contract

Full contract: [references/design-memory.md](references/design-memory.md).


Use coordinator-supplied paths and the active change identity; do not repeat path discovery.

Durability test: the locked sections yes — they are the structure every later pass styles and implements, so they merge into the prototype. The five-state definitions yes — they are acceptance criteria someone will re-derive otherwise, so they promote to capability records. The journey maps and working drafts no; they were the argument.

When sync is authorized, `write-prd` promotes accepted state definitions into canonical capability records and replaces the working definitions with links. Alternatives that were considered and rejected stay in working memory and are discarded with it.

**Return the transition to the coordinator at the approval gate** — structure locked, the `data-surface` anchors touched, next stage `/visual-design-variants`. That pointer is what lets the next stage start without re-reading everything here.
