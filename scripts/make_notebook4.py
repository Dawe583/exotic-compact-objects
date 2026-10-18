#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "04_white_hole_instability.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# White Hole Instability – Conceptual + Toy Model

White holes are hypothetical time-reversed black holes. In general relativity they are
expected to be **unstable**: any small perturbation grows, so a white hole cannot
remain in equilibrium. This notebook collects:
- Conceptual notes
- A toy exponential-growth model for perturbations
- Timescale estimates
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

md("## 1. Key ideas")
md("""
- A white hole has an event horizon that matter/energy can only exit, not enter.
- Small perturbations are amplified; the horizon is unstable to infalling matter.
- Hypothesized outcomes: explosion, transition to black hole, or connection to Big Bang/cosmology.
- No direct observational evidence; models are speculative.
""")

md("## 2. Instability timescale")
code("""for m in [1, 10, 36, 4.1e6]:
    mm = m * u.Msun
    tau = white_hole_instability_timescale(mm)
    print(f"M={m:>10g} Msun  tau_instability ~ {tau.value:.3e} s ({tau.to(u.yr).value:.3e} yr)")""")

md("## 3. Perturbation growth")
code("""M = 10 * u.Msun
t = np.linspace(0, 5*white_hole_instability_timescale(M).value, 200)
delta = white_hole_perturbation_growth(t, 1e-6, M)
plt.figure(figsize=(8,5))
plt.semilogy(t/white_hole_instability_timescale(M).value, delta)
plt.xlabel('t / tau'); plt.ylabel('perturbation amplitude')
plt.title('Toy perturbation growth (white hole)')
plt.grid(True, alpha=0.3); plt.show()""")

md("## 4. Comparison with black hole stability")
md("""
- Black holes are stable to small perturbations (ringdown damps).
- White holes lack a stable equilibrium; perturbations grow exponentially (toy model).
- This asymmetry is one reason white holes are not expected to persist.
""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
