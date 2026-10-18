#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "10_complete_theory.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Complete Theory – Black Holes, Wormholes, White Holes

This notebook collects the **full theoretical framework** with derivations, explanations,
and consistency checks. It is written as a readable theory document with runnable code.
""")

md("""## Part I – General Relativity Basics

### 1. Metric and line element
The spacetime interval:
$$ds^2 = g_{\mu\nu}\,dx^\mu dx^\nu$$

### 2. Christoffel symbols
$$\Gamma^\lambda_{\mu\nu} = \\frac{1}{2} g^{\lambda\sigma}(\\partial_\mu g_{\nu\sigma} + \\partial_\nu g_{\mu\sigma} - \\partial_\sigma g_{\mu\nu})$$

### 3. Riemann curvature
$$R^\rho_{\ \sigma\mu\nu} = \\partial_\mu \Gamma^\rho_{\nu\sigma} - \\partial_\nu \Gamma^\rho_{\mu\sigma} + \Gamma^\rho_{\mu\lambda}\Gamma^\lambda_{\nu\sigma} - \Gamma^\rho_{\nu\lambda}\Gamma^\lambda_{\mu\sigma}$$

### 4. Ricci tensor and scalar
$$R_{\mu\nu} = R^\lambda_{\ \mu\lambda\nu}, \\qquad R = g^{\mu\nu}R_{\mu\nu}$$

### 5. Einstein equations
$$G_{\mu\nu} + \Lambda g_{\mu\nu} = \\frac{8\pi G}{c^4} T_{\mu\nu}, \\qquad G_{\mu\nu}=R_{\mu\nu}-\\frac{1}{2}R g_{\mu\nu}$$
""")

md("""## Part II – Schwarzschild Black Hole

### Derivation (vacuum, spherical symmetry)
Assume static, spherically symmetric metric:
$$ds^2 = -e^{2\Phi(r)}c^2 dt^2 + e^{2\Lambda(r)} dr^2 + r^2 d\Omega^2$$
Vacuum Einstein equations $G_{\mu\nu}=0$ give $\Phi' = -\Lambda'$ and $e^{-2\Lambda}=1-2GM/(rc^2)$.
Choosing asymptotic flatness yields Schwarzschild:
$$ds^2 = -(1-\\frac{2GM}{rc^2})c^2 dt^2 + (1-\\frac{2GM}{rc^2})^{-1} dr^2 + r^2 d\Omega^2$$

### Event horizon
$g_{tt}=0 \\Rightarrow r = 2GM/c^2 \\equiv R_s$ (Schwarzschild radius).

### Hawking temperature
Surface gravity $\kappa = c^4/(4GM)$. Quantum field theory in curved spacetime gives
$$T_H = \\frac{\hbar \kappa}{2\pi k_B c} = \\frac{\hbar c^3}{8\pi G M k_B}$$
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
from astropy import units as u
from models.equations import *
# Verify Schwarzschild radius for 1, 10, 1e6 Msun
for m in [1,10,1e6]:
    print(f"M={m:g} Msun  Rs={schwarzschild_radius(m*u.Msun).value:.4e} km  T_H={hawking_temperature(m*u.Msun).value:.4e} K")""")

md("""## Part III – White Holes

### 1. Maximal extension (Kruskal–Szekeres)
The Schwarzschild geometry has four regions:
- I: our universe (exterior)
- II: black hole interior
- III: parallel universe (other exterior)
- IV: **white hole** interior

A white hole is the time reverse of a black hole: horizon is in the past; matter/energy can only exit.

### 2. Time reversal
Schwarzschild metric is static (independent of $t$), so $t\\to -t$ is a symmetry. White hole = same geometry with reversed time orientation.

### 3. Instability
White holes are not stable equilibria. Small perturbations grow exponentially (toy model):
$$\delta(t)=\delta_0 e^{t/\tau}, \\qquad \tau \\sim GM/c^3$$
Any infalling matter triggers explosive decay. No stable white hole is expected to persist.

### 4. Hypothesized observations
- Gamma-ray bursts / fast radio bursts as explosive endpoints
- Cosmological white hole = Big Bang (speculative)
""")

md("""## Part IV – Wormholes (Morris–Thorne)

### 1. Metric
$$ds^2 = -e^{2\Phi(r)}dt^2 + (1-\\frac{b(r)}{r})^{-1}dr^2 + r^2 d\Omega^2$$
where $\Phi(r)$ is redshift function, $b(r)$ shape function.

### 2. Throat
Throat at $r=r_0$ where $b(r_0)=r_0$ (minimum radius).

### 3. Flare-out condition
At throat: $b'(r_0) < 1$ (equivalently $(b - r b')/(2b^2)>0$). This requires **exotic matter** (negative energy density) via Einstein equations.

### 4. Traversability
Requires no horizons ($\Phi$ finite everywhere) and tidal forces within human tolerance.

### 5. Embedding
The spatial slice embedding satisfies $dz/dr = \\pm \\sqrt{b/(r-b)}$.
""")

code("""import numpy as np
import matplotlib.pyplot as plt
from astropy import units as u
from models.equations import *
# Flare-out numeric check for Morris-Thorne b=b0^2/r
b0=10.0
r=np.linspace(b0*1.01, 5*b0, 200)
b=morris_thorne_shape_function(r,b0)
db=np.gradient(b,r)
num=b - r*db
print('flare-out numerator at throat (r~b0):', num[0])
print('positive?', num[0]>0)""")

md("""## Part V – Hawking Radiation and Black Hole Thermodynamics

### Hawking temperature
$$T_H = \\frac{\hbar c^3}{8\pi G M k_B}$$

### Bekenstein–Hawking entropy
$$S = \\frac{k_B c^3 A}{4 G \hbar} = \\frac{k_B c^3}{4 G \hbar} 4\pi R_s^2$$

### Four laws of black hole mechanics
1. Zeroth: surface gravity $\kappa$ is constant on horizon.
2. First: $dM = \frac{\kappa}{8\pi} dA + \Omega_H dJ + \Phi_H dQ$.
3. Second: area $A$ never decreases (classical).
4. Third: $\kappa \\to 0$ cannot be reached in finite steps.

### Evaporation
Power $P \\propto M^{-2}$; lifetime $\tau \\propto M^3$.
""")

md("""## Part VI – Observational Status

- **Black holes**: LIGO/Virgo/KAGRA GW events, EHT images (M87*, Sgr A*), X-ray binaries.
- **Wormholes**: none; constraints from lensing/GW.
- **White holes**: none; speculative.
""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
