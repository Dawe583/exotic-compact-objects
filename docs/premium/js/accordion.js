/* Astro Science — Accordion / Collapsible Sections */
(function () {
  "use strict";

  function init() {
    document.querySelectorAll("[data-accordion]").forEach((acc) => {
      const header = acc.querySelector("[data-accordion-header]");
      const body = acc.querySelector("[data-accordion-body]");
      if (!header || !body) return;
      body.style.maxHeight = "0";
      body.style.overflow = "hidden";
      body.style.transition = "max-height .3s ease";
      header.style.cursor = "pointer";
      header.addEventListener("click", () => {
        const open = acc.classList.toggle("open");
        body.style.maxHeight = open ? body.scrollHeight + "px" : "0";
        header.setAttribute("aria-expanded", open ? "true" : "false");
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
CSS