---
name: writing-great-skills
description: Author or revise a predictable system skill. Use when defining a skill's invocation boundary, procedure, references, completion criteria, or shared-memory contract.
---

# Writing Great Skills

Last updated: 2026-08-25

Predictability means the agent follows the same process, not that every output is identical.

1. **Choose invocation.** Keep model invocation only when the agent or another skill must discover the skill. For a hand-invoked skill, set `disable-model-invocation: true` and make the description a human-facing summary. The choice is complete when every intended caller can reach the skill and unintended prompts do not trigger it.
2. **Write the pointer.** For a model-invoked skill, front-load the leading action and name each distinct trigger branch once. Put boundaries in the description only when they prevent a plausible misroute.
3. **Protect the hierarchy.** Keep the universal procedure in `SKILL.md`. Move branch-only reference behind a direct pointer, and keep each concept's definition, rules, and caveats together. Split only when invocation or sequence creates a real context boundary.
4. **Sharpen completion.** End every step or stage with a checkable, exhaustive done condition. Declare persistent artifacts as `reads`, `owns`, `updates`, or `hands off`; keep one canonical owner per fact.
5. **Prune.** Remove duplicated meanings, environment lookups, stale history, speculative branches, default behavior, and prose that does not change execution. Prefer positive target behavior; reserve prohibitions for hard guardrails and pair them with the required alternative.
6. **Validate.** Parse frontmatter, resolve every local pointer, exercise bundled scripts, and test realistic trigger and non-trigger prompts. The skill is ready when all paths terminate at their stated completion criteria and every referenced artifact exists.

When an external skill influences the result, record its source, revision, license, retained principle, and local behavioral changes in the system provenance record.
