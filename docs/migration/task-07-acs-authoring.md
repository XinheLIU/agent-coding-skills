# Task 07: Create acs-authoring Plugin

**Agent**: Authoring-Plugin-Agent  
**Priority**: P2 (meta-tooling, depends on acs-context)  
**Estimated effort**: 2-3 hours

## Objective

Extract authoring/meta skills into an independent `acs-authoring` plugin for skill development and system introspection.

## Input Resources

- `system/skills-src/authoring/` — 5 skills
- DAG rendering scripts
- Skill authoring templates

## Deliverables

### 1. Plugin Structure

```
plugins/acs-authoring/
├── package.json
├── catalog/
│   └── skill-set.json
├── skills/
│   ├── acs-research/
│   ├── acs-challenge-decision/
│   ├── acs-draw-portfolio-dag/
│   ├── acs-create-skill/
│   └── acs-optimize-skill/
├── shared/
│   ├── scripts/
│   │   └── render-dag.js
│   └── templates/
│       └── skill-template.md
└── README.md
```

### 2. Skills to Extract

**Research**:
1. **acs-research** — primary-source research (may also be in plan/)

**Decision Tools**:
2. **acs-challenge-decision** — adversarial decision review

**Visualization**:
3. **acs-draw-portfolio-dag** — render ticket/portfolio DAGs

**Skill Development**:
4. **acs-create-skill** — scaffold new skills
5. **acs-optimize-skill** — optimize existing skills

### 3. Scripts to Bundle

From `system/commands/` or inline in skills:
- DAG rendering scripts (Mermaid, DOT, or custom)
- Skill validation scripts

### 4. package.json

```json
{
  "name": "acs-authoring",
  "version": "0.4.0",
  "description": "ACS meta-tooling - research, DAG visualization, skill development",
  "main": "catalog/skill-set.json",
  "keywords": ["agent", "coding", "authoring", "meta", "tooling"],
  "dependencies": {
    "acs-context": "^0.4.0"
  },
  "peerDependencies": {}
}
```

### 5. catalog/skill-set.json

List all 5 skills with:
- Correct `id` (acs-*)
- Phase: `authoring`
- Dependencies:
  - Required: `acs-init-context`
  - Optional: none (meta-tools are independent)

### 6. SKILL.md Updates

For each skill:
- Rewrite paths to `shared/` resources
- Update script references
- Declare dependencies:
  ```yaml
  dependencies:
    required:
      - acs-init-context
    optional: []
    phase: authoring
  ```

### 7. README.md

Document:
- Plugin purpose (meta-tooling and skill development)
- Skill inventory
- DAG rendering capabilities
- Installation and usage examples
- Note: This plugin is for ACS maintainers and advanced users

## Acceptance Criteria

- [ ] Plugin installs standalone with only acs-context
- [ ] All 5 skills pass validation
- [ ] DAG rendering works for ticket graphs
- [ ] Test: Run acs-draw-portfolio-dag on a delivery plan
- [ ] Test: Run acs-create-skill to scaffold a new skill
- [ ] README documents all meta-tools

## Verification Script

```bash
cd /tmp/test-acs-authoring
npm install acs-context
npm install acs-authoring

find skills -name "SKILL.md" | wc -l  # Should be 5

# Test DAG rendering
cd /tmp/test-repo-with-delivery-plan
# Run: acs-init-context
# Run: acs-draw-portfolio-dag
# Verify: DAG visualization generated

# Test skill creation
# Run: acs-create-skill --name "test-skill"
# Verify: skill scaffold created
```

## Notes

- **acs-research** may be in both plan/ and authoring/; verify and deduplicate
- DAG rendering is used by build plugin; ensure no circular dependency
- Skill creation/optimization tools are for ACS maintainers
- This plugin is lowest priority for end users; prioritize other phases first
