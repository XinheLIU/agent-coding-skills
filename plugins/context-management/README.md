# Context Management Plugin

Last updated: 2026-08-26

This is the small, portable context-management set extracted from the coding system:

- `init-context` — initialize repository memory routing and layers
- `sync-context` — detect and repair context drift
- `translate-agent-context` — port runtime-specific context surfaces

The three skills are materialized here for standalone publishing. The canonical source remains under `system/skills-src/craft/context/`; run `scripts/build-context-plugin.py --output <directory>` to refresh another standalone copy after source changes.

Runtime entry points:

```text
Claude Code       .claude-plugin/plugin.json
Codex             .codex-plugin/plugin.json
Pi                package.json (`pi.skills`)
DeepSeek Harness  .dsh/skills/ or .agents/skills/
```

DeepSeek Harness needs no native Cordis code for this set: copy the generated `skills/` directory into `.dsh/skills/` or `.agents/skills/`.

## Design Principles

**Three-layer model:**
- **Human** (WHY only): decisions, constraints, terminology, product intent — things code cannot show
- **Code Index** (WHAT/HOW, optional): where code lives, what calls what — rebuildable from code
- **Working** (NOW): current effort state, next actions, drafts — ephemeral

**Human layer = WHY only.** Does NOT document current code structure, patterns, or how things work — agents discover those from code or optional index.

**Minimal templates, no playbooks.** Agents read code to discover WHAT and HOW. Human layer documents only decisions that code cannot show.

**Completion compacts.** Finished plans, implemented specs, task state, and scratch artifacts are removed after their durable residue is extracted. Rationale and meaningful rejected alternatives go to ADRs; reader-relevant shipped outcomes go to the repository's existing changelog; both point to code, tests, issues, or releases instead of preserving the execution narrative.

## What Was Simplified

**Removed from Human layer:**
- `docs/ARCHITECTURE.md` — agents read code structure
- `docs/CONVENTIONS.md` — agents infer patterns from code
- `docs/TECH_DECISIONS.md` — merged into ADRs (only decisions with rationale)
- `docs/QUALITY.md` — too generic
- `docs/exec-plans/` — working memory handles backlog and debt

**Removed templates:** ARCHITECTURE, CONVENTIONS, TECH_DECISIONS, QUALITY, backlog, tech-debt-tracker, task, spec (kept: AGENTS routing index only)

**Removed playbooks:** All 8 playbooks removed (50+ KB of C4 syntax, entry-points, module-deps, external-deps, data-model, doc-types, readme-template) — agents generate these on-demand from code

**Added:** Matt Pocock's minimal ADR and CONTEXT formats (1-3 sentence decisions, tight terminology)

**Result:** 242KB → 140KB, 41 files → 15 files, focus on WHY not WHAT/HOW
