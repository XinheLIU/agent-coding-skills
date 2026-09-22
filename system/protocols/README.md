# Agent Coding Skills Protocol System

Last updated: 2026-09-20

## What Are Protocols?

Protocols are **shared contracts** that define how skills coordinate work, manage context, and exchange information. They're stable, versioned documents that multiple skills depend on.

Think of protocols as:
- **APIs between skills** — not code, but documented agreements
- **First-class citizens** — they live in `protocols/`, not buried in one skill's folder
- **Versioned contracts** — skills can declare which protocol versions they require

## Why Protocols Enable Modularity

**Before (broken):**
```markdown
[shared protocol](../../../craft/context/acs-init-context/references/PROTOCOL.md)
```

This relative path only works if both skills ship in the exact same directory tree. Install them as separate plugins → broken link.

**After (portable):**
```markdown
[shared protocol](protocol:acs:skill-declarations)
```

This logical ID resolves at skill-load time to wherever the protocol is actually installed. Skills can now ship separately.

## Available Protocols

### Core Coordination

- **`protocol:acs:skill-declarations`** — The six-field YAML context contract: `requires`, `retrieves`, `produces`, `updates`, `invalidates`, `handoff_to`
- **`protocol:acs:context-coordination`** — How the active agent assembles context, schedules work, reconciles contributions, and manages transitions

### Domain Memory Contracts

- **`protocol:acs:product-memory`** — Problem, intent, requirements, criteria, scope
- **`protocol:acs:design-memory`** — UX/UI decisions, contracts, prototypes, ADRs
- **`protocol:acs:engineering-memory`** — Implementation evidence, tests, verification
- **`protocol:acs:operations-memory`** — Environment, deployment, release decisions

### Delivery

- **`protocol:acs:orchestration`** — How `acs-implement` coordinates parallel ticket execution

## For Skill Authors

### Referencing a Protocol

Use the logical ID in markdown links:

```markdown
Shared semantics: [shared protocol](protocol:acs:skill-declarations)
```

With an anchor (optional):

```markdown
Return the [handoff envelope](protocol:acs:skill-declarations#handoff-envelope)
```

With a version constraint (future):

```markdown
Requires [protocol v1.x](protocol:acs:skill-declarations@1.x)
```

### Local vs Shared References

**Use a protocol when:**
- 2+ skills need the same contract
- The document defines coordination semantics
- Skills from different plugins depend on it

**Keep it local when:**
- Only 1 skill uses it
- It's skill-specific implementation guidance
- It doesn't define cross-skill contracts

Example: `acs-design-context/references/framework.md` is local — only that skill uses it. `protocol:acs:design-memory` is shared — all design skills read it.

## Resolution Algorithm

At skill-load time, `protocol:acs:NAME` resolves through this chain:

1. **Plugin protocols directory** — `<plugin-root>/protocols/NAME.md`
2. **Shared protocol cache** — `~/.agent-skills/protocols/acs/NAME@VERSION.md`
3. **Remote canonical URL** — `https://raw.githubusercontent.com/.../protocols/NAME.md` (cached)
4. **Inline fallback** — embedded minimal protocol (catalog only)

This allows:
- Local development (resolve from working tree)
- Separate plugin installs (resolve from peer dependency)
- Graceful degradation (fetch missing protocols remotely)

## Plugin Packaging Model

### Bundled protocols (v0.3.0+)

Each plugin carries only the protocols it needs. There is no shared protocol plugin or peer dependency — protocols are small, stable contracts, and bundling them alongside the skills that use them avoids cross-plugin install-order problems.

**Example: acs-build plugin structure:**
```
acs-build/
  protocols/
    skill-declarations.md
    engineering-memory.md
    orchestration.md
  workflows/
    build.md
    feature-delivery.md
  skills/
    acs-implement/
    acs-tdd/
    acs-plan-delivery/
```

**Protocol distribution by plugin:**

| Plugin | Protocols bundled |
| --- | --- |
| acs-plan | skill-declarations, product-memory |
| acs-design | skill-declarations, design-memory, product-memory |
| acs-build | skill-declarations, engineering-memory, orchestration |
| acs-test | skill-declarations, engineering-memory, orchestration |
| acs-context | skill-declarations, context-coordination |
| acs-authoring | skill-declarations |
| acs-deploy | skill-declarations, operations-memory |
| acs-maintain | skill-declarations, operations-memory |

### Plugin Manifests

Plugin manifests no longer declare `peerDependencies`. The `skills` field points to the local skills directory:

```json
{
  "name": "acs-build",
  "version": "0.3.0",
  "description": "Delivery planning, implementation, and TDD skills for the ACS suite.",
  "skills": "./skills/"
}
```

`system/protocols/` remains the canonical source of truth for the monolithic `agent-coding-skills` install.

## Creating a New Protocol

### 1. Identify the need

Create a protocol when:
- Multiple skills reference the same contract
- The contract defines coordination semantics
- Skills might ship in separate plugins

### 2. Add to registry

Edit `system/protocols/registry.json`:

```json
{
  "protocols": {
    "new-protocol-name": {
      "id": "protocol:acs:new-protocol-name",
      "title": "Human-Readable Title",
      "canonical": "protocols/new-protocol-name.md",
      "version": "1.0.0",
      "status": "stable"
    }
  }
}
```

### 3. Write the protocol

Create `system/protocols/new-protocol-name.md` with frontmatter:

```markdown
---
protocol: acs:new-protocol-name
version: 1.0.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/new-protocol-name.md
---

# Protocol Title

Last updated: YYYY-MM-DD

[Protocol content here]
```

### 4. Update skills

Replace relative references with the logical ID:

```markdown
Old: [contract](../../../path/to/contract.md)
New: [contract](protocol:acs:new-protocol-name)
```

### 5. Validate

```bash
python3 scripts/validate-protocols.py
```

## Versioning

Protocols use semantic versioning:

- **1.0.0** → **1.0.1** — clarifications, typos, non-breaking additions
- **1.0.0** → **1.1.0** — new optional fields, backward-compatible extensions
- **1.0.0** → **2.0.0** — breaking changes (removed fields, changed semantics)

Skills can declare version constraints:

```markdown
[protocol v1.x](protocol:acs:skill-declarations@1.x)
```

The resolver checks compatibility at load time.

## Status Levels

- **`stable`** — production-ready, won't break without a major version bump
- **`beta`** — functional but may change, use with caution
- **`draft`** — experimental, breaking changes expected
- **`deprecated`** — use `superseded_by` to point to replacement

## Migration from Relative Paths

The `scripts/migrate-protocol-refs.py` script automated the migration. If you need to update a skill manually:

**Before:**
```markdown
Shared semantics: [shared protocol](../../craft/context/acs-init-context/references/PROTOCOL.md#skill-declarations)
```

**After:**
```markdown
Shared semantics: [shared protocol](protocol:acs:skill-declarations)
```

Run validation to confirm:
```bash
python3 scripts/validate-protocols.py
```

## Implementation Status

✅ **Phase 1 complete:** Registry created, 7 protocols moved and versioned  
✅ **Phase 2 complete:** All 40+ skills migrated to logical IDs  
⏳ **Phase 3 in progress:** Build catalog integration  
⏳ **Phase 4 planned:** Plugin packaging and distribution

## See Also

- [Harness Architecture](../docs/harness-architecture.md) — Runtime integration boundaries
- [Build Catalog Script](../../scripts/build-catalog.mjs) — Catalog generation with protocol resolution
