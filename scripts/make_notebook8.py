#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "08_sympy_christoffel.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Christoffel Symbols via SymPy

Symbolic computation of Christoffel symbols for Schwarzschild and Morris-Thorne metrics.
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import sympy as sp
from sympy import symbols, diag, Matrix, simplify, pprint
print('ok')""")

md("## 1. Schwarzschild metric (spherical)")
code("""t,r,theta,phi = symbols('t r theta phi', real=True)
M = symbols('M', positive=True)
# geometric units c=G=1: ds^2 = -(1-2M/r)dt^2 + (1-2M/r)^-1 dr^2 + r^2 dtheta^2 + r^2 sin^2theta dphi^2
g = sp.diag(-(1-2*M/r), 1/(1-2*M/r), r**2, r**2*sp.sin(theta)**2)
coords = [t,r,theta,phi]
# Christoffel Gamma^k_{ij} = 1/2 g^{kl}(g_{li,j}+g_{lj,i}-g_{ij,l})
def christoffel(g, coords):
    n = len(coords)
    ginv = g.inv()
    Gamma = []
    for k in range(n):
        mat = []
        for i in range(n):
            row = []
            for j in range(n):
                s = sum((sp.Rational(1,2))*ginv[k,l]*(sp.diff(g[l,j],coords[i])+sp.diff(g[l,i],coords[j])-sp.diff(g[i,j],coords[l])) for l in range(n))
                row.append(sp.simplify(s))
            mat.append(row)
        Gamma.append(mat)
    return Gamma
Gamma = christoffel(g, coords)
# print a few non-zero
for k in range(4):
    for i in range(4):
        for j in range(i,4):
            val = Gamma[k][i][j]
            if val != 0:
                print(f"Gamma^{k}_{i}{j} =", val)""")

md("## 2. Morris-Thorne metric (equatorial slice)")
code("""b0 = symbols('b0', positive=True)
Phi = symbols('Phi', real=True)
# Use simple b(r)=b0^2/r and Phi=0 for throat demo; metric diag(-1, 1/(1-b/r), r^2, r^2 sin^2 theta)
g2 = sp.diag(-1, 1/(1 - (b0**2/r)/r), r**2, r**2*sp.sin(theta)**2)
coords2 = [t,r,theta,phi]
Gamma2 = christoffel(g2, coords2)
count=0
for k in range(4):
    for i in range(4):
        for j in range(i,4):
            val = Gamma2[k][i][j]
            if val != 0:
                count+=1
print('non-zero Christoffel components:', count)
# show radial ones
for i in range(4):
    print(f"Gamma^r_{i}{i} =", sp.simplify(Gamma2[1][i][i]))""")

md("## 3. Verification: Schwarzschild Christoffel matches known")
md("Check $\Gamma^r_{tt} = (M/r^2)(1-2M/r)$ etc.")
code("""val = sp.simplify(Gamma[1][0][0])
print('Gamma^r_tt =', val)
expected = (M/r**2)*(1-2*M/r)
print('expected    =', sp.simplify(expected))
print('equal?', sp.simplify(val-expected)==0)""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
