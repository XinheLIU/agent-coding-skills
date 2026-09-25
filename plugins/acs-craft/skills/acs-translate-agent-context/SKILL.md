---
name: acs-translate-agent-context
description: >
  Preserve required agent behavior while translating instructions, skills,
  commands, hooks, roles, and context between agent runtimes or host applications.
  Use for runtime migration, parity, or drift across any named or unknown agent
  system, including Codex-like hosts. Classify source and target by verified
  discovery, tools, delegation, permissions, persistence, enforcement, and
  lifecycle or timing rather than by brand. Use `acs-review-agent-instructions` for
  content quality alone.
---

# Translate Agent Context

Last updated: 2026-09-25

## Context contract

```yaml
context:
  requires: [context.source_behavior, runtime.target_capabilities]
  retrieves: [context.configuration]
  produces: [context.parity_report]
  updates: [context.runtime_bindings]
  invalidates: [context.runtime_assumptions]
  handoff_to: [coordinator]
```

Shared semantics: [shared protocol](../acs-init-context/references/PROTOCOL.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


Translate required behavior, not filenames or brand-specific conventions. The source remains available until its destination exists and passes an equivalent check.

## 1. Classify the surfaces

Before choosing a destination, identify the source and target capabilities. Record
which class applies to each runtime or host:

| Capability class | Questions to answer |
| --- | --- |
| Context loader | What is loaded automatically, at what scope, and at what session or turn boundary? |
| Package discovery | How are skills, plugins, prompts, and references found or explicitly invoked? |
| Tool and command surface | Are actions instructional, executable, API-backed, shell-based, or mediated by permissions? |
| Delegation | Can the host spawn, steer, wait for, and aggregate other agents, or only start subprocesses? |
| Lifecycle and timing | Does behavior run at startup, per turn, before/after a tool, on commit, on a schedule, or in the background? |
| State and persistence | Which context survives turns, sessions, processes, and machines? |
| Enforcement and safety | Can checks be enforced by hooks, policy, CI, or only described as guidance? |

Treat runtime names as examples and aliases, not as a closed registry. If a target's
capabilities or timing are unclear, inspect its local configuration and current
documentation before mapping it. Preserve the user's terminology and intent while
translating the mechanism into the target's native form.

## 2. Inventory behavior

Confirm source runtime, target runtimes, and the behaviors that must remain available. Load [`references/agent-surface.md`](references/agent-surface.md), then inventory every relevant instruction file, scoped rule, skill, command, hook, role prompt, script, and runtime config.

For each surface record its path, consumer, load mechanism, behavior, canonical content owner, and target-runtime requirement. Inventory is complete when every discovered surface is either in the translation map or explicitly runtime-specific by intent.

## 3. Map mechanisms

Load [`references/runtime-parity-translation.md`](references/runtime-parity-translation.md). For each required behavior, record:

| Source | Behavior | Canonical destination | Target binding | Parity | Verification |
| --- | --- | --- | --- | --- | --- |

Use `equivalent`, `partial`, or `missing` for parity. Keep shared content in one runtime-neutral home and make runtime bindings point to it where the runtime permits. Keep genuinely different control flow in runtime-specific bindings behind one shared contract.

Treat skills that dispatch roles or parallel workers as orchestrators. Separate their shared procedure, role prompts, and runtime control flow before choosing the target binding. Mapping is complete when every required behavior has a destination, verification method, and explicit parity grade.

## 4. Approve trade-offs

Present the translation map before writes. Ask for a decision when an artifact requires a dependency, a mechanism downgrade, a runtime-specific duplicate, a symlink migration, or removal of the source. Prefer the smallest edit surface that achieves equivalent behavior.

Approval is complete when each non-equivalent row and destructive disposition has an explicit user decision.

## 5. Apply destination first

Create or update canonical neutral content, then target-runtime bindings, then concise routing pointers in `AGENTS.md` or the runtime's native index. Preserve existing target content and resolve collisions deliberately.

For shared skill directories, populate and verify the canonical target before replacing discovery paths with symlinks. For orchestrators, implement the approved runtime control flow while keeping the shared contract and role content outside that binding.

Application is complete when every destination exists and each target runtime can discover it through its actual load mechanism.

## 6. Verify parity

Exercise the verification recorded for every map row. Confirm executable checks remain executable, scoped rules retain their scope, commands reach the same outcome, and orchestration preserves required roles and aggregation. Advisory prose counts as a downgrade from an enforced hook or check.

After destination verification, archive or remove a source only when the approved plan named that disposition. Update agent-surface routing and `Last updated:` dates for all edited Markdown.

Translation is complete when every required behavior is `equivalent` or has an approved downgrade, every runtime-specific artifact names its consumer, all pointers resolve, and no unapproved source was removed. Use `acs-review-agent-instructions` afterward only when the resulting instruction file needs a separate content review. Leave commits to the user.
