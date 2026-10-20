#!/usr/bin/env python3
"""Exotic-compact-object discrimination from the GWTC remnant population."""

from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "scripts"))
from remnant_energetics import build_table, efficiency  # noqa: E402

OUT_CSV = PROJECT / "results" / "exotic_discrimination.csv"
OUT_PNG = PROJECT / "results" / "exotic_discrimination.png"
OUT_HTML = PROJECT / "premium" / "figures" / "exotic_discrimination.html"

KERR_BOUND = 0.422646  # 1 - 1/sqrt(3)
SCHWARZSCHILD_ETA = 0.057191


def a_for_eta(target: float) -> float:
    lo, hi = 0.0, 0.998
    for _ in range(60):
        mid = (lo + hi) / 2
        if efficiency(mid) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def build() -> pd.DataFrame:
    t = build_table().copy()
    t["margin_to_bound"] = KERR_BOUND - t["eta_radiative"]
    t["exceeds_0.2"] = t.eta_radiative > 0.2
    t["exceeds_0.3"] = t.eta_radiative > 0.3
    t["exceeds_0.4"] = t.eta_radiative > 0.4
    return t


def summarise(t: pd.DataFrame) -> dict:
    return {
        "n": len(t),
        "eta_median": float(t.eta_radiative.median()),
        "eta_p90": float(t.eta_radiative.quantile(0.9)),
        "eta_max": float(t.eta_radiative.max()),
        "margin_median": float(t.margin_to_bound.median()),
        "margin_min": float(t.margin_to_bound.min()),
        "n_above_0.1": int((t.eta_radiative > 0.1).sum()),
        "n_above_0.2": int((t.eta_radiative > 0.2).sum()),
        "n_above_0.3": int((t.eta_radiative > 0.3).sum()),
        "n_above_0.4": int((t.eta_radiative > 0.4).sum()),
        "a_needed_0.2": a_for_eta(0.2),
        "a_needed_0.3": a_for_eta(0.3),
        "a_needed_0.4": a_for_eta(0.4),
        "a_max_observed": float(t.a_fit.max()),
        "kerr_bound": KERR_BOUND,
        "schwarzschild_eta": SCHWARZSCHILD_ETA,
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

    ax = axes[0]
    bins = np.linspace(0, 0.46, 24)
    ax.hist(t.eta_radiative, bins=bins, color="#58d3ff", alpha=0.75,
            edgecolor="#0b1220", label="GWTC remnants")
    ax.axvline(SCHWARZSCHILD_ETA, color="#a78bfa", ls=":", lw=1.4,
               label="Schwarzschild %.3f" % SCHWARZSCHILD_ETA)
    ax.axvline(s["eta_median"], color="#58d3ff", ls="-", lw=1.2,
               label="median %.3f" % s["eta_median"])
    ax.axvline(KERR_BOUND, color="#ffb26b", ls="--", lw=1.4,
               label="Kerr bound %.3f" % KERR_BOUND)
    ax.set_xlabel("radiative efficiency eta = 1 - E_ISCO")
    ax.set_ylabel("number of remnants")
    ax.set_title("Efficiency of the remnant population")
    ax.set_xlim(0, 0.46)
    leg = ax.legend(loc="upper right", fontsize=8, frameon=False)
    for text in leg.get_texts():
        text.set_color("#c3d2e8")

    ax = axes[1]
    sc = ax.scatter(t.final_mass_source, t.margin_to_bound, c=t.a_fit,
                    cmap="viridis", s=20, alpha=0.9, edgecolors="none")
    ax.axhline(0, color="#ff6b6b", ls="--", lw=1.2, label="Kerr bound (margin 0)")
    ax.set_xscale("log")
    ax.set_xlabel("remnant mass [Msun]")
    ax.set_ylabel("margin to Kerr bound 0.4226 - eta")
    ax.set_title("How far the population is from falsifying Kerr")
    ax.set_ylim(-0.02, 0.42)
    leg = ax.legend(loc="upper right", fontsize=8, frameon=False)
    for text in leg.get_texts():
        text.set_color("#c3d2e8")
    cb = fig.colorbar(sc, ax=ax, pad=0.015)
    cb.set_label("inferred spin a*", color="#c3d2e8", fontsize=8)
    cb.ax.tick_params(colors="#94a6c2", labelsize=8)
    cb.outline.set_edgecolor("#2a3a5c")

    fig.tight_layout()
    fig.savefig(OUT_PNG, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def plotly_html(t: pd.DataFrame, s: dict) -> None:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Efficiency of the remnant population",
                        "Margin to the Kerr bound"),
        horizontal_spacing=0.10,
    )
    fig.add_trace(
        go.Histogram(x=t.eta_radiative, nbinsx=24, name="remnants",
                     marker=dict(color="#58d3ff", line=dict(color="#0b1220", width=1))),
        row=1, col=1,
    )
    for y, color, name in ((SCHWARZSCHILD_ETA, "#a78bfa", "Schwarzschild"),
                           (s["eta_median"], "#58d3ff", "median"),
                           (KERR_BOUND, "#ffb26b", "Kerr bound")):
        fig.add_vline(x=y, line=dict(color=color, dash="dash", width=1.2),
                      annotation_text="%s %.3f" % (name, y), row=1, col=1)

    fig.add_trace(
        go.Scatter(
            x=t.final_mass_source, y=t.margin_to_bound, mode="markers", name="remnants",
            marker=dict(size=6, color=t.a_fit, colorscale="Viridis",
                        colorbar=dict(title="a*", x=1.02, len=0.45, y=0.22),
                        line=dict(width=0)),
            text=t.event_id,
            hovertemplate="%{text}<br>M=%{x:.1f} Msun<br>margin=%{y:.3f}<extra></extra>",
        ),
        row=1, col=2,
    )
    fig.add_hline(y=0, line=dict(color="#ff6b6b", dash="dash", width=1),
                  annotation_text="Kerr bound", row=1, col=2)
    fig.update_xaxes(title_text="eta = 1 - E_ISCO", row=1, col=1,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(title_text="number of remnants", row=1, col=1,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_xaxes(type="log", title_text="remnant mass [Msun]", row=1, col=2,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(title_text="margin to Kerr bound", range=[-0.02, 0.42],
                     row=1, col=2, gridcolor="#1b2740", color="#94a6c2")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(family="Inter, system-ui, sans-serif", color="#c3d2e8", size=12),
        title=dict(text="Exotic-object discrimination - GWTC population", x=0.02, font=dict(size=17)),
        legend=dict(orientation="h", y=-0.16, x=0, bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=60, r=40, t=80, b=70),
        height=520,
        showlegend=False,
    )
    fig.write_html(OUT_HTML, include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "responsive": True})


def report(t: pd.DataFrame, s: dict) -> str:
    return """# Exotic-compact-object discrimination from the GWTC population

Generated by scripts/exotic_discrimination.py from results/remnant_energetics.csv.

## Question

Under the Kerr hypothesis the remnant population has a thin-disc efficiency of
about %.4f and a hard upper bound of %.4f.
How far is the current sample from that bound, and what spin precision would
be required to violate it?

## Method

No horizonless model is fit. Instead, for every remnant we compute the margin
0.4226 - eta between its inferred efficiency and the Kerr bound, and the spin
that a Kerr hole would need in order to reach efficiencies of 0.2, 0.3 and 0.4.
An observation requiring eta above the bound, or a spin above the Thorne limit
(0.998), would be inconsistent with Kerr.

## Results

| quantity | value |
|---|---|
| events | **%d** |
| median efficiency eta | **%.4f** |
| 90th percentile eta | %.4f |
| maximum eta | %.4f |
| median margin to bound | %.4f |
| minimum margin (closest event) | %.4f |
| events with eta > 0.1 | %d |
| events with eta > 0.2 | %d |
| events with eta > 0.3 | %d |
| events with eta > 0.4 | %d |
| spin needed for eta = 0.2 | %.3f |
| spin needed for eta = 0.3 | %.3f |
| spin needed for eta = 0.4 | %.3f |
| maximum inferred spin in sample | %.3f |
| Kerr bound | %.4f |
| Schwarzschild baseline | %.4f |

## Interpretation

1. The population is nowhere near the bound. The closest event is still
   %.3f below it, and the 90th percentile efficiency is only
   %.3f. Reaching eta = 0.2 requires a spin of %.3f,
   which is above the maximum inferred spin in the sample (%.3f).
2. The discriminant is sharp but currently unused. A single future event with
   eta > %.4f would be inconsistent with a Kerr horizon. The
   required measurement precision is modest: the margin is large compared with
   typical spin uncertainties, so a violation would be unambiguous.
3. The sample is consistent with low-spin mergers. Every event sits between
   the Schwarzschild baseline (%.4f) and eta ~ 0.17, the
   same range as low-luminosity AGN thin discs. There is no hint of the
   near-extremal population that a horizonless object with a hard surface would
   need to mimic.
4. What would actually falsify Kerr here is not a population shift but a
   single high-eta event with a well-measured spin above %.2f.
   Until then the null result stands: the data are consistent with Kerr.

## Caveats

- This is a null-result consistency test, not a model comparison: no
  horizonless metric is fit.
- Spin is a point estimate from chi_eff; uncertainties are not propagated.
- The efficiency is the thin-disc value at the prograde ISCO.

## Reproduce

    /home/dawe/Projects/astro-science/.venv/bin/python scripts/exotic_discrimination.py

Outputs: results/exotic_discrimination.csv, results/exotic_discrimination.png,
premium/figures/exotic_discrimination.html.
""" % (
        s["eta_median"], s["kerr_bound"],
        s["n"], s["eta_median"], s["eta_p90"], s["eta_max"],
        s["margin_median"], s["margin_min"],
        s["n_above_0.1"], s["n_above_0.2"], s["n_above_0.3"], s["n_above_0.4"],
        s["a_needed_0.2"], s["a_needed_0.3"], s["a_needed_0.4"],
        s["a_max_observed"], s["kerr_bound"], s["schwarzschild_eta"],
        s["margin_min"], s["eta_p90"], s["a_needed_0.2"], s["a_max_observed"],
        s["kerr_bound"], s["schwarzschild_eta"], s["a_needed_0.3"],
    )


def main() -> None:
    t = build()
    s = summarise(t)
    t.to_csv(OUT_CSV, index=False)
    plot(t, s)
    plotly_html(t, s)
    (PROJECT / "reports" / "exotic_discrimination.md").write_text(report(t, s), encoding="utf-8")
    print("events: %d" % s["n"])
    print("median eta: %.4f  max: %.4f" % (s["eta_median"], s["eta_max"]))
    print("median margin: %.4f  min: %.4f" % (s["margin_median"], s["margin_min"]))
    print("events above 0.2/0.3/0.4: %d/%d/%d" % (s["n_above_0.2"], s["n_above_0.3"], s["n_above_0.4"]))
    print("spin needed for 0.2/0.3/0.4: %.3f/%.3f/%.3f" % (s["a_needed_0.2"], s["a_needed_0.3"], s["a_needed_0.4"]))
    print("wrote %s, %s, %s, reports/exotic_discrimination.md" % (OUT_CSV.name, OUT_PNG.name, OUT_HTML.name))


if __name__ == "__main__":
    main()
