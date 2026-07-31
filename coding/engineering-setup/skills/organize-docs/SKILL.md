---
name: organize-docs
description: Audit and organize repo documentation into clear, MECE canonical homes. Use when the user asks to scan docs, clean up markdown, dedupe documentation, move docs under /docs, or reorganize READMEs and reference files without touching runtime skill, prompt, or agent-package definitions.
disable-model-invocation: true
---

**Announce at start:** "I'm using the organize-docs skill to audit and reorganize repo documentation."

## Goal

Audit repo documentation for necessity, accuracy, conflicts, redundancy, and ownership. Then propose a concrete reorganization plan that makes the docs set **clear**, **MECE**, and biased toward **canonical homes under `/docs`**. Apply changes only after user confirmation.

This skill is not just a scanner. It should try to leave the repo with a cleaner documentation layout than it found.

**Scope boundary with `review-claude-md`:** This skill may fix factual doc issues anywhere in scope, including `CLAUDE.md`, but it does NOT do a Claude-principles review or rewrite Claude-specific guidance strategy. That remains `review-claude-md`'s job.

---

## In Scope vs Out of Scope

### In scope

- Project docs such as root `README.md`, `AGENTS.md`, `CLAUDE.md`, `DESIGN.md`, docs under `/docs`, architecture notes, API docs, runbooks, specs, and service/module READMEs.
- Markdown files whose primary role is to document the repo, a module, an interface, or an operational workflow.

### Out of scope

- Any runtime-specific skill, prompt, or agent-package tree, regardless of vendor or folder name. This includes examples such as `skills/`, `.claude/skills/`, `.codex/skills/`, opencode skills, Gemini/Gems-style prompt packs, Trae agent assets, and similar runtime-owned bundles the agent judges to be implementation material rather than repo docs.
- Bundled materials beneath those trees, such as `references/`, `assets/`, `evals/`, examples, templates, test fixtures, or skill-local docs.
- Vendored, generated, cache, and dependency directories such as `node_modules/`, `.git/`, `.venv/`, build outputs, coverage outputs, and lockfiles.

If a markdown file lives under one of those runtime-owned trees, treat it as implementation material, not repo documentation. Use judgment by ownership and purpose, not just by directory name. Do not audit, reorganize, or rewrite it with this skill.

---

## Doc Ownership Model

Prefer a MECE layout. Each doc should have one primary job and one canonical home. For a project knowledge base, **two levels is usually the sweet spot**. The goal is discoverability, not perfect taxonomy.

Use this default ownership model:

- Root `README.md`: shortest possible entrypoint to the repo.
- Root context files like `AGENTS.md` / `CLAUDE.md`: contributor or runtime instructions that must stay at repo root.
- `/docs/architecture/`: **How the system works.** Contains system architecture, C4 diagrams, domain/data models, core workflows, entry points, external dependencies, service contracts, critical paths, scalability/security considerations, and Architecture Decision Records (ADRs). Rule: *If a new engineer asks "how is this system built?", the answer should be here.*
- `/docs/product/`: **What we are building and why.** Contains product vision, capability map, product boundaries, personas, user journeys, user stories, PRDs, and acceptance criteria. Rule: *If a PM asks "what problem are we solving?" the answer should be here.*
- `/docs/conventions/`: **How we write software.** Contains coding standards, naming conventions, API design guidelines, testing standards, logging/observability standards, configuration management, Git workflow, and deployment conventions. Rule: *If two engineers disagree on implementation style, this folder decides.*
- `/docs/quality/`: **What good looks like.** Contains Definition of Done, quality gates, testing strategy, performance requirements, reliability requirements, security requirements, and release checklists. Rule: *Before something is considered complete, it must satisfy this folder.*
- `/docs/tech-decisions/`: **Why we made certain choices.** Contains technology selection rationale, tradeoff analyses, alternatives considered, and major decisions and outcomes. Rule: *Every significant decision should have a recorded reason.*
- `/docs/runbooks/`: **How to operate the system.** Contains deployment procedures, monitoring guides, incident response, recovery procedures, and troubleshooting guides. Rule: *If production is on fire, people read this folder.*
- `/docs/data/`: **Shared understanding of data.** Contains metrics definitions, semantic layer, entity definitions, data contracts, data quality rules, feature definitions, and lineage documentation. Rule: *Any business metric should have exactly one authoritative definition here.*
- `/docs/agents/`: **Agent-specific architecture and behavior.** Contains agent architecture, skills, tools, memory systems, planning approaches, evaluation datasets, guardrails, prompting strategies. Rule: *Everything unique to AI/Agent behavior belongs here, not in architecture.*
- `/docs/exec-plans/`: **Execution and project management.** Contains active plans, completed plans, backlog, roadmap, technical debt tracker, design proposals, and postmortems. Rule: *This folder changes frequently; everything else should be relatively stable.* Sub-level advice:
  ```text
  ├── active/              ← Currently ongoing plans (empty directory, keep .gitkeep)
  ├── completed/           ← Completed plans (empty directory, keep .gitkeep)
  ├── backlog.md           ← Pending features list (known requirements, unscheduled)
  └── tech-debt-tracker.md ← Known technical debt
  ```
- `/docs/others/`: Everything else that needs human further organization.

### Mental Model

| Folder             | Question                        |
| :----------------- | :------------------------------ |
| **Product**        | What are we building?           |
| **Architecture**   | How does it work?               |
| **Data**           | What does the data mean?        |
| **Agents**         | How does the intelligence work? |
| **Conventions**    | How do we build it?             |
| **Quality**        | When is it done?                |
| **Tech Decisions** | Why was this chosen?            |
| **Runbooks**       | How do we operate it?           |
| **Exec Plans**     | What are we doing next?         |

For an AI-native system (Data Agent, Marketing Agent, RPA Agent, etc.), this is usually enough. Anything more granular tends to become documentation entropy. The test is simple:
*A new engineer should be able to find any information within **two clicks** from `docs/`.*

### README rule

Keep a module README in place only when it is the right local entrypoint for that directory.

If a module README contains large durable reference material, detailed architecture, long workflows, or historical context, move that substance under the canonical `/docs` structure, or place it under `/docs/others/` if it requires further human organization. Leave behind a short local README that points to the canonical doc.

---

## Step 1 — Inventory Documentation

1. Glob for repo documentation files, excluding all out-of-scope locations above.
2. Record for each file: **path**, **line count**, **last-modified date** (`git log -1 --format=%ci`), **title** (first `#` heading), **apparent role** (`entrypoint`, `architecture`, `api`, `runbook`, `service guide`, `decision`, `archive`, `unknown`).
3. Present the inventory as a table:

```text
| #   | File | Lines | Last Modified | Role | Title |
| --- | ---- | ----- | ------------- | ---- | ----- |
```

---

## Step 2 — Decide Canonical Homes

For each in-scope doc, decide whether it is already in the right place.

Classify each file as one of:

- `KEEP IN PLACE`
- `MOVE to /docs/...`
- `SPLIT` (keep short local entrypoint, move durable content to `/docs/...`)
- `MERGE into <target>`
- `DELETE (obsolete)`
- `NEEDS UPDATE`

Use these tests:

1. **Is this file an entrypoint or a reference?**
   Entry points stay near the thing they introduce. Reference docs belong under `/docs`.
2. **Does it overlap another doc's ownership?**
   If yes, choose one canonical home and trim or merge the rest.
3. **Would a new contributor know where to look?**
   If the answer depends on tribal knowledge, reorganize.
4. **Is the current location forcing duplication?**
   If local placement causes repeated architecture or workflow content, move the durable content under `/docs`.

---

## Step 3 — Verify Accuracy Against Code

For every file that will survive in some form, verify claims against the live repo:

1. **Paths** — referenced paths exist.
2. **Commands** — commands, flags, tool names, and working directories are correct.
3. **Symbols** — functions, classes, modules, scripts, and config names exist.
4. **Env vars and settings** — names and defaults match source or `.env.example`.
5. **Interfaces and schemas** — endpoints, table names, fields, and contracts match the current code.

Record each issue as: **file**, **line**, **claim**, **actual value**, **fix**.

---

## Step 4 — Find Conflicts and Redundancy

Compare files that cover the same topic. Look for:

1. **Contradictory facts**
2. **Divergent instructions**
3. **Terminology drift**
4. **Subset duplication**
5. **A detailed doc trapped in the wrong location**

For each issue, record: **topic**, **files involved**, **canonical home**, **what stays**, **what moves/removes**, **why**.

---

## Step 5 — Produce the Organization Report

Use this structure:

```text
## Organize Docs Report

### Inventory
| #   | File | Role | Status |
| --- | ---- | ---- | ------ |

### Canonical Homes
| #   | File | Current Home | Canonical Home | Action |
| --- | ---- | ------------ | -------------- | ------ |

### Accuracy Issues
| #   | File | Line | Claim | Actual | Fix |
| --- | ---- | ---- | ----- | ------ | --- |

### Conflicts And Redundancies
| #   | Topic | Files | Canonical Home | Action |
| --- | ----- | ----- | -------------- | ------ |

### Proposed Actions (ordered)
1. MOVE: <file> -> <docs target> — <reason>
2. SPLIT: <README> -> keep local summary, move durable content to <docs target>
3. MERGE: <file-a> + <file-b> -> <target>
4. UPDATE: <file> — <what changes>
5. DELETE: <file> — <reason>
```

Ask: **"Apply all changes? (yes / yes but skip #N,M / no)"**

---

## Step 6 — Apply Changes (on confirmation)

Execute in this order:

1. **Create canonical `/docs` targets first**
2. **Move or split misplaced docs**
3. **Update surviving entrypoint READMEs to point at canonical docs**
4. **Fix factual inaccuracies**
5. **Resolve conflicts and remove redundant content**
6. **Repair internal links and references**
7. **Update `Last updated:` near the top of every touched markdown file**

When splitting a README:

- Keep it short and local.
- Leave setup/discovery content that helps someone in that directory.
- Move durable reference material into `/docs/...`.
- Add a direct pointer to the new canonical doc.

Report:

**"Done. <N> files moved, <M> files split, <P> files updated, <Q> redundant docs removed."**

---

## Guardrails

- **Do not touch runtime skill, prompt, or agent-package files, or their bundled docs.** Treat all such trees as out of scope, even when they use nonstandard names.
- **Prefer `/docs` as the canonical home** unless the file must stay at root or beside a module as a local entrypoint.
- **Do not bloat local READMEs.** If they are no longer acting as entrypoints, split them.
- **Never delete unique rationale silently.** Move it to a better canonical home or archive it.
- **Verify against code, not against other docs.**
- **Always confirm before applying.** Present the full ordered action list first.
- **Update `Last updated:` on every markdown file you touch.**
- **When unsure, flag with `[VERIFY]` instead of guessing.**
