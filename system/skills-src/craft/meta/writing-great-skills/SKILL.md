---
name: writing-great-skills
description: Design and revise predictable agent skills with concise triggers, checkable completion criteria, progressive disclosure, and explicit shared-memory ownership. Use when adding or improving a system skill.
---

# Writing Great Skills

Last updated: 2026-08-02

Predictability means the same process, not identical prose.

1. Give the skill one clear invocation boundary and verb-led name.
2. Put triggers and exclusions in the description; keep the body procedural.
3. End each stage with a checkable completion condition.
4. Keep one source of truth for each rule. Move branch-only detail into directly linked references.
5. Prefer a strong leading concept over repeated explanations.
6. Remove no-op instructions, stale sediment, duplication, and speculative branches.
7. Declare which shared-memory artifacts the skill reads, owns, updates, and hands off.
8. Keep Markdown authoritative when the skill generates HTML, and define the rebuild path.
9. Validate frontmatter, links, scripts, and realistic trigger behavior before integration.

When adapting an external skill, record source, revision, license, retained principle, renamed concepts, changed paths, runtime changes, and commit-policy changes in the system provenance report.
