// Homepage filter pills: [data-filter] buttons show/hide cards by [data-type].

const LABELS = { academic: "research", professional: "professional" };

function initFilters() {
  const group = document.querySelector("[data-filters]");
  const grid = document.querySelector("[data-filter-grid]");
  if (!group || !grid) return;

  const buttons = [...group.querySelectorAll("[data-filter]")];
  const cards = [...grid.querySelectorAll("[data-type]")];
  const status = document.querySelector("[data-filter-status]");

  function apply(filter) {
    let shown = 0;
    for (const button of buttons) {
      button.setAttribute("aria-pressed", String(button.dataset.filter === filter));
    }
    for (const card of cards) {
      const match = filter === "all" || card.dataset.type === filter;
      card.hidden = !match;
      if (match) shown += 1;
    }
    if (status) {
      const kind = LABELS[filter] ? `${LABELS[filter]} ` : "";
      status.textContent = `Showing ${shown} ${kind}project${shown === 1 ? "" : "s"}.`;
    }
  }

  group.addEventListener("click", (event) => {
    const button = event.target.closest("[data-filter]");
    if (button) apply(button.dataset.filter);
  });

  // The pills are hidden in the HTML so they never appear without working JS.
  group.hidden = false;
}

initFilters();
