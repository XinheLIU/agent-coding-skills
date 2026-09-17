# Runtime Parity Translation

Last updated: 2026-08-25

Load this after the agent-surface inventory. Preserve required behavior with the smallest verified destination; preserve mechanisms only when the target runtime consumes them.

The goal is not to preserve runtime-specific mechanisms as artifacts. Preserve the behavior they create so every agent the repo supports — named or unknown, interactive or headless, single-agent or delegated — can follow the same rules and complete the same workflows.

## Parity grades

| Grade | Meaning |
| --- | --- |
| `equivalent` | Target behavior and enforcement match the source requirement |
| `partial` | Required behavior remains, but scope, automation, timing, or enforcement is weaker |
| `missing` | No target behavior exists |

Every `partial` or `missing` result requires an explicit user decision.

## Capability-first mapping

Choose a target mechanism from the target's verified capability profile, not from its product name. At minimum, check:

- when context is loaded and refreshed;
- how skills, prompts, and references are discovered;
- how tools, commands, permissions, and sandboxes are invoked;
- whether delegation is native, subprocess-based, serialized, or unavailable;
- which state persists across turns, sessions, and processes;
- whether timing matters (startup, per-turn, pre/post tool, commit/CI, scheduled, or background execution).

If a requirement has no direct target primitive, preserve its observable behavior with the narrowest native binding and record the timing, scope, and enforcement difference in the parity grade. Do not invent a familiar path or lifecycle.

## Mechanism mapping

| Source behavior | Preferred destination |
| --- | --- |
| Cross-cutting instruction | Runtime-neutral entry instructions |
| Scoped instruction | Narrowest target-supported scoped instruction |
| Repeatable model workflow | Shared skill or playbook plus target discovery binding |
| Executable command | Repository script or tool plus a trigger pointer |
| Preventive hook or gate | Existing CI, pre-commit, or executable check framework, preserving trigger timing |
| Role prompt | Neutral prompt plus target-native custom-agent, launcher, or serialized binding |
| Runtime setting | Target runtime config when an equivalent control exists |

Choose paths from the repository and current target documentation. Hardcoded runtime layouts are examples, not a contract.

## Orchestrators

Separate an orchestrator into:

| Part | Canonical concern |
| --- | --- |
| Procedure | Shared steps, inputs, completion criteria, and aggregation contract |
| Roles | Specialized prompts and their required outputs |
| Control flow | Target-native spawning, steering, waiting, permissions, and timing |

Rank target strategies:

1. **Native delegation (`equivalent`).** Use the target's verified subagent workflow and custom-agent bindings.
2. **Subprocess delegation (`equivalent` or `partial`).** Use when the target exposes a stable non-interactive launcher but no in-session delegation.
3. **Serialized procedure (`partial`).** One agent performs the same bounded roles sequentially.
4. **Runtime-specific (`missing` elsewhere).** Retain the source and declare the unsupported targets.

Verify native capability in the installed target and its current documentation. A Codex-like host may provide native subagents, separate worker processes, or neither; the installed behavior is authoritative.

## Translation sequence

1. Create the neutral procedure and role content.
2. Create target bindings using documented load mechanisms.
3. Update concise entry pointers with their trigger conditions and timing.
4. Exercise the target behavior and compare enforcement, scope, timing, and output with the source requirement.
5. Remove or archive the source only after approved destination verification.

Translation is complete when every inventory row has a verified destination and parity grade, every target can discover its binding, and each duplicated runtime file names a synchronization mechanism.
