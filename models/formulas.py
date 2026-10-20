"""Extended physics formulas (numeric, astropy-united).

Complements models/equations.py (Schwarzschild/Kerr basic, Morris-Thorne basic).
Everything here is SI-based with astropy constants; inputs with units, outputs with units.

Each function cites the formula and (where meaningful) the symbolic derivation
that backs it in models/derivations.py.
"""

from __future__ import annotations

import numpy as np
from astropy import constants as const
from astropy import units as u

# ------------------------------------------------------------------ Kerr ISCO


def kerr_isco_radius(
    mass: u.Quantity, a: float, retrograde: bool = False
) -> u.Quantity:
    """Exact ISCO radius of a Kerr BH (Bardeen, Press & Teukolsky 1972).

    r_isco/M = 3 + Z2 ∓ sqrt((3 - Z1)(3 + Z1 + 2 Z2))
    Z1 = 1 + (1-a^2)^(1/3) [(1+a)^(1/3)+(1-a)^(1/3)]
    Z2 = sqrt(3 a^2 + Z1^2)

    `a` is the dimensionless spin chi = c|J|/(G M^2) in [0, 1].
    Prograde orbits use the minus sign, retrograde the plus sign.
    """
    a = float(np.clip(a, 0.0, 1.0))
    Z1 = 1.0 + (1.0 - a**2) ** (1.0 / 3.0) * (
        (1.0 + a) ** (1.0 / 3.0) + (1.0 - a) ** (1.0 / 3.0)
    )
    Z2 = np.sqrt(3.0 * a**2 + Z1**2)
    inner = (3.0 - Z1) * (3.0 + Z1 + 2.0 * Z2)
    disc = np.sqrt(max(inner, 0.0))
    geo = 3.0 + Z2 + (disc if retrograde else -disc)
    GM_c2 = (const.G * mass / const.c**2).to(u.m)
    return (geo * GM_c2).to(u.km)


def isco_frequency(mass: u.Quantity) -> u.Quantity:
    """Orbital frequency f at the Schwarzschild ISCO: f = c^3 / (2 pi 6^(3/2) G M)."""
    omega = (const.c**3 / (6.0**1.5 * const.G * mass)).to(1 / u.s)
    return (omega / (2 * np.pi)).to(u.Hz)


# ------------------------------------------------------------- Eddington limit


def eddington_luminosity(mass: u.Quantity) -> u.Quantity:
    """L_Edd = 4 pi G M m_p c / sigma_T (hydrogen-only scattering limit)."""
    return (4 * np.pi * const.G * mass * const.m_p * const.c / const.sigma_T).to(u.W)


def eddington_mass_accretion_rate(
    mass: u.Quantity, efficiency: float = 0.1
) -> u.Quantity:
    """Mdot_Edd = L_Edd / (efficiency * c^2)."""
    L = eddington_luminosity(mass)
    return (L / (efficiency * const.c**2)).to(u.kg / u.s)


# -------------------------------------------------- gravitational-wave chirp


def gw_chirp_mass(m1: u.Quantity, m2: u.Quantity) -> u.Quantity:
    """M_chirp = (m1 m2)^(3/5) / (m1+m2)^(1/5)."""
    return ((m1 * m2) ** (3 / 5) / (m1 + m2) ** (1 / 5)).to(m1.unit)


def gw_symmetric_mass_ratio(m1: u.Quantity, m2: u.Quantity) -> float:
    """eta = m1 m2 / (m1+m2)^2, in (0, 1/4]."""
    return float((m1 * m2 / (m1 + m2) ** 2).to(u.dimensionless_unscaled).value)


def gw_delta(m1: u.Quantity, m2: u.Quantity) -> float:
    """Delta = (m1 - m2) / (m1 + m2)."""
    return float(((m1 - m2) / (m1 + m2)).to(u.dimensionless_unscaled).value)


def gw_time_to_coalescence(m_chirp: u.Quantity, f_gw: u.Quantity) -> u.Quantity:
    """Leading-order PA time to coalescence: t = (5/256) (c^3/GM_c)^{5/3} (pi f)^{-8/3}."""
    return (
        (5 / 256)
        * (const.c**3 / (const.G * m_chirp)) ** (5 / 3)
        * (np.pi * f_gw) ** (-8 / 3)
    ).to(u.s)


def gw_peak_strain_leading_order(
    m_chirp: u.Quantity, d_l: u.Quantity, f_gw: u.Quantity
) -> float:
    """Order-of-magnitude leading-order inspiral strain amplitude at frequency f (dimensionless).

    h ~ (4 / (c^4 D)) (G M_c)^(5/3) (pi f)^(2/3)
    """
    h = (
        4.0
        * (const.G * m_chirp) ** (5 / 3)
        * (np.pi * f_gw) ** (2 / 3)
        / (const.c**4 * d_l)
    ).to(u.dimensionless_unscaled)
    return float(h.value)


# --------------------------------------------------------------- BH shadows


def shadow_diameter_schwarzschild(mass: u.Quantity) -> u.Quantity:
    """D_sh = 2 * 3 sqrt(3) G M / c^2 (photon capture disk diameter, in km)."""
    return (2.0 * np.sqrt(27.0) * const.G * mass / const.c**2).to(u.km)


def shadow_angular_diameter(mass: u.Quantity, distance: u.Quantity) -> u.Quantity:
    """Angular diameter theta = D_sh / distance (radians), for a Schwarzschild BH."""
    sh = shadow_diameter_schwarzschild(mass).to(u.m)
    dist = distance.to(u.m)
    return np.arctan((sh / dist).to(u.dimensionless_unscaled).value) * u.rad


# ------------------------------------------------ neutron-star deformability


def tidal_deformability(compactness: float, love_number_k2: float = 0.085) -> float:
    """Lambda = (2/3) k2 C^-5 with C = GM/(R c^2)."""
    C = float(compactness)
    return (2.0 / 3.0) * love_number_k2 * C**-5


# ------------------------------------------------------------ Penrose ceiling


def penrose_max_extraction_efficiency() -> float:
    """Maximum Penrose-process efficiency: 1 - 1/sqrt(2) ≈ 0.29289 (29.29 %)."""
    return float(1.0 - 1.0 / np.sqrt(2.0))


def penrose_max_specific_energy_spin(a: float) -> float:
    """Linearized demo of efficiency vs spin: eta(a) ≈ (1 - 1/sqrt(2)) * a.

    Physically meaningful only as a sketch; the exact maximal case is a=1
    with eta = 1 - 1/sqrt(2) ≈ 29.29% (see penrose_max_extraction_efficiency).
    """
    a = float(np.clip(a, 0.0, 1.0))
    return (1.0 - 1.0 / np.sqrt(2.0)) * a


# ----------------------------------------------------------------- cosmology


def friedmann_H(
    z: float,
    H0: u.Quantity,
    Omega_m: float,
    omega_de: u.Quantity,
    Omega_k: float = 0.0,
    Omega_r: float = 0.0,
) -> u.Quantity:
    """H(z) = H0 sqrt( Omega_r (1+z)^4  + Omega_m (1+z)^3 + Omega_k (1+z)^2 + Omega_L ).
    Omega_L accepts either a Quantity (dimensionless) or float.
    """
    L = (
        omega_de.to_value(u.dimensionless_unscaled)
        if isinstance(omega_de, u.Quantity)
        else float(omega_de)
    )
    E2 = Omega_r * (1 + z) ** 4 + Omega_m * (1 + z) ** 3 + Omega_k * (1 + z) ** 2 + L
    return (H0 * np.sqrt(E2)).to(1 / u.s)
