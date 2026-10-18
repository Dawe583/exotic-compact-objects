#!/usr/bin/env python3
import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from astropy import units as u
from models.equations import *
OUT = ROOT / 'premium' / 'figures'
OUT.mkdir(parents=True, exist_ok=True)
TEMPLATE = 'plotly_dark'

# 1. GWTC mass
gw = pd.read_csv(ROOT/'data/processed/gwosc_gwtc.csv')
m = gw['total_mass_source_msun'].dropna()
fig = go.Figure(go.Histogram(x=m, nbinsx=40, marker_color='#4f8cff', opacity=0.85))
fig.update_layout(template=TEMPLATE, title='GWTC compact-binary total mass', xaxis_title='Total mass (Msun)', yaxis_title='Events', bargap=0.05)
fig.write_html(str(OUT/'gw_mass.html'), include_plotlyjs='cdn')

# 2. AGN masses
agn = pd.read_csv(ROOT/'data/external/agn_bh_mass.csv', skiprows=2)
agn['logM'] = pd.to_numeric(agn['log M_BH'], errors='coerce')
fig = go.Figure(go.Histogram(x=agn['logM'], nbinsx=20, marker_color='#ff7a4f', opacity=0.85))
fig.update_layout(template=TEMPLATE, title='AGN black hole masses (reverberation)', xaxis_title='log10 M (Msun)', yaxis_title='Objects', bargap=0.05)
fig.write_html(str(OUT/'agn_mass.html'), include_plotlyjs='cdn')

# 3. Rs vs mass
masses = np.logspace(0,10,200)
rs = [schwarzschild_radius(m*u.Msun).value for m in masses]
fig = go.Figure(go.Scatter(x=masses, y=rs, mode='lines', line=dict(color='#4f8cff', width=3)))
fig.update_layout(template=TEMPLATE, title='Schwarzschild radius vs mass', xaxis_title='Mass (Msun)', yaxis_title='Rs (km)', xaxis_type='log', yaxis_type='log')
fig.write_html(str(OUT/'rs_mass.html'), include_plotlyjs='cdn')

# 4. Kerr ISCO
spins = np.linspace(0,0.998,100)
risco = [isco_radius_kerr(10*u.Msun, a).value for a in spins]
fig = go.Figure(go.Scatter(x=spins, y=risco, mode='lines', line=dict(color='#ff4f8c', width=3)))
fig.update_layout(template=TEMPLATE, title='Kerr ISCO vs spin (M=10 Msun)', xaxis_title='spin a', yaxis_title='ISCO (km)')
fig.write_html(str(OUT/'kerr_isco.html'), include_plotlyjs='cdn')

# 5. White hole decay
t = np.linspace(0,5,200)
L = np.exp(-t)
fig = go.Figure(go.Scatter(x=t, y=L, mode='lines', line=dict(color='#ffd166', width=3)))
fig.update_layout(template=TEMPLATE, title='White hole toy decay', xaxis_title='t/tau', yaxis_title='L/L0')
fig.write_html(str(OUT/'wh_decay.html'), include_plotlyjs='cdn')

# 6. 3D wormhole embedding
b0=10.0
r = np.linspace(b0, 40*b0, 50)
theta = np.linspace(0, 2*np.pi, 50)
R,T = np.meshgrid(r,theta)
Z = np.zeros_like(R)
for i in range(R.shape[0]):
    for j in range(R.shape[1]):
        Z[i,j] = morris_thorne_embedding_z(np.array([R[i,j]]), b0)[0]
X = R*np.cos(T); Y=R*np.sin(T)
fig = go.Figure()
fig.add_trace(go.Surface(x=X,y=Y,z=Z, colorscale='Viridis', showscale=False))
fig.add_trace(go.Surface(x=X,y=Y,z=-Z, colorscale='Viridis', showscale=False))
fig.update_layout(template=TEMPLATE, title='Morris-Thorne wormhole embedding', scene=dict(xaxis_title='X',yaxis_title='Y',zaxis_title='Z'))
fig.write_html(str(OUT/'wormhole_3d.html'), include_plotlyjs='cdn')

# 7. Schwarzschild orbit
from einsteinpy.geodesic import Timelike
geod = Timelike(metric='Schwarzschild', metric_params=(), position=[40.0,np.pi/2,0.0], momentum=[0.0,0.0,3.83405], steps=1000, delta=1.0)
geod.calculate_trajectory()
traj = geod.trajectory[1]
r=traj[:,1]; phi=traj[:,3]
fig = go.Figure(go.Scatter(x=r*np.cos(phi), y=r*np.sin(phi), mode='lines', line=dict(color='#4f8cff', width=1.5)))
th=np.linspace(0,2*np.pi,200)
fig.add_trace(go.Scatter(x=2*np.cos(th), y=2*np.sin(th), mode='lines', line=dict(color='white', width=2), name='horizon'))
fig.update_layout(template=TEMPLATE, title='Schwarzschild orbit', xaxis_title='x (M)', yaxis_title='y (M)', yaxis_scaleanchor='x')
fig.write_html(str(OUT/'orbit_schw.html'), include_plotlyjs='cdn')

print('premium figures done')
