---
name: index-codebase
description: Build and maintain the wiki layer — a machine-generated semantic and procedural index of the code that agents query instead of grepping. Use to set up a code index, choose between codemap/codegraph/graphify/GitNexus, refresh a stale index, or teach AGENTS.md how to query it.
---

# Index Codebase

Last updated: 2026-08-03

Owner of the wiki layer — the generated code-index layer of the context-management collection. Reads `docs/agents/memory.md` for configuration; writes the index location and query instructions into the agent context file. The tool comparison — codemap, codegraph, graphify, GitNexus — ships with this skill at [`references/external-tools.md`](references/external-tools.md).

The wiki layer answers *where is X and what connects to it*. It is generated, not written. An index the agent does not know how to query is dead weight, so the pointer in `AGENTS.md` is part of the deliverable, not an afterthought.

## 1. Check what exists

Look for an index before proposing one: `.codemap/`, `.codegraph/`, `graphify-out/`, `.gitnexus/`, `docs/wiki/`. Check whether the tool is installed and whether an MCP server is already registered. Read the agent context file to see if a pointer already exists.

If an index exists and is merely stale, refresh it — do not switch tools. Competing indexes drift apart and the agent cannot tell which one is lying.

## 2. Choose a tool

Default to **codemap** — fastest, no runtime, covers structure, dependency flow, and blast radius. Choose **codegraph** when staleness is the real problem (it watches the filesystem), **graphify** when the corpus includes PDFs or images, **GitNexus** for multi-repo groups or visual exploration. The full comparison, install commands, and hardening flags are in this skill's `references/external-tools.md`.

State the recommendation and the reason, then confirm before installing. Every option adds a dependency, and the MCP variants edit agent configuration.

## 3. Build the index

Run the tool's own build command from the repo root. Do not run the setup subcommands that rewrite agent config (`codemap setup`, `codegraph install`, `gitnexus setup`) unless the user asked for MCP wiring — report that they exist and let the user choose.

Verify the index is real: query one symbol you can independently confirm in the source. An index that returns nothing is worse than none, because it reads as an authoritative absence.

## 4. Decide the git policy

Track the index by default, so every session and teammate shares one map.

Exclude it when it is large or churns on every commit. Use `.git/info/exclude` rather than the tracked `.gitignore` — the choice is local to the developer who made it and should not be imposed on the repo. Record whichever policy applies in `docs/agents/memory.md`.

## 5. Make it discoverable

Add or update a short section in `AGENTS.md` (or `CLAUDE.md`) naming the tool, the index path, the query command or MCP tool, and when to prefer it over reading files:

```markdown
## Code index
This repo is indexed with <tool>; the index lives at `<path>`.
Query it with `<command>` or the `<mcp-tool>` MCP tool before grepping for
symbols, callers, or change impact. Refresh with `<refresh-command>`.
```

Keep it to a few lines. If the context file is at its line ceiling, hand the detail to `docs/` and leave a pointer — `review-agent-instructions` owns that structure.

## Guardrails

- **Treat the index as a lead, not proof.** Inferred edges, confidence labels, and staleness windows are all fallible. Confirm against the source file before acting.
- Preserve confidence labels (`EXTRACTED` / `INFERRED` / `AMBIGUOUS`) when reporting graphify findings; cite the source file, not the inference.
- Never expose an index server beyond loopback. `codemap serve` has no authentication.
- Do not create watchers, daemons, or git hooks unless the user asked for them.
- Do not commit.

Report the tool chosen, the index path, the git policy, the query entry point, and the pointer written. When the index and the human docs disagree, hand off to `manage-context` (Phase B).
