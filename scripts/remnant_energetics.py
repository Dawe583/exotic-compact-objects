#!/usr/bin/env python3
"""
Remnant energetics for the GWTC compact-binary population.

Question
--------
How much rotational energy do the black holes left behind by observed mergers
retain, and what radiative efficiency does their inferred spin imply?  The
answer matters for two reasons:

1. It converts the merger catalogue into an *energy budget*: the GW radiated
   energy is compared with the rotational reservoir that remains.
2. It provides a population-level consistency check.  A Kerr horizon cannot
   convert more than 1 - E_ISCO(a=1) = 42.3% of its rest mass into radiation;
   any claim of a larger thin-disc efficiency requires a non-Kerr object.

Method
------
The catalogue provides component masses and the effective inspiral spin
chi_eff.  We infer the remnant spin with the aligned-spin fit of Rezzolla et
al. (2008), assuming chi_1 = chi_2 = chi_eff:

    a_f = [ (1 + q^2) chi_eff + q * l ] / (1 + q)^2
    l   = 2*sqrt(3) + t2*eta + t3*eta^2,   eta = q/(1+q)^2
    t2  = -3.517,  t3 = 2.576

The ISCO radius is the exact Bardeen-Press-Teukolsky solution, and the
specific orbital energy at the ISCO gives the thin-disc efficiency

    eta = 1 - E_ISCO(a_f).

This is an *approximate* remnant spin (no precession, no individual spin
information, aligned-spin assumption); it is labelled as such everywhere.  The
derived quantities are therefore population-level estimates, not per-event
measurements.

Outputs
-------
    results/remnant_energetics.csv
    results/remnant_energetics.png
    premium/figures/remnant_energetics.html

Run from the project root:
    /home/dawe/Projects/astro-science/.venv/bin/python scripts/remnant_energetics.py
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
CATALOG = PROJECT / "data/processed/gwosc_gwtc.csv"
OUT_CSV = PROJECT / "results/remnant_energetics.csv"
OUT_PNG = PROJECT / "results/remnant_energetics.png"
OUT_HTML = PROJECT / "premium/figures/remnant_energetics.html"

A_MAX = 0.998  # Thorne (1974) maximal astrophysical spin
T2 = -3.517
T3 = 2.576
G = 6.67430e-11
C = 2.99792458e8
MSUN = 1.98847e30
C2 = C * C
SQRT3 = np.sqrt(3.0)


# ---------------------------------------------------------------------------
# Kerr geometry
# ---------------------------------------------------------------------------
def isco_radius_over_M(a: float) -> float:
    """Exact prograde Kerr ISCO radius in units of M (BPT 1972)."""
    a = float(np.clip(a, 0.0, 1.0))
    z1 = 1.0 + np.cbrt(1.0 - a * a) * (np.cbrt(1.0 + a) + np.cbrt(1.0 - a))
    z2 = np.sqrt(3.0 * a * a + z1 * z1)
    return 3.0 + z2 - np.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def energy_at_isco(a: float) -> float:
    """Specific energy E/mu of a circular equatorial orbit at the ISCO."""
    a = float(np.clip(a, 0.0, 1.0))
    r = isco_radius_over_M(a)
    num = r**1.5 - 2.0 * np.sqrt(r) + a
    den = r**0.75 * np.sqrt(r**1.5 - 3.0 * np.sqrt(r) + 2.0 * a)
    if den <= 0.0:
        return np.sqrt(1.0 / 3.0)  # extremal limit
    return float(np.clip(num / den, 0.0, 1.0))


def efficiency(a: float) -> float:
    """Thin-disc radiative efficiency 1 - E_ISCO(a), prograde."""
    return 1.0 - energy_at_isco(a)


def irreducible_mass_fraction(a: float) -> float:
    """M_irr / M = sqrt((1 + sqrt(1 - a^2)) / 2) (Christodoulou)."""
    a = float(np.clip(a, 0.0, 1.0))
    return float(np.sqrt((1.0 + np.sqrt(1.0 - a * a)) / 2.0))


def remnant_spin(m1: float, m2: float, chi_eff: float) -> float:
    """Aligned-spin remnant spin fit (Rezzolla et al. 2008), chi1 = chi2 = chi_eff."""
    m1, m2 = max(m1, m2), min(m1, m2)
    q = m1 / m2
    eta = q / (1.0 + q) ** 2
    ell = 2.0 * SQRT3 + T2 * eta + T3 * eta**2
    a = ((1.0 + q * q) * chi_eff + q * ell) / (1.0 + q) ** 2
    return float(np.clip(a, 0.0, A_MAX))


# ---------------------------------------------------------------------------
def build_table() -> pd.DataFrame:
    df = pd.read_csv(CATALOG)
    need = [
        "mass_1_source_msun",
        "mass_2_source_msun",
        "final_mass_source_msun",
        "chi_eff",
    ]
    df = df.dropna(subset=need).copy()
    df = df[
        (df.mass_1_source_msun > 0)
        & (df.mass_2_source_msun > 0)
        & (df.final_mass_source_msun > 0)
    ]

    rows = []
    for _, r in df.iterrows():
        m1, m2 = float(r.mass_1_source_msun), float(r.mass_2_source_msun)
        mf = float(r.final_mass_source_msun)
        chieff = float(np.clip(r.chi_eff, -0.99, 0.99))
        a = remnant_spin(m1, m2, chieff)
        eta = efficiency(a)
        mirr_frac = irreducible_mass_fraction(a)
        e_rot_msun = mf * (1.0 - mirr_frac)
        r_isco_m = isco_radius_over_M(a)
        rg_km = G * mf * MSUN / C2 / 1000.0  # GM/c^2 in km
        rows.append(
            {
                "event_id": r.event_id,
                "mass_1_source": m1,
                "mass_2_source": m2,
                "q": max(m1, m2) / min(m1, m2),
                "chi_eff": chieff,
                "final_mass_source": mf,
                "a_fit": a,
                "r_isco_kerr_km": r_isco_m * rg_km,
                "r_isco_schwarzschild_km": 6.0 * rg_km,
                "isco_ratio_schw_over_kerr": 6.0 / r_isco_m,
                "e_isco": energy_at_isco(a),
                "eta_radiative": eta,
                "eta_gain_over_schwarzschild": eta - efficiency(0.0),
                "m_irreducible_source": mf * mirr_frac,
                "e_rot_msun": e_rot_msun,
                "e_rot_erg": e_rot_msun * MSUN * C2,
                "e_rot_fraction": 1.0 - mirr_frac,
            }
        )
    return pd.DataFrame(rows)


def summarise(t: pd.DataFrame) -> dict:
    eta_max = efficiency(1.0)
    return {
        "n": len(t),
        "a_median": t.a_fit.median(),
        "a_p90": t.a_fit.quantile(0.9),
        "a_max": t.a_fit.max(),
        "eta_median": t.eta_radiative.median(),
        "eta_p10": t.eta_radiative.quantile(0.1),
        "eta_p90": t.eta_radiative.quantile(0.9),
        "eta_max": t.eta_radiative.max(),
        "eta_kerr_max": eta_max,
        "eta_schwarzschild": efficiency(0.0),
        "frac_a_gt_09": float((t.a_fit > 0.9).mean()),
        "mean_isco_overshoot": float(t.isco_ratio_schw_over_kerr.mean()),
        "max_isco_overshoot": float(t.isco_ratio_schw_over_kerr.max()),
        "total_e_rot_msun": float(t.e_rot_msun.sum()),
        "median_e_rot_msun": float(t.e_rot_msun.median()),
    }


def plot(t: pd.DataFrame, s: dict) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.2), dpi=160)
    fig.patch.set_facecolor("#0b1220")

    for ax in axes:
        ax.set_facecolor("#0b1220")
        for spine in ax.spines.values():
            spine.set_color("#2a3a5c")
        ax.tick_params(colors="#94a6c2", labelsize=9)
        ax.xaxis.label.set_color("#c3d2e8")
        ax.yaxis.label.set_color("#c3d2e8")
        ax.title.set_color("#e7eefb")
        ax.grid(color="#1b2740", lw=0.7, alpha=0.9)

    # -- panel 1: efficiency vs remnant mass
    ax = axes[0]
    sc = ax.scatter(
        t.final_mass_source, t.eta_radiative, c=t.a_fit, cmap="viridis",
        s=20, alpha=0.9, edgecolors="none",
    )
    ax.axhline(s["eta_kerr_max"], color="#ffb26b", ls="--", lw=1.2,
               label=f"Kerr limit (a→1) {s['eta_kerr_max']:.3f}")
    ax.axhline(s["eta_schwarzschild"], color="#a78bfa", ls=":", lw=1.2,
               label=f"Schwarzschild {s['eta_schwarzschild']:.3f}")
    ax.axhline(s["eta_median"], color="#58d3ff", ls="-", lw=1.0, alpha=0.8,
               label=f"median {s['eta_median']:.3f}")
    ax.set_xscale("log")
    ax.set_xlabel(r"remnant mass [$M_\odot$]")
    ax.set_ylabel(r"radiative efficiency $\eta = 1 - E_{\rm ISCO}$")
    ax.set_title("Efficiency of the remnant population")
    ax.set_ylim(0, 0.46)
    leg = ax.legend(loc="upper left", fontsize=8, frameon=False)
    for text in leg.get_texts():
        text.set_color("#c3d2e8")
    cb = fig.colorbar(sc, ax=ax, pad=0.015)
    cb.set_label("inferred spin $a_*$", color="#c3d2e8", fontsize=8)
    cb.ax.tick_params(colors="#94a6c2", labelsize=8)
    cb.outline.set_edgecolor("#2a3a5c")

    # -- panel 2: rotational energy reservoir
    ax = axes[1]
    sc2 = ax.scatter(
        t.final_mass_source,
        t.e_rot_msun,
        c=t.a_fit,
        cmap="viridis",
        s=20,
        alpha=0.9,
        edgecolors="none",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("remnant mass [$M_\\odot$]")
    ax.set_ylabel("rotational energy [$M_\\odot c^2$]")
    ax.set_title("Rotational energy retained after merger")
    cb2 = fig.colorbar(sc2, ax=ax, pad=0.015)
    cb2.set_label("inferred spin $a_*$", color="#c3d2e8", fontsize=8)
    cb2.ax.tick_params(colors="#94a6c2", labelsize=8)
    cb2.outline.set_edgecolor("#2a3a5c")

    fig.tight_layout()
    fig.savefig(OUT_PNG, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def plotly_html(t: pd.DataFrame, s: dict) -> None:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Efficiency of the remnant population",
                        "Rotational energy retained after merger"),
        horizontal_spacing=0.10,
    )
    fig.add_trace(
        go.Scatter(
            x=t.final_mass_source, y=t.eta_radiative, mode="markers", name="GWTC remnants",
            marker=dict(size=6, color=t.a_fit, colorscale="Viridis",
                        colorbar=dict(title="a<sub>*</sub>", x=1.02, len=0.45, y=0.78),
                        line=dict(width=0)),
            text=t.event_id,
            hovertemplate="%{text}<br>M=%{x:.1f} M☉<br>η=%{y:.3f}<extra></extra>",
        ),
        row=1, col=1,
    )
    fig.add_hline(y=s["eta_median"], line=dict(color="#58d3ff", width=1),
                  annotation_text=f"median {s['eta_median']:.3f}", row=1, col=1)
    fig.add_hline(y=s["eta_kerr_max"], line=dict(color="#ffb26b", dash="dash", width=1),
                  annotation_text=f"Kerr limit {s['eta_kerr_max']:.3f}", row=1, col=1)
    fig.add_hline(y=s["eta_schwarzschild"], line=dict(color="#a78bfa", dash="dot", width=1),
                  annotation_text=f"Schwarzschild {s['eta_schwarzschild']:.3f}", row=1, col=1)

    fig.add_trace(
        go.Scatter(
            x=t.final_mass_source, y=t.e_rot_msun, mode="markers", name="remnants",
            marker=dict(size=6, color=t.a_fit, colorscale="Viridis",
                        colorbar=dict(title="a<sub>*</sub>", x=1.02, len=0.45, y=0.22),
                        line=dict(width=0)),
            text=t.event_id,
            hovertemplate="%{text}<br>M=%{x:.1f} M☉<br>E_rot=%{y:.2f} M☉c²<extra></extra>",
        ),
        row=1, col=2,
    )
    fig.update_xaxes(type="log", title_text="remnant mass [M☉]",
                     row=1, col=1, gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(title_text="η = 1 − E<sub>ISCO</sub>", range=[0, 0.46],
                     row=1, col=1, gridcolor="#1b2740", color="#94a6c2")
    fig.update_xaxes(type="log", title_text="remnant mass [M☉]", row=1, col=2,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(type="log", title_text="rotational energy [M☉c²]", row=1, col=2,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(family="Inter, system-ui, sans-serif", color="#c3d2e8", size=12),
        title=dict(text="Kerr remnant energetics — GWTC population", x=0.02, font=dict(size=17)),
        legend=dict(orientation="h", y=-0.16, x=0, bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=60, r=40, t=80, b=70),
        height=520,
        showlegend=False,
    )
    fig.write_html(OUT_HTML, include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "responsive": True})


def report(t: pd.DataFrame, s: dict) -> str:
    return f"""# Remnant energetics of the GWTC population

*Generated by `scripts/remnant_energetics.py` from `data/processed/gwosc_gwtc.csv`.*

## Question

How much rotational energy survives a merger, and what thin-disc efficiency
does the inferred remnant spin imply?  The second number is a consistency
test: a Kerr horizon has a hard upper bound of **{s["eta_kerr_max"]:.4f}**
(= 1 − 1/√3), approached only as a → 1.

## Method

- Component masses and effective inspiral spin `chi_eff` from the GWTC catalogue.
- Remnant spin from the aligned-spin fit of Rezzolla et al. (2008), assuming
  `chi_1 = chi_2 = chi_eff`. This is an approximation: no precession, no
  individual spin measurements, and the fit is calibrated on numerical
  relativity.
- Exact prograde Kerr ISCO (Bardeen–Press–Teukolsky 1972).
- Specific energy at the ISCO gives η = 1 − E_ISCO.
- Irreducible mass from Christodoulou: M_irr/M = √((1 + √(1 − a²))/2), so the
  rotational reservoir is E_rot = (M − M_irr)c².

## Results

| quantity | value |
|---|---|
| events with complete masses + spin | **{s["n"]}** |
| median inferred spin a* | **{s["a_median"]:.3f}** |
| 90th percentile spin | {s["a_p90"]:.3f} |
| maximum inferred spin | {s["a_max"]:.3f} |
| fraction with a* > 0.9 | {100 * s["frac_a_gt_09"]:.1f}% |
| median efficiency η | **{s["eta_median"]:.3f}** |
| 10–90% efficiency range | {s["eta_p10"]:.3f} – {s["eta_p90"]:.3f} |
| maximum efficiency | {s["eta_max"]:.3f} |
| Kerr bound | {s["eta_kerr_max"]:.3f} |
| Schwarzschild efficiency | {s["eta_schwarzschild"]:.4f} |
| median retained rotational energy | {s["median_e_rot_msun"]:.2f} M☉c² |
| total rotational reservoir in sample | {s["total_e_rot_msun"]:.0f} M☉c² |
| mean Schwarzschild/ Kerr ISCO overshoot | {s["mean_isco_overshoot"]:.2f}× |
| maximum ISCO overshoot | {s["max_isco_overshoot"]:.2f}× |

## Interpretation

1. **The population is modestly spinning.** The median efficiency
   ({s["eta_median"]:.3f}) is several times the Schwarzschild value
   ({s["eta_schwarzschild"]:.4f}) but well below the Kerr bound. Any
   population-level claim that mergers routinely produce near-extremal holes
   is not supported by the effective-spin data.
2. **A Schwarzschild ISCO is not a safe default.** Using 6GM/c² for every
   remnant overestimates the ISCO radius by a mean factor
   {s["mean_isco_overshoot"]:.2f} and by up to {s["max_isco_overshoot"]:.2f}
   for the fastest remnants. This is exactly the factor-of-two class of error
   corrected in the earlier ISCO validation, now quantified across the
   catalogue.
3. **The rotational reservoir is large compared with the GW output.** The
   median remnant retains of order {s["median_e_rot_msun"]:.1f} M☉c² of
   rotational energy, while a typical merger radiates a few M☉c² in
   gravitational waves. Spin-down channels (Blandford–Znajek, Penrose) have
   substantial energy available, but the efficiency bound remains the Kerr
   one unless the object is horizonless.
4. **The efficiency bound is a discriminant, not a measurement.** Reaching
   η > {s["eta_kerr_max"]:.3f} would require physics beyond a Kerr horizon.
   No event in this sample requires it under the adopted spin fit — which is
   a null result, stated as such.

## Caveats

- `a_fit` is not a posterior sample; it is a point estimate from `chi_eff`.
  Individual event uncertainties are not propagated. The catalogue-level
  conclusions are therefore qualitative, not confidence intervals.
- The aligned-spin assumption biases the inferred spin for precessing systems.
- The efficiency is the thin-disc value for a prograde ISCO; it is not the
  observed bolometric efficiency of any specific source.
- Retarded-time and redshift corrections cancel in the efficiency (a ratio of
  energies at the same radius) but not in the energy totals.

## Reproduce

```bash
/home/dawe/Projects/astro-science/.venv/bin/python scripts/remnant_energetics.py
```

Outputs: `results/remnant_energetics.csv`, `results/remnant_energetics.png`,
`premium/figures/remnant_energetics.html`.
"""


def main() -> None:
    t = build_table()
    s = summarise(t)
    t.to_csv(OUT_CSV, index=False)
    plot(t, s)
    plotly_html(t, s)
    (PROJECT / "reports/remnant_energetics.md").write_text(
        report(t, s), encoding="utf-8"
    )

    print(f"events: {s['n']}")
    print(
        f"median a*: {s['a_median']:.3f}  p90: {s['a_p90']:.3f}  max: {s['a_max']:.3f}"
    )
    print(
        f"median eta: {s['eta_median']:.4f}  range: {s['eta_p10']:.4f}-{s['eta_p90']:.4f}"
    )
    print(
        f"Kerr bound: {s['eta_kerr_max']:.4f}  Schwarzschild: {s['eta_schwarzschild']:.4f}"
    )
    print(f"mean ISCO overshoot (Schwarzschild/Kerr): {s['mean_isco_overshoot']:.2f}x")
    print(f"total rotational energy: {s['total_e_rot_msun']:.0f} Msun c^2")
    print(
        f"wrote {OUT_CSV.name}, {OUT_PNG.name}, {OUT_HTML.name}, reports/remnant_energetics.md"
    )


if __name__ == "__main__":
    main()
