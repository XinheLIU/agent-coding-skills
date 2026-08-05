---
description: Configure the shared memory protocol for this repository
argument-hint: "[optional: tracker, work-root, or wiki preference]"
---

# Setup Agent Coding System

Last updated: 2026-08-05

Use the `manage-context` skill. It reads `docs/agents/memory.md` and auto-selects Phase A (setup) when routing is absent, or Phase B (sync) when it exists. Pass `$ARGUMENTS` as preferences, inspect the repository, present the memory configuration for approval, then write it. Do not install dependencies or create empty memory artifacts.
