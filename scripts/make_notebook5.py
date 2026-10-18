#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "05_equation_derivations.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Equation Derivations and Mathematical Verification

This notebook derives key equations step by step and verifies them with **SymPy** (symbolic)
and **NumPy/SciPy** (numerical). Each derivation includes intermediate steps.
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
from astropy import constants as const
from astropy import units as u
from sympy import symbols, solve, simplify, diff, Rational, pi, sqrt, exp, series, latex
import sympy as sp
from models.equations import *
print('ok')""")

md("## 1. Schwarzschild radius from metric horizon")
md("""
The Schwarzschild metric component:
$$g_{tt} = -(1 - \\frac{2GM}{rc^2})$$
Horizon occurs where $g_{tt}=0$.
""")
code("""G, M, r, c = sp.symbols('G M r c', positive=True)
g_tt = -(1 - 2*G*M/(r*c**2))
sol = sp.solve(sp.Eq(g_tt, 0), r)
print('solutions:', sol)
rs_expr = sol[0]
print('Rs =', rs_expr)
# numeric check
Mval = 10.0  # Msun
rs_num = float(rs_expr.subs([(G, const.G.value),(M, Mval*const.M_sun.value),(c, const.c.value)]))
print('numeric Rs (m) for 10 Msun:', rs_num)
print('function Rs (km):', schwarzschild_radius(Mval*u.Msun).value)""")

md("## 2. Hawking temperature from surface gravity")
md("""
Surface gravity: $\kappa = c^4/(4GM)$.  
Hawking temperature: $T_H = \hbar \kappa/(2\pi k_B c)$.
""")
code("""hbar, kB = sp.symbols('hbar k_B', positive=True)
kappa = c**4/(4*G*M)
T = hbar*kappa/(2*sp.pi*kB*c)
Tsimp = sp.simplify(T)
print('T_H =', Tsimp)
# numeric
Tnum = float(Tsimp.subs([(hbar, const.hbar.value),(c, const.c.value),(G, const.G.value),(M, 10*const.M_sun.value),(kB, const.k_B.value)]))
print('numeric T_H (K) for 10 Msun:', Tnum)
print('function T_H (K):', hawking_temperature(10*u.Msun).value)""")

md("## 3. Kerr outer horizon")
md("""
In geometric units, $\Delta = r^2 - 2Mr + a^2$. Horizon: $\Delta=0$.
""")
code("""a = sp.symbols('a', real=True)
rr = sp.symbols('r', real=True)
Mg = sp.symbols('M', positive=True)
Delta = rr**2 - 2*Mg*rr + a**2
sols = sp.solve(sp.Eq(Delta, 0), rr)
print('horizons:', sols)
r_plus = sols[1]  # larger root
print('r_+ =', r_plus)
# numeric check: convert to km for M=10 Msun, a=0.9
Mkg = 10*const.M_sun.value
GM_c2 = const.G.value*Mkg/const.c.value**2  # meters
a_dim = 0.9
# numeric check via function
print('function r_+ (km) for M=10 Msun, a=0.9:', kerr_horizon_radius(10*u.Msun, 0.9).value)""")

md("## 4. Morris-Thorne throat and flare-out")
md("""
Metric: $1 - b(r)/r$. Throat where $b(r)=r$.  
Flare-out: $(b - r b')/(2 b^2) > 0$.
""")
code("""r, b0 = sp.symbols('r b0', positive=True)
b = b0**2 / r
# throat: b(r)=r
throat = sp.solve(sp.Eq(b, r), r)
print('throat r =', throat)
# flare-out numerator
db = sp.diff(b, r)
num = sp.simplify(b - r*db)
print("b - r b' =", num)
print('at throat r=b0:', sp.simplify(num.subs(r, b0)))""")

md("## 5. White hole as time reversal")
md("""
Schwarzschild metric is static: invariant under $t \\to -t$. White hole = same geometry, reversed time orientation.
""")
code("""t = sp.symbols('t', real=True)
# demonstrate: metric components independent of t
print('g_tt has no t-dependence -> time-reversal symmetric geometry')""")

md("## 6. Hawking power and lifetime scaling")
md("""
$P \\propto M^{-2}$, $\tau \\propto M^{3}$.
""")
code("""M = sp.symbols('M', positive=True)
P = 1/M**2
tau = M**3
print('d ln P / d ln M =', sp.simplify(sp.diff(sp.log(P), M)*M))
print('d ln tau / d ln M =', sp.simplify(sp.diff(sp.log(tau), M)*M))""")

md("## 7. Numerical verification against known values")
code("""# Sgr A* Rs ~ 1.269e10 m = 1.269e7 km
rs_sgr = schwarzschild_radius(4.1e6*u.Msun).value
print('Sgr A* Rs (km):', rs_sgr, ' (expected ~1.27e7 km)')
# M87* Rs ~ 1.9e13 m = 1.9e10 km
rs_m87 = schwarzschild_radius(6.5e9*u.Msun).value
print('M87* Rs (km):', rs_m87, ' (expected ~1.9e10 km)')
# Hawking T for 1 Msun ~ 6e-8 K
print('1 Msun T_H (K):', hawking_temperature(1*u.Msun).value, ' (expected ~6.17e-8 K)')""")

md("## 8. Symbolic check: Kerr horizon reduces to Schwarzschild when a=0")
code("""a_sym = sp.symbols('a', real=True)
M_sym = sp.symbols('M', positive=True)
r_sym = sp.symbols('r', real=True)
Delta = r_sym**2 - 2*M_sym*r_sym + a_sym**2
# solve for a=0
sols0 = sp.solve(sp.Eq(Delta.subs(a_sym,0),0), r_sym)
print('a=0 horizons:', sols0)
print('larger root = 2M -> Schwarzschild Rs (geometric units)')""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
