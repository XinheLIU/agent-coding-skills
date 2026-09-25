# Canonical Documentation Layout

Last updated: 2026-09-25

[PROTOCOL.md](../../../../protocols/skill-declarations.md#two-memories-and-a-presenter) defines Working/Persistent Memory and Presenter. This guide maps artifact roles to homes; it does not define another layer system. Preserve configured paths and formats.

| Artifact role | Memory / home |
| --- | --- |
| Mission, vision, principles, non-goals | Persistent Intent; relevant product/strategy records |
| Product baseline, applicable design rules, architecture boundaries, runbooks | Persistent Current; configured product, DESIGN.md, architecture, operations docs with evidence/revision |
| Ticket, requirements, review proposals, accepted contracts/designs, decisions, verification, release references | Persistent Changes; existing tracker/docs, otherwise tracked `docs/changes/<change-id>/` |
| Execution plan, claims, checklist, drafts, raw logs, session handoff | Working; configured work root |
| Code map or roadmap view | Presenter view derived from declared sources; no independent facts |
| AGENTS.md and docs/agents/memory.md | Routing indexes into the above; no duplicate normative facts |

A product HTML document may contain Persistent Intent, Current and Changes records. Proposed review inputs are Persistent before acceptance; discovery drafts remain Working only while no review or downstream reliance needs them. An ADR preserves historical rationale; a System State summary states applicable boundaries now. The prototype preserves accepted design intent; shipped code establishes actual behavior. Do not require a synchronized second UI implementation.

## Classification during setup or sync

| Finding | Action |
| --- | --- |
| `OK` | Correct home, usable evidence and references |
| `UPDATE` | Repair a stale assertion or reference within ownership; freshness needs evidence, not merely a new date |
| `STRUCTURAL` / `MISSING` | Repair missing routing or required substantive context; do not scaffold empty domains |
| `MOVE` / `PROMOTE` | Reconcile a durable fact from scratch into its domain's canonical record and leave a pointer |
| `COMPACT` | Retain compact Persistent Changes and reconcile Persistent Current; remove only disposable execution detail |
| `DELETE` | Remove a redundant copy or reconciled scratch within authorized scope after checking inbound links and unique evidence |

Current-state architecture or runbook summaries are useful when they explain present truth and cite executable sources. Do not delete them merely because source code can also answer part of the question. No classification authorizes rewriting another domain's accepted decisions.

## Verification

Routing files point to accessible records and name when to read them. The memory config identifies canonical tracker/change paths, run root, single configured recovery entry, and index status. Canonical reviewed versions and required assets are retrievable. Derived views contain no unique domain conclusions. Run scratch is ignored without accidentally ignoring retained change records. If an index is enabled, record its tool, path, query and refresh commands and verify a source-backed query. If disabled, say so explicitly. At completion run the retention gate from the protocol, including checking durable links while scratch is unavailable.
