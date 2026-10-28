/* Astro Science — Toast Notifications */
(function () {
  "use strict";

  const container = document.createElement("div");
  container.style.cssText = "position:fixed;bottom:24px;right:24px;z-index:200;display:flex;flex-direction:column;gap:8px;pointer-events:none";
  document.body.appendChild(container);

  const COLORS = {
    success: "var(--emerald)",
    warning: "var(--amber)",
    error: "var(--rose)",
    info: "var(--sky)",
  };

  window.showToast = function (message, type, duration) {
    type = type || "info";
    duration = duration || 4000;
    const toast = document.createElement("div");
    toast.style.cssText = `pointer-events:auto;padding:12px 18px;border-radius:var(--radius-sm);background:var(--surface-2);border:1px solid var(--line-strong);border-left:3px solid ${COLORS[type] || COLORS.info};color:var(--text);font-family:var(--mono);font-size:.82rem;box-shadow:var(--shadow-md);opacity:0;transform:translateX(20px);transition:opacity .2s ease,transform .2s ease;max-width:360px`;
    toast.textContent = message;
    container.appendChild(toast);
    requestAnimationFrame(() => {
      toast.style.opacity = "1";
      toast.style.transform = "translateX(0)";
    });
    setTimeout(() => {
      toast.style.opacity = "0";
      toast.style.transform = "translateX(20px)";
      setTimeout(() => toast.remove(), 200);
    }, duration);
  };
})();
CSS