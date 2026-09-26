# Namespace every skill with an `acs-` prefix

Last updated: 2026-09-26

Change: IMPROVEMENT-PLAN — naming strategy
Status: accepted
Basis: shipped in `17c3eb2`, tagged `v0.4.0`; 44 skill packages under `system/skills-src/` all carry the prefix
affects: every skill `name`, `system/skills/` symlinks, `catalog/skill-set.json`, host invocation syntax
supersedes: the per-skill renaming table proposed in the improvement plan

Agents selecting a skill by name confused this suite's skills with similarly-named reference skills from other collections — `write-prd`, `spec`, `prototype`, `interaction-design`, `tdd` and a dozen others are generic enough to collide. Every skill takes a uniform `acs-` prefix, so the suite is identifiable from the name alone.

## Considered options

The improvement plan first proposed renaming each colliding skill to something semantically distinctive: `define-outcomes` instead of `write-prd`, `settle-requirements` instead of `spec`, `challenge-approach` instead of `grilling`. That was rejected in favour of a uniform prefix. Per-skill renaming distorts each name to carry namespace information — `settle-requirements` is a worse description of the skill than `spec` — and it only defends against collisions already known, so every new reference collection reopens the question. A prefix is one rule, it defends against unknown collections, and it leaves each bare name free to be the clearest description of its own job.

Some of the distinctive names survived on their own merits where they genuinely described the skill better; they are not namespace devices.

## Consequences

The prefix is part of the skill `name`, not a host concept. Neither `/`, `$`, nor a host or plugin namespace becomes part of it — hosts add their own invocation syntax around the ID. See [the harness architecture](../../system/docs/harness-architecture.md).

External skill names and protocol selectors such as `research.question` are unchanged; the prefix applies to this suite's skills only.
