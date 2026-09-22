# acs-context

Foundation plugin for the ACS (Agent Coding Skills) ecosystem. Provides shared memory and context infrastructure that all other ACS plugins depend on.

## Purpose

`acs-context` is the root of the ACS plugin dependency hierarchy. It defines the canonical context paths, memory protocols, and domain-modeling skills that every other plugin expects to find already in place. Install this plugin first.

## Zero dependencies

This plugin has no runtime dependencies on other ACS plugins. It is the root node in the dependency graph.

## Skills

| Skill | Role |
|---|---|
| `acs-init-context` | One-time repository setup — creates `docs/agents/memory.md`, configures canonical context paths, durable change records, and run scratch |
| `acs-manage-context` | Compatibility router for context setup, synchronization, and cross-runtime translation; delegates to focused skills for new integrations |
| `acs-sync-context` | Detects and repairs context drift after initial setup — use when routing is broken, domain context is stale, or working memory no longer matches repository state |
| `acs-translate-agent-context` | Preserves required agent behavior while translating instructions, skills, commands, hooks, and context between agent runtimes or host applications |
| `acs-engineer-domain-model` | Maintains shared domain language and durable architectural decisions (ADRs) — use when terms are vague or conflicting, or when a hard-to-reverse trade-off needs a record |

## Protocol files

The `protocols/` directory bundles the memory and coordination protocols that back these skills:

| File | Purpose |
|---|---|
| `context-coordination.md` | Rules for how skills coordinate reads and writes to shared context |
| `engineering-memory.md` | Durable engineering-decision memory schema |
| `product-memory.md` | Product-decision and requirement memory schema |
| `operations-memory.md` | Operational runbook and incident memory schema |
| `design-memory.md` | Design-decision and rationale memory schema |
| `orchestration.md` | Orchestration patterns and handoff contracts |
| `skill-declarations.md` | Canonical skill registration format |
| `registry.json` | Machine-readable skill registry |

## Installation

Install `acs-context` before any other ACS plugin. All downstream plugins (`acs-plan`, `acs-design`, `acs-build`, `acs-test`, `acs-maintain`, `acs-authoring`) assume its skills and protocols are already present.

```bash
# Copy plugin into your skills directory
cp -rP plugins/acs-context ~/.claude/plugins/acs-context
```

## Dependency hierarchy

```
acs-context          ← install first (this plugin)
├── acs-plan
├── acs-design
├── acs-build
├── acs-test
├── acs-maintain
└── acs-authoring
```

Every plugin in the hierarchy above depends on `acs-context` at runtime. None of them depend on each other.
