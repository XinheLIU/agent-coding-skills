---
name: acs-design-system-create
description: Use when a product needs visual style or a design system and has no DESIGN.md or reference brand to adopt.
---

Last updated: 2026-10-23

## Context contract

```yaml
context:
  requires: [product.relevant_context]
  retrieves: [design.existing_authority, operations.constraints]
  produces: [design.tokens, design.rationale]
  updates: [design.applicable_rules, design.accepted_decisions]
  invalidates: [design.token_dependents]
  handoff_to: [interaction_design, visual_design]
```

[Shared semantics](../../../../docs/shared-semantics.md#execution)

# Design System Creation

## Procedure

0. Use coordinator paths/identity, never newest effort/first product. Existing DESIGN.md: summarize, ask validate/use (stop), update (pre-fill), replace (authorized). Legacy `docs/design/system.md` without DESIGN.md → `acs-design-context` migration. Offer fitting reference adoption there only on approval.
1. Read configured persona/problem/platform (canonical legacy PRD allowed), CONTEXT.md/README. One coordinator question with sourced defaults for gaps: purpose/persona/platform/category/memorable quality/direction.
2. Propose product-grounded aesthetic, ONE heading/body pairing/fallbacks, 16px type scale (1.25/1.333), sizes/weights, line heights (body 1.5–1.75/headings 1.2–1.4), semantic palette/spacing/layout/radii/components. Optional type/color sources are cited; native fallback remains.
3. Self-contained inline-style `system-preview.html` in `<work-root>/<effort>/design/` (no effort: `<work-root>/design/`): h1–h4/body/small, hex swatches, spacing ruler, button variants/states, form default/focus/error, card.
4. Before formal review persist exact proposal/revision/preview/assets per [design memory](references/design-memory.md); bind feedback. Present rationale/rendered preview via coordinator: approve/adjust/restart. Adjust ≤3 iterations; restart at context.
5. On approval write root DESIGN.md: YAML tokens; prose judgment/usage/contrast, no duplicate values. [Example](references/output-examples.md#example-1), [specification](references/system-specification.md): type/palette/spacing/layout/radii/components/a11y/References provenance. Sync existing prototype `:root` from frontmatter via `acs-design-context` Step 4.
6. Return DESIGN.md, decision IDs/references/rationale/alternatives, requirement/token/contract revisions, surfaces/delta/blockers/next action. Structure → `acs-design-interaction-flow`; visuals → `acs-visual-design-variants`; implementation → `acs-design-implement`. Engineering constraints → ADR; taste stays DESIGN.md. Retain review evidence before reconciled cleanup.

## Completion criteria and hard rules

- No writing/replacing design authority before approval. Current authority is reused; migration and reference adoption belong to `acs-design-context`.
- Ban Papyrus, Comic Sans, Lobster, Impact, Jokerman. Inter, Roboto, Poppins and system-ui need strong justification. Test type readability at all sizes; fonts and aesthetic must fit product needs.
- ONE decisive accent with hover/active states; only 2–3 surface levels. Include page/raised/overlay surfaces, primary/secondary/tertiary text, success/warning/error/info and default/subtle border tokens. Validate ALL text/background pairs: WCAG AA 4.5:1 normal, 3:1 large (18pt+).
- Use a geometric spacing scale, flex as primary layout, grid only for 2D content. Specify widths, 640/768/1024/1280 breakpoints and small/medium/large/full radii. Define patterns, not production components.
- Buttons: primary/secondary/ghost; default/hover/active/disabled/loading. Forms: default/focus/error/disabled, explicit labels (not placeholders alone), specific error text below field. Cards: padding/border/shadow; interactive cards have hover, static cards do not. Touch targets at least 44×44px; visible 3px focus outlines; semantic HTML.
- DESIGN.md has tokens AND prose plus provenance. Preview and re-synced prototype need `generated`/`source-revision` matching visible date/revision; run the [HTML validator](../../../authoring/scripts/validate-report-html.py) with `--version-only` and fix errors.
- DESIGN.md is canonical authority; preview is exploration, but exact reviewed appearance/assets and accepted decision rationale survive in Persistent Memory. Never discard decision evidence as disposable preview output.

<!-- compaction-core:end -->
