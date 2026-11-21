// Scroll reveal for [data-animate] and lazy loader for [data-effect] modules (effects/README.md).

const root = document.documentElement;
// Re-add .js (base.html removes it if this script is slow) and mark the script as running.
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
    const module = await import(new URL(`./effects/${name}.js`, import.meta.url).href);
    await module.default(element);
    element.dataset.effectState = "ready";
  } catch (error) {
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
