/* Astro Science — Dark/Light Theme Toggle */
(function () {
  "use strict";

  const STORAGE_KEY = "astro-theme";
  const DARK = "dark";
  const LIGHT = "light";

  function getPreferred() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored === DARK || stored === LIGHT) return stored;
    return window.matchMedia("(prefers-color-scheme: light)").matches ? LIGHT : DARK;
  }

  function apply(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem(STORAGE_KEY, theme);
    const btn = document.querySelector("[data-theme-toggle]");
    if (btn) {
      btn.setAttribute("aria-label", theme === DARK ? "Switch to light mode" : "Switch to dark mode");
      btn.innerHTML = theme === DARK
        ? '<svg class="icon icon--md" aria-hidden="true"><use href="icons.svg#icon-sun"/></svg>'
        : '<svg class="icon icon--md" aria-hidden="true"><use href="icons.svg#icon-moon"/></svg>';
    }
  }

  // Apply on load
  apply(getPreferred());

  // Toggle button
  document.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-theme-toggle]");
    if (btn) {
      const current = document.documentElement.getAttribute("data-theme") || DARK;
      apply(current === DARK ? LIGHT : DARK);
    }
  });

  // Listen for system preference changes
  window.matchMedia("(prefers-color-scheme: light)").addEventListener("change", (e) => {
    if (!localStorage.getItem(STORAGE_KEY)) {
      apply(e.matches ? LIGHT : DARK);
    }
  });
})();
CSS