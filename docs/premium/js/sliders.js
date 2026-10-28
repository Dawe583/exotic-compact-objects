/* Astro Science — Interactive Parameter Sliders */
(function () {
  "use strict";

  /* ---- Kerr ISCO Explorer ---- */
  function kerrIsco(a) {
    // Bardeen-Press-Teukolsky ISCO radius in units of M
    const Z1 = 1 + Math.cbrt(1 - a * a) * (Math.cbrt(1 + a) + Math.cbrt(1 - a));
    const Z2 = Math.sqrt(3 * a * a + Z1 * Z1);
    const inner = (3 - Z1) * (3 + Z1 + 2 * Z2);
    const disc = Math.sqrt(Math.max(inner, 0));
    const geo = 3 + Z2 - disc; // prograde (minus)
    return geo;
  }

  function initKerrSlider() {
    const slider = document.getElementById("kerr-spin-slider");
    const valueDisplay = document.getElementById("kerr-spin-value");
    const iscoDisplay = document.getElementById("kerr-isco-value");
    const plotContainer = document.getElementById("kerr-isco-plot");
    if (!slider) return;

    function update() {
      const a = parseFloat(slider.value);
      const r = kerrIsco(a);
      if (valueDisplay) valueDisplay.textContent = a.toFixed(3);
      if (iscoDisplay) iscoDisplay.textContent = r.toFixed(3) + " M";
      if (plotContainer) {
        plotContainer.innerHTML = `
          <div style="text-align:center;padding:12px">
            <div style="font-family:var(--mono);font-size:.85rem;color:var(--muted)">
              Spin a/M = <b style="color:var(--emerald)">${a.toFixed(3)}</b>
            </div>
            <div style="font-family:var(--mono);font-size:.85rem;color:var(--muted)">
              ISCO radius = <b style="color:var(--sky)">${r.toFixed(3)} M</b>
            </div>
            <div style="margin-top:8px;height:8px;background:var(--line);border-radius:4px;overflow:hidden">
              <div style="width:${(r / 6) * 100}%;height:100%;background:linear-gradient(90deg,var(--emerald),var(--sky));border-radius:4px;transition:width .2s"></div>
            </div>
            <div style="font-family:var(--mono);font-size:.7rem;color:var(--dim);margin-top:4px">
              0 M (extremal) ─────────────── 6 M (Schwarzschild)
            </div>
          </div>`;
      }
    }
    slider.addEventListener("input", update);
    update();
  }

  /* ---- Penrose Efficiency Explorer ---- */
  function penroseEff(a) {
    if (a <= 0) return 0;
    return (Math.sqrt(2) * Math.sqrt(1 - Math.sqrt(1 - a * a)) - a) / (2 * a);
  }

  function initPenroseSlider() {
    const slider = document.getElementById("penrose-spin-slider");
    const valueDisplay = document.getElementById("penrose-spin-value");
    const effDisplay = document.getElementById("penrose-eff-value");
    const totalDisplay = document.getElementById("penrose-total-value");
    const plotContainer = document.getElementById("penrose-plot");
    if (!slider) return;

    function update() {
      const a = parseFloat(slider.value);
      const eta = penroseEff(a);
      const total = 1 - 1 / Math.sqrt(2) * (1 - a); // approximate total reservoir
      if (valueDisplay) valueDisplay.textContent = a.toFixed(3);
      if (effDisplay) effDisplay.textContent = (eta * 100).toFixed(2) + "%";
      if (totalDisplay) totalDisplay.textContent = (total * 100).toFixed(2) + "%";
      if (plotContainer) {
        plotContainer.innerHTML = `
          <div style="text-align:center;padding:12px">
            <div style="font-family:var(--mono);font-size:.85rem;color:var(--muted)">
              Spin a/M = <b style="color:var(--emerald)">${a.toFixed(3)}</b>
            </div>
            <div style="font-family:var(--mono);font-size:.85rem;color:var(--muted)">
              Single-decay η = <b style="color:var(--sky)">${(eta * 100).toFixed(2)}%</b>
            </div>
            <div style="font-family:var(--mono);font-size:.85rem;color:var(--muted)">
              Total reservoir ≈ <b style="color:var(--violet)">${(total * 100).toFixed(2)}%</b>
            </div>
            <div style="margin-top:8px;height:8px;background:var(--line);border-radius:4px;overflow:hidden">
              <div style="width:${eta * 100 * 4.8}%;height:100%;background:linear-gradient(90deg,var(--sky),var(--violet));border-radius:4px;transition:width .2s"></div>
            </div>
            <div style="font-family:var(--mono);font-size:.7rem;color:var(--dim);margin-top:4px">
              0% ─────────────── 20.7% (max single-decay)
            </div>
          </div>`;
      }
    }
    slider.addEventListener("input", update);
    update();
  }

  /* ---- Hawking Temperature Explorer ---- */
  function hawkingTemp(massMsun) {
    const hbar = 1.054571817e-34;
    const c = 2.99792458e8;
    const G = 6.67430e-11;
    const kB = 1.380649e-23;
    const Msun = 1.98847e30;
    const M = massMsun * Msun;
    return (hbar * c ** 3) / (8 * Math.PI * G * M * kB);
  }

  function initHawkingSlider() {
    const slider = document.getElementById("hawking-mass-slider");
    const valueDisplay = document.getElementById("hawking-mass-value");
    const tempDisplay = document.getElementById("hawking-temp-value");
    if (!slider) return;

    function update() {
      const m = parseFloat(slider.value);
      const T = hawkingTemp(m);
      if (valueDisplay) valueDisplay.textContent = m.toExponential(2) + " M☉";
      if (tempDisplay) tempDisplay.textContent = T.toExponential(2) + " K";
    }
    slider.addEventListener("input", update);
    update();
  }

  /* ---- Init all ---- */
  function init() {
    initKerrSlider();
    initPenroseSlider();
    initHawkingSlider();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
CSS