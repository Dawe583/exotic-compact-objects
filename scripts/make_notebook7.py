#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "07_geodesics.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Geodesic Simulations – Orbits around Compact Objects

Numerical integration of timelike geodesics (EinsteinPy) for Schwarzschild and Kerr.
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import matplotlib.pyplot as plt
from einsteinpy.geodesic import Timelike
print('ok')""")

md("## 1. Schwarzschild orbit")
code("""geod = Timelike(metric='Schwarzschild', metric_params=(), position=[40.0, np.pi/2, 0.0],
                 momentum=[0.0, 0.0, 3.83405], steps=2000, delta=1.0)
geod.calculate_trajectory()
traj = geod.trajectory[1]
r = traj[:,1]; phi = traj[:,3]
x = r*np.cos(phi); y = r*np.sin(phi)
plt.figure(figsize=(6,6))
plt.plot(x, y, lw=0.8)
# horizon
th = np.linspace(0,2*np.pi,200)
plt.plot(2*np.ones_like(th)*np.cos(th), 2*np.ones_like(th)*np.sin(th), 'k-', label='r=2M')
plt.gca().set_aspect('equal'); plt.title('Schwarzschild orbit (geometric units)')
plt.grid(True, alpha=0.3); plt.legend()
plt.savefig(str(ROOT/'figures'/'schw_orbit.png'), dpi=150)
plt.show()""")

md("## 2. Kerr orbit (a=0.9)")
code("""geod = Timelike(metric='Kerr', metric_params=(0.9,), position=[40.0, np.pi/2, 0.0],
                 momentum=[0.0, 0.0, 3.83405], steps=2000, delta=1.0)
geod.calculate_trajectory()
traj = geod.trajectory[1]
r = traj[:,1]; phi = traj[:,3]
x = r*np.cos(phi); y = r*np.sin(phi)
plt.figure(figsize=(6,6))
plt.plot(x, y, lw=0.8, color='darkred')
th = np.linspace(0,2*np.pi,200)
a=0.9
rplus = 1+np.sqrt(1-a*a)
plt.plot(rplus*np.cos(th), rplus*np.sin(th), 'k-', label='horizon')
plt.gca().set_aspect('equal'); plt.title('Kerr orbit a=0.9 (geometric units)')
plt.grid(True, alpha=0.3); plt.legend()
plt.savefig(str(ROOT/'figures'/'kerr_orbit.png'), dpi=150)
plt.show()""")

md("## 3. Radial infall profile")
code("""geod = Timelike(metric='Schwarzschild', metric_params=(), position=[20.0, np.pi/2, 0.0],
                 momentum=[0.0,0.0,0.0], steps=500, delta=0.5)
geod.calculate_trajectory()
traj = geod.trajectory[1]
t = traj[:,0]; r = traj[:,1]
plt.figure(figsize=(8,5))
plt.plot(t, r)
plt.xlabel('proper/coord time'); plt.ylabel('r (M)')
plt.title('Radial infall (Schwarzschild)'); plt.grid(True, alpha=0.3)
plt.savefig(str(ROOT/'figures'/'radial_infall.png'), dpi=150)
plt.show()""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
