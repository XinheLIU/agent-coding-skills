---
name: improve-codebase-architecture
description: Survey architectural friction and propose deepening opportunities as linked Markdown and HTML reports. Use when modules are hard to understand, change, test, or navigate with agents.
---

# Improve Codebase Architecture

Last updated: 2026-08-02

Read memory routing, domain context, ADRs, and `codebase-design`. Scope the survey to the user’s target or recent hot spots.

Identify shallow modules, scattered knowledge, leaky seams, and tests coupled to internals. Apply the deletion test before recommending a new interface.

Write a canonical Markdown report under `docs/architecture/reviews/` with files, problem, proposed deepening, leverage/locality benefit, test impact, ADR conflicts, and recommendation strength. Generate a same-named self-contained HTML view with before/after diagrams. The HTML must cite its Markdown source and generation time.

Ask which candidate to explore. Route the selected candidate into `grilling`; do not refactor during the survey.
