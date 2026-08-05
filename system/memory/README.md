# Shared Memory System

Last updated: 2026-08-03

Skills in this system coordinate through repository artifacts rather than private session state. The setup command records the repository-specific paths in `docs/agents/memory.md`; every memory-aware skill reads that file before choosing inputs or outputs.

## Layers

| Layer | Purpose | Default artifacts |
| --- | --- | --- |
| Core | Stable vocabulary, decisions, and architecture | `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/`, Markdown architecture documents, generated HTML architecture views |
| Human | Documentation optimized for maintainers and users | `README.md`, `docs/`, runbooks, conventions, reports |
| Wiki | Optional navigation for large codebases | `docs/wiki/index.md`, `code-map.md`, generated `code-map.html` |
| Working | Active effort state shared across sessions and agents | `.scratch/<effort>/state.md`, discovery records, PRD, specs, decision maps, issue files, research, diagnoses, handoffs, `roadmap.md`, generated `roadmap.html` |

Repositories may preserve an established work root such as `specs/`. The configured path in `docs/agents/memory.md` wins over the default.

The skills that create and reconcile these layers are collected in the [`context-management`](../skills-src/context-management/README.md) category, which also documents the external indexers available for the wiki layer. `manage-context` Phase B is the one entry point responsible for keeping the layers consistent with each other.

## Source and view

Markdown is the semantic source of truth. HTML is a first-class human interface, but it must be reproducible from Markdown and declared inputs. Browser-local state may store layout preferences only; task status, decisions, and dependencies remain in Markdown.

The protocol spec — read/write rules and the ownership registry — travels with its owning skill at [`manage-context/references/PROTOCOL.md`](../skills-src/context-management/manage-context/references/PROTOCOL.md), so a skill copied out of this repo carries the contract with it.
