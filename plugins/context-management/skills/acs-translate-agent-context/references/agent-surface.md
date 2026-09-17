# Agent Surface Inventory

Last updated: 2026-08-25

Load this before translating runtime-specific behavior. Inventory consumers and load mechanisms from current runtime documentation and local configuration; runtime conventions change.

## Surface classes

| Class | Examples | Inventory question |
| --- | --- | --- |
| Entry instructions | `AGENTS.md`, `CLAUDE.md`, scoped instruction files | Which runtime loads it, at what scope? |
| Skills | `SKILL.md` packages and plugin-provided skills | How is it discovered or explicitly invoked? |
| Roles | Runtime agent manifests, role prompts | Is the prompt shared? How is the role spawned? |
| Commands | Slash commands, prompt files, scripts | Is the behavior instructional or executable? |
| Enforcement | Hooks, CI, pre-commit, permission policy | What bad state does it prevent? |
| Runtime config | `.claude/`, `.codex/`, `.cursor/`, and equivalents | Is this a true runtime toggle or hidden behavioral guidance? |
| Neutral implementation | scripts, `tools/`, shared docs | Which runtime-specific binding points here? |

Search the repository for configured runtime roots rather than assuming this list is exhaustive.

## Capability profile

Runtime names are labels, not translation rules. For every source and target, add a
short capability profile before selecting a binding:

```text
Instruction loading: automatic | explicit | mixed | unknown
Skill/package discovery: native | plugin | path-based | prompt-only | unknown
Tool execution: native tools | shell/API | external bridge | advisory only
Delegation: in-session agents | subprocesses | serialized only | unavailable
Lifecycle: startup | per turn | pre/post tool | commit/CI | scheduled/background
Persistence: turn | session | project | external store | none
Enforcement: hook/policy | CI/check | advisory | unknown
```

Derive the profile from repository files, installed commands, and current target
documentation. Do not infer that an unlisted runtime behaves like Claude, Codex,
or any other familiar host. A capability marked `unknown` is a verification task,
not permission to choose a fallback silently.

## Inventory record

For every relevant surface, record:

```text
Path:
Consumer:
Load mechanism:
Behavior:
Canonical content owner:
Required targets:
Enforcement: executable | advisory
Disposition: keep | translate | archive | remove
```

The inventory is complete when every surface is recorded once and every supported runtime has an explicit entry path to the behaviors it requires.

## Canonical-home rules

- Cross-cutting repository instructions live in the runtime-neutral entry file supported by the repository.
- Subtree-specific instructions live at the narrowest supported scope.
- Reusable workflow instructions live in skills or a shared playbook.
- Role content lives in one neutral prompt when runtime bindings can reference it; otherwise each required copy names its canonical source and synchronization check.
- Executable behavior lives in scripts or tools. CI or the repository's existing check framework preserves enforcement.
- True runtime controls stay in runtime config.

An enforced hook translated only into prose is `partial`, not `equivalent`.

## Runtime-specific vs runtime-neutral

- Rules every agent must follow belong in the runtime-neutral entry file supported by the repository.
- Role prompts belong in `agents/`; executable integrations belong in `tools/` or scripts.
- True runtime controls stay in the target's own configuration.
- Runtime-specific automation may remain under its host directory when the behavior is intentionally host-only; label that choice and its consumer.

Do not invent a new host-specific subtree for content that belongs in a neutral prompt,
tool, or instruction file.
