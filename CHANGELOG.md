# Changelog

Last updated: 2026-08-18

## Unreleased

### Existing-product product lane

Added an explicit product workflow for existing codebases and active-product improvements.

- Added `map-current-product`, which owns `discovery/current-product.md` and extracts
  product-facing roles, flows, implemented user stories, in-progress/planned behavior, gaps, and
  source evidence from an existing codebase.
- Added `scope-product-increment`, which owns `discovery/increment.md` and scopes
  existing-product improvements as `ADDED / MODIFIED / REMOVED` behavior with P0/P1/out-of-scope,
  acceptance criteria, edge cases, instrumentation, success metrics, and refinement notes.
- Updated product routing so codebase user-story requests go to `map-current-product`,
  active-product improvements baseline before scoping, greenfield MVPs stay on `scope-mvp`, and
  architecture-only refactors route outside product.
- Added PRD delta mode so `write-prd` preserves existing edits while appending update-log entries
  and applying accepted product increments.
- Published the two skills through `system/skills/` symlinks and `catalog/skill-set.json`.

### Product skills published to the loader and catalog

Made the eight product skills discoverable. The sources landed in the previous change; this publishes them.

- Added `system/skills/` symlinks for `brainstorm`, `validate-demand`, `run-premortem`, `ideate-product`, `shape-solution`, `scope-mvp`, `prototype`, and `write-prd`. Without these the loader cannot see a skill regardless of its source being present.
- Rebuilt `catalog/skill-set.json` around the category source tree. Product is now two categories — `product/discovery` (brainstorm, validate-demand, run-premortem, ideate-product) and `product/definition` (shape-solution, scope-mvp, prototype, write-prd) — replacing the flat `product-ideation` category, which still advertised six skills that no longer exist under those names (`analyze-jtbd`, `critique-idea`, `design-mvp`, `generate-product-ideas`, `review-product-strategy`, `validate-product-opportunity`, `write-user-story`).
- Remaining categories follow the same restructure: `design/ux`, `design/technical`, `engineering/feature`, `engineering/frontend`, `quality/testing`, `quality/review`, `quality/debugging`, `craft/context`, `craft/meta`.
- Dropped two `design/ux` entries — `interaction-design` and `visual-design-variants` — that resolved to nothing on disk. The design skills own their catalog entries when that work lands.

All 48 advertised skills now resolve to a real path.


### Memory contract — layer boundaries and product intent promotion

Clarified the four-layer memory contract so the Human/Working split is a content rule, not an audience label. Every product skill now declares its layer explicitly, and the PRD moves from the gitignored work root into the tracked Human layer.

**The core change.** The old boundary was "Human = docs for maintainers." That describes a reader, not a content type. The new rule is a question: *if the work root were deleted today, would the project have lost a fact it still needs?* Yes → tracked layer. No → working memory. Promotion flows one way only — Working → Human or Core, never back.

**Product intent is Human-layer.** `write-prd` now owns `<product-docs>/<slug>/prd.md` (default `docs/product/<slug>/prd.md`) instead of `<effort>/prd.md`. The discovery files (`brainstorm.md`, `demand.md`, `solution.md`, `mvp.md`, `premortem.md`) remain working-layer drafts — useful while the effort runs, gone when it ends, with their durable conclusions living in the PRD.

**Two promotion points in the product pipeline.** `validate-demand` returning Green is the first: the core idea (persona, job, struggle, demand type, evidence grade) has earned a place in the tracked layer. `write-prd` runs in early mode at that point — Part 1 filled, later sections marked `Pending — awaiting <skill>`. The second run extends the PRD once scope and risks are settled. Efforts abandoned mid-pipeline still leave a record of what was considered and why.

**Every product skill gets a `Layer / Owns / Promotes` declaration.** Six skills are Working-layer owners; `write-prd` is the Human-layer owner and the pipeline's one promotion step; `ideate-product` is Transient (routes state, writes none).

**`manage-context` gains layer awareness.** Phase A emits a `Product docs:` config line alongside the existing `Work root:` line, making the tracked/disposable split explicit from the first session. Phase B's drift detection adds a layer-misplacement check — a Green `demand.md` with no PRD is a higher-priority finding than a stale path. Phase B's promotion table gains an explicit product-intent row routing to `write-prd`.

**`prototype` decisions classify on write.** Interaction decisions promote to the PRD's Part 3; architectural decisions promote to an ADR via `domain-modeling`. The skill states which kind before handing back.

**Renamed `design-solution` → `shape-solution`** and cleaned up all resulting stale references in the protocol, reference files, and routing tables.

**Design-layer routing arrives ahead of its skills.** The memory config gained a `Design docs:` line (`docs/design/`) and the routing template gained a Design Workflow section applying the same split: the design system and component docs are tracked Human-layer reference material, while HTML variant exploration under `.scratch/<effort>/designs/` is disposable scaffolding that production code supersedes. The design skills themselves are not in this change — only the memory contract they will write against.

**Files changed:** `system/memory/README.md`, `manage-context/SKILL.md`, `manage-context/references/PROTOCOL.md`, all seven product `SKILL.md` files, `product/README.md`, `system/workflows/ideas.md`, `system/workflows/feature-delivery.md`, `system/README.md`, `system/docs/organization-report.md`, `write-prd/references/prd-principles.md`, two reference files carrying the rename.


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
