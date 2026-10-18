#!/usr/bin/env python3
"""
Create advanced animations for exotic compact objects research.
Generates both Plotly (interactive HTML) and matplotlib (MP4/GIF) animations.
"""

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
from mpl_toolkits.mplot3d import Axes3D
import os
import warnings
warnings.filterwarnings('ignore')

# Ensure output directory exists
output_dir = "/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects/premium/figures"
os.makedirs(output_dir, exist_ok=True)

# ============================================================
# 1. BH MERGER ANIMATION - Inspiral, Merger, Ringdown
# ============================================================
print("Creating BH Merger Animation...")

# Time arrays for three phases
t_inspiral = np.linspace(-100, -5, 200)
t_merger = np.linspace(-5, 5, 100)
t_ringdown = np.linspace(5, 50, 150)

# Inspiral: chirp signal (avoid negative base for fractional powers)
tau = 100 + t_inspiral  # tau goes from 0 to 95
# Add small epsilon to avoid division by zero at tau=0
eps = 1e-10
tau_safe = np.maximum(tau, eps)
f_inspiral = 20 * (tau_safe/100)**(-3/8)
h_inspiral = (tau_safe/100)**(-1/4) * np.sin(2*np.pi * np.cumsum(f_inspiral) * (t_inspiral[1]-t_inspiral[0]))

# Merger: peak amplitude
h_merger = 3 * np.exp(-((t_merger)/1.5)**2) * np.sin(2*np.pi*150*t_merger + 0.5*t_merger**2)

# Ringdown: damped sinusoid
h_ringdown = 2 * np.exp(-(t_ringdown-5)/10) * np.sin(2*np.pi*250*(t_ringdown-5))

# Combine
t_all = np.concatenate([t_inspiral, t_merger, t_ringdown])
h_all = np.concatenate([h_inspiral, h_merger, h_ringdown])

# --- Plotly Animation ---
fig_bh = go.Figure()

# Initial trace
fig_bh.add_trace(go.Scatter(
    x=t_all[:1], y=h_all[:1],
    mode='lines', line=dict(color='#00d4ff', width=2),
    name='Strain h(t)'
))

# Add frames
frames = []
n_frames = 150
for i in range(1, len(t_all), max(1, len(t_all)//n_frames)):
    frames.append(go.Frame(
        data=[go.Scatter(x=t_all[:i], y=h_all[:i])],
        name=f"frame{i}"
    ))
fig_bh.frames = frames

# Layout with slider
fig_bh.update_layout(
    title="Binary Black Hole Merger: Inspiral → Merger → Ringdown",
    xaxis_title="Time (M)",
    yaxis_title="Strain h(t)",
    template="plotly_dark",
    width=1000, height=500,
    sliders=[dict(
        active=0,
        steps=[dict(method="animate", args=[[f"frame{i}"], dict(mode="immediate", frame=dict(duration=30, redraw=True), transition=dict(duration=0))], label="") for i in range(len(frames))],
        x=0.1, y=0, len=0.9
    )],
    updatemenus=[dict(type="buttons", showactive=False,
        buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=30, redraw=True), fromcurrent=True)]),
                 dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])],
        x=0.05, y=1.05)]
)

fig_bh.write_html(f"{output_dir}/bh_merger_animation.html")

# --- Matplotlib Animation ---
fig, ax = plt.subplots(figsize=(12, 5), facecolor='#0d1117')
ax.set_facecolor('#0d1117')
line, = ax.plot([], [], color='#00d4ff', linewidth=2)
ax.set_xlim(t_all[0], t_all[-1])
ax.set_ylim(1.2*h_all.min(), 1.2*h_all.max())
ax.set_xlabel('Time (M)', color='white', fontsize=12)
ax.set_ylabel('Strain h(t)', color='white', fontsize=12)
ax.set_title('BH Merger: Inspiral → Merger → Ringdown', color='white', fontsize=14)
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('white')

# Phase markers
ax.axvspan(-100, -5, alpha=0.1, color='cyan', label='Inspiral')
ax.axvspan(-5, 5, alpha=0.2, color='yellow', label='Merger')
ax.axvspan(5, 50, alpha=0.1, color='orange', label='Ringdown')
ax.legend(loc='upper right', facecolor='#161b22', edgecolor='white', labelcolor='white')

def update_bh(frame):
    idx = min(frame * (len(t_all)//150), len(t_all)-1)
    line.set_data(t_all[:idx], h_all[:idx])
    return line,

anim_bh = animation.FuncAnimation(fig, update_bh, frames=150, interval=30, blit=True)
anim_bh.save(f"{output_dir}/bh_merger_animation.mp4", writer='ffmpeg', fps=30, dpi=150)
anim_bh.save(f"{output_dir}/bh_merger_animation.gif", writer=PillowWriter(fps=20))
plt.close()

print("  ✓ BH Merger Animation created")

# ============================================================
# 2. KERR ERGOSPHERE PRECESSION
# ============================================================
print("Creating Kerr Ergosphere Precession Animation...")

# Kerr metric parameters
a = 0.9  # spin parameter
M = 1.0

# Ergosphere boundaries
theta = np.linspace(0, np.pi, 100)
r_ergo = M + np.sqrt(M**2 - a**2 * np.cos(theta)**2)
r_horizon = M + np.sqrt(M**2 - a**2)

# Particle orbit in ergosphere (precessing ellipse)
def particle_orbit(t, a=0.9):
    # Simplified precessing orbit in ergosphere
    r0 = 1.8
    ecc = 0.3
    phi_dot = 0.8  # orbital frequency
    prec = 0.15    # precession rate
    
    phi = phi_dot * t
    r = r0 * (1 - ecc * np.cos(phi))
    phi_prec = phi + prec * t
    
    x = r * np.sin(np.pi/2) * np.cos(phi_prec)
    y = r * np.sin(np.pi/2) * np.sin(phi_prec)
    z = r * np.cos(np.pi/2)
    return x, y, z, r, phi_prec

# --- Plotly 3D Animation ---
fig_kerr = go.Figure()

# Ergosphere surface
x_ergo = r_ergo[:, None] * np.sin(theta[:, None]) * np.cos(np.linspace(0, 2*np.pi, 50))
y_ergo = r_ergo[:, None] * np.sin(theta[:, None]) * np.sin(np.linspace(0, 2*np.pi, 50))
z_ergo = r_ergo[:, None] * np.cos(theta[:, None])

fig_kerr.add_trace(go.Surface(
    x=x_ergo, y=y_ergo, z=z_ergo,
    colorscale='Viridis', opacity=0.3, showscale=False,
    name='Ergosphere'
))

# Horizon
r_h = r_horizon
phi_h = np.linspace(0, 2*np.pi, 50)
th_h = np.linspace(0, np.pi, 30)
PHI, TH = np.meshgrid(phi_h, th_h)
x_h = r_h * np.sin(TH) * np.cos(PHI)
y_h = r_h * np.sin(TH) * np.sin(PHI)
z_h = r_h * np.cos(TH)

fig_kerr.add_trace(go.Surface(
    x=x_h, y=y_h, z=z_h,
    colorscale=[[0, '#ff6b6b'], [1, '#ff6b6b']], opacity=0.6, showscale=False,
    name='Event Horizon'
))

# Particle trajectory
t_vals = np.linspace(0, 100, 500)
traj = np.array([particle_orbit(t) for t in t_vals])
x_traj, y_traj, z_traj = traj[:, 0], traj[:, 1], traj[:, 2]

fig_kerr.add_trace(go.Scatter3d(
    x=x_traj[:1], y=y_traj[:1], z=z_traj[:1],
    mode='lines+markers', line=dict(color='#ffd700', width=4),
    marker=dict(size=8, color='#ffd700'),
    name='Particle'
))

# Frames
frames_kerr = []
for i in range(0, len(t_vals), 5):
    frames_kerr.append(go.Frame(
        data=[
            go.Surface(x=x_ergo, y=y_ergo, z=z_ergo),
            go.Surface(x=x_h, y=y_h, z=z_h),
            go.Scatter3d(x=x_traj[:i], y=y_traj[:i], z=z_traj[:i],
                        mode='lines+markers', line=dict(color='#ffd700', width=4),
                        marker=dict(size=8, color='#ffd700'))
        ],
        name=f"frame{i}"
    ))
fig_kerr.frames = frames_kerr

fig_kerr.update_layout(
    title="Kerr Ergosphere: Particle Orbit Precession (a=0.9M)",
    scene=dict(
        xaxis_title='X (M)', yaxis_title='Y (M)', zaxis_title='Z (M)',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
        bgcolor='#0d1117'
    ),
    template="plotly_dark", width=900, height=700,
    sliders=[dict(active=0, steps=[dict(method="animate", args=[[f"frame{i}"], dict(mode="immediate", frame=dict(duration=50, redraw=True))], label="") for i in range(len(frames_kerr))], x=0.1, y=0, len=0.9)],
    updatemenus=[dict(type="buttons", showactive=False,
        buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]),
                 dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])],
        x=0.05, y=1.05)]
)

fig_kerr.write_html(f"{output_dir}/kerr_ergosphere_precession.html")

# --- Matplotlib 3D Animation ---
fig = plt.figure(figsize=(10, 8), facecolor='#0d1117')
ax = fig.add_subplot(111, projection='3d', facecolor='#0d1117')

# Ergosphere wireframe
theta_m = np.linspace(0, np.pi, 30)
phi_m = np.linspace(0, 2*np.pi, 40)
TH, PHI = np.meshgrid(theta_m, phi_m)
R_ergo = M + np.sqrt(M**2 - a**2 * np.cos(TH)**2)
X_ergo = R_ergo * np.sin(TH) * np.cos(PHI)
Y_ergo = R_ergo * np.sin(TH) * np.sin(PHI)
Z_ergo = R_ergo * np.cos(TH)
ax.plot_surface(X_ergo, Y_ergo, Z_ergo, alpha=0.2, color='cyan', rstride=2, cstride=2)

# Horizon
R_h = r_horizon
X_h = R_h * np.sin(TH) * np.cos(PHI)
Y_h = R_h * np.sin(TH) * np.sin(PHI)
Z_h = R_h * np.cos(TH)
ax.plot_surface(X_h, Y_h, Z_h, alpha=0.5, color='red', rstride=2, cstride=2)

# Particle trajectory line
traj_line, = ax.plot([], [], [], color='#ffd700', linewidth=2)
particle, = ax.plot([], [], [], 'o', color='#ffd700', markersize=10)

ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 3)
ax.set_xlabel('X (M)', color='white')
ax.set_ylabel('Y (M)', color='white')
ax.set_zlabel('Z (M)', color='white')
ax.set_title('Kerr Ergosphere Precession (a=0.9M)', color='white', fontsize=14)
ax.tick_params(colors='white')

def update_kerr(frame):
    idx = min(frame * 5, len(t_vals)-1)
    traj_line.set_data(x_traj[:idx], y_traj[:idx])
    traj_line.set_3d_properties(z_traj[:idx])
    particle.set_data([x_traj[idx]], [y_traj[idx]])
    particle.set_3d_properties([z_traj[idx]])
    return traj_line, particle

anim_kerr = animation.FuncAnimation(fig, update_kerr, frames=100, interval=50, blit=True)
anim_kerr.save(f"{output_dir}/kerr_ergosphere_precession.mp4", writer='ffmpeg', fps=20, dpi=150)
anim_kerr.save(f"{output_dir}/kerr_ergosphere_precession.gif", writer=PillowWriter(fps=15))
plt.close()

print("  ✓ Kerr Ergosphere Precession created")

# ============================================================
# 3. WORMHOLE TRAVERSAL - Camera flying through Morris-Thorne throat
# ============================================================
print("Creating Wormhole Traversal Animation...")

# Morris-Thorne wormhole: ds² = -dt² + dl² + (b₀² + l²)(dθ² + sin²θ dφ²)
# Shape function b(r) = b₀²/r, throat at r = b₀
b0 = 1.0

# Camera path through throat
l_vals = np.linspace(-8, 8, 200)  # proper radial coordinate
# Camera position: moving along l-axis through throat
# Visualize as 3D embedding: x = sqrt(r² - b₀²) cos φ, y = sqrt(r² - b₀²) sin φ, z = ±b₀ ln(r/b₀ + sqrt(r²/b₀² - 1))

def wormhole_embedding(l):
    r = np.sqrt(b0**2 + l**2)
    # Embedding function z(r)
    if r > b0:
        z = b0 * np.log(r/b0 + np.sqrt(r**2/b0**2 - 1))
    else:
        z = 0
    return r, z

# Create wormhole surface for visualization
phi = np.linspace(0, 2*np.pi, 60)
l_surf = np.linspace(-5, 5, 80)
PHI, L = np.meshgrid(phi, l_surf)
R_surf = np.sqrt(b0**2 + L**2)
Z_surf = np.zeros_like(L)
for i in range(len(l_surf)):
    r_val = np.sqrt(b0**2 + l_surf[i]**2)
    if r_val > b0:
        Z_surf[i, :] = b0 * np.log(r_val/b0 + np.sqrt(r_val**2/b0**2 - 1))
    else:
        Z_surf[i, :] = 0

X_surf = R_surf * np.cos(PHI)
Y_surf = R_surf * np.sin(PHI)

# Camera path
l_cam = np.linspace(-8, 8, 200)
r_cam = np.sqrt(b0**2 + l_cam**2)
z_cam = np.array([wormhole_embedding(l)[1] for l in l_cam])
x_cam = r_cam * np.cos(0.3 * l_cam)  # spiraling view
y_cam = r_cam * np.sin(0.3 * l_cam)

# --- Plotly Animation ---
fig_wh = go.Figure()

# Wormhole surface
fig_wh.add_trace(go.Surface(
    x=X_surf, y=Y_surf, z=Z_surf,
    colorscale='Plasma', opacity=0.4, showscale=False,
    name='Wormhole Throat'
))

# Other side (negative z)
fig_wh.add_trace(go.Surface(
    x=X_surf, y=Y_surf, z=-Z_surf,
    colorscale='Plasma', opacity=0.4, showscale=False,
    showlegend=False
))

# Camera position
fig_wh.add_trace(go.Scatter3d(
    x=[x_cam[0]], y=[y_cam[0]], z=[z_cam[0]],
    mode='markers', marker=dict(size=12, color='#00ff00', symbol='diamond'),
    name='Camera'
))

# Camera trail
fig_wh.add_trace(go.Scatter3d(
    x=x_cam[:1], y=y_cam[:1], z=z_cam[:1],
    mode='lines', line=dict(color='#00ff00', width=3),
    name='Path'
))

frames_wh = []
for i in range(0, len(l_cam), 2):
    frames_wh.append(go.Frame(
        data=[
            go.Surface(x=X_surf, y=Y_surf, z=Z_surf),
            go.Surface(x=X_surf, y=Y_surf, z=-Z_surf),
            go.Scatter3d(x=[x_cam[i]], y=[y_cam[i]], z=[z_cam[i]],
                        mode='markers', marker=dict(size=12, color='#00ff00', symbol='diamond')),
            go.Scatter3d(x=x_cam[:i], y=y_cam[:i], z=z_cam[:i],
                        mode='lines', line=dict(color='#00ff00', width=3))
        ],
        name=f"frame{i}"
    ))
fig_wh.frames = frames_wh

fig_wh.update_layout(
    title="Morris-Thorne Wormhole Traversal: Camera Flythrough",
    scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
        camera=dict(eye=dict(x=2, y=0, z=1.5)),
        bgcolor='#0d1117'
    ),
    template="plotly_dark", width=900, height=700,
    sliders=[dict(active=0, steps=[dict(method="animate", args=[[f"frame{i}"], dict(mode="immediate", frame=dict(duration=50, redraw=True))], label="") for i in range(len(frames_wh))], x=0.1, y=0, len=0.9)],
    updatemenus=[dict(type="buttons", showactive=False,
        buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]),
                 dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])],
        x=0.05, y=1.05)]
)

fig_wh.write_html(f"{output_dir}/wormhole_traversal.html")

# --- Matplotlib Animation ---
fig = plt.figure(figsize=(12, 8), facecolor='#0d1117')
ax = fig.add_subplot(111, projection='3d', facecolor='#0d1117')

# Plot wormhole surfaces
ax.plot_surface(X_surf, Y_surf, Z_surf, alpha=0.3, cmap='plasma', rstride=2, cstride=2)
ax.plot_surface(X_surf, Y_surf, -Z_surf, alpha=0.3, cmap='plasma', rstride=2, cstride=2)

cam_trail, = ax.plot([], [], [], color='#00ff00', linewidth=2, alpha=0.7)
cam_pos, = ax.plot([], [], [], 'D', color='#00ff00', markersize=12)

ax.set_xlim(-6, 6)
ax.set_ylim(-6, 6)
ax.set_zlim(-6, 6)
ax.set_xlabel('X', color='white')
ax.set_ylabel('Y', color='white')
ax.set_zlabel('Z', color='white')
ax.set_title('Morris-Thorne Wormhole Traversal', color='white', fontsize=14)
ax.tick_params(colors='white')

def update_wh(frame):
    idx = min(frame * 2, len(l_cam)-1)
    cam_trail.set_data(x_cam[:idx], y_cam[:idx])
    cam_trail.set_3d_properties(z_cam[:idx])
    cam_pos.set_data([x_cam[idx]], [y_cam[idx]])
    cam_pos.set_3d_properties([z_cam[idx]])
    return cam_trail, cam_pos

anim_wh = animation.FuncAnimation(fig, update_wh, frames=100, interval=50, blit=True)
anim_wh.save(f"{output_dir}/wormhole_traversal.mp4", writer='ffmpeg', fps=20, dpi=150)
anim_wh.save(f"{output_dir}/wormhole_traversal.gif", writer=PillowWriter(fps=15))
plt.close()

print("  ✓ Wormhole Traversal created")

# ============================================================
# 4. WHITE HOLE EXPLOSION - Expanding shell
# ============================================================
print("Creating White Hole Explosion Animation...")

# White hole: time-reversed black hole, matter/energy explodes outward
# Simulate expanding spherical shell with decreasing density
r_shell = np.linspace(0.5, 10, 50)  # shell radii over time
theta = np.linspace(0, np.pi, 40)
phi = np.linspace(0, 2*np.pi, 60)
TH, PHI = np.meshgrid(theta, phi)

# --- Plotly Animation ---
fig_wh_exp = go.Figure()

# Initial shell
r0 = r_shell[0]
X0 = r0 * np.sin(TH) * np.cos(PHI)
Y0 = r0 * np.sin(TH) * np.sin(PHI)
Z0 = r0 * np.cos(TH)

fig_wh_exp.add_trace(go.Surface(
    x=X0, y=Y0, z=Z0,
    colorscale=[[0, '#ff6b6b'], [0.5, '#ffd700'], [1, '#ffffff']],
    opacity=0.7, showscale=False, name='Ejecta Shell'
))

# Central remnant
fig_wh_exp.add_trace(go.Scatter3d(
    x=[0], y=[0], z=[0],
    mode='markers', marker=dict(size=20, color='white', symbol='circle'),
    name='Central Engine'
))

frames_wh_exp = []
for i, r in enumerate(r_shell):
    X = r * np.sin(TH) * np.cos(PHI)
    Y = r * np.sin(TH) * np.sin(PHI)
    Z = r * np.cos(TH)
    opacity = 0.7 * np.exp(-r/8)  # fading as expands
    frames_wh_exp.append(go.Frame(
        data=[
            go.Surface(x=X, y=Y, z=Z,
                      colorscale=[[0, '#ff6b6b'], [0.5, '#ffd700'], [1, '#ffffff']],
                      opacity=opacity, showscale=False),
            go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
                        marker=dict(size=20, color='white'))
        ],
        name=f"frame{i}"
    ))
fig_wh_exp.frames = frames_wh_exp

fig_wh_exp.update_layout(
    title="White Hole Explosion: Expanding Ejecta Shell",
    scene=dict(
        xaxis_title='X', yaxis_title='Y', zaxis_title='Z',
        camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)),
        bgcolor='#0d1117'
    ),
    template="plotly_dark", width=900, height=700,
    sliders=[dict(active=0, steps=[dict(method="animate", args=[[f"frame{i}"], dict(mode="immediate", frame=dict(duration=80, redraw=True))], label="") for i in range(len(frames_wh_exp))], x=0.1, y=0, len=0.9)],
    updatemenus=[dict(type="buttons", showactive=False,
        buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=80, redraw=True), fromcurrent=True)]),
                 dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])],
        x=0.05, y=1.05)]
)

fig_wh_exp.write_html(f"{output_dir}/white_hole_explosion.html")

# --- Matplotlib Animation ---
fig = plt.figure(figsize=(10, 8), facecolor='#0d1117')
ax = fig.add_subplot(111, projection='3d', facecolor='#0d1117')

# Store artists for cleanup
artists = []

# Initial shell
shell = ax.plot_surface(X0, Y0, Z0, alpha=0.7, cmap='hot', rstride=1, cstride=1)
center = ax.scatter([0], [0], [0], color='white', s=200, marker='*')
artists.extend([shell, center])

ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_zlim(-12, 12)
ax.set_xlabel('X', color='white')
ax.set_ylabel('Y', color='white')
ax.set_zlabel('Z', color='white')
ax.set_title('White Hole Explosion', color='white', fontsize=14)
ax.tick_params(colors='white')

def update_wh_exp(frame):
    # Remove previous artists
    for artist in artists:
        artist.remove()
    artists.clear()
    
    r = r_shell[frame]
    X = r * np.sin(TH) * np.cos(PHI)
    Y = r * np.sin(TH) * np.sin(PHI)
    Z = r * np.cos(TH)
    opacity = 0.7 * np.exp(-r/8)
    shell = ax.plot_surface(X, Y, Z, alpha=opacity, cmap='hot', rstride=1, cstride=1)
    center = ax.scatter([0], [0], [0], color='white', s=200, marker='*')
    artists.extend([shell, center])
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.set_zlim(-12, 12)
    return shell, center

anim_wh_exp = animation.FuncAnimation(fig, update_wh_exp, frames=len(r_shell), interval=80, blit=False)
anim_wh_exp.save(f"{output_dir}/white_hole_explosion.mp4", writer='ffmpeg', fps=12, dpi=150)
anim_wh_exp.save(f"{output_dir}/white_hole_explosion.gif", writer=PillowWriter(fps=10))
plt.close()

print("  ✓ White Hole Explosion created")

# ============================================================
# 5. CMB EVOLUTION - Power spectra with cosmological parameters
# ============================================================
print("Creating CMB Evolution Animation...")

# CMB power spectrum evolution with changing cosmological parameters
# Vary: H0, Omega_m, Omega_Lambda, ns, As
ells = np.logspace(1, 3.3, 200)

def cmb_spectrum(ell, H0=70, Om=0.3, OL=0.7, ns=0.96, As=2.1e-9):
    # Simplified CMB power spectrum (Sachs-Wolfe + acoustic peaks)
    # This is a toy model for visualization
    k = ell / 14000  # approximate k-ell relation
    
    # Sachs-Wolfe plateau
    sw = As * (ell/10)**(ns-1) * (ell < 100)
    
    # Acoustic peaks (toy model)
    peak_locs = [220, 540, 800, 1100, 1400]
    peak_heights = [1.0, 0.5, 0.3, 0.2, 0.15]
    acoustic = np.zeros_like(ell)
    for pl, ph in zip(peak_locs, peak_heights):
        acoustic += ph * As * np.exp(-(ell - pl)**2 / (2 * 50**2))
    
    # Damping tail
    damping = As * np.exp(-ell/1500) * (ell > 1000)
    
    return sw + acoustic + damping

# Parameter variations
H0_vals = np.linspace(60, 80, 30)
Om_vals = np.linspace(0.2, 0.4, 30)
ns_vals = np.linspace(0.92, 1.0, 30)

# --- Plotly Animation (varying H0) ---
fig_cmb = go.Figure()

# Initial spectrum
cl_init = cmb_spectrum(ells, H0=70)
fig_cmb.add_trace(go.Scatter(
    x=ells, y=cl_init * ells**2 / (2*np.pi),
    mode='lines', line=dict(color='#00d4ff', width=2),
    name='CMB Power Spectrum'
))

frames_cmb = []
for i, H0 in enumerate(H0_vals):
    cl = cmb_spectrum(ells, H0=H0)
    frames_cmb.append(go.Frame(
        data=[go.Scatter(x=ells, y=cl * ells**2 / (2*np.pi), mode='lines')],
        name=f"frame{i}",
        layout=go.Layout(title=f"CMB Power Spectrum Evolution: H₀ = {H0:.1f} km/s/Mpc")
    ))
fig_cmb.frames = frames_cmb

fig_cmb.update_layout(
    title="CMB Power Spectrum: Varying H₀",
    xaxis_title="Multipole ℓ", yaxis_title="ℓ(ℓ+1)Cₗ/2π [μK²]",
    xaxis_type="log", yaxis_type="log",
    template="plotly_dark", width=1000, height=500,
    sliders=[dict(active=0, steps=[dict(method="animate", args=[[f"frame{i}"], dict(mode="immediate", frame=dict(duration=100, redraw=True))], label=f"{H0:.0f}") for i, H0 in enumerate(H0_vals)], x=0.1, y=0, len=0.9)],
    updatemenus=[dict(type="buttons", showactive=False,
        buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=100, redraw=True), fromcurrent=True)]),
                 dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])],
        x=0.05, y=1.05)]
)

fig_cmb.write_html(f"{output_dir}/cmb_evolution.html")

# --- Matplotlib Animation (multi-parameter) ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10), facecolor='#0d1117')
for ax in axes.flat:
    ax.set_facecolor('#0d1117')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('Multipole ℓ', color='white')
    ax.set_ylabel('ℓ(ℓ+1)Cₗ/2π [μK²]', color='white')

lines = []
params_list = [
    ('H₀ (km/s/Mpc)', H0_vals, 'H0'),
    ('Ωₘ', Om_vals, 'Om'),
    ('nₛ', ns_vals, 'ns'),
    ('Aₛ (×10⁻⁹)', np.linspace(1.5, 2.5, 30), 'As')
]

for idx, (title, param_vals, param_name) in enumerate(params_list):
    ax = axes.flat[idx]
    cl_init = cmb_spectrum(ells)
    line, = ax.plot(ells, cl_init * ells**2 / (2*np.pi), color='#00d4ff', linewidth=2)
    lines.append(line)
    ax.set_title(f'CMB Spectrum: Varying {title}', color='white', fontsize=12)

def update_cmb(frame):
    for idx, (title, param_vals, param_name) in enumerate(params_list):
        kwargs = {'H0': 70, 'Om': 0.3, 'OL': 0.7, 'ns': 0.96, 'As': 2.1e-9}
        kwargs[param_name] = param_vals[frame]
        cl = cmb_spectrum(ells, **kwargs)
        lines[idx].set_ydata(cl * ells**2 / (2*np.pi))
    return lines

anim_cmb = animation.FuncAnimation(fig, update_cmb, frames=30, interval=150, blit=True)
anim_cmb.save(f"{output_dir}/cmb_evolution.mp4", writer='ffmpeg', fps=10, dpi=150)
anim_cmb.save(f"{output_dir}/cmb_evolution.gif", writer=PillowWriter(fps=8))
plt.close()

print("  ✓ CMB Evolution created")

# ============================================================
# 6. GW MEMORY EFFECT - Permanent displacement after burst
# ============================================================
print("Creating GW Memory Effect Animation...")

# Gravitational wave memory: permanent displacement of test masses
# Burst + memory offset
t = np.linspace(-50, 100, 500)

# GW burst (e.g., from binary merger)
burst = 2 * np.exp(-(t-10)**2 / 8) * np.sin(2*np.pi*0.5*(t-10))

# Memory effect: step function that turns on after burst
memory = 0.5 * (1 + np.tanh((t - 15) / 2))  # smooth step

# Total strain
h_total = burst + memory

# Test particle positions (ring of particles)
n_particles = 30
angles = np.linspace(0, 2*np.pi, n_particles)
r0 = 5.0

# --- Plotly Animation ---
fig_mem = go.Figure()

# Initial ring
x0 = r0 * np.cos(angles)
y0 = r0 * np.sin(angles)
h0 = h_total[0]

# Deformed ring
x_def = x0 * (1 + h0/2)
y_def = y0 * (1 - h0/2)  # Quadrupole deformation

fig_mem.add_trace(go.Scatter(
    x=x0, y=y0, mode='markers',
    marker=dict(size=10, color='#888888'), name='Initial Ring'
))
fig_mem.add_trace(go.Scatter(
    x=x_def, y=y_def, mode='markers+lines',
    marker=dict(size=12, color='#ff6b6b'), line=dict(color='#ff6b6b', width=2),
    name='Deformed Ring'
))
# Strain plot
fig_mem.add_trace(go.Scatter(
    x=t[:1], y=h_total[:1], mode='lines',
    line=dict(color='#00d4ff', width=2), name='h(t)',
    xaxis='x2', yaxis='y2'
))
# Memory offset line
fig_mem.add_trace(go.Scatter(
    x=t[:1], y=memory[:1], mode='lines',
    line=dict(color='#ffd700', width=2, dash='dash'), name='Memory',
    xaxis='x2', yaxis='y2'
))

frames_mem = []
for i in range(1, len(t), 3):
    h = h_total[i]
    x_def = x0 * (1 + h/2)
    y_def = y0 * (1 - h/2)
    frames_mem.append(go.Frame(
        data=[
            go.Scatter(x=x0, y=y0, mode='markers', marker=dict(size=10, color='#888888')),
            go.Scatter(x=x_def, y=y_def, mode='markers+lines',
                      marker=dict(size=12, color='#ff6b6b'), line=dict(color='#ff6b6b', width=2)),
            go.Scatter(x=t[:i], y=h_total[:i], mode='lines', line=dict(color='#00d4ff', width=2), xaxis='x2', yaxis='y2'),
            go.Scatter(x=t[:i], y=memory[:i], mode='lines', line=dict(color='#ffd700', width=2, dash='dash'), xaxis='x2', yaxis='y2')
        ],
        name=f"frame{i}"
    ))
fig_mem.frames = frames_mem

fig_mem.update_layout(
    title="Gravitational Wave Memory Effect: Permanent Displacement",
    xaxis=dict(title='X', range=[-8, 8], scaleanchor='y'),
    yaxis=dict(title='Y', range=[-8, 8]),
    xaxis2=dict(title='Time', domain=[0.55, 1], range=[-50, 100]),
    yaxis2=dict(title='Strain', domain=[0, 0.45], range=[-1, 2]),
    template="plotly_dark", width=1200, height=600,
    sliders=[dict(active=0, steps=[dict(method="animate", args=[[f"frame{i}"], dict(mode="immediate", frame=dict(duration=30, redraw=True))], label="") for i in range(len(frames_mem))], x=0.1, y=0, len=0.4)],
    updatemenus=[dict(type="buttons", showactive=False,
        buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=30, redraw=True), fromcurrent=True)]),
                 dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])],
        x=0.05, y=1.05)]
)

fig_mem.write_html(f"{output_dir}/gw_memory_effect.html")

# --- Matplotlib Animation ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor='#0d1117')
for ax in [ax1, ax2]:
    ax.set_facecolor('#0d1117')
    ax.tick_params(colors='white')
    for spine in ax.spines.values():
        spine.set_color('white')

# Left: particle ring
ax1.set_aspect('equal')
ax1.set_xlim(-8, 8)
ax1.set_ylim(-8, 8)
ax1.set_xlabel('X', color='white')
ax1.set_ylabel('Y', color='white')
ax1.set_title('Test Particle Ring', color='white', fontsize=14)

# Initial ring (reference)
ax1.scatter(x0, y0, s=50, color='#888888', alpha=0.5, label='Initial')
ring_scatter = ax1.scatter(x_def, y_def, s=80, color='#ff6b6b', label='Deformed')
ring_line, = ax1.plot(np.append(x_def, x_def[0]), np.append(y_def, y_def[0]), color='#ff6b6b', linewidth=2)
ax1.legend(facecolor='#161b22', edgecolor='white', labelcolor='white')

# Right: strain
ax2.plot(t, h_total, color='#00d4ff', linewidth=1.5, alpha=0.5, label='Total h(t)')
ax2.plot(t, memory, color='#ffd700', linewidth=2, linestyle='--', label='Memory')
ax2.set_xlim(-50, 100)
ax2.set_ylim(-1.5, 2)
ax2.set_xlabel('Time', color='white')
ax2.set_ylabel('Strain', color='white')
ax2.set_title('GW Strain + Memory', color='white', fontsize=14)
ax2.legend(facecolor='#161b22', edgecolor='white', labelcolor='white')

vline = ax2.axvline(t[0], color='white', linestyle=':', alpha=0.5)

def update_mem(frame):
    i = min(frame * 3, len(t)-1)
    h = h_total[i]
    x_def = x0 * (1 + h/2)
    y_def = y0 * (1 - h/2)
    ring_scatter.set_offsets(np.column_stack([x_def, y_def]))
    ring_line.set_data(np.append(x_def, x_def[0]), np.append(y_def, y_def[0]))
    vline.set_xdata([t[i], t[i]])
    return ring_scatter, ring_line, vline

anim_mem = animation.FuncAnimation(fig, update_mem, frames=150, interval=30, blit=True)
anim_mem.save(f"{output_dir}/gw_memory_effect.mp4", writer='ffmpeg', fps=30, dpi=150)
anim_mem.save(f"{output_dir}/gw_memory_effect.gif", writer=PillowWriter(fps=20))
plt.close()

print("  ✓ GW Memory Effect created")

# ============================================================
# 7. PENROSE PROCESS ANIMATION - Particle splitting in ergosphere
# ============================================================
print("Creating Penrose Process Animation...")

# Penrose process: particle enters ergosphere, splits into two
# One escapes with more energy, one falls in with negative energy
a = 0.95
M = 1.0
r_ergo_eq = 2*M  # ergosphere at equator
r_horizon = M + np.sqrt(M**2 - a**2)

# Particle trajectories
t_vals = np.linspace(0, 50, 200)

# Incoming particle (from infinity)
def incoming_particle(t):
    if t < 15:
        r = 10 - 0.4 * t
        phi = 0.1 * t
    else:
        # At ergosphere, splits - stay at split position
        r = 10 - 0.4 * 15  # = 4
        phi = 0.1 * 15     # = 1.5
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y, r, phi

# After split: particle 1 (escapes to infinity with more energy)
def escaping_particle(t):
    if t >= 15:
        dt = t - 15
        r = 2.5 + 0.3 * dt
        phi = 0.1*15 + 0.5 * dt
    else:
        r, phi = -100, 0
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y, r, phi

# Particle 2 (falls into BH with negative energy)
def captured_particle(t):
    if t >= 15:
        dt = t - 15
        r = max(2.5 - 0.2 * dt, r_horizon + 0.1)
        phi = 0.1*15 + 0.8 * dt
    else:
        r, phi = -100, 0
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y, r, phi

# Compute trajectories
traj_in = np.array([incoming_particle(t) for t in t_vals])
traj_esc = np.array([escaping_particle(t) for t in t_vals])
traj_cap = np.array([captured_particle(t) for t in t_vals])

# Ergosphere boundary (equatorial slice)
phi_ergo = np.linspace(0, 2*np.pi, 100)
r_ergo = np.ones_like(phi_ergo) * r_ergo_eq
x_ergo = r_ergo * np.cos(phi_ergo)
y_ergo = r_ergo * np.sin(phi_ergo)

# Horizon
r_h = r_horizon
x_h = r_h * np.cos(phi_ergo)
y_h = r_h * np.sin(phi_ergo)

# --- Plotly Animation ---
fig_pen = go.Figure()

# Ergosphere
fig_pen.add_trace(go.Scatter(
    x=x_ergo, y=y_ergo, mode='lines',
    line=dict(color='cyan', width=2, dash='dash'), name='Ergosphere'
))
# Horizon
fig_pen.add_trace(go.Scatter(
    x=x_h, y=y_h, mode='lines',
    line=dict(color='red', width=3), name='Horizon'
))

# Particles
fig_pen.add_trace(go.Scatter(
    x=[traj_in[0,0]], y=[traj_in[0,1]], mode='markers',
    marker=dict(size=14, color='#00d4ff'), name='Incoming (E>0)'
))
fig_pen.add_trace(go.Scatter(
    x=[traj_esc[0,0]], y=[traj_esc[0,1]], mode='markers',
    marker=dict(size=14, color='#00ff00'), name='Escaping (E>E₀)'
))
fig_pen.add_trace(go.Scatter(
    x=[traj_cap[0,0]], y=[traj_cap[0,1]], mode='markers',
    marker=dict(size=14, color='#ff6b6b'), name='Captured (E<0)'
))

# Trails
fig_pen.add_trace(go.Scatter(x=[], y=[], mode='lines', line=dict(color='#00d4ff', width=2), showlegend=False))
fig_pen.add_trace(go.Scatter(x=[], y=[], mode='lines', line=dict(color='#00ff00', width=2), showlegend=False))
fig_pen.add_trace(go.Scatter(x=[], y=[], mode='lines', line=dict(color='#ff6b6b', width=2), showlegend=False))

frames_pen = []
for i in range(len(t_vals)):
    # Determine which particles are active
    if i < 75:  # Before split
        x_in, y_in = traj_in[i,0], traj_in[i,1]
        frames_pen.append(go.Frame(
            data=[
                go.Scatter(x=x_ergo, y=y_ergo),
                go.Scatter(x=x_h, y=y_h),
                go.Scatter(x=[x_in], y=[y_in], mode='markers', marker=dict(size=14, color='#00d4ff')),
                go.Scatter(x=[-100], y=[-100], mode='markers'),
                go.Scatter(x=[-100], y=[-100], mode='markers'),
                go.Scatter(x=traj_in[:i+1,0], y=traj_in[:i+1,1], mode='lines', line=dict(color='#00d4ff', width=2)),
                go.Scatter(x=[], y=[], mode='lines'),
                go.Scatter(x=[], y=[], mode='lines')
            ], name=f"frame{i}"
        ))
    else:  # After split
        x_esc, y_esc = traj_esc[i,0], traj_esc[i,1]
        x_cap, y_cap = traj_cap[i,0], traj_cap[i,1]
        frames_pen.append(go.Frame(
            data=[
                go.Scatter(x=x_ergo, y=y_ergo),
                go.Scatter(x=x_h, y=y_h),
                go.Scatter(x=[-100], y=[-100], mode='markers'),  # incoming gone
                go.Scatter(x=[x_esc], y=[y_esc], mode='markers', marker=dict(size=14, color='#00ff00')),
                go.Scatter(x=[x_cap], y=[y_cap], mode='markers', marker=dict(size=14, color='#ff6b6b')),
                go.Scatter(x=traj_in[:75,0], y=traj_in[:75,1], mode='lines', line=dict(color='#00d4ff', width=2)),
                go.Scatter(x=traj_esc[75:i+1,0], y=traj_esc[75:i+1,1], mode='lines', line=dict(color='#00ff00', width=2)),
                go.Scatter(x=traj_cap[75:i+1,0], y=traj_cap[75:i+1,1], mode='lines', line=dict(color='#ff6b6b', width=2))
            ], name=f"frame{i}"
        ))

fig_pen.frames = frames_pen

fig_pen.update_layout(
    title="Penrose Process: Energy Extraction from Kerr Black Hole (a=0.95M)",
    xaxis_title='X (M)', yaxis_title='Y (M)',
    xaxis=dict(range=[-12, 12], scaleanchor='y'),
    yaxis=dict(range=[-12, 12]),
    template="plotly_dark", width=800, height=800,
    sliders=[dict(active=0, steps=[dict(method="animate", args=[[f"frame{i}"], dict(mode="immediate", frame=dict(duration=50, redraw=True))], label="") for i in range(len(frames_pen))], x=0.1, y=0, len=0.9)],
    updatemenus=[dict(type="buttons", showactive=False,
        buttons=[dict(label="▶ Play", method="animate", args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)]),
                 dict(label="⏸ Pause", method="animate", args=[[None], dict(frame=dict(duration=0, redraw=False), mode="immediate")])],
        x=0.05, y=1.05)]
)

fig_pen.write_html(f"{output_dir}/penrose_process.html")

# --- Matplotlib Animation ---
fig, ax = plt.subplots(figsize=(10, 10), facecolor='#0d1117')
ax.set_facecolor('#0d1117')
ax.set_aspect('equal')
ax.set_xlim(-12, 12)
ax.set_ylim(-12, 12)
ax.set_xlabel('X (M)', color='white')
ax.set_ylabel('Y (M)', color='white')
ax.set_title('Penrose Process: Energy Extraction from Kerr BH (a=0.95M)', color='white', fontsize=14)
ax.tick_params(colors='white')
for spine in ax.spines.values():
    spine.set_color('white')

# Ergosphere and horizon
ax.plot(x_ergo, y_ergo, 'c--', linewidth=2, label='Ergosphere', alpha=0.7)
ax.plot(x_h, y_h, 'r-', linewidth=3, label='Horizon')
ax.legend(facecolor='#161b22', edgecolor='white', labelcolor='white')

# Particle markers
p_in, = ax.plot([], [], 'o', color='#00d4ff', markersize=14, label='Incoming (E>0)')
p_esc, = ax.plot([], [], 'o', color='#00ff00', markersize=14, label='Escaping (E>E₀)')
p_cap, = ax.plot([], [], 'o', color='#ff6b6b', markersize=14, label='Captured (E<0)')

# Trails
trail_in, = ax.plot([], [], '-', color='#00d4ff', linewidth=2, alpha=0.7)
trail_esc, = ax.plot([], [], '-', color='#00ff00', linewidth=2, alpha=0.7)
trail_cap, = ax.plot([], [], '-', color='#ff6b6b', linewidth=2, alpha=0.7)

def update_pen(frame):
    if frame < 75:
        p_in.set_data([traj_in[frame,0]], [traj_in[frame,1]])
        p_esc.set_data([-100], [-100])
        p_cap.set_data([-100], [-100])
        trail_in.set_data(traj_in[:frame+1,0], traj_in[:frame+1,1])
        trail_esc.set_data([], [])
        trail_cap.set_data([], [])
    else:
        p_in.set_data([-100], [-100])
        p_esc.set_data([traj_esc[frame,0]], [traj_esc[frame,1]])
        p_cap.set_data([traj_cap[frame,0]], [traj_cap[frame,1]])
        trail_in.set_data(traj_in[:75,0], traj_in[:75,1])
        trail_esc.set_data(traj_esc[75:frame+1,0], traj_esc[75:frame+1,1])
        trail_cap.set_data(traj_cap[75:frame+1,0], traj_cap[75:frame+1,1])
    return p_in, p_esc, p_cap, trail_in, trail_esc, trail_cap

anim_pen = animation.FuncAnimation(fig, update_pen, frames=len(t_vals), interval=50, blit=True)
anim_pen.save(f"{output_dir}/penrose_process.mp4", writer='ffmpeg', fps=20, dpi=150)
anim_pen.save(f"{output_dir}/penrose_process.gif", writer=PillowWriter(fps=15))
plt.close()

print("  ✓ Penrose Process created")

# ============================================================
# Summary
# ============================================================
print("\n" + "="*60)
print("ALL ANIMATIONS CREATED SUCCESSFULLY!")
print("="*60)

files_created = [
    "bh_merger_animation.html", "bh_merger_animation.mp4", "bh_merger_animation.gif",
    "kerr_ergosphere_precession.html", "kerr_ergosphere_precession.mp4", "kerr_ergosphere_precession.gif",
    "wormhole_traversal.html", "wormhole_traversal.mp4", "wormhole_traversal.gif",
    "white_hole_explosion.html", "white_hole_explosion.mp4", "white_hole_explosion.gif",
    "cmb_evolution.html", "cmb_evolution.mp4", "cmb_evolution.gif",
    "gw_memory_effect.html", "gw_memory_effect.mp4", "gw_memory_effect.gif",
    "penrose_process.html", "penrose_process.mp4", "penrose_process.gif"
]

print("\nFiles created in premium/figures/:")
for f in files_created:
    path = f"{output_dir}/{f}"
    if os.path.exists(path):
        size = os.path.getsize(path)
        print(f"  ✓ {f} ({size/1024:.1f} KB)")
    else:
        print(f"  ✗ {f} (MISSING)")

print(f"\nTotal: {sum(1 for f in files_created if os.path.exists(f'{output_dir}/{f}'))}/{len(files_created)} files created")