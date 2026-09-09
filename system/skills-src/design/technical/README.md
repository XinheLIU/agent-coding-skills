# Design · Technical

Last updated: 2026-09-09

System architecture and structural decisions — the load-bearing design choices that constrain implementation. Feeds `engineering/feature` and `engineering/frontend`. Upstream: the product document resolved through `docs/agents/memory.md` and `state.md` (`product.html#prd`, or a canonical legacy PRD) when one exists; entry criteria live in [`../README.md`](../README.md) and the `write-prd` design gate.

| Skill | Owns |
| --- | --- |
| `domain-modeling` | Core domain entities, relationships, and invariants |
| `codebase-design` | Module boundaries, layer responsibilities, dependency rules |
| `design-agent-architecture` | Agent topology, tool contracts, and memory protocols |
| `design-operational-ontology` | Operational concepts, taxonomy, and shared vocabulary for a domain |
| `improve-codebase-architecture` | Identify and reduce structural debt in an existing codebase |

The two skills that emit a diagram — `design-agent-architecture` and `design-operational-ontology` — offer an installed **diagramming** capability for it (one that renders a described structure into an exportable SVG, HTML, or image) and fall back to drawing it directly. That offer is stateless: technical skills hold no effort-scoped memory and write no capability record. Adversarial challenge is already native here — `improve-codebase-architecture` routes candidates into `grilling`.

Architecture decisions that need a record of their rationale belong in ADRs — use `codebase-design` to scaffold that. Design review lives in `quality/review/review-architecture`.
