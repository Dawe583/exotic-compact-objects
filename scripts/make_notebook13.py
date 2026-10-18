#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "13_white_hole_deep_dive.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# White Hole Deep Dive – Maximal Extension, Instability, Observables

A focused treatment of white holes: geometry, instability, and possible signatures.
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

md("## 1. Maximal extension (Kruskal–Szekeres)")
md("""
Regions:
- I: exterior (our universe)
- II: black hole interior
- III: other exterior
- IV: white hole interior

White hole horizon is in the past; no matter can enter, only exit.
""")

md("## 2. Instability timescales")
code("""for m in [0.1, 1, 10, 100, 1e6]:
    mm = m*u.Msun
    tau = white_hole_instability_timescale(mm)
    print(f"M={m:>8g} Msun  tau={tau.value:.3e} s = {tau.to(u.yr).value:.3e} yr")""")

md("## 3. Toy explosion light curve")
code("""# L(t) = L0 * exp(-t/tau) for t>0
tau = 1.0
t = np.linspace(0, 5, 200)
L = np.exp(-t/tau)
plt.figure(figsize=(8,5))
plt.plot(t, L)
plt.xlabel('t/tau'); plt.ylabel('L/L0')
plt.title('Toy white-hole decay (exponential)')
plt.grid(True, alpha=0.3)
plt.savefig(str(ROOT/'figures'/'wh_decay.png'), dpi=150)
plt.show()""")

md("## 4. Comparison with black hole (stability)")
md("""
- BH: perturbations damp (ringdown).
- WH: perturbations grow (unstable).
- This asymmetry makes persistent white holes unlikely.
""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
