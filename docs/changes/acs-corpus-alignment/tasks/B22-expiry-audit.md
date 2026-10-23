# B22-expiry-audit: Audit and expire skills when a new model lands

Last updated: 2026-10-23

Parent: acs-corpus-alignment
Type: implementation
Status: pending
Readiness: needs-design
depends_on: B16-eval-harness
affects: `system/skills-src/authoring/acs-writing-great-skills/SKILL.md`; a recorded audit table
Effort: M

## Scope

`acs-resolving-merge-conflicts` survives the model change that made Pocock delete his equivalent, and no skill carries the model it was last tested on.

Add a rule to `acs-writing-great-skills`: every section must pass the no-op test on the current model; record the model it was last tested on. When a new frontier model lands, run B16's with/without comparison per skill and per section for long ones; delete what no longer changes behavior and record the deletion with the model and the evidence.

First pass candidates: `acs-resolving-merge-conflicts`, the mandatory parts of the UX and plan pipelines, and long rationale prose.

## Inputs

- Analysis: §8.8 G12, §10 B22.
- Sources: Anthropic 2026-03-24; Pocock `writing-for-agents:81`; Superpowers' placeholder datum.

## Verification

- An audit table lists skill, model, delta and decision.
- At least one skill is deleted or shrunk with the evidence recorded.
- The authoring skill states the rule and the required record.

## Blockers

Needs B16 to produce the comparison; without it, the audit is opinion.

## Coordination proposal

Depends on B16. Edits `acs-writing-great-skills`; B18 edits `acs-review-agent-instructions`.

## Evidence

Not yet collected.
