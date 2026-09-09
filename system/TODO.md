# System TODO

Last updated: 2026-09-08

This list separates adaptation work inherited from Matt’s model from cleanup required by the existing system. Priority reflects workflow correctness and data integrity.

## P0 — Catalog/discovery drift

- [x] ~~Reconcile `craft/context` discovery~~ — Done 2026-08-25: `init-context`, `sync-context`, and `translate-agent-context` are the canonical loader entries; obsolete links to removed skills were deleted, and Claude/Codex/Pi manifests now expose the same skill tree.

## P0 — Shared memory and delivery

- [ ] Implement the missing `plan` skill. It must own `plan.md`, testing seams, architecture decisions, and the handoff to dependency tickets.
- [ ] Update every persistent existing skill to read `docs/agents/memory.md`, declare owned artifacts, and update `state.md` at transitions.
- [ ] Change `tasks` from a single `tasks.md` checklist to one vertical-slice issue file per ticket with `Status`, `Blocked by`, and `Claimed by`.
- [ ] Resolve the PRD/spec boundary: `write-prd` owns product intent; `spec` owns technical feature behavior.

## P0 — Matt-derived capability modifications

- [ ] Merge domain-aware persistence from `grill-with-docs` into `brainstorm-feature`; use `grilling` as the question primitive and `domain-modeling` as the only glossary/ADR writer.
- [ ] Add a synthesis mode from `to-spec` to `spec` that consumes approved conversation/map decisions without repeating the interview.
- [ ] Merge tracer-bullet and expand-contract rules from `to-tickets` into `tasks`.
- [ ] Merge `implement` into the delivery executor: claim one frontier issue, use TDD, run project checks, review, update shared state, and never commit automatically.
- [ ] Reconcile TDD contracts: keep behavior-level red/green slices at agreed public seams; decide whether refactoring occurs inside each cycle or in the review phase.
- [x] ~~Add Standards and Spec as separate axes in `review-code-quality`~~ — Done 2026-09-08: findings are axis-tagged and reported separately; the Spec axis runs as an inline spec-fidelity pass reusing gap-analysis statuses, so no third overlapping reviewer was created.
- [ ] Connect `wayfinder` ticket creation and completion directly to the roadmap renderer.
- [ ] Add tracker-specific GitHub, GitLab, and local-Markdown templates to `manage-context` (Phase A).
- [ ] Add deterministic HTML generation templates for architecture reviews while keeping Markdown canonical.
- [ ] Add realistic eval cases for setup, routing, handoff, wayfinding, debugging, and no-auto-commit behavior.

## P0 — Existing skill correctness

- [x] ~~Remove or redesign `request-code-review`~~ — Done 2026-09-08: removed; its pre-commit triggers and static security greps were folded into `review-code-quality`, and its auto-fix/auto-commit behavior was dropped by design.
- [ ] Fix `document-codebase` stale names (`review-Codex-md`, `.Codex/rules`), duplicated AGENTS/CLAUDE wording, project-specific residue, and README ownership overlap.
- [x] ~~Fix `analyze-test-gaps` artifact-count contradiction~~ — Done 2026-09-08: description and Output Contract now say three artifacts across four steps.
- [ ] Unify the `analyze-test-gaps` critical-path location with `document-codebase`.
- [ ] Correct the retained `tdd-builder` agent’s nonexistent spec “Step 3.5” reference.
- [ ] Make `create-readme` the sole root-README author; `document-codebase` should delegate or exclude that output.

## P1 — Runtime and discoverability

- [ ] Replace runtime-specific calls such as `AskUserQuestion`, `EnterWorktree`, `TaskList`, `TaskUpdate`, `delegate_task`, and hardcoded model names with capability checks and runtime adapters.
- [ ] Resolve script paths through the plugin/skill root. Current DAG and UI/UX examples assume obsolete working-directory layouts.
- [x] ~~Repair `ui-ux-pro-max` documentation~~ — Done 2026-08-17: the vendored copy was removed instead; layer-② dispatch to external knowledge skills now lives in `design/ux` pipeline skills, catalogued in `design/ux/README.md`.
- [ ] Decide whether `review-architecture` is a generic reviewer or a data-platform reviewer; remove hardcoded ODS/DWD/APP, Hologres, MinIO, FastAPI, and Compose assumptions or rename it.
- [ ] Narrow `design-agent-architecture` to authoring; keep review and documentation ownership in their dedicated skills.
- [ ] Normalize skill descriptions to concise trigger and boundary text.
- [ ] Generate or refresh `agents/openai.yaml` for all system skills.

## P1 — Documentation and provenance

- [ ] Remove or clearly label absent Taste and Impeccable packages in the frontend guide.
- [ ] Complete provenance and license records for every existing third-party skill package.
- [ ] Add an artifact registry check that rejects two skills claiming canonical ownership of the same path.

## P2 — Verification

- [ ] Add a repository verification command covering JSON/YAML/frontmatter parsing, unique skill/agent names, local Markdown links, plugin inventory, and dates on edited Markdown.
- [ ] Add synthetic DAG fixtures and scan/render assertions for finished, frontier, blocked, cross-workstream, and unresolved dependencies.
- [ ] Convert legacy `evals.json` files to supported plugin eval cases.
- [ ] Establish minimum eval coverage for state-mutating skills.
- [ ] Add CI after local verification is stable.
