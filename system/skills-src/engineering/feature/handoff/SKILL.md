---
name: handoff
description: Preserve the current work for a fresh agent session using the shared memory protocol. Use before a context reset, when branching into research or a prototype, or when transferring an active effort.
---

# Handoff

Last updated: 2026-08-16

**Announce at start:** "I'm using the handoff skill to preserve context for the next session."

Capture the current effort's state into a handoff document that a cold session can act on without re-reading the full history. Reads both the feature artifacts in the worktree and the working memory in `.scratch/`.

---

## Inputs

Read in this order:

1. `docs/agents/memory.md` — resolve the work root and active effort slug.
2. `.scratch/<effort>/state.md` — current posture, next action, blockers, pointers.
3. `.scratch/<effort>/progress.md` — recent session log (last 3–5 entries).
4. `.scratch/<effort>/specs/*.md` — design initiatives, if any.
5. `.scratch/<effort>/tasks/*.md` — claimed or in-progress task files, if any.
6. Feature artifacts via `state.md` Pointers — `specs/NNN-name/spec.md`, `plan.md`, `tasks.md` (read only the sections needed: status, open tasks, current phase).

If `docs/agents/memory.md` is absent, use the current branch name as the effort slug and `.scratch/` as the work root.

---

## Output

Write `<work-root>/<effort>/handoffs/YYYYMMDD-HHMM-<focus>.md` where `<focus>` is a 2–3 word description of the current sub-task (e.g., `auth-middleware`, `api-contracts`).

Structure:

```markdown
# Handoff: <focus>

Date: YYYY-MM-DD HH:MM
Effort: <effort-slug>
Branch: <branch-name>

## Objective
<One sentence: what is the overall feature or effort trying to achieve.>

## Current status
<Two to four sentences: what was done in this session, where it landed.>

## Confirmed decisions
- <Decision and its rationale — point to ADR or spec section if it exists.>

## Open questions
- <Unresolved questions that block or shape the next step.>

## Blockers
<What is preventing progress. "none" if nothing.>

## Next concrete action
<One specific action — enough to start without reading anything else. Name the file and the change.>

## Source pointers
- Working memory state: `.scratch/<effort>/state.md`
- Feature spec: `specs/NNN-name/spec.md` (section X if relevant)
- Task list: `specs/NNN-name/tasks.md` (phase Y, next unchecked task)
- Active task files: `.scratch/<effort>/tasks/` (list any `in-progress` or `review` tasks)
- Code: <file:line for the most relevant context>
- Verification: <last known test run result or `n/a`>

## Suggested skills for the receiving session
- <skill-name> — reason
```

Reference existing artifacts instead of duplicating them. Redact secrets and personal data. Keep the handoff under 60 lines — it is a pointer document, not a transcript.

---

## After writing

Update `.scratch/<effort>/state.md`:

- Set `## Status` to "Handoff written — session ended."
- Set `## Next action` to the same text as `## Next concrete action` in the handoff.
- Add a pointer under `## Pointers`: `- Handoff: .scratch/<effort>/handoffs/<filename>.md`
- Append to `progress.md`:
  ```
  ## YYYY-MM-DD — Handoff to <focus>
  Session ended. Wrote handoff at handoffs/<filename>.md. Next: <one-line summary of next action>.
  ```

Do not commit.
