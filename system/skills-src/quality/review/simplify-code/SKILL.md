---
name: simplify-code
description: Polish recently modified code for clarity and project-style consistency without changing behavior. Renames vague identifiers, flattens nesting with early returns, drops redundant wrappers and dead comments, replaces nested ternaries, aligns with the repo's style guide. Use after writing or editing code, before commit. Preserves all functionality and verifies with tests.
---

Last updated: 2026-08-02

# Code Simplify

You polish code that was just written or edited. The bar is **explicit, readable, idiomatic to this repo** — not shorter, not cleverer. Behavior must not change.

## Default scope

Recently modified code only, unless the user names a different scope:
- Files touched in the current session, or
- Files in `git diff` against the merge base, or
- A specific section the user points at.

If scope is ambiguous, ask one short question and proceed. Do not crawl the codebase.

## What to look for

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
Read `CLAUDE.md`, `AGENTS.md`, and any `docs/spec.md` in the repo before editing. Apply the standards you find there. Common ones in this codebase:
- ES modules, sorted imports, explicit extensions
- `function` keyword over arrow functions
- Explicit return types on top-level functions
- React components with explicit `Props` types
- Prefer upfront checks over try/catch when an error is predictable
- Consistent naming conventions

If a project rule conflicts with these defaults, the project rule wins.

## What NOT to do

- Do not change external behavior. Outputs, side effects, and signatures must remain identical.
- Do not extract classes, apply design patterns, or restructure across files. That is a different kind of change and warrants its own conversation.
- Do not delete pre-existing dead code unless asked — flag it instead.
- Do not "improve" code outside the changed region.
- Do not trade readability for fewer lines. Explicit > compact.
- Do not combine unrelated concerns into one function.
- Do not remove a helpful abstraction just because it could be inlined.

## Workflow

1. Identify the in-scope code (default: recent diff).
2. List the polish opportunities you see — keep it brief, this is not a proposal doc.
3. Apply the edits.
4. Run the test suite. On failure, revert and report — do not paper over a behavior change.
5. Note any structural smells you noticed but deliberately did not touch (e.g. duplicated logic across files, a class doing too much). Surface them; let the user decide.

## Self-check before finishing

- Does every changed line trace to a clarity, redundancy, or style issue?
- Could a reader unfamiliar with the change read the result faster than the original?
- Are tests still green?

If yes to all three, you're done.
