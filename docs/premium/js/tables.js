/* Astro Science — Sortable, Filterable Data Tables */
(function () {
  "use strict";

  function initTable(table) {
    const tbody = table.querySelector("tbody");
    if (!tbody) return;
    const headers = Array.from(table.querySelectorAll("thead th"));
    const rows = Array.from(tbody.querySelectorAll("tr"));

    // Sort
    headers.forEach((th, colIdx) => {
      th.style.cursor = "pointer";
      th.addEventListener("click", () => {
        const asc = !th.classList.contains("sort-asc");
        headers.forEach((h) => h.classList.remove("sort-asc", "sort-desc"));
        th.classList.add(asc ? "sort-asc" : "sort-desc");
        rows.sort((a, b) => {
          const aVal = a.cells[colIdx]?.textContent.trim() || "";
          const bVal = b.cells[colIdx]?.textContent.trim() || "";
          const aNum = parseFloat(aVal);
          const bNum = parseFloat(bVal);
          if (!isNaN(aNum) && !isNaN(bNum)) {
            return asc ? aNum - bNum : bNum - aNum;
          }
          return asc ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
        });
        rows.forEach((r) => tbody.appendChild(r));
      });
    });

    // Search/filter
    const searchInput = table.parentElement?.querySelector("[data-table-search]");
    if (searchInput) {
      searchInput.addEventListener("input", (e) => {
        const q = e.target.value.toLowerCase();
        rows.forEach((r) => {
          const text = r.textContent.toLowerCase();
          r.style.display = text.includes(q) ? "" : "none";
        });
      });
    }
  }

  function init() {
    document.querySelectorAll("table[data-sortable]").forEach(initTable);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
CSS