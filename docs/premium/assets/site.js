/* Astro Science — site interactions (no dependencies) */
(function () {
  "use strict";

  /* ---- mobile navigation ---- */
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", () => {
      const open = nav.classList.toggle("open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    nav.addEventListener("click", (e) => {
      if (e.target.tagName === "A") nav.classList.remove("open");
    });
  }

  /* ---- mark current page in nav ---- */
  const here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll("#site-nav a").forEach((a) => {
    const href = (a.getAttribute("href") || "").split("/").pop();
    if (href === here) a.setAttribute("aria-current", "page");
  });

  /* ---- table of contents for long prose pages ---- */
  const prose = document.querySelector(".prose");
  const toc = document.getElementById("toc");
  if (prose && toc) {
    const heads = Array.from(prose.querySelectorAll("h2, h3")).filter(
      (h) => (h.textContent || "").trim().length > 0
    );
    if (heads.length >= 3) {
      const frag = document.createDocumentFragment();
      const title = document.createElement("div");
      title.className = "toc-title";
      title.textContent = "On this page";
      frag.appendChild(title);

      const links = [];
      heads.forEach((h, i) => {
        if (!h.id) {
          h.id = "sec-" + i + "-" + (h.textContent || "")
            .toLowerCase()
            .replace(/[^a-z0-9]+/g, "-")
            .replace(/^-+|-+$/g, "")
            .slice(0, 48);
        }
        const a = document.createElement("a");
        a.href = "#" + h.id;
        a.textContent = h.textContent.trim();
        if (h.tagName === "H3") a.className = "h3";
        frag.appendChild(a);
        links.push({ a, h });
      });

      // reading progress indicator
      const bar = document.createElement("div");
      bar.style.cssText =
        "height:2px;background:linear-gradient(90deg,#2fe3ac,#a48bff);width:0;margin-bottom:14px;border-radius:2px;transition:width .1s linear";
      toc.appendChild(bar);
      toc.appendChild(frag);

      const onScroll = () => {
        const st = window.scrollY || document.documentElement.scrollTop;
        const h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? Math.min(100, (st / h) * 100) : 0) + "%";

        let active = null;
        for (const { h } of links) {
          if (h.getBoundingClientRect().top - 110 <= 0) active = h;
          else break;
        }
        links.forEach(({ a, h }) => a.classList.toggle("active", h === active));
      };
      let ticking = false;
      window.addEventListener("scroll", () => {
        if (!ticking) {
          ticking = true;
          requestAnimationFrame(() => { onScroll(); ticking = false; });
        }
      }, { passive: true });
      onScroll();
    }
  }

  /* ---- lazy loading for heavy Plotly iframes ---- */
  const lazy = document.querySelectorAll("iframe[data-src]");
  if (lazy.length) {
    const load = (el) => {
      if (!el.src) el.src = el.getAttribute("data-src");
      el.removeAttribute("data-src");
    };
    if ("IntersectionObserver" in window) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => {
          if (en.isIntersecting) { load(en.target); io.unobserve(en.target); }
        });
      }, { rootMargin: "300px 0px" });
      lazy.forEach((el) => io.observe(el));
    } else {
      lazy.forEach(load);
    }
  }

  /* ---- reveal-on-scroll intentionally removed: content is always visible,
         so nothing depends on scroll choreography to become readable ---- */

  /* ---- external links open in new tab ---- */
  document.querySelectorAll("a[href^='http']").forEach((a) => {
    if (a.hostname && a.hostname !== location.hostname) {
      a.target = "_blank";
      a.rel = "noopener noreferrer";
    }
  });

  /* ---- copy link buttons (anchors) ---- */
  document.querySelectorAll("[data-copy]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(location.href);
        const old = btn.textContent;
        btn.textContent = "Copied";
        setTimeout(() => (btn.textContent = old), 1400);
      } catch (e) { /* ignore */ }
    });
  });
})();
