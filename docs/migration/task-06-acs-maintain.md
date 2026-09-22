# Task 06: Create acs-maintain Plugin

**Agent**: Maintain-Plugin-Agent  
**Priority**: P2 (smaller scope, depends on acs-context)  
**Estimated effort**: 2-3 hours

## Objective

Extract maintenance-phase skills into an independent `acs-maintain` plugin for incident diagnosis and fixes.

## Input Resources

- `system/skills-src/maintain/` — 1 skill (diagnose-incident)
- `system/workflows/debugging.md` (shared with test)
- Incident triage templates

## Deliverables

### 1. Plugin Structure

```
plugins/acs-maintain/
├── package.json
├── catalog/
│   └── skill-set.json
├── skills/
│   ├── acs-diagnose-incident/
│   └── acs-fix-incident/  (planned, may not exist yet)
├── shared/
│   ├── workflows/
│   │   └── debugging.md
│   └── templates/
│       └── incident-report-template.md
└── README.md
```

### 2. Skills to Extract

1. **acs-diagnose-incident** — incident diagnosis
2. **acs-fix-incident** — incident fix (check if exists; may be planned)

### 3. Workflow to Bundle

From `system/workflows/`:
- `debugging.md` — debugging workflow (shared with test)

### 4. package.json

```json
{
  "name": "acs-maintain",
  "version": "0.4.0",
  "description": "ACS maintain phase - incident diagnosis and fixes",
  "main": "catalog/skill-set.json",
  "keywords": ["agent", "coding", "maintenance", "incident", "debugging"],
  "dependencies": {
    "acs-context": "^0.4.0"
  },
  "peerDependencies": {
    "acs-test": "^0.4.0"
  }
}
```

### 5. catalog/skill-set.json

List skills (1-2) with:
- Correct `id` (acs-*)
- Phase: `maintain`
- Dependencies:
  - Required: `acs-init-context`
  - Optional: `acs-debug`, `acs-triage-issue`

### 6. SKILL.md Updates

For each skill:
- Rewrite paths to `shared/` resources
- Declare dependencies:
  ```yaml
  dependencies:
    required:
      - acs-init-context
    optional:
      - acs-debug
      - acs-triage-issue
    phase: maintain
  ```

### 7. README.md

Document:
- Plugin purpose (incident response)
- Maintenance workflow: diagnose → fix
- Installation and usage examples
- Note: This phase is early; more skills planned

## Acceptance Criteria

- [ ] Plugin installs standalone with only acs-context
- [ ] All skills (1-2) pass validation
- [ ] Test: Run diagnose-incident on a bug scenario
- [ ] Incident report template generates correctly
- [ ] README documents current and planned skills

## Verification Script

```bash
cd /tmp/test-acs-maintain
npm install acs-context
npm install acs-maintain

find skills -name "SKILL.md" | wc -l  # Should be 1-2

# Test incident diagnosis
cd /tmp/repo-with-bug
# Run: acs-init-context
# Run: acs-diagnose-incident --issue "login fails on production"
# Verify: diagnosis report generated
```

## Notes

- Smallest plugin; may only have 1 skill currently
- **acs-fix-incident** may be planned but not implemented; verify
- Shares debugging workflow with test plugin
- Future expansion expected as maintain phase matures
