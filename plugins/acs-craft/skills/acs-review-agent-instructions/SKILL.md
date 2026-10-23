---
name: acs-review-agent-instructions
description: Use when AGENTS.md or CLAUDE.md needs an incident lesson, hierarchy repair, guidance pruning, or context routing repair.
---

# Review Agent Instructions

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [repository.instructions]
  retrieves: [context.configuration, repository.incident_evidence]
  produces: [context.instruction_findings]
  updates: [context.instructions]
  invalidates: [context.instruction_dependents]
  handoff_to: [coordinator]
```

Shared semantics: [shared protocol](../../resources/protocols/skill-declarations.md#skill-declarations); shared execution: [Coordination](../../resources/protocols/context-coordination.md). Apply their memory ownership and save-before-handoff rules; existing authorization persists. For human reports or review feedback, use [Presenter](../../resources/protocols/presenter.md); source records retain authority.


Own the requested `AGENTS.md` or `CLAUDE.md` and its context pointers. The file should contain only always-needed repository constraints and trigger-bearing pointers to canonical detail.

## 1. Triage

Choose the narrowest mode supported by the request:

| Signal | Mode |
| --- | --- |
| One concrete failure or repeated correction | Intake |
| Broad quality, size, hierarchy, or reliability concern | Review |
| Cold sessions cannot find shared context | Wire context |

When the signal is ambiguous and the difference changes edit scope, ask whether the user wants the single lesson recorded or the whole file reviewed. If both runtime files exist and the problem is parity rather than content quality, hand off to `acs-translate-agent-context`.

## 2. Inspect evidence

Read the requested file, the repository instructions that govern it, and every local document it points to. Inspect current configuration for commands and paths. For Intake, capture the failure, expected behavior, consequence, and available check. For Review, inspect relevant history when it can distinguish earned guidance from abandoned sediment.

Inspection is complete when every proposed change is grounded in an incident, a broken pointer, a canonical-ownership conflict, or a sentence that demonstrably fails to change behavior.

## 3. Apply the selected mode

### Intake

Before writing an instruction, choose the highest applicable rung that prevents the recorded failure. Inspect the repository's existing check commands and how they run; an existing check that is unwired or broken is the finding, not a reason to duplicate it. Record why each higher rung cannot prevent this failure.

| Rung, in order | Enforcement |
| --- | --- |
| Architecture | Remove the invalid path or give shared state one owner so the mistake cannot be expressed. |
| Types | Make the invalid state fail type checking. |
| Lint | Add a deterministic check whose error names the fix. |
| Test | Add a regression check at the relevant behavioral boundary. |
| Documentation | Only when no check is possible, record an explicit **instruction fallback** and why architecture, types, lint, and tests cannot enforce the lesson. |

Each new check must fail on the recorded mistake: use the old code or a faithful reproducer, verify the expected failure reason (not an import or setup error), then run the same check unchanged on the corrected code and require it to pass. Record the incident, chosen rung, exact command/result, tested revision or tree fingerprint, and timestamp under the [evidence contract](../../resources/protocols/orchestration.md#evidence-contract). Missing tools, permission, or a runnable reproducer leave the check incomplete; they do not establish that no check is possible.

For example, a lesson that a technically accurate review sounded dismissive can be an **instruction fallback**: architecture, types, lint, and tests cannot decide whether wording respects the reader in context. Record the observed wording and the desired respectful, concrete alternative; a word ban cannot enforce that judgment.

Route an instruction fallback or a pointer to enforcement at the narrowest scope:

| Lesson scope | Home |
| --- | --- |
| Every session in the repository | Root instruction file |
| One subtree | Nearest scoped instruction file supported by the runtime |
| Detailed procedure or reference | Canonical document or skill, with a trigger pointer |
| Active effort only | Configured run recovery entry or linked effort artifact |

For a fallback, write the minimum instruction that names the target behavior, reason or consequence, and manual verification. Keep the lesson and its enforcer or fallback rationale together in the owned record; a repeated lesson whose rule already exists is an enforcement finding. Make room by removing or disclosing weaker material from the same owned file. Preserve unrelated structure.

Intake is complete when the new check would have failed on the recorded failure and passes on the correction, or no check is possible and the instruction is explicitly marked as the fallback with its rationale. Any retained instruction or pointer lives at the narrowest correct scope and does not duplicate another canonical rule.

### Review

Audit every line against these criteria:

- **Relevance:** it changes repository-specific behavior at startup or routes to material that does.
- **Pointer:** the trigger says when to load a target, and the target resolves.
- **Ownership:** each fact and rule has one canonical home.
- **Checkability:** constraints name an observable boundary; executable enforcement is linked when it exists.
- **Positive target:** prohibitions name the required alternative and consequence.
- **Hierarchy:** universal instructions stay visible; branch-only detail is disclosed.
- **Headroom:** the file can absorb the next earned lesson without burying its routing and constraints.

Report numbered findings before a structural rewrite. Name exact evidence, behavior impact, and proposed disposition: keep, sharpen, move, merge, or delete. Ask for one approval over the numbered plan.

After approval, rewrite when hierarchy is the defect; patch when findings are local. Load [`references/writing-the-file.md`](references/writing-the-file.md) only for a rewrite.

Review is complete when every line passes the criteria, every moved fact has one canonical home, and every pointer resolves with a trigger.

### Wire context

When `docs/agents/memory.md` exists, add or repair:

- a pointer that tells agents when to read it;
- a startup sequence that resolves the active effort, reads the configured run recovery entry, and follows its minimum pointers;
- context pointers for relevant terminology, ADRs, and product intent.

Point to configured values instead of copying them. When memory routing is absent, hand off to `acs-init-context`; when it exists but its targets are stale, hand off to `acs-sync-context`.

Wiring is complete when a cold session can reach one concrete next action using only the instruction file and the targets it names.

## 4. Verify

Resolve every changed local link, execute literal commands where safe, confirm scoped instructions are placed at their intended boundary, and update `Last updated:` in each edited Markdown file. Report changed behavior and any findings owned by other files without editing those files.

The task is complete when the selected mode's criterion and all verification checks pass. Preserve commits for the user.
