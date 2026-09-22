# Phase Plugin Refactoring Plan

Last updated: 2026-09-22

## Goal

Refactor agent-coding-skills from monolithic plugin to:
1. **6 independent phase plugins** (ACS Plan, Design, Build, Test, Deploy, Maintain)
2. **Each skill independently installable** from its phase plugin

## Target Structure

```
agent-coding-skills/
├── plugins/
│   ├── acs-plan/
│   │   ├── package.json
│   │   ├── catalog/skill-set.json
│   │   ├── skills/                # Plan phase skills
│   │   ├── shared/                # Phase-internal shared resources
│   │   └── README.md
│   ├── acs-design/
│   │   ├── package.json
│   │   ├── catalog/skill-set.json
│   │   ├── skills/
│   │   ├── shared/
│   │   └── README.md
│   ├── acs-build/
│   ├── acs-test/
│   ├── acs-deploy/
│   ├── acs-maintain/
│   └── acs-context/              # Base infrastructure plugin
│       ├── package.json
│       ├── catalog/skill-set.json
│       ├── skills/               # context + authoring skills
│       ├── protocols/            # Shared memory/context protocols
│       └── README.md
├── system/                       # Legacy structure (deprecated after migration)
└── docs/
    └── migration/
        ├── dependency-map.md
        ├── phase-boundaries.md
        └── standalone-checklist.md
```

## Dependency Model

### Phase Plugin Dependencies

| Plugin | Required Deps | Optional Deps |
|--------|--------------|---------------|
| acs-plan | acs-context | - |
| acs-design | acs-context | acs-plan (for PRD) |
| acs-build | acs-context | acs-design (for architecture) |
| acs-test | acs-context | acs-build (for impl context) |
| acs-deploy | acs-context | acs-test (for test evidence) |
| acs-maintain | acs-context | acs-test (for debugging) |
| acs-context | - | - |

### Skill-Level Dependencies

Each skill's `SKILL.md` frontmatter declares:

```yaml
dependencies:
  required:
    - acs-init-context      # From acs-context plugin
  optional:
    - acs-research          # Graceful degradation if absent
  phase: build              # Parent plugin
  standalone: true          # Can be installed independently
```

## Phase Plugin Breakdown

### 1. acs-context (Base Infrastructure)
**Skills**: 3
- acs-init-context
- acs-manage-context
- acs-translate-agent-context

**Shared Resources**:
- `protocols/` — Memory contracts from `system/memory/`
- Core role prompts
- Base templates

**Purpose**: Foundation that all other plugins consume; no domain logic.

---

### 2. acs-plan
**Skills**: 8
- acs-brainstorm
- acs-validate-demand
- acs-shape-solution
- acs-write-prd
- acs-research
- acs-decide
- acs-challenge-decision
- acs-map-decisions

**Shared Resources**:
- `workflows/plan/` workflows
- Decision mapping templates
- PRD templates

---

### 3. acs-design
**Skills**: 10
- acs-settle-requirements
- acs-design-interaction-flow
- acs-design-visual-system
- acs-design-unified-doc
- acs-design-architecture
- acs-engineer-domain-model
- acs-design-shared-foundations
- acs-design-module-contracts
- acs-wayfinder
- acs-verify-reachability

**Shared Resources**:
- `workflows/design/` workflows
- Architecture review templates
- UX design templates

---

### 4. acs-build
**Skills**: 7
- acs-plan-delivery
- acs-implement
- acs-tdd
- acs-generate-tests
- acs-create-readme
- acs-document-codebase
- acs-create-discovery-report

**Shared Resources**:
- `workflows/build/` workflows
- `agents/` — tdd-executor, implementer agents
- DAG rendering scripts
- Test templates

---

### 5. acs-test
**Skills**: 9
- acs-analyze-test-gaps
- acs-review-code-quality
- acs-review-architecture
- acs-review-design
- acs-analyze-gaps
- acs-triage-issue
- acs-debug
- acs-resolve-merge-conflict
- acs-generate-integration-tests

**Shared Resources**:
- `workflows/test/` workflows
- Review specialist agents
- Test coverage templates

---

### 6. acs-deploy
**Skills**: 2 (planned)
- acs-release
- acs-review-pr

**Shared Resources**:
- `workflows/deploy/` workflows
- Release checklist templates

---

### 7. acs-maintain
**Skills**: 2
- acs-diagnose-incident
- acs-fix-incident

**Shared Resources**:
- `workflows/maintain/` workflows
- Incident triage templates

---

## Migration Tasks (Parallel Execution)

### Task 1: Create acs-context plugin
**Owner**: Phase-1 Agent
**Deliverables**:
- Extract memory protocols from `system/memory/`
- Package acs-init-context, acs-manage-context, acs-translate-agent-context
- Create standalone package.json with zero dependencies
- Verify standalone installation

---

### Task 2: Create acs-plan plugin
**Owner**: Phase-2 Agent
**Depends on**: Task 1
**Deliverables**:
- Extract 8 plan skills
- Bundle plan workflows
- Declare acs-context as required dependency
- Create plugin package.json
- Verify: acs-brainstorm → acs-write-prd flow works standalone

---

### Task 3: Create acs-design plugin
**Owner**: Phase-3 Agent
**Depends on**: Task 1
**Deliverables**:
- Extract 10 design skills
- Bundle design workflows + architecture templates
- Declare acs-context required, acs-plan optional
- Create plugin package.json
- Verify: acs-settle-requirements → acs-design-architecture flow

---

### Task 4: Create acs-build plugin
**Owner**: Phase-4 Agent
**Depends on**: Task 1
**Deliverables**:
- Extract 7 build skills
- Bundle specialist agents (tdd-executor, implementer)
- Bundle DAG scripts from `system/commands/`
- Declare acs-context required, acs-design optional
- Create plugin package.json
- Verify: acs-plan-delivery → acs-tdd → acs-implement flow

---

### Task 5: Create acs-test plugin
**Owner**: Phase-5 Agent
**Depends on**: Task 1
**Deliverables**:
- Extract 9 test/review skills
- Bundle review specialists
- Declare acs-context required, acs-build optional
- Create plugin package.json
- Verify: acs-review-code-quality runs standalone

---

### Task 6: Create acs-maintain plugin
**Owner**: Phase-6 Agent
**Depends on**: Task 1
**Deliverables**:
- Extract 2 maintain skills
- Bundle incident workflows
- Declare acs-context required, acs-test optional
- Create plugin package.json
- Verify: acs-diagnose-incident runs standalone

---

## Orchestrator Responsibilities (This Session)

1. **Pre-flight**:
   - Analyze current `system/` dependencies
   - Generate dependency graph
   - Create migration checklist

2. **Dispatch**:
   - Spawn 6 herdr agents for Tasks 1-6
   - Pass phase-specific resource lists to each agent
   - Monitor progress via herdr status

3. **Verification**:
   - Collect plugin packages from each agent
   - Run standalone installation tests
   - Verify inter-plugin optional dependencies work
   - Run integration test: full lifecycle with only required plugins installed

4. **Reconciliation**:
   - Update root catalog/skill-set.json to list 7 plugins
   - Archive `system/` as `legacy/`
   - Update README.md with new structure
   - Update CLAUDE.md with plugin installation instructions

## Acceptance Criteria

### Per-Plugin
- [ ] Plugin installs standalone with only acs-context
- [ ] All skills in plugin pass `python3 system/memory/validate_suite.py`
- [ ] catalog/skill-set.json lists correct skill count
- [ ] README.md documents plugin purpose and skill list

### Per-Skill
- [ ] Skill installs independently from plugin
- [ ] Skill runs with only declared required dependencies
- [ ] Skill degrades gracefully when optional deps absent
- [ ] SKILL.md frontmatter declares correct dependencies

### Integration
- [ ] Full lifecycle (plan → maintain) works with all plugins installed
- [ ] Minimal workflow (acs-context + acs-build) executes acs-tdd
- [ ] Removing optional plugin doesn't break required workflows

## Next Steps

1. **Generate dependency map** — scan current `system/skills-src/` for cross-references
2. **Create migration workspace** — `docs/migration/`
3. **Dispatch herdr tasks** — one agent per phase plugin
4. **Verify and reconcile** — orchestrator validates all outputs
