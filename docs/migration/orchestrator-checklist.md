# Orchestrator Verification Checklist

Last updated: 2026-09-22

## Pre-Dispatch

- [x] Dependency map created
- [x] 7 task specs written (tasks 01-07)
- [x] Dispatch script created
- [ ] Dispatch script executed
- [ ] 7 agents spawned and running

## During Execution (Monitor)

### Task 1: acs-context
- [ ] Agent spawned successfully
- [ ] Plugin directory created at `plugins/acs-context/`
- [ ] 5 skills extracted
- [ ] Protocols bundled
- [ ] package.json created (zero dependencies)
- [ ] catalog/skill-set.json created
- [ ] README.md complete
- [ ] Agent reports completion

### Task 2: acs-plan
- [ ] Agent spawned successfully
- [ ] Plugin directory created at `plugins/acs-plan/`
- [ ] 10 skills extracted
- [ ] Workflows bundled
- [ ] package.json created (depends on acs-context)
- [ ] catalog/skill-set.json lists 10 skills
- [ ] README.md complete
- [ ] Agent reports completion

### Task 3: acs-build
- [ ] Agent spawned successfully
- [ ] Plugin directory created at `plugins/acs-build/`
- [ ] 7 skills extracted
- [ ] Specialist agents bundled (tdd-executor, implementer)
- [ ] DAG scripts bundled
- [ ] package.json created
- [ ] catalog/skill-set.json lists 7 skills
- [ ] README.md complete
- [ ] Agent reports completion

### Task 4: acs-design
- [ ] Agent spawned successfully
- [ ] Plugin directory created at `plugins/acs-design/`
- [ ] 12 skills extracted
- [ ] Architecture specialists bundled (10+)
- [ ] package.json created
- [ ] catalog/skill-set.json lists 12 skills
- [ ] README.md complete
- [ ] Agent reports completion

### Task 5: acs-test
- [ ] Agent spawned successfully
- [ ] Plugin directory created at `plugins/acs-test/`
- [ ] 9 skills extracted
- [ ] Review specialists bundled (20+)
- [ ] package.json created
- [ ] catalog/skill-set.json lists 9 skills
- [ ] README.md complete
- [ ] Agent reports completion

### Task 6: acs-maintain
- [ ] Agent spawned successfully
- [ ] Plugin directory created at `plugins/acs-maintain/`
- [ ] Skills extracted (1-2)
- [ ] package.json created
- [ ] catalog/skill-set.json created
- [ ] README.md complete
- [ ] Agent reports completion

### Task 7: acs-authoring
- [ ] Agent spawned successfully
- [ ] Plugin directory created at `plugins/acs-authoring/`
- [ ] 5 skills extracted
- [ ] Scripts bundled
- [ ] package.json created
- [ ] catalog/skill-set.json lists 5 skills
- [ ] README.md complete
- [ ] Agent reports completion

## Post-Completion Verification

### Per-Plugin Checks
Run for each plugin:
```bash
cd plugins/<plugin-name>
# Check structure
ls -la
find skills -name "SKILL.md" | wc -l
find shared -type f | head -10

# Validate catalog
cat catalog/skill-set.json | jq '.skills | length'

# Check dependencies
cat package.json | jq '.dependencies'
```

### Standalone Installation Tests
For each plugin:
```bash
cd /tmp/test-<plugin>
npm install /path/to/plugins/<plugin>
# Verify installation succeeded
# Run representative skill
```

### Integration Test
Full lifecycle with all plugins:
```bash
cd /tmp/fresh-integration-test
git init
npm install acs-context acs-plan acs-design acs-build acs-test acs-maintain

# Test flow: plan → design → build → test
# Verify each phase works with only required dependencies
```

### Reconciliation

- [ ] Update root catalog/skill-set.json to list 7 plugins
- [ ] Archive `system/` as `legacy/system/`
- [ ] Update root README.md with new plugin structure
- [ ] Update CLAUDE.md with plugin installation instructions
- [ ] Update TODO.md to mark refactoring complete
- [ ] Run validation: `python3 system/memory/validate_suite.py` (if still applicable)

## Success Criteria

- [ ] All 7 plugins install independently
- [ ] Each plugin passes its acceptance criteria
- [ ] Full lifecycle works with all plugins
- [ ] Minimal workflow (context + build) works
- [ ] No hardcoded paths to source checkout
- [ ] Documentation updated

## Blocker Resolution

If any agent encounters blockers:
1. Check agent status: `herdr agent status <agent-name>`
2. Read agent transcript for errors
3. Resolve blocker (missing files, ambiguous structure)
4. Resume agent or dispatch new task
