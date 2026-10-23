# Fifth batch source review

Last updated: 2026-10-23

## Review

**BLOCKERS: none**

**Merge verdict: OK with notes** for the reviewed B7/B10/B11/B17/B23 source. Two P2 findings follow. No P0/P1 defect or dangerous default release action was found.

This was a read-only inspection of the working-tree diff, integrated source, tickets, fixtures, and focused tests. No edits, commands, model calls, or subagents were run. The reported 152 passing tests, configured tokenizer checks, builder/check, and 45-skill validators are parent-supplied results, not independently executed results from this review.

### Correct

- **B7 — Narrow review and separate budgets.** [orchestration.md:56](/Users/xhl/GitHub/skills/agent-coding-skills/system/protocols/orchestration.md:56) requires readable brief, criteria, diff, and source/input identities, and says: “Never pass the implementer's report … including during re-review.” Spec compliance precedes quality; unresolved verification and stale verdicts block completion. [Line 66](/Users/xhl/GitHub/skills/agent-coding-skills/system/protocols/orchestration.md:66) specifies resume for rounds 1–3, fresh implementers for 4–5, and no automatic sixth round. [Line 70](/Users/xhl/GitHub/skills/agent-coding-skills/system/protocols/orchestration.md:70) states “Neither counter resets the other”; operational retries remain capped at two after the initial attempt. Coordinator/worker boundaries and the separate whole-branch review are explicit.

- **B10 — Release defaults preserve authorization and evidence gates.** [acs-ship:28](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/deploy/acs-ship/SKILL.md:28) says invocation alone does not authorize commits, pushes, PR writes, merges, or deployment. Verification reruns every invocation; three persisted review-fix rounds end in `converged: false` when unresolved. [acs-release:26](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/deploy/acs-release/SKILL.md:26) blocks unset commands/environments and grants no release authority. The following steps require merge-state readback without merge retry, a non-mutating first-use/configuration-change invocation ending `not released`, current source/artifact/environment evidence, error-budget gates, and staged rollout. Canary debouncing explicitly cannot delay immediate safety stops. No default production target or mutating release command is supplied.

- **B11 — Observable local failure exercise, with appropriately limited claims.** [acs-design-contracts:63](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/design/technical/acs-design-contracts/SKILL.md:63) requires 2–4 questions before signals, complete signal mapping, three-line runbooks, alert receipts, and telemetry-only diagnosis. The [local test:97](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/tests/test_design_contracts_observability.py:97) injects a provider timeout, emits telemetry, writes and reads a temporary alert receipt, and passes only telemetry plus the runbook query into `diagnose`. This exercises a real local code path; it does not demonstrate model diagnosis or production observability.

- **B17 — Safe execution defaults and explicit-only separation.** [trigger_evals.py:184](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/trigger_evals.py:184) defaults to a dry plan. Execution requires model, adapter argv, and a sufficient call ceiling. Requests omit target labels and expected answers; unauthorized explicit-only selections void the run. Metrics separate automatic and explicit cases, and near-misses must select their named neighbor. The new [ship fixtures](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/deploy/acs-ship/evals/trigger-fixtures.json:1) and [release fixtures](/Users/xhl/GitHub/skills/agent-coding-skills/system/skills-src/deploy/acs-release/evals/trigger-fixtures.json:1) each contain eight positives and eight reciprocal negatives.

- **B23 — Read-only mechanics match the settled adapter scope.** [acs-coordination.py:40](/Users/xhl/GitHub/skills/agent-coding-skills/scripts/acs-coordination.py:40) rejects ambiguous identities and reuses B14 status logic. Freshness leaves unbound records `unassessed` and reports changed, missing, or unsupported premises. `verify` uses B19 without executing evidence commands. [Checks:114](/Users/xhl/GitHub/skills/agent-coding-skills/scripts/acs-coordination.py:114) invokes fixed validators and builder `--check`; [build-plugins.py:337](/Users/xhl/GitHub/skills/agent-coding-skills/scripts/build-plugins.py:337) builds comparison output in temporary scratch. These paths do not rewrite selected source/generated trees or grant authority.

**Fixed:** None; read-only review.

### Findings

1. **P2 — Newly added skill bodies can escape the trigger runner’s source-drift check.**

   **Location:** [trigger_evals.py:128](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/trigger_evals.py:128), with the final comparison at [line 221](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/trigger_evals.py:221).

   **Evidence:** `fingerprint` hashes `list(sources.values())`, where `sources` was discovered once before execution. Both initial and final fingerprints receive that same dictionary. Fixture paths are rediscovered, but `SKILL.md` paths are not.

   Consequently, adding a new `skills-src/.../SKILL.md` during adapter execution, without adding a fixture file, changes the catalog but neither fingerprint. The run can report metrics against the old catalog without becoming `void`. This contradicts the guide’s claim that the fingerprint covers all source skill bodies and detects source changes during execution.

   **Smallest fix:** Rediscover `SKILL.md` paths inside `fingerprint`, retaining the fixture and runner hashing. Add a regression that creates a new skill body during a mocked adapter call and expects `status: void` with empty metrics.

2. **P2 — The trigger guide understates the integrated query and call counts.**

   **Location:** [trigger-evals.md:25](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/trigger-evals.md:25).

   **Evidence:** The guide says: “The current 552 queries at three repetitions require 1,656 adapter calls.” The added ship/release files contribute 32 cases, bringing the integrated inventory to **584 queries and 1,752 calls** at three repetitions. The regression inventory now explicitly expects 35 automatic skills in [test_trigger_evals.py:60](/Users/xhl/GitHub/skills/agent-coding-skills/system/evals/tests/test_trigger_evals.py:60).

   Someone choosing the documented call ceiling would encounter a budget rejection. The executable computes the larger count and rejects before execution, so this does not permit overspending.

   **Smallest fix:** Update the figures to 584/1,752, or direct users to the dry-plan output instead of maintaining a hard-coded “current” total.

### Acceptance gaps independent of defects

| Ticket | What remains unverified |
|---|---|
| **B7** | The scratch lifecycle and missing-package rejection are authored test oracles, not observed host enforcement. Actual reviewer judgment, live missing-brief rejection, and resume/fresh-executor behavior remain unverified, as disclosed in [B7:67](/Users/xhl/GitHub/skills/agent-coding-skills/docs/changes/acs-corpus-alignment/tasks/B7-review-seat.md:67). |
| **B10** | The local branch rehearsal executes checks and prepares a body, but does not invoke an independent shipping agent. Merge-error readback, dry-run behavior, and canary sequencing are authored traces. They do not establish live agent/provider compliance. External PR/deploy/rollback execution was deliberately outside this contribution’s authorization; it is not required merely to repair these source changes. |
| **B11** | The local mock establishes the named telemetry-only exercise. Model-generated design, independent model diagnosis, external alert delivery, and staging/production telemetry remain unverified. No broader operational-readiness claim follows from the mock. |
| **B17** | **Actual weak-model precision, recall, and collision correctness remain unmeasured.** User selection of model and budget is pending. Mock success and balanced fixtures cannot satisfy the measured gate. B16/B22 remain blocked on their stated user-owned decisions. |
| **B23** | Local Markdown resolution, hashes, status, evidence validation, and fixed checks are the implemented scope. Remote tracker integration, claims/dispatch enforcement, execution attestation, and semantic freshness propagation are explicitly outside that adapter. Historical ticket smoke outputs do not establish the current integrated frontier or freshness state. |

Neither the source-review verdict nor the reported green suite closes the live-behavior or measured-model gaps above.
## Parent disposition

Both P2 findings fixed: fingerprint rediscovers SKILL.md files; actual mocked-adapter mutation test creates a new skill and requires void/empty metrics. Guide count corrected to 584/1,752 with dry-plan authority. All 16 trigger tests pass.
