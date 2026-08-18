---
name: wayfinder
description: Plan an effort too large for one session as a shared map of decision tickets with Markdown and HTML dependency views. Use when the destination is known but the route remains foggy or decisions can proceed concurrently.
---

# Wayfinder

Last updated: 2026-08-10

Wayfinding resolves decisions; it does not execute the destination.

## Chart

1. Read shared memory and relevant domain context — including `docs/product/<slug>/prd.md` when the effort has one; the PRD's scope and Not-To-Do lists seed Destination and Out of scope.
2. Use `grilling` to name the destination and scope.
3. Write `<effort>/map.md` with Destination, Notes, Decisions so far, Not yet specified, and Out of scope.
4. Create one Markdown issue per precise decision. Record type, status, blockers, and claim.
5. Render the dependency sources to `roadmap.md` and `roadmap.html` with `draw-portfolio-dag`.
6. Stop after charting; execution requires a separate request.

## Resolve

Work one frontier ticket per session unless independent research tickets are explicitly delegated. Claim before working. Store the full answer in its ticket, append only a linked gist to `map.md`, graduate newly visible fog into tickets, then regenerate both roadmap views. A ticket conversation can't settle can be resolved with `prototype`; the recorded decision lands in the ticket.

The map is complete when no in-scope fog or open decision remains. Hand off to `spec`; do not implement directly unless the effort was explicitly re-scoped.
