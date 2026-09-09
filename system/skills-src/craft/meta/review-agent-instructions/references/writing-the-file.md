# Writing the Instruction File

Last updated: 2026-08-25

Load only for an approved structural rewrite. This is a hierarchy guide, not a required template.

## Order by need

1. **Purpose:** enough domain intent to orient the agent; link the durable product source when one exists.
2. **Verified commands:** literal commands whose omission would slow or misdirect work.
3. **Repository constraints:** cross-cutting, checkable behavior with consequences and alternatives.
4. **Shared-context startup:** how to resolve active work and canonical Human-layer facts.
5. **Context pointers:** trigger -> target for branch-specific detail.
6. **Danger zones and historical reasons:** only when experience earned them.

Omit any section with no behavior-changing content. Use the repository's existing headings when they already express this order clearly.

## Content tests

| Candidate content | Keep inline when | Otherwise |
| --- | --- | --- |
| Project description | A short statement prevents domain confusion | Point to product docs |
| Command | It is literal, current, and frequently needed | Leave it discoverable in configuration |
| Constraint | Every session needs it and violation is observable | Scope it or point to its canonical owner |
| Procedure | Every relevant branch follows it | Put it in a skill or document and keep a trigger pointer |
| Current structure | It is a routing table that saves meaningful search | Let agents inspect source or the configured index |
| History | It explains a surprising constraint | Record an ADR and point to it |

## Pointer format

A useful pointer names both branch and target:

```markdown
- Before changing settlement response shapes, read `docs/adr/0012-settlement-contract.md`.
```

“See docs for more information” has a target category but no branch and should be sharpened or removed.

## Constraint format

Lead with required behavior. Add the prohibition only when the hard boundary matters:

```markdown
- Add settlement characterization coverage in `tests/settlement/` before changing
  `OrderService.calculateTotal`; the untested batch consumer shares this contract.
```

## Reject

- Generic engineering advice the agent already follows
- Restatements of manifests, schemas, directory trees, or generated indexes
- Rules with no repository evidence or plausible failure
- Unverifiable adjectives such as “clean,” “careful,” or “robust”
- Pointers without trigger conditions
- The same meaning in multiple runtime or documentation files without a canonical owner
- Fixed section filling or line-count optimization that ignores behavioral value
