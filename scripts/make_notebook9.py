#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "09_white_hole_extended.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# White Hole Extended – Instability, Accretion, Observational Candidates

Discussion of white-hole instability, possible observational signatures, and a toy energy-release model.
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from astropy import constants as const
from models.equations import *
print('ok')""")

md("## 1. Instability and accretion")
md("""
- White holes cannot accrete matter through the horizon; matter can only exit.
- Any small perturbation grows; equilibrium is impossible.
- Hypothesized signatures: gamma-ray bursts, fast radio bursts, or cosmological (Big Bang as white hole).
""")

md("## 2. Toy energy release")
code("""for m in [1, 10, 1e6]:
    mm = m * u.Msun
    E = (mm.to(u.kg) * const.c**2).to(u.J)
    tau = white_hole_instability_timescale(mm)
    P = (E / tau).to(u.W)
    print(f"M={m:>8g} Msun  E={E.value:.3e} J  tau={tau.value:.3e} s  P~={P.value:.3e} W")""")

md("## 3. Comparison with GRB luminosities (order of magnitude)")
code("""for m in [1, 10, 1e6]:
    mm = m * u.Msun
    tau = white_hole_instability_timescale(mm).value
    E = (mm.to(u.kg).value * (3e8)**2)
    P = E/tau
    print(f"M={m:>8g} Msun  P~={P:.3e} W  (GRB~1e45 W)  ratio={P/1e45:.3e}")""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
