#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "02_extended_models.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Extended Models – Geodesics, ISCO, Wormhole Throat, Hawking Radiation

Extends the first model with:
- Kerr ISCO vs spin
- Effective potential (Schwarzschild timelike geodesics)
- Morris-Thorne flare-out + embedding
- Hawking radiation power/lifetime + white-hole analog
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from models.equations import *
print('ok')""")

md("## 1. Kerr ISCO radius vs spin")
code("""M = 10 * u.Msun
spins = np.linspace(0, 0.998, 100)
r_isco = [isco_radius_kerr(M, a).value for a in spins]
plt.figure(figsize=(8,5))
plt.plot(spins, r_isco)
plt.xlabel('Spin a'); plt.ylabel('ISCO radius (km)')
plt.title('Kerr ISCO vs spin (M=10 Msun)')
plt.grid(True, alpha=0.3); plt.show()""")

md("## 2. Effective potential (Schwarzschild)")
code("""M = 1 * u.Msun
Rs = schwarzschild_radius(M).value
r = np.linspace(Rs*1.1, 50*Rs, 500)
plt.figure(figsize=(8,5))
for L in [0, 3, 5, 8]:
    V = effective_potential_schwarzschild(r, M, L)
    plt.plot(r/Rs, V, label=f'L={L}')
plt.axvline(3, color='k', ls='--', alpha=0.5, label='ISCO~6? (3Rs)')
plt.xlabel('r / Rs'); plt.ylabel('V_eff'); plt.title('Effective potential (Schwarzschild)')
plt.legend(); plt.grid(True, alpha=0.3); plt.ylim(-1,3); plt.show()""")

md("## 3. Morris-Thorne: shape function & flare-out")
code("""b0 = 10.0
r = np.linspace(b0*1.01, 50*b0, 400)
b = morris_thorne_shape_function(r, b0)
db = np.gradient(b, r)
flare = flare_out_condition(b, db)
plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.plot(r, b, label='b(r)'); plt.plot(r, r, '--', label='r')
plt.xlabel('r (km)'); plt.ylabel('b(r)'); plt.legend(); plt.title('Shape function'); plt.grid(True,alpha=0.3)
plt.subplot(1,2,2)
plt.plot(r, flare)
plt.axhline(0, color='k', ls='--')
plt.xlabel('r (km)'); plt.ylabel("b - b' r"); plt.title('Flare-out numerator'); plt.grid(True,alpha=0.3)
plt.tight_layout(); plt.show()""")

md("## 4. Embedding diagram (Morris-Thorne)")
code("""b0 = 10.0
r = np.linspace(b0, 40*b0, 300)
z = morris_thorne_embedding_z(r, b0)
plt.figure(figsize=(8,5))
plt.plot(r, z, label='z(r)')
plt.plot(r, -z, label='-z(r)')
plt.xlabel('r (km)'); plt.ylabel('z (km)'); plt.title('Embedding diagram (throat at r=b0)')
plt.legend(); plt.grid(True, alpha=0.3); plt.show()""")

md("## 5. Hawking radiation")
code("""for m in [1, 10, 36, 4.1e6]:
    mm = m * u.Msun
    print(f"M={m:>10g} Msun  T_H={hawking_temperature(mm).value:.3e} K  P={hawking_power(mm).value:.3e} W  tau={hawking_lifetime(mm).value:.3e} s")""")

code("""# Lifetime vs mass
ms = np.logspace(0, 8, 50) * u.Msun
taus = [hawking_lifetime(m).value for m in ms]
plt.figure(figsize=(8,5))
plt.loglog(ms.value, taus)
plt.xlabel('Mass (Msun)'); plt.ylabel('Evaporation time (s)')
plt.title('Hawking lifetime vs mass'); plt.grid(True, alpha=0.3); plt.show()""")

md("## 6. White hole analog")
code("""for m in [1, 10, 36]:
    mm = m * u.Msun
    print(f"M={m} Msun  BH T_H={hawking_temperature(mm).value:.3e} K  white-hole analog T={white_hole_hawking_analog(mm).value:.3e} K")""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
