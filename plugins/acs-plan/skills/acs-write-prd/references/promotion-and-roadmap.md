# Promotion and Roadmap Decomposition

Last updated: 2026-09-26

This is the workflow `acs-write-prd` follows when consolidating durable knowledge into `product.html`. Record semantics, vocabularies, and authority rules live in [the product memory contract](../../../resources/protocols/product-memory.md); this reference sequences the work.

## Promotion

Promote settled product intent with the minimum evidence and rationale needed to understand it. `acs-write-prd` can run early, incrementally, or from explicit standalone inputs. It does not validate demand, invent scope, or turn unresolved analysis into accepted requirements.

Promotion order:

1. Write and verify the durable record and its essential supporting evidence.
2. Repair links among promoted records.
3. Replace working conclusions with pointers; a working amendment ID can become a pointer to the durable record it amended.
4. Update routing.

Durable records must not depend on disposable effort files for essential rationale or evidence. Preserve required observations in the durable evidence record when their only source was working notes; link stable external/code sources where available. Preserve stable IDs when moving records. When amending an existing durable subject, reconcile the accepted amendment into that record rather than creating a duplicate. Link supporting records once; an overview or requirements index links to them rather than repeating their normative text. A consequential prototype decision is retained in summary — verdict, basis, meaningful alternatives, and consumed revisions — when accepted, before implementation or cleanup. Before effort deletion, verify the durable document remains understandable and its necessary links resolve without that effort.

## Readiness gate

Check the `research-coverage` record in `discovery.html` before decomposing research into roadmap tickets:

```html
<section id="research">
  <h2>Research coverage</h2>
  <article id="research-coverage-baseline" data-kind="research-coverage">
    <h3>Coverage and readiness</h3>
    <p>Assessed: web app (all routes), REST API, CLI export. Not assessed: mobile app (&lt;5% MAU per <a href="#evidence-analytics">analytics</a>).</p>
    <p><strong>Ready for roadmap: yes</strong> — all P0 gaps evidenced, primary personas mapped, no blocking questions.</p>
  </article>
</section>
```

When it says not ready, roadmap promotion waits — early promotion of settled records (a Green demand verdict, a confirmed vision) still proceeds. Reassess readiness after conflicting evidence or changed premises; document existence is never a gate. Keep partial readiness explicit: list outstanding questions and what they block.

## Roadmap decomposition

When research is ready, decompose accepted findings into `roadmap-ticket` records:

- Every P0 finding maps to at least one ticket; every ticket links its research basis and its mission/vision alignment.
- Overlap between tickets is reviewed — MECE as judgment, not automation.
- Assign each ticket its type: settled requirements become a **spec ticket** linked to its sole canonical spec; an open design question becomes a **prototype ticket** whose request hands off to `design/ux/prototype`.

## Spec files

A spec file opens with a link back to its roadmap ticket and covers problem, solution, requirements with acceptance criteria, explicit out-of-scope, and success measures for that one change — normative detail lives in the spec; the ticket summarizes status and links. The spec is canonical for its change; the canonical ticket (roadmap article or linked tracker record) owns priority and status.

## PRD navigation

The PRD is a reading order over canonical records, not another maintained document. PRD navigation uses `prd` for the reading index, and anchors to actual records for problem, users, goals, capabilities, scope, acceptance, risks, measures, and launch decisions. The roadmap section is the PRD's forward-looking view; the reading index links it rather than repeating it.
