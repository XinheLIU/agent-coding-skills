---
name: analyze
description: Non-destructive cross-artifact consistency and quality audit across spec.md, plan.md, and tasks.md. Use after /tasks and before implementation to catch duplication, ambiguity, terminology drift, coverage gaps, and constitution violations. Read-only — produces a report, never edits files.
---

# /analyze — Cross-artifact consistency audit

Read `spec.md`, `plan.md`, and `tasks.md` for the current feature and report inconsistencies, duplications, ambiguities, coverage gaps, and constitution misalignment. This is an **optional, read-only** step between `/tasks` and implementation in the spec-driven workflow (`/spec` → `/plan` → `/tasks` → `/analyze` → implement).

## When to use

Invoke this skill when the user:

- Just finished `/tasks` and wants a consistency check before implementing.
- Runs `/analyze` or says "audit the spec", "cross-check", "is everything consistent?".
- Manually edited any of `spec.md`, `plan.md`, or `tasks.md` and wants to re-verify.

Do NOT use this skill before `tasks.md` exists. All three artifacts must be present.

## Inputs

- **Required**: `spec.md`, `plan.md`, `tasks.md` for the current feature.
- **Constitution** (optional): `CLAUDE.md` and/or `AGENTS.md` at repo root — same resolution as `/plan`.
- **Context** (optional): `$ARGUMENTS` — e.g., focus areas like `"constitution only"`, `"coverage only"`.

## Outputs

- A Markdown report emitted to the conversation. **No file writes.**
- Optional remediation suggestions (only if the user explicitly approves).

## Operating constraints

- **STRICTLY READ-ONLY.** Never modify, create, or delete files. Never stage, commit, or push.
- **Constitution is non-negotiable.** Any conflict with a MUST principle is automatically CRITICAL and requires editing the spec/plan/tasks — never the constitution itself (that is a separate, explicit action).
- **No hallucinations.** If a section is missing, report it as missing; do not infer its contents.
- **Deterministic IDs.** Finding IDs must be stable across reruns when the inputs are unchanged.

## Prerequisites check

Resolve `FEATURE_DIR` the same way `/plan` and `/tasks` do:

1. `git rev-parse --show-toplevel` → repo root.
2. Try `<repo-root>/specs/<current-branch>/` first.
3. Fall back to scanning `<repo-root>/specs/*/` — if exactly one, use it; if multiple, ask via `AskUserQuestion`.
4. Confirm `spec.md`, `plan.md`, and `tasks.md` all exist. If any is missing, stop and tell the user which upstream skill to run first.

## Workflow

### Step 1 — Load artifacts (progressive disclosure)

Read only the sections you need for analysis — do not dump full artifacts into working memory.

**From `spec.md`:** Overview, Functional Requirements (`FR-###`), Success Criteria (`SC-###`), User Stories (priority + Given/When/Then), Edge Cases, Assumptions, Clarifications.

**From `plan.md`:** Summary, Technical Context, Constitution Check, Architecture & Design subsections (Research notes, Data model, Contracts, Validation), Project Structure, Complexity Tracking.

**From `tasks.md`:** Task IDs (`T###`), descriptions, phase grouping, `[P]` markers, `[USn]` tags, referenced file paths, Coverage gaps note (if any).

**From constitution (`CLAUDE.md` + `AGENTS.md`):** principle names and MUST/SHOULD statements. Ignore generic boilerplate. If no constitution is present, note "N/A — no constitution" in the report and skip pass D.

### Step 2 — Build semantic inventories

Construct lightweight internal indexes (do NOT include raw content in output):

- **Requirements inventory**: one entry per `FR-###`, keyed by the FR ID. Include the verb phrase and the measurable object (if any). Also index `SC-###` — flag each SC as either `buildable` (requires tasks — e.g., "95% line coverage", "P95 latency < 200ms") or `outcome-metric` (post-launch business KPI — e.g., "reduce support tickets by 50%").
- **User story inventory**: one entry per story with its priority (P1/P2/…), acceptance scenarios, and the `[USn]` tag it maps to.
- **Task → anchor map**: for each `T###`, infer which FR(s), SC(s), or user story it fulfills — by explicit ID mention, `[USn]` tag, or keyword/file-path match.
- **Entity set**: entities named in `plan.md` Data model.
- **Contract set**: endpoints / commands / event schemas in `plan.md` Contracts.
- **Project structure paths**: directories declared in `plan.md` Project Structure.
- **Constitution rules**: MUST and SHOULD statements.

### Step 3 — Detection passes

Run the six passes below. Cap total findings at 50; aggregate overflow into a single "N more low-severity findings" summary line.

**A. Duplication** — near-duplicate FRs or SCs (same verb + object, different wording). Recommend consolidation, keeping the clearer phrasing.

**B. Ambiguity** — vague adjectives (`fast`, `scalable`, `secure`, `intuitive`, `robust`, `user-friendly`, `modern`) without measurable criteria. Unresolved placeholders (`TODO`, `TKTK`, `???`, `<...>`, `NEEDS CLARIFICATION`). Requirements with subjective pass/fail.

**C. Underspecification** — requirements with a verb but no object or measurable outcome. User stories missing at least one Given/When/Then. Tasks referencing files under a directory not declared in plan's Project Structure.

**D. Constitution alignment** — any FR, plan decision, or task that conflicts with a constitution MUST statement. Missing constitution-mandated sections or quality gates. **All findings here are CRITICAL.**

**E. Coverage gaps** — (bidirectional)
- FRs with zero mapped tasks.
- `buildable` SCs with zero mapped validating task.
- User stories with zero mapped task.
- Tasks with no mappable anchor (candidate scope creep).
- Entities in `plan.md` Data model with no spec basis (candidate scope creep).
- Contracts in `plan.md` with no FR anchor.

**F. Inconsistency** —
- Terminology drift: the same concept named differently across artifacts (e.g., spec says "reservation", plan says "booking", tasks say "slot").
- Conflicting tech choices (e.g., plan Technical Context says "pytest" but a task references `jest`).
- Task ordering contradictions (e.g., integration tasks before foundational setup with no dependency note).
- Data entities referenced in plan but absent from spec (or vice versa).
- Tech stack references that contradict constitution.

### Step 4 — Severity assignment

| Severity | Triggers |
|---|---|
| **CRITICAL** | Constitution MUST violation; core spec artifact missing; P1 story has zero task coverage; conflicting tech mandates |
| **HIGH** | Duplicate or conflicting requirement; ambiguous security/performance attribute; untestable acceptance criterion; buildable SC with zero coverage |
| **MEDIUM** | Terminology drift; missing non-functional task coverage; underspecified edge case; entity in plan with no spec basis |
| **LOW** | Style/wording improvement; minor redundancy not affecting execution order |

### Step 5 — Produce the report

Emit a Markdown block. No file writes. Use this exact structure:

```markdown
## Specification Analysis Report

**Feature**: <NNN-name> • **Scope**: spec.md + plan.md + tasks.md

### Findings

| ID | Category | Severity | Location | Summary | Recommendation |
|----|----------|----------|----------|---------|----------------|
| D1 | Duplication | HIGH | spec.md FR-012, FR-018 | Two FRs describe the same upload flow with different wording | Merge into FR-012; retire FR-018 |
| ... | | | | | |

Finding IDs use one-letter category prefix:
D=Duplication, A=Ambiguity, U=Underspecification, C=Constitution, G=Coverage gap, I=Inconsistency.

### Coverage Summary

| Anchor | Has task? | Task IDs | Notes |
|--------|-----------|----------|-------|
| FR-001 | ✓ | T014, T022 | |
| FR-007 | ✗ | — | **GAP** — HIGH |
| SC-003 (buildable) | ✗ | — | **GAP** — HIGH |
| SC-005 (outcome-metric) | N/A | — | post-launch KPI |
| US1 | ✓ | T010–T019 | |

### Metrics

- Total FRs: N
- Total SCs: N (buildable: M, outcome-metric: K)
- Total user stories: N
- Total tasks: N
- FR coverage: X/N (Y%)
- Buildable SC coverage: X/M (Y%)
- Ambiguity count: N
- Duplication count: N
- **Critical issues: N**
- High issues: N

### Next actions

- If CRITICAL > 0: **Stop.** Resolve before implementation. Re-run `/spec` or `/plan` to fix upstream, then `/tasks`, then re-run `/analyze`.
- If HIGH > 0: Review and decide per finding. Low-friction ones can be fixed by editing `tasks.md` or `plan.md` directly.
- If only MEDIUM/LOW: Safe to proceed. Consider fixing during Polish phase.
```

### Step 6 — Offer remediation

After the report, ask the user in plain text:

> "Would you like me to draft concrete remediation edits for the top N findings? I will not apply them without your approval."

If the user declines or wants to handle edits manually, stop. If they approve, propose **diff-style suggestions** (not file writes) that the user can review and apply themselves — do NOT invoke `Edit` or `Write` from within this skill.

## Hard rules

- Never modify, create, or delete files from within this skill.
- Never invoke `/spec`, `/plan`, or `/tasks` — suggest them in Next actions if upstream changes are needed.
- Never fabricate FRs, SCs, tasks, or constitution rules that aren't in the artifacts.
- Constitution conflicts are ALWAYS CRITICAL. No exceptions.
- If an artifact cannot be parsed (malformed structure), report it under Underspecification and halt — do not attempt partial analysis that could mislead.

## Key principles

- **High-signal tokens.** Actionable findings beat exhaustive documentation. A 50-row cap is a ceiling, not a target.
- **Progressive disclosure.** Load sections, not whole files.
- **Deterministic output.** Same inputs → same finding IDs and counts.
- **Cite specifics.** Every finding names an artifact + line/section anchor. No "something seems off" without a location.
- **Zero issues is a valid report.** Emit the success header + coverage table + metrics; do not invent problems.
