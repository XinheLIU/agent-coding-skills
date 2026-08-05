# Common Audit Workflow

Last updated: 2026-08-06

Use this workflow when auditing a root AI context file such as `CLAUDE.md` or `AGENTS.md` plus every file it references.

- `audit` stops after Step 1 and the mapping portions of Step 2.
- `organize` uses Step 1 plus the content-ownership portion of Step 2.
- `normalize` uses the full workflow for runtime-neutral rewrites.

## Step 1 — Inventory

1. Read the root context file in full.
2. Collect every file path mentioned anywhere in it: inline code paths, links, tables, comments, and examples.
3. Read each collected file in full.
4. Record `exists`, `missing`, or `empty` for each path.

## Step 2 — Cross-File MECE Analysis

Before evaluating individual files, map the full content landscape across all files.

For each piece of information, ask: is this the single canonical home for it, or does it duplicate or overlap with another file?

Build a content ownership map:

```text
Topic -> owned by <file> | duplicated in <file-a>, <file-b>
```

Common MECE violations to look for:

- The same commands appear in both the root context file and a referenced doc.
- Architecture is described in both the root context file and a doc file.
- Setup steps are split across multiple files without clear ownership.
- Two doc files cover overlapping subsystems with no clear boundary.
- A doc file is really two unrelated topics stapled together.
- A doc file is so short it should be absorbed into another file.
- A doc file is so large it should be split by a clearer topic boundary.

If the audit involves migration between agent runtimes, also build a mechanism-translation map:

```text
Old surface -> behavior -> new canonical surface -> parity status
```

## Step 3 — Per-File Analysis Against the 14 Principles

For the root context file and each referenced file, record each issue as:

- `File`
- `line range`
- `principle #`
- `problem` in one sentence
- `fix` as a concrete action

When a target-specific rewrite template exists, use that template as the canonical output shape during the rewrite phase.

### The 14 Principles

1. **Less Is More**: the root context file should usually land in the 60-300 line range. Delete anything a competent engineer can infer from reading the repo.
2. **Be Specific, Not Generic**: every sentence must change agent behavior. If covering the line changes nothing, delete it.
3. **Encode Style via Tooling**: replace prose style rules with formatter or linter commands whenever tooling can enforce them.
4. **WHY -> WHAT -> HOW**: non-obvious rules need the reason, the rule, and the exact alternative command or file to use.
5. **Progressive Disclosure**: the root context file is the entry point only. Every cross-reference must say when to read the target file.
6. **Alternatives Not Just Prohibitions**: every "don't" rule must say what to do instead.
7. **Living Sync**: after structural changes, verify referenced paths still exist, commands still run, and tables still match the repo.
8. **Hierarchical Structure**: rules scoped to one subdirectory or one agent belong in a narrower local context file, not in the root.
9. **Git Discipline**: include commit, branch, or PR rules only when the repo truly has a non-default convention.
10. **Factor Repetition**: if the same multi-step workflow appears twice, extract it into a script, command, or one canonical doc.
11. **Live Context over Static Text**: facts that change often should be represented as commands the agent can run, not prose snapshots.
12. **MECE**: each fact should have one canonical home, and each file should have one clear purpose.
13. **Checkable Constraints**: verification only checks what the constraint names. Every rule must be stated so that a test, linter, CI gate, or reviewer could decide whether it was violated. "Keep the code clean" is unverifiable and therefore unenforced — delete or sharpen it. Prefer naming the check itself: "response shapes of `/api/v1/*` are frozen — `tests/contract/` covers them."
14. **Earned by Experience**: a rule earns its line when something went wrong without it. Rules with no incident, no regression, and no explicit decision behind them are speculation. During audit, ask of each rule: what breaks if this line is deleted? No answer means delete.

## Index Plus Common Sense

The single most common failure is writing too much: prose restatements of the architecture diagram, the whole interface inventory, every table and every column. Thousands of lines, loaded on every startup, pushing the agent into the dumb zone.

**The file's job is index plus common sense.** The index points at the detail in `docs/`; the common sense is what the agent must know the moment it starts. Every line is either one or the other — anything else, delete.

| Include | How to write it |
| --- | --- |
| What the project is | One sentence |
| Core architecture | One paragraph plus a link to the diagram. Never rewrite the diagram as prose |
| Key modules | Small table, one sentence of responsibility each; detailed dependencies stay in the module graph |
| Key conventions | Hard rules, no rationale. "All REST responses are wrapped in `Result`." "DB columns snake_case, Java fields camelCase" |
| How to run it | One sentence plus a link to the runbook |
| Forbidden zones and historical baggage | The soul of a legacy project — the only sections worth real space |

Leave out: full architecture detail, the full interface inventory, the full data model (all three already live in `docs/`), generic coding standards not specific to this project, and background story. The agent does not need the project's origin myth to work.

## Step 4 — Produce the Audit Report

Use this template, replacing placeholders with the actual root context file name:

```markdown
## <ROOT_CONTEXT_FILE> Audit Report

### Summary
- <ROOT_CONTEXT_FILE>: <N> lines
- Referenced files: <list - exists/missing>
- MECE violations: <count>
- Other issues: <count>

### Content Ownership Map
| Topic | Canonical Home | Also appears in |
|-------|----------------|-----------------|
| Setup commands | <ROOT_CONTEXT_FILE> | docs/setup.md |

### Mechanism Translation Map
| Old surface | Behavior | New canonical surface | Parity status |
|-------------|----------|-----------------------|---------------|
| .claude/rules/backend.md | Backend edit rules | src/AGENTS.md | Equivalent |

### MECE Violations
| # | Topic | Files | Problem | Fix |
|---|-------|-------|---------|-----|
| 1 | Setup steps | <ROOT_CONTEXT_FILE> + docs/setup.md | Duplicated verbatim | Remove from docs/setup.md |

### Per-File Issues
#### <ROOT_CONTEXT_FILE>
| # | Lines | Principle | Problem | Fix |
|---|-------|-----------|---------|-----|

#### docs/some-file.md
| # | Lines | Principle | Problem | Fix |
|---|-------|-----------|---------|-----|

### Proposed File Operations
- CREATE: <path> - <reason>
- DELETE: <path> - <reason>
- RENAME: <old> -> <new> - <reason>
- MERGE: <file-a> + <file-b> -> <target> - <reason>
- SPLIT: <file> -> <file-a> + <file-b> - <reason>
```
