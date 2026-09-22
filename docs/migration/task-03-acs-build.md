# Task 03: Create acs-build Plugin

**Agent**: Build-Plugin-Agent  
**Priority**: P1 (most critical for execution)  
**Estimated effort**: 4-5 hours

## Objective

Extract build/delivery phase skills into an independent `acs-build` plugin, including TDD execution, delivery planning, and specialist agents.

## Input Resources

- `system/skills-src/build/` — 3 core skills + 4 documentation skills
- `system/workflows/build.md`, `feature-delivery.md`
- `system/agents/` — tdd-executor, implementer agents (subset)
- DAG rendering scripts from `system/commands/`

## Deliverables

### 1. Plugin Structure

```
plugins/acs-build/
├── package.json
├── catalog/
│   └── skill-set.json
├── skills/
│   ├── acs-plan-delivery/
│   ├── acs-implement/
│   ├── acs-tdd/
│   ├── acs-generate-tests/
│   ├── acs-create-readme/
│   ├── acs-document-codebase/
│   └── acs-create-discovery-report/
├── shared/
│   ├── workflows/
│   │   ├── build.md
│   │   └── feature-delivery.md
│   ├── agents/
│   │   ├── tdd-executor.md
│   │   └── implementer.md
│   ├── scripts/
│   │   └── render-dag.js
│   └── templates/
│       ├── delivery-report.md
│       └── test-template.md
└── README.md
```

### 2. Skills to Extract

**Core Build**:
1. **acs-plan-delivery** — ticket DAG generation
2. **acs-implement** — feature implementation orchestrator
3. **acs-tdd** — criterion-based red-green-refactor

**Test Generation**:
4. **acs-generate-tests** — test case generation

**Documentation**:
5. **acs-create-readme** — root README author
6. **acs-document-codebase** — CLAUDE.md/AGENTS.md generation
7. **acs-create-discovery-report** — codebase discovery report

### 3. Specialist Agents to Bundle

From `system/agents/`:
- `tdd-executor.md` — TDD loop executor
- `implementer.md` — implementation agent
- Any other agents referenced by build skills

### 4. Scripts to Bundle

From `system/commands/`:
- DAG rendering script (if exists as separate file)
- Portfolio visualization scripts
- Any build orchestration scripts

### 5. package.json

```json
{
  "name": "acs-build",
  "version": "0.4.0",
  "description": "ACS build phase - delivery planning, TDD, implementation",
  "main": "catalog/skill-set.json",
  "keywords": ["agent", "coding", "build", "tdd", "delivery"],
  "dependencies": {
    "acs-context": "^0.4.0"
  },
  "peerDependencies": {
    "acs-design": "^0.4.0"
  }
}
```

### 6. SKILL.md Updates

For each skill:
- Rewrite relative paths to `shared/` resources
- Update agent references to `shared/agents/`
- Update workflow references to `shared/workflows/`
- Declare dependencies:
  ```yaml
  dependencies:
    required:
      - acs-init-context
    optional:
      - acs-design-architecture  # for implementation guidance
      - acs-settle-requirements   # for acceptance criteria
    phase: build
  ```

### 7. README.md

Document:
- Plugin purpose (delivery planning and TDD execution)
- Build workflow: plan-delivery → implement → tdd
- Skill inventory with one-line descriptions
- Specialist agents and their roles
- Installation: `claude plugin install acs-build`
- Usage examples

## Acceptance Criteria

- [ ] Plugin installs standalone with only acs-context
- [ ] All 7 skills pass validation
- [ ] Specialist agents resolve correctly
- [ ] DAG rendering works for ticket graphs
- [ ] Test: Run delivery flow (plan-delivery → implement → tdd) in isolated repo
- [ ] TDD loop: red → green → refactor works standalone
- [ ] Documentation skills generate correct output
- [ ] No hardcoded paths to source checkout
- [ ] README complete with orchestration examples

## Verification Script

```bash
# In isolated directory
cd /tmp/test-acs-build
npm install acs-context
npm install acs-build

# Verify skills
find skills -name "SKILL.md" | wc -l  # Should be 7

# Verify agents
find shared/agents -name "*.md" | wc -l  # Should be 2+

# Test build flow
cd /tmp/fresh-repo
git init
echo "# Test" > README.md
# Run: acs-init-context
# Run: acs-plan-delivery --scope "add login feature"
# Verify: delivery-plan.html created
# Run: acs-tdd --ticket "T001"
# Verify: tests created and pass
```

## Notes

- **acs-implement** dispatches **acs-tdd** per ticket; ensure orchestration works
- DAG rendering may depend on external tools (Graphviz); document requirements
- **acs-create-readme** and **acs-document-codebase** may overlap; clarify ownership in README
- Specialist agents reference may need path rewriting
