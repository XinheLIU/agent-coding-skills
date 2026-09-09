# Working Memory Protocol

Last updated: 2026-09-08

Load this reference when creating or maintaining an active effort. Working memory answers: *what is happening now and what happens next?* It is disposable scaffolding under the configured, ignored work root.

## Boundary

Apply the durability test before writing: if deleting the work root would remove a fact the project still needs, route that fact to the Human layer. Working memory keeps drafts, plans, evidence, status, and pointers; Human memory keeps durable product intent, terminology, constraints, and decisions.

Promotion moves a settled fact from Working to its Human-layer owner. Replace the working copy with a pointer while the effort remains active; remove the working artifact when the effort closes.

## Shape

Create only artifacts earned by the active workflow:

```text
<work-root>/<effort>/
├── state.md
├── progress.md
├── brief.md
├── discovery.html   # authoritative shared product records
├── map.md
├── spec.md
├── plan.md
├── issues/NN-<slug>.md
├── research/
├── prototypes/
├── handoffs/
├── diagnosis.md
├── roadmap.md
└── roadmap.html
```

The configured work root and established repository layout win over these defaults. Engineering artifacts that an existing workflow deliberately tracks elsewhere remain there and are linked from `state.md`; working memory does not duplicate them.

Product efforts use [product-memory.md](product-memory.md): record product identity and the durable `product.html` path in state pointers, then follow relevant anchors. Preserve source-backed coverage; no per-skill discovery copies. Before compaction, verify essential durable evidence and rationale do not depend on the effort directory.

## `state.md`

```markdown
# <Effort>: State

Last updated: YYYY-MM-DD

## Status
<Current posture in one or two sentences.>

## Next action
<One concrete action that a cold session can start immediately.>

## Blockers
<Specific blockers, or "none".>

## Pointers
- <Only the artifacts needed to resume.>
```

Update `state.md` after each workflow transition. It is valid when every pointer resolves and `## Next action` needs no reconstruction from prior conversation.

## `progress.md`

Append one dated entry per meaningful transition. Preserve prior entries; correct a mistake with a newer entry.

```markdown
## YYYY-MM-DD: <summary>
<What changed, what was decided, and the relevant source paths.>
```

## Decision issues

An effort that tracks open decisions as tickets uses `issues/NN-<slug>.md` with these visible fields:

```markdown
# NN: <Decision title>

**Status:** todo | claimed | blocked | done | abandoned
**Blocked by:** None | NN - <ticket> | <external condition>
**Claimed by:** None | <agent or person>

## Question
<The exact decision whose answer closes this ticket.>

## Decision
<Answer and evidence; empty while open.>
```

A ticket is frontier work when all ticket blockers are `done` and external conditions are satisfied. Claim it before work. `done` requires a concrete answer in `## Decision`; `abandoned` requires a reason. The Markdown fields own state and dependencies; roadmap views only render them.

## Promotion

| Durable fact found in Working | Route it to |
| --- | --- |
| Product intent, problem framing, scope, or explicit non-goals | the repository's product-intent home |
| Terminology or bounded-context language | the repository's terminology home |
| A settled, hard-to-reverse decision with rationale | the repository's decision-record home |
| A reader-relevant shipped, removed, deprecated, or migrated outcome | the repository's existing changelog or release-history home |

Use the paths the memory config names; where none is configured, propose one and let the user confirm before writing. A specification promotes the same way: the build steps stay in working memory, the design choice they encode moves to the decision-record home, and a noteworthy shipped outcome may become one changelog entry.

Promotion is complete when the Human artifact contains the fact and every working reference points to it instead of repeating it.

## Completion compaction

Close an effort only after repository evidence shows it landed or was abandoned:

1. Verify the outcome against code, tests, configuration, and repository history.
2. Extract lasting rationale, rejected alternatives that prevent re-litigation, and still-normative product facts into their canonical Human-layer owners.
3. Add a concise entry to the repository's existing changelog or release history only when the outcome matters to its readers. Point to the ADR, issue, code, test, or release that holds the core fact.
4. Confirm no unique durable fact remains in the working artifacts.
5. Remove the effort directory and any completed spec, plan, task, handoff, generated view, or scratch file created only to execute it. Remove stale pointers to them.

Do not create an archive or a new changelog solely to retain completed working material. An explicit audit, regulatory, or repository retention rule may require an archive; record that rule and keep only the required evidence.

Completion is compact when the implementation remains discoverable from source and history, durable rationale is canonical, noteworthy outcomes are summarized once, and no finished execution narrative remains in the repository.
