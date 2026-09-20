# UI Prototype

Last updated: 2026-09-08

Several structurally different renderings of one surface, switchable in the browser. The user flips through, picks one or takes pieces from each, and the rest is discarded.

Wrong branch if the question is about behavior or state. See [LOGIC.md](LOGIC.md).

## Signals this is the right shape

- The layout of a page is undecided and argument has not settled it.
- A few options need to exist side by side before one can be committed to.
- The alternative is the user holding three vague mockups in their head for a day.

## Where the variants live

**Sub-shape A — inside an existing page. This is the default.**

A layout is only judgeable against the rest of the app: real header, real sidebar, real data, real density. On an empty route every variant looks fine, which is exactly the failure this shape avoids. Variants render on the existing route, gated by `?variant=`; data fetching, params, and auth stay untouched — only the rendered subtree swaps.

Something that has no page yet but would naturally live inside one — a new dashboard section, a settings card, a step in an existing flow — is still sub-shape A. Mount the variants in the host page.

**Sub-shape B — a new throwaway route. Last resort.**

Only when there is genuinely no page to embed in: a new top-level surface, or a flow that cannot sit anywhere sensible. Follow the project's existing routing convention, put `prototype` in the path, use the same `?variant=` pattern.

Before choosing B, check again for a host page. An empty route hides the problems a populated one would expose.

## Process

### 1. Fix the question and the count

Three variants by default. Past five they stop being alternatives and become noise — cap there. State the plan in one line at the top of the file:

> Three variants of the settings page, `?variant=`, on the existing `/settings` route.

### 2. Draft variants that actually disagree

Each variant answers to the page's purpose and the data it can reach, and uses the project's existing component and styling system. Export a clear name per variant.

They must differ **structurally** — layout, information hierarchy, primary affordance. Three retuned card grids is wallpaper, not a prototype. If two drafts converge, redo one under an explicit prohibition ("no card grid").

### 3. Wire the switch

One switcher on the route selects by search param:

```tsx
// adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

Sub-shape A keeps all existing data fetching above the switcher. Sub-shape B mounts the same switcher on the throwaway route.

### 4. Build the floating bar

Fixed at bottom-center: left arrow, current variant label (key plus name if the variant exports one — `B — Sidebar layout`), right arrow. Both arrows wrap.

- Arrows update the search param through the project's router, so a variant is shareable and survives reload.
- `<-` and `->` cycle too, except while an `<input>`, `<textarea>`, or `[contenteditable]` has focus.
- Visually unmistakable as not-the-design — high-contrast pill, clear shadow.
- Gated out of production builds, so a stray merge cannot ship it.

One shared component, reused by both sub-shapes, living wherever shared UI lives.

### 5. Hand it over

Give the URL and the variant keys. The most useful reply is usually "the header from B with the sidebar from C" — that is the design, arrived at by comparison.

### 6. Capture and clean up

Capture the answer as [SKILL.md](../SKILL.md) describes, then fold the winner into real code:

- **Sub-shape A** — winner merges into the existing page; losing variants and the switcher leave main.
- **Sub-shape B** — winner is promoted to a real route; the throwaway route and switcher leave main.

The full variant set is the primary source, so it lands on the throwaway branch rather than the bin. Variants left in main rot and mislead the next reader.

## Anti-patterns

- **Differing only in color or copy.** Real variants disagree about structure.
- **Sharing a layout between variants.** A shared header is fine; a shared layout defeats the exercise. Each variant may throw out the structure.
- **Real mutations.** Read-only is fine; point writes at stubs. The question is what it should look like, not whether the backend works.
- **Promoting prototype code as-is.** It was written with no tests and minimal error handling. Rewrite when folding in.
