---
name: acs-refactor-code
description: "Improve existing code without changing behavior, at two depths. Depth 1 — quick polish of recently modified code — renames vague identifiers, flattens nesting with early returns, drops redundant wrappers and dead comments, aligns with the repo's style guide; applied directly, verified by tests. Depth 2 — structural refactor — extracts abstractions, eliminates duplication across files, applies design patterns (Strategy / Template Method / Adapter) where they earn their keep, breaks up overgrown units; workflow is scope confirmation → baseline metrics → ranked proposal → user approval → grouped edits with tests between groups → re-measured before/after report. Triggers: \"refactor\", \"simplify\", \"polish\", \"clean up what I just wrote\", \"reduce duplication\", \"break up this class\". Tests are the safety net; behavior must not change."
---

Last updated: 2026-09-17

## Context contract

```yaml
context:
  requires: [system.invariants, source.refactor_scope]
  retrieves: [change.requirements, design.relevant_decisions, system.dependencies, verification.baseline]
  produces: [change.preservation_evidence, design.structural_delta]
  updates: [source.implementation, system.current_state, design.applicable_decisions]
  invalidates: [verification.for_changed_code, system.boundary_dependents]
  handoff_to: [testing, design, code_review]
```

Shared semantics: [shared protocol](../../protocols/skill-declarations.md); shared execution: [Coordination](../../protocols/context-coordination.md). Domain results and proposed transitions use those contracts; existing authorization persists.


# Refactor Code

You improve the internal structure of existing code while keeping every external behavior identical. Two depths share that invariant but differ in ceremony: a quick polish is applied directly; a structural refactor is measured, proposed, and approved before any edit.

## Context and preservation contract

Read [engineering context](../../protocols/engineering-memory.md) for the active change and preservation evidence. Require relevant architecture invariants, accepted behavior/criteria, dependencies, tests, and consequential rationale. For a standalone refactor, record the scoped preservation baseline instead of inventing product requirements.

Capture before/after source revisions or diff identities and equivalent checks/environment. Return `change.preservation_evidence`: invariant/criterion → before/after check → result, structural delta, omissions, and next action. If module boundaries or dependency rules change, update the configured System State with current evidence and amend or supersede applicable ADRs while preserving history. When another owner must author an amendment, return a blocking handoff until it is reconciled. If architecture is unchanged, record that assessment without creating an empty ADR. External behavior changes return to Product/Design for scope resolution.

The coordinator resolves paths, claims, and shared writes; this skill owns the structural judgment and preservation assessment.

## Depth selector

| Signal | Depth |
| --- | --- |
| Clarity/style work on recently modified code; no logic moves between files | **1 — Polish** (no gate) |
| Extracting shared logic across files, applying a design pattern, breaking up an overgrown class/function, complexity reduction | **2 — Structural** (metrics + approval gate) |

"Simplify", "polish", "clean up" → Depth 1. "Refactor", "deduplicate across modules", "break up X" → Depth 2. If the request is ambiguous, ask one short question and proceed. Polish that uncovers structural smells escalates by *offering* Depth 2 — never by silently doing it.

## Shared guardrails (both depths)

- Behavior must not change. Outputs, side effects, and signatures stay identical; tests are the proof.
- Never touch code outside the confirmed scope.
- Do not delete pre-existing dead code unless asked — flag it instead.
- Do not add new dependencies without explicit user approval.
- Readability wins over compactness and over micro-performance. Explicit > clever.
- On test failure, revert and report — never paper over a behavior change.

## Depth 1 — Polish

The bar is **explicit, readable, idiomatic to this repo** — not shorter, not cleverer.

### Default scope

Recently modified code only, unless the user names a different scope:
- Files touched in the current session, or
- Files in `git diff` against the merge base, or
- A specific section the user points at.

Do not crawl the codebase.

### What to look for

**Clarity**
- Vague names → precise names. Longer descriptive beats short and ambiguous.
- Nested conditionals → guard clauses + early returns.
- Nested ternaries → `if/else` or `switch`.
- Dense one-liners that hide intent → split across lines.
- Comments that restate the code → delete. Keep only those that explain *why*.

**Redundancy**
- One-line wrapper that adds no meaning → inline it.
- Variable assigned once and immediately used → inline it.
- Imports / locals your edits orphaned → remove.
- Dead branches your edits made unreachable → remove.

**Project style**
Read `CLAUDE.md`, `AGENTS.md`, and any `docs/spec.md` in the repo before editing. Apply the standards you find there; a project rule always wins over these defaults.

### Polish workflow

1. Identify the in-scope code (default: recent diff).
2. List the polish opportunities you see — keep it brief, this is not a proposal doc.
3. Apply the edits.
4. Run the test suite. On failure, revert and report.
5. Note any structural smells you noticed but deliberately did not touch (duplicated logic across files, a class doing too much). Offer them as Depth 2 candidates; let the user decide.

### Self-check before finishing

- Does every changed line trace to a clarity, redundancy, or style issue?
- Could a reader unfamiliar with the change read the result faster than the original?
- Are tests still green?

## Depth 2 — Structural refactor

Restructuring work that warrants a deliberate, measured cycle: a baseline, a ranked plan the user approves, grouped edits with tests between each group, and a before/after report. Concretely:

- Extracting an abstraction shared by multiple call sites
- Removing duplication that spans files or modules
- Applying a design pattern where it genuinely reduces cognitive load
- Breaking up a class or function that has accumulated too many responsibilities
- Reducing cyclomatic complexity in a unit that has grown unwieldy
- Pulling shared logic up an inheritance line, or pushing specialized logic down

SOLID is used as a lens to *spot* these smells, not as a mandate to fix every violation.

### 1. Confirm scope (first action, before any read of code)

Ask the user:

> "Refactor scope: (a) recent changes, (b) a specific file, (c) a module / package, or (d) whole codebase? Any files to explicitly exclude?"

Do not assume — scope directly controls blast radius. If the user already specified a scope in the request, confirm it back in one line and proceed.

### 2. Measure baseline metrics

Compute and record, for files in scope:

- LOC per file
- Per-function cyclomatic complexity (avg + max)
- Duplicate-block count

See the *Metrics* section below for the method. Store the numbers — you will cite them in the final report.

### 3. Identify opportunities, rank, present

Read the in-scope code and list candidate refactorings. Rank by **impact ÷ risk**: high-impact low-risk first. Present the shortlist (roughly 3–7 items) to the user before editing, like:

```
Proposed refactorings (ranked):
1. Extract `_parse_amount` from csv_parser.py — used in 3 places, currently inlined.
2. Replace conditional chain in expense_categorizer.categorize() with a rule table.
3. Pull `validate_row` up from csv_parser + data_validator into a shared helper.
...
```

Wait for the user's go-ahead (or their subset) before editing.

### 4. Apply changes in logical groups

A **group** is one cohesive transformation — e.g. "Extract Method across `csv_parser.py`" or "Introduce Parameter Object for `ReportConfig`". One pattern application per group. Do not batch unrelated refactorings into a single group.

Between groups:

1. Run the project's canonical test command — detect it from project config (`pytest`, `npm test`, `go test ./...`, `cargo test`, `mvn test`); marker-scoped if the user specified one (e.g. `pytest -m unit`), otherwise the full suite.
2. If tests pass → move to the next group.
3. If tests fail → reverse only this group's own edits, preserving pre-existing and concurrent work, then stop and surface the failure to the user. Do **not** attempt to fix behavior drift silently; the whole point of refactoring is that tests are the safety net.

### 5. Re-measure metrics

After the last group passes, recompute the same metrics from step 2 for the same files.

### 6. Emit the before/after report

Include a visual structural delta for cross-file refactors: removed shallow modules, new seams, moved ownership, and preserved behavior. Use inline SVG first, retain ordinary HTML fallback labels, and link each visual claim to preservation evidence.

Use the local [visual report contract](references/visual-report.md) and the *Report format* below. For complex multi-dimensional refactoring with substantial before/after comparisons across multiple architectural concerns, reference `craft/meta/references/tabbed-discovery-report.md` for the tabbed HTML output protocol. Be honest about debt that was deferred — do not claim wins you did not achieve.

## Refactoring catalog

Reach for these; pick the lightest one that solves the problem:

- **Extract Function / Extract Class** — pull out a named unit when logic is duplicated or a function does more than one thing.
- **Inline Function / Variable** — remove a layer that adds nothing.
- **Move Method / Move Field** — relocate behavior to the class it mostly uses.
- **Replace Conditional with Polymorphism** — when an if/elif/switch dispatches on a type field.
- **Introduce Parameter Object** — when 3+ parameters always travel together.
- **Replace Magic Number/String with Named Constant** — when a literal carries meaning.
- **Decompose Conditional** — extract each branch of a dense if-block into a named helper.
- **Pull Up / Push Down Method** — move behavior along the inheritance line to where it belongs.
- **Strategy / Template Method / Adapter** — the three patterns that most often genuinely pay off; others are almost always over-engineering.
- **Replace Loop with Pipeline** — when a for-loop is really filter/map/reduce in disguise.

## SOLID as lenses, not mandates

Use SOLID to *spot* smells, not to force changes:

- Single Responsibility → Is this class or function juggling more than one reason to change?
- Open/Closed → Does adding a new variant require editing existing code instead of adding a new file?
- Liskov → Does a subclass silently break its parent's contract?
- Interface Segregation → Are callers forced to depend on methods they do not use?
- Dependency Inversion → Is a high-level module importing a concrete low-level one when an abstraction would serve?

A violation is a candidate, not a requirement. Skip fixes that would make code harder to read.

## Metrics (Depth 2)

For Python projects, all metrics use the built-in `ast` module — no new dependency. For other languages, fall back to LOC plus the normalized duplicate scan below, and ask before adding a complexity tool.

### LOC

Lines of code per file (non-blank, non-comment) — compute via simple file read.

### Cyclomatic complexity (per function)

Start at 1 per function/method. Add 1 for each of:

- `ast.If`, `ast.For`, `ast.While`, `ast.Try`, `ast.ExceptHandler`, `ast.With` (if multi-item)
- Each additional `and` / `or` inside a `BoolOp`
- Each comprehension clause (`ListComp`, `SetComp`, `DictComp`, `GeneratorExp` with `if` filters)
- Each `case` in a `match`

Report the per-file average and max.

### Duplicate blocks

Approximate by function-level normalization: strip comments and whitespace, replace identifiers with `$v`, hash the result, and count collisions across in-scope files. Report the number of function pairs with identical normalized hashes.

**Optional upgrade:** if the user wants richer numbers (maintainability index, cognitive complexity, Halstead), ask before adding `radon` to `requirements.txt` — do not add it unprompted (project rule).

## Report format (Depth 2)

ALWAYS emit this exact structure at the end of a structural refactor:

```
## Refactoring report
**Scope:** <files>
**Groups applied:** <N>

| Metric           | Before | After | Δ   |
| ---------------- | ------ | ----- | --- |
| LOC              | ...    | ...   | ... |
| Avg cyclomatic   | ...    | ...   | ... |
| Max cyclomatic   | ...    | ...   | ... |
| Duplicate blocks | ...    | ...   | ... |

### Patterns applied
- <Pattern> on <file>:<func/class> — <one-line why>
- ...

### Tests
- Group 1: <result — pass/fail, count>
- Group 2: ...

### Architecture context
- System State / ADR amendments: <references and revisions, or evidence that boundaries are unchanged>
- Preservation: <invariant/criterion mapping, baseline/current revisions, environment and omissions>

### Remaining debt (deferred)
- <Item> — <why deferred>
- ...
```

If a metric went the wrong way (e.g. LOC up because a helper was introduced), call that out explicitly and justify it.

Depth 1 needs no metrics report — a brief list of what was polished and the test result suffices.
