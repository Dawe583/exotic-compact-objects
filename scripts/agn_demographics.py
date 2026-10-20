#!/usr/bin/env python3
"""AGN reverberation-mapped mass demographics."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
SRC = PROJECT / "data/processed/agn_reverberation_masses.csv"
OUT_CSV = PROJECT / "results" / "agn_demographics.csv"
OUT_PNG = PROJECT / "results" / "agn_demographics.png"
OUT_HTML = PROJECT / "premium" / "figures" / "agn_demographics.html"


def build() -> pd.DataFrame:
    df = pd.read_csv(SRC).copy()
    df = df[df.mass_msun > 0].copy()
    df["log10_mass"] = np.log10(df.mass_msun)
    df["rs_km"] = 2 * 6.67430e-11 * df.mass_msun * 1.98847e30 / (2.99792458e8 ** 2) / 1000.0
    df["eddington_lum_log10"] = np.log10(df.eddington_luminosity_erg_s)
    return df


def summarise(t: pd.DataFrame) -> dict:
    return {
        "n": len(t),
        "mass_median_log": float(t.log10_mass.median()),
        "mass_min_log": float(t.log10_mass.min()),
        "mass_max_log": float(t.log10_mass.max()),
        "mass_mean_log": float(t.log10_mass.mean()),
        "mass_std_log": float(t.log10_mass.std()),
        "z_median": float(t.redshift.median()),
        "z_min": float(t.redshift.min()),
        "z_max": float(t.redshift.max()),
        "rs_median_km": float(t.rs_km.median()),
        "edd_lum_median_log": float(t.eddington_lum_log10.median()),
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
    ax.hist(t.log10_mass, bins=18, color="#a78bfa", alpha=0.78,
            edgecolor="#0b1220", label="reverberation masses")
    ax.axvline(s["mass_median_log"], color="#58d3ff", ls="--", lw=1.4,
               label="median %.2f" % s["mass_median_log"])
    ax.set_xlabel("log10(M_BH / Msun)")
    ax.set_ylabel("number of AGN")
    ax.set_title("AGN black-hole mass distribution")
    leg = ax.legend(loc="upper right", fontsize=8, frameon=False)
    for text in leg.get_texts():
        text.set_color("#c3d2e8")

    ax = axes[1]
    sc = ax.scatter(t.redshift, t.log10_mass, c=t.mass_msun, cmap="plasma",
                    s=22, alpha=0.9, edgecolors="none")
    ax.set_xlabel("redshift z")
    ax.set_ylabel("log10(M_BH / Msun)")
    ax.set_title("Mass vs redshift (reverberation sample)")
    cb = fig.colorbar(sc, ax=ax, pad=0.015)
    cb.set_label("mass [Msun]", color="#c3d2e8", fontsize=8)
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
        subplot_titles=("AGN mass distribution", "Mass vs redshift"),
        horizontal_spacing=0.10,
    )
    fig.add_trace(
        go.Histogram(x=t.log10_mass, nbinsx=18, name="AGN",
                     marker=dict(color="#a78bfa", line=dict(color="#0b1220", width=1))),
        row=1, col=1,
    )
    fig.add_vline(x=s["mass_median_log"], line=dict(color="#58d3ff", dash="dash", width=1.2),
                  annotation_text="median %.2f" % s["mass_median_log"], row=1, col=1)
    fig.add_trace(
        go.Scatter(
            x=t.redshift, y=t.log10_mass, mode="markers", name="AGN",
            marker=dict(size=7, color=t.mass_msun, colorscale="Plasma",
                        colorbar=dict(title="M [Msun]", x=1.02, len=0.45, y=0.5),
                        line=dict(width=0)),
            text=t.name,
            hovertemplate="%{text}<br>z=%{x:.3f}<br>logM=%{y:.2f}<extra></extra>",
        ),
        row=1, col=2,
    )
    fig.update_xaxes(title_text="log10(M_BH / Msun)", row=1, col=1,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(title_text="number of AGN", row=1, col=1,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_xaxes(title_text="redshift z", row=1, col=2,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(title_text="log10(M_BH / Msun)", row=1, col=2,
                     gridcolor="#1b2740", color="#94a6c2")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(family="Inter, system-ui, sans-serif", color="#c3d2e8", size=12),
        title=dict(text="AGN reverberation-mapped masses", x=0.02, font=dict(size=17)),
        margin=dict(l=60, r=40, t=80, b=60),
        height=520,
        showlegend=False,
    )
    fig.write_html(OUT_HTML, include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "responsive": True})


def report(t: pd.DataFrame, s: dict) -> str:
    return """# AGN reverberation-mapped mass demographics

Generated by scripts/agn_demographics.py from data/processed/agn_reverberation_masses.csv.

## Sample

%d supermassive black holes with reverberation-mapped masses (line widths and
time delays from the literature compilation). The sample anchors the
Eddington-ratio distribution used in the early-SMBH growth analysis.

## Results

| quantity | value |
|---|---|
| sources | **%d** |
| median log10(M/Msun) | **%.2f** |
| mass range (log10) | %.2f - %.2f |
| std (log10) | %.3f |
| median redshift | %.4f |
| redshift range | %.4f - %.4f |
| median Schwarzschild radius | %.0f km |
| median Eddington luminosity | 10^%.2f erg/s |

## Interpretation

1. The sample spans about %.1f dex in mass, centred on 10^%.2f Msun, the
   regime where reverberation mapping is most reliable.
2. Redshifts are low (median z = %.4f), so the masses are measured in the
   local universe; extrapolation to high redshift is not supported by this
   sample alone.
3. The Eddington luminosity scales as L_Edd ~ 1.26e38 (M/Msun) erg/s; the
   observed luminosities needed for true Eddington ratios are not part of this
   catalogue, so L/L_Edd is left to the early-SMBH-growth notebook.

## Reproduce

    /home/dawe/Projects/astro-science/.venv/bin/python scripts/agn_demographics.py

Outputs: results/agn_demographics.csv, results/agn_demographics.png,
premium/figures/agn_demographics.html.
""" % (
        s["n"], s["n"], s["mass_median_log"], s["mass_min_log"], s["mass_max_log"],
        s["mass_std_log"], s["z_median"], s["z_min"], s["z_max"],
        s["rs_median_km"], s["edd_lum_median_log"], s["mass_max_log"] - s["mass_min_log"],
        s["mass_median_log"], s["z_median"],
    )


def main() -> None:
    t = build()
    s = summarise(t)
    t.to_csv(OUT_CSV, index=False)
    plot(t, s)
    plotly_html(t, s)
    (PROJECT / "reports" / "agn_demographics.md").write_text(report(t, s), encoding="utf-8")
    print("sources: %d" % s["n"])
    print("median logM: %.2f (range %.2f-%.2f)" % (s["mass_median_log"], s["mass_min_log"], s["mass_max_log"]))
    print("median z: %.4f (range %.4f-%.4f)" % (s["z_median"], s["z_min"], s["z_max"]))
    print("wrote %s, %s, %s, reports/agn_demographics.md" % (OUT_CSV.name, OUT_PNG.name, OUT_HTML.name))


if __name__ == "__main__":
    main()
