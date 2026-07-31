# Agent Coding Skills

Last updated: 2026-07-31

Composable AI agent skills for the software build lifecycle — from architecture design through code delivery. Organized as two capability domains that cover the full engineering workflow.

Extracted from [XinheLIU/agent-skills](https://github.com/XinheLIU/agent-skills). Works with Claude Code, Codex, Cursor, OpenCode, and similar agent environments.

## Domains

### `architecture-design/` — Design and review

| Skill | Purpose |
| --- | --- |
| `design-agent-architecture` | 6-layer agent system architecture (L1–L6): Markdown doc + Mermaid diagram with observability |
| `review-architecture` | TOGAF 4A + Deploy + ADR review; orchestrates explorer/reviewer subagent pairs in parallel |
| `review-code-quality` | Production-readiness review: API, DB, auth, reliability, performance, security; merge verdict |
| `review-design-doc` | Pre-implementation review: catches scope creep, missing failure modes, overcomplexity |
| `review-implementation-gaps` | Compares codebase against a design doc; complete/partial/missing/divergent gap analysis |
| `analyze-test-gaps` | Audits test adequacy from business-critical paths (not line coverage) |

The `code-review/agents/` directory holds 27 shared sub-agent definitions used across the review suite.

### `coding/` — Implementation and setup

**Working on a feature** (`working-on-a-feature/`) — spec → tasks → TDD workflow:
`brainstorm-feature` → `spec` → `tasks` → `tdd` → `analyze`

**Code quality** (`code-quality/`): `refactor-code`, `simplify-code`, `request-code-review`

**Engineering setup** (`engineering-setup/`) — context and documentation tooling:
`review-claude-md`, `review-agent-md`, `extract-rules`, `translate-agent-context`, `organize-docs`, `document-codebase`, `create-readme`, `build-skeleton`

**Technical design** (`tech-design/`): `design-operational-ontology`

**Frontend** (`frontend/`): `frontend-design`, `frontend-design-antigravity`, `ui-ux-pro-max`

**Git slash commands** (`git/commands/`): `/commit`, `/pr-create`, `/git:log`, `/git:status`

## Install

```bash
# Via plugin marketplace (Claude Code)
/plugin marketplace add XinheLIU/agent-coding-skills
/plugin install agent-coding-skills@agent-coding-skills
```

```bash
# Via skills ecosystem
npx skills add XinheLIU/agent-coding-skills
```

```bash
# Manual: copy one skill
cp -R architecture-design/code-review/skills/review-code-quality ~/.claude/skills/
cp -R coding/working-on-a-feature/skills/spec ~/.claude/skills/
```

## Workflow chains

Architecture review:
```
review-architecture → review-design-doc → review-implementation-gaps → analyze-test-gaps
```

Feature delivery (TDD):
```
brainstorm-feature → spec → tasks → tdd → analyze → review-code-quality
```

Context setup (new project):
```
review-claude-md → extract-rules → document-codebase → create-readme
```

See each skill's `SKILL.md` for the full workflow, constraints, and output format.
