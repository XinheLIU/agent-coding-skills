# B16-eval-harness: Build a behavioral eval harness for ACS skills

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: pending
Readiness: needs-design
depends_on: none
affects: `system/evals/`; reuse `../../agent-skills/user-setup/skills/optimize-skill`
Effort: L

## Scope

33 behavioral scenarios in `system/evals/evals/` each need a manual isolated run; the last independent forward test is marked historical.

Build a harness that runs with-skill and without-skill pairs, grades transcripts with an agent that also critiques weak assertions, and reports a delta. Combine: pstack's blinding; Superpowers' no-guidance control and five or more repetitions; PM-Skills' three arms (skill, template only, freehand) with `void` on partial runs; gstack's cheap deterministic checks plus scheduled judged checks.

Start with `acs-research`, `acs-tdd`, `acs-review-code-quality`, `acs-implement`. Measure two contested decisions first: blocks of 4–5 questions versus frontier rounds, and B1's shorter descriptions.

## Inputs

- Analysis: §7.7, §8.8 G9, §10 B16.
- Sources: `optimize-skill`; PM-Skills `output-eval-informed`; pstack eval playbook; Superpowers controls; gstack tiers.

## Verification

- One skill produces a with/without delta over five runs with a control.
- A partial run is recorded as `void`, not a pass.
- Results are stored under `system/evals/` with the model, date and harness revision.

## Blockers

Decide the grading model and the budget before building. The harness must not depend on Claude Code alone.

## Coordination proposal

B22 consumes this. B17 is separate. Both write `system/evals/`; sequence or namespace by directory.

## Evidence

Not yet collected.
