# Task 04: Create acs-design Plugin

**Agent**: Design-Plugin-Agent  
**Priority**: P1 (depends on acs-context)  
**Estimated effort**: 4-5 hours

## Objective

Extract design-phase skills into an independent `acs-design` plugin covering requirements, UX, and architecture.

## Input Resources

- `system/skills-src/design/` — 12 skills
- `system/workflows/design.md` — design workflow
- Architecture review specialists from `system/agents/`

## Deliverables

### 1. Plugin Structure

```
plugins/acs-design/
├── package.json
├── catalog/
│   └── skill-set.json
├── skills/
│   ├── acs-settle-requirements/
│   ├── acs-design-interaction-flow/
│   ├── acs-design-visual-system/
│   ├── acs-design-unified-doc/
│   ├── acs-design-architecture/
│   ├── acs-engineer-domain-model/
│   ├── acs-design-shared-foundations/
│   ├── acs-design-module-contracts/
│   ├── acs-wayfinder/
│   ├── acs-verify-reachability/
│   ├── acs-review-design/
│   └── acs-analyze-gaps/
├── shared/
│   ├── workflows/
│   │   └── design.md
│   ├── agents/
│   │   ├── architecture-explorer.md
│   │   ├── architecture-reviewer.md
│   │   └── (other arch specialists)
│   └── templates/
│       ├── architecture-doc-template.md
│       └── ux-flow-template.md
└── README.md
```

### 2. Skills to Extract

**Requirements**:
1. **acs-settle-requirements** — functional requirements from PRD

**UX Design**:
2. **acs-design-interaction-flow** — user interaction flows
3. **acs-design-visual-system** — visual design system
4. **acs-design-unified-doc** — unified design document

**Technical Architecture**:
5. **acs-design-architecture** — system architecture
6. **acs-engineer-domain-model** — domain model and glossary
7. **acs-design-shared-foundations** — shared libraries and utilities
8. **acs-design-module-contracts** — module interfaces

**Navigation**:
9. **acs-wayfinder** — architectural wayfinding
10. **acs-verify-reachability** — dependency reachability verification

**Review**:
11. **acs-review-design** — design review
12. **acs-analyze-gaps** — gap analysis

### 3. Specialist Agents to Bundle

From `system/agents/`:
- Architecture explorer/reviewer pairs
- API explorer/reviewer
- Data architecture explorer/reviewer
- Business logic explorer/reviewer
- Any other design-phase specialists

### 4. package.json

```json
{
  "name": "acs-design",
  "version": "0.4.0",
  "description": "ACS design phase - requirements, UX, architecture",
  "main": "catalog/skill-set.json",
  "keywords": ["agent", "coding", "design", "architecture", "ux"],
  "dependencies": {
    "acs-context": "^0.4.0"
  },
  "peerDependencies": {
    "acs-plan": "^0.4.0"
  }
}
```

### 5. SKILL.md Updates

For each skill:
- Rewrite paths to `shared/` resources
- Update agent references
- Declare dependencies:
  ```yaml
  dependencies:
    required:
      - acs-init-context
    optional:
      - acs-write-prd  # for requirements phase
    phase: design
  ```

### 6. README.md

Document:
- Plugin purpose (design and architecture)
- Design workflow: requirements → UX → architecture → contracts
- Skill inventory
- Installation and usage examples

## Acceptance Criteria

- [ ] Plugin installs standalone with only acs-context
- [ ] All 12 skills pass validation
- [ ] Architecture specialists resolve correctly
- [ ] Test: Run design flow (settle-requirements → design-architecture → design-module-contracts)
- [ ] Wayfinder queries work against existing architectures
- [ ] README complete with workflow examples

## Verification Script

```bash
cd /tmp/test-acs-design
npm install acs-context
npm install acs-design

find skills -name "SKILL.md" | wc -l  # Should be 12
find shared/agents -name "*.md" | wc -l  # Should be 10+

# Test design flow
cd /tmp/fresh-repo
# Run: acs-init-context
# Run: acs-settle-requirements
# Run: acs-design-architecture
# Verify: docs/architecture.md created
```

## Notes

- **acs-engineer-domain-model** may also be in context/; verify location
- Architecture specialists are numerous; ensure all are bundled
- Wayfinder and reachability skills query existing state; verify they work standalone
