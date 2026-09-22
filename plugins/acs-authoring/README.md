# acs-authoring

Meta-tooling plugin for ACS maintainers and advanced users. Provides skills for researching engineering questions, visualizing portfolio DAGs, authoring new skills, reviewing agent instructions, and resolving blocked decisions.

**Phase**: authoring  
**Version**: 0.4.0  
**Depends on**: `acs-context ^0.4.0`

---

## Skill Inventory

### acs-research

Resolve an external technical fact blocking an engineering decision, specification, diagnosis, or implementation, with cited primary evidence. Use for bounded engineering questions unavailable in the repository; learning-oriented synthesis and original research belong to the user's research workflow.

**When to use**: A decision or implementation is blocked on an external fact (API behavior, spec detail, library version constraint) that cannot be discovered from the repository.

**Output**: A focused research report under `<effort>/research/` with cited evidence, implications, and unresolved uncertainty, plus a pointer added to `state.md` or the waiting ticket.

---

### acs-draw-portfolio-dag

Render Markdown workstreams and dependency tickets as an interactive HTML DAG or Mermaid flowchart. Use for portfolio sequencing, frontier visibility, cross-cutting ticket tags, or live progress rendering during an implement run.

**When to use**: You need to visualize ticket dependencies from a delivery plan, see the current frontier, or track cross-cutting tags across workstreams.

**Input**: Canonical delivery tickets from `acs-plan-delivery` in one change directory or `docs/changes/`.

**Output**: An interactive HTML DAG or Mermaid flowchart showing workstream structure, dependency edges, and ticket status.

**Scripts**: Uses `shared/scripts/check-visual-report-contract.py` and `shared/scripts/validate-report-html.py` for report validation. Reference templates in `shared/references/` for the HTML output contract.

---

### acs-challenge-approach

Resolve user-owned decisions one at a time. Use when choices that cannot be discovered from the environment block an idea, plan, design, triage brief, or wayfinder ticket.

**When to use**: A blocker is a genuine decision (not a discoverable fact) — an unresolved choice about approach, scope, priority, or design that requires the user's judgment.

**How it works**: Walks prerequisite decisions before downstream choices, asks one question at a time leading with a recommendation and trade-off, and stops when every decision required by the caller's completion criterion is resolved.

**Output**: Confirmed decisions and genuinely open questions returned to the caller, which owns persistence and implementation.

---

### acs-review-agent-instructions

Review or update a repository's `AGENTS.md` or `CLAUDE.md`. Use to encode one incident lesson, repair instruction hierarchy and pointers, prune ineffective guidance, or reconnect shared-context routing.

**When to use**: After an incident, when instructions have drifted, when pointers are broken, or when guidance has become redundant or ineffective. Use `acs-translate-agent-context` for runtime migration (a separate skill).

**Output**: Updated `AGENTS.md` or `CLAUDE.md` with repairs scoped to the requested mode (encode lesson / repair hierarchy / prune / reconnect routing).

---

### acs-writing-great-skills

Author or revise a predictable system skill. Use when defining a skill's invocation boundary, procedure, references, completion criteria, or shared-memory contract.

**When to use**: Creating a new skill, revising an existing skill's invocation trigger, tightening completion criteria, or declaring the six YAML context fields for a skill's shared-memory contract.

**Output**: A `SKILL.md` with correct frontmatter, invocation boundary, structured procedure, and context declaration.

---

## Bundled Scripts

Located in `shared/scripts/`:

- `check-visual-report-contract.py` — validates that a visual report's output conforms to the expected contract structure; used by `acs-draw-portfolio-dag`
- `validate-report-html.py` — validates rendered HTML report output; used by `acs-draw-portfolio-dag`

## Reference Templates

Located in `shared/references/`:

- `tabbed-discovery-report.md` — Markdown template for tabbed discovery reports
- `tabbed-discovery-template.html` — HTML template for tabbed DAG/discovery output
- `visual-report.md` — Markdown contract for visual report structure

---

## Installation

This plugin requires `acs-context ^0.4.0`. Install it first, then add this plugin alongside it in your `.claude/skills/` or equivalent skills directory.

```bash
# From your project root
cp -r plugins/acs-authoring ~/.claude/skills/acs-authoring
```

---

## Usage Notes

- All skills in this plugin require `acs-init-context` to have run and populated shared context before invocation.
- `acs-draw-portfolio-dag` calls its bundled scripts by absolute path — ensure the plugin directory is not moved after installation, or update `SKILL_DIR` resolution accordingly.
- This plugin is intended for ACS maintainers and advanced users. End-user-facing skills live in the phase-specific plugins (`acs-plan`, `acs-implement`, etc.).
- `acs-research` may overlap topically with skills in the `plan/` phase; this copy owns the authoring-phase research workflow. Do not duplicate it.
