---
name: sync-context
description: Detect and repair shared-context drift after setup. Use for broken routing, stale Human-layer facts, an outdated code index, or working memory that no longer matches repository state; use init-context when routing is absent.
---

# Sync Context

Last updated: 2026-09-08

`docs/agents/memory.md` is the prerequisite. When it is absent, hand off to `init-context`.

Read the layer and ownership contract in [`references/PROTOCOL.md`](references/PROTOCOL.md). Load [`references/canonical-doc-layout.md`](references/canonical-doc-layout.md) for routing classification. Load the code-index or working-memory references only when the selected mode reaches those branches.

## Modes

| Mode | Trigger | Scope |
| --- | --- | --- |
| Fast | Default, after a narrow change | Routing paths, pointers, and commands |
| Full | `--full`, pre-handoff, after a merge, or periodic maintenance | Fast checks plus Human facts, code index, and active working memory |

## 1. Establish the boundary

Read the memory config and resolve all enabled roots. Select a concrete comparison boundary from the requested commit range, merge, release, or last successful sync; use document dates only as a fallback. Inspect changed, moved, and deleted files plus dependency changes.

The baseline is complete when every later finding can cite either current repository state or a diff since the boundary.

## 2. Audit routing

For each existing routing document, verify:

- local paths resolve and each pointer states when to follow it;
- literal commands match current configuration and execute where safe;
- `Last updated:` reflects relevant changes;
- each durable fact appears in one canonical home;
- `AGENTS.md` or `CLAUDE.md` remains an index instead of a cache of discoverable repository facts.

Classify each finding as `OK`, `UPDATE`, `STRUCTURAL`, `MISSING`, `MOVE`, `PROMOTE`, `COMPACT`, or `DELETE`. A legacy architecture, conventions, quality, or technology document is a migration candidate when it only caches current code or configuration; retain unique rationale by moving it to `CONTEXT.md` or an ADR before proposing deletion.

Routing is audited when every path and changed fact in scope has one classification and one owner.

## 3. Audit full-mode branches

### Code index

When enabled, query a symbol changed since the boundary and confirm the result against source. A stale index is refreshed with its recorded command. Load [`references/index-tools/external-tools.md`](references/index-tools/external-tools.md) only when the configured tool cannot be identified or operated from repository instructions.

This branch is complete when the configured index is explicitly disabled or a source-verified query succeeds.

### Working memory

Load [`references/working-memory.md`](references/working-memory.md). For each active effort, verify that:

- `state.md` matches landed or abandoned work;
- `## Next action` is directly executable;
- every pointer resolves to substantive content;
- issue status, blockers, and claims agree with repository history;
- generated views can be rebuilt from their declared sources;
- product HTML is audited as a semantic source under [the product contract](references/product-memory.md): shared IDs and anchors resolve, relevant evidence and accepted decisions remain distinct, and stale dependent conclusions are visible. Do not demand a Markdown source or regenerate product HTML.

For product promotion or compaction, verify essential durable evidence and rationale survive effort deletion. Route accepted amendments and disputed assessments to the relevant product skill; do not overwrite them as factual routing repairs.

Apply the durability test to working facts: if deleting the work root would lose a fact the project still needs, flag it for promotion to its Human-layer owner.

Scan the work root and tracked documentation locations for finished execution artifacts, including implemented specs, completed plans, closed task files, obsolete handoffs, generated working views, and scratch notes. For each completed effort, propose one `COMPACT` action:

- rationale and meaningful rejected alternatives -> the existing decision-record home;
- reader-relevant shipped outcome -> the existing changelog or release-history home;
- current behavior and verification -> pointers to code, tests, configuration, issues, or release records;
- remaining execution narrative -> delete after confirming it contains no unique durable fact.

Do not propose an archive unless an explicit retention rule requires it. Do not create a changelog merely to preserve working history.

This branch is complete when every active effort has a valid next action, every finished artifact has a verified compaction or deletion finding, and every durable fact has a canonical destination.

## 4. Report and apply

Report findings before structural writes, promotions, or deletions. Each finding names evidence, classification, canonical owner, exact action, and verification. Ask for one approval covering the numbered action plan; a skipped action remains unchanged.

This skill may directly repair factual routing, refresh an enabled index, update current `state.md` fields, and regenerate views. Route structural work as follows:

| Finding | Owner |
| --- | --- |
| Missing memory configuration or layer structure | `init-context` |
| Instruction-file hierarchy or pointer quality | `review-agent-instructions` |
| Product intent awaiting promotion | the skill that owns product docs, when one is installed |
| Terminology or a durable technical decision | the skill that owns decisions and terminology, when one is installed |
| Reader-relevant completed change | the workflow that owns the existing changelog or release history, else the user |

Where no such skill is installed, report the promotion candidate and leave authoring to the user. This skill detects misplacement; it does not author decisions.

Apply independent actions concurrently only when their files and state do not overlap. Update `Last updated:` in every edited Markdown file and preserve unrelated user content.

Synchronization is complete when every approved action is verified, every deferred action is explicit, all routing pointers resolve, no promoted fact remains duplicated in working memory, and no approved completed execution artifact remains. Leave commits to the user.
