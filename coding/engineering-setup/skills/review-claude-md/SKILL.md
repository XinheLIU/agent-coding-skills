---
name: review-claude-md
description: >
  Audit and restructure CLAUDE.md and every file it references, focusing on the
  project's what/why context — Project Overview, business scenarios, architecture,
  modules, interfaces, data tables, and test coverage. Produces a MECE rewrite to
  a canonical 9-section skeleton with a 200-line ceiling. Use when the user asks
  to "review CLAUDE.md", "audit context files", "shrink CLAUDE.md", "deduplicate
  context docs", or "restructure CLAUDE.md to canonical form". Does NOT extract
  or document agent-behavior rules, coding conventions, or per-task guardrails —
  see `extract-rules` for that.
---

# Review CLAUDE.md

Last updated: 2026-05-08

**Announce at start:** "I'm using the review-claude-md skill to audit your context files."

## Goal

Audit `CLAUDE.md` and every file it references. Produce a concrete change list, then apply on user confirmation. This skill owns the project's **what/why** context only — what the project does, how it's organized, what its modules and interfaces are. It does not own behavior rules or coding conventions.

## Scope: What This Skill Owns

| In scope (this skill) | Out of scope — handoff |
|---|---|
| Project Overview (one-sentence definition) | Naming / formatting / lint rules → `extract-rules` |
| Architecture decisions (WHY+WHAT) | API endpoint conventions → `extract-rules` |
| Module/directory layout | DB conventions → `extract-rules` |
| Exposed vs internal interfaces (catalog only) | Security / logging rules → `extract-rules` |
| Data table relationships (catalog only) | Per-task guardrails → `extract-rules` |
| Test coverage description | Implicit "do not delete" markers → `extract-rules` |
| Canonical file structure + line ceiling | Cross-runtime mechanism translation → `translate-agent-context` |
| `Context Files` table shape (in CLAUDE.md) | AGENTS.md structure audit → `review-agent-md` |

If the audit surfaces rule-shaped content embedded in CLAUDE.md prose, **flag it** for eviction — do not rewrite the rule body here. Recommend `extract-rules` to triage it into `.claude/rules/`, `AGENTS.md`, or `docs/spec.md`.

## Workflow

### Step 1 — Inventory

1. Read `CLAUDE.md` in full.
2. Collect every file path mentioned anywhere: inline code paths, links, tables, comments, examples.
3. Read each collected file in full.
4. Record `exists`, `missing`, or `empty` for each path.

### Step 2 — Cross-File MECE Analysis

Map the full content landscape across all files. For each piece of information, ask: is this the single canonical home for it, or does it duplicate another file?

Build a content ownership map:

```text
Topic -> owned by <file> | duplicated in <file-a>, <file-b>
```

Common MECE violations:

- Same commands appear in both `CLAUDE.md` and a referenced doc.
- Architecture is described in both `CLAUDE.md` and a doc file.
- Setup steps split across multiple files without clear ownership.
- Two doc files cover overlapping subsystems with no clear boundary.
- A doc file is two unrelated topics stapled together.
- A doc file is so short it should be absorbed into another file.
- A doc file is so large it should be split by a clearer topic boundary.

### Step 3 — Per-File Analysis Against the 12 Principles

For `CLAUDE.md` and each referenced file, record each issue as:

- `File`
- `line range`
- `principle #`
- `problem` (one sentence)
- `fix` (concrete action)

#### The 12 Principles

1. **Less Is More** — `CLAUDE.md` should usually land in 60–300 lines. Delete anything a competent engineer can infer from reading the repo.
2. **Be Specific, Not Generic** — every sentence must change agent behavior. If covering the line changes nothing, delete it.
3. **Encode Style via Tooling** — replace prose style rules with formatter or linter commands whenever tooling can enforce them.
4. **WHY → WHAT → HOW** — non-obvious rules need the reason, the rule, and the exact alternative command or file to use.
5. **Progressive Disclosure** — `CLAUDE.md` is the entry point only. Every cross-reference must say *when* to read the target file.
6. **Alternatives Not Just Prohibitions** — every "don't" rule must say what to do instead.
7. **Living Sync** — after structural changes, verify referenced paths still exist, commands still run, tables still match the repo.
8. **Hierarchical Structure** — rules scoped to one subdirectory or one agent belong in a narrower local context file, not the root.
9. **Git Discipline** — include commit/branch/PR rules only when the repo truly has a non-default convention.
10. **Factor Repetition** — if the same multi-step workflow appears twice, extract it into a script, command, or one canonical doc.
11. **Live Context over Static Text** — facts that change often should be commands the agent can run, not prose snapshots.
12. **MECE** — each fact has one canonical home; each file has one clear purpose.

### Step 4 — Audit Report

Produce the report using this template:

```markdown
## CLAUDE.md Audit Report

### Summary
- CLAUDE.md: <N> lines
- Referenced files: <list — exists/missing>
- MECE violations: <count>
- Other issues: <count>
- Rule-shaped content to evict (handoff to extract-rules): <count>

### Content Ownership Map
| Topic          | Canonical Home | Also appears in |
| -------------- | -------------- | --------------- |
| Setup commands | CLAUDE.md      | docs/setup.md   |

### MECE Violations
| #   | Topic       | Files                     | Problem             | Fix                       |
| --- | ----------- | ------------------------- | ------------------- | ------------------------- |
| 1   | Setup steps | CLAUDE.md + docs/setup.md | Duplicated verbatim | Remove from docs/setup.md |

### Per-File Issues
#### CLAUDE.md
| #   | Lines | Principle | Problem | Fix |
| --- | ----- | --------- | ------- | --- |

#### docs/some-file.md
| #   | Lines | Principle | Problem | Fix |
| --- | ----- | --------- | ------- | --- |

### Rule-Shaped Content (handoff to extract-rules)
| Lines | Content type | Suggested home |
| ----- | ------------ | -------------- |

### Proposed File Operations
- CREATE: <path> — <reason>
- DELETE: <path> — <reason>
- RENAME: <old> → <new> — <reason>
- MERGE: <file-a> + <file-b> → <target> — <reason>
- SPLIT: <file> → <file-a> + <file-b> — <reason>
```

### Step 5 — Confirm and Apply

Ask: **"Apply all changes? (yes / yes but skip #N,M / no)"**

On confirmation, execute in this order:

1. Apply file operations: merges, splits, deletes, renames of referenced docs.
2. Rewrite `CLAUDE.md` with the full new content (see Canonical Structure below).
3. Update all cross-references across Markdown files.
4. Verify referenced paths still exist.
5. Check the final line count; flag anything that should be extracted if the file is still too long.

## Canonical CLAUDE.md Structure

Rewrite `CLAUDE.md` from scratch — do not patch the old structure. Sections are ordered by how often the agent needs them. Omit a section only when it has nothing non-obvious to say.

Read the canonical structure from `references/claude-md-template.md` and use it as your exact blueprint.

## Content Constraints

### What Belongs in CLAUDE.md

- **Project Positioning:** One sentence explaining "what this is" and its core capabilities (e.g., "AdminX is an open-source Agent management platform providing Prompt management, Datasets, Evaluators, and Trace observability").
- **Core Architecture:** A brief paragraph + link to `docs/architecture.svg`. Only provide a high-level overview of layers or core components; do not recreate the diagram in text.
- **Key Modules:** A small table or short list mapping modules to a "one-sentence responsibility". Complex dependencies belong in `module-deps.svg`.
- **Key Conventions:** Project-specific hard rules (e.g., unified response wrappers, field naming conventions). State the rule directly without expanding on the rationale.
- **How to Run:** A one-sentence summary + link to the run documentation in `docs/`. Keep details in the dedicated doc.
- **Danger Zones:** Critical for legacy projects. Document code, interfaces, or configs that will "blow up if touched".
- **Historical Baggage:** Explain designs that "look weird but have historical reasons" to prevent AI or newcomers from casually refactoring and causing disasters.

### What MUST NOT be in CLAUDE.md

- **Full Architecture Details:** Leave them to `architecture.svg` or `docs/`. `CLAUDE.md` is only the entry point.
- **Full API Lists:** Put them in `api-list.md`. Do not copy endpoints into `CLAUDE.md`.
- **Full Data Models:** Put them in `data-model.md`. Do not list every table and field in `CLAUDE.md`.
- **Generic Standards:** e.g., generic coding guidelines. They dilute the project-specific focus.
- **Backstories:** Project origins or organizational gossip are unnecessary for an AI writing code.
- **The Golden Principle:** Every single bullet point must be either "essential knowledge the AI must know on startup" or "an entry point pointing to docs". Otherwise, delete it.

## Anti-Patterns to Reject

- Heading-plus-one-bullet sections that should be absorbed into a neighboring section.
- Horizontal rules between every section.
- Intro lines like "This file provides guidance to Claude Code".
- Repeating the same warning in multiple sections.
- Domain definitions that belong in a doc file.
- Long embedded procedures that belong in a script or dedicated doc.

## Restructure Rules

1. Rewrite the file from scratch. Do not incrementally preserve the old structure.
2. Keep the canonical section order exactly as listed above.
3. Consolidate duplicates ruthlessly. A fact appears once, in the best section, and nowhere else.
4. Move business-domain content to docs and reference it via `Context Files`.
5. Move long procedures to docs or scripts if they exceed roughly 15 lines.
6. Kill filler: repetitive intros, decorative separators, prose that does not change behavior.
7. Hard ceiling of 200 lines. If the rewrite exceeds that, more content belongs in a doc file.
8. For rule-shaped content (naming, formatting, API patterns), reference `.claude/rules/*.md` instead of inlining — those files are owned by `extract-rules`.

## Guardrails

- **Never delete** content encoding non-obvious decisions or historical rationale — move it to the right file instead.
- **Never shorten** a file without first confirming its unique content is preserved somewhere.
- **Never create** a new file if the content fits cleanly into an existing one.
- **Never absorb** a doc into `CLAUDE.md` if doing so would push it over 200 lines.
- If a referenced file is missing and its content isn't covered elsewhere, flag it as a gap — do not silently skip.
- If unsure whether a section is "obvious from the code," keep it and note the uncertainty in the report.
- **Always rewrite `CLAUDE.md` to canonical structure** — incremental edits that preserve the old layout defeat the purpose of this skill.
- **Dedup is mandatory** — if the audit finds the same fact in 3 places, the rewrite must have it in exactly 1 place. This is the single most common failure mode; check explicitly before finalizing.
- **Never rewrite rule bodies** — flag rule-shaped content for eviction and recommend `extract-rules`.

## Handoff to extract-rules

When the audit surfaces rule-shaped content (naming, formatting, API patterns, dynamic per-task guardrails, implicit "do not delete" markers), **list it in the "Rule-Shaped Content" section of the audit report** — do not rewrite it inline. After this skill finishes, recommend the user invoke `extract-rules` to:

- Classify each finding as static / dynamic / implicit.
- Route static rules to `.claude/rules/*.md` (path-scoped or global) or `AGENTS.md` (cross-runtime).
- Document dynamic per-task patterns in `docs/spec.md`.
- Surface implicit conventions inline + index in `docs/spec.md`.

This skill owns table shape and structure of the `Context Files` table; `extract-rules` adds rows pointing to its outputs.
