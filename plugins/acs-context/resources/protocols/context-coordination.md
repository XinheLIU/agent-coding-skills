---
protocol: acs:context-coordination
version: 1.1.0
status: stable
canonical: https://github.com/XinheLIU/agent-coding-skills/blob/main/system/protocols/context-coordination.md
---

# Context Coordination

Last updated: 2026-09-25

The active agent performs this coordinator role under the [shared protocol](../../skills/acs-init-context/references/PROTOCOL.md), including when invoking a skill standalone. This is a written Harness contract, not a new executable service. Domain skills return results and proposed transitions; the coordinator applies shared state changes through capabilities actually available in the session.

The [harness architecture](../docs/harness-architecture.md) defines source identity, standalone packaging, and the boundary with Codex, Claude Code, Pi, OpenCode, and DeepSeek harness adapters. Keep domain procedures and shared state semantics here; put host APIs, invocation syntax, worker executables, and lifecycle integrations in their binding. A plugin manifest alone does not establish runtime support.

## Assemble only the needed context

1. Resolve canonical change/task identity and paths by the protocol's precedence. Keep the established tracker; for new local changes use tracked `docs/changes/<change-id>/`, with scratch in the configured work root.
2. Read canonical ticket status and the active run's single configured recovery entry. Follow the chosen skill's `context.requires` and relevant `retrieves` selectors. Product HTML: read navigation, then only the relevant articles and their premises; do not load every domain contract.
3. Supply references, consumed revisions, scope, relevant constraints, and known review findings. Resolve missing answers from existing artifacts before asking. An inaccessible source is transported as a bounded temporary excerpt with its source revision; never create another normative spec.
4. Bind requests to tools, skills, agents, shell commands, or direct work that actually exist. A named consumer is not a dispatch instruction. If a capability is absent, perform the stage directly when competent, or report the concrete missing capability and its blocking effect.

## Schedule and reconcile

Implementation proposes slices, dependency edges, and shared-write risks. The coordinator schedules the unblocked frontier only when delegation is available and authorized. Disjoint filenames alone do not prove independence: check shared contracts, generated outputs, configuration, migrations, and tests.

Use the protocol's exclusive claims and serialized writer. Check the target and premise revisions immediately before applying a contribution; a changed revision requires reconciliation. A stale claim request loses to the current claim and returns a conflict, never an overwrite. Without atomic claims or a single writer, work serially. Keep ticket progress in its canonical tracker; claims and scratch steps do not mirror it as another source.

Preserve contribution ownership. Reconcile by stable subject/record IDs; repeat submissions with unchanged evidence are no-ops. Conflicting assessments remain visible until their owner resolves them. Skill output may propose changes to another domain, but does not authorize them.

## Transition and verification

On a meaningful transition, update the single configured Working recovery entry with the next action, blockers, canonical status link, changed anchors, and consumed revisions. Append a concise progress entry. Apply freshness propagation from the protocol, routing reassessment to each domain owner. Regenerate only affected derived views.

Testing owns evidence interpretation. The coordinator records its exact code/diff revision, criteria, commands, environment/configuration assumptions, failures, skipped/not-run checks, and omissions in compact Persistent Changes. A high pass percentage or completed checklist cannot establish readiness over missing criteria. A changed artifact or environment cannot inherit a previous verification verdict without reassessment.

Use the common handoff envelope for every domain or session transfer. Transfer claims explicitly. Before formal review or downstream reliance, save necessary proposals and evidence in Persistent Memory; `proposed` is a valid durable status. At completion follow the protocol's retention gate; verify durable links with the run directory unavailable before removing reconciled scratch. Do not delete accepted requirements, design rationale, or final verification.

## Human review and presentation

When human reading benefits from a view, invoke [Presenter](presenter.md) as a responsibility of the active agent: pass canonical references/revisions and the reading or decision focus. Domain owners provide meaning; Presenter provides layout. A view is optional in a handoff and cannot be its only evidence.

Reconcile feedback using the Presenter review sequence: identify reviewed subject/version/scope and actual source, preserve exact reviewed content, deduplicate against current records, serialize writes, and route content changes to their owner. Preserve existing authorization; a view introduces no new approval requirement. Update only materially affected freshness, and retain visual snapshots when their presentation influenced the decision.

## Optional capability selection

For design slots, use the capability signatures in [the UX guide](../skills-src/design/ux/README.md). Probe only slots requested by the stage, reuse previous choices, and prefer the native path when nothing suitable is available. Record `none`, `declined`, or `accepted` once per slot in `<work-root>/<effort>/design/capabilities.md`, with the capability and reconciliation constraints. This is Working Memory. The coordinator owns discovery, availability checks, user choices when needed, runtime calls, and this shared record; the domain skill owns interpretation and validation of the result. A missing optional slot never blocks native work.

## Authorization

Existing task authorization and recorded decisions persist. Ask only for missing decisions or actions beyond that authorization; do not repeat settled approvals. No workflow automatically authorizes sending messages, installing dependencies, committing, publishing, or deploying.
