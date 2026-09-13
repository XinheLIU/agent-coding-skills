# Improvement Plan: AI-Native SDLC Alignment

Last updated: 2026-09-12

## Executive Summary

Restructure agent-coding-skills to align with Anthropic's AI-Native SDLC while preserving the rigorous memory protocol and coordination model. Move from six domain-organized phases (product, design, engineering, quality, operations, craft) to six lifecycle-aligned phases (plan, design, build, test, deploy, maintain) and incorporate six enhancements from Anthropic's playbook that increase velocity, simplicity, and autonomous capability.

**Key improvements:**
- Distinct skill naming to avoid confusion with reference skills
- Clear UI/UX boundary: functional requirements define WHAT, UX defines HOW
- DDD-style tech design with three-phase progression: prototype validation → engineering hardening → component extraction
- Role evolution: from feature implementer → system designer → platform curator

**Timeline:** 10-12 weeks for core restructuring, enhancements, and new design phase.

**Success criteria:** Users can invoke the suite with Anthropic's six verbs, the memory protocol remains intact, continuous evals run in CI, autonomous maintenance closes the loop, and the design phase delivers genuine engineering design work.

---

## Current State

### Phase Structure (Current)

```
system/skills-src/
├── product/          # Discovery + Definition (10 skills) — MATURE
├── design/           # UX + Technical (11 skills) — PARTIAL (UX mature, tech design placeholders)
├── engineering/      # Feature delivery (5 skills) — PLACEHOLDERS
├── quality/          # Testing + Review + Debugging (11 skills) — PLACEHOLDERS
├── operations/       # Planned, 0 skills
└── craft/            # Context + Meta (10 skills) — MATURE
```

**Strengths:**
- Rigorous memory protocol with lifecycle classification (North Star, Current State, Change Context, Run Context)
- Explicit coordinator for serialization, freshness, conflict resolution
- Addressable HTML records with IDs, authority tracking, promotion criteria
- 47 skills with YAML context contracts (requires, retrieves, produces, updates, invalidates, handoff_to)
- Mature product and UX skills with real implementation depth

**Gaps:**
- Phase names don't match Anthropic's vocabulary (users know "Plan" not "Product")
- No top-level entry points (users navigate 47 skills vs invoking 6 verbs)
- Autonomous maintenance missing (Operations has 0 skills)
- No continuous skill evals in CI
- Plans live in conversation, not committed artifacts
- Policy enforcement in skill logic, not repo-level hooks
- **Naming collision risk**: Current skill names may overlap with reference skills (Matt's skills), causing agent confusion
- **UI/UX boundary blur**: UX skills focus on individual functions/pages, not whole-product inspection; prototype/design handoff unclear
- **Tech design missing**: No DDD-style engineering design phase; no distinction between prototype validation, engineering hardening, and component extraction
- **Most skills are placeholders**: Only product and UX phases have real depth; engineering, quality, operations need building from scratch

---

## Target Architecture

### Phase Structure (Target)

```
system/skills-src/
├── plan/             # Product discovery + definition → durable intent
├── design/           # Three sub-phases with clear boundaries
│   ├── requirements/  # WHAT: functional requirements, acceptance criteria
│   ├── ux/           # HOW (delivery): interaction, visual, one prototype/design doc
│   └── technical/    # HOW (engineering): three-phase DDD progression
│       ├── prototype-validation/    # Problem space: is it worth building?
│       ├── engineering-hardening/   # Solution space: can we maintain it long-term?
│       └── component-extraction/    # Composable space: turn work into reusable assets
├── build/            # Implementation + Frontend/Backend → working code
├── test/             # TDD + Test gaps + Verification → passing tests
├── deploy/           # CI/CD + Release + Infra → production evidence
└── maintain/         # Monitoring + Diagnosis + Autonomous loop → implementation changes
```

Each phase gets:
- One top-level workflow (`/plan`, `/design`, `/build`, `/test`, `/deploy`, `/maintain`)
- Clear entry artifact (what it reads)
- Clear exit artifact (what it commits)
- Approval gate definition (what requires user sign-off)

**Design phase boundaries:**
- Requirements define WHAT capabilities the product provides
- UX defines HOW those capabilities are delivered (interaction + visual, based on prototype + product vision)
- Technical design follows three-phase progression:
  1. Prototype validation (problem space): validate whether something is worth building
  2. Engineering hardening (solution space): turn "can be built" into "can be maintained long-term"
  3. Component extraction (composable space): turn "one-off built work" into reusable assets

### Entry Points (New)

Six user-facing verbs route to the appropriate workflow:

| Verb | Entry Workflow | Reads | Writes | Hands off to |
|------|---------------|-------|--------|--------------|
| `/plan` | `plan/ideas.md` | Problem description, user input | `docs/product/<product>/product.html` (accepted intent records) | `/design` when intent accepted |
| `/design` | `design/full-design.md` | Accepted intent | Requirements (`specs/<spec>.md`), UX design doc, technical design decisions (`DESIGN.md`), prototype decisions | `/build` when all three design layers settled |
| `/build` | `build/feature-delivery.md` | Spec + design decisions | `plan.md` (proposed approach), code changes, `state.md` | `/test` after implementation |
| `/test` | `test/testing.md` | Code changes, existing tests | Passing tests, coverage report | `/deploy` when green |
| `/deploy` | `deploy/release.md` | Passing changes, target environment | Release evidence, deployment record | `/maintain` after shipped |
| `/maintain` | `maintain/autonomous-loop.md` | Monitoring alerts, logs | Implementation change records → re-enters `/build` | Closes the loop |

**Design phase structure:** The `/design` workflow coordinates three sequential sub-phases:
1. **Requirements** — define WHAT capabilities the product provides (functional requirements, acceptance criteria)
2. **UX** — define HOW those capabilities are delivered (interaction + visual design, one unified prototype/design doc inspecting the whole product vision)
3. **Technical** — define HOW to engineer it (DDD-style, three-phase progression: prototype validation → engineering hardening → component extraction)

**Backward compatibility:** Existing skills remain invocable by name (`/brainstorm`, `/write-prd`, `/spec`). The six verbs are routers, not replacements.

---

## Naming Strategy

**Problem:** Current skill names may collide with reference skills (Matt's skills), causing agent confusion when selecting which to invoke.

**Solution:** Use distinct naming that signals this suite's identity while remaining clear:

| Our Skill | Matt's Reference Skill | Distinction Strategy |
|-----------|----------------------|---------------------|
| `define-outcomes` | `write-prd` | Emphasize measurable outcomes over document format |
| `design-experiment` | `prototype` | Emphasize validation/experiment framing |
| `settle-requirements` | `spec` | Emphasize finalization/agreement over initial draft |
| `engineer-domain-model` | `domain-modeling` | Add "engineer" prefix for DDD engineering phase |
| `harden-architecture` | `codebase-design` | Emphasize hardening/maintenance over initial design |
| `extract-components` | (none) | No collision; new concept |
| `validate-prototype` | `prototype` | Different phase; emphasize validation |
| `design-interaction-flow` | `interaction-design` | Emphasize flow/journey over static design |
| `implement-feature` | `tasks` | Emphasize implementation over task breakdown |
| `verify-implementation` | `tdd` | Broader than TDD; includes integration checks |
| `audit-architecture` | `improve-codebase-architecture` | Emphasize assessment/audit over improvement action |
| `challenge-approach` | `grilling` | Emphasize constructive challenge over adversarial grilling |
| `explore-unknowns` | `wayfinders` | Emphasize technical exploration over navigation metaphor |

**Naming principles:**
- Use verbs that signal the phase and role transformation (define, settle, engineer, harden, extract, validate)
- Add context when collision risk is high (engineer-domain-model vs domain-modeling)
- Preserve clarity over cleverness (settle-requirements is clearer than finalize-spec)
- Let the skill description handle disambiguation when names are similar

---

## Three-Phase Technical Design

The technical design phase follows a DDD-style progression that matches role evolution:

### Phase 1: Prototype Validation (Problem Space)

**Goal:** Validate whether something is worth building.

**Role:** Feature implementer exploring feasibility.

**Activities:**
- Spike technical unknowns (can this API do what we need?)
- Build throwaway prototypes to test assumptions
- Identify showstoppers early (performance cliff, missing capability, incompatible license)
- Estimate complexity and risk

**Exit criteria:** Green light to proceed OR pivot to different approach OR kill the feature.

**Artifacts:** Spike code (discarded), validation notes, go/no-go decision.

### Phase 2: Engineering Hardening (Solution Space)

**Goal:** Turn "can be built" into "can be maintained long-term."

**Role:** System designer constraining the solution space.

**The core shift:** Move from simply writing pages to implement features, to defining the entire system. Sort out domain models, state ownership, module boundaries, and interface contracts.

**Activities:**
- Design domain models: entities, value objects, aggregates, bounded contexts
- Define module boundaries and interface contracts
- Choose data structures, algorithms, persistence strategy
- Plan error handling, logging, monitoring, testing strategy
- Establish engineering infrastructure: code standards, testing strategy, CI/CD pipeline, monitoring
- Document architectural decisions (ADRs)

**Exit criteria:** Implementation plan that the team can follow independently, with clear system boundaries and contracts.

**Artifacts:** `DESIGN.md`, ADRs, domain model diagrams, interface specs, test strategy, infrastructure plan.

### Phase 3: Component Extraction (Composable Space)

**Goal:** Turn "one-off built work" into reusable assets.

**Role:** Platform curator building shared capabilities.

**The core shift:** Componentization is not just splitting files. Its core lies in designing component contracts, boundaries, and compatibility strategies, while accounting for themes, accessibility, and version management.

**Activities:**
- Identify reusable patterns across features (require 3+ uses to justify extraction)
- Design component contracts, boundaries, compatibility strategies
- Extract shared UI components with themes, accessibility, version management
- Build design systems with tokens, variants, composition rules
- Establish supporting quality mechanisms: reviews, documentation, versioning, performance checks

**Exit criteria:** Reusable components with clear contracts, documentation, examples, and evidence of 3+ use cases.

**Artifacts:** Component library, design system, usage docs, storybook/catalog.

**Sequencing:** Prototype validation happens per feature. Engineering hardening happens when patterns stabilize (2-3 features). Component extraction happens when duplication is visible (3-5 uses). Follow this sequence to avoid over-abstraction.

**Trade-offs:** Earlier extraction = more rework when requirements change; later extraction = more duplication to maintain. Aim for the Goldilocks zone: extract when the pattern is proven but before duplication becomes painful.

---

## Migration Plan

### Phase 1: Restructure Directory Layout (Week 1-2)

**Goal:** Move existing skills into the six lifecycle phases without breaking references.

**Note:** Parallel orchestration (subagents, fan-out patterns) is deferred. Current plan focuses on serial workflows with explicit coordination.

#### 1.1 Skill Mapping

Map current skills to target phases:

```yaml
plan/:
  - brainstorm              # product/discovery/ → KEEP (mature)
  - validate-demand         # product/discovery/ → KEEP (mature)
  - map-current-product     # product/discovery/ → KEEP (mature)
  - run-premortem           # product/discovery/ → KEEP (mature)
  - ideate-product          # product/discovery/ → KEEP (mature)
  - shape-solution          # product/definition/ → KEEP (mature)
  - define-outcomes         # product/definition/ → KEEP (mature, renamed from older version)
  - design-experiment       # product/definition/ → KEEP (mature, renamed from older version)
  - write-prd               # product/definition/ → KEEP (mature)

design/:
  requirements/:
    - settle-requirements      # NEW (was spec, but renamed to avoid collision with build/spec)
    
  ux/:
    - design-context           # design/ux/ → KEEP (mature)
    - design-interaction-flow  # design/ux/ → RENAME from interaction-design
    - visual-design-variants   # design/ux/ → KEEP (mature)
    - design-implement         # design/ux/ → KEEP (mature)
    - validate-prototype       # design/ux/ → RENAME from prototype (emphasize validation)
    - design-system-create     # design/ux/ → KEEP (mature)
    
  technical/:
    # Core SDLC technical design skills (general-purpose, part of the main loop)
    - explore-unknowns               # RENAME from wayfinders (technical exploration, spike unknowns)
    - engineer-domain-model          # RENAME from domain-modeling (entities, aggregates, bounded contexts)
    - design-module-boundaries       # NEW (define interfaces, contracts, state ownership)
    - harden-architecture            # RENAME from codebase-design (standards, testing, CI/CD, monitoring)
    - design-component-contracts     # NEW (reusable components, boundaries, compatibility)
    - audit-architecture             # RENAME from improve-codebase-architecture (assessment before refactoring)
    - challenge-approach             # RENAME from grilling (adversarial review of design decisions)
    
    # Agent-specific skills (outside the SDLC loop, only for agent/LLM projects)
    - design-agent-architecture      # Agent-specific: LLM orchestration, tool calling, memory
    - design-operational-ontology    # Agent-specific: knowledge representation, reasoning
    
    # Three-phase progression (prototype → engineer → extract) is guidance embedded in skills above

build/:
  - orchestrate-tickets      # NEW (figures out DAG between tickets, orchestrates through herdr)
  - analyze                  # engineering/feature/ → KEEP but enhance
  - brainstorm-approaches    # engineering/feature/ → RENAME from brainstorm-feature
  - plan-implementation      # engineering/feature/ → RENAME from spec (writes plan.md)
  - break-into-tasks         # engineering/feature/ → RENAME from tasks
  - implement-feature        # NEW (the actual implementation loop with TDD)
  - tdd                      # quality/testing/ → MOVE HERE (test-driven development is part of build)
  - handoff                  # engineering/feature/ → KEEP

test/:
  - analyze-test-gaps        # quality/testing/ → KEEP (audit coverage, add missing tests)
  - verify-coverage          # NEW (check coverage meets threshold)

deploy/:
  - deploy-staging           # NEW
  - deploy-production        # NEW
  - rollback                 # NEW

maintain/:
  - monitor-alert                  # NEW (ingest alerts, diagnose)
  - record-implementation-change   # NEW (write verifiable product function/implementation changes)
  - autonomous-coordinator         # NEW (decide whether to auto-fix or escalate)
  - diagnose-incident              # quality/debugging/ → MOVE HERE (was diagnosing-bugs)
```

**Key changes:**
- Design phase now has three sequential sub-phases with clear boundaries
- Technical design has 7 general-purpose SDLC skills (part of main loop) + 2 agent-specific skills (outside loop)
- Build phase skills renamed to avoid collisions (plan-implementation vs spec), added orchestrate-tickets
- Test phase simplified to coverage audit (TDD moved to build phase)
- Deploy and maintain phases populated with core skills

**Review and debugging skills:** These apply across lifecycle, not just one phase. Options:

1. **Keep cross-cutting:** Move to `craft/` and reference from workflows
2. **Duplicate routing:** Symlink into each phase where they're used
3. **Phase-specific specialization:** `build/review-code-quality` vs `design/review-design-doc`

**Recommendation:** Option 3. Review and debugging are context-specific; a review pass during build checks different things than a review during design.

#### 1.2 Directory Operations

```bash
# Backup current structure
cp -r system/skills-src system/skills-src.backup

# Create new phase directories
mkdir -p system/skills-src/{plan,design,build,test,deploy,maintain}

# Move skills (example for plan/)
mv system/skills-src/product/discovery/* system/skills-src/plan/
mv system/skills-src/product/definition/* system/skills-src/plan/

# Update symlinks in system/skills/
# (Symlink targets change but names stay the same for backward compat)
cd system/skills
for skill in brainstorm validate-demand ...; do
  ln -sf ../skills-src/plan/$skill $skill
done

# Update catalog/skill-set.json categories
```

**Verification:**
- All 47 skills resolve through symlinks
- `catalog/skill-set.json` validates
- Cross-references in SKILL.md files resolve (may need path updates)

#### 1.3 Update Cross-References

Audit all `references/` paths in SKILL.md files:

```bash
# Find all relative references to moved files
grep -r '(\.\./\.\./\.\./craft' system/skills-src/
grep -r '\[.*\](references/' system/skills-src/ | grep -v 'references/[^/]*\.md'
```

Update patterns:
- `../../../craft/context/manage-context/references/PROTOCOL.md` → stays the same (PROTOCOL.md ships with every skill)
- `../../../../workflows/context-coordination.md` → update based on new depth
- Cross-skill references by name (e.g., `/write-prd`, `/prototype`) → no change needed

### Phase 2: Create Six Top-Level Workflows (Week 3-4)

**Goal:** Add routing workflows that map Anthropic's six verbs to your skill sequences.

#### 2.1 Workflow Structure Template

Each workflow follows this shape:

```markdown
---
name: <phase>
description: <one-line purpose>
entry_artifact: <what it reads>
exit_artifact: <what it commits>
approval_gate: <what requires user sign-off>
---

# <Phase> Workflow

## Purpose

<What this phase achieves in the SDLC>

## Entry Criteria

- [ ] <Artifact exists>
- [ ] <Prerequisite met>

## Routing Decision

<How to pick which skill to invoke>

## Skill Sequence

<Typical flow through skills in this phase>

## Exit Criteria

- [ ] <Exit artifact committed>
- [ ] <Quality gate passed>

## Handoff

<What the next phase receives>
```

#### 2.2 Implement Each Workflow

**`system/workflows/plan.md`**

```yaml
entry_artifact: User problem description, opportunity, or alert
exit_artifact: docs/product/<product>/product.html (accepted intent records)
approval_gate: User must accept demand verdict and scope before handoff

routing:
  - If problem is clear → shape-solution
  - If problem is uncertain → brainstorm → validate-demand
  - If existing product needs mapping → map-current-product
  - If risk assessment needed → run-premortem
  - Consolidate into write-prd when intent is accepted

skills_used:
  - brainstorm, validate-demand, map-current-product, run-premortem
  - ideate-product, shape-solution, define-outcomes, design-experiment
  - write-prd (final consolidation)

handoff_to: /design when product.html has accepted intent
```

**`system/workflows/design.md`**

```yaml
entry_artifact: docs/product/<product>/product.html (accepted intent)
exit_artifact: specs/<spec>.md (requirements + acceptance criteria), docs/design/ux-design.html (unified UX design doc), DESIGN.md (technical decisions + ADRs)
approval_gate: User must approve all three layers (requirements, UX, technical) before handoff

structure: Three sequential sub-phases with clear boundaries

phase_1_requirements:
  goal: Define WHAT capabilities the product provides
  skills:
    - settle-requirements (defines functional requirements, acceptance criteria)
    - define-acceptance (extracts testable acceptance criteria)
    - map-user-journeys (cross-functional requirements)
  exit_criteria: specs/<spec>.md with complete functional requirements
  
phase_2_ux:
  goal: Define HOW those capabilities are delivered (interaction + visual)
  prerequisite: Phase 1 complete
  skills:
    - design-context (inspect whole product vision and status)
    - validate-prototype (problem space validation)
    - design-interaction-flow (user journey, state transitions)
    - visual-design-variants (visual layer, one unified design)
    - design-system-create (reusable patterns)
    - design-implement (final prototype/design doc)
  exit_criteria: docs/design/ux-design.html with unified design inspecting whole product
  note: UX skills now inspect the whole product and produce ONE design doc, not individual page designs
  
phase_3_technical:
  goal: Define HOW to engineer it (DDD-style engineering design)
  prerequisite: Phase 2 complete
  
  skills:
    - engineer-domain-model (DDD entities, value objects, aggregates, bounded contexts)
    - harden-architecture (module boundaries, seams, deep modules, maintainability)
    - design-agent-architecture (agent-specific design)
    - design-operational-ontology (agent-specific)
    - improve-codebase-architecture (refactoring guidance)
  
  exit_criteria: DESIGN.md with ADRs, domain model, module boundaries, interface specs
  
  note: |
    The three-phase progression (prototype validation → engineering hardening → component extraction)
    is guidance embedded in the skills, not separate sub-phases with separate skills.
    
    - Prototype validation: Skills guide spiking unknowns before committing to full design
    - Engineering hardening: engineer-domain-model and harden-architecture produce maintainable systems
    - Component extraction: improve-codebase-architecture identifies reuse opportunities after 2-3 features
    
    This is NOT just writing pages to implement features—it's defining the entire system:
    domain models, state ownership, module boundaries, interface contracts.

handoff_to: /build when all three design layers are complete and approved
```

**`system/workflows/build.md`**

```yaml
entry_artifact: specs/<spec>.md (requirements + acceptance criteria), DESIGN.md (technical decisions)
exit_artifact: plan.md (proposed implementation), code changes with passing tests, state.md (resume point)
approval_gate: User must approve plan.md before implementation; user approves risky changes during implementation

role: System implementer following the engineering design

routing:
  - orchestrate-tickets → figure out DAG between tickets, coordinate execution (uses herdr for now)
  - analyze → understand codebase context
  - brainstorm-approaches → generate implementation approaches (optional)
  - plan-implementation → generate plan.md (read-only pass over codebase, renamed from spec)
  - **USER APPROVES plan.md**
  - break-into-tasks → break into incremental steps (renamed from tasks)
  - implement-feature → execute implementation with TDD loop (write test, make it pass, refactor)
  - tdd → test-driven development (moved from test phase, integrated into build loop)
  - handoff → write state.md for resume

skills_used:
  - orchestrate-tickets (DAG coordination), analyze, brainstorm-approaches, plan-implementation
  - break-into-tasks, implement-feature, tdd, handoff

handoff_to: /test when implementation is complete and unit tests pass

note: TDD happens during implementation, not as a separate phase. The orchestrator coordinates multi-ticket work.
```

**`system/workflows/test.md`**

```yaml
entry_artifact: Code changes with passing unit tests (from build phase)
exit_artifact: Full test suite passing, coverage report
approval_gate: Tests must meet coverage threshold before handoff

routing:
  - analyze-test-gaps → audit coverage, identify missing tests
  - verify-coverage → check coverage meets threshold (e.g., 80%)
  - Add integration/e2e tests if gaps found
  - Run full suite, verify green

skills_used:
  - analyze-test-gaps, verify-coverage

handoff_to: /deploy when all tests pass and coverage threshold met

note: TDD happens in build phase, not here. Test phase is for coverage audit and integration tests.
```

**`system/workflows/deploy.md`**

```yaml
entry_artifact: Passing changes on branch, target environment config
exit_artifact: Release evidence (deploy log, version tag, rollback plan), updated docs/operations/releases.md
approval_gate: User must approve production deploy; staging deploys may be auto-approved via hooks

routing:
  - Verify environment constraints (docs/operations/environments.md)
  - Check release gate (all tests green, required approvals, no blocking issues)
  - Execute deployment steps (CI/CD pipeline, manual steps via wizard if needed)
  - Record release evidence
  - Update release index

skills_used:
  - (to be implemented) ci-cd-gate, deploy-staging, deploy-production, rollback, wizard

handoff_to: /maintain after successful deploy
```

**`system/workflows/maintain.md`**

```yaml
entry_artifact: Monitoring alerts, scheduled scans, on-call incidents
exit_artifact: Implementation change records in docs/product/<product>/product.html OR immediate fix + regression test
approval_gate: Autonomous for low-risk fixes within control band; escalate to user for breaking changes or data loss risk

routing:
  - monitor-alert → ingest alert, extract symptoms
  - diagnosing-bugs → build hypothesis, test, diagnose root cause
  - Decision point:
    - Within control band (config tweak, known pattern, rollback, non-breaking bug fix) → record-implementation-change → /build → /test → /deploy
    - Outside control band (behavior change requiring design, data migration, breaking API change) → record-implementation-change with open questions → escalate to user
  - Record diagnosis and resolution in docs/operations/incidents.md

skills_used:
  - monitor-alert, diagnosing-bugs, triage, record-implementation-change, autonomous-coordinator

closes_the_loop: Yes — verifiable implementation changes re-enter /build without human initiation for allowed patterns
```

#### 2.3 Update Workflow Index

Update `system/workflows/README.md`:

```markdown
# Workflows

Workflows compose skills around the [shared memory protocol](../skills-src/craft/context/init-context/references/PROTOCOL.md). 

## Six Lifecycle Phases

Use these six verbs to invoke the full lifecycle:

- [Plan](plan.md) — turn uncertain concepts into accepted intent
- [Design](design.md) — settle requirements, UX, and technical structure
- [Build](build.md) — implement features with plan approval and verification
- [Test](test.md) — TDD, coverage audit, regression tests
- [Deploy](deploy.md) — release to staging/production with evidence
- [Maintain](maintain.md) — autonomous monitoring, diagnosis, and loop closure

## Legacy Workflows (Retained)

- [Ideas](ideas.md) — detailed product discovery sequence (now invoked by /plan)
- [Feature delivery](feature-delivery.md) — detailed build sequence (now invoked by /build)
- [Testing](testing.md) — detailed test sequence (now invoked by /test)
- [Debugging](debugging.md) — detailed diagnosis sequence (now invoked by /maintain)

Shared [context coordination](context-coordination.md) owns resolution, runtime binding, scheduling, claims, shared writes, freshness, and retention.
```

### Phase 3: Implement Six Enhancements (Week 5-10)

#### Enhancement 1: Autonomous Loop Closure (Week 5-6)

**Goal:** `/maintain` can ingest monitoring alerts, diagnose, write verifiable product function/implementation changes, and re-enter `/build` or `/deploy` without human initiation.

**Components:**

1. **New skill: `maintain/monitor-alert`**
   - Reads alert payload (JSON, structured log, webhook)
   - Extracts symptoms (service down, latency spike, error rate threshold)
   - Routes to `diagnosing-bugs` for diagnosis

2. **New skill: `maintain/record-implementation-change`**
   - Takes diagnosis result (root cause, evidence, proposed fix)
   - Writes verifiable change record in `docs/product/<product>/product.html`:
     - Current behavior (what broke, observed symptoms)
     - Intended behavior (what should happen, acceptance criteria)
     - Implementation scope (config change, hotfix, rollback)
   - Classifies as P0/P1/P2 based on severity
   - Does NOT re-enter discovery—records concrete function/implementation changes only

3. **New skill: `maintain/autonomous-coordinator`**
   - Decision logic: within control band (auto-fix) vs outside (escalate)
   - Control band: config rollback, known hotfix pattern, scaling adjustment, non-breaking bug fix
   - Outside: schema change, behavior change requiring design, data loss risk, breaking API change
   - Logs decision and rationale

**Integration points:**
- Monitoring tools send webhooks to a local endpoint (or agent polls logs)
- Alert ingestion writes to `docs/operations/alerts/<alert-id>.json`
- Coordinator updates `docs/operations/incidents.md` with resolution
- Within control band: writes change record → `/build` → `/test` → `/deploy`
- Outside control band: writes change record with open questions → escalates to user

**Approval policy:**
- Autonomous fixes require user to configure allowed patterns in `.claude/settings.json` under `maintenance.autonomy_rules`
- First 5 autonomous fixes in a project are logged and require retroactive approval (user reviews `incidents.md`)

**Success criteria:**
- Alert → diagnosis → implementation change record → `/build` → `/test` → `/deploy` completes without human in the loop for an allowed pattern
- Unallowed patterns escalate to user with diagnosis summary and change record with open questions
- Change records are verifiable (current behavior, intended behavior, acceptance criteria)

#### Enhancement 2: Continuous Skill Evals (Week 7-8)

**Goal:** CI runs evals on skill triggering accuracy and output quality, tracking drift over time.

**Components:**

1. **Eval fixture format**

```
system/evals/skills/<skill-name>/
├── fixtures/
│   ├── 001-trigger-match/
│   │   ├── input.md          # User request
│   │   ├── context/           # Repo state (files, git status)
│   │   ├── expected.json      # { "should_trigger": true, "confidence": "high" }
│   │   └── notes.md           # Why this should trigger
│   ├── 002-output-quality/
│   │   ├── input.md
│   │   ├── context/
│   │   ├── expected-output.md # What the skill should produce
│   │   └── rubric.json        # Scoring criteria
│   └── 003-no-trigger/
│       ├── input.md
│       ├── expected.json      # { "should_trigger": false }
│       └── notes.md
└── eval-config.yaml           # Thresholds, model, comparison mode
```

2. **Eval runner script: `scripts/eval-skills.py`**

```python
"""
Run skill evals: triggering accuracy and output quality.

Usage:
  python scripts/eval-skills.py --skill write-prd --fixture 002-output-quality
  python scripts/eval-skills.py --all                    # Run all fixtures
  python scripts/eval-skills.py --ci                     # CI mode: fail on threshold
"""

import json
import subprocess
from pathlib import Path

def eval_trigger_match(skill_name, fixture_dir):
    """Check if skill triggers on input.md"""
    input_text = (fixture_dir / "input.md").read_text()
    expected = json.loads((fixture_dir / "expected.json").read_text())
    
    # Invoke Claude Code with input, check if skill was invoked
    result = subprocess.run(
        ["claude", "--eval-mode", "--input", str(fixture_dir / "input.md")],
        capture_output=True, text=True
    )
    
    triggered = skill_name in result.stdout
    confidence = "high" if triggered == expected["should_trigger"] else "low"
    
    return {
        "passed": triggered == expected["should_trigger"],
        "expected": expected["should_trigger"],
        "actual": triggered,
        "confidence": confidence
    }

def eval_output_quality(skill_name, fixture_dir):
    """Compare skill output to expected output"""
    input_text = (fixture_dir / "input.md").read_text()
    expected_output = (fixture_dir / "expected-output.md").read_text()
    rubric = json.loads((fixture_dir / "rubric.json").read_text())
    
    # Run skill, capture output
    result = subprocess.run(
        ["claude", "--eval-mode", f"/invoke-skill {skill_name}", 
         "--input", str(fixture_dir / "input.md")],
        capture_output=True, text=True, cwd=fixture_dir / "context"
    )
    
    actual_output = result.stdout
    
    # Use LLM-as-judge to score against rubric
    score = llm_judge(expected_output, actual_output, rubric)
    
    return {
        "passed": score >= rubric.get("pass_threshold", 0.8),
        "score": score,
        "rubric": rubric,
        "diff_summary": diff_summary(expected_output, actual_output)
    }

def llm_judge(expected, actual, rubric):
    """Score actual output against expected using rubric"""
    # Call Claude API with judge prompt
    # Return score 0.0-1.0
    pass

def run_all_evals():
    """Run all fixtures for all skills"""
    results = []
    for skill_dir in Path("system/evals/skills").iterdir():
        if not skill_dir.is_dir():
            continue
        skill_name = skill_dir.name
        for fixture_dir in (skill_dir / "fixtures").iterdir():
            if "trigger" in fixture_dir.name:
                result = eval_trigger_match(skill_name, fixture_dir)
            elif "output" in fixture_dir.name:
                result = eval_output_quality(skill_name, fixture_dir)
            results.append({
                "skill": skill_name,
                "fixture": fixture_dir.name,
                **result
            })
    
    return results

if __name__ == "__main__":
    results = run_all_evals()
    
    # Write results to system/evals/results/<timestamp>.json
    # Track drift: compare to baseline
    # CI mode: exit 1 if pass rate < threshold
```

3. **CI integration: `.github/workflows/eval-skills.yml`**

```yaml
name: Skill Evals

on:
  pull_request:
    paths:
      - 'system/skills-src/**'
      - 'system/evals/**'
  schedule:
    - cron: '0 2 * * *'  # Daily at 2am

jobs:
  eval:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          pip install anthropic rich
      
      - name: Run skill evals
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          python scripts/eval-skills.py --ci
      
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: eval-results
          path: system/evals/results/
      
      - name: Comment on PR
        if: github.event_name == 'pull_request' && failure()
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '❌ Skill evals failed. Check artifacts for details.'
            })
```

**Success criteria:**
- 10+ fixtures per critical skill (write-prd, spec, tdd, diagnosing-bugs)
- CI runs on every PR touching skills
- Baseline established; drift detection alerts when pass rate drops >10%

#### Enhancement 3: Plan.md as Reviewable Artifact (Week 9)

**Goal:** Materialize implementation plans as committed `plan.md` so humans and future sessions can review "did we build what we planned."

**Changes to `build/spec` skill:**

Current behavior:
1. Read spec
2. Analyze codebase
3. Propose approach in conversation
4. Wait for approval
5. Implement

New behavior:
1. Read spec
2. Analyze codebase
3. **Write `docs/changes/<change-id>/plan.md`** with:
   - Problem statement (from spec)
   - Proposed approach (architecture, seams, files to modify)
   - Implementation steps (ordered)
   - Verification plan (tests, manual checks)
   - Risks and alternatives considered
4. **Commit `plan.md` to branch**
5. Wait for approval (user reviews `plan.md` in PR or diff)
6. Implement according to plan
7. After implementation, compare actual changes to plan (did we deviate? why?)

**Plan.md template:**

```markdown
# Implementation Plan: <change-id>

**Spec:** [<spec-title>](../../specs/<spec>.md)  
**Branch:** `<branch-name>`  
**Created:** <timestamp>  
**Status:** proposed | approved | implemented | deviated

## Problem Statement

<Copy from spec: what are we solving?>

## Proposed Approach

<High-level architecture: which modules, which seams, which patterns>

## Implementation Steps

1. <Step 1: file, change description>
2. <Step 2: file, change description>
3. ...

## Verification Plan

- [ ] Unit tests: <what to test>
- [ ] Integration tests: <what to test>
- [ ] Manual checks: <what to verify>

## Risks and Alternatives

**Risks:**
- <Risk 1 and mitigation>

**Alternatives considered:**
- <Alternative approach and why not chosen>

## Actual Implementation Notes

<Updated during implementation: deviations, discoveries, rationale>
```

**Integration with code review:**

In `quality/review-code-quality` (or new `build/review-plan`):
- Read `plan.md`
- Compare to actual diff
- Flag deviations (new files not in plan, skipped steps, different approach)
- Ask: was the deviation necessary? Should the plan be updated?

**Success criteria:**
- Every feature branch has `docs/changes/<change-id>/plan.md` committed before implementation
- Code review includes plan conformance check
- Deviations are explicitly noted and justified

#### Enhancement 4: Hooks for Policy Enforcement (Week 10)

**Goal:** Repo-level hooks enforce policies (never modify `product.html` directly, specs require linked tickets) across all sessions and skills.

**Hook types:**

1. **Pre-write hooks** (before file is written)
2. **Post-write hooks** (after file is written, before returning to user)
3. **Pre-commit hooks** (before git commit, can block)

**Example hooks:**

```yaml
# .claude/hooks/pre-write.yaml

- name: protect-product-html
  pattern: "**/product.html"
  action: block
  message: |
    product.html is canonical memory. Use /write-prd to update it.
    Direct edits bypass promotion criteria and break record IDs.
  allow_skills:
    - write-prd
    - init-context  # Can create initial structure

- name: specs-require-tickets
  pattern: "docs/specs/*.md"
  action: warn
  check: |
    grep -q "Ticket:" "$FILE" || exit 1
  message: |
    Spec files must link to a canonical ticket.
    Add a line: **Ticket:** [#123](link-to-ticket)

- name: no-secrets-in-memory
  pattern: "docs/agents/memory.md"
  action: block
  check: |
    grep -E '(password|api[_-]?key|secret|token)' "$FILE" && exit 1
  message: |
    Secrets detected in memory.md. Use environment variables or .env files.

- name: design-decisions-require-rationale
  pattern: "DESIGN.md"
  action: warn
  check: |
    # Check that each decision has a "Why:" section
    awk '/^## /{decision=1} decision && /Why:/{found=1} END{exit !found}' "$FILE"
  message: |
    Design decisions need rationale. Add a "Why:" section to each decision.
```

**Hook implementation:**

Add to harness (requires Claude Code support) or implement as pre-commit hook:

```bash
# .git/hooks/pre-commit (generated by /agent-coding-skills:setup)

#!/bin/bash
set -e

# Load hooks from .claude/hooks/pre-commit.yaml
# For each changed file, check if it matches a hook pattern
# Run hook check script
# Block commit if hook fails with action: block

echo "Running agent-coding-skills policy checks..."

python scripts/run-hooks.py --stage pre-commit --changed-files "$(git diff --cached --name-only)"

echo "✓ All policy checks passed"
```

**Success criteria:**
- Direct edits to `product.html` are blocked (unless from write-prd)
- Specs without ticket links generate warnings
- Hooks run in CI (same checks as local pre-commit)
- Users can configure custom hooks in `.claude/hooks/`

#### Enhancement 5: Simpler Entry Points (Week 9, Part 1)

**Goal:** Users invoke six verbs (`/plan`, `/design`, `/build`, `/test`, `/deploy`, `/maintain`) instead of navigating 47 skills.

**Implementation:**

1. **Register six skills as thin routing wrappers:**

```markdown
---
name: plan
description: Turn ideas, opportunities, or alerts into accepted product intent. Use when starting discovery, scoping a feature, or recording validated demand.
---

# Plan

Routes to the appropriate discovery or definition skill based on context.

## Routing Logic

1. Check if `docs/agents/memory.md` exists
   - No → run `/init-context` first
   
2. Check if problem is clear
   - Unclear → `/brainstorm` → `/validate-demand`
   - Clear but risky → `/run-premortem`
   - Clear and validated → `/shape-solution`
   
3. Check if scope is settled
   - No → `/define-outcomes` or `/design-experiment`
   - Yes → `/write-prd`

## Entry Point

Invoke this with:
- `/plan` (routes automatically)
- `/plan --problem "description"` (starts with problem description)
- `/plan --from-alert <alert-id>` (maintenance loop entry)

## Exit

Hands off to `/design` when `product.html` has accepted intent records.
```

Repeat for `/design`, `/build`, `/test`, `/deploy`, `/maintain`.

2. **Add routing intelligence to each wrapper:**

The wrapper skill:
- Reads `state.md` to understand current context
- Reads `product.html`, `specs/`, `DESIGN.md` to know what's settled
- Reads git status to know what's changed
- Invokes the appropriate sub-skill
- Updates `state.md` with next action

3. **Update catalog to feature the six verbs prominently:**

```json
{
  "categories": [
    {
      "id": "lifecycle",
      "label": "SDLC Lifecycle",
      "description": "Six entry points for the full software development lifecycle",
      "skills": ["plan", "design", "build", "test", "deploy", "maintain"]
    },
    {
      "id": "plan",
      "label": "Plan (detailed)",
      "skills": ["brainstorm", "validate-demand", "shape-solution", ...]
    },
    ...
  ]
}
```

**Success criteria:**
- A new user can start with `/plan` and reach `/deploy` without knowing any sub-skill names
- The six verbs appear first in catalog
- README.md and docs show the six verbs in "Quick Start"

#### Enhancement 6: Single-Product Defaults (Week 9, Part 2)

**Goal:** Simplify routing for repos with one product (the common case).

**Current behavior:**
- Skills ask `--product <slug>` or read from `state.md`
- Multi-product repos need explicit routing

**New behavior:**
- If only one `docs/product/*/product.html` exists, default to it
- If multiple exist, require explicit `--product` or error with list
- If none exist, `/init-context` creates the first one

**Implementation:**

Update `workflows/context-coordination.md`:

```markdown
## Product Resolution

1. Check `state.md` for explicit `product: <slug>`
   - Present → use it
   
2. Check `--product` flag
   - Present → use it
   
3. Scan `docs/product/` for existing products
   - Zero products → error "No product found. Run /init-context first."
   - One product → default to it (log: "Defaulting to product: <slug>")
   - Multiple products → error "Multiple products found: [list]. Specify --product <slug>."

4. For new projects, `/init-context` asks:
   - "Product name?" (converts to slug)
   - "One product or multiple?" (single → default mode, multiple → always require --product)
```

**Success criteria:**
- Single-product repos never require `--product` flag
- Multi-product repos error helpfully and list available products
- `/init-context` sets up default mode correctly

---

## Implementation Roadmap

### Phase 1: Restructure Directory Layout (Week 1-2)

- [ ] Map current 47 skills to 6 phases with new naming
- [ ] Create new directory structure with three design sub-phases
- [ ] Move existing mature skills (product, UX, context, craft)
- [ ] Rename skills to avoid collisions (see naming strategy)
- [ ] Update symlinks in `system/skills/`
- [ ] Update `catalog/skill-set.json` with new categories and names
- [ ] Audit all cross-references in SKILL.md files
- [ ] Verify all skills resolve and no broken links
- [ ] Test that renamed skills still trigger correctly

### Phase 2: Write New Design Phase Skills (Week 3-5)

**Requirements sub-phase (Week 3):**
- [ ] Write `design/requirements/settle-requirements` skill
- [ ] Write `design/requirements/define-acceptance` skill
- [ ] Write `design/requirements/map-user-journeys` skill
- [ ] Test requirements workflow on sample feature

**UX sub-phase (Week 4):**
- [ ] Update `design/ux/design-context` to inspect whole product
- [ ] Rename and enhance `design/ux/design-interaction-flow`
- [ ] Update `design/ux/validate-prototype` to emphasize validation
- [ ] Enhance `design/ux/design-implement` to produce unified design doc
- [ ] Test UX workflow produces one design doc, not per-page designs

**Technical sub-phase (Week 5):**
- [ ] Rename `design/technical/engineer-domain-model` (was domain-modeling)
- [ ] Rename `design/technical/harden-architecture` (was codebase-design)
- [ ] Update `design/technical/design-agent-architecture` with three-phase guidance
- [ ] Update `design/technical/design-operational-ontology` with three-phase guidance
- [ ] Update `design/technical/improve-codebase-architecture` with component extraction guidance
- [ ] Document three-phase progression as embedded guidance, not separate skills
- [ ] Test technical design workflow

### Phase 3: Write Top-Level Workflows (Week 6-7)

- [ ] Write `system/workflows/plan.md` (keep current, mostly mature)
- [ ] Write `system/workflows/design.md` (three sequential sub-phases)
- [ ] Write `system/workflows/build.md` (updated with renamed skills)
- [ ] Write `system/workflows/test.md` (enhanced with integration tests)
- [ ] Write `system/workflows/deploy.md` (fully specified with 5 new skills)
- [ ] Write `system/workflows/maintain.md` (autonomous loop)
- [ ] Update `system/workflows/README.md` with role evolution narrative
- [ ] Test each workflow end-to-end on a sample repo

### Phase 4: Write Build Phase Skills (Week 8)

- [ ] Write `build/orchestrate-tickets` (figures out DAG between tickets, orchestrates through herdr)
- [ ] Rename `build/brainstorm-approaches` (was brainstorm-feature)
- [ ] Rename `build/plan-implementation` (was spec, writes plan.md)
- [ ] Rename `build/break-into-tasks` (was tasks)
- [ ] Write `build/implement-feature` (actual implementation loop with TDD)
- [ ] Move `build/tdd` from quality/testing (test-driven development during build)
- [ ] Update `build/analyze` to work with DESIGN.md
- [ ] Update `build/handoff` to reference plan conformance
- [ ] Test build workflow with orchestrator coordinating multi-ticket work

### Phase 5: Write Test Phase Skills (Week 9)

- [ ] Enhance `test/analyze-test-gaps` with coverage verification
- [ ] Write `test/verify-coverage` (check coverage meets threshold)
- [ ] Test full test workflow (coverage audit after build's TDD)

### Phase 6: Write Deploy Phase Skills (Week 10)

- [ ] Write `deploy/deploy-staging`
- [ ] Write `deploy/deploy-production`
- [ ] Write `deploy/rollback`
- [ ] Test deploy workflow with staging → production progression

### Phase 7: Autonomous Maintenance (Week 11-12)

- [ ] Write `maintain/monitor-alert` skill
- [ ] Write `maintain/record-implementation-change` skill (writes verifiable product function/implementation changes)
- [ ] Write `maintain/autonomous-coordinator` skill
- [ ] Move `maintain/diagnose-incident` from quality/debugging
- [ ] Add control-band rules to `.claude/settings.json` schema
- [ ] Test alert → diagnosis → implementation change record → build loop
- [ ] Document autonomy policies and change record format

### Phase 8: Continuous Evals (Week 13-14)

- [ ] Design fixture format
- [ ] Write `scripts/eval-skills.py`
- [ ] Create 10 fixtures for `define-outcomes` (renamed from write-prd)
- [ ] Create 10 fixtures for `plan-implementation` (renamed from spec)
- [ ] Create 10 fixtures for `engineer-domain-model` (renamed from domain-modeling)
- [ ] Create 10 fixtures for `tdd`
- [ ] Create 10 fixtures for `diagnose-incident` (renamed from diagnosing-bugs)
- [ ] Add `.github/workflows/eval-skills.yml`
- [ ] Establish baseline pass rates
- [ ] Set up drift detection

### Phase 9: Plan.md Artifact + Entry Points + Defaults (Week 15-16)

- [ ] Update `build/plan-implementation` to write `plan.md` (already renamed from spec)
- [ ] Create `plan.md` template
- [ ] Update code review to check plan conformance
- [ ] Document plan-driven development in `build/README.md`
- [ ] Test plan → implement → review cycle
- [ ] Write 6 routing wrapper skills (plan, design, build, test, deploy, maintain)
- [ ] Update catalog to feature lifecycle category first
- [ ] Update README.md with six-verb quick start and role evolution narrative
- [ ] Implement single-product defaults in coordinator
- [ ] Update `/init-context` to set product mode
- [ ] Write migration guide for existing users

### Phase 10: Policy Hooks (Week 17)

- [ ] Design `.claude/hooks/` schema
- [ ] Write `scripts/run-hooks.py`
- [ ] Add 5 example hooks (product.html protection, specs-require-tickets, etc.)
- [ ] Generate `.git/hooks/pre-commit`
- [ ] Add hook verification to CI
- [ ] Document hook authoring

### Phase 11: Polish and Documentation (Week 18-20)

- [ ] Write comprehensive tutorial (idea → shipped feature using 6 verbs)
- [ ] Write role evolution narrative for README.md (feature implementer → system designer → platform curator)
- [ ] Document the three-phase technical design approach with examples
- [ ] Document UI/UX boundary (functional requirements define WHAT, UX defines HOW)
- [ ] Update all skill documentation for new phase layout and renamed skills
- [ ] Audit and fix all broken cross-references after renaming
- [ ] Add troubleshooting guide for common design phase questions
- [ ] Write comparison doc (old vs new workflow, naming changes)
- [ ] Write migration guide for existing users (backward compatibility, renamed skills)
- [ ] Record demo video showing full lifecycle with role evolution
- [ ] Tag release `v2.0.0` with AI-Native SDLC alignment (breaking: renamed skills)

---

## Migration Guide for Existing Users

**Breaking changes:**
- Skill paths changed (`system/skills-src/product/discovery/brainstorm` → `system/skills-src/plan/brainstorm`)
- **Skill names changed** to avoid collisions with reference skills:
  - `write-prd` → `define-outcomes` (emphasizes measurable outcomes)
  - `prototype` → `validate-prototype` (emphasizes validation phase)
  - `spec` → `plan-implementation` (writes plan.md, avoids collision)
  - `domain-modeling` → `engineer-domain-model` (DDD engineering phase)
  - `codebase-design` → `harden-architecture` (emphasizes maintenance)
  - `interaction-design` → `design-interaction-flow` (emphasizes journey)
  - `brainstorm-feature` → `brainstorm-approaches` (implementation approaches)
  - `tasks` → `break-into-tasks` (clearer action verb)
  - `diagnosing-bugs` → `diagnose-incident` (moved to maintain phase)
- Design phase now has three mandatory sequential sub-phases (requirements → UX → technical)
- Technical design requires DESIGN.md with ADRs (not optional)
- Six new top-level verbs route to workflows

**Non-breaking:**
- Old skill names redirect to renamed versions for 6 months with deprecation notice
- Memory protocol unchanged
- `catalog/skill-set.json` format unchanged (category IDs and names updated)
- Existing mature skills (product, UX, context, craft) work unchanged

**Migration steps:**
1. Pull latest version (v2.0.0)
2. Review renamed skills in naming strategy table
3. Update any automation/scripts that invoke skills by old names
4. Run `/init-context` to update `docs/agents/memory.md` routing
5. Start using six verbs (`/plan`, `/design`, `/build`, `/test`, `/deploy`, `/maintain`)
6. (Optional) Configure autonomy rules for `/maintain` in `.claude/settings.json`
7. (Optional) Add policy hooks to `.claude/hooks/`

**Gradual adoption:**
- Old skill names redirect with deprecation warnings (6-month grace period)
- Six verbs are convenience routers that compose renamed skills
- Design phase sub-phases can be invoked individually or via `/design` workflow
- Autonomous maintenance is opt-in (requires alert integration)
- Component extraction is opt-in (only after 2-3 features stabilize patterns)

**What to expect:**
- Agent triggering may improve (less confusion between our skills and reference skills)
- Design workflow takes longer initially (three sub-phases vs ad-hoc), but produces better artifacts
- Build phase faster (implements from DESIGN.md vs designing on the fly)
- Evals track that renamed skills trigger correctly on typical requests

---

## Success Metrics

**Adoption:**
- [ ] 50% of users invoke top-level verbs vs individual skills (tracked via telemetry)
- [ ] Autonomous maintenance handles 80% of alerts within control band (no escalation)
- [ ] Design phase used for 80% of features (not skipped to go straight to build)

**Quality:**
- [ ] Skill eval pass rate >90% and stable (no >10% drift after renaming)
- [ ] Policy hooks block 100% of direct product.html edits
- [ ] UX design produces one unified design doc per feature (not per-page fragments)
- [ ] Technical design phase produces DESIGN.md with ADRs for 90% of features

**Velocity:**
- [ ] Plan approval cycle <24h (plan.md committed, reviewed, approved)
- [ ] Design phase (all three sub-phases) completes in <3 days for typical feature
- [ ] Component extraction reduces time-to-implement for 3rd+ similar feature by 40%

**Completeness:**
- [ ] All 6 phases have mature skills (plan 9, design 25+, build 6+, test 4+, deploy 5, maintain 4)
- [ ] `/deploy` phase has CI/CD, staging, production, rollback skills
- [ ] `/maintain` closes the loop (alert → diagnosis → implementation change → build without human)
- [ ] Technical design has all three sub-phases fully specified

**Role Evolution:**
- [ ] Users report progression from "writing pages" to "designing systems" in feedback
- [ ] Component extraction used after 2-3 features stabilize (not prematurely)
- [ ] Engineering design artifacts (DESIGN.md, ADRs) referenced during code review for 80% of PRs

---

## Risks and Mitigations

**Risk:** Breaking existing workflows during restructure and skill renaming  
**Mitigation:** Keep symlinks stable; backward compatibility maintained through old skill names redirecting to renamed versions; comprehensive test suite covers all 47+ skills; gradual rollout with migration guide

**Risk:** Naming collisions with reference skills cause agent confusion  
**Mitigation:** Distinct naming strategy applied (define-outcomes vs write-prd, plan-implementation vs spec, engineer-domain-model vs domain-modeling); skill descriptions explicitly disambiguate; evals track triggering accuracy before and after renaming

**Risk:** Three-phase design process is too heavy, slows velocity  
**Mitigation:** Prototype validation is optional (skip for simple features); component extraction is deferred (only after 2-3 features stabilize); engineering hardening is the only mandatory phase; workflows provide "fast path" routing for routine features

**Risk:** UI/UX boundary unclear after refactoring  
**Mitigation:** Explicit workflow documentation: requirements define WHAT, UX defines HOW (delivery), technical defines HOW (engineering); UX skills updated to inspect whole product, not per-page; design workflow enforces sequential sub-phases with clear handoff criteria

**Risk:** Role evolution narrative feels aspirational, not actionable  
**Mitigation:** Concrete skill sequences show progression (spike-unknowns → engineer-domain-model → extract-components); success metrics track artifact production (DESIGN.md, ADRs, component docs); evals measure whether skills actually produce system design artifacts vs per-page implementations

**Risk:** Autonomous maintenance makes unsafe changes  
**Mitigation:** Control-band rules explicit in `.claude/settings.json`; first 5 auto-fixes require retroactive approval; always log to `incidents.md`; change records require verifiable current/intended behavior

**Risk:** Continuous evals flaky or expensive after renaming  
**Mitigation:** Start with 10 fixtures per critical renamed skill; baselines established before and after rename; cache results; run on schedule not every commit; drift detection alerts on >10% degradation

**Risk:** Users confused by two ways to invoke (verb vs skill name) plus renamed skills  
**Mitigation:** Docs emphasize six verbs as entry points; skill names for power users; catalog shows lifecycle first; migration guide lists all renamed skills with old→new mapping; old names redirect with deprecation notice for 6 months

**Risk:** 20-week timeline is too aggressive for 30+ new skills  
**Mitigation:** Phased rollout allows early phases to ship while later phases develop; product and UX skills already mature (minimal work); focus first 10 weeks on design phase (highest value); deploy/maintain phases can ship incrementally

---

## Open Questions

1. **Should `/deploy` support multiple environments (dev/staging/prod) or one workflow per environment?**
   - Recommendation: One workflow, environment as parameter (`/deploy --env staging`)

2. **How do we test autonomous maintenance without real monitoring infrastructure?**
   - Recommendation: Mock alert payloads in evals; integration test with local Prometheus

3. **Do we keep legacy workflows (ideas.md, feature-delivery.md) or retire them?**
   - Recommendation: Keep for 6 months; mark deprecated; route users to new verbs

4. **Should plan.md be committed to feature branch or kept in docs/changes/?**
   - Recommendation: Commit to branch (like a spec); reviewed in PR; moves to docs/changes/ on merge

5. **How do we version the memory protocol if it needs to change?**
   - Recommendation: Protocol version in `docs/agents/memory.md`; skills check version; migrations scripted

6. **Should we add parallel orchestration later?**
   - Recommendation: Defer until core lifecycle is stable and demand is clear; current serial workflows are sufficient

7. **How do we prevent over-abstraction in the component extraction phase?**
   - Recommendation: Enforce "3 uses minimum" rule; component extraction skills check for duplication evidence; reject extraction PRs without 2-3 existing implementations referenced

8. **Should renamed skills redirect permanently or expire after 6 months?**
   - Recommendation: 6-month redirect with deprecation warnings; hard cutoff forces migration; old names removed in v3.0.0

9. **How do we ensure DESIGN.md is actually used during build phase?**
   - Recommendation: build/plan-implementation skill reads DESIGN.md and references it in plan.md; code review checks for conformance; hooks warn if DESIGN.md is stale (>30 days old for active feature)

10. **Should we build frontend/backend specialization in build phase now or later?**
    - Recommendation: Later (after v2.0.0 ships); current build skills are general-purpose; specialization comes when role-specific patterns are clear from real usage

---

## Appendix: File Inventory After Restructuring

```
system/
├── skills/                   # 47 symlinks (unchanged entry points)
├── skills-src/               # Source organized by lifecycle
│   ├── plan/                 # 10 skills (was product/)
│   ├── design/               # 11 skills (was design/)
│   ├── build/                # 5 skills (was engineering/)
│   ├── test/                 # 2 skills (was quality/testing/)
│   ├── deploy/               # 4 skills (new, was operations/ empty)
│   ├── maintain/             # 3 skills (new, autonomous loop)
│   └── craft/                # 12 skills (context + meta, cross-cutting)
├── workflows/
│   ├── plan.md               # NEW: top-level plan workflow
│   ├── design.md             # NEW: top-level design workflow
│   ├── build.md              # NEW: top-level build workflow
│   ├── test.md               # NEW: top-level test workflow
│   ├── deploy.md             # NEW: top-level deploy workflow
│   ├── maintain.md           # NEW: top-level maintain workflow
│   ├── ideas.md              # DEPRECATED: use /plan
│   ├── feature-delivery.md   # DEPRECATED: use /build
│   ├── testing.md            # DEPRECATED: use /test
│   ├── debugging.md          # DEPRECATED: use /maintain
│   └── context-coordination.md  # Unchanged (already handles serialization)
├── memory/                   # Unchanged
├── agents/                   # Unchanged
├── commands/                 # Unchanged
├── docs/                     # Unchanged
└── evals/                    # NEW: continuous skill evals
    ├── skills/
    │   ├── write-prd/
    │   │   ├── fixtures/
    │   │   └── eval-config.yaml
    │   ├── spec/
    │   ├── tdd/
    │   └── diagnosing-bugs/
    └── results/              # Timestamped eval results

scripts/
├── eval-skills.py            # NEW: eval runner
├── run-hooks.py              # NEW: policy hook executor
└── (existing scripts)

.claude/hooks/                # NEW: repo-level policy hooks
├── pre-write.yaml
├── post-write.yaml
└── pre-commit.yaml

.github/workflows/
└── eval-skills.yml           # NEW: CI for skill evals
```

---

**End of Improvement Plan**

Next steps:
1. Review and approve this plan
2. Create GitHub issues for each week's work
3. Start with Week 1-2 (restructure) on a branch
4. Merge incrementally with thorough testing
