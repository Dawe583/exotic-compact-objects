#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "01_exotic_compact_objects_fundamentals.ipynb"

nb = nbf.v4.new_notebook()
cells = []

def md(text): cells.append(nbf.v4.new_markdown_cell(text))
def code(text): cells.append(nbf.v4.new_code_cell(text))

md("""# Exotic Compact Objects – First Theoretical Model

**Objects:** Black holes (BH), wormholes (WH), white holes (white holes)  
**Focus:** theoretical metrics and basic equations (first pass)  
**Data:** GWOSC GWTC, HEASARC compact-object catalogs, theoretical grids

This notebook implements first-pass models:
- Schwarzschild & Kerr black holes
- Morris-Thorne wormhole
- White hole (time-reversed Schwarzschild + negative-mass demo)
""")

code("""import sys
from pathlib import Path
ROOT = Path.cwd().parent if Path.cwd().name == 'notebooks' else Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from astropy import constants as const
from astropy import units as u
from models.equations import *
print("Loaded models from", ROOT / "models")""")

md("## 1. Schwarzschild black hole – basic quantities")
code("""masses = [1, 10, 36, 29, 4.1e6, 6.5e9] * u.Msun
print(f"{'Mass (Msun)':>14} {'Rs (km)':>14} {'T_H (K)':>14} {'ISCO (km)':>14} {'r_ph (km)':>14}")
for m in masses:
    print(f"{m.value:>14.3g} {schwarzschild_radius(m).value:>14.4g} {hawking_temperature(m).value:>14.4g} {isco_radius_schwarzschild(m).value:>14.4g} {photon_sphere_radius_schwarzschild(m).value:>14.4g}")""")

code("""# Plot Rs vs mass
m_range = np.logspace(0, 10, 200) * u.Msun
rs_range = [schwarzschild_radius(m).value for m in m_range]
plt.figure(figsize=(8,5))
plt.loglog(m_range.value, rs_range)
plt.xlabel('Mass (Msun)'); plt.ylabel('Schwarzschild radius (km)')
plt.title('Schwarzschild radius vs mass')
plt.grid(True, alpha=0.3)
plt.show()""")

md("## 2. Kerr black hole – horizon vs spin")
code("""M = 10 * u.Msun
spins = np.linspace(0, 0.99, 50)
rp = [kerr_horizon_radius(M, a).value for a in spins]
plt.figure(figsize=(8,5))
plt.plot(spins, rp)
plt.xlabel('Spin a'); plt.ylabel('Outer horizon r_+ (km)')
plt.title('Kerr outer horizon vs spin (M=10 Msun)')
plt.grid(True, alpha=0.3)
plt.show()""")

md("## 3. Morris-Thorne wormhole")
code("""b0 = 10.0  # km throat scale
r = np.linspace(b0*1.01, 100*b0, 500)
g_tt, g_rr = morris_thorne_metric_components(r, b0)
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(r, g_tt); plt.xlabel('r (km)'); plt.ylabel('g_tt'); plt.title('Morris-Thorne g_tt'); plt.grid(True,alpha=0.3)
plt.subplot(1,2,2)
plt.plot(r, g_rr); plt.xlabel('r (km)'); plt.ylabel('g_rr'); plt.title('Morris-Thorne g_rr'); plt.grid(True,alpha=0.3)
plt.tight_layout(); plt.show()
print('Throat radius:', wormhole_throat_radius(b0))""")

md("## 4. White hole models")
code("""wh1 = white_hole_time_reversed_schwarzschild(10 * u.Msun)
print('Time-reversed white hole:', wh1)
wh2 = white_hole_negative_mass_radius(10)
print('Negative-mass demo radius (km):', wh2)""")

md("## 5. Data exploration – GWOSC & HEASARC")
code("""gw = pd.read_csv(ROOT / 'data' / 'processed' / 'gwosc_gwtc.csv')
print('GWOSC events:', len(gw))
print(gw[['event_id','total_mass_source_msun','network_snr']].head())
print('Mass non-null:', gw['total_mass_source_msun'].notna().sum())""")

code("""for name in ['xrbcat','m87cxo','sgraregcsc','ulxrbcat']:
    p = ROOT / 'data' / 'external' / f'{name}.csv'
    if p.exists():
        d = pd.read_csv(p)
        print(name, d.shape, list(d.columns)[:6])""")

md("## 6. Compactness comparison")
code("""objects = [
    ('Stellar BH 10Msun', 10*u.Msun, schwarzschild_radius(10*u.Msun)),
    ('Sgr A*', 4.1e6*u.Msun, schwarzschild_radius(4.1e6*u.Msun)),
    ('Wormhole b0=10km', 1*u.Msun, 10*u.km),
]
for name, m, r in objects:
    print(f"{name:22s} compactness C = {compactness(m, r):.4g}")""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print("Notebook written:", NB)
