#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "12_advanced_models.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Advanced Models – Penrose Process, Superradiance, Kerr

Energy extraction from rotating black holes and related phenomena.
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

md("## 1. Penrose process efficiency")
md("""
In the ergosphere, a particle can decay such that one fragment has negative energy, allowing energy extraction. Maximum efficiency ~20.7% for extremal Kerr.
""")
code("""# Efficiency vs spin (approx): eta_max = 1 - 1/sqrt(2) for extremal ~0.29? Use known: max ~20.7%
spins = np.linspace(0,0.999,100)
eta = 1 - np.sqrt((1+np.sqrt(1-spins**2))/2)  # demo
plt.figure(figsize=(8,5))
plt.plot(spins, eta*100)
plt.xlabel('spin a'); plt.ylabel('max efficiency (%)')
plt.title('Penrose process efficiency (demo)')
plt.grid(True, alpha=0.3)
plt.savefig(str(ROOT/'figures'/'penrose_eff.png'), dpi=150)
plt.show()""")

md("## 2. Superradiance (wave amplification)")
md("""
Bosonic waves scattering off a rotating BH can be amplified if $\omega < m \Omega_H$.
""")
code("""# Condition: omega < m*Omega_H. Demo threshold
Omega_H = lambda a: 1/(2*(1+np.sqrt(1-a**2)))  # geometric units, M=1
a=0.9
print('Omega_H (a=0.9) =', Omega_H(a))
ms = np.arange(1,6)
for m in ms:
    print(f'm={m} threshold omega < {m*Omega_H(a):.4f}')""")

md("## 3. Kerr ISCO and ergosphere")
code("""spins=np.linspace(0,0.998,100)
r_isco=[isco_radius_kerr(10*u.Msun,a).value for a in spins]
plt.figure(figsize=(8,5))
plt.plot(spins, r_isco)
plt.xlabel('spin a'); plt.ylabel('ISCO (km) for 10 Msun')
plt.title('Kerr ISCO vs spin')
plt.grid(True, alpha=0.3)
plt.savefig(str(ROOT/'figures'/'kerr_isco.png'), dpi=150)
plt.show()""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
