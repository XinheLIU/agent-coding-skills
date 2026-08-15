# User Profile

Last updated: 2026-08-02

- [Your Profile, what you know, eg, Full-stack developer, strongest in algorithms and data structures]
- Prefers depth over breadth — understand the problem before writing code

# Communication Preferences

- Be concise. No fluff, no filler, no restating what I just said.
- When explaining, lead with the "why" not the "what."
- If something is ambiguous, ask — don't guess and apologize later.
- Skip the caveats and disclaimers unless there's a real risk.
- Use code to explain, not paragraphs. A 5-line example beats a 5-paragraph description.
- When presenting options, rank them with your recommendation first.

# Personal Coding Style

- Prefer explicit over implicit. No magic.
- Favor flat over nested — early returns, guard clauses.
- Name things precisely. A longer descriptive name beats a short vague one.
- Prefer pure functions and immutability where practical.
- Minimize state. Derive what you can, store only what you must.
- Prefer composition over inheritance.
- Algorithms should be readable — comment the invariant or the trick, not the obvious.
- Type everything. Avoid any, object, untyped dicts.

# Preferred Tools & Stack

- Python package manager: uv (not pip, not poetry), always create isolated environments (no global installs)
- Don't commit to git unless I explicitly tell you to.
- When suggesting new dependencies, confirm before adding — stay within the current tech stack.
- Use a shared project-level skills directory (~/skills/{prompt,coding,data}) and symlink both ~/.claude/skills and ~/.codex/skills to it; if a skill is not cross-compatible, keep tool-specific versions instead of sharing.

# Documentation Rule

- When updating any Markdown file, also update a Last updated date near the top of that file.


# Design Principles

- Do not introduce unnecessary design patterns unless explicitly required.
- Avoid over‑abstraction; do not split logic into two layers if one layer suffices.
- Do not introduce dependencies outside the current tech stack; confirm first if needed.


## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification
