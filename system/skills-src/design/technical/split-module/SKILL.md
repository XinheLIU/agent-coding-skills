---
name: split-module
description: Decompose monolithic modules by cohesion analysis — identify clusters, sequence extraction, preserve working state. Use when modules exceed 5k LOC or handle too many concerns.
---

# Split Module

Last updated: 2026-09-13

## Context contract

```yaml
context:
  requires: [system.affected_source]
  retrieves: [design.structural_assessment, system.invariants, design.relevant_decisions]
  produces: [design.extraction_plan, design.migration_plan]
  updates: [design.module_contracts]
  invalidates: [change.implementation_plan, verification.affected_evidence]
  handoff_to: [design_modules, implementation]
```

## What this skill does

Decomposes a monolithic module or service into smaller, cohesive pieces. Produces an extraction plan that identifies what to split, where boundaries should go, and how to migrate incrementally without breaking existing callers.

## When to use

- Module exceeds 5k LOC or has 20+ exports
- `AUDIT.md` flags module as "god object", "too shallow", or "low cohesion"
- User says: "split this module", "break apart the monolith", "this is doing too much"
- Single module handles multiple unrelated concerns
- Changes to one feature require touching many unrelated functions

**Entry requirement:** Module exists and is demonstrably doing too much (large, many exports, or flagged by audit).

## What you'll produce

- `SPLIT-PLAN.md` — extraction sequence with rollback points
- Interface contracts for new modules
- Module responsibility assignments
- Migration runbook for callers

## How it works

### 1. Analyze cohesion

Read the target module and identify clusters:

**Feature clusters:** Functions/classes that serve one feature
**Layer clusters:** Functions at same abstraction level (e.g., all DB access)
**Domain clusters:** Code related to one domain concept

Use these signals:
- Functions that call each other frequently belong together
- Functions that share data structures belong together
- Functions with similar import lists belong together
- Functions that change together belong together

Document each cluster with:
- What it's responsible for
- Which functions/classes belong
- Why they're cohesive

### 2. Choose split strategy

Pick the strategy that best matches the cohesion analysis:

**By feature:** Extract one feature as a new module (e.g., `user-profile` from `user`)
**By layer:** Extract infrastructure layer (e.g., `user-db` from `user`)
**By bounded context:** Extract a domain subdomain (e.g., `billing` from `orders`)

For each proposed module, define:
- Module name
- Responsibility (one sentence)
- What gets extracted (functions, classes, types)
- Public interface (what it exports)
- Dependencies (what it imports)

### 3. Sequence the extraction

Order the splits to minimize disruption:

1. **Extract leaves first:** Modules with fewest callers
2. **One extraction at a time:** Don't split multiple things simultaneously
3. **Preserve facade:** Keep old module working during migration
4. **Migrate callers incrementally:** Don't force big-bang updates

For each extraction:
- Create new module
- Move code (copy first, then delete once working)
- Update imports in original module to re-export from new module (facade pattern)
- Migrate callers one by one
- Remove facade once all callers migrated
- Specify rollback point

### 4. Define interface contracts

For each new module, specify:
- Public exports (what callers can depend on)
- Private internals (what they cannot)
- Stability guarantee (can interface change?)
- Migration deadline (when does facade disappear?)

Write this as comments in the new module or as ADRs.

### 5. Write migration runbook

Document for each caller:
- Old import: `from bigmodule import foo`
- New import: `from newmodule import foo`
- When to migrate (immediately or wait for facade removal)
- Breaking changes (if any)

## Example: Splitting user module by layer

### Current state
```
user/
  __init__.py (50 exports)
  models.py
  db.py
  api.py
  validation.py
  auth.py
```

### Cohesion analysis

**Cluster 1 - Data access:** `db.py` + DB-related functions
**Cluster 2 - Business logic:** `models.py`, `validation.py`
**Cluster 3 - Infrastructure:** `auth.py`

### Split strategy: By layer

Extract `user-db` module containing data access layer.

### Extraction sequence

**Step 1:** Create `user-db/` module
- Move `db.py` → `user-db/db.py`
- Define interface: `get_user()`, `save_user()`, `delete_user()`
- Test: ensure DB functions work in isolation

**Step 2:** Update `user/` to re-export from `user-db`
```python
# user/__init__.py
from user_db import get_user, save_user, delete_user
```
- Verify: existing callers still work (facade pattern)

**Step 3:** Migrate callers incrementally
- Update high-traffic paths: `from user_db import get_user`
- Update low-traffic paths after high-traffic validated
- Monitor: no breakage

**Step 4:** Remove facade
- Delete re-exports from `user/__init__.py`
- Verify: all callers migrated, no imports from old location

**Rollback:** If Step 3 fails, revert to Step 2 (facade still works)

## Exit criteria

- `SPLIT-PLAN.md` complete with extraction sequence
- Each new module has clear responsibility and interface
- Migration path preserves existing callers
- Rollback points identified
- All changes keep tests passing

## What this skill does NOT do

- Implement the split (that's `build/incremental`)
- Fix bugs in the module
- Refactor without splitting
- Optimize performance

## Cross-references

- Upstream: `design/technical/audit-architecture` identifies modules to split
- Downstream: `build/incremental` implements the extraction
- Related: `refactor-boundaries` if the split reveals boundary issues
- Related: `engineer-domain-model` if naming needs clarity

---

## Instructions for the agent

You are splitting a monolithic module into smaller cohesive pieces.

### Step 1: Analyze cohesion

Read the target module and identify clusters by:
- Which functions call each other
- Which functions share data structures
- Which functions have similar imports
- Which functions change together for the same features

Group into clusters and name each cluster by its responsibility.

### Step 2: Choose split strategy

Pick the best strategy:
- **By feature:** Extract one feature as new module
- **By layer:** Extract data/API/validation layer
- **By domain:** Extract subdomain concept

For each proposed new module, specify:
- Name
- Responsibility (one sentence)
- What gets extracted
- Public interface
- Dependencies

### Step 3: Sequence the extraction

Order extractions:
1. Leaves first (fewest callers)
2. One at a time
3. Preserve facade during migration
4. Migrate callers incrementally

For each extraction specify:
- Create new module (what moves)
- Update old module (re-export facade)
- Migrate callers (which ones, in what order)
- Remove facade (when safe)
- Rollback point

### Step 4: Define interfaces

For each new module document:
- Public exports
- Private internals
- Stability guarantee
- Migration deadline

### Step 5: Write migration runbook

For each caller:
- Old import statement
- New import statement
- When to migrate
- Breaking changes (if any)

### Output format

Write `SPLIT-PLAN.md`:

```markdown
# Split Plan: [Module Name]

## Current State
- LOC: [count]
- Exports: [count]
- Problems: [why splitting]

## Cohesion Analysis

### Cluster 1: [Name]
**Responsibility:** [one sentence]
**Contains:** [functions/classes]
**Why cohesive:** [rationale]

### Cluster 2: ...

## Split Strategy

### New Module: [name]
**Responsibility:** [one sentence]
**Extracted from:** [source module]
**Contains:** [what moves]
**Interface:** [public exports]
**Dependencies:** [imports]

## Extraction Sequence

### Step 1: Create [new-module]
- Move: [what]
- Interface: [exports]
- Verify: [tests]

### Step 2: Preserve facade in [old-module]
- Re-export: [what]
- Verify: [existing callers work]

### Step 3: Migrate callers
- High-traffic: [which files]
- Low-traffic: [which files]
- Monitor: [no breakage]

### Step 4: Remove facade
- Delete: [re-exports]
- Verify: [all migrated]

**Rollback:** [where to revert if failure]

## Interface Contracts

### [module-name]
- Public: [exports]
- Private: [internals]
- Stability: [can it change?]
- Deadline: [facade removal date]

## Migration Runbook

| Caller | Old Import | New Import | When |
|--------|-----------|------------|------|
| [file] | [old] | [new] | [immediately/later] |
```

### Quality checklist

Before finishing:
- [ ] Each cluster has clear responsibility
- [ ] Split strategy matches cohesion analysis
- [ ] Extraction preserves working state at each step
- [ ] Facade pattern allows incremental migration
- [ ] Interface contracts define public/private boundary
- [ ] Rollback points identified
- [ ] Migration runbook covers all callers

### Boundaries

This skill plans the split; `build/incremental` implements it. Do not write code here.

If the module has boundary violations with other modules, fix those with `refactor-boundaries` after splitting.

If the module is <2k LOC or has <10 exports, question whether splitting is necessary. Splitting creates coordination overhead.
