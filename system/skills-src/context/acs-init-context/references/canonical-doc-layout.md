# Canonical Documentation Layout

Last updated: 2026-09-26

[PROTOCOL.md](../../../../protocols/skill-declarations.md#two-memories-and-a-presenter) defines Working/Persistent Memory and Presenter. This guide maps artifact roles to homes; it does not define another layer system. Preserve configured paths and formats.

| Artifact role | Memory / home |
| --- | --- |
| Mission, vision, principles, non-goals | Persistent Intent; relevant product/strategy records |
| Product baseline, applicable design rules, architecture boundaries, runbooks | Persistent Current; configured product, DESIGN.md, architecture, operations docs with evidence/revision |
| Ticket, requirements, review proposals, accepted contracts/designs, decisions, verification, release references | Persistent Changes; existing tracker/docs, otherwise tracked `docs/changes/<change-id>/` |
| Execution plan, claims, checklist, drafts, raw logs, session handoff | Working; configured work root |
| Code map or roadmap view | Presenter view derived from declared sources; no independent facts |
| AGENTS.md and docs/agents/memory.md | Routing indexes into the above; no duplicate normative facts |
| Product source — the artifact this repository builds | `NOT-CONTEXT: product-source`; governed by its own domain skills, not by retention |
| Generated build output reproducible from source | `NOT-CONTEXT: generated`; report staleness, never edit in place |
| Vendored or copied third-party corpus | `NOT-CONTEXT: external`; read-only, never edited or committed |
| Repository interface and legal — README, LICENSE, notices, install guide | `NOT-CONTEXT: interface`; repair only a broken routing pointer inside them |

A changelog is not `NOT-CONTEXT`. It is the promotion destination for retained summaries, which makes it Persistent Changes: a compacted, release-linked history.

A product HTML document may contain Persistent Intent, Current and Changes records. Proposed review inputs are Persistent before acceptance; discovery drafts remain Working only while no review or downstream reliance needs them. An ADR preserves historical rationale; a System State summary states applicable boundaries now. The prototype preserves accepted design intent; shipped code establishes actual behavior. Do not require a synchronized second UI implementation.

## Classification during setup or sync

Classify on two axes. The memory class says what kind of record a document is; the disposition says what happens to it. Keeping them separate stops a state (`OK`), a gap (`MISSING`) and an action (`PROMOTE`) from competing for one column.

| Memory class | Holds |
| --- | --- |
| `INTENT` | Persistent Intent: mission, vision, principles, non-goals |
| `CURRENT` | Persistent Current: evidenced behavior, applicable design rules, boundaries, runbooks |
| `CHANGES` | Persistent Changes: ticket/spec, proposals, accepted decisions, ADRs, verification, release history |
| `WORKING` | Working Memory: execution plan, checklist, task breakdown, claims, drafts, raw output |
| `VIEW` | Derived Presenter view: report, code index, roadmap render |
| `ROUTING` | Routing index: pointers only, no normative facts |
| `NOT-CONTEXT` | Not a memory record; names one reason code from the table above |

| Finding | Action |
| --- | --- |
| `OK` | Correct home, usable evidence and references |
| `UPDATE` | Repair a stale assertion or reference within ownership; freshness needs evidence, not merely a new date |
| `STRUCTURAL` / `MISSING` | Repair missing routing or required substantive context; do not scaffold empty domains |
| `MOVE` / `PROMOTE` | Reconcile a durable fact from scratch into its domain's canonical record and leave a pointer |
| `COMPACT` | Retain compact Persistent Changes and reconcile Persistent Current; remove only disposable execution detail |
| `DELETE` | Remove a redundant copy or reconciled scratch within authorized scope after checking inbound links and unique evidence |
| `EXPIRE` | Remove Working Memory past the retention window after promoting its unique durable facts and obtaining explicit confirmation; age authorizes the decision, not the skipping of promotion |
| `OUT-OF-SCOPE` | A `NOT-CONTEXT` row: named, counted, and not acted on; a broken routing pointer inside it is still `UPDATE` |

`DELETE` and `EXPIRE` differ in what authorizes them. `DELETE` rests on redundancy — a second copy exists, or the content is reconciled scratch. `EXPIRE` rests on age plus confirmation: nothing about the document is redundant, it is being let go. A reader confirming the plan needs to see which claim each row makes.

## Census

An inspection scoped to changed paths cannot see a document that no commit has touched since the one that shipped it. A census fixes that by accounting for every document in the boundary.

Scan tracked documents, then name any untracked scan separately:

```bash
git ls-files '*.md' '*.html'
```

Do not walk the filesystem for the boundary. A bare `find` descends into vendored corpora that repository instructions forbid touching, inflating the count with files no disposition applies to.

Class follows role, not location. A tracked, committed execution plan under `docs/` or the repository root is `WORKING` that was misfiled, and the retention window applies to it. Directory alone never settles the class in either direction.

Every document in the boundary appears in exactly one classification row, or inside one named exclusion rule carrying its file count. Classified rows plus excluded counts equal the scan count; that arithmetic is what makes the census reviewable, and "etc." breaks it.

Current-state architecture or runbook summaries are useful when they explain present truth and cite executable sources. Do not delete them merely because source code can also answer part of the question. No classification authorizes rewriting another domain's accepted decisions.

## Verification

Routing files point to accessible records and name when to read them. The memory config identifies canonical tracker/change paths, run root, single configured recovery entry, and index status. Canonical reviewed versions and required assets are retrievable. Derived views contain no unique domain conclusions. Run scratch is ignored without accidentally ignoring retained change records. If an index is enabled, record its tool, path, query and refresh commands and verify a source-backed query. If disabled, say so explicitly. At completion run the retention gate from the protocol, including checking durable links while scratch is unavailable.
