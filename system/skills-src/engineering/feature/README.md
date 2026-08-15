# Engineering · Feature

Last updated: 2026-08-10

Delivering a feature from PRD to merged code. Consumes `product/definition/write-prd` — directly, or through the optional `design/` phase when the PRD left experience or structure open; produces a spec, a task list, and working code.

| Skill | Owns |
| --- | --- |
| `analyze` | Break down a feature request into components, risks, and unknowns before committing |
| `brainstorm-feature` | Generate implementation approaches for a specific feature |
| `spec` | Technical spec — implementation contract consumed by task breakdown |
| `tasks` | Task list decomposed from spec, sized for one session each |
| `handoff` | Context package for handing work to another agent or session |

The happy path is `spec` → `tasks` → implement. `analyze` is an optional read-only audit after `tasks` — it cross-checks `spec.md`, `plan.md`, and `tasks.md`, so it cannot run first. `brainstorm-feature` precedes `spec` when the implementation approach is non-obvious. `handoff` closes a session without losing state.
