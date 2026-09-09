---
name: wayfinder
description: Map a multi-session effort into dependency-ordered decision tickets. Use when the destination is known but the route is unclear, or independent decisions can proceed concurrently.
---

# Wayfinder

Last updated: 2026-08-25

Wayfinding resolves the route; the delivery workflow executes it.

## Chart

1. Read shared memory and relevant domain context, including the effort PRD when present. Extract the destination, fixed scope, and explicit exclusions.
2. Use `grilling` until destination and scope are concrete enough to distinguish an in-scope decision from an unrelated question.
3. Write `<effort>/map.md` with Destination, Decisions so far, Open decisions, and Out of scope.
4. Create one `issues/NN-<slug>.md` per open decision. Each ticket records status, blockers, claim, and the exact question whose answer closes it.
5. Use `draw-portfolio-dag` to regenerate `roadmap.md` and `roadmap.html`. Charting is complete when every open decision is represented once and every dependency is either an edge or an explicit external blocker.

## Resolve

Work one frontier ticket per session unless the user authorizes independent tickets to run concurrently. Claim the ticket before working, store its full answer in the ticket, and keep only a linked summary in `map.md`. Turn newly exposed uncertainty into tickets, then regenerate both roadmap views.

The map is complete when no in-scope open decision remains. Hand the resolved map to `spec`; implementation requires a separate request or an explicit scope change.
