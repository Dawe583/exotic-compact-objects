"""PTA target figure from real ATNF pulsar data."""
from pathlib import Path
import pandas as pd
import numpy as np
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "premium/figures/pta_targets.html"
df = pd.read_csv(ROOT / "data/external/atnfpulsar.csv")

# Millisecond pulsars: period < 30 ms, with a distance measurement
msp = df[(df["period"] < 0.030) & (df["distance"].notna()) & (df["distance"] > 0)].copy()
msp["P_ms"] = msp["period"] * 1000.0
# Fiducial GW residual amplitude for h=1e-15 at f=1 nHz
h = 1e-15; f_gw = 1e-9
r_ns = h / (2*np.pi*f_gw) * 1e9  # nanoseconds
# Proxy timing precision: scale with flux (brighter -> better); use 1/sqrt(flux) scaling
# If no flux, assume 1 us
flux = msp["flux_1400_mhz"].fillna(1.0).clip(lower=0.1)
sigma_us = (1.0 / np.sqrt(flux))  # microseconds, relative
sigma_us = sigma_us.clip(lower=0.1, upper=10.0)
msp["sigma_us"] = sigma_us
msp["snr_proxy"] = (r_ns / 1000.0) / sigma_us  # residual(us)/sigma(us)
top = msp.sort_values("snr_proxy", ascending=False).head(20)

fig = go.Figure()
fig.add_trace(go.Scatter(x=msp["P_ms"], y=msp["distance"], mode="markers",
    marker=dict(size=5, color=msp["snr_proxy"], colorscale="Viridis", showscale=True,
               colorbar=dict(title="SNR proxy")),
    text=msp["name"], hovertemplate="%{text}<br>P=%{x:.2f} ms<br>d=%{y:.2f} kpc<extra></extra>",
    name="MSPs"))
fig.add_trace(go.Scatter(x=top["P_ms"], y=top["distance"], mode="markers+text",
    marker=dict(size=10, color="#ff8073", symbol="star"),
    text=top["name"], textposition="top center", textfont=dict(size=9, color="#ff8073"),
    name="Top 20 PTA targets"))
fig.update_layout(template="plotly_dark",
    title="Millisecond pulsars as PTA targets (real ATNF catalog)",
    xaxis_title="Spin period (ms)", yaxis_title="Distance (kpc)", height=560,
    annotations=[dict(text=f"{len(msp)} MSPs with measured distance. "
                          f"Fiducial residual for h=1e-15 at 1 nHz: {r_ns:.0f} ns. "
                          "SNR proxy = residual / nominal timing precision (flux-scaled).",
                      xref="paper", yref="paper", x=0, y=-0.16, showarrow=False,
                      font=dict(size=11, color="#95a5c0"), align="left")],
    margin=dict(b=110))
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn")
print(OUT, "MSPs:", len(msp), "top:", top["name"].iloc[0])
