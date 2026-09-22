# Task 02: Create acs-plan Plugin

**Agent**: Plan-Plugin-Agent  
**Priority**: P1 (independent of design/build/test)  
**Estimated effort**: 3-4 hours

## Objective

Extract planning-phase skills into an independent `acs-plan` plugin, enabling users to run product discovery and PRD generation without installing the full suite.

## Input Resources

- `system/skills-src/plan/` — 10 skills
- `system/workflows/plan.md` — planning workflow
- Related authoring skills for research and decision mapping

## Deliverables

### 1. Plugin Structure

```
plugins/acs-plan/
├── package.json
├── catalog/
│   └── skill-set.json
├── skills/
│   ├── acs-brainstorm/
│   ├── acs-validate-demand/
│   ├── acs-shape-solution/
│   ├── acs-write-prd/
│   ├── acs-research/
│   ├── acs-decide/
│   ├── acs-challenge-decision/
│   ├── acs-map-decisions/
│   ├── acs-explore-unknowns/
│   └── acs-plan-architecture/
├── shared/
│   ├── workflows/
│   │   └── plan.md
│   └── templates/
│       ├── prd-template.md
│       └── decision-map-template.md
└── README.md
```

### 2. Skills to Extract

**Core Planning Flow**:
1. **acs-brainstorm** — initial feature exploration
2. **acs-validate-demand** — validate problem-solution fit
3. **acs-shape-solution** — shape the solution approach
4. **acs-write-prd** — generate PRD document

**Decision Support**:
5. **acs-research** — primary-source research
6. **acs-decide** — structured decision-making
7. **acs-challenge-decision** — adversarial decision review
8. **acs-map-decisions** — decision dependency mapping

**Exploration**:
9. **acs-explore-unknowns** — identify knowledge gaps
10. **acs-plan-architecture** — architectural planning (check if this exists or is in design/)

### 3. Workflow to Bundle

From `system/workflows/`:
- `plan.md` — planning phase workflow
- Extract relevant sections from `ideas.md`

### 4. package.json

```json
{
  "name": "acs-plan",
  "version": "0.4.0",
  "description": "ACS planning phase - discovery, validation, PRD generation",
  "main": "catalog/skill-set.json",
  "keywords": ["agent", "coding", "planning", "prd", "discovery"],
  "dependencies": {
    "acs-context": "^0.4.0"
  },
  "peerDependencies": {}
}
```

### 5. catalog/skill-set.json

List all 10 skills with:
- Correct `id` (acs-*)
- Phase: `plan`
- Dependencies:
  - Required: `acs-init-context`
  - Optional: none (plan is the entry phase)

### 6. SKILL.md Updates

For each skill:
- Rewrite relative paths to resolve from plugin root
- Update cross-references to other acs-* skills
- Declare dependencies in frontmatter:
  ```yaml
  dependencies:
    required:
      - acs-init-context
    optional: []
    phase: plan
  ```

### 7. README.md

Document:
- Plugin purpose (product discovery and planning)
- Planning workflow: brainstorm → validate → shape → PRD
- Skill inventory with one-line descriptions
- Installation: `claude plugin install acs-plan`
- Usage examples

## Acceptance Criteria

- [ ] Plugin installs standalone with only acs-context
- [ ] All 10 skills pass validation
- [ ] Workflow file paths resolve correctly
- [ ] Test: Run planning flow (brainstorm → validate → shape → write-prd) in isolated repo
- [ ] PRD template generates correctly
- [ ] Decision mapping works for multi-option scenarios
- [ ] README complete with examples

## Verification Script

```bash
# In isolated directory
cd /tmp/test-acs-plan
npm install acs-context
npm install acs-plan

# Verify skills
find skills -name "SKILL.md" | wc -l  # Should be 10

# Test planning flow
cd /tmp/fresh-repo
git init
# Run: acs-init-context
# Run: acs-brainstorm --feature "user authentication"
# Run: acs-write-prd
# Verify: docs/prd.md created
```

## Notes

- **acs-plan-architecture** may not exist; verify in source
- Research skill is heavyweight; ensure it bundles all references
- Decision mapping may reference external tools; verify all dependencies bundled
