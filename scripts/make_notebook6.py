#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "06_visual_models.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Visual Models – 3D and Interactive

Interactive 3D visualizations (Plotly) for wormhole embedding, Kerr ergosphere, etc.
HTML exports are saved to `figures/` for phone viewing.
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import plotly.graph_objects as go
from astropy import units as u
from models.equations import *
print('ok')""")

md("## 1. Morris-Thorne embedding surface (3D)")
code("""b0 = 10.0
r = np.linspace(b0, 40*b0, 60)
theta = np.linspace(0, 2*np.pi, 60)
R, T = np.meshgrid(r, theta)
Z = np.zeros_like(R)
# embedding z(r) (one side)
for i in range(R.shape[0]):
    for j in range(R.shape[1]):
        val = morris_thorne_embedding_z(np.array([R[i,j]]), b0)[0]
        Z[i,j] = val
X = R*np.cos(T)
Y = R*np.sin(T)
fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis', name='upper'),
                      go.Surface(x=X, y=Y, z=-Z, colorscale='Viridis', name='lower', showscale=False)])
fig.update_layout(title='Morris-Thorne wormhole embedding', scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'))
fig.write_html(str(ROOT/'figures'/'wormhole_embedding_3d.html'))
fig.show()
print('saved')""")

md("## 2. Schwarzschild light cone / horizon (2D polar)")
code("""import matplotlib.pyplot as plt
Rs = 1.0
theta = np.linspace(0, 2*np.pi, 200)
plt.figure(figsize=(6,6))
plt.plot(Rs*np.cos(theta), Rs*np.sin(theta), 'k-', label='Horizon')
for frac in [1.5, 2, 3, 5]:
    plt.plot(frac*Rs*np.cos(theta), frac*Rs*np.sin(theta), '--', alpha=0.5, label=f'r={frac}Rs')
plt.gca().set_aspect('equal'); plt.legend(); plt.title('Schwarzschild horizon (equatorial)')
plt.grid(True, alpha=0.3)
plt.savefig(str(ROOT/'figures'/'schwarzschild_horizon.png'), dpi=150)
plt.show()""")

md("## 3. Kerr ergosphere (equatorial) – 2D")
code("""import matplotlib.pyplot as plt
M = 1.0
a = 0.9
# ergosphere outer boundary at equator: r = 2M (in geometric units); horizon r_+
r_plus = (M + np.sqrt(M**2 - a**2))  # geometric units
theta = np.linspace(0, 2*np.pi, 200)
plt.figure(figsize=(6,6))
plt.plot(r_plus*np.cos(theta), r_plus*np.sin(theta), 'r-', label='Horizon r_+')
plt.plot(2*M*np.cos(theta), 2*M*np.sin(theta), 'b--', label='Ergosphere (equator) r=2M')
plt.gca().set_aspect('equal'); plt.legend(); plt.title('Kerr equatorial (geometric units)')
plt.grid(True, alpha=0.3)
plt.savefig(str(ROOT/'figures'/'kerr_ergosphere.png'), dpi=150)
plt.show()""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
