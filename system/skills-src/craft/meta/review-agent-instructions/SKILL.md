---
name: review-agent-instructions
description: >
  Write and maintain a repository's agent instruction file — CLAUDE.md or
  AGENTS.md — and keep it wired to the memory system. Triage first: fold in a
  single lesson after an incident, review and rewrite a file whose shape has
  decayed, or reconnect a file that no longer routes to memory. Use when asked
  to review, audit, shrink, or restructure CLAUDE.md / AGENTS.md, or to record
  a lesson in one. Not for rule extraction (`extract-rules`), cross-runtime
  translation (`translate-agent-context`), doc-tree structure
  (`scaffold-agent-docs`), or drift detection (`manage-context` Phase B).
---

# Review Agent Instructions

Last updated: 2026-08-06

**Announce at start:** "I'm using the review-agent-instructions skill on your instruction file."

## What This Skill Owns

One file — `CLAUDE.md` or `AGENTS.md`, whichever the repo has — plus its pointers into the memory system. The file's job is **index plus common sense**: what the agent must know the moment it starts, and where to look for everything else.

This is the **constraint** link in the reliability chain. Comprehension (`document-codebase`, `index-codebase`) makes the agent *see*; constraint makes it *obey*; verification (tests, CI) makes it *checkable*. Two consequences shape every decision below: you cannot write a constraint more precise than your understanding of the code, and a constraint nothing can check is not a constraint. It is also the only link that **learns** — assets get regenerated and gates get written against known failures, but this file is where an unanticipated failure becomes a rule.

Not this skill's business: the doc tree's shape (`scaffold-agent-docs`), rule bodies (`extract-rules`), runtime portability (`translate-agent-context`), whether claims still match the code (`manage-context` Phase B).

## Triage First

Read the request before reading the file. Three modes, cheapest first:

| Signal | Mode |
| --- | --- |
| A specific thing went wrong — a regression, a bad agent edit, a correction repeated twice | [Intake](#mode-1--intake) |
| "Review it", "it's too long", "the agent ignores it", no specific incident | [Review](#mode-2--review) |
| Sessions start cold, pointers are dead, the file never says where state lives | [Wire Memory](#mode-3--wire-memory) |

Ambiguous requests are usually Intake wearing Review's clothes. "Fix CLAUDE.md, the agent keeps reformatting my imports" is one lesson, not an audit. Ask which it is rather than restructuring 200 lines to add one.

Then check which file exists: `CLAUDE.md` (Claude-only repo), `AGENTS.md` (multi-runtime; also carries an Agent Surface section). Both present and in conflict is a parity problem — handle the one asked about and flag the other for `translate-agent-context`. Neither present → `scaffold-agent-docs`.

## Mode 1 — Intake

The common case. An append, not an audit.

1. **Get the failure concrete.** What broke, what the agent did, what it should have done instead. A lesson you cannot state concretely is not ready to write down.
2. **Route it by layer before writing.** Not everything belongs in this file:

   | The lesson is… | Home |
   | --- | --- |
   | A cross-cutting fact or prohibition every session needs | this file |
   | A coding rule with a body (naming, formatting, API shape) | `extract-rules` → rules file, linked from here |
   | Scoped to one subtree | subdirectory `AGENTS.md` / scoped file |
   | A long procedure or reference detail | `docs/`, with a pointer here |
   | True only of the work in flight | working memory (`state.md`), not here |

3. **Write one line, in the section that owns it.** Reason, rule, alternative — phrased so something could check it:

   ```markdown
   <!-- unverifiable, no alternative, no reason -->
   - Be careful when modifying the order service.

   <!-- checkable -->
   - `OrderService.calculateTotal` is called by the settlement batch job, which has
     no test coverage. Changing its signature breaks settlement silently — add a
     characterization test in `tests/settlement/` before touching it.
   ```

4. **Make room if there isn't any.** Evict before appending — see [the budget](#the-budget-is-the-point).
5. Update `Last updated`, then report what was added and how much room is left.

Do not restructure anything else. If the file is too broken to accept a line, say so and offer Review as a separate pass.

## Mode 2 — Review

Read the file and everything it points at, then judge it against [the five principles](#the-five-principles). Read its git history when available (`git log --follow`) — a file with three commits after a year of development is abandoned, not stable, and that is the finding worth reporting.

Report before touching anything. No fixed template — say what is wrong in whatever form fits, but always cover:

- **Size against budget**, and what would be evicted first.
- **Lines that change no behavior** — prose restating the architecture diagram, generic advice, origin story, filler intros like "This file provides guidance to Claude Code".
- **Constraints nothing can check** — quote them; they are unenforced today.
- **Rules with no incident behind them** — ask what breaks if the line is deleted. No answer means delete.
- **Facts stated in more than one place** — name the single home each should have. Where the duplicate lives in a doc this skill does not own, report it and hand off rather than editing.
- **Dead or unexplained pointers** — a path that no longer resolves, or a reference that never says *when* to read the target.
- **Structure** — sections in a sane order, nothing that is a heading plus one orphan bullet, rule-shaped content flagged for `extract-rules` rather than rewritten here.

Then ask: **"Apply these? (yes / yes but skip N / no)"**

Rewrite rather than patch when the shape itself is the problem — a file reorganized incrementally keeps the layout that failed. Preserve every non-obvious decision and historical reason; move them, never drop them. Verify pointers resolve afterward, and leave room for the next lesson.

## Mode 3 — Wire Memory

The file reads fine but sessions still start cold. Three connections carry that weight, and this skill keeps them accurate:

- **Startup sequence** — how a session gets oriented: run the init script, read recent `git log`, read `state.md`, follow its pointers. Written by `manage-context` Phase A; verify it is present and still true.
- **Memory routing pointer** — a short section pointing at `docs/agents/memory.md`, where the work root, tracker, and layer configuration actually live. Point at it; never restate its contents, and never edit that file.
- **Context Files table** — path plus the trigger that should make an agent open it. A pointer with no trigger gets ignored; so does a table listing every file in the repo.

Never delete these pointers to save room. Removing them makes the wiki and working layers invisible, which costs far more than the lines. Over budget with pointers intact is the right trade — push the detail into `docs/`.

If routing does not exist at all, this is the wrong skill: run `manage-context` Phase A first.

## The Five Principles

Everything above reduces to these. When a case is not covered, reason from them.

1. **Index plus common sense.** Every line is either something the agent needs at startup or a pointer into `docs/`. Anything else, delete. Never rewrite an asset that already exists — link the diagram, the API list, the schema.
2. **Earned by experience.** A rule earns its line when something went wrong without it. Speculative rules written to look thorough dilute the ones that matter.
3. **Checkable.** State each constraint so a test, linter, CI gate, or reviewer could decide whether it was violated. Name the check when one exists: "response shapes of `/api/v1/*` are frozen — `tests/contract/` covers them."
4. **Alternatives, not just prohibitions.** Every "don't" names what to do instead, and why. A prohibition without an alternative gets worked around.
5. **Room to grow.** A file with no headroom cannot absorb the next lesson, and the loop that keeps it valuable breaks silently.

## The Budget Is the Point

Roughly 200 lines for `CLAUDE.md`, 220 for `AGENTS.md`. These are budgets, not validation rules — a 210-line file that earns every line is fine; a 150-line file of generic advice is not. What matters is the pressure: past this size the file stops being read, so every addition should displace something.

When a lesson does not fit, in order: delete rules principle 2 cannot justify → compress prose into an index row → move subtree-scoped rules into a scoped file → move detail into `docs/` and keep the pointer. Raising the budget is not on the list.

## Guardrails

- Never delete a non-obvious decision or historical reason to save room — move it.
- Never invent structure the comprehension assets do not support. Leave the section thin and name the gap.
- Never rewrite rule bodies, port runtime mechanisms, or reorganize the doc tree — hand off.
- Never edit `docs/agents/memory.md`.
- Never run a full restructure to add one line.
- Update `Last updated:` on every file touched. Do not commit.

## Handoffs

| Situation | Skill |
| --- | --- |
| Architecture, API, or data-model assets missing — constraints stay unwritable without them | `document-codebase`, `index-codebase` |
| Rule-shaped content found in prose | `extract-rules` |
| No memory routing exists yet | `manage-context` Phase A |
| Claims no longer match the code | `manage-context` Phase B |
| `CLAUDE.md` and `AGENTS.md` out of parity, or Claude-only mechanisms need porting | `translate-agent-context` |
| Doc tree itself is disorganized | `scaffold-agent-docs` Mode B |

For section-by-section guidance during a rewrite, load [writing-the-file.md](references/writing-the-file.md).
