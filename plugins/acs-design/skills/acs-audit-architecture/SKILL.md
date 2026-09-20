---
name: acs-audit-architecture
description: Reconstruct current module boundaries, dependencies, coupling, and compatibility constraints before brownfield design. Use when the existing structure or runtime path cannot be established cheaply; use acs-review-architecture for holistic architecture judgment.
---

# Audit Architecture

Last updated: 2026-09-17

Read [the visual report contract](references/visual-report.md) and [the HTML report format](references/HTML-REPORT.md) before generating the companion. For complex multi-dimensional analysis with substantial findings across multiple architectural concerns, reference `craft/meta/references/tabbed-discovery-report.md` for the tabbed HTML output protocol. These local references are bundled with the skill; do not depend on `/meta` or another installed skill.

## Context contract

```yaml
context:
  requires: [system.affected_source]
  retrieves: [system.invariants, design.relevant_decisions, verification.failure_history]
  produces: [design.structural_assessment]
  updates: []
  invalidates: [design.disproved_assumptions]
  handoff_to: [design_architecture, design_modules]
```

Shared semantics: [shared protocol](../../protocols/skill-declarations.md); shared execution: [Coordination](../../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.

## What this skill does

Comprehensive architectural assessment of existing codebases. Identifies boundary violations, coupling hotspots, shallow modules, cohesion problems, and technical debt. Produces `AUDIT.md` that feeds refactoring and redesign work.

**Expanded scope:** This skill now serves as the Phase 0 entry point for all brownfield work — not just component extraction, but module splits, boundary refactoring, and architectural cleanup.

## When to use

- Existing codebase needs structural improvement
- User says: "this is messy", "code is tangled", "hard to change", "tech debt", "needs refactoring"
- Before starting brownfield refactoring
- After 2-3 features have stabilized patterns (component extraction mode)
- Module boundaries unclear or violated
- Changes ripple unexpectedly across the codebase

## What you’ll produce

- `AUDIT.md` — structural findings ranked by impact, with evidence
- Dependency graph highlighting violations
- Module boundary violations (circular deps, hidden coupling, leaky abstractions)
- Cohesion analysis (modules doing too much, scattered concerns)
- Shallow module identification (high interface complexity, low implementation value)
- Deepening opportunities (where to hide complexity)
- Extraction/split/merge recommendations with rationale
- Priority ranking (what to fix first)

## How it works

Read memory routing, domain context, ADRs, and existing `DESIGN.md` or `CONTEXT.md` if present. Scope the survey to the user’s target or recent hot spots (use git history and change frequency).

For deep analysis, dispatch one architecture-explorer sub-agent with the scoped paths and evidence requirements, then consolidate its findings inline when delegation is unavailable. Preserve file/line anchors and state the fallback explicitly.

### Assess module boundaries

**Circular dependencies:** Map import chains that form cycles
**Hidden coupling:** Modules that should be independent but share mutable state
**Leaky abstractions:** Implementation details exposed across boundaries
**Wrong seams:** Boundaries that don’t match actual concerns

For each violation, document:
- Which modules are involved
- How they’re coupled
- Why it’s problematic
- Proposed fix direction (defer details to `acs-design-modules`)

### Analyze cohesion

**God objects:** Modules doing too many unrelated things
**Feature envy:** Functions that primarily use data from another module
**Scattered concerns:** Related functionality split across unrelated modules
**Inappropriate intimacy:** Modules too familiar with each other’s internals

For each cohesion problem, document:
- Which module or cluster is involved
- What concerns are mixed or scattered
- Impact on changeability
- Proposed split or merge (defer details to `acs-design-modules`)

### Identify shallow modules

Use the deep modules heuristic:
- **Shallow:** High interface complexity (many params, many methods) with low implementation value
- **Deep:** Simple interface hiding significant complexity

Apply the deletion test: "If we removed this abstraction, how much simpler would callers be vs. how much complexity would they absorb?"

For each shallow module, document:
- Interface complexity (method count, parameter count, conceptual surface area)
- Implementation value (what complexity does it actually hide?)
- Proposed deepening (combine with related modules, simplify interface, or delete)

### Map technical debt

**Change amplification:** Simple features requiring changes to 10+ files
**Cognitive load:** Modules hard to understand even after reading
**Test brittleness:** Tests coupled to implementation details, not behavior
**Navigation friction:** Hard to find where features live

For each debt item, document:
- Symptom (what’s hard)
- Root cause (why it’s hard)
- Impact (how often does it hurt)
- Fix difficulty (easy/medium/hard)

### Rank findings

Priority = Impact × Frequency / Fix Difficulty

High priority:
- Boundary violations on hot paths (changed frequently)
- God objects blocking multiple features
- Shallow modules with high cognitive load

Low priority:
- Violations in stable code (rarely changed)
- Aesthetic issues with no change impact
- Premature abstractions that could just be deleted

### Output format

Write canonical `docs/architecture/reviews/AUDIT.md`:

```markdown
# Architecture Audit: [Codebase Name]

## Summary
[High-level findings — 3-5 key problems]

## Boundary Violations

### Circular Dependency: [module-a ↔ module-b]
**Problem:** [description]
**Evidence:** [import chains, file paths]
**Impact:** Changes to A require understanding B and vice versa
**Priority:** High/Medium/Low
**Recommended fix:** [direction only — defer to acs-design-modules]

## Cohesion Problems

### God Object: [module-name]
**Problem:** Handles [list unrelated concerns]
**Evidence:** [LOC count, export count, responsibility list]
**Impact:** Every feature touches this module
**Priority:** High/Medium/Low
**Recommended fix:** [direction only — defer to acs-design-modules]

## Shallow Modules

### [module-name]
**Interface complexity:** [method count, parameter counts]
**Implementation value:** [what complexity does it hide?]
**Deletion test:** Removing it would [simplify/complicate] callers
**Priority:** High/Medium/Low
**Recommended fix:** [deepen, merge, or delete]

## Technical Debt

### Change Amplification: [feature-type]
**Symptom:** Simple changes touch 10+ files
**Root cause:** [why scattered]
**Frequency:** [how often]
**Fix difficulty:** Medium
**Priority:** High

## Recommendations (Ranked)

1. **[Fix type]** — [module/area] — Priority: High — Feeds: [acs-design-architecture/design-modules]
2. [...]
```

Generate `AUDIT.html` using the local visual report contract and HTML format. Render one card per ranked finding with a current/target visual, concise problem and fix direction, wins, collapsed evidence, source link, and generation time. Use inline SVG first and Mermaid only for graph-shaped relationships. Keep `AUDIT.md` evidence-rich and the HTML concise; do not turn the companion into a roadmap.

### Handoff

Present the ranked recommendations. Ask which area to tackle first.

Route the selected work to `acs-design-architecture` when the target system shape is unsettled, or to `acs-design-modules` when the target is selected and needs boundary, cohesion, interface, or migration contracts. Use `acs-engineer-domain-model` when shared terminology is the blocking issue.

Do not refactor during the audit. This skill assesses; other skills fix.

## Exit criteria

- `AUDIT.md` complete with evidence-based findings
- All boundary violations documented
- Cohesion problems identified
- Shallow modules assessed with deletion test
- Technical debt mapped to root causes
- Findings ranked by priority
- Handoff routing clear (which skill handles which finding)

## Boundaries

This skill surveys; it does not fix. Design changes belong in `acs-design-architecture` or `acs-design-modules`; implementation belongs in `build/acs-implement`.

If the codebase is greenfield (no existing structure to assess), use `acs-design-architecture` instead.

If specific functionality is unclear, defer to `acs-engineer-domain-model` for domain modeling.

## Cross-references

- Downstream: `acs-design-architecture` (select the target system shape)
- Downstream: `acs-design-modules` (design boundaries, splits, interfaces, and migration)
- Downstream: `acs-engineer-domain-model` (resolve naming issues)
- Related: `acs-challenge-approach` (stress-test proposed changes)
