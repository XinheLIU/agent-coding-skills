# Brainstorm Strategy Variants

Last updated: 2026-08-06

## Systematic (`--strategy systematic`)

**Best for**: Greenfield products, complex domains, deep feasibility research.

**Phase sequence**:
1. **Clarify** — Ask 3–5 targeted Socratic questions to surface assumptions and constraints
2. **Decompose** — Break the idea into functional domains (data, logic, UI, integrations)
3. **Multi-persona sweep** — Rotate through relevant expert lenses:
   - Architect: system design, scalability, tech stack trade-offs
   - Analyst: feasibility, market fit, risk identification
   - Domain expert: business rules, compliance, edge cases
4. **Synthesize** — Consolidate findings into a structured requirements draft
5. **Handoff** — Output an actionable brief with open questions flagged

**Tools to prefer**: the runtime's normal reasoning tools; available search for technology validation; `<effort>/discovery/brainstorm.md` for cross-session persistence.

---

## Agile (`--strategy agile`)

**Best for**: Feature scoping, sprint planning, rapid iteration on existing products.

**Phase sequence**:
1. **Goal alignment** — Confirm the desired user outcome in one sentence
2. **Parallel exploration** — Spawn independent threads for frontend, backend, and integration concerns (use `--parallel` flag)
3. **Slice ruthlessly** — Identify the smallest shippable unit; push everything else to backlog
4. **Story draft** — Produce 2–4 user stories ready for estimation
5. **Risk flag** — Surface top 2–3 blockers or unknowns

**Tools to prefer**: `Task` for parallel exploration threads; `mcp__magic__21st_magic_component_builder` for UI feasibility; `TaskCreate` / `TaskUpdate` for backlog tracking.

---

## Enterprise (`--strategy enterprise`)

**Best for**: Large-scale platforms, regulated industries, multi-stakeholder alignment.

**Phase sequence**:
1. **Stakeholder map** — Identify primary, secondary, and regulatory stakeholders
2. **Constraint inventory** — Document compliance, security, SLA, and integration requirements before any solution design
3. **Architecture review** — Evaluate proposed approach against enterprise patterns (SSO, audit logging, RBAC, data residency)
4. **Cross-domain validation** — Security, DevOps, and data governance lenses applied sequentially
5. **Discovery record** — Produce a structured record in `<effort>/discovery/brainstorm.md`

**Tools to prefer**: repository memory for persistent context; available search for compliance standards; normal file editing for the configured discovery artifact.

---

## Depth Modifiers

| Flag | Behaviour |
|------|-----------|
| `--depth shallow` | Skip multi-persona sweep; produce a one-page summary only |
| `--depth normal` | Default — full phase sequence, moderate detail |
| `--depth deep` | Extended questioning rounds, competitive research via `WebSearch`, full specification output |

## Parallel Flag (`--parallel`)

When `--parallel` is set, use the `Task` tool to launch independent sub-agents for distinct exploration threads (e.g., frontend feasibility and backend architecture simultaneously). Synthesize results before the Handoff phase.
