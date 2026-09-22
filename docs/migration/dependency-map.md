# Dependency Map for Phase Plugin Refactoring

Last updated: 2026-09-22

## Analysis Summary

**Total skills**: 44
- plan: 10
- design: 12  
- build: 3
- test: 8
- deploy: 0 (planned)
- maintain: 1
- context: 5
- authoring: 5

**Shared resources**:
- 26 specialist agent files in `system/agents/`
- Phase-specific workflows in `system/workflows/`
- Protocol definitions referenced in context skills
- Command entry points in `system/commands/`

## Cross-Phase Dependencies

### Inbound Dependencies (Required by)

**acs-context skills** (foundation):
- Required by: ALL other phases
- Skills: acs-init-context, acs-manage-context, acs-translate-agent-context
- Resources: Memory protocols, core templates

**acs-plan outputs** (PRD, decisions):
- Required by: acs-design (requirements), acs-build (planning)
- Skills: acs-write-prd, acs-map-decisions
- Resources: Decision maps, PRD templates

**acs-design outputs** (architecture, contracts):
- Required by: acs-build (implementation guidance)
- Skills: acs-design-architecture, acs-design-module-contracts
- Resources: Architecture diagrams, module interfaces

**acs-build outputs** (implementation, tests):
- Required by: acs-test (test gaps), acs-maintain (debugging context)
- Skills: acs-tdd, acs-implement
- Resources: Test evidence, delivery DAGs

**acs-test outputs** (verification):
- Required by: acs-deploy (release gating), acs-maintain (regression analysis)
- Skills: acs-review-code-quality, acs-analyze-test-gaps
- Resources: Review findings, coverage reports

### Within-Phase Dependencies

**plan/** internal:
- acs-brainstorm → acs-validate-demand → acs-shape-solution → acs-write-prd
- acs-research (optional enhancement for any planning skill)
- acs-decide, acs-challenge-decision → acs-map-decisions

**design/** internal:
- acs-settle-requirements (consumes PRD from plan)
- acs-design-interaction-flow → acs-design-unified-doc
- acs-design-architecture → acs-engineer-domain-model → acs-design-module-contracts
- acs-wayfinder, acs-verify-reachability (query existing architecture)

**build/** internal:
- acs-plan-delivery (creates ticket DAG)
- acs-implement (dispatches acs-tdd per ticket)
- acs-tdd (criterion-based red-green-refactor)

**test/** internal:
- acs-analyze-test-gaps → acs-generate-integration-tests
- acs-review-* suite (code-quality, architecture, design) are parallel/independent
- acs-triage-issue → acs-debug
- acs-resolve-merge-conflict (standalone)

## Resource Distribution

### To acs-context plugin
- `system/skills-src/context/` → all 5 skills
- `system/skills-src/context/*/references/` → protocol docs
- Core memory contracts (currently referenced, not in system/memory/)
- Base templates

### To acs-plan plugin
- `system/skills-src/plan/` → all 10 skills
- `system/workflows/plan.md`
- PRD and decision map templates

### To acs-design plugin  
- `system/skills-src/design/` → all 12 skills
- `system/workflows/design.md`
- Architecture review templates
- UX design workflows

### To acs-build plugin
- `system/skills-src/build/` → 3 skills (plan-delivery, implement, tdd)
- `system/workflows/build.md`, `system/workflows/feature-delivery.md`
- `system/agents/` → tdd-executor, implementer agents (subset)
- `system/commands/` → DAG rendering scripts
- README/documentation skills (create-readme, document-codebase, create-discovery-report)

### To acs-test plugin
- `system/skills-src/test/` → 8 skills
- `system/workflows/testing.md`, `system/workflows/debugging.md`
- `system/agents/` → all reviewer specialists (20+ files)
- Coverage and review templates

### To acs-maintain plugin
- `system/skills-src/maintain/` → 1 skill (diagnose-incident, fix-incident planned)
- `system/workflows/debugging.md` (shared with test)
- Incident triage templates

### To acs-authoring plugin (meta/tooling)
- `system/skills-src/authoring/` → 5 skills
- Research, decision challenge, DAG rendering, skill authoring
- Meta-tools for building ACS itself

## Missing/Unresolved

1. **deploy phase**: 0 skills currently; `system/workflows/deploy.md` exists but no skill implementations
2. **system/memory/**: Referenced in docs but directory doesn't exist; protocols may be embedded in context skills
3. **Cross-references**: Only 5 skills have explicit `[acs-*]` markdown links; most dependencies are implicit in descriptions
4. **Standalone readiness**: Current skills have relative path references (`../memory/`, `../../workflows/`) that need rewriting

## Verification Checklist

Per plugin, before considering it complete:
- [ ] All source skills copied with complete subdirectories
- [ ] Relative paths rewritten to resolve from plugin root
- [ ] package.json with correct dependencies declared
- [ ] catalog/skill-set.json listing all included skills
- [ ] README.md documenting plugin purpose and skill inventory
- [ ] Standalone installation test (isolated directory, no sibling checkouts)
- [ ] Representative workflow test (e.g., plan → validate → PRD for acs-plan)

## Next: Task Spec Generation

Will create 7 detailed task specs (one per plugin) for herdr dispatch.
