# acs-maintain

Maintenance-phase plugin for the Agent Coding Skills (ACS) system. Handles incident response: reproducing failures, diagnosing root causes, and applying minimal fixes with regression coverage.

## Current skills

| Skill | Phase | Purpose |
|-------|-------|---------|
| `acs-diagnose-incident` | maintain | Diagnose hard bugs and performance regressions through a red-capable feedback loop, evidence log, and regression test |

**Planned but not yet implemented:** `acs-fix-incident` — a dedicated skill for applying and verifying fixes after diagnosis is complete. For now, `acs-diagnose-incident` covers the full diagnose-to-fix loop (see phase 4 of its SKILL.md).

## Maintenance workflow

```
acs-init-context
      ↓
acs-diagnose-incident   ← build red loop → reproduce → hypothesize → fix → close
      ↓
acs-fix-incident        (planned)
```

## Installation

Copy the plugin into your skills directory:

```bash
cp -r plugins/acs-maintain ~/.claude/plugins/
```

Or reference it directly from this repository by adding `plugins/acs-maintain/skills/` to your agent's skill search path.

## Usage

Requires `acs-context` (for shared memory and context protocol). Works alongside `acs-test` for regression verification.

1. Run `acs-init-context` to initialise shared memory for the active effort.
2. Invoke `acs-diagnose-incident` with a symptom description:

```
acs-diagnose-incident --issue "login fails on production after deploy #412"
```

The skill will build a reproducible red loop, minimise the case, test ranked hypotheses, apply a fix, and produce a `diagnosis.md` with the confirmed root cause and verification evidence.

## Dependencies

- Required: `acs-context ^0.4.0`
- Peer: `acs-test ^0.4.0` (recommended for regression test integration)
