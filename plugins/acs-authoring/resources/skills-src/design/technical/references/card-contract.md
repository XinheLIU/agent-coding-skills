# Technical Design Card Contract

Last updated: 2026-09-29

Technical design is split into **aspect cards**. Each card owns one aspect end to end: it assesses what exists, designs the target, and reviews the proposal. All cards write to **one shared record**, so running several cards produces one document, not several overlapping reports.

| Card | Aspect | Section | ID prefix |
| --- | --- | --- | --- |
| `acs-technical-design` | Router: scope, card selection, cross-card consolidation | `## Overview` | — |
| `acs-design-architecture` | System shape, capabilities, shared foundations, data/tech/deploy fit, decisions | `## Architecture` | `ARC` |
| `acs-design-modules` | Responsibilities, interfaces, dependency direction, wiring, migration | `## Modules & Interfaces` | `MOD` |
| `acs-design-contracts` | Invariants, pre/postconditions, errors, failure modes, evolution | `## Contracts & Correctness` | `CON` |
| `acs-design-test-strategy` | Test layers, seams, doubles, fixtures, gates, verification per item | `## Test Strategy` | `TST` |
| `acs-trace-requirements` | Requirement → entry → module → contract → test reachability | `## Traceability` | `TRC` |

## Record

The canonical record is `docs/design/technical-design.md`, unless `docs/agents/memory.md` or an explicit user path names an established home. Change-scoped work cites record IDs from `docs/changes/<change-id>/`; it never forks a second technical-design file. Create the record from the skeleton below on first use; keep sections a card has not run as a one-line `Status: not assessed`.

```markdown
# Technical Design — <system>

Last updated: YYYY-MM-DD
Consumed: <spec/criteria IDs@revision> · Source baseline: <commit>

## Overview
## Architecture (ARC)
## Modules & Interfaces (MOD)
## Contracts & Correctness (CON)
## Test Strategy (TST)
## Traceability (TRC)
## Findings Ledger
## Decisions
```

## Section schema

Every card section uses the same four blocks, so readers and downstream skills parse all cards the same way:

```markdown
## <Card> (<PREFIX>)
Status: not assessed | draft | proposed | accepted · Mode: design | review · Consumed: <upstream IDs@revision>

### Current
Evidence-backed state of this aspect (brownfield only). Every claim carries a file:line or record anchor.

### Target
Items with stable IDs (`ARC-3`, `MOD-7` …). IDs are never reused; a removed item stays as `~~ARC-3~~ superseded by ARC-9`.

### Decisions
Links to ADRs or `## Decisions` rows. Consequential rationale lives there, not inline.

### Open
Unresolved questions, each naming the owning card and what it blocks.
```

## Card loop

Every card runs the same loop, in one of two modes:

- **design** — no accepted target exists for this aspect; produce one.
- **review** — a target exists (in the record, or in a plan/RFC the user supplies); check it against requirements, upstream sections, and the code.

1. **Read.** Load the record, the upstream sections this card consumes, and the requirement/criterion IDs. Record their revisions in `Consumed:`.
2. **Assess current.** For brownfield scope, reconstruct this aspect from the code with anchors. Skip for greenfield.
3. **Design or review the target.** Apply the card's lenses. In review mode, every problem becomes a ledger finding against a target item.
4. **Write.** Update only this card's section and this card's ledger rows. Set `Status: proposed` before any human review.
5. **Hand off.** Return target IDs, findings, open items, and the next card. Ask Presenter to refresh the view when a human will read it.

## Findings ledger

One table for all cards. A finding is a problem; a target item is a design. Findings point at the target item they threaten.

```markdown
| ID | Sev | Conf | Anchor | Target | Finding | Status | Routed to |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FND-ARC-1 | P0 | HIGH | src/a.ts:40 | ARC-2 | Orders writes Billing's table directly | open | MOD |
```

- **Severity:** `P0` data loss, security breach, or outage · `P1` visible bug or major rework · `P2` maintenance friction.
- **Confidence:** `HIGH` verified in code or stated in the record · `MEDIUM` strong pattern match · `LOW` plausible; kept out of summaries. Never promote a `LOW` finding to `P0`.
- **Status:** `open` · `accepted` (risk taken, cite decision) · `resolved` (cite the target revision that fixed it) · `routed` (another card or skill owns it).
- **Dedupe** by anchor. When two cards flag the same anchor, keep one row and add `Confirmed by: ARC, CON` in the Finding cell.
- **Quote evidence**; do not paraphrase anchors away.

## Ownership rules

- A card writes only its own section and rows whose ID carries its prefix. It may change another card's row only to add `Confirmed by`.
- A cross-card problem becomes an `Open` item on the owning card plus a `routed` finding; the discovering card does not fix it.
- Code-level defects (a handler bug, a missing timeout, an N+1 query) route to `acs-review-code-quality`. Behavior-preserving code changes route to `acs-refactor-code`. Implementation routes to `acs-implement`.
- Terminology conflicts route to `acs-engineer-domain-model`.

## Handoff order

```text
requirements → ARC → MOD → CON → TST → TRC(pre-build) → build → TRC(post-build)
```

The order is a dependency, not a ceremony: a card may run alone whenever its upstream sections are accepted or explicitly out of scope. A card whose upstream is missing says so and stops, or runs in review mode against the code alone and labels its section `Consumed: code only`.

## View

`docs/design/technical-design.html` is a rebuildable view of the record. Build it from [the technical view template](technical-view.md). Deleting the view loses nothing.
