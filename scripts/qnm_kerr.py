#!/usr/bin/env python3
"""Quasinormal mode frequencies for Kerr black holes (eikonal approximation)."""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
OUT_CSV = PROJECT / "results" / "qnm_kerr.csv"
OUT_PNG = PROJECT / "results" / "qnm_kerr.png"
OUT_HTML = PROJECT / "premium" / "figures" / "qnm_kerr.html"


def isco_radius(a):
    a = float(np.clip(a, 0.0, 0.998))
    z1 = 1.0 + np.cbrt(1.0 - a * a) * (np.cbrt(1.0 + a) + np.cbrt(1.0 - a))
    z2 = np.sqrt(3.0 * a * a + z1 * z1)
    return 3.0 + z2 - np.sqrt((3.0 - z1) * (3.0 + z1 + 2.0 * z2))


def photon_sphere_radius(a):
    """Photon sphere radius for Kerr (equatorial, prograde) — approximate."""
    # r_ph = 2M [1 + cos(2/3 arccos(-a))]  (Bardeen 1973, a in [0,1])
    a = float(np.clip(a, 0.0, 0.998))
    return 2.0 * (1.0 + np.cos((2.0 / 3.0) * np.arccos(-a)))


def qnm_eikonal(a, l=2, n=0):
    """Eikonal approximation: omega = (l+1/2)*Omega_ph - i*(n+1/2)*lambda.

    Returns (real_freq, damping) in units of 1/M.
    """
    r_ph = photon_sphere_radius(a)
    # orbital frequency at photon sphere
    omega_ph = 1.0 / (r_ph ** 1.5 + a)
    # Lyapunov exponent (damping) — approximate
    lam = np.sqrt(4.0 * (1.0 - (a / r_ph) ** 2)) / (2.0 * r_ph)  # rough
    if lam <= 0:
        lam = 0.1
    real = (l + 0.5) * omega_ph
    damp = (n + 0.5) * lam
    return real, damp


def q_factor(real, damp):
    if damp <= 0:
        return float("inf")
    return real / (2 * damp)


def build_table() -> pd.DataFrame:
    rows = []
    for a in np.linspace(0, 0.998, 50):
        for l in (2, 3, 4):
            for n in (0, 1):
                re_, im = qnm_eikonal(a, l, n)
                rows.append({
                    "spin_a": round(float(a), 4),
                    "l": l,
                    "n": n,
                    "omega_real": re_,
                    "omega_imag": im,
                    "frequency_M": re_ / (2 * np.pi),
                    "damping_M": im,
                    "Q_factor": q_factor(re_, im),
                    "isco_radius": isco_radius(a),
                    "photon_sphere": photon_sphere_radius(a),
                })
    return pd.DataFrame(rows)


def summarise(t: pd.DataFrame) -> dict:
    t0 = t[(t.l == 2) & (t.n == 0)]
    return {
        "n": len(t),
        "spin_range": (float(t.spin_a.min()), float(t.spin_a.max())),
        "freq_l2n0_a0": float(t0[t0.spin_a == 0].frequency_M.iloc[0]),
        "freq_l2n0_a0998": float(t0[t0.spin_a == t0.spin_a.max()].frequency_M.iloc[0]),
        "Q_l2n0_a0": float(t0[t0.spin_a == 0].Q_factor.iloc[0]),
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
    for l in (2, 3, 4):
        sub = t[(t.l == l) & (t.n == 0)]
        ax.plot(sub.spin_a, sub.frequency_M, lw=2, label="l=%d, n=0" % l)
    ax.set_xlabel("spin a*")
    ax.set_ylabel("ringdown frequency [1/M]")
    ax.set_title("QNM frequency vs spin (eikonal)")
    leg = ax.legend(loc="upper left", fontsize=8, frameon=False)
    for text in leg.get_texts():
        text.set_color("#c3d2e8")

    ax = axes[1]
    sub = t[(t.l == 2) & (t.n == 0)]
    ax.plot(sub.spin_a, sub.Q_factor, color="#58d3ff", lw=2)
    ax.set_xlabel("spin a*")
    ax.set_ylabel("quality factor Q")
    ax.set_title("QNM quality factor (l=2, n=0)")

    fig.tight_layout()
    fig.savefig(OUT_PNG, facecolor=fig.get_facecolor(), bbox_inches="tight")
    plt.close(fig)


def plotly_html(t: pd.DataFrame, s: dict) -> None:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("QNM frequency vs spin (eikonal)",
                        "Quality factor (l=2, n=0)"),
        horizontal_spacing=0.10,
    )
    for l in (2, 3, 4):
        sub = t[(t.l == l) & (t.n == 0)]
        fig.add_trace(
            go.Scatter(x=sub.spin_a, y=sub.frequency_M, mode="lines",
                       name="l=%d" % l, line=dict(width=2)),
            row=1, col=1,
        )
    sub = t[(t.l == 2) & (t.n == 0)]
    fig.add_trace(
        go.Scatter(x=sub.spin_a, y=sub.Q_factor, mode="lines",
                   name="Q", line=dict(color="#58d3ff", width=2),
                   showlegend=False),
        row=1, col=2,
    )
    fig.update_xaxes(title_text="spin a*", row=1, col=1, gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(title_text="frequency [1/M]", row=1, col=1, gridcolor="#1b2740", color="#94a6c2")
    fig.update_xaxes(title_text="spin a*", row=1, col=2, gridcolor="#1b2740", color="#94a6c2")
    fig.update_yaxes(title_text="quality factor Q", row=1, col=2, gridcolor="#1b2740", color="#94a6c2")
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0b1220",
        plot_bgcolor="#0b1220",
        font=dict(family="Times New Roman, Times, serif", color="#c3d2e8", size=12),
        title=dict(text="Kerr quasinormal modes (eikonal)", x=0.02, font=dict(size=17)),
        margin=dict(l=60, r=40, t=80, b=60),
        height=520,
    )
    fig.write_html(OUT_HTML, include_plotlyjs="cdn", full_html=True,
                   config={"displayModeBar": True, "responsive": True})


def report(t: pd.DataFrame, s: dict) -> str:
    return """# Kerr quasinormal modes (eikonal approximation)

Generated by scripts/qnm_kerr.py.

## Method

Eikonal approximation: omega = (l+1/2)*Omega_ph - i*(n+1/2)*lambda,
where Omega_ph is the photon-sphere orbital frequency and lambda the
Lyapunov exponent. This is approximate (valid for large l) and serves as
a reference for the ringdown analysis.

## Results

| quantity | value |
|---|---|
| modes computed | %d |
| l values | 2, 3, 4 |
| n values | 0, 1 |
| spin range | %.3f - %.3f |
| f_ring (l=2,n=0, a=0) | %.4f [1/M] |
| f_ring (l=2,n=0, a=0.998) | %.4f [1/M] |
| Q (l=2,n=0, a=0) | %.2f |

## Caveats

- Eikonal approximation is valid for large l; l=2 is marginal.
- Lyapunov exponent is approximate.
- A proper QNM table (e.g., from Berti et al. 2009) should replace this.

## Reproduce

    python scripts/qnm_kerr.py

Outputs: results/qnm_kerr.csv, results/qnm_kerr.png, premium/figures/qnm_kerr.html.
""" % (s["n"], s["spin_range"][0], s["spin_range"][1],
       s["freq_l2n0_a0"], s["freq_l2n0_a0998"], s["Q_l2n0_a0"])


def main() -> None:
    t = build_table()
    s = summarise(t)
    t.to_csv(OUT_CSV, index=False)
    plot(t, s)
    plotly_html(t, s)
    (PROJECT / "reports" / "qnm_kerr.md").write_text(report(t, s), encoding="utf-8")
    print("modes: %d" % s["n"])
    print("f_ring (l=2,n=0): %.4f (a=0) to %.4f (a=0.998)" % (s["freq_l2n0_a0"], s["freq_l2n0_a0998"]))
    print("wrote %s, %s, %s, reports/qnm_kerr.md" % (OUT_CSV.name, OUT_PNG.name, OUT_HTML.name))


if __name__ == "__main__":
    main()
