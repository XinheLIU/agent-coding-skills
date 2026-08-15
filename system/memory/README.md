# Shared Memory System

Last updated: 2026-08-10

Skills in this system coordinate through repository artifacts rather than private session state. The setup command records the repository-specific paths in `docs/agents/memory.md`; every memory-aware skill reads that file before choosing inputs or outputs.

## Layers

A layer is defined by the question its artifacts answer and how long the answer stays true — not by who reads it or which skill wrote it.

| Layer | Answers | Lifetime | Git | Default artifacts |
| --- | --- | --- | --- | --- |
| Core | What words and constraints bind this project | Project | Tracked | `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/adr/` |
| Human | What we are building, why, and how it works | Project | Tracked | `README.md`, `docs/product/` (vision, personas, journeys, PRDs), `docs/architecture/`, `docs/conventions/`, runbooks |
| Wiki | Where the code for X lives | Rebuildable | Tracked or ignored | `docs/wiki/index.md`, `code-map.md`, generated `code-map.html` |
| Working | How the current effort is going and what happens next | Effort | Ignored | `<work-root>/<effort>/state.md`, `progress.md`, discovery drafts, `spec.md`, `plan.md`, `issues/`, research, prototypes, diagnoses, handoffs, roadmaps |

Repositories may preserve an established work root such as `specs/`. The configured path in `docs/agents/memory.md` wins over the default.

## The boundary

**Working memory is scaffolding. The Human and Core layers are the building.**

Apply the durability test before writing anything persistent:

> If the work root were deleted today, would the project have lost a fact it still needs?

If yes, that fact belongs in the Human or Core layer. If no, it belongs in working memory.

This is why a PRD is Human-layer and a `spec.md` is Working-layer even though both are documents written during the same effort. The PRD states what the product is for; it stays true after the effort closes. The spec states how this increment gets built; once the code ships, the code is the better answer.

Concretely:

| Belongs in Human / Core | Belongs in Working |
| --- | --- |
| Product intent — persona, job, demand verdict, user stories, scope commitments, Not-To-Do list | Discovery drafts and the conversation that produced them |
| Architecture boundaries and dependency rules | The plan for changing them |
| Settled trade-offs with rationale (ADRs) | The options considered while deciding |
| Conventions the next contributor must follow | The refactor that establishes one |
| How to operate and deploy the system | Task claims, status, blockers, progress log |

## Promotion

Facts move **up** — Working → Human or Core. Never down.

Promote when a decision is settled, hard to reverse, and would surprise someone who did not watch it happen. When a fact is promoted, the working artifact keeps a link to its new home, not a copy. Write each fact once.

Three promotion points are built into the workflows:

| Trigger | Promotes | To |
| --- | --- | --- |
| Demand gate returns Green (`validate-demand`) | Persona, job, struggle, demand type, evidence grade | `<product-docs>/<slug>/prd.md` Part 1, via `write-prd` |
| Scope is locked (`scope-mvp` → `write-prd`) | Requirement list, in/out-of-scope, Not-To-Do, interaction specs, NFRs | The same PRD, extended |
| A prototype settles an architectural question | The decision and its rationale | An ADR, via `domain-modeling` |

Everything else is promoted by `manage-context` Phase B, which detects settled decisions still sitting in working memory and routes them to their owner.

## Source and view

Markdown is the semantic source of truth. HTML is a first-class human interface, but it must be reproducible from Markdown and declared inputs. Browser-local state may store layout preferences only; task status, decisions, and dependencies remain in Markdown.

## Where the rules live

The skills that create and reconcile these layers are collected in [`craft/context`](../skills-src/craft/context/README.md). `init-context` configures all four layers on first setup; `sync-context` is the one entry point responsible for keeping them consistent after code changes.

The protocol spec — read/write rules, the layer contract, and the ownership registry — travels with its owning skill at [`init-context/references/PROTOCOL.md`](../skills-src/craft/context/setup/init-context/references/PROTOCOL.md), so a skill copied out of this repo carries the contract with it.
