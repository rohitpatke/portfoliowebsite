/**
 * Recruiter mode: paste a job description, get the three most relevant projects.
 *
 * Today the matching is client-side keyword search over each project's skills and their
 * aliases (content/site.yaml → skill_aliases). The data comes from the
 * <script type="application/json" id="recruiter-data"> tag rendered by the homepage route.
 *
 * The job description is untrusted input: results are built with DOM methods and
 * textContent only, never innerHTML.
 */

const MIN_LENGTH = 20;
const MAX_RESULTS = 3;

const SAMPLE_JD = `Machine Learning Engineer, Risk

We are looking for an engineer to build and run real-time ML systems. You will design
streaming features on Kafka, deploy models to Kubernetes and run A/B tests to measure
impact. Strong Python and SQL are required; a background in statistics is a plus.`;

function loadProjects() {
  const node = document.getElementById("recruiter-data");
  if (!node) return [];
  try {
    return JSON.parse(node.textContent);
  } catch (error) {
    console.warn("[recruiter] Could not read project data", error);
    return [];
  }
}

const PROJECTS = loadProjects();

function escapeRegExp(text) {
  return text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/** True if `term` appears in `text` as a whole word or phrase ("ml" must not match "html"). */
function mentions(text, term) {
  return new RegExp(`(^|[^a-z0-9])${escapeRegExp(term)}($|[^a-z0-9])`).test(text);
}

/**
 * Return up to three projects that match the job description, best first.
 * Shape: [{ title, type, label, url, evidence, matched: ["Python", ...] }]
 */
export async function findMatches(text) {
  // ── Swap point: AI matcher ──────────────────────────────────────────────────
  // Once POST /api/jd-match is implemented (ENABLE_JD_MATCH=true), replace the keyword
  // matching below with a call that returns the same shape:
  //
  //   const endpoint = document.querySelector("[data-recruiter-form]").dataset.endpoint; // "/api/jd-match"
  //   const response = await fetch(endpoint, {
  //     method: "POST",
  //     headers: { "Content-Type": "application/json" },
  //     body: JSON.stringify({ text }),
  //   });
  //   if (!response.ok) throw new Error(`jd-match failed with status ${response.status}`);
  //   return (await response.json()).matches;
  // ────────────────────────────────────────────────────────────────────────────
  const haystack = text.toLowerCase().replace(/\s+/g, " ");
  return PROJECTS.map(({ title, type, label, url, evidence, skills }) => ({
    title,
    type,
    label,
    url,
    evidence,
    matched: skills
      .filter((skill) => skill.terms.some((term) => mentions(haystack, term)))
      .map((skill) => skill.name),
  }))
    .filter((project) => project.matched.length > 0)
    .sort((a, b) => b.matched.length - a.matched.length) // stable: ties keep site order
    .slice(0, MAX_RESULTS);
}

function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function renderMatches(container, matches) {
  if (matches.length === 0) {
    container.replaceChildren(
      element(
        "p",
        "results__empty",
        "No clear overlap with my projects yet. Try pasting the full description, including the requirements.",
      ),
    );
    return;
  }

  const heading = element("h4", "results__heading", matches.length === 1 ? "Best match" : `Top ${matches.length} matches`);
  const list = element("ol", "matches");
  list.setAttribute("role", "list");

  for (const match of matches) {
    const item = element("li", `match track--${match.type}`);

    const header = element("div", "match__header");
    const link = element("a", "match__title", match.title);
    link.href = match.url;
    const badge = element("span", "match__badge");
    const dot = element("span", "track-dot");
    dot.setAttribute("aria-hidden", "true");
    badge.append(dot, match.label);
    header.append(link, badge);

    const skills = element("ul", "tags");
    skills.setAttribute("role", "list");
    skills.setAttribute("aria-label", "Matching skills");
    for (const name of match.matched) skills.append(element("li", "tag tag--match", name));

    item.append(header, element("p", "match__evidence", match.evidence), skills);
    list.append(item);
  }
  container.replaceChildren(heading, list);
}

function initRecruiter() {
  const form = document.querySelector("[data-recruiter-form]");
  const results = document.querySelector("[data-recruiter-results]");
  if (!form || !results) return;

  const input = form.querySelector("textarea");
  const error = form.querySelector("[data-recruiter-error]");
  const sampleButton = form.querySelector("[data-recruiter-sample]");

  function showError(message) {
    error.textContent = message;
    input.setAttribute("aria-invalid", "true");
  }

  function clearError() {
    error.textContent = "";
    input.removeAttribute("aria-invalid");
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const text = input.value.trim();
    if (text.length < MIN_LENGTH) {
      showError(`Please paste at least ${MIN_LENGTH} characters of the job description (you have ${text.length}).`);
      input.focus();
      return;
    }
    clearError();
    results.setAttribute("aria-busy", "true");
    try {
      renderMatches(results, await findMatches(text));
    } catch (failure) {
      console.error("[recruiter]", failure);
      results.replaceChildren(element("p", "results__empty", "Matching failed. Please try again."));
    } finally {
      results.removeAttribute("aria-busy");
    }
  });

  input.addEventListener("input", () => {
    if (error.textContent && input.value.trim().length >= MIN_LENGTH) clearError();
  });

  sampleButton.addEventListener("click", () => {
    input.value = SAMPLE_JD;
    clearError();
    form.requestSubmit();
  });
}

initRecruiter();
