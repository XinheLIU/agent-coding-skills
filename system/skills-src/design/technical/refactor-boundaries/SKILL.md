---
name: refactor-boundaries
description: Fix module boundary violations in existing codebases — break circular dependencies, extract interfaces, apply strangler fig pattern. Produces refactoring plan with sequenced steps and rollback points.
---

# Refactor Module Boundaries

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [design.structural_assessment]
  retrieves: [system.affected_source, system.invariants, design.relevant_decisions]
  produces: [design.refactoring_plan, design.migration_plan]
  updates: [design.module_contracts, design.accepted_decisions]
  invalidates: [change.implementation_plan, verification.affected_evidence]
  handoff_to: [design_modules, implementation]
```

## What this skill does

Redesigns module boundaries in existing codebases to fix tangled dependencies, circular imports, and leaky abstractions. Produces a step-by-step refactoring plan that breaks cycles, extracts interfaces, and enforces cleaner boundaries without rewriting from scratch.

## When to use

- `AUDIT.md` documents boundary violations (circular deps, hidden coupling)
- Modules are tangled and changes ripple unexpectedly
- User says: "fix these boundaries", "break the circular dependency", "untangle this mess"
- Multiple modules import from each other in cycles
- Implementation details leak across module boundaries

**Entry requirement:** `design/technical/audit-architecture` has run and produced `AUDIT.md` with documented boundary problems.

## What you'll produce

- `REFACTORING-PLAN.md` — step-by-step boundary changes with rollback points
- ADRs for new seams and interface contracts
- Updated `DESIGN.md` reflecting target architecture
- Migration sequence that preserves working state at each step

## How it works

### 1. Load the audit findings

Read `AUDIT.md` to understand:
- Which boundaries are violated
- Circular dependency chains
- Coupling hotspots
- Modules with too many responsibilities

Extract the boundary violations into a working list.

### 2. Identify seams

For each boundary violation, find the natural seam:

**Dependency inversion:** When A depends on B's concrete implementation, extract an interface that A owns and B implements.

**Strangler fig:** When two modules are too entangled to separate cleanly, introduce a new boundary layer that both depend on, then migrate incrementally.

**Interface extraction:** When implementation details leak, hide them behind a minimal interface that exposes only what callers actually need.

**Module split:** When one module handles multiple concerns, identify cohesive clusters and extract them as separate modules.

Document each seam decision in `REFACTORING-PLAN.md` with:
- Current state (what's coupled)
- Target state (new boundary)
- Why this seam (rationale)

### 3. Sequence the refactoring

Order the changes to minimize breakage:

1. **Bottom-up:** Start with modules that have no outgoing dependencies
2. **Break cycles first:** Tackle circular dependencies before other improvements
3. **One boundary at a time:** Don't change multiple boundaries simultaneously
4. **Preserve tests:** Ensure tests pass after each boundary change

For each step, specify:
- Files to change
- New interfaces/modules to create
- Order of operations (create interface, update callers, move impl)
- How to verify (which tests must still pass)
- Rollback procedure if the step fails

### 4. Document interface contracts

For each new boundary, write an ADR covering:
- What the interface exposes
- What it hides
- Who owns it (which module)
- Stability guarantee (how often can it change)
- Migration path from old to new

### 5. Update design docs

Update `DESIGN.md` to reflect:
- New module boundaries
- Dependency direction rules
- Interface ownership
- What each module is responsible for

## Example: Breaking a circular dependency

### Current state (from AUDIT.md)
```
orders → inventory (to check stock)
inventory → orders (to reserve items)
```

### Seam decision
Introduce `StockReservation` interface owned by `orders`:
```
orders → StockReservation interface
inventory → implements StockReservation
```

### Refactoring sequence

**Step 1:** Create `StockReservation` interface in `orders/` module
- Define methods: `checkAvailability(sku, qty)`, `reserve(sku, qty)`
- Write ADR explaining ownership and contract

**Step 2:** Make `inventory` implement `StockReservation`
- Implement interface without changing behavior
- Verify: existing inventory tests pass

**Step 3:** Update `orders` to depend on interface, not concrete `inventory`
- Change imports from `inventory.StockChecker` to `StockReservation`
- Verify: order placement tests pass

**Step 4:** Remove `inventory → orders` dependency
- Inventory no longer imports from orders
- Verify: all tests pass, circular dependency broken

**Rollback:** If Step 3 fails, revert to Step 2 state (interface exists but unused)

## Exit criteria

- `REFACTORING-PLAN.md` complete with sequenced steps
- Each boundary violation has a seam and refactoring sequence
- ADRs written for new interfaces
- `DESIGN.md` updated with target architecture
- All changes preserve existing test suite

## What this skill does NOT do

- Implement the refactoring (that's `build/incremental`)
- Rewrite modules from scratch (use `design/technical/harden-architecture` for greenfield)
- Fix bugs unrelated to boundaries
- Optimize performance

## Cross-references

- Upstream: `design/technical/audit-architecture` produces the audit
- Downstream: `build/incremental` implements the refactoring plan
- Related: `engineer-domain-model` if naming needs clarity
- Related: `split-module` if a module needs decomposition first

---

## Instructions for the agent

You are refactoring module boundaries in an existing codebase.

### Step 1: Load audit findings

Read `AUDIT.md` and extract:
- Circular dependency chains
- Boundary violations (who imports what)
- Coupling hotspots
- Modules doing too much

Confirm you understand the problems before proposing solutions.

### Step 2: Propose seams

For each boundary violation, identify the seam using these patterns:

**Dependency inversion:** Extract interface owned by the caller
**Strangler fig:** Introduce new boundary layer, migrate incrementally
**Interface extraction:** Hide implementation behind minimal API
**Module split:** Break module into cohesive pieces (defer to `split-module` if complex)

Document each seam with:
- Current coupling
- Target boundary
- Why this approach

### Step 3: Sequence the work

Order changes to preserve working state:
1. Bottom-up (leaves first)
2. Break cycles before other improvements
3. One boundary per change
4. Tests must pass after each step

For each step specify:
- What to change
- What to create
- Order of operations
- Verification (which tests)
- Rollback procedure

### Step 4: Write ADRs

For each new interface/boundary, write an ADR covering:
- What it exposes
- What it hides
- Who owns it
- Stability guarantee
- Migration approach

### Step 5: Update design docs

Update `DESIGN.md` with:
- New boundaries
- Dependency rules
- Interface ownership
- Module responsibilities

### Output format

Write `REFACTORING-PLAN.md`:

```markdown
# Refactoring Plan: [Module Boundary Improvements]

## Current Problems
- [List boundary violations from AUDIT.md]

## Target Architecture
- [Describe new boundaries]

## Seam Decisions

### Seam 1: [Name]
**Current:** [coupling description]
**Target:** [new boundary]
**Approach:** [pattern + rationale]

## Refactoring Sequence

### Step 1: [Description]
- Create: [files/interfaces]
- Change: [what gets updated]
- Verify: [which tests]
- Rollback: [if it fails]

### Step 2: ...

## Interface Contracts
[Link to ADRs]

## Updated Design
[Link to updated DESIGN.md sections]
```

### Quality checklist

Before finishing:
- [ ] Every boundary violation has a seam
- [ ] Sequence preserves working tests at each step
- [ ] Each step has clear verification and rollback
- [ ] ADRs explain interface ownership
- [ ] `DESIGN.md` reflects target architecture
- [ ] No step tries to change more than one boundary

### Boundaries

This skill plans the refactoring; `build/incremental` implements it. Do not write code here.

If a module needs to be split before boundaries can be fixed, defer to `split-module` first.

If the codebase has no `AUDIT.md`, tell the user to run `audit-architecture` first.
