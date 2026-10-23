# acs-corpus-alignment

Last updated: 2026-10-23

Status: implementing
Type: change record
Analysis: [`references/ANALYSIS.md`](../../../references/ANALYSIS.md) · Chinese: [`ANALYSIS.zh-CN.md`](../../../references/ANALYSIS.zh-CN.md)

## Accepted scope

Close the gap between what the reference corpus analysis recommends and what this repository currently does. The analysis ranks 25 changes (B1–B25) against the assumptions ACS carries; this change turns each into one independently deliverable ticket under [`tasks/`](tasks/).

In scope:

- the 25 ranked recommendations, unchanged in intent and IDs;
- the dependency edges and readiness each one actually has today.

Out of scope:

- re-litigating the analysis. A ticket may reject its recommendation only by recording the refusal with evidence.
- changes to `references/`, which is read-only source material.

The current user request authorizes implementation with parallel GPT-6 Astra workers, one pane per task, and closure of finished panes. It does not authorize commits, publication, releases, or new dependency installation.

## What the tickets are for

The analysis separates three deficits. Only two survive model progress:

| Deficit | Decays? | Where this change acts |
| --- | --- | --- |
| Capability — planning, decomposition, staying on task | Yes | Nothing here adds more of it; B9 and B21 remove weight |
| Information — intent, vocabulary, rationale | No | B2, B15, B19, B25 protect it |
| Accountability — self-assessment and unverified claims | No | B7, B12, B13, B16, B19 build it |

Every ticket therefore either **removes decaying scaffolding**, **moves a rule into a sensor**, or **strengthens a record**. A ticket that only adds prose is out of scope.

## Groups

| Group | Tickets | Question it answers |
| --- | --- | --- |
| Catalog and routing | B1, B17 | Does the agent load the right skill without paying for all of them? |
| Human interface | B2, B25, B9 | Who is asked, how, and how much process the task gets |
| Loop | B7, B8, B19, B14 | Who reviews, who rules, and what counts as evidence |
| Discipline | B4, B5, B6, B12, B13, B18 | Which rules become checks rather than sentences |
| Delivery tail | B10, B11 | What happens after green tests |
| Weight and expiry | B3, B21, B22, B20 | What gets smaller, and when it expires |
| Kernel and hosts | B23, B24, B15 | What the host executes instead of the prose |

## Dependency edges

Only real prerequisites are encoded. Shared files are handled in each ticket's coordination note, not by inventing edges.

```text
B2  → B8  → B7
B19 → B7
B19 → B10
B1  → B17
B1  → B23
B14 → B23
B19 → B23
B16 → B22
B9  → B25
B15 → B24
```

Critical path by ticket count: B2 → B8 → B7 (3), tied with B1 → B23 (2) and B9 → B25 (2).

## Ticket index

| Ticket | Outcome | Effort | Readiness | depends_on |
| --- | --- | --- | --- | --- |
| [B1](tasks/B1-catalog-budget.md) | Catalog fits the host budget | S | ready | none |
| [B2](tasks/B2-questioning-protocol.md) | One questioning protocol | S-M | ready | none |
| [B3](tasks/B3-scope-postures.md) | Scope postures have a home | S | ready | none |
| [B4](tasks/B4-tdd-seams.md) | Seam rule; refactor leaves the loop | S | ready | none |
| [B5](tasks/B5-diagnosis-stops.md) | Diagnosis stop rules | S | ready | none |
| [B6](tasks/B6-review-quote-gate.md) | Unquotable findings are unverified | S | ready | none |
| [B7](tasks/B7-review-seat.md) | A reviewer between collect and done | M | ready | B8, B19 |
| [B8](tasks/B8-rulings.md) | Rulings and bounded retries | M | ready | B2 |
| [B9](tasks/B9-rigor-tiers.md) | Three declared tiers | M | ready | none |
| [B10](tasks/B10-release-tail.md) | acs-ship and acs-release | L | needs-design | B19 |
| [B11](tasks/B11-observability.md) | Observability answers on-call questions | M | needs-design | none |
| [B12](tasks/B12-constraint-floor.md) | Constraint floor for silenced checks | M | ready | none |
| [B13](tasks/B13-security-evidence.md) | Security evidence rubric | M | ready | none |
| [B14](tasks/B14-status-json.md) | Status JSON and one next action | S-M | ready | none |
| [B15](tasks/B15-phase-boundary.md) | Phase-boundary rule | S | ready | none |
| [B16](tasks/B16-eval-harness.md) | Behavioral eval harness | L | needs-design | none |
| [B17](tasks/B17-trigger-fixtures.md) | Trigger fixtures and collision pairs | M | ready | B1 |
| [B18](tasks/B18-lesson-ladder.md) | Lessons become checks first | M | ready | none |
| [B19](tasks/B19-evidence-binding.md) | Evidence bound to command and revision | M | ready | none |
| [B20](tasks/B20-generated-boilerplate.md) | No fixed date, no duplicated boilerplate | S-M | ready | none |
| [B21](tasks/B21-compaction-safe-bodies.md) | Compaction-safe skill bodies | S | ready | none |
| [B22](tasks/B22-expiry-audit.md) | Per-model expiry audit | M | needs-design | B16 |
| [B23](tasks/B23-coordination-kernel.md) | Executable coordination kernel | L | needs-design | B1, B14, B19 |
| [B24](tasks/B24-host-primitives.md) | Duties bound to host primitives | M | ready | B15 |
| [B25](tasks/B25-positioning.md) | Audience and default path | S | ready | B9 |

Twenty-five tickets, nineteen execution-ready, five waiting on a decision, one design ticket.

## Readiness

Five tickets are `needs-design` because a decision must land before code:

| Ticket | Decision owed |
| --- | --- |
| B10 | Which commands count as verification, and which environments exist |
| B11 | Whether observability lives in the design contract or the release skill |
| B16 | Which model grades, and what the run budget is |
| B22 | Nothing new; it waits on B16 to supply measurement |
| B23 | Where the kernel lives and in which language |

The rest are `ready`: the files, the measured baseline and the acceptance checks exist.

## Sequencing

| Wave | Tickets | Why together |
| --- | --- | --- |
| 1 | B1, B2, B3, B4, B5, B6, B14, B15, B18, B19, B20, B21, B24 | Independent, cheap, and each removes a contradiction or a stale artifact |
| 2 | B8, B9, B12, B13, B17 | Depend on wave 1's protocol, tier names, or final descriptions |
| 3 | B7, B25 | Depend on rulings, evidence binding, tiers |
| 4 | B10, B11, B16, B23 | Need a design decision or a kernel surface |
| 5 | B22 | Needs the eval harness |

Wave 1 is the answer to "what do I change first": four questioning rules collapse into one protocol, 22 descriptions shrink, and the loop stops accepting unverified green.

## How to use a ticket

Each file carries the fields the task-graph scanner reads (`Status`, `Type`, `Readiness`, `depends_on`, `affects`) and the six sections the delivery format requires. Run:

```bash
python3 system/skills-src/authoring/acs-draw-portfolio-dag/scripts/scan_tasks.py docs/changes/acs-corpus-alignment -o /tmp/acs-corpus-alignment.json
```

Status stays `pending` until execution starts. A completed ticket keeps its evidence in the ticket and moves its status to `done`; stale evidence moves `Readiness` to `needs-review`, never back to `ready` by assumption.

The scanner reports 25 nodes, zero warnings and zero unresolved dependencies. [`delivery-plan.html`](delivery-plan.html) is the derived DAG and reading view; regenerate it after any ticket edit. The Presenter's card-format validator does not apply to this page.

## Non-goals

- No second router, no bootstrap hook, no coercion layer. The analysis refuses all three (§11).
- No spec-as-source code generation.
- No new runtime dependency without explicit authorization.
- No rewrite of the durable core: typed records, freshness propagation, authorization separation, retained rationale, release identity.

## Execution checkpoint — 2026-10-23

22 tickets accepted for their source contracts and recorded local validation. B17 implementation is present but measured routing remains blocked. B16 awaits grading model and budget before harness construction; B22 waits on B16 measurement. All task panes are closed. See ticket evidence for distinctions between scripted fixtures, bounded model exercises, and unverified live-host behavior.
