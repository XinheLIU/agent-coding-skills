# Changelog

Last updated: 2026-08-05

## Unreleased

### Context management

- Added the `context-management` collection documenting the three context layers — Human docs, the generated Wiki index, and gitignored Working memory — with `manage-context` as the single entry point and orchestrator.
- Added `manage-context`, a two-phase skill that reads `docs/agents/memory.md` and auto-selects its phase. Phase A (setup) configures the memory layers, writes the routing config, and bootstraps the Working layer; Phase B (sync) detects cross-layer drift, repairs narrow factual errors directly, and invokes the owning skill for structural work. The split is on whether the routing config exists, not on repository age — the two phases have genuinely different inputs.
- Applied dependency inversion across the collection: each layer skill owns exactly one layer, and `manage-context` orchestrates them. Phase B dispatches to `scaffold-agent-docs` (Human-layer structure), `document-codebase` (stale content, one call per surface), `review-agent-instructions` (context-file shape), `create-readme`, `extract-rules`, and `index-codebase`.
- Made `scaffold-agent-docs` mode-aware. Mode A creates `AGENTS.md` and the `docs/` structure from templates and fills them from the code; Mode B audits existing docs, verifies every claim against live code, classifies each document, and applies structural repairs. Content gaps are reported for `manage-context` to delegate rather than filled in place.
- Consolidated `setup-agent-system`, `setup-session-memory`, `sync-context`, and `choose-workflow` into `manage-context`, and absorbed `organize-codebase-docs` into `scaffold-agent-docs` Mode B. Merged `review-claude-md` and `review-agent-md` into `review-agent-instructions`, which detects which file is present and applies the matching skeleton and line ceiling.
- Added seven fill-in Human-layer templates (shipped inside `scaffold-agent-docs/references/templates/`) for `AGENTS.md`, `ARCHITECTURE.md`, `CONVENTIONS.md`, `TECH_DECISIONS.md`, `QUALITY.md`, `backlog.md`, and `tech-debt-tracker.md`, plus a canonical `/docs` layout reference for repositories that outgrow the flat shape.
- Documented the four external indexers with verified install commands, index locations, MCP registration, and hardening flags in `index-codebase/references/external-tools.md`.
- Moved the shared memory protocol into its owning skill at `context-management/manage-context/references/PROTOCOL.md` so a skill copied out of this repo carries the contract with it.

### Repository structure

- Reorganized skills into a browsable category source tree (`system/skills-src/<category>/`) with a flat symlink farm at `system/skills/` for loader discovery. Categories: context-management, product-ideation, feature-delivery, code-quality, architecture-design, frontend, debugging, research-planning. This also fixes `product-ideation`, whose skills were previously nested one level too deep and therefore undiscoverable.
- Made every skill self-contained and portable: per-skill `references/` carry their own templates and tool docs, and skill bodies refer to sibling skills by name rather than by repo-relative path.
- Reorganized the product as a valid plugin root under `system/` with flat `skills/`, shared `agents/`, `commands/`, memory, workflows, and human docs.
- Removed the `examples/` scaffolding once its templates were extracted.

### Earlier

- Added a shared memory protocol covering core, human, optional wiki, and working memory; Markdown owns semantic state and HTML provides generated views.
- Added setup, routing, idea, feature-delivery, testing, and debugging entry points.
- Adapted 14 capabilities from Matt Pocock's skill set, mapped six overlaps for integration, and recorded revisions and MIT attribution.
- Added the 34th pre-existing skill, `draw-portfolio-dag`, to the product inventory and made roadmap integration a P0 item.
- Added an organization report and prioritized TODO for Matt adaptations and existing-skill cleanup.
- Kept local upstream snapshots under the ignored, read-only `references/` boundary.

## v0.1.0 — 2026-07-31

Initial extraction from [XinheLIU/agent-skills](https://github.com/XinheLIU/agent-skills).

**Moved in:**
- `architecture-design/` — agent architecture design skill + 5-skill code review suite (review-architecture, review-code-quality, review-design-doc, review-implementation-gaps, analyze-test-gaps) with 27 shared sub-agent definitions.
- `coding/` — code-quality (refactor, simplify, request-code-review), engineering-setup (8 skills: review-claude-md, review-agent-md, extract-rules, translate-agent-context, organize-docs, document-codebase, create-readme, build-skeleton), frontend design (3 skills), tech-design (design-operational-ontology), working-on-a-feature (5-skill TDD workflow), and git slash commands (/commit, /pr-create, /git:log, /git:status).
