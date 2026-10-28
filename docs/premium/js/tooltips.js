/* Astro Science — Tooltip System */
(function () {
  "use strict";

  const tooltip = document.createElement("div");
  tooltip.className = "tooltip-popup";
  tooltip.style.cssText = "position:fixed;z-index:300;background:var(--surface-2);border:1px solid var(--line-strong);border-radius:var(--radius-sm);padding:8px 12px;font-size:.82rem;max-width:280px;pointer-events:none;opacity:0;transition:opacity .15s ease;box-shadow:var(--shadow-md);color:var(--text);font-family:var(--serif);line-height:1.5";
  document.body.appendChild(tooltip);

  let hideTimer = null;

  function show(target) {
    const text = target.getAttribute("data-tooltip");
    if (!text) return;
    tooltip.textContent = text;
    const rect = target.getBoundingClientRect();
    tooltip.style.left = (rect.left + rect.width / 2) + "px";
    tooltip.style.top = (rect.top - 8) + "px";
    tooltip.style.transform = "translate(-50%, -100%)";
    tooltip.style.opacity = "1";
    clearTimeout(hideTimer);
  }

  function hide() {
    hideTimer = setTimeout(() => { tooltip.style.opacity = "0"; }, 100);
  }

  document.addEventListener("mouseover", (e) => {
    const target = e.target.closest("[data-tooltip]");
    if (target) show(target);
  });
  document.addEventListener("mouseout", (e) => {
    const target = e.target.closest("[data-tooltip]");
    if (target) hide();
  });
  document.addEventListener("focusin", (e) => {
    const target = e.target.closest("[data-tooltip]");
    if (target) show(target);
  });
  document.addEventListener("focusout", (e) => {
    const target = e.target.closest("[data-tooltip]");
    if (target) hide();
  });
})();
CSS