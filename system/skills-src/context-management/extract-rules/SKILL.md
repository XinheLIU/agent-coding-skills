---
name: extract-rules
description: >
  Discover, classify, and document agent-behavior rules — static constraints
  (naming, formatting, backward-compat, security), dynamic per-task guardrails,
  and implicit conventions hidden in HTML comments or sidebar notes. Routes
  findings to the project's actual context surfaces: `.claude/rules/*.md` (Claude),
  inline AGENTS.md or `docs/conventions/*.md` (Codex / OpenCode / Cursor), or
  both with cross-references when the repo supports multiple runtimes. Auto-detects
  runtime from the presence of `.claude/`, `AGENTS.md`, or `.cursorrules`. Use
  when the user asks to "extract project rules", "extract conventions", "document
  our standards", "create spec.md", "audit coding rules", "find hidden conventions",
  "set up .claude/rules", or "set up rules in AGENTS.md". Does NOT restructure
  CLAUDE.md or AGENTS.md prose — see `review-agent-instructions`.
  Does NOT port Claude-specific surfaces cross-runtime — see `translate-agent-context`.
---

# Rules Extract

Last updated: 2026-08-02

**Announce at start:** "I'm using the extract-rules skill to extract and route project rules."

## Goal

Discover and document **how the agent must behave** in this codebase. Classify each finding into one of three constraint types, detect the project's runtime (Claude / AGENTS.md / multi-runtime), then route the finding to its runtime-appropriate canonical home. Output goes to `.claude/rules/*.md`, `docs/conventions/*.md`, AGENTS.md (inline), or `docs/spec.md` — never to `CLAUDE.md` or AGENTS.md prose body sections that this skill doesn't own.

This skill does not own the project's *what/why* sections (Project Overview, architecture, modules, data tables, test coverage). Those belong to `review-agent-instructions`.

## Scope: What This Skill Owns

| In scope (this skill) | Out of scope — handoff |
|---|---|
| Static rules (naming, formatting, API patterns, DB conventions, security, logging) | Project Overview / business scenarios → `review-agent-instructions` |
| Dynamic per-task guardrails (scope limits, confirmation policies) | Architecture decisions → `review-agent-instructions` |
| Implicit conventions ("Do not delete this section", "Used by Partner A") | Module/directory layout → `review-agent-instructions` |
| `.claude/rules/*.md` and AGENTS.md rules-section authoring | Cross-runtime parity translation (slash commands, hooks, symlinks) → `translate-agent-context` |
| `docs/conventions/*.md` (long rules in AGENTS.md-only repos) | AGENTS.md structural rewrite → `review-agent-instructions` |
| `docs/spec.md` authoring | CLAUDE.md structural rewrite → `review-agent-instructions` |
| Adding rows to CLAUDE.md / AGENTS.md `Context Files` table | Table shape/format of `Context Files` table → `review-agent-instructions` |

## The Three Constraint Types

This is the framework. Every finding gets classified as exactly one of these.

### Static constraints

**Permanent rules** that apply across all tasks. Examples:

- Class method signatures must remain backward-compatible.
- Use `snake_case` for variables, `PascalCase` for classes.
- Only modify the targeted files; no incidental refactoring.
- Parameterized queries only — no string concatenation in SQL.

**Home depends on detected runtime** (see Step 1 and the routing table below):
- `claude-only` → `.claude/rules/*.md` (Claude auto-loads these)
- `agents-md-only` (Codex / OpenCode / Cursor) → inline AGENTS.md (short) or `docs/conventions/*.md` referenced from AGENTS.md (long)
- `multi-runtime` → `.claude/rules/*.md` (or `docs/conventions/*.md` for the canonical body) + AGENTS.md reference so both runtimes see the rule

Always-on context regardless of runtime.

### Dynamic constraints

**Ad-hoc per-task guardrails** that the user re-states each invocation. The agent cannot reliably remember them — they must be provided every time. Examples:

- "Limit edits to the three files I named."
- "Show me the plan before writing code."
- "Pause and ask if anything is unclear instead of guessing."

**Home:** document the *meta-pattern* in `docs/spec.md` §Workflow Norms (e.g., "this team typically narrows edit scope per task — ask before broadening"). The actual guardrail still gets re-stated in each task prompt. Do **not** encode dynamic rules statically in `.claude/rules/`.

### Implicit conventions

**Undocumented norms** that exist beyond the code itself. Examples:

- HTML comment in a doc: `<!-- Do not delete this section -->`.
- Sidebar note on an interface: "This is consumed by Partner A — keep stable."
- File-level marker: `# DO NOT MOVE — referenced by external job`.

**Home:** leave the marker in place at the source. Index it in `docs/spec.md` §Implicit Conventions so the agent can discover it. If the convention is generalizable (e.g., "interfaces consumed by external partners are always stable"), promote to an explicit rule using the runtime-appropriate home from the routing table.

When classification is unclear, load `references/constraint-taxonomy.md` for definitions, examples, and decision rules.

## Workflow

### Step 1 — Codebase Exploration

Build a mental map before scanning:

- Read top-level directory structure (files, folders, configs).
- Check existing docs: `/docs`, `README.md`, `CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `.editorconfig`, linter configs.
- Identify primary language(s) and framework(s).
- Note existing style guides: `.eslintrc`, `pyproject.toml [tool.ruff]`, `prettier`, `.clang-format`, etc.
- Check `package.json` / `pyproject.toml` / `Makefile` / `Cargo.toml` for scripts, linters, formatters.
- **Detect runtime.** Inspect: `.claude/` (Claude), `AGENTS.md` / `.codex/` / `.config/opencode/` (Codex / OpenCode), `.cursorrules` (Cursor). Output one of: `claude-only`, `agents-md-only`, `multi-runtime`. This determines routing in Step 4.

Sample, don't exhaustively read.

### Step 2 — Constraint Discovery Scan

Load `references/scan-checklist.md` for the 10 categories and sampling tactics. For each category, report:

- **Status:** `Established` / `Partial` / `Missing`
- **Current convention** (if any): what the code does today
- **Evidence:** 2–3 concrete `file:line` examples
- **Constraint type:** static / dynamic / implicit (use `references/constraint-taxonomy.md` if ambiguous)

### Step 3 — Gap Analysis & User Consultation

For every category marked `Partial` or `Missing`, present the gap. Load `references/gap-consultation-format.md` for the template and worked example. Each gap shows 2–3 options with one-line trade-offs. **Wait for the user's decision** before proceeding.

If the user defers a category, mark it `Deferred`.

### Step 4 — Tier and Place Each Decision

For every finalized decision, select its canonical home using the routing table below, **keyed on the runtime detected in Step 1**:

- `claude-only` → write to `.claude/rules/*.md`. Load `references/rules-file-format.md` for YAML frontmatter spec and `paths:` glob syntax.
- `agents-md-only` → short rules go inline in AGENTS.md `Coding Standards` / `Special Constraints`; long rules (>~10 lines) go to `docs/conventions/<topic>.md` and AGENTS.md links to them. AGENTS.md has no auto-load equivalent for `.claude/rules/`, so prefer linking to keep AGENTS.md readable.
- `multi-runtime` → write the rule body **once** (in `.claude/rules/<topic>.md` if Claude auto-load is wanted, or in `docs/conventions/<topic>.md` for a runtime-neutral home), then reference it from AGENTS.md. Single-source the rule body to avoid drift. The cross-runtime symlink layout (e.g., `.codex/rules → .claude/rules`) is `translate-agent-context`'s territory; this skill produces the files and references.

If a rules file already exists, **append or merge** — don't overwrite.

### Step 5 — Write/Update `docs/spec.md`

Load `references/spec-template.md` only when authoring or updating `spec.md`. The spec file is a **reference index** — it links to `.claude/rules/*.md` files instead of duplicating their content. Mark deferred items with `<!-- TODO: decide on X -->`.

If `docs/spec.md` already exists, diff against it and only change what's new or revised.

### Step 6 — Sync Context Files

Add rows to the `Context Files` table of every entry-point file present in the repo:

- `CLAUDE.md` (when present) → reference `docs/spec.md` and `.claude/rules/`
- `AGENTS.md` (when present) → reference `docs/spec.md` and `docs/conventions/` (or `.claude/rules/` if `multi-runtime` and the Claude rules are the canonical body)

```markdown
| `docs/spec.md` | Before writing or reviewing any code — contains all project conventions |
| `docs/conventions/` | Before writing API / DB / security code — runtime-neutral rules |
```

**Do not restructure CLAUDE.md or AGENTS.md sections.** If either file violates the canonical 9-section structure, exceeds its line ceiling (200 / 220), or contains content that should be reorganized, recommend `review-agent-instructions`.

## Routing Table — Where Each Constraint Lives

Routing keys on the runtime detected in Step 1.

| Constraint type | `claude-only` | `agents-md-only` | `multi-runtime` |
|---|---|---|---|
| Static, path-scoped (api, db, tests) | `.claude/rules/<area>.md` with `paths:` | inline AGENTS.md (short) or `docs/conventions/<area>.md` referenced from AGENTS.md (long) | `.claude/rules/<area>.md` + `docs/conventions/<area>.md` (single-source body) referenced from AGENTS.md |
| Static, global (naming, formatting) | `.claude/rules/<topic>.md` (no `paths:`) | inline AGENTS.md or `docs/conventions/<topic>.md` | `.claude/rules/<topic>.md` + AGENTS.md reference |
| Static, cross-runtime | `AGENTS.md` (cross-runtime by definition; create AGENTS.md if missing) | `AGENTS.md` | `AGENTS.md` |
| Dynamic per-task pattern | `docs/spec.md` §Workflow Norms | `docs/spec.md` §Workflow Norms | `docs/spec.md` §Workflow Norms |
| Implicit, generalizable | Inline annotation + `.claude/rules/` | Inline annotation + `docs/conventions/` | Inline annotation + `.claude/rules/` + AGENTS.md ref |
| Implicit, asset-specific | Inline annotation; index in `docs/spec.md` §Implicit Conventions | Inline annotation; index in `docs/spec.md` | Inline annotation; index in `docs/spec.md` |

`docs/conventions/*.md` is the recommended home for AGENTS.md-only repos when a rule is too long to inline (>~10 lines) — keeps AGENTS.md readable and gives the rule its own canonical home. For `multi-runtime` repos, the runtime-neutral version lives in `docs/conventions/` and Claude's auto-loaded `.claude/rules/<topic>.md` simply references it (or vice versa) — single-source the body, avoid drift.

## Important Principles

- **Don't guess.** If unsure whether a pattern is intentional or accidental, ask the user. A spec built on wrong assumptions is worse than no spec.
- **Sample, don't exhaustively read.** 3–5 representative files per category establishes the pattern.
- **Respect existing docs.** If a doc already covers something, link to it — don't duplicate.
- **Language-aware.** Tailor suggestions to the project's actual stack. Don't suggest ESLint rules for a Python project.
- **Incremental updates.** If `docs/spec.md` already exists from a prior run, treat this as an update — diff and modify only relevant sections.

## Handoff to review-agent-instructions

If the scan reveals that CLAUDE.md or AGENTS.md violates the canonical skeleton, exceeds its line ceiling, has duplicated content, or contains rule-shaped prose that should be evicted, **do not refactor it here**. Recommend the user run `review-agent-instructions` for structural rewrite. This skill only adds rows to the `Context Files` table.

## Handoff to translate-agent-context

If extraction produces rules that need to be ported across runtimes — e.g., rules written to `.claude/rules/` that should also be discoverable from a Codex setup, or behaviors currently encoded as Claude-specific hooks/slash commands that need agent-agnostic equivalents — recommend `translate-agent-context` for the cross-runtime symlink/copy layout and mechanism translation. This skill stops at producing the canonical files and references; it does not symlink runtime discovery paths.
