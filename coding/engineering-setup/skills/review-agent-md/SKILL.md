---
name: review-agent-md
description: >
  Audit and restructure AGENTS.md and every file it references. Direct parallel
  to `review-claude-md` but for AGENTS.md (Codex / OpenCode / Cursor). Produces
  a MECE rewrite to a canonical 9-section skeleton (with an Agent Surface table)
  and a 220-line ceiling. Use when the user asks to "review AGENTS.md", "audit
  AGENTS.md", "shrink AGENTS.md", "deduplicate AGENTS.md context docs", or
  "restructure AGENTS.md to canonical form". Does NOT translate Claude-specific
  surfaces (slash commands, hooks, .claude/rules/, orchestrator skills) to
  agent-agnostic form — see `translate-agent-context`. Does NOT extract or
  document agent-behavior rules — see `extract-rules`.
disable-model-invocation: true
---

# Review AGENTS.md

Last updated: 2026-05-08

**Announce at start:** "I'm using the review-agent-md skill to audit your AGENTS.md."

## Goal

Audit `AGENTS.md` and every file it references. Produce a concrete change list, then apply on user confirmation. This skill owns the **content shape** of AGENTS.md — its canonical structure, the Agent Surface table, the docs it links to, and dedup across that set. It does not own rules extraction or cross-runtime translation.

## Scope: What This Skill Owns

| In scope (this skill) | Out of scope — handoff |
|---|---|
| AGENTS.md structure & content audit | Cross-runtime translation (CLAUDE.md ↔ AGENTS.md) → `translate-agent-context` |
| Canonical 9-section skeleton + Agent Surface table | Rule extraction & routing (static / dynamic / implicit) → `extract-rules` |
| Subdirectory `AGENTS.md` cleanup | CLAUDE.md content rewrite → `review-claude-md` |
| `agents/`, `tools/` placement clarity | Orchestrator decomposition → `translate-agent-context` |
| MECE dedup across AGENTS.md and its referenced docs | Slash command / hook portage → `translate-agent-context` |

If the audit surfaces rule-shaped content embedded in AGENTS.md prose, **flag it** for eviction — do not rewrite the rule body here. Recommend `extract-rules` to triage it. If the audit reveals cross-runtime parity gaps (e.g., behaviors carried only by Claude-specific surfaces), recommend `translate-agent-context`.

## Workflow

### Step 1 — Inventory

1. Read `AGENTS.md` in full.
2. Collect every file path mentioned anywhere: inline code paths, links, tables (especially the `Agent Surface` rows), comments, examples.
3. Read each collected file in full.
4. Record `exists`, `missing`, or `empty` for each path.
5. Also record subdirectory `AGENTS.md` files in the repo (these are subtree-scoped rules and part of the audit surface).

### Step 2 — Cross-File MECE Analysis

Map the full content landscape across AGENTS.md and every referenced file. For each piece of information, ask: is this the single canonical home, or does it duplicate another file?

Build a content ownership map:

```text
Topic -> owned by <file> | duplicated in <file-a>, <file-b>
```

Common MECE violations:

- Same commands appear in both `AGENTS.md` and a referenced doc.
- Architecture is described in both `AGENTS.md` and a doc file.
- Setup steps split across multiple files without clear ownership.
- Two doc files cover overlapping subsystems with no clear boundary.
- A doc file is two unrelated topics stapled together.
- Subdirectory `AGENTS.md` repeats content already in the root `AGENTS.md`.
- Rules duplicated across `AGENTS.md` and runtime-specific dirs (`.cursor/rules/`, `.claude/rules/`) without naming a canonical home.

### Step 3 — Per-File Analysis Against the 12 Principles

For `AGENTS.md` and each referenced file, record each issue as:

- `File`
- `line range`
- `principle #`
- `problem` (one sentence)
- `fix` (concrete action)

#### The 12 Principles

1. **Less Is More** — `AGENTS.md` should usually land in 60–300 lines. Delete anything a competent engineer can infer from reading the repo.
2. **Be Specific, Not Generic** — every sentence must change agent behavior. If covering the line changes nothing, delete it.
3. **Encode Style via Tooling** — replace prose style rules with formatter or linter commands whenever tooling can enforce them.
4. **WHY → WHAT → HOW** — non-obvious rules need the reason, the rule, and the exact alternative command or file to use.
5. **Progressive Disclosure** — `AGENTS.md` is the entry point only. Every cross-reference must say *when* to read the target file.
6. **Alternatives Not Just Prohibitions** — every "don't" rule must say what to do instead.
7. **Living Sync** — after structural changes, verify referenced paths still exist, commands still run, the `Agent Surface` table matches the repo.
8. **Hierarchical Structure** — rules scoped to one subdirectory or one agent belong in a narrower local context file (subdirectory `AGENTS.md`), not the root.
9. **Git Discipline** — include commit/branch/PR rules only when the repo truly has a non-default convention.
10. **Factor Repetition** — if the same multi-step workflow appears twice, extract it into a script, command, or one canonical doc.
11. **Live Context over Static Text** — facts that change often should be commands the agent can run, not prose snapshots.
12. **MECE** — each fact has one canonical home; each file has one clear purpose.

### Step 4 — Audit Report

Produce the report using this template:

```markdown
## AGENTS.md Audit Report

### Summary
- AGENTS.md: <N> lines
- Referenced files: <list — exists/missing>
- Subdirectory AGENTS.md files: <list>
- MECE violations: <count>
- Other issues: <count>
- Rule-shaped content to evict (handoff to extract-rules): <count>
- Cross-runtime parity gaps (handoff to translate-agent-context): <count>

### Content Ownership Map
| Topic          | Canonical Home | Also appears in |
| -------------- | -------------- | --------------- |
| Setup commands | AGENTS.md      | docs/setup.md   |

### MECE Violations
| #   | Topic       | Files                     | Problem             | Fix                       |
| --- | ----------- | ------------------------- | ------------------- | ------------------------- |
| 1   | Setup steps | AGENTS.md + docs/setup.md | Duplicated verbatim | Remove from docs/setup.md |

### Per-File Issues
#### AGENTS.md
| #   | Lines | Principle | Problem | Fix |
| --- | ----- | --------- | ------- | --- |

#### docs/some-file.md
| #   | Lines | Principle | Problem | Fix |
| --- | ----- | --------- | ------- | --- |

### Rule-Shaped Content (handoff to extract-rules)
| Lines | Content type | Suggested home |
| ----- | ------------ | -------------- |

### Cross-Runtime Parity Gaps (handoff to translate-agent-context)
| Source surface | Behavior | Missing in |
| -------------- | -------- | ---------- |

### Proposed File Operations
- CREATE: <path> — <reason>
- DELETE: <path> — <reason>
- RENAME: <old> → <new> — <reason>
- MERGE: <file-a> + <file-b> → <target> — <reason>
- SPLIT: <file> → <file-a> + <file-b> — <reason>
```

For deeper structural decisions (Agent Surface table rows, anti-patterns, restructure rules), load [agent-md-rewrite-target.md](references/agent-md-rewrite-target.md) on demand. For surface inventory and ownership classification, load [agent-surface.md](references/agent-surface.md). For full audit-step detail (matching the workflow above), load [common-audit-workflow.md](references/common-audit-workflow.md).

### Step 5 — Confirm and Apply

Ask: **"Apply all changes? (yes / yes but skip #N,M / no)"**

On confirmation, execute in this order:

1. Apply file operations: merges, splits, deletes, renames of referenced docs.
2. Rewrite `AGENTS.md` with the full new content (see Canonical Structure below).
3. Update all cross-references across Markdown files.
4. Verify referenced paths still exist and the `Agent Surface` table matches the repo.
5. Check the final line count; flag anything that should be extracted if the file is still too long.

## Canonical AGENTS.md Structure

Rewrite `AGENTS.md` from scratch — do not patch the old structure. AGENTS.md is the runtime-neutral entry point: every supported agent (Claude, Codex, Cursor, Continue, Aider, ...) should be able to read it first and get the cross-cutting rules. Same base skeleton as CLAUDE.md plus one section for the agent surface. Omit a section only when it has nothing non-obvious to say.

```markdown
## Project Overview
[A concise one-sentence definition of the project's nature and core objectives.]

## Tech Stack
[Programming languages, frameworks, databases, testing tools, and other technical components.]

## Project Structure
[Directory layout and corresponding functional responsibilities.]

## Architecture Decisions
[WHY + WHAT for each non-obvious decision. No implementation detail.]

## Coding Standards
[Naming conventions, code style guidelines, and prohibited practices. NOTE: prefer linking to `docs/conventions/*.md` (managed by extract-rules) over inlining when rules grow long. AGENTS.md has no `.claude/rules/` analogue — long rules either inline here or live in referenced docs.]

## Workflow
[Commit specifications, branching strategy, CI/CD pipeline rules, key commands, run/startup instructions.]

## Special Constraints
[Security, performance, and compliance requirements — non-negotiable rules.]

## Key Extension Points
[Table: goal → exact file and function to edit.]

## Agent Surface
[Table: path | runtime | owner | purpose | when to edit. `runtime` is one of `neutral`, `claude`, `codex`, `cursor`, `continue`, `aider`, etc.]

## Context Files
[Table: file path | read-when trigger condition.]
```

For **agent roles** (subagents), the Agent Surface table records: the runtime-neutral prompt file (usually `agents/<role>.md`), the per-runtime binding file, and the invocation command per supported runtime. Agent roles are not portable by copy — see `translate-agent-context` for the decomposition pattern.

## Anti-Patterns to Reject

- Treating any runtime's `.xxx/` folder as a dumping ground for all agent-related files.
- Listing one runtime's mechanism as if every runtime consumes it directly.
- Deleting a runtime's rules, hooks, or commands without porting the behavior they carried (that's a translation job — handoff to `translate-agent-context`).
- Embedding large prompt bodies in `AGENTS.md` when they belong in `agents/*.md`.
- Duplicating tool behavior in both `AGENTS.md` and `tools/` docs.
- Keeping parallel copies of the same rule across multiple runtime folders without naming the canonical home.
- Replacing an enforced hook with vague prose when a script, tool, or CI check should own it.
- Heading-plus-one-bullet sections that should be absorbed into a neighboring section.
- Repeating the same warning in multiple sections.

## Restructure Rules

1. Rewrite the file from scratch. Do not incrementally preserve the old structure.
2. Keep the canonical section order exactly as listed above.
3. Consolidate duplicates ruthlessly. A fact appears once, in the best section, and nowhere else.
4. Keep `AGENTS.md` focused on cross-cutting guidance; move scoped rules into subdirectory `AGENTS.md` and agent-specific detail into `agents/` or `tools/`.
5. Move long procedures to docs or scripts if they exceed roughly 15 lines.
6. Explicitly label any retained runtime-specific artifacts in the `Agent Surface` table — do not pretend they are neutral.
7. Kill filler: repetitive intros, decorative separators, prose that does not change behavior.
8. Hard ceiling of 220 lines. If the rewrite exceeds that, more content belongs in a doc file or a subdirectory `AGENTS.md`.
9. Define forbidden patterns ("Don't X → do Y instead") and detailed rules directly in AGENTS.md or in `docs/conventions/` (since AGENTS.md has no `.claude/rules.md` equivalent).

## Guardrails

- **Never delete** content encoding non-obvious decisions or historical rationale — move it to the right file instead.
- **Never shorten** a file without first confirming its unique content is preserved somewhere.
- **Never create** a new file if the content fits cleanly into an existing one.
- **Never absorb** a doc into `AGENTS.md` if doing so would push it over 220 lines.
- If a referenced file is missing and its content isn't covered elsewhere, flag it as a gap — do not silently skip.
- If unsure whether a section is "obvious from the code," keep it and note the uncertainty in the report.
- **Always rewrite `AGENTS.md` to canonical structure** — incremental edits that preserve the old layout defeat the purpose of this skill.
- **Dedup is mandatory** — if the audit finds the same fact in 3 places, the rewrite must have it in exactly 1 place. Check explicitly before finalizing.
- **Never rewrite rule bodies** — flag rule-shaped content for eviction and recommend `extract-rules`.
- **Never port mechanisms** — if a runtime-specific mechanism (slash command, hook, orchestrator) needs an equivalent in another runtime, that is `translate-agent-context`'s job.

## Handoff to extract-rules

When the audit surfaces rule-shaped content (naming, formatting, API patterns, dynamic per-task guardrails, implicit "do not delete" markers), **list it in the "Rule-Shaped Content" section of the audit report** — do not rewrite it inline. After this skill finishes, recommend the user invoke `extract-rules` to classify each finding and route it. For AGENTS.md-only repos, `extract-rules` routes static rules either inline in AGENTS.md (short) or to `docs/conventions/*.md` referenced from AGENTS.md (long), since `.claude/rules/` is Claude-only.

## Handoff to translate-agent-context

When the audit reveals that the repo wants cross-runtime parity — both `CLAUDE.md` and `AGENTS.md` exist, `.claude/skills/` should be available cross-runtime, slash commands or hooks encode behavior another runtime should respect — **list each gap in the "Cross-Runtime Parity Gaps" section of the audit report**. Recommend the user invoke `translate-agent-context` for the mechanism translation, orchestrator decomposition, and shared `skills/` symlink layout. This skill never ports mechanisms itself.

## Handoff to review-claude-md

If the audit reveals that `CLAUDE.md` (when present) violates the canonical 9-section structure or exceeds 200 lines, recommend `review-claude-md`. This skill only audits AGENTS.md.
