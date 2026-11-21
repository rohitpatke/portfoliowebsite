# Effect modules

This folder is empty on purpose. It holds optional, heavier animations (Lottie, GSAP,
Three.js) that load only on pages that ask for them.

## How loading works

`../motion.js` looks for elements with a `data-effect` attribute:

```html
<figure class="teaser" data-effect="lottie" data-project="clinical-entity-recognition">
  <!-- static fallback content, shown until the effect is ready (and forever if it fails) -->
</figure>
```

When such an element comes within 200px of the viewport, `motion.js` runs
`import("./effects/<name>.js")` and calls the module's default export with the element.
The element gets `data-effect-state="loading"`, then `"ready"` or `"failed"`.

Nothing loads when the visitor has `prefers-reduced-motion: reduce`.

Allowed names are `lottie`, `gsap` and `three` (the `hero_effect` values accepted in project
frontmatter and the `KNOWN_EFFECTS` set in `motion.js`). To add a different name, update both.

## Writing an effect module

Create `<name>.js` in this folder and export one default function:

```js
// effects/gsap.js
export default async function mount(element) {
  const { gsap } = await import("https://cdn.jsdelivr.net/npm/gsap@3.12.7/+esm");
  gsap.from(element.querySelectorAll(".teaser__bar"), {
    scaleY: 0,
    transformOrigin: "bottom",
    stagger: 0.08,
    duration: 0.8,
    ease: "power3.out",
  });
}
```

Rules of thumb:

- Load the library inside the function with `import()`, pinned to an exact version, so pages
  without the effect never download it.
- Keep the element's static content as the fallback. Replace or hide it only once the effect
  is ready.
- Throw (or let errors propagate) on failure. `motion.js` catches the error, logs a warning
  and leaves the fallback in place.
- Resolve asset paths relative to the module (`new URL("../../lottie/x.json", import.meta.url)`)
  so the site works under a URL prefix, such as a GitHub Pages project site.

For a Lottie teaser: save the JSON as `static/lottie/<project-slug>.json`, create
`effects/lottie.js` like the sketch below, then set `hero_effect: lottie` in the project's
frontmatter.

```js
export default async function mount(element) {
  const { default: lottie } = await import("https://cdn.jsdelivr.net/npm/lottie-web@5.12.2/+esm");
  const animation = lottie.loadAnimation({
    container: element.querySelector(".teaser__canvas"),
    renderer: "svg",
    path: new URL(`../../lottie/${element.dataset.project}.json`, import.meta.url).href,
  });
  await new Promise((resolve) => animation.addEventListener("DOMLoaded", resolve));
  element.querySelectorAll(".teaser__bar").forEach((bar) => bar.remove());
}
```
