# Canonical Documentation Layout

Last updated: 2026-08-26

Reference for the canonical home of every fact in the three-layer memory model. Load this when:
- **Setting up** — init-context Phase 2, to scaffold the right structure.
- **Checking drift** — sync-context Job A, to enforce canonical homes and required docs.

---

## Governing principle

One fact, one canonical home. The layer is determined by **three tests**:

### 1. The Durability Test
**If the work root were deleted today, would the project lose a fact it still needs?**

- **YES** → Human layer (decisions, constraints, product intent that outlive any single effort)
- **NO** → Working layer (ephemeral exploration, session logs, throwaway drafts)

### 2. The Question Test
**What question does this document answer?**

- **WHY** (decisions, rationale, context) → Human layer
- **WHAT/HOW** (structure, patterns, relationships) → Code Index layer (optional) or read from code
- **NOW** (current status, next action, blockers) → Working layer

### 3. The Source Test
**Can agents derive this from code, manifests, or index?**

- **NO** (decisions code cannot show) → Human layer
- **YES** (current state, structure, patterns) → Code Index or read directly; do not duplicate in docs

When a fact appears in more than one place, the copy in the canonical home wins — the other is drift.

---

## Layer boundaries

| Layer | What belongs | Lifetime | Git |
|---|---|---|---|
| **Human** | Decisions, constraints, terminology, product intent that survive efforts | Project | Tracked |
| **Code Index** | Structure, dependencies, relationships derived from code | Rebuildable | Either |
| **Working** | Session logs, exploration drafts, current status, ephemeral artifacts | Effort | Ignored |

**Key distinction:** Product decisions (WHY we're building this, WHAT problem it solves) belong in Human layer even if discovered during an effort. Implementation specs (HOW to build step-by-step) stay in Working layer unless they document a lasting design choice.

---

## Human layer — what to include

**Include:**
- Project entrypoint (README.md)
- Agent routing (AGENTS.md or CLAUDE.md)
- Vocabulary and bounded contexts (CONTEXT.md)
- Architecture decisions with rationale (docs/adr/)
- Existing changelog or release history for reader-relevant outcomes, with pointers to canonical evidence
- Product intent and problem framing (docs/product/)
- Memory layer configuration (docs/agents/memory.md)

**Exclude:**
- Current code structure (agents read from code or index)
- Coding patterns and conventions (agents infer from code)
- Technology lists without rationale (agents read package manifests)
- Generic guidance applicable to all projects (belongs in team standards)
- Diagrams and graphs agents can generate on demand

**Unification principle:**

When existing docs overlap or duplicate code facts:
- **If it describes a decision with rationale** → extract into ADR or CONTEXT.md
- **If it duplicates what code/manifests already show** → delete; agents read from source
- **If it's generic guidance** → belongs in team standards, not per-repo docs

---

## Code Index layer — canonical location (optional)

The code index path is set by `Code index:` in `docs/agents/memory.md`.

**Purpose:** Indexes code structure, dependencies, and relationships to answer WHAT and HOW questions without reading every file. Agents query the index for structure discovery, then read specific files for implementation details.

**`AGENTS.md` entry invariant:** when code index is enabled, `AGENTS.md` must contain a `## Code index` section naming the tool, path, query command, and refresh command. Without this entry the index is invisible to agents.

**When to enable:** Only when the codebase is large enough that querying an index is faster than grepping and reading files directly.

---

## Working layer — what belongs

**Include:**
- Session logs and progress tracking
- Exploration drafts and brainstorming
- Current status, next actions, blockers
- Implementation plans for current effort
- Prototypes and experiments
- Research notes specific to this effort
- Handoff artifacts for current work

These artifacts remain valid only while the effort is active. Completion triggers compaction, including for specs and plans that an established workflow tracks outside the work root.

**Promote to Human layer when:**
- A decision has rationale that code cannot show → ADR
- A term becomes part of the project vocabulary → CONTEXT.md
- Product intent crystallizes and needs to be shared → docs/product/
- An MVP definition or feature scope needs to outlive the current effort → docs/product/

**The promotion test:** Will another person (or future you) need this fact to understand WHY something exists, even after this work is shipped?

**Gitignore invariant:** The work root must appear in `.gitignore` or `.git/info/exclude`. Working layer artifacts should never be tracked in git.

---

## Classification protocol

Apply these tests to every document when setting up or checking drift:

### Decision tests (in order)

1. **Durability test** — Would the project lose a needed fact if this were deleted?
   - YES → Human or Code Index layer
   - NO → Working layer or delete

2. **Question test** — What question does this answer?
   - WHY (decisions, rationale) → Human layer
   - WHAT/HOW (structure, patterns) → Code Index or derive from code
   - NOW (status, next steps) → Working layer

3. **Source test** — Can agents derive this from code, manifests, or index?
   - NO (decisions code cannot show) → Human layer
   - YES (current state, patterns) → Delete doc; agents read from source

4. **Overlap test** — Does this duplicate content from another doc?
   - YES → Merge into canonical home; delete duplicate

5. **Completion test** — Is the artifact still guiding active work?
   - NO → Extract durable rationale to an ADR, record a reader-relevant outcome in the existing changelog when warranted, then delete the execution artifact

### Classification outcomes

| Status | Meaning | Action |
|---|---|---|
| `OK` | In correct layer, content current, no duplicates | None |
| `MOVE` | Durable content in Working layer, or misplaced within layer | Move to correct location |
| `PROMOTE` | Working layer content that passed durability test | Move to Human layer (ADR, CONTEXT.md, or docs/product/) |
| `DELETE` | Duplicates code facts, generic guidance, or truly ephemeral | Delete after confirming no unique rationale |
| `COMPACT` | A finished plan, spec, scratch artifact, or effort contains a small durable residue | Extract that residue to canonical records, then delete the source artifact |
| `UPDATE` | Correct location but content stale or incomplete | Correct inline |

Precedence: `PROMOTE` > `COMPACT` > `MOVE` > `UPDATE` > `DELETE` > `OK`.

---

## Structural invariants

Required conditions across all three layers. sync-context enforces them on every full run; init-context enforces them before writing anything.

**Human layer:**
1. An agent context file exists at the repo root with routing content, and it is short enough to read in full.
2. The memory config records the work root, issue tracker, and code index status.
3. Every path referenced from a routing file resolves to an existing file.
4. No two documents claim the same fact as their own.

**Code Index layer:**
5. If enabled: the index exists at the configured path, and the routing file names the tool, path, query command, and refresh command.
6. If disabled: the memory config says so explicitly, so an agent does not go looking.

**Working layer:**
7. The work root is git-ignored.
8. Each active effort has a state file whose next action is specific enough to start work without re-deriving context.

Flag violations as `STRUCTURAL`. Trivial violations (broken paths, stale dates) are corrected in place; missing structure requires a setup run.

---

## Common misplacement patterns

| What you find | Why it is misplaced | Outcome |
|---|---|---|
| A doc restating current code structure or module layout | Agents read structure from code or index | DELETE |
| A doc listing patterns the code already demonstrates | Agents infer patterns from code | DELETE |
| A technology list with no rationale | Agents read package manifests | DELETE |
| A technology choice with its trade-off | The rationale is durable and code cannot show it | PROMOTE to a decision record |
| Product intent, problem framing, or scope in the work root | It outlives the effort and needs to be shared | PROMOTE to product docs |
| A term defined inline in several places | Vocabulary needs one canonical definition | PROMOTE to the terminology doc, link elsewhere |
| A design choice buried in a session log | The conclusion is durable; the log is not | PROMOTE the conclusion, leave a pointer |
| Generic engineering advice not specific to this repo | Not a project fact | DELETE (team standards, not repo docs) |
| An implemented spec or completed plan | Its execution sequence is stale; only rationale or outcome may remain useful | COMPACT to an ADR and, when reader-relevant, one changelog entry; then DELETE |
| Finished scratch notes, task state, handoffs, or evidence logs | Their job ended with the effort | DELETE after the completion scan finds no unique durable fact |
