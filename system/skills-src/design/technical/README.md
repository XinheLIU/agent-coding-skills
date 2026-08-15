# Design · Technical

Last updated: 2026-08-10

System architecture and structural decisions — the load-bearing design choices that constrain implementation. Feeds `engineering/feature` and `engineering/frontend`. Upstream: the effort PRD (`docs/product/<slug>/prd.md`) when one exists; entry criteria live in [`../README.md`](../README.md) and the `write-prd` design gate.

| Skill | Owns |
| --- | --- |
| `domain-modeling` | Core domain entities, relationships, and invariants |
| `codebase-design` | Module boundaries, layer responsibilities, dependency rules |
| `design-agent-architecture` | Agent topology, tool contracts, and memory protocols |
| `design-operational-ontology` | Operational concepts, taxonomy, and shared vocabulary for a domain |
| `improve-codebase-architecture` | Identify and reduce structural debt in an existing codebase |

Architecture decisions that need a record of their rationale belong in ADRs — use `codebase-design` to scaffold that. Design review lives in `quality/review/review-architecture`.
