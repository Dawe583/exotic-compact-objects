"""AGN reverberation-mapped mass distribution figure (real data)."""
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "premium/figures/agn_mass_distribution.html"
df = pd.read_csv(ROOT / "data/processed/agn_reverberation_masses.csv")

fig = make_subplots(rows=1, cols=2, subplot_titles=("Mass distribution", "Eddington luminosity vs mass"))
fig.add_trace(go.Histogram(x=df["log10_mass_msun"], nbinsx=18, marker_color="#a48bff",
                          name="log10 M (M☉)"), row=1, col=1)
# Eddington luminosity line + scatter
M = df["mass_msun"].values
Ledd = 1.26e31 * M  # erg/s for M in Msun? 1.26e38 * (M/Msun) erg/s -> in erg/s
fig.add_trace(go.Scatter(x=np.log10(M), y=np.log10(Ledd), mode="lines",
                        line=dict(color="#ff8073", dash="dash"), name="L_Edd (Eddington)"), row=1, col=2)
fig.add_trace(go.Scatter(x=np.log10(M), y=np.log10(df["eddington_luminosity_erg_s"]),
                        mode="markers", marker=dict(color="#2fe3ac", size=7),
                        text=df["name"], hovertemplate="%{text}<br>log M=%{x:.2f}<extra></extra>",
                        name="Catalog L_Edd"), row=1, col=2)
fig.update_xaxes(title_text="log10(M/M☉)", row=1, col=1)
fig.update_xaxes(title_text="log10(M/M☉)", row=1, col=2)
fig.update_yaxes(title_text="Count", row=1, col=1)
fig.update_yaxes(title_text="log10 L (erg/s)", row=1, col=2)
fig.update_layout(template="plotly_dark", title="AGN reverberation-mapped masses (real data, 70 sources)",
                  height=520, showlegend=True,
                  annotations=[dict(text=f"N={len(df)}, median log M={df['log10_mass_msun'].median():.2f}, "
                                        f"z median={df['redshift'].median():.3f}. "
                                        "Reverberation mapping = broad-line response delay + line width.",
                                    xref="paper", yref="paper", x=0, y=-0.12, showarrow=False,
                                    font=dict(size=11, color="#95a5c0"), align="left")],
                  margin=dict(b=90))
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn")
print(OUT, "N=", len(df))
