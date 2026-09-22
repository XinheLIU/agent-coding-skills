# Task 01: Create acs-context Plugin

**Agent**: Context-Plugin-Agent  
**Priority**: P0 (required by all other plugins)  
**Estimated effort**: 2-3 hours

## Objective

Extract the foundational context/memory infrastructure into an independent `acs-context` plugin that all other phase plugins will depend on.

## Input Resources

- `system/skills-src/context/` — 5 skills
- `system/protocols/` — shared protocol definitions
- Context skill references in `system/skills-src/context/*/references/`

## Deliverables

### 1. Plugin Structure

```
plugins/acs-context/
├── package.json
├── catalog/
│   └── skill-set.json
├── skills/
│   ├── acs-init-context/
│   ├── acs-manage-context/
│   ├── acs-translate-agent-context/
│   ├── acs-sync-context/
│   └── acs-engineer-domain-model/
├── protocols/
│   ├── memory-contract.md
│   ├── context-coordination.md
│   └── engineering-memory.md
└── README.md
```

### 2. Skills to Extract

1. **acs-init-context** — one-time repository setup
2. **acs-manage-context** — context lifecycle management
3. **acs-translate-agent-context** — cross-harness translation
4. **acs-sync-context** — memory synchronization
5. **acs-engineer-domain-model** — domain glossary and ADR (may move to design later)

### 3. Protocol Files to Bundle

From `system/protocols/`:
- Memory contract definitions
- Context coordination rules
- Engineering memory structure

From `system/skills-src/context/*/references/`:
- `agent-surface.md` — capability profile
- `runtime-parity-translation.md`
- `product-memory.md`
- `canonical-doc-layout.md`

### 4. package.json

```json
{
  "name": "acs-context",
  "version": "0.4.0",
  "description": "ACS foundational context and memory infrastructure",
  "main": "catalog/skill-set.json",
  "keywords": ["agent", "coding", "context", "memory"],
  "dependencies": {},
  "peerDependencies": {}
}
```

### 5. catalog/skill-set.json

List all 5 skills with:
- Correct `id` (acs-*)
- Phase: `context`
- Dependencies: none (foundation layer)

### 6. README.md

Document:
- Plugin purpose (foundation for all ACS phases)
- Skill inventory with one-line descriptions
- Installation: `claude plugin install acs-context`
- Usage: initialize with `/acs-init-context` in target repository

## Acceptance Criteria

- [ ] Plugin installs standalone: `cd plugins/acs-context && npm link`
- [ ] All 5 skills pass validation
- [ ] No external dependencies (foundation layer)
- [ ] Protocol files resolve from plugin root
- [ ] Relative paths in SKILL.md rewritten to plugin-relative
- [ ] README documents all skills
- [ ] Test: Run `/acs-init-context` in a fresh repo, verify `docs/agents/memory.md` created

## Verification Script

```bash
# In isolated directory
cd /tmp/test-acs-context
git clone <path-to-plugins/acs-context> .
npm link

# Verify skills discoverable
find skills -name "SKILL.md" | wc -l  # Should be 5

# Test acs-init-context
cd /tmp/fresh-repo
git init
# Invoke skill via test harness
# Verify docs/agents/memory.md created
```

## Notes

- **acs-engineer-domain-model** currently in context/; consider moving to design/ if it's domain-specific rather than infrastructure
- Zero dependencies — this is the foundation everything else builds on
- Protocol files may need consolidation; avoid duplication across skills
