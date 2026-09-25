# Tabbed Discovery Report Protocol

Last updated: 2026-09-25

Use this protocol for complex multi-dimensional analysis with real interactive tabs that hide inactive content. When the analysis has 3+ major concerns, substantial revision history, nested options, or before/after comparisons across multiple dimensions, a tabbed layout outperforms a flat card structure.

## When to use

**Use tabs for:**
- Architecture discovery with 4+ structural issues
- Design documents comparing 3+ materially different options
- Analysis with substantial revision history requiring context
- Multi-phase migrations with interdependent steps
- Before/after transformations across multiple layers

**Stay with cards for:**
- Simple findings (1-5 cards, single dimension)
- Linear progressions without nested structure
- Reports where everything fits comfortably in 2-3 viewport heights

## Three-tab baseline

Default structure: Problems → Design → Migration

```
┌──────────────────────────────────────┐
│ Metrics Card (header)                │
├──────────────────────────────────────┤
│ [Problems] [Design] [Migration]      │  ← Tab buttons
├──────────────────────────────────────┤
│                                      │
│  Active tab content                  │
│  (other tabs hidden)                 │
│                                      │
└──────────────────────────────────────┘
```

Adapt tab names to the domain:
- Technical refactoring: Current → Target → Path
- Product analysis: Gaps → Opportunities → Roadmap
- Architecture audit: Findings → Options → Decision

## Tab interface specification

### HTML structure

```html
<div class="tabs" role="tablist">
  <nav class="tab-nav">
    <button class="tab-btn active"
            role="tab"
            aria-selected="true"
            aria-controls="problems-panel"
            data-tab="problems">
      Problems
    </button>
    <button class="tab-btn"
            role="tab"
            aria-selected="false"
            aria-controls="design-panel"
            data-tab="design">
      Design
    </button>
    <button class="tab-btn"
            role="tab"
            aria-selected="false"
            aria-controls="migration-panel"
            data-tab="migration">
      Migration
    </button>
  </nav>

  <div class="tab-panel active"
       id="problems-panel"
       role="tabpanel"
       aria-labelledby="tab-problems">
    <!-- Problem cards -->
  </div>

  <div class="tab-panel"
       id="design-panel"
       role="tabpanel"
       aria-labelledby="tab-design"
       hidden>
    <!-- Design content, may contain nested sub-tabs -->
  </div>

  <div class="tab-panel"
       id="migration-panel"
       role="tabpanel"
       aria-labelledby="tab-migration"
       hidden>
    <!-- Migration timeline -->
  </div>
</div>
```

### Vanilla JS tab switching

Inline at the end of the document. No dependencies.

```javascript
(function() {
  'use strict';

  const tabs = document.querySelectorAll('.tab-btn');
  const panels = document.querySelectorAll('.tab-panel');

  function activateTab(targetId) {
    tabs.forEach(tab => {
      const isActive = tab.dataset.tab === targetId;
      tab.classList.toggle('active', isActive);
      tab.setAttribute('aria-selected', isActive);
    });

    panels.forEach(panel => {
      const isActive = panel.id === targetId + '-panel';
      panel.classList.toggle('active', isActive);
      panel.hidden = !isActive;
    });
  }

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      activateTab(tab.dataset.tab);
    });

    // Keyboard navigation
    tab.addEventListener('keydown', (e) => {
      const tabArray = Array.from(tabs);
      const currentIndex = tabArray.indexOf(tab);

      let targetIndex = currentIndex;
      if (e.key === 'ArrowRight') targetIndex = (currentIndex + 1) % tabs.length;
      if (e.key === 'ArrowLeft') targetIndex = (currentIndex - 1 + tabs.length) % tabs.length;
      if (e.key === 'Home') targetIndex = 0;
      if (e.key === 'End') targetIndex = tabs.length - 1;

      if (targetIndex !== currentIndex) {
        e.preventDefault();
        tabArray[targetIndex].focus();
        activateTab(tabArray[targetIndex].dataset.tab);
      }
    });
  });

  // Initialize: activate first tab
  if (tabs.length > 0) activateTab(tabs[0].dataset.tab);

  // Optional: URL hash navigation
  if (window.location.hash) {
    const hashTab = window.location.hash.slice(1);
    if (document.getElementById(hashTab + '-panel')) {
      activateTab(hashTab);
    }
  }
})();
```

## Component patterns

### Metrics card (header summary)

Place before tabs. Shows key numbers, status badges, top decision.

```html
<div class="metrics-card">
  <div class="metrics-row">
    <div class="metric">
      <div class="metric-value">193 → 60</div>
      <div class="metric-label">SKILL.md lines</div>
    </div>
    <div class="metric">
      <div class="metric-value">16 → 1</div>
      <div class="metric-label">Write paths</div>
    </div>
    <div class="metric">
      <div class="metric-value">3 / 4</div>
      <div class="metric-label">Layers affected</div>
    </div>
  </div>
  <div class="status-row">
    <span class="badge badge-problem">4 problems</span>
    <span class="badge badge-decided">3 decided</span>
    <span class="badge badge-pending">2 undecided</span>
  </div>
</div>
```

### Before/after comparison card

Each problem or refactoring delta gets one card.

```html
<div class="comparison-card">
  <h3>
    Problem 1: Schema Leak
    <span class="badge badge-high">High</span>
  </h3>

  <div class="comparison">
    <div class="before">
      <h4>Current ❌</h4>
      <svg class="diagram" width="280" height="160">
        <!-- Inline SVG showing architecture violation -->
      </svg>
      <pre><code>// 120 lines of schema in SKILL.md
statuses: [...]
projectNatures: [...]</code></pre>
      <p class="cost">Cost: Goes stale after migration, no type safety</p>
    </div>

    <div class="after">
      <h4>Target ✅</h4>
      <svg class="diagram" width="280" height="160">
        <!-- Inline SVG showing fixed architecture -->
      </svg>
      <pre><code>horizon schema describe --output json
// Returns live schema from server</code></pre>
      <p class="gain">Gain: Single source of truth, always current</p>
    </div>
  </div>

  <details class="evidence">
    <summary>Evidence (3 files affected)</summary>
    <ul>
      <li><code>project-manager/SKILL.md:45-165</code> — 120 lines of enumerated schema</li>
      <li><code>projectPlanCommands.ts</code> — validation duplicates schema</li>
      <li><code>worklogCommands.ts</code> — status checks hardcoded</li>
    </ul>
  </details>
</div>
```

Keep code snippets ≤ 5 lines. Full schemas belong in `<details>`.

### Diagram pattern guidance

**Mix diagram types** — don't make every card look the same. Pick the pattern that fits the content:

1. **Mermaid graph** (workhorse for dependencies/call flow) — use `flowchart` or `graph` when the point is "X calls Y calls Z, look at the mess." Style with `classDef` to color leakage edges red and deep modules dark. Sequence diagrams work for "before: 6 round-trips; after: 1."

2. **Hand-built boxes-and-arrows** (when Mermaid's layout fights you) — modules as `<div>`s with borders, arrows as inline SVG `<line>` or `<path>`. Use when you want one thick-bordered deep module with greyed-out internals.

3. **Cross-section** (good for layered shallowness) — stack horizontal bands to show layers. Before: 6 thin layers. After: 1 thick consolidated band.

4. **Mass diagram** (interface vs. implementation) — two rectangles per module. Before: interface nearly as tall as implementation (shallow). After: short interface, tall implementation (deep).

5. **Call-graph collapse** — before: tree of function calls as nested boxes. After: collapsed into one box with faded internals.

**Diagram style:** Keep ~320px tall so before/after sits side by side without scrolling. Use `text-xs uppercase tracking-wider` for labels inside diagrams — schematic, not UI.

### Decision history callout

For §7-style revisions. Shows how a decision evolved.

```html
<div class="decision-callout">
  <div class="decision-header">
    <span class="decision-icon">📍</span>
    <strong>Decision (2026-09-17):</strong> Single skill, not 4 separate skills
  </div>
  <div class="decision-body">
    <p><strong>Context:</strong> impeccable v3.0 merged 17 skills → 1. Same judgment criteria apply.</p>
    <details>
      <summary>Rationale (4 criteria matched)</summary>
      <ul>
        <li><strong>Description conflict:</strong> "what did I do last week" triggers both <code>report</code> and <code>worklog-entry</code></li>
        <li><strong>Implicit state handoff:</strong> <code>preview → fingerprint → apply</code> is a stale-able snapshot chain</li>
        <li><strong>Shared reference:</strong> <code>cli-contract.md</code> needed by all 4</li>
        <li><strong>Enumerable commands:</strong> <code>auth/context/report/plan/worklogs</code> fit Commands table</li>
      </ul>
    </details>
    <p class="timing">Timing: routing散文 currently in only 1 SKILL.md, not yet copied 20 times</p>
  </div>
</div>
```

Place decision callouts in the tab they affect. If a decision spans multiple concerns, duplicate the callout or use cross-tab anchor links.

### Nested sub-tabs

Use when one main tab has 4+ distinct options or layers.

```html
<div class="tab-panel" id="design-panel" role="tabpanel">
  <div class="sub-tabs">
    <nav class="sub-tab-nav" role="tablist">
      <button class="sub-tab-btn active"
              role="tab"
              data-subtab="cli-read">
        CLI Read
      </button>
      <button class="sub-tab-btn"
              role="tab"
              data-subtab="cli-write">
        CLI Write
      </button>
      <button class="sub-tab-btn"
              role="tab"
              data-subtab="skill">
        Skill Layer
      </button>
      <button class="sub-tab-btn"
              role="tab"
              data-subtab="harness">
        Harness
      </button>
    </nav>

    <div class="sub-tab-panel active" id="cli-read" role="tabpanel">
      <!-- CLI Read design content -->
    </div>
    <div class="sub-tab-panel" id="cli-write" role="tabpanel" hidden>
      <!-- CLI Write design content -->
    </div>
    <!-- ... other sub-panels -->
  </div>
</div>
```

Sub-tabs need their own JS initialization (same pattern as main tabs, scoped to `.sub-tab-btn` and `.sub-tab-panel`).

### Migration timeline

Visual sequence for migration tab.

```html
<div class="timeline">
  <div class="timeline-step">
    <div class="timeline-marker">1</div>
    <div class="timeline-content">
      <h4><code>schema describe</code> + strip enums from SKILL.md</h4>
      <p>Stops schema drift immediately. No server changes needed.</p>
      <span class="badge badge-ready">Ready</span>
    </div>
  </div>

  <div class="timeline-step">
    <div class="timeline-marker">2</div>
    <div class="timeline-content">
      <h4><code>report *</code> + purpose-specific server reads</h4>
      <p>Unlocks all read use cases. Can run parallel with step 3.</p>
      <span class="badge badge-blocked">Needs API</span>
    </div>
  </div>

  <!-- ... more steps -->
</div>
```

Or use a horizontal flow diagram with SVG arrows.

## Progressive disclosure

Three levels:
1. **Tab level** — Major concerns separated by tabs
2. **Card level** — One card per problem/option/finding
3. **Evidence level** — File paths, detailed rationale in `<details>`

Never duplicate content across levels. Evidence lives only at level 3.

## Design tokens

Match existing ACS visual-report.md tokens:

**Colors:**
- Base: `--bg`, `--fg`, `--mut` (muted text), `--line` (borders)
- Status: `--problem` (red), `--warn` (amber), `--ok` (emerald), `--neutral` (slate)
- Accent: `--acc` (indigo or orange, one only)
- Code: `--code` (slightly darker/lighter than base)
- **Use color sparingly:** one accent plus red for leakage/problems and amber for warnings

**Typography:**
- Body: `ui-sans-serif, -apple-system, system-ui, sans-serif`
- Code: `ui-monospace, SFMono-Regular, Menlo, monospace`
- Headings: same family, heavier weight (serif optional for editorial tone)
- Module labels inside diagrams: `text-xs uppercase tracking-wider` — schematic, not UI

**Spacing:**
- Generous whitespace: 1.5–2rem between cards
- Compact within cards: 0.5–0.75rem between elements
- Maximum width: 920px for prose, wider allowed for diagrams
- Keep diagrams ~320px tall so before/after sits side by side without scrolling

**Light/dark mode:**
Use CSS custom properties with `@media (prefers-color-scheme: dark)` override. Never fix colors in declarations.

**Editorial tone:**
Lean editorial, not corporate-dashboard. Generous whitespace. Stone/slate palette works well with serif headings for editorial feel.

## Accessibility

**ARIA labels:**
- Tab buttons: `role="tab"`, `aria-selected`, `aria-controls`
- Tab panels: `role="tabpanel"`, `aria-labelledby`, `hidden`
- Tab container: `role="tablist"`

**Keyboard navigation:**
- Tab focuses tab buttons
- Arrow keys switch tabs
- Home/End jump to first/last tab
- Enter/Space activate (implicit with button)

**Screen reader:**
- Announce "X of Y tabs" on focus
- Announce tab name and selected state
- Content inside inactive tabs truly hidden (not just `display:none`)

## Fallback behavior

When JavaScript is disabled or fails:
- All tab panels remain visible in document order
- Tab buttons become section headers or remain clickable (no-op)
- Progressive enhancement: base HTML is readable, JS adds interaction

Implement with `<noscript>` style override or initial state where all panels are visible.

## Portability

- Reference this file as `references/tabbed-discovery-report.md` (relative)
- Never require suite-level paths (`/authoring/...`)
- Never require another skill or external service
- Inline CSS and vanilla JS only
- Optional CDN dependencies (Mermaid, Tailwind) with graceful fallback

A packaged skill must include this reference and all templates it needs.

## Quality gates

- Every tab has at least one card or meaningful content
- Before/after comparisons show actual diagrams, not placeholder text
- Evidence is reachable but collapsed by default
- Diagram labels are legible without magnification
- Code snippets are syntax-highlighted (via `<code class="language-*">` + Prism/highlight.js, or plain monospace)
- Internal links resolve (anchors, tab switches)
- Mobile viewable: tabs stack or horizontal-scroll, content reflows

## Tone and phrasing

Plain, concise, evidence-first. No hedging, no throat-clearing, no "it's worth noting that...". If a sentence could be a bullet, make it a bullet. If a bullet could be cut, cut it.

**Problem/solution statements:** One sentence each. What hurts, what changes.

**Wins bullets:** Name the concrete gain in ≤6 words. Examples:
- "Tests hit one interface"
- "Schema leak eliminated"
- "Batch edits now expressible"
- "Delete 4 shallow wrappers"

Never write vague wins like "easier to maintain" or "cleaner code" — be specific about what improved.

**Cost/gain labels:** State the concrete impact:
- Cost: "Goes stale after migration, no type safety"
- Gain: "Single source of truth, always current"

Avoid "better", "improved", "enhanced" without saying what got better.

## Related contracts

- [visual-report.md](visual-report.md) — Card-based reports, inline SVG patterns
- [html-report.md](../../plan/acs-map-current-product/references/html-report.md) — Progressive disclosure for product mapping

Use tabbed-discovery-report.md when the structure requires hiding inactive sections. Use visual-report.md when all findings fit comfortably in one scrollable page.
