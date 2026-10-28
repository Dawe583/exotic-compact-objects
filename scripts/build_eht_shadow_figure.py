"""Build an EHT shadow comparison figure (real EHT parameters)."""
from pathlib import Path
import json
import numpy as np
import plotly.graph_objects as go

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "premium/figures/eht_shadow.html"
SUMMARY = ROOT / "data/external/eht_summary.json"
s = json.loads(SUMMARY.read_text())

G = 6.67430e-11; c = 2.99792458e8; Msun = 1.98847e30; pc = 3.085677581e16

def shadow_diam(M_msun, D_mpc, spin=0.0):
    M = M_msun*Msun; D = D_mpc*1e6*pc
    theta = 2*3*np.sqrt(3)*G*M/(c**2*D) * (1 - 0.05*spin)
    return theta*(180/np.pi)*3600*1e6

names = ["M87*", "Sgr A*"]
measured = [s["m87"]["ring_diameter_uas"], s["sgra"]["ring_diameter_uas"]]
sch = [shadow_diam(s["m87"]["mass_Msun"], s["m87"]["distance_Mpc"], 0.0),
       shadow_diam(s["sgra"]["mass_Msun"], s["sgra"]["distance_kpc"]/1e3, 0.0)]
kerr = [shadow_diam(s["m87"]["mass_Msun"], s["m87"]["distance_Mpc"], 0.9),
        shadow_diam(s["sgra"]["mass_Msun"], s["sgra"]["distance_kpc"]/1e3, 0.9)]

fig = go.Figure()
fig.add_trace(go.Bar(name="Schwarzschild prediction", x=names, y=sch, marker_color="#4fb7fb",
                    text=[f"{v:.1f}" for v in sch], textposition="outside"))
fig.add_trace(go.Bar(name="Kerr (a=0.9) prediction", x=names, y=kerr, marker_color="#a48bff",
                    text=[f"{v:.1f}" for v in kerr], textposition="outside"))
fig.add_trace(go.Scatter(name="EHT measured ring", x=names, y=measured, mode="markers",
                        marker=dict(color="#ff8073", size=14, symbol="diamond"),
                        text=[f"{v:.1f}" for v in measured], textposition="top center"))
fig.update_layout(template="plotly_dark", title="EHT shadow: prediction vs measurement (real EHT parameters)",
                  yaxis_title="Angular diameter (microarcseconds)", barmode="group", height=520,
                  annotations=[dict(text="Masses and distances from EHT (2019/2022). "
                                         "Predictions use the Schwarzschild/Kerr shadow radius r = 3√3 GM/c² "
                                         "(Kerr corrected by ~5% for a=0.9). The EHT ring is a photon ring, "
                                         "not the shadow edge, hence the ~3–6% offset.",
                                    xref="paper", yref="paper", x=0, y=-0.18, showarrow=False,
                                    font=dict(size=11, color="#95a5c0"), align="left")],
                  margin=dict(b=110))
OUT.parent.mkdir(parents=True, exist_ok=True)
fig.write_html(OUT, include_plotlyjs="cdn")
print(OUT)
