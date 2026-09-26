# Organize skills by lifecycle phase, not by domain

Last updated: 2026-09-26

Change: IMPROVEMENT-PLAN — AI-Native SDLC alignment
Status: accepted
Basis: shipped across `17c3eb2`..`eb84af4`, tagged `v0.4.0`; target tree present at `system/skills-src/{plan,design,build,test,deploy,maintain}`
affects: every skill path, `catalog/skill-set.json`, plugin boundaries, workflow names

The suite was organized by domain — `product/`, `design/`, `engineering/`, `quality/`, `operations/`, `craft/` — which named the team that owns a skill rather than the moment a user needs it. Users arriving at 47 skills had to know that "write a PRD" lives under `product/` and "review this code" under `quality/`, and there were no top-level entry points: navigating 47 skills instead of invoking a handful of verbs. Skills were re-grouped under the six lifecycle phases of Anthropic's AI-native SDLC playbook, so the directory a skill lives in is the phase a user is in when they want it.

## Considered options

Keeping domain organization and adding a routing layer on top was rejected: it preserves the mismatch and adds a second thing to maintain. The domain grouping survives where it is genuinely orthogonal — `context/` is cross-cutting and sits outside the six phases rather than being forced into one.

## Consequences

`deploy/` currently exists as an empty phase directory. The lifecycle vocabulary commits the suite to a deploy phase before skills exist to fill it; the alternative was omitting the phase and renumbering later, which would have broken installed plugin names a second time.

The prior lifecycle labels remain readable as compatibility aliases — see the compatibility section of [the shared protocol](../../system/protocols/skill-declarations.md).
