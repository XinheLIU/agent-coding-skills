# Review Formats

Last updated: 2026-10-23

Load for the active scan/report. The [skill procedure](../SKILL.md) governs evidence and separate-axis verdicts; these are formatting examples and routing details, not extra gates.

## Security scans

```bash
DIFF="git diff <range>"   # the scope's diff command from Step 0
$DIFF | grep "^+" | grep -iE "(api_key|secret|password|token|passwd)\s*=\s*['\"][^'\"]{6,}['\"]"   # hardcoded secrets
$DIFF | grep "^+" | grep -E "os\.system\(|subprocess.*shell=True"                                  # shell injection
$DIFF | grep "^+" | grep -E "\beval\(|\bexec\("                                                    # dangerous eval/exec
$DIFF | grep "^+" | grep -E "pickle\.loads?\("                                                     # unsafe deserialization
$DIFF | grep "^+" | grep -E "execute\(f\"|\.format\(.*SELECT|\.format\(.*INSERT"                   # SQL via string formatting
```

## Report layout

Keep Standards and Spec in separate subsections in each priority bucket and the appendix. Retain consumed revisions and unassessed scope.

```markdown
# Code Review — Mode {A|B|C} — {scope summary}
Generated: {YYYY-MM-DD HH:MM}
Branch: {branch}
Scope: {TRC rows | user path | git range | FND-ARC drill files}
Reviewer: acs-review-code-quality
Spec source: {path | "none — Standards-only review"}
Lenses delegated: {list, or "none — inline only"}
Lenses skipped: {list with reason: NOT DETECTED | failed | not invoked}

## Verdict
READY | READY-WITH-FIXES | NOT-READY
Reasoning: <1–2 sentences. Cite blocking Criticals and their axis if NOT-READY.>

## Summary
- Findings: N total (P0: a, P1: b, P2: c — Standards: s, Spec: p)
- Coverage: X branches, Y tested (Z%)
- Critical steps: N  Important: N  Nice-to-have: N

## Strengths
<2–5 specific bullets of what's done well.>

## CRITICAL
{entries in dependency order}

## IMPORTANT
{entries}

## NICE-TO-HAVE
{entries}

## Findings (appendix)
{findings in canonical format, including appendix-only low-confidence and unverified entries; keep these separate from main findings}

## Coverage Diagram
{ASCII diagram from Step 3}

## Per-Domain Reports
{one section per lens that ran; "Not detected" or "Skipped — inline" where applicable}
```

## Security finding fields

For every security finding append the [security evidence rubric](../SKILL.md#security-evidence-rubric) fields (including explicit unknowns):

```
  Severity: <P0/P1/P2; impact and attacker prerequisites>
  Confidence rationale: <support, unknowns and counterevidence for N/10 above>
  Evidence state: <candidate | supported-static | supported-reproduced | disproved>
  Entrypoint: <attacker control, quote/revision or unknown; next check>
  Boundary crossing: <path, invariant, controls, quote/revision or unknown; next check>
  Demonstrated impact: <effect, static trace or executed evidence, or unknown; next check>
  Reachability: <reachable | unknown | unreachable; scoped evidence or next check>
  Challenge: <independent input/response references or sequential limitation; dissent and reconciliation>
```

## Design routing

Standards and Spec findings stay in separate subsections. Route design-level findings separately; never demote them to code findings.

| Concern | acs-review-code-quality | Design card |
|---|---|---|
| Handler validation, error envelope, status codes | ✓ | — |
| SQL correctness, injection, indexing, N+1 | ✓ | — |
| Code-level auth bugs, weak defaults, missing role check | ✓ | — |
| Concrete reliability bugs (no timeout, no shutdown handler) | ✓ | — |
| Local performance smells (per-row insert, model reload) | ✓ | — |
| Concrete security bugs (committed secrets, TLS off) | ✓ | — |
| Test coverage / quality, complexity, smells | ✓ | — |
| Module boundaries, layering, ownership | — | ARC / MOD |
| Service / deploy topology, network exposure | — | ARC |
| Canonical data model, schema ownership, lineage | — | ARC |
| Tech-stack fit, scaling cliffs | — | ARC |
| Cross-cutting design decisions (ADRs) | — | ARC |
| API surface design (versioning, contract style) | — | CON |
| Authn/authz architecture (trust boundaries, role topology) | — | ARC / CON |
| Invariants, error semantics, failure-mode design | — | CON |
| Test strategy (layers, seams, gates) | — | TST |

Cross-reference format: `[→ <ARC|MOD|CON|TST> (<lens>)] file:line — description`.

## Provenance

Provenance: adapted from [gstack CSO's evidence rubric](https://github.com/garrytan/gstack/blob/35dd014c580037d1c009776d8b0584587c1bd42c/cso/SKILL.md.tmpl) (Phase 12, rubric only) and [Addy Osmani's security-and-hardening](https://github.com/addyosmani/agent-skills/blob/aeac41d/skills/security-and-hardening/SKILL.md) (input ownership, boundaries and abuse cases). ACS retains its quote gate and ARC/CON routing; no upstream security runtime is included.
