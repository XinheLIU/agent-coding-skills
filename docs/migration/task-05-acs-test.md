# Task 05: Create acs-test Plugin

**Agent**: Test-Plugin-Agent  
**Priority**: P1 (depends on acs-context)  
**Estimated effort**: 4-5 hours

## Objective

Extract test and review skills into an independent `acs-test` plugin covering coverage, quality reviews, and debugging.

## Input Resources

- `system/skills-src/test/` — 8 skills
- `system/workflows/testing.md`, `debugging.md`
- Majority of review specialists from `system/agents/`

## Deliverables

### 1. Plugin Structure

```
plugins/acs-test/
├── package.json
├── catalog/
│   └── skill-set.json
├── skills/
│   ├── acs-analyze-test-gaps/
│   ├── acs-review-code-quality/
│   ├── acs-review-architecture/
│   ├── acs-review-design/
│   ├── acs-analyze-gaps/
│   ├── acs-triage-issue/
│   ├── acs-debug/
│   ├── acs-resolve-merge-conflict/
│   └── acs-generate-integration-tests/
├── shared/
│   ├── workflows/
│   │   ├── testing.md
│   │   └── debugging.md
│   ├── agents/
│   │   ├── code-reviewer.md
│   │   ├── auth-explorer.md
│   │   ├── auth-reviewer.md
│   │   ├── performance-explorer.md
│   │   ├── performance-reviewer.md
│   │   └── (20+ review specialists)
│   └── templates/
│       ├── review-findings-template.md
│       └── test-coverage-report.md
└── README.md
```

### 2. Skills to Extract

**Test Coverage**:
1. **acs-analyze-test-gaps** — identify test gaps
2. **acs-generate-integration-tests** — generate integration tests

**Code Review**:
3. **acs-review-code-quality** — code quality review (Standards, Patterns, Spec axes)
4. **acs-review-architecture** — architecture review
5. **acs-review-design** — design review (may be in design/)
6. **acs-analyze-gaps** — gap analysis (may be in design/)

**Debugging**:
7. **acs-triage-issue** — issue triage
8. **acs-debug** — debugging assistant
9. **acs-resolve-merge-conflict** — merge conflict resolution

### 3. Specialist Agents to Bundle

From `system/agents/` (majority of 26 files):
- code-reviewer.md
- All explorer/reviewer pairs:
  - auth-explorer/reviewer
  - performance-explorer/reviewer
  - reliability-explorer/reviewer
  - db-explorer/reviewer
  - api-explorer/reviewer
  - deploy-explorer/reviewer
  - data-architecture-explorer/reviewer
  - business-explorer/reviewer
  - application-explorer/reviewer
  - adr-explorer/reviewer

### 4. package.json

```json
{
  "name": "acs-test",
  "version": "0.4.0",
  "description": "ACS test phase - coverage, review, debugging",
  "main": "catalog/skill-set.json",
  "keywords": ["agent", "coding", "testing", "review", "debugging"],
  "dependencies": {
    "acs-context": "^0.4.0"
  },
  "peerDependencies": {
    "acs-build": "^0.4.0"
  }
}
```

### 5. SKILL.md Updates

For each skill:
- Rewrite paths to `shared/` resources
- Update agent references to `shared/agents/`
- Declare dependencies:
  ```yaml
  dependencies:
    required:
      - acs-init-context
    optional:
      - acs-implement  # for implementation context
      - acs-tdd  # for test evidence
    phase: test
  ```

### 6. README.md

Document:
- Plugin purpose (testing and quality assurance)
- Review workflow: test gaps → review → debug
- Skill inventory
- Specialist agents and their domains
- Installation and usage examples

## Acceptance Criteria

- [ ] Plugin installs standalone with only acs-context
- [ ] All 9 skills pass validation
- [ ] 20+ review specialists bundled correctly
- [ ] Test: Run review flow (analyze-test-gaps → review-code-quality)
- [ ] Debug workflow works for issue triage
- [ ] Merge conflict resolution works standalone
- [ ] README complete with review examples

## Verification Script

```bash
cd /tmp/test-acs-test
npm install acs-context
npm install acs-test

find skills -name "SKILL.md" | wc -l  # Should be 9
find shared/agents -name "*.md" | wc -l  # Should be 20+

# Test review flow
cd /tmp/existing-repo-with-code
# Run: acs-init-context
# Run: acs-analyze-test-gaps
# Verify: test gap report generated
# Run: acs-review-code-quality
# Verify: review findings reported
```

## Notes

- This is the largest plugin by specialist agent count
- **acs-review-design** and **acs-analyze-gaps** may overlap with design/; verify location
- Code reviewer is the core agent; ensure it's correctly bundled
- Review findings use structured output; verify templates are included
