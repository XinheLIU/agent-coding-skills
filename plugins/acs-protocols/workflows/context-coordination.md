---
protocol: acs:context-coordination
version: 1.2.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/context-coordination.md
---

# Context Coordination

Last updated: 2026-10-23

The active agent performs this coordinator role under the [shared protocol](../protocols/skill-declarations.md), including when invoking a skill standalone. This is a Harness contract supported by a read-only executable kernel, not a new coordination service. Domain skills return results and proposed transitions; the coordinator applies shared state changes through capabilities actually available in the session.

The [harness architecture](../resources/docs/harness-architecture.md) defines source identity, standalone packaging, and the boundary with Codex, Claude Code, Pi, OpenCode, and DeepSeek harness adapters. Keep domain procedures and shared state semantics here; put host APIs, invocation syntax, worker executables, and lifecycle integrations in their binding. A plugin manifest alone does not establish runtime support. Bind claims, dispatch, progress, and approval through the [coordination duty adapter table](../resources/docs/harness-architecture.md#coordination-duty-bindings); a binding is unavailable until verified in the current host/session. The rules below are semantic obligations, not claims that prose implements locks, subagents, todos, or hooks.

## Executable mechanics

The source-checkout [coordination kernel](https://github.com/XinheLIU/agent-coding-skills/blob/main/scripts/acs-coordination.py) provides `resolve`, `status`, `freshness`, `verify`, and `checks` commands; run `python3 scripts/acs-coordination.py --help` and each command's `--help` for arguments and input formats. It reuses the canonical task scanner, evidence checker, catalog validator and derived-surface checker. Hosts resolve explicit references and configured tracker/active-state pointers under the [resolution precedence](../protocols/skill-declarations.md#repository-configuration-and-resolution), then supply local paths. The local Markdown adapter rejects ambiguous task IDs; it does not replace an established tracker or infer identity from a branch name.

For file premises, the `freshness` command reads optional `acs-consumed-revisions` JSON fences inside the owning Markdown record. Each binding names `source` (relative to that record), `revision` (SHA-256 of exact file bytes), and affected `scope`; its command help defines the format. This is an in-record relationship, not a sidecar status store. Unbound records remain unassessed. Missing, changed, or unsupported revisions are review candidates; malformed bindings fail. Other tracker/HTML/environment revision formats require a host adapter or domain review. The kernel reports candidates without deciding material impact, propagating status, or erasing accepted history.

`verify` compares recorded evidence with independently resolved dispatch and completion identities; it cannot prove the command ran. `checks` runs fixed repository validators and the builder's `--check`; derived comparison uses temporary scratch, leaving the selected output unchanged. All commands emit JSON; nonzero means invalid input, review candidates, rejected evidence, or a failed check. No command acquires claims, writes canonical records, runs evidence-supplied commands, delegates, or grants authorization. Shared-write serialization, claims, approval and domain judgment remain the obligations below. Installations without the source-checkout CLI must expose a verified binding or report the capability unavailable; a packaged link alone is not runtime support.

## Enter or resume a run

Before the first skill, apply the [rigor tiers](README.md#rigor-tiers): announce the tier and reason and record the tier, current stage, approval reference or pending gate, and model/sensor cadence in the single configured recovery entry. On resume, recover that selection and its approvals; hidden complexity can only raise the tier. The workflow owns tier selection and staged approval; [Questioning](../protocols/questioning.md) owns how missing decisions are asked. This applies to standalone skill entry as well as workflow entry.

## Assemble only the needed context

1. Resolve canonical change/task identity and paths by the protocol's precedence. Keep the established tracker; for new local changes use tracked `docs/changes/<change-id>/`, with scratch in the configured work root.
2. Read canonical ticket status and the active run's single configured recovery entry. Follow the chosen skill's `context.requires` and relevant `retrieves` selectors. Product HTML: read navigation, then only the relevant articles and their premises; do not load every domain contract.
3. Supply references, consumed revisions, scope, relevant constraints, and known review findings. Resolve missing answers from existing artifacts before asking. An inaccessible source is transported as a bounded temporary excerpt with its source revision; never create another normative spec.
4. Bind requests to tools, skills, agents, shell commands, or direct work that actually exist. A named consumer is not a dispatch instruction. If a capability is absent, perform the stage directly when competent, or report the concrete missing capability and its blocking effect.

## Schedule and reconcile

**Dispatch semantics.** Implementation proposes slices, dependency edges, and shared-write risks. Only the unblocked frontier may be delegated through a verified, authorized subagent binding under the [orchestration contract](../protocols/orchestration.md). Disjoint filenames alone do not prove independence: shared contracts, generated outputs, configuration, migrations, and tests can still require serialization. Unavailable delegation means direct serial execution when competent.

**Claim semantics.** The protocol's [exclusive claims and serialized writer](../protocols/skill-declarations.md#coordinated-writes-and-claims) protect canonical task ownership and shared state. Worktrees isolate contributions; one writer reconciles shared files/tracker records. Check target and premise revisions immediately before applying a contribution; changed revisions require reconciliation. A stale claim request returns a conflict, never an overwrite. Without safe claims, work serially; without exclusive shared-write authority, block the affected writes. Canonical ticket status stays in its tracker; claims and execution steps do not become another status source.

**Reconciliation semantics.** Preserve contribution ownership. Reconcile by stable subject/record IDs; repeat submissions with unchanged evidence are no-ops. Conflicting assessments remain visible until their owner resolves them. Skill output may propose changes to another domain, but does not authorize them.

## Execution-time rulings

Resolve lookup and observable facts first under [Questioning](../protocols/questioning.md#classify-before-asking), then classify each open execution decision using its three decision classes:

| Class | Execution route |
| --- | --- |
| Mechanical decision | Decide from evidence and existing constraints within the authorized scope; record a ruling and continue. |
| Taste decision | Choose provisionally within the authorized scope; record the recommendation and trade-off as a ruling, continue, and surface it at the next existing review gate. |
| User challenge | Ask before changing the user's stated direction or deciding a user-reserved matter. Keep the original direction; block only dependent work until answered. |

Write each mechanical or taste ruling in the run's single configured recovery entry, with its classification and relevant task/revision reference:

```text
Ruling: <what> — <why> — <cost if wrong>
```

Promote consequential rulings to Persistent Changes before formal review, downstream reliance, or handoff, following [Phase boundaries](#phase-boundaries) and the shared retention rules. A provisional taste ruling remains provisional; recording it does not turn it into an accepted user decision. Include a **Rulings made** list in the [handoff envelope](../protocols/skill-declarations.md#handoff-envelope), with accessible references to consequential records and any review still due.

### Stop classes

Within an authorized execution plan, these action/plan classes require a stop of the affected work:

| Stop class | Required response |
| --- | --- |
| Irreversible or destructive operation | Check existing explicit authorization for this exact action; if missing or insufficient, stop and ask before acting. |
| Security-sensitive action | Check existing explicit authorization for this exact action; if missing or insufficient, stop and ask before acting. |
| Externally visible action | Check existing explicit authorization for this exact action; if missing or insufficient, stop and ask before acting. |
| Hopeless plan | Stop and report when no evidence-backed safe path remains; do not guess a new direction. |

These four classes do not override user challenges, explicit user gates, missing required capabilities, or the [bounded retry policy](../protocols/orchestration.md#failure-policy). Existing authorization persists: do not ask again for an already authorized action whose scope and conditions still match. A mechanical or taste classification grants no authority to cross a gate. Continue independent authorized work while a dependent action is stopped. Ordinary ambiguity within scope is a ruling, not a reason to stall the whole run.

Adapted from Superpowers [`subagent-driven-development`](https://github.com/obra/superpowers/blob/5bf4e78/skills/subagent-driven-development/SKILL.md) (rulings and four stop classes) and gstack [`autoplan`](https://github.com/garrytan/gstack/blob/35dd014/autoplan/SKILL.md.tmpl) (decision taxonomy), with ACS authorization and user-challenge rules preserved.

## Transition and verification

**Progress semantics.** Use the verified host todo list for run-local execution steps; when unavailable, keep those steps in the single configured Working recovery entry. Todo completion is a scheduler observation, not canonical ticket status or verification. On a meaningful transition, preserve the next action, blockers, canonical status link, changed anchors, and consumed revisions in that recovery entry so a new session can resume; do not duplicate the todo history. Apply freshness propagation from the protocol, routing reassessment to each domain owner. Regenerate only affected derived views.

Testing owns evidence interpretation. The coordinator records its exact code/diff revision, criteria, commands, environment/configuration assumptions, failures, skipped/not-run checks, and omissions in compact Persistent Changes. A high pass percentage or completed checklist cannot establish readiness over missing criteria. A changed artifact or environment cannot inherit a previous verification verdict without reassessment.

Use the common handoff envelope for transfers under [Phase boundaries](#phase-boundaries), and transfer claims explicitly. Save necessary proposals and evidence in Persistent Memory at the boundary required there; `proposed` is a valid durable status. At completion follow the protocol's retention gate; verify durable links with the run directory unavailable before removing reconciled scratch. Do not delete accepted requirements, design rationale, or final verification.

## Phase boundaries

At the end of a phase, before persisting a handoff, assess two questions from the available context:

1. Does the next phase consume this one as a primary source?
2. Is there enough context room left for the next phase?

If both answers are yes and the same agent continues in the same session and worktree, continue with the live reasoning and persist the necessary proposals and evidence afterwards. A domain or skill change alone does not require a serialized handoff. This defers phase-boundary persistence, not the final durable record. If either answer is no or unknown, persist the necessary records and minimum evidence before the next phase; do not assume context capacity or discard relevant reasoning.

A handoff remains mandatory across sessions, worktrees, and agents, even when both answers are yes. Before the transfer, persist the receiver's necessary records and minimum evidence and provide the [handoff envelope](../protocols/skill-declarations.md#handoff-envelope) with accessible, revision-labelled references. Formal review and reliance outside the continuous phase sequence also require persistence before they begin. The continuation exception does not waive these gates, existing authorization boundaries, or the retention and completion requirements.

Adapted from Matt Pocock's [`ask-matt/PHASE-BOUNDARIES.md`](https://github.com/mattpocock/skills/blob/49dd158/engineering/ask-matt/PHASE-BOUNDARIES.md). ACS requires both answers to be yes and retains mandatory transfer and review persistence; it does not adopt upstream host commands or token thresholds.

## Human review and presentation

When human reading benefits from a view, invoke [Presenter](../protocols/presenter.md) as a responsibility of the active agent: pass canonical references/revisions and the reading or decision focus. Domain owners provide meaning; Presenter provides layout. A view is optional in a handoff and cannot be its only evidence.

Reconcile feedback using the Presenter review sequence: identify reviewed subject/version/scope and actual source, preserve exact reviewed content, deduplicate against current records, serialize writes, and route content changes to their owner. Preserve existing authorization; a view introduces no new approval requirement. Update only materially affected freshness, and retain visual snapshots when their presentation influenced the decision.

## Optional capability selection

For design slots, use the capability signatures in [the UX guide](../resources/skills-src/design/ux/README.md). Probe only slots requested by the stage, reuse previous choices, and prefer the native path when nothing suitable is available. Record `none`, `declined`, or `accepted` once per slot in `<work-root>/<effort>/design/capabilities.md`, with the capability and reconciliation constraints. This is Working Memory. The coordinator owns discovery, availability checks, user choices when needed, runtime calls, and this shared record; the domain skill owns interpretation and validation of the result. A missing optional slot never blocks native work.

## Authorization

**Approval semantics.** Existing task authorization and recorded decisions persist. Ask only for missing decisions or actions beyond that authorization; do not repeat settled approvals. Approval belongs at the existing workflow or action gate, not mid-build during already authorized work. Complete authorized preparation before that gate so the decision has reviewable scope and evidence; a newly discovered missing decision or authority stops the affected action before it proceeds. Preserve the decision's scope and reference in the single recovery entry.

Use a verified approval hook at that gate when available. Without one, explicitly pause for the required decision through an available interaction channel; a manual pause is not executable enforcement, and missing required enforcement is a blocker. Hook availability neither adds approval requirements nor grants authority. No workflow automatically authorizes sending messages, installing dependencies, committing, publishing, or deploying.
