# Context Management Refactoring Summary

Last updated: 2026-09-17

**Date:** 2026-08-25

## Problem Statement

The original three-layer structure had several issues:

1. **Not MECE** — Core layer (CONTEXT.md, ADRs) vs Human layer (docs/) both documented "WHY", creating overlap
2. **Human layer bloat** — 171KB of references including 9 templates and 8 playbooks (50+ KB of C4 docs alone)
3. **Wrong separation principle** — separated by lifetime (project vs effort) instead of question type (WHY vs WHAT/HOW)
4. **Double documentation risk** — encouraged maintaining both "docs state" and "code state" in parallel

## Solution Applied

### Simplified to 3 Clean Layers

| Layer | Documents | Principle |
|-------|-----------|-----------|
| **Human** (WHY only) | ADRs, CONTEXT.md, AGENTS.md (routing), PRDs | Decisions code cannot show |
| **Code Index** (WHAT/HOW, optional) | Generated index, module maps | Current state agents discover |
| **Working** (NOW) | state.md, progress.md, drafts | Ephemeral effort state |

### Key Changes

**Removed from Human layer:**
- `docs/ARCHITECTURE.md` — agents read code structure from code or index
- `docs/CONVENTIONS.md` — agents infer patterns from code
- `docs/TECH_DECISIONS.md` — merged into ADRs (only decisions with rationale)
- `docs/QUALITY.md` — too generic, belongs in team standards
- `docs/exec-plans/` — working memory handles backlog and debt

**Removed templates (8 of 9):**
- ✗ ARCHITECTURE.template.md
- ✗ CONVENTIONS.template.md
- ✗ TECH_DECISIONS.template.md
- ✗ QUALITY.template.md
- ✗ backlog.template.md
- ✗ tech-debt-tracker.template.md
- ✗ task.template.md
- ✗ spec.template.md
- ✓ AGENTS.template.md (kept — routing index only)

**Removed all playbooks (9 files, ~100KB):**
- ✗ c4-syntax.md (16KB)
- ✗ c4-anti-patterns.md (16KB)
- ✗ c4-advanced-patterns.md (18KB)
- ✗ entry-points-playbook.md
- ✗ module-deps-playbook.md
- ✗ external-deps-playbook.md
- ✗ data-model-playbook.md
- ✗ doc-types-playbook.md
- ✗ readme-template.md

**Added Matt Pocock's minimal formats:**
- ✓ ADR-FORMAT.md (2.7KB) — 1-3 sentence decisions
- ✓ CONTEXT-FORMAT.md (2.2KB) — tight terminology definitions

**Removed Phase 4 from acs-init-context:**
- No longer generates agent-behavior rules files
- Removed entire `rules/` directory (5 files, ~25KB)

### Results

**Before:**
- Size: 242KB
- Files: 41 files
- Templates: 9
- Playbooks: 9
- Principle: Separate by lifetime

**After:**
- Size: 128KB (47% reduction)
- Files: 14 markdown files + 4 symlinks
- Templates: 1 (AGENTS routing only)
- Playbooks: 0
- Principle: Separate by question type (WHY vs WHAT/HOW)

### Updated Skills

**acs-init-context:**
- Phase 0: Inspect (unchanged)
- Phase 1: Routing config and working memory (unchanged)
- Phase 2: Human-layer docs (WHY only) — simplified to AGENTS.md, README.md, CONTEXT.md (lazy), ADRs (lazy)
- Phase 3: Code index (unchanged)
- ~~Phase 4: Agent-behavior rules~~ (removed)

**acs-sync-context:**
- Job A: Human-layer routing (fast + full) — checks only WHY docs, flags WHAT/HOW docs for deletion
- Job B: Code index freshness (full only) — unchanged
- Job C: Working-memory maintenance (full only) — unchanged

### Benefits

1. **MECE achieved** — Human = WHY only, Code Index = WHAT/HOW, no overlap
2. **Lighter maintenance** — acs-sync-context checks routing + ADRs, not comprehensive docs
3. **Less drift** — agents derive WHAT/HOW from code, don't maintain parallel documentation
4. **Aligned with Matt's principle** — document decisions and constraints, not current state
5. **Faster setup** — acs-init-context creates 3 files instead of 7+
6. **Clearer contract** — "does this document a decision or describe current state?" determines the layer

## Migration Path

For existing repos using the old structure:

1. Run `/acs-sync-context --full` — it will flag ARCHITECTURE.md, CONVENTIONS.md, TECH_DECISIONS.md, QUALITY.md for deletion
2. Extract any unique rationale from those files into ADRs before deletion
3. Delete the flagged files
4. Agents will now read code structure directly instead of maintaining parallel docs

## Philosophy

**Human layer = WHY only.** If an agent can figure it out by reading code or querying an index, it doesn't belong in Human layer docs. Only document:
- Decisions that would surprise someone ("why did they do it this way?")
- Constraints that bind the project ("we can't use AWS because...")
- Terminology that must stay consistent ("we call this Order, not Purchase")
- Product intent that code cannot show ("we're building this because...")
