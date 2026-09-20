# Migration Guide

## v0.2.x → v0.3.0

v0.3.0 restructures the plugin set to align with the [AI-native SDLC playbook](https://claude.com/blog/the-ai-native-sdlc-playbook) six-phase model.

### Breaking changes

**Plugin renames and splits:**

| Old plugin | New plugin(s) |
| --- | --- |
| `acs-quality` | `acs-test` |
| `acs-craft` | `acs-context` + `acs-authoring` |

**Removed plugins:**

| Removed | Reason |
| --- | --- |
| `acs-protocols` | Protocols and workflows bundled into each phase plugin |
| `context-management` | Duplicate removed; use `acs-context` |

**No skill names changed.** All `acs-*` skill IDs, invocation triggers, and behavior are identical. Only the plugin that packages them changed.

### How to upgrade

If you installed individual plugins:

```bash
# Remove old plugins
npx skills remove acs-quality acs-craft context-management acs-protocols -g

# Install new replacements
npx skills install /path/to/agent-coding-skills/plugins/acs-test -g
npx skills install /path/to/agent-coding-skills/plugins/acs-context -g
npx skills install /path/to/agent-coding-skills/plugins/acs-authoring -g
```

If you installed the monolith:

```bash
npx skills remove agent-coding-skills -g
npx skills install /path/to/agent-coding-skills/system -g
```

### New plugin structure

```
plugins/
├── acs-plan/       Product discovery and intent (11 skills)
├── acs-design/     Requirements, UX, technical design (11 skills)
├── acs-build/      Delivery planning and implementation (3 skills)
├── acs-test/       Verification, review, and debugging (9 skills)
├── acs-deploy/     Release and governance (roadmap)
├── acs-maintain/   Incident diagnosis and operations (1 skill)
├── acs-context/    Agent context lifecycle (5 skills)
└── acs-authoring/  Skill authoring and meta-skills (5 skills)
```
