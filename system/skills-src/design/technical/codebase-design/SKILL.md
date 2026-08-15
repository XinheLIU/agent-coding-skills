---
name: codebase-design
description: Apply shared deep-module vocabulary to interfaces and test seams. Use when designing or improving a module, deciding where behavior belongs, or making code more testable and agent-navigable.
---

# Codebase Design

Last updated: 2026-08-10

Use these terms consistently:

- **Module**: anything with an interface and implementation.
- **Interface**: every fact a caller must know, including invariants and failures.
- **Seam**: a place where behavior can vary without editing the caller.
- **Adapter**: a concrete implementation at a seam.
- **Depth**: behavior exposed per unit of interface.
- **Leverage**: capability gained by callers.
- **Locality**: change and verification concentrated in one place.

Prefer a small interface hiding substantial behavior. Apply the deletion test: deleting a useful module redistributes complexity across callers; deleting a pass-through removes complexity. Treat the interface as the public test surface. Introduce a seam when real variation exists, not for hypothetical flexibility.

This skill owns vocabulary, not persistent artifacts. Record accepted designs in the active `plan.md` or an earned ADR — `tasks` and `tdd` consume them. The PRD or spec naming the behavior is the upstream input when one exists.
