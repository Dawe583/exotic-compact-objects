"""Core equations for black holes, wormholes, and white holes.

Basic (first-pass) implementations. Units via astropy.
"""
import numpy as np
from astropy import constants as const
from astropy import units as u

# ---------- Black holes: Schwarzschild ----------

def schwarzschild_radius(mass):
    """Rs = 2 G M / c^2"""
    return (2 * const.G * mass / const.c**2).to(u.km)

def hawking_temperature(mass):
    """T_H = hbar c^3 / (8 pi G M k_B)"""
    return (const.hbar * const.c**3 / (8 * np.pi * const.G * mass * const.k_B)).to(u.K)

def isco_radius_schwarzschild(mass):
    """R_isco = 6 Rs (Schwarzschild)"""
    return (6 * schwarzschild_radius(mass)).to(u.km)

def photon_sphere_radius_schwarzschild(mass):
    """R_ph = 3 Rs/2 = 3GM/c^2"""
    return (3 * const.G * mass / const.c**2).to(u.km)

# ---------- Black holes: Kerr (basic) ----------

def kerr_horizon_radius(mass, spin_a):
    """Outer horizon r_+ = (GM/c^2)(1 + sqrt(1 - a^2)), a dimensionless spin in [0,1)."""
    a = np.asarray(spin_a, dtype=float)
    GM_c2 = (const.G * mass / const.c**2).to(u.km).value
    r_plus = GM_c2 * (1.0 + np.sqrt(np.clip(1.0 - a**2, 0, None)))
    return r_plus * u.km

def ergosphere_radius_equatorial(mass, spin_a):
    """Equatorial ergosphere outer boundary r_ergo = (GM/c^2)(1 + sqrt(1 - a^2 cos^2 theta)) with theta=pi/2 -> (GM/c^2)(1+1)=2GM/c^2? Use general: r_ergo = GM/c^2 (1 + sqrt(1 - a^2 cos^2 theta)). At equator cos=0 -> 2GM/c^2."""
    GM_c2 = (const.G * mass / const.c**2).to(u.km).value
    return (2 * GM_c2) * u.km

# ---------- Wormholes: Morris-Thorne ----------

def morris_thorne_shape_function(r, b0):
    """b(r) = b0^2 / r  (simple demo shape function)."""
    r = np.asarray(r, dtype=float)
    return b0**2 / np.where(r == 0, np.nan, r)

def morris_thorne_redshift_function(r, b0, Phi0=1.0):
    """Phi(r) = Phi0 * (1 - b0/r) demo (asymptotically flat)."""
    r = np.asarray(r, dtype=float)
    return Phi0 * (1.0 - b0 / np.where(r == 0, np.nan, r))

def wormhole_throat_radius(b0):
    """Throat radius r0 = b0 (where b(r0)=r0)."""
    return float(b0) * u.km

def morris_thorne_metric_components(r, b0, Phi0=1.0):
    """Return (g_tt, g_rr) demo components for Morris-Thorne metric:
    ds^2 = -e^{2Phi} dt^2 + (1 - b/r)^-1 dr^2 + r^2 dOmega^2
    """
    r = np.asarray(r, dtype=float)
    b = morris_thorne_shape_function(r, b0)
    Phi = morris_thorne_redshift_function(r, b0, Phi0)
    g_tt = -np.exp(2 * Phi)
    g_rr = 1.0 / np.clip(1.0 - b / np.where(r == 0, np.nan, r), 1e-12, None)
    return g_tt, g_rr

# ---------- White holes ----------

def white_hole_time_reversed_schwarzschild(mass):
    """White hole as time-reversed Schwarzschild: same radius, negative time orientation."""
    rs = schwarzschild_radius(mass)
    return {"radius_km": rs, "time_orientation": "reversed", "mass_msun_equiv": mass}

def white_hole_negative_mass_radius(mass_abs):
    """Demo: Newtonian escape radius for negative mass M=-|M|: r = 2 G |M| / c^2 (magnitude)."""
    m = -abs(float(mass_abs)) * u.Msun
    return schwarzschild_radius(abs(mass_abs) * u.Msun)

# ---------- Extended: Kerr ISCO ----------

def isco_radius_kerr(mass, spin_a):
    """Approximate ISCO radius for Kerr (Bardeen et al. 1972) in units of GM/c^2.
    Prograde: r_isco = 3 + Z2 - sqrt((3-Z1)(3+Z1+2*Z2)) in units of M (geometric), times GM/c^2.
    We return km for mass."""
    a = float(spin_a)
    Z1 = 1 + (1 - a**2)**(1.0/3.0) * ((1 + a)**(1.0/3.0) + (1 - a)**(1.0/3.0))
    Z2 = np.sqrt(3 * a**2 + Z1**2)
    r_msun_units = 3 + Z2 - np.sqrt((3 - Z1) * (3 + Z1 + 2 * Z2))  # in units of GM/c^2
    GM_c2_km = (const.G * mass / const.c**2).to(u.km).value
    return r_msun_units * GM_c2_km * u.km

# ---------- Effective potential (Schwarzschild timelike) ----------

def effective_potential_schwarzschild(r_km, mass, L):
    """V_eff(r) = (1 - Rs/r)(1 + L^2/r^2) for timelike geodesics (units: dimensionless)."""
    Rs = schwarzschild_radius(mass).value
    r = np.asarray(r_km, dtype=float)
    return (1 - Rs / r) * (1 + (L**2) / (r**2))

# ---------- Wormhole: flare-out & embedding ----------

def flare_out_condition(b, db_dr):
    """Morris-Thorne flare-out: (b - b' r)/(2 b^2) > 0  <=> b' < b/r at throat."""
    return (b - db_dr * np.asarray(b, dtype=float))  # positive -> flare-out

def morris_thorne_embedding_z(r, b0):
    """Embedding function dz/dr = +/- sqrt(b/(r-b)) for Morris-Thorne (demo)."""
    r = np.asarray(r, dtype=float)
    b = morris_thorne_shape_function(r, b0)
    val = b / np.clip(r - b, 1e-9, None)
    return np.sqrt(np.clip(val, 0, None))

# ---------- Hawking radiation basics ----------

def hawking_power(mass):
    """Approximate Hawking power P ~ hbar c^6 / (15360 pi G^2 M^2) (Schwarzschild)."""
    M = mass.to(u.kg) if hasattr(mass, "to") else mass * u.Msun
    P = const.hbar * const.c**6 / (15360 * np.pi * const.G**2 * M**2)
    return P.to(u.W)

def hawking_lifetime(mass):
    """Evaporation time ~ 5120 pi G^2 M^3 / (hbar c^4) (approx)."""
    M = mass.to(u.kg) if hasattr(mass, "to") else mass * u.Msun
    t = 5120 * np.pi * const.G**2 * M**3 / (const.hbar * const.c**4)
    return t.to(u.s)

def white_hole_hawking_analog(mass):
    """Analog: white hole emits with opposite sign temperature (demo): T = -T_H."""
    T = hawking_temperature(mass)
    return -T

# ---------- White hole instability (toy model) ----------

def white_hole_instability_timescale(mass):
    """Toy instability e-folding time ~ GM/c^3 (geometric time)."""
    M = mass.to(u.kg) if hasattr(mass, "to") else mass * u.Msun
    t = const.G * M / const.c**3
    return t.to(u.s)

def white_hole_perturbation_growth(t, delta0, mass):
    """delta(t) = delta0 * exp(t / tau) with tau = GM/c^3."""
    tau = white_hole_instability_timescale(mass).value
    return delta0 * np.exp(np.asarray(t, dtype=float) / tau)

# ---------- Comparison helpers ----------

def compactness(mass, radius):
    """Compactness C = GM/(R c^2)."""
    M = mass.to(u.kg) if hasattr(mass, "to") else mass * u.Msun
    R = radius.to(u.m) if hasattr(radius, "to") else radius * u.km
    return (const.G * M / (R * const.c**2)).decompose().value
