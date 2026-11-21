/**
 * Motion levels 2 and 3 (level 1 is CSS-only, in motion.css).
 *
 * Level 2, scroll reveal: adds `.is-visible` to `[data-animate]` elements as they enter
 *   the viewport. Templates stagger siblings with `style="--delay: N"`.
 * Level 3, effect loader: `[data-effect="lottie|gsap|three"]` lazily imports
 *   `./effects/<name>.js` when the element nears the viewport and calls its default export
 *   with the element. See effects/README.md.
 *
 * With prefers-reduced-motion: reduce, everything is shown at once and no effects load.
 */

const root = document.documentElement;
// Re-assert .js (the inline fallback in base.html may have removed it on a slow load)
// and signal that the reveal script is running.
root.classList.add("js", "motion-ready");

const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
const KNOWN_EFFECTS = new Set(["lottie", "gsap", "three"]);

function initReveal() {
  const targets = document.querySelectorAll("[data-animate]");
  if (reducedMotion.matches || !("IntersectionObserver" in window)) {
    targets.forEach((element) => element.classList.add("is-visible"));
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0 },
  );
  targets.forEach((element) => observer.observe(element));
}

async function mountEffect(element) {
  const name = element.dataset.effect;
  if (!KNOWN_EFFECTS.has(name)) {
    console.warn(`[motion] Unknown effect "${name}"`);
    return;
  }
  element.dataset.effectState = "loading";
  try {
    // Resolved relative to this file, so it works under any URL prefix.
    const module = await import(new URL(`./effects/${name}.js`, import.meta.url).href);
    await module.default(element);
    element.dataset.effectState = "ready";
  } catch (error) {
    // The static fallback inside the element stays visible.
    element.dataset.effectState = "failed";
    console.warn(`[motion] Effect "${name}" could not be loaded`, error);
  }
}

function initEffects() {
  const hosts = document.querySelectorAll("[data-effect]");
  if (hosts.length === 0 || reducedMotion.matches) return;
  if (!("IntersectionObserver" in window)) {
    hosts.forEach(mountEffect);
    return;
  }

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        observer.unobserve(entry.target);
        mountEffect(entry.target);
      }
    },
    { rootMargin: "200px 0px" },
  );
  hosts.forEach((element) => observer.observe(element));
}

initReveal();
initEffects();
