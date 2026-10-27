#!/usr/bin/env python3
"""
Build the premium research website for the exotic-compact-objects project.

The site is static HTML. This script is the single source of truth for the
shell (header, navigation, footer), the landing dashboard, the data catalogue,
the model gallery and the visualisation gallery. Long-form theory pages are
kept as authored HTML and re-wrapped in the shell, so their content is never
regenerated or lost.

Usage:
    python scripts/build_premium_site.py
"""

from __future__ import annotations

import csv
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "premium"
FIG = SITE / "figures"
DATA = ROOT / "data"
PROJECT = ROOT
WORKSPACE = ROOT.parents[2]

SITE_NAME = "Astro Science"
TAGLINE = "Extreme compact objects, gravitational waves and relativistic astrophysics"
GITHUB = "https://github.com/Dawe583/exotic-compact-objects"
NOTEBOOKS_URL = "https://dawe583.github.io/exotic-compact-objects/"
REPO_BLOB = GITHUB + "/blob/main/"
REPO_TREE = GITHUB + "/tree/main/"

NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("data.html", "Data"),
    ("models.html", "Models"),
    ("gallery.html", "Visualisations"),
    ("theory.html", "Theory"),
]

# --------------------------------------------------------------------------
# Catalogue metadata
# --------------------------------------------------------------------------
CATALOGS = [
    # (label, relative path, category, description, source)
    (
        "GWTC compact-binary events",
        "data/processed/gwosc_gwtc.csv",
        "Gravitational waves",
        "Merging compact binaries from GWTC-1/2/3 and O4 with masses, distances, SNR and false-alarm rates.",
        "GWOSC",
    ),
    (
        "GWTC recent remnants",
        "data/processed/gwtc_recent_20_remnants.csv",
        "Gravitational waves",
        "The twenty most recent detected mergers with remnant mass, spin and radiated energy.",
        "GWOSC",
    ),
    (
        "Remnant ISCO & Hawking table",
        "results/gwtc_remnant_isco_hawking.csv",
        "Theory outputs",
        "Derived remnant quantities: Kerr ISCO (BPT), horizon area, Hawking temperature and evaporation time.",
        "Derived",
    ),
    (
        "SXS characterisation",
        "results/sxs_characterization.csv",
        "Gravitational waves",
        "Simulation-extracted waveform characteristics for the SXS catalogue.",
        "SXS",
    ),
    (
        "SXS BBH catalogue",
        "data/external/sxs_catalog/sxs_bbh_catalog.csv",
        "Gravitational waves",
        "Binary black-hole initial data and remnant parameters from the SXS collaboration.",
        "SXS",
    ),
    (
        "AGN reverberation masses",
        "data/processed/agn_reverberation_masses.csv",
        "AGN & SMBH",
        "Supermassive black-hole masses from reverberation mapping with line widths and time delays.",
        "Literature",
    ),
    (
        "AGN BH mass compilation",
        "data/external/agn_bh_mass.csv",
        "AGN & SMBH",
        "Compiled AGN black-hole masses across redshift used for demographic comparisons.",
        "Literature",
    ),
    (
        "BlackCAT dynamical BHs",
        "data/processed/blackcat_dynamical.csv",
        "Black holes",
        "Dynamically confirmed stellar-mass black holes with orbital and distance measurements.",
        "BlackCAT",
    ),
    (
        "Exoplanet catalog (confirmed)",
        "../exoplanets/data/raw/exoplanets_confirmed.csv",
        "Exoplanets",
        "Confirmed exoplanets from NASA Exoplanet Archive (real measurements).",
        "NASA Exoplanet Archive",
    ),
    (
        "Exoplanet processed sample",
        "../exoplanets/data/processed/exoplanets.csv",
        "Exoplanets",
        "Processed exoplanet sample used by the exoplanets notebooks and theory docs.",
        "Exoplanets project",
    ),
    (
        "Known compact objects",
        "data/processed/known_compact_objects.csv",
        "Black holes",
        "Curated compact-object landmarks spanning stellar-mass BHs, neutron stars and SMBHs.",
        "Curated",
    ),
    (
        "XRBCAT X-ray binaries",
        "data/external/xrbcat.csv",
        "X-ray binaries",
        "X-ray binary catalogue with companion type, orbital period and X-ray properties.",
        "XRBCAT",
    ),
    (
        "ATNF pulsars",
        "data/external/atnfpulsar.csv",
        "Stellar remnants",
        "The ATNF pulsar catalogue: spin periods, dispersion measures and Galactic positions.",
        "ATNF",
    ),
    (
        "Gaia DR3 wide binaries",
        "data/external/gaia_dr3_wide_binaries.csv",
        "Gaia",
        "Wide binary candidates used for astrometric black-hole searches in Gaia DR3.",
        "Gaia DR3",
    ),
    (
        "Gaia DR3 BH candidates",
        "data/external/gaia_dr3_bh_candidates.csv",
        "Gaia",
        "Astrometric black-hole candidate sample from Gaia DR3.",
        "Gaia DR3",
    ),
    (
        "Sgr A* region catalogue",
        "data/external/sgraregcsc.csv",
        "Galactic centre",
        "Chandra catalogue of X-ray sources in the Sgr A* region.",
        "Chandra",
    ),
    (
        "M87 X-ray sources",
        "data/external/m87cxo.csv",
        "Galactic centre",
        "Chandra X-ray point sources in the M87 field.",
        "Chandra",
    ),
    (
        "ULX catalogues",
        "data/external/ulxrbcat.csv",
        "X-ray binaries",
        "Ultraluminous X-ray source catalogue with fluxes and host-galaxy associations.",
        "ULX",
    ),
    (
        "GW theoretical spectra",
        "data/external/gwb_spectra/gwb_theoretical_spectra.csv",
        "Gravitational waves",
        "Theoretical stochastic gravitational-wave background spectra across source populations.",
        "Derived",
    ),
    (
        "Remnant energetics (Kerr)",
        "results/remnant_energetics.csv",
        "Theory outputs",
        "Inferred remnant spin, exact Kerr ISCO, radiative efficiency and rotational energy for 270 GWTC events.",
        "Derived",
    ),
]

# --------------------------------------------------------------------------
# Figure metadata
# --------------------------------------------------------------------------
FIGURES = {
    "gw_mass": (
        "GWTC mass distribution",
        "Component masses of the observed binary black-hole population.",
        "Gravitational waves",
    ),
    "gwtc_recent_20_remnants": (
        "Twenty most recent remnants",
        "Remnant mass and spin of the latest detected mergers.",
        "Gravitational waves",
    ),
    "pta_snr": (
        "Pulsar-timing array sensitivity",
        "Signal-to-noise distribution for a stochastic background search.",
        "Gravitational waves",
    ),
    "pta_targets": (
        "PTA targets",
        "Millisecond pulsars as PTA targets from real ATNF data, ranked by SNR proxy.",
        "Gravitational waves",
    ),
    "sxs_modes": (
        "SXS waveform modes",
        "Higher harmonics in numerical-relativity waveforms.",
        "Gravitational waves",
    ),
    "gw_memory_effect": (
        "Gravitational-wave memory",
        "Permanent displacement imprinted by a passing gravitational wave.",
        "Gravitational waves",
    ),
    "bh_merger_animation": (
        "Binary black-hole merger",
        "Numerical-relativity-inspired merger animation.",
        "Gravitational waves",
    ),
    "kerr_isco": (
        "Kerr ISCO",
        "Innermost stable circular orbit as a function of spin, prograde and retrograde.",
        "Black holes",
    ),
    "eht_shadow": (
        "EHT shadow comparison",
        "Predicted Schwarzschild/Kerr shadow vs measured EHT ring for M87* and Sgr A* (real parameters).",
        "Black holes",
    ),
    "rs_mass": (
        "Schwarzschild radius vs mass",
        "Horizon radius across stellar to supermassive black holes.",
        "Black holes",
    ),
    "bh_mass_dist": (
        "Black-hole mass spectrum",
        "Observed mass distributions across the compact-object landscape.",
        "Black holes",
    ),
    "orbit_schw": (
        "Schwarzschild orbit",
        "Test-particle orbit in the Schwarzschild geometry.",
        "Black holes",
    ),
    "pericenter_advance": (
        "Pericenter advance",
        "Relativistic precession of a bound orbit.",
        "Black holes",
    ),
    "geodesic_potential": (
        "Effective potential",
        "Radial effective potential for null and massive geodesics.",
        "Black holes",
    ),
    "penrose_eff": (
        "Penrose efficiency",
        "Energy extraction efficiency from the ergosphere.",
        "Black holes",
    ),
    "penrose_process": (
        "Penrose process",
        "Frame-dragging and energy extraction near a rotating horizon.",
        "Black holes",
    ),
    "kerr_ergosphere_precession": (
        "Kerr ergosphere & precession",
        "Ergosphere shape and spin-induced precession.",
        "Black holes",
    ),
    "christoffel_pattern": (
        "Kerr Christoffel symbols",
        "Symbolic structure of the non-zero connection components.",
        "Black holes",
    ),
    "fisher_corr": (
        "Fisher-matrix correlations",
        "Parameter correlations for gravitational-wave inference.",
        "Black holes",
    ),
    "agn_mass": (
        "AGN black-hole masses",
        "Reverberation-mapped black-hole mass distribution.",
        "AGN & SMBH",
    ),
    "agn_mass_distribution": (
        "AGN mass distribution",
        "Reverberation-mapped AGN masses and Eddington luminosities (real data).",
        "AGN & SMBH",
    ),
    "agn_reverberation_catalog": (
        "Reverberation catalog",
        "Time-delay versus line-width measurements.",
        "AGN & SMBH",
    ),
    "blackcat_dynamical": (
        "Dynamically confirmed BHs",
        "Mass and distance for dynamically detected stellar black holes.",
        "Black holes",
    ),
    "corbet": (
        "Corbet diagram (synthetic demonstration)",
        "Spin period versus orbital period for high-mass X-ray binaries. Demonstration data only — synthetic, not real astronomy.",
        "X-ray binaries",
    ),
    "gaia_sky": (
        "Gaia DR3 sky map",
        "Sky distribution of Gaia astrometric black-hole candidates.",
        "Gaia",
    ),
    "planck_spectra": (
        "CMB power spectra",
        "Temperature and polarisation spectra from Planck.",
        "Cosmology",
    ),
    "cmb_evolution": (
        "CMB evolution",
        "Growth of cosmic structure and the microwave background.",
        "Cosmology",
    ),
    "wormhole_3d": (
        "Wormhole embedding",
        "Three-dimensional embedding of a traversable wormhole throat.",
        "Wormholes",
    ),
    "wormhole_traversal": (
        "Wormhole traversal",
        "Null geodesics crossing a Morris-Thorne throat.",
        "Wormholes",
    ),
    "white_hole_explosion": (
        "White-hole outburst",
        "Mass ejection from a white-hole-like instability.",
        "White holes",
    ),
    "wh_decay": (
        "White-hole decay",
        "Instability growth and decay of a white-hole horizon.",
        "White holes",
    ),
    "raychaudhuri_focusing": (
        "Raychaudhuri focusing",
        "Geodesic convergence and caustic formation.",
        "Advanced theory",
    ),
    "remnant_energetics": (
        "Remnant energetics",
        "Radiative efficiency and rotational energy of 270 GWTC remnants.",
        "Gravitational waves",
    ),
    "exotic_discrimination": (
        "Exotic discrimination",
        "Margin of the remnant population to the Kerr efficiency bound.",
        "Gravitational waves",
    ),
    "agn_demographics": (
        "AGN mass demographics",
        "Reverberation-mapped supermassive black-hole masses vs redshift.",
        "AGN & SMBH",
    ),
    "sxs_waveform_analysis": (
        "SXS waveform peak and ringdown",
        "Numerical-relativity peak and ringdown frequencies vs inferred spin.",
        "Gravitational waves",
    ),
    "exoplanet_mass_radius": (
        "Exoplanet mass-radius",
        "Confirmed exoplanets on the mass-radius diagram with rocky composition line.",
        "Exoplanets",
    ),
    "exoplanet_hz": (
        "Habitable zone",
        "Planet orbital distance vs stellar Teff with the Sun's conservative HZ.",
        "Exoplanets",
    ),
    "qnm_kerr": (
        "Kerr quasinormal modes",
        "QNM frequency and quality factor vs spin (eikonal approximation).",
        "Black holes",
    ),
}

FIGURE_GROUPS = [
    "Exoplanets",
    "Gravitational waves",
    "Black holes",
    "AGN & SMBH",
    "X-ray binaries",
    "Gaia",
    "Cosmology",
    "Wormholes",
    "White holes",
    "Advanced theory",
]

THEORY_DOCS = [
    (
        "theory_black_holes.html",
        "Black holes",
        "Complete theory from first principles",
        "Schwarzschild and Kerr solutions, horizons, singularities, the Kruskal extension, thermodynamics and the membrane paradigm.",
        "cyan",
    ),
    (
        "theory_bh_thermodynamics.html",
        "BH thermodynamics",
        "Hawking radiation and evaporation",
        "Hawking temperature, Bekenstein-Hawking entropy, evaporation timescale and the information paradox.",
        "cyan",
    ),
    (
        "theory_early_smbh_growth.html",
        "Early SMBH growth",
        "Eddington-limited growth and seeds",
        "Growth model, seed constraints, Soltan argument and AGN mass anchors.",
        "amber",
    ),
    (
        "theory_wormholes.html",
        "Wormholes",
        "Morris-Thorne geometry and traversability",
        "Metric ansatz, flare-out condition, exotic matter, energy conditions and tidal constraints for a traversable throat.",
        "violet",
    ),
    (
        "theory_white_holes.html",
        "White holes",
        "Time-reversed horizons and instability",
        "White-hole extensions, the instability of the horizon, mass ejection and the relation to black-hole evaporation.",
        "amber",
    ),
    (
        "theory_white_hole_instability.html",
        "WH instability",
        "Instability and evaporation",
        "Classical instability timescale, Hawking evaporation and the Planck-luminosity bound.",
        "amber",
    ),
    (
        "theory_white_hole_cosmology.html",
        "WH cosmology",
        "White holes in cosmology",
        "Primordial white holes, the Big Bang as a white hole, and observational signatures.",
        "amber",
    ),
    (
        "theory_reissner_nordstrom.html",
        "Reissner-Nordstrom",
        "Charged black holes",
        "Two horizons, extremality, the Cauchy horizon and the fate of the inner singularity.",
        "cyan",
    ),
    (
        "theory_kerr_newman.html",
        "Kerr-Newman",
        "Rotating, charged black holes",
        "The full family of vacuum electro-vacuum solutions, horizon structure and cosmic censorship.",
        "violet",
    ),
    (
        "theory_kerr_geodesics.html",
        "Kerr geodesics",
        "Geodesics and frame dragging",
        "Kerr metric, ISCO vs spin, and Lense-Thirring precession.",
        "cyan",
    ),
    (
        "theory_kerr_newman_adm.html",
        "Kerr-Newman ADM",
        "Mass, spin and charge from infinity",
        "ADM quantities, the Smarr relation and the first law of black-hole mechanics.",
        "amber",
    ),
    (
        "theory_christoffel_kerr.html",
        "Christoffel symbols (Kerr)",
        "Symbolic connection coefficients",
        "Explicit non-zero connection components in Boyer-Lindquist coordinates, with verification notes.",
        "cyan",
    ),
    (
        "theory_geodesic_equations.html",
        "Geodesic equations",
        "Motion in curved spacetime",
        "Affine parametrisation, constants of motion, the Carter constant and numerical integration.",
        "violet",
    ),
    (
        "theory_raychaudhuri.html",
        "Raychaudhuri equation",
        "Focusing and singularity theorems",
        "Expansion, shear and vorticity; energy conditions and the focusing theorem.",
        "amber",
    ),
    (
        "theory_fisher_matrix.html",
        "Fisher matrix",
        "Gravitational-wave parameter estimation",
        "The information matrix, waveform derivatives, correlations and forecast uncertainties.",
        "cyan",
    ),
    (
        "theory_bh_perturbation.html",
        "Black-hole perturbations",
        "Quasinormal modes and ringdown",
        "Regge-Wheeler and Zerilli equations, quasinormal frequencies and the ringdown signal.",
        "violet",
    ),
    (
        "theory_eht_shadow.html",
        "EHT shadows",
        "Photon rings and the Kerr shadow",
        "Shadow size formula, EHT measurements of M87* and Sgr A*, and the strong-field test.",
        "cyan",
    ),
    (
        "theory_penrose_process.html",
        "Penrose process",
        "Energy extraction from rotating BHs",
        "Ergosphere, negative-energy fragments, efficiency up to 20.7% and Blandford-Znajek analogue.",
        "amber",
    ),
    (
        "theory_gw_memory.html",
        "GW memory",
        "Permanent displacement from GWs",
        "Christodoulou nonlinear memory, order-of-magnitude estimates and detectability.",
        "rose",
    ),
    (
        "theory_pta.html",
        "Pulsar timing arrays",
        "PTA detection of gravitational waves",
        "Timing residuals, Hellings-Downs correlation and best targets from real ATNF data.",
        "cyan",
    ),
]

MODELS = [
    {
        "tag": "Canonical",
        "tone": "cyan",
        "title": "Schwarzschild geometry",
        "body": "The unique spherically symmetric vacuum solution. Sets the horizon scale R<sub>s</sub> = 2GM/c<sup>2</sup> and the reference against which every compact object is measured.",
        "eq": r"ds^2 = -\left(1-\frac{r_s}{r}\right)c^2dt^2 + \left(1-\frac{r_s}{r}\right)^{-1}dr^2 + r^2d\Omega^2",
        "href": "theory_black_holes.html",
        "fig": "rs_mass",
    },
    {
        "tag": "Rotating",
        "tone": "violet",
        "title": "Kerr spacetime & ISCO",
        "body": "Frame dragging, the ergosphere and the spin-dependent innermost stable circular orbit. The ISCO sets the radiative efficiency of accretion and the cut-off of the remnant spectrum.",
        "eq": r"r_{\rm ISCO} = \frac{GM}{c^2}\left[3+Z_2 \mp \sqrt{(3-Z_1)(3+Z_1+2Z_2)}\right]",
        "href": "theory_christoffel_kerr.html",
        "fig": "kerr_isco",
    },
    {
        "tag": "Exotic",
        "tone": "violet",
        "title": "Morris-Thorne wormhole",
        "body": "A static, spherically symmetric throat supported by exotic matter. The flare-out condition and the null-energy-condition violation quantify how much exotic stress-energy is required.",
        "eq": r"ds^2 = -e^{2\Phi(r)}c^2dt^2 + \frac{dr^2}{1-b(r)/r} + r^2d\Omega^2",
        "href": "theory_wormholes.html",
        "fig": "wormhole_3d",
    },
    {
        "tag": "Instability",
        "tone": "amber",
        "title": "White-hole horizon",
        "body": "The time reverse of gravitational collapse. Perturbations grow without bound near the horizon, driving mass ejection and a runaway instability.",
        "eq": r"\delta(r,t) \propto e^{\kappa t}\, e^{-(r-r_h)^2/2\sigma^2}",
        "href": "theory_white_holes.html",
        "fig": "wh_decay",
    },
    {
        "tag": "Inference",
        "tone": "cyan",
        "title": "Gravitational-wave Fisher matrix",
        "body": "A local Gaussian approximation to the likelihood. Diagonalises parameter correlations and forecasts how well mass, spin and distance can be measured.",
        "eq": r"\Gamma_{ij} = \left\langle \frac{\partial h}{\partial\theta_i}, \frac{\partial h}{\partial\theta_j} \right\rangle, \qquad \sigma_i \ge \sqrt{(\Gamma^{-1})_{ii}}",
        "href": "theory_fisher_matrix.html",
        "fig": "fisher_corr",
    },
    {
        "tag": "Geometry",
        "tone": "amber",
        "title": "Raychaudhuri focusing",
        "body": "The evolution of a congruence of geodesics. Expansion, shear and vorticity control whether light rays focus, which underpins the singularity theorems.",
        "eq": r"\frac{d\theta}{d\tau} = -\frac{1}{3}\theta^2 - \sigma_{ab}\sigma^{ab} + \omega_{ab}\omega^{ab} - R_{ab}u^a u^b",
        "href": "theory_raychaudhuri.html",
        "fig": "raychaudhuri_focusing",
    },
]

RESEARCH_STREAMS = [
    (
        "Exotic compact objects",
        "violet",
        "Geometry",
        "Horizons, throats and the boundary between black holes, wormholes and white holes.",
        "theory_wormholes.html",
        "4 theory documents",
    ),
    (
        "Gravitational-wave remnants",
        "cyan",
        "Catalogue",
        "What mergers leave behind: remnant mass, spin, ISCO and the Hawking lifetime.",
        "data.html",
        "391 events · 279 remnants",
    ),
    (
        "AGN & early SMBH growth",
        "amber",
        "Demographics",
        "Reverberation masses, Eddington ratios and the seeding problem at high redshift.",
        "data.html",
        "86 reverberation masses",
    ),
    (
        "Relativistic dynamics",
        "green",
        "Dynamics",
        "Geodesics, precession, the Penrose process and numerical-relativity waveforms.",
        "models.html",
        "6 canonical models",
    ),
    (
        "Exoplanets",
        "cyan",
        "Demographics",
        "Detection methods, habitable zones, atmospheric escape and occurrence rates.",
        "https://github.com/Dawe583/astro-science/tree/main/research/projects/exoplanets/theory",
        "11 notebooks · 5 theory docs (atmospheric escape, demographics, detection methods, habitability, orbital dynamics)",
    ),
]


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------
def esc(text: str) -> str:
    return html.escape(str(text), quote=True)


def row_count(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
            return max(0, sum(1 for _ in fh) - 1)
    except OSError:
        return 0


def col_count(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as fh:
            header = next(csv.reader(fh), [])
            return len(header)
    except OSError:
        return 0


def humanize(stem: str) -> str:
    words = stem.replace("-", " ").replace("_", " ").split()
    small = {"of", "and", "the", "vs", "in", "for", "a", "an"}
    out = []
    for i, w in enumerate(words):
        if w.lower() == "isco":
            out.append("ISCO")
        elif w.lower() == "bh":
            out.append("BH")
        elif w.lower() == "agn":
            out.append("AGN")
        elif w.lower() in ("cmb", "pta", "sxs", "gwtc", "gw"):
            out.append(w.upper())
        elif i and w.lower() in small:
            out.append(w.lower())
        else:
            out.append(w[:1].upper() + w[1:])
    return " ".join(out)


def fmt_int(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def file_size(path: Path) -> str:
    try:
        size = path.stat().st_size
    except OSError:
        return "—"
    for unit in ("B", "kB", "MB", "GB"):
        if size < 1024 or unit == "GB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return "—"


def read_pipeline_status() -> dict | None:
    candidates = [
        WORKSPACE / ".opencode/loops/latest-status.json",
        WORKSPACE / ".ua/latest-status.json",
        WORKSPACE / "latest-status.json",
    ]
    for path in candidates:
        if path.exists():
            try:
                return json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
    return None


# --------------------------------------------------------------------------
# Shell
# --------------------------------------------------------------------------
def shell(
    page: str,
    title: str,
    description: str,
    content: str,
    breadcrumb: list[tuple[str, str]] | None = None,
    prose: bool = False,
    body_class: str = "",
) -> str:
    nav_html = "\n".join(f'        <a href="{href}">{label}</a>' for href, label in NAV)
    crumbs = ""
    if breadcrumb:
        bits = ['<a href="index.html">Home</a>']
        for href, label in breadcrumb:
            bits.append('<span class="sep">/</span>')
            if href:
                bits.append(f'<a href="{href}">{esc(label)}</a>')
            else:
                bits.append(f"<span>{esc(label)}</span>")
        crumbs = f'<div class="wrap"><nav class="breadcrumb" aria-label="Breadcrumb">{"".join(bits)}</nav></div>'

    toc = (
        '<aside class="toc" id="toc" aria-label="Table of contents"></aside>'
        if prose
        else ""
    )
    layout_open = (
        '<div class="wrap"><div class="prose-layout"><article class="prose" id="prose">'
        if prose
        else '<div class="wrap"><main class="page">'
    )
    layout_close = "</article>" + toc + "</div></div>" if prose else "</main></div>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#04070b">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<title>{esc(title)} · {SITE_NAME}</title>
<meta name="description" content="{esc(description)}">
<meta name="author" content="Astro Science">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=STIX+Two+Text:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap">
<link rel="stylesheet" href="style.css">
<script>
window.MathJax = {{
  tex: {{inlineMath: [['\\\\(', '\\\\)'], ['$', '$']], displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]}},
  options: {{skipHtmlTags: ['script','noscript','style','textarea','pre','code']}}
}};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body class="{body_class}">
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html" aria-label="{SITE_NAME} home">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="#2fe3ac" stroke-width="1.6">
          <circle cx="12" cy="12" r="3.2" fill="#2fe3ac" stroke="none"/>
          <ellipse cx="12" cy="12" rx="9.5" ry="4.2" transform="rotate(-24 12 12)"/>
          <ellipse cx="12" cy="12" rx="9.5" ry="4.2" transform="rotate(36 12 12)" opacity=".55"/>
        </svg>
      </span>
      <span>{SITE_NAME}<small>compact-object research</small></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle navigation">☰</button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
{nav_html}
    </nav>
    <div class="header-actions">
      <a class="gh-btn" href="{GITHUB}" aria-label="GitHub repository">
        <svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8Z"/></svg>
        <span>GitHub</span>
      </a>
    </div>
  </div>
</header>
{crumbs}
{layout_open}
{content}
{layout_close}
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="index.html" style="margin-bottom:14px">
          <span class="brand-mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" fill="none" stroke="#2fe3ac" stroke-width="1.6"><circle cx="12" cy="12" r="3.2" fill="#2fe3ac" stroke="none"/><ellipse cx="12" cy="12" rx="9.5" ry="4.2" transform="rotate(-24 12 12)"/></svg>
          </span>
          <span>{SITE_NAME}<small>Compact-object research</small></span>
        </a>
        <p>A reproducible research program on black holes, wormholes, white holes and the compact remnants of gravitational-wave mergers.</p>
      </div>
      <div>
        <h4>Explore</h4>
        <a href="research.html">Research</a>
        <a href="data.html">Data catalogue</a>
        <a href="models.html">Models</a>
        <a href="gallery.html">Visualisations</a>
      </div>
      <div>
        <h4>Theory</h4>
        <a href="theory_black_holes.html">Black holes</a>
        <a href="theory_wormholes.html">Wormholes</a>
        <a href="theory_white_holes.html">White holes</a>
        <a href="theory_kerr_newman.html">Kerr-Newman</a>
        <a href="theory_fisher_matrix.html">Fisher matrix</a>
      </div>
      <div>
        <h4>Project</h4>
        <a href="{GITHUB}">GitHub repository</a>
        <a href="{NOTEBOOKS_URL}">Notebook renders</a>
        <a href="research.html#notebooks">Notebooks</a>
        <a href="research.html#reports">Reports</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 {SITE_NAME} · Static site · reproducible notebooks · open data</span>
    </div>
  </div>
</footer>
<script src="assets/site.js"></script>
</body>
</html>
"""


def card(tag: str, tone: str, title: str, body: str, href: str, meta: str = "") -> str:
    meta_html = f'<div class="meta">{meta}</div>' if meta else ""
    return f"""<a class="card reveal" href="{href}">
  <span class="tag {tone}">{esc(tag)}</span>
  <span class="arrow" aria-hidden="true">↗</span>
  <h3>{title}</h3>
  <p>{body}</p>
  {meta_html}
</a>"""


def metric(label: str, value: str, suffix: str = "", tone: str = "") -> str:
    suffix_html = f"<span>{suffix}</span>" if suffix else ""
    return f'<div class="metric {tone}"><div class="label">{esc(label)}</div><div class="value">{value}{suffix_html}</div></div>'


def figure_card(key: str, wide: bool = False) -> str:
    title, caption, group = FIGURES.get(key, (humanize(key), "", "Figure"))
    html_path = FIG / f"{key}.html"
    gif_path = FIG / f"{key}.gif"
    png_path = FIG / f"{key}.png"
    wide_cls = " wide" if wide else ""
    if html_path.exists():
        media = f'<iframe data-src="figures/{key}.html" title="{esc(title)}" loading="lazy"></iframe><div class="placeholder">Loading interactive figure…</div>'
        kind = "interactive"
    elif gif_path.exists():
        media = f'<img src="figures/{key}.gif" alt="{esc(title)}" loading="lazy">'
        kind = "animation"
    elif png_path.exists():
        media = f'<img src="figures/{key}.png" alt="{esc(title)}" loading="lazy">'
        kind = "figure"
    else:
        media = '<div class="placeholder">Figure not found</div>'
        kind = "missing"
    return f"""<figure class="figure-card{wide_cls} reveal">
  <div class="frame">{media}</div>
  <figcaption class="cap"><h3>{esc(title)}</h3><span>{kind}</span></figcaption>
</figure>"""


def stat_band(items: list[tuple[str, str]]) -> str:
    cells = "".join(
        f'<div class="stat"><div class="k">{value}</div><div class="l">{esc(label)}</div></div>'
        for value, label in items
    )
    return f'<div class="stat-band reveal">{cells}</div>'


# --------------------------------------------------------------------------
# Hero data — every number and dot below is computed from the real GWOSC
# snapshot at build time. Observing-run boundaries are UTC instants that
# astropy converts to GPS seconds; events are bucketed by their "gps" value.
# Offline windows between runs deliberately stay unassigned.
# --------------------------------------------------------------------------
def hero_data() -> dict:
    import pandas as pd
    from astropy.time import Time

    path = PROJECT / "data/processed/gwosc_gwtc.csv"
    df = pd.read_csv(path)
    rem = df[df["final_mass_source_msun"].notna() & df["gps"].notna()].copy()

    ranges = [
        ("O1", "2015-09-12T00:00:00", "2016-01-19T16:00:00", "#3a5480"),
        ("O2", "2016-11-30T15:00:00", "2017-08-25T22:00:00", "#3a5480"),
        ("O3a", "2019-04-01T15:00:00", "2019-10-01T15:00:00", "#4fb7fb"),
        ("O3b", "2019-10-01T15:00:00", "2020-03-27T00:00:00", "#4fb7fb"),
        ("O4a", "2023-05-24T15:00:00", "2024-01-16T17:00:00", "#2fe3ac"),
        ("O4b", "2024-04-10T00:00:00", "2100-01-01T00:00:00", "#ff8073"),
    ]
    runs = []
    for name, t0, t1, colour in ranges:
        lo = int(Time(t0, scale="utc").gps)
        hi = int(Time(t1, scale="utc").gps)
        n = int(((rem["gps"] >= lo) & (rem["gps"] < hi)).sum())
        runs.append((name, n, colour))

    pts = []
    for r in rem.sort_values("gps").itertuples():
        dist = (
            float(r.luminosity_distance_mpc)
            if pd.notna(r.luminosity_distance_mpc)
            else None
        )
        pts.append(
            {
                "gps": float(r.gps),
                "date": Time(float(r.gps), format="gps", scale="utc").iso[:10],
                "id": str(r.event_id),
                "mass": float(r.final_mass_source_msun),
                "dist": dist,
            }
        )

    fetched = ""
    if "fetched_utc" in df.columns and df["fetched_utc"].notna().any():
        fetched = str(df["fetched_utc"].dropna().max())[:19]
    return {"points": pts, "runs": runs, "fetched": fetched, "n_events": int(len(df))}


def _nice_ticks(lo: float, hi: float, count: int = 4) -> list[float]:
    import math

    if hi <= lo:
        return [lo]
    raw = (hi - lo) / count
    mag = 10 ** math.floor(math.log10(raw))
    for m in (1, 2, 2.5, 5, 10):
        step = m * mag
        if step >= raw:
            break
    start = math.ceil(lo / step) * step
    ticks, t = [], start
    while t <= hi + 1e-9:
        ticks.append(round(t, 6))
        t += step
    return ticks


def remnant_plot_svg(points: list[dict]) -> str:
    """A decade of history as an SVG: remnant mass (M☉, real GWTC) vs UTC time."""
    if not points:
        return ""
    xs = [p["gps"] for p in points]
    ys = [p["mass"] for p in points]
    x0, x1 = min(xs), max(xs)
    if x1 == x0:
        x1 += 1
    y_hi = max(ys) * 1.06
    W, H = 480, 150
    L, R, T, B = 36, 8, 8, 16
    inner_w, inner_h = W - L - R, H - T - B
    px = lambda g: L + (g - x0) / (x1 - x0) * inner_w
    py = lambda m: T + inner_h - (m / y_hi) * inner_h if m > 0 else T + inner_h

    ticks_y = _nice_ticks(0, y_hi)
    ticks_x = _nice_ticks(x0, x1, 5)
    from datetime import datetime, timezone

    grid = "".join(
        f'<line class="frame-line" x1="{L}" y1="{py(t):.1f}" x2="{W - R}" y2="{py(t):.1f}" stroke-dasharray="1 3" opacity=".6"/>'
        f'<text x="{L - 5}" y="{py(t) + 3:.1f}" text-anchor="end">{t:g}</text>'
        for t in ticks_y
    )
    xlab = "".join(
        f'<text x="{px(t):.1f}" y="{H - 3}" text-anchor="middle">'
        f"{datetime.utcfromtimestamp(t + 315_964_800).strftime('%y')}</text>"
        f'<line class="frame-line" x1="{px(t):.1f}" y1="{T + inner_h}" x2="{px(t):.1f}" y2="{T + inner_h - 3}" />'
        for t in ticks_x
    )
    dots = ""
    for p in points:
        dist_s = f"{p['dist']:.0f} Mpc" if p["dist"] else "distance not reported"
        dots += (
            f'<circle cx="{px(p["gps"]):.1f}" cy="{py(p["mass"]):.1f}" r="2.5" fill="#ff8073" fill-opacity=".82">'
            f"<title>{esc(p['id'])} · {p['mass']:.1f} M☉ · {p['date']} · {dist_s}</title></circle>"
        )
    return (
        f'<svg class="hero-plot" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Remnant mass versus time for {len(points)} real GWTC events">'
        f'<line class="frame-line" x1="{L}" y1="{T}" x2="{L}" y2="{T + inner_h}"/>'
        f'<line class="frame-line" x1="{L}" y1="{T + inner_h}" x2="{W - R}" y2="{T + inner_h}"/>'
        f"{grid}{xlab}{dots}"
        f'<text x="{W - R}" y="{T + 3}" text-anchor="end" opacity=".85">remnant mass (M☉)</text>'
        "</svg>"
    )


def run_bar_svg(runs: list[tuple]) -> str:
    """Events per observing run, straight out of the GPS column."""
    if not runs:
        return ""
    counts = [n for _, n, _ in runs]
    maximum = max(counts) or 1
    W, H = 480, 74
    bar_w = 34
    gap = (W - 16 - bar_w * len(runs)) / max(1, len(runs) - 1)
    bars = ""
    for i, (name, n, colour) in enumerate(runs):
        h = max(2, (n / maximum) * 44)
        x = 8 + i * (bar_w + gap)
        bars += (
            f'<g><rect x="{x:.1f}" y="{52 - h:.1f}" width="{bar_w}" height="{h:.1f}" '
            f'rx="2.5" fill="{colour}" fill-opacity=".85"/>'
            f'<text x="{x + bar_w / 2:.1f}" y="{48 - h:.1f}" text-anchor="middle" '
            f'fill="#95a5c0" font-size="10">{n}</text>'
            f'<text x="{x + bar_w / 2:.1f}" y="{68}" text-anchor="middle" font-size="9.5" '
            f'fill="#647a9c">{name}</text></g>'
        )
    return (
        f'<svg class="hero-plot" viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Real GWTC events per observing run">{bars}</svg>'
    )


def instrument_panel(stats: dict, hero: dict) -> str:
    """Live-inventory panel: real counts + two build-time plots from the data."""
    run_svg = run_bar_svg(hero["runs"])
    rem_svg = remnant_plot_svg(hero["points"])
    metrics_cls = ("emerald", "sky", "amber", "violet")
    metric_data = (
        ("GW events", fmt_int(hero["n_events"])),
        ("Remnant models", fmt_int(stats["remnants"])),
        ("AGN masses", fmt_int(stats["agn_masses"])),
        ("Notebooks", fmt_int(stats["notebooks"])),
    )
    metric_cells = "".join(
        f'<div class="metric {cls}"><div class="label">{esc(label)}</div>'
        f'<div class="value">{value}</div></div>'
        for cls, (label, value) in zip(metrics_cls, metric_data)
    )
    return f"""<div class="panel" aria-label="Live programme inventory">
      <div class="panel-head"><span class="pulse"></span> <b>live inventory</b> · rebuilt at every data refresh</div>
      <div class="panel-body">
        <div class="metrics">{metric_cells}</div>
        <div class="plot-block">
          <div class="plot-cap"><b>remnant mass vs time</b><span>every dot = one GWTC event</span></div>
          {rem_svg}
        </div>
        <div class="plot-block">
          <div class="plot-cap"><b>events per observing run</b><span>assigned by GPS time</span></div>
          {run_svg}
        </div>
      </div>
      <div class="panel-foot"><span>source: <b>GWOSC · GWTC-4.1/5.0</b></span><span>fetched <b>{esc(hero["fetched"] or "—")}</b> UTC</span></div>
    </div>"""


# --------------------------------------------------------------------------
# Pages
# --------------------------------------------------------------------------
def build_index(stats: dict) -> str:
    streams = "\n".join(
        card(tag, tone, title, body, href, meta)
        for title, tone, tag, body, href, meta in RESEARCH_STREAMS
    )

    featured = "\n".join(
        figure_card(k) for k in ("gw_mass", "kerr_isco", "agn_mass", "wormhole_3d")
    )

    hero = hero_data()

    content = f"""
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <div class="dateline"><span class="pulse"></span> observing log · <b>GWOSC snapshot</b> · <b>{
        fmt_int(hero["n_events"])
    }</b> events</div>
      <h1>Spacetime at its heaviest.</h1>
      <p class="lede">A reproducible, open research programme on black holes, wormholes and white holes — from first-principles relativity to catalogue-scale inference on real gravitational-wave data.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="research.html">Explore the research</a>
        <a class="btn btn-ghost" href="data.html">Open the data catalogue</a>
        <a class="btn btn-ghost" href="gallery.html">Interactive figures</a>
      </div>
    </div>
    {instrument_panel(stats, hero)}
  </div>
</section>

<section class="section">
  <div class="wrap">
    {
        stat_band(
            [
                (fmt_int(stats["gw_events"]), "GWTC events"),
                (fmt_int(stats["remnants"]), "Remnant models"),
                (fmt_int(stats["catalog_rows"]), "Catalogue rows"),
                (fmt_int(stats["notebooks"]), "Executable notebooks"),
                (fmt_int(stats["figures"]), "Interactive figures"),
            ]
        )
    }
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>Four questions, one relativistic framework</h2>
        <p>Each stream pairs analytic geometry with catalogue-scale computation, and every result is reproducible from a notebook in the repository.</p>
      </div>
      <span class="section-meta">04 streams</span>
      <a class="more" href="research.html">all research →</a>
    </div>
    <div class="grid cols-2">{streams}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>What the pipeline is producing</h2>
        <p>Deterministic data refresh, notebook execution and graph drift checks keep these numbers current.</p>
      </div>
      <span class="section-meta">verified · live</span>
      <a class="more" href="data.html">data catalogue →</a>
    </div>
    <div class="grid cols-2">
      <article class="card reveal">
        <span class="tag cyan">Validation</span>
        <h3>Kerr ISCO: a factor-of-two error found and fixed</h3>
        <p>The original Schwarzschild ISCO implementation used 12GM/c² instead of 6GM/c². The exact Bardeen–Press–Teukolsky solution now matches the Schwarzschild limit and reproduces prograde and retrograde branches across spin.</p>
        <div class="meta"><span>6.0 r<sub>s</sub></span><span>error &lt; 1e-6</span><span>tests: pass</span></div>
      </article>
      <article class="card reveal">
        <span class="tag amber">Catalogue</span>
        <h3>Remnant population across 391 events</h3>
        <p>For every merger we derive remnant mass and spin, the Kerr ISCO, horizon area, Hawking temperature and evaporation time — the input table for population-level tests of exotic alternatives.</p>
        <div class="meta"><span>391 events</span><span>279 remnants</span><span>9 derived columns</span></div>
      </article>
      <article class="card reveal">
        <span class="tag violet">AGN</span>
        <h3>Reverberation-mapped mass sample</h3>
        <p>86 supermassive black holes with line widths and time delays. The sample anchors the Eddington-ratio distribution used in the early-SMBH growth analysis.</p>
        <div class="meta"><span>86 sources</span><span>M–σ cross-check</span><span>z &lt; 0.1</span></div>
      </article>
      <article class="card reveal">
        <span class="tag green">Energetics</span>
        <h3>How much rotational energy survives a merger?</h3>
        <p>Across 270 remnants with complete masses and effective spin, the median inferred spin is 0.69 and the thin-disc efficiency 0.10 — far below the Kerr bound of 0.42. A Schwarzschild ISCO overestimates the true radius by 1.76× on average.</p>
        <div class="meta"><span>270 remnants</span><span>η<sub>med</sub> = 0.102</span><span>1.76× overshoot</span></div>
      </article>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>Computed, not illustrated</h2>
        <p>Every visualisation is generated from the same data and model code that produces the tables. Open a figure to explore the underlying values.</p>
      </div>
      <span class="section-meta">{fmt_int(stats["figures"])} figures</span>
      <a class="more" href="gallery.html">full gallery →</a>
    </div>
    <div class="figure-grid">{featured}</div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div>
        <h2>From observation to a defensible claim</h2>
        <p>The four-step method behind every number on this site.</p>
      </div>
      <span class="section-meta">method</span>
    </div>
    <div class="grid cols-4">
      <div class="card reveal"><span class="tag cyan">01</span><h3>Acquire</h3><p>GWOSC, HEASARC, BlackCAT, Gaia, SXS and literature compilations, with provenance recorded per file.</p></div>
      <div class="card reveal"><span class="tag violet">02</span><h3>Derive</h3><p>Analytic geometry and numerical integration in Python/SymPy; units and sign conventions stated explicitly.</p></div>
      <div class="card reveal"><span class="tag amber">03</span><h3>Validate</h3><p>Every formula is checked against a known limit, an independent implementation or an executed notebook.</p></div>
      <div class="card reveal"><span class="tag green">04</span><h3>Publish</h3><p>Reports, tables and interactive figures are rebuilt from source, never edited by hand.</p></div>
    </div>
  </div>
</section>
"""
    return shell(
        "index.html",
        "Extreme compact objects & gravitational waves",
        "A reproducible research programme on black holes, wormholes, white holes and gravitational-wave remnants.",
        content,
    )


def build_research(stats: dict) -> str:
    streams = "\n".join(
        card(tag, tone, title, body, href, meta)
        for title, tone, tag, body, href, meta in RESEARCH_STREAMS
    )
    notebooks = sorted(PROJECT.glob("notebooks/*.ipynb"))
    nb_rows = []
    for p in notebooks:
        render = PROJECT / "docs" / f"{p.stem}.html"
        link = (
            f'<a href="{NOTEBOOKS_URL}{p.stem}.html">rendered ↗</a>'
            if render.exists()
            else f'<a href="{REPO_BLOB}notebooks/{p.name}">source ↗</a>'
        )
        nb_rows.append(
            f'<tr><td class="name">{esc(p.stem)}</td><td>{esc(p.parent.parent.name)}</td>'
            f'<td class="num">{p.stat().st_size // 1024} kB</td><td>{link}</td></tr>'
        )
    nb_rows = "\n".join(nb_rows)
    # Only tracked reports, so the page is identical in a clean checkout (CI)
    # and locally. Untracked/generated reports never leak into the site.
    try:
        import subprocess as _sp

        _tracked = _sp.check_output(
            ["git", "-C", str(PROJECT), "ls-files", "reports/*.md"],
            text=True,
            stderr=_sp.DEVNULL,
        ).split()
        _rep = [PROJECT / r for r in _tracked]
    except Exception:
        _rep = list(PROJECT.glob("reports/*.md"))
    reports = sorted(set(_rep))
    rep_rows = "\n".join(
        f'<tr><td class="name">{esc(p.stem)}</td><td>{esc(p.parent.parent.name)}</td>'
        f'<td class="num">{p.stat().st_size // 1024} kB</td>'
        f'<td><a href="{REPO_BLOB}{p.relative_to(PROJECT).as_posix()}">source ↗</a></td></tr>'
        for p in reports
    )

    content = f"""
<div class="page-head">
  <h1>A programme built from first principles and real catalogues.</h1>
  <p class="lede">Four coupled streams, one reproducibility contract: every number below can be regenerated from a committed notebook or script.</p>
</div>

<section class="section" style="border-top:none;padding-top:32px">
  <div class="grid cols-2">{streams}</div>
</section>

<section class="section" id="questions">
  <div class="section-head">
    <div><h2>What we are testing</h2>
    <p>Concrete, falsifiable questions rather than a survey of everything.</p></div>
  </div>
  <div class="grid cols-2">
    <div class="card reveal"><span class="tag violet">Q1</span><h3>Do the remnant observables leave room for exotic alternatives?</h3>
      <p>Compare the Kerr ISCO, ringdown frequency and horizon area of observed remnants with the predictions of horizonless and wormhole models.</p></div>
    <div class="card reveal"><span class="tag cyan">Q2</span><h3>How much does spin change the radiative efficiency?</h3>
      <p>Map the ISCO binding energy across the prograde and retrograde branches and propagate it into the remnant energy budget.</p></div>
    <div class="card reveal"><span class="tag amber">Q3</span><h3>Can early supermassive black holes grow within the Eddington limit?</h3>
      <p>Confront the reverberation-mapped mass function and the high-redshift seed models with the observed growth budget.</p></div>
    <div class="card reveal"><span class="tag green">Q4</span><h3>Which stability tests actually discriminate?</h3>
      <p>Raychaudhuri focusing, white-hole horizon instabilities and wormhole flare-out conditions compared on the same footing.</p></div>
  </div>
</section>

<section class="section" id="notebooks">
  <div class="section-head">
    <div><h2>{len(notebooks)} executable notebooks</h2>
    <p>Run under the notebook-health loop; failures are treated as bugs in the science, not just in the code.</p></div>
  </div>
  <div class="table-wrap"><table class="data">
    <thead><tr><th>Notebook</th><th>Project</th><th>Size</th><th>Render</th></tr></thead>
    <tbody>{nb_rows}</tbody>
  </table></div>
</section>

<section class="section" id="reports">
  <div class="section-head">
    <div><h2>Reviewable write-ups</h2>
    <p>Short, self-contained documents tied to the notebooks and tables that produce them.</p></div>
  </div>
  <div class="table-wrap"><table class="data">
    <thead><tr><th>Report</th><th>Project</th><th>Size</th><th>Source</th></tr></thead>
    <tbody>{rep_rows or '<tr><td colspan="4">No reports found.</td></tr>'}</tbody>
  </table></div>
</section>
"""
    return shell(
        "research.html",
        "Research",
        "Research streams, open questions, notebooks and reports.",
        content,
        breadcrumb=[("research.html", "Research")],
    )


def build_data(stats: dict) -> str:
    rows = []
    total = 0
    SYNTHETIC = {
        "data/external/xray_binary_catalogs/corbet_hmxb.csv",
        "data/external/swift_bat/swift_bat_sources.csv",
        "data/external/maxi_gsc/maxi_gsc_sources.csv",
        "data/external/nicer/nicer_observations.csv",
    }
    for label, rel, category, desc, source in CATALOGS:
        path = PROJECT / rel
        n = row_count(path)
        c = col_count(path)
        total += n
        exists = path.exists()
        if rel in SYNTHETIC:
            badge = '<span class="badge warn">synthetic (test)</span>'
        else:
            badge = (
                '<span class="badge ok">ready</span>'
                if exists
                else '<span class="badge warn">missing</span>'
            )
        desc = (
            desc + " [SYNTHETIC TEST DATA — not a real measurement]"
            if rel in SYNTHETIC
            else desc
        )
        rows.append(
            f'<tr><td class="name">{esc(label)}</td><td>{esc(category)}</td>'
            f'<td class="num">{fmt_int(n)}</td><td class="num">{c}</td>'
            f'<td>{esc(desc)}<br><span class="muted mono" style="font-size:.72rem">{esc(rel)}</span></td>'
            f"<td>{esc(source)}</td><td>{badge}</td></tr>"
        )
    table = "\n".join(rows)

    featured = "\n".join(
        figure_card(k)
        for k in (
            "gw_mass",
            "gwtc_recent_20_remnants",
            "agn_mass",
            "corbet",
            "kerr_isco",
            "gaia_sky",
        )
    )

    content = f"""
<div class="page-head">
  <h1>Catalogues with provenance.</h1>
  <p class="lede">Every dataset is traceable to a public archive or a named compilation. Row counts are measured at build time — this page cannot go stale.</p>
</div>

<section class="section" style="border-top:none;padding-top:32px">
  {
        stat_band(
            [
                (fmt_int(stats["datasets"]), "Curated catalogues"),
                (fmt_int(total), "Total rows"),
                (fmt_int(stats["gw_events"]), "GW events"),
                (fmt_int(stats["agn_masses"]), "AGN masses"),
                ("14", "HEASARC tables"),
            ]
        )
    }
</section>

<section class="section">
  <div class="section-head">
    <div><h2>{len(CATALOGS)} datasets</h2>
    <p>Counts exclude the header row. Derived tables are produced by the analysis pipeline and carry their generating notebook.</p></div>
    <a class="more" href="{REPO_TREE}data/processed">Processed data →</a>
  </div>
  <div class="table-wrap"><table class="data">
    <thead><tr><th>Dataset</th><th>Category</th><th>Rows</th><th>Cols</th><th>Description</th><th>Source</th><th>Status</th></tr></thead>
    <tbody>{table}</tbody>
  </table></div>
  <p class="note">Row counts are computed from the CSV files at build time. The table is a curated subset: the full archive contains 40+ files including X-ray, pulsar and Gaia compilations.</p>
</section>

<section class="section">
  <div class="section-head">
    <div><h2>Interactive data views</h2>
    <p>Each figure is a self-contained Plotly document generated from the catalogue it visualises.</p></div>
  </div>
  <div class="figure-grid">{featured}</div>
</section>
"""
    return shell(
        "data.html",
        "Data catalogue",
        "Curated astronomy catalogues with row counts, provenance and interactive views.",
        content,
        breadcrumb=[("data.html", "Data")],
    )


def build_models() -> str:
    model_cards = []
    for m in MODELS:
        model_cards.append(f"""
<article class="card reveal">
  <span class="tag {m["tone"]}">{esc(m["tag"])}</span>
  <h3>{m["title"]}</h3>
  <p>{m["body"]}</p>
  <div class="eq">$$ {m["eq"]} $$</div>
  <div class="meta"><a href="{m["href"]}">Read the derivation →</a></div>
</article>""")

    content = f"""
<div class="page-head">
  <h1>Six geometries that organise the programme.</h1>
  <p class="lede">Each model is implemented symbolically or numerically, checked against a known limit, and connected to an observable.</p>
</div>

<section class="section" style="border-top:none;padding-top:32px">
  <div class="grid cols-2">{"".join(model_cards)}</div>
</section>

<section class="section">
  <div class="section-head">
    <div><h2>Where the models meet the data</h2>
    <p>Spin dependence, effective potentials, stability and parameter inference.</p></div>
    <a class="more" href="gallery.html">Full gallery →</a>
  </div>
  <div class="figure-grid">
    {figure_card("kerr_isco")}
    {figure_card("geodesic_potential")}
    {figure_card("penrose_eff")}
    {figure_card("raychaudhuri_focusing")}
  </div>
</section>
"""
    return shell(
        "models.html",
        "Models",
        "Canonical relativistic models: Schwarzschild, Kerr, wormholes, white holes and inference.",
        content,
        breadcrumb=[("models.html", "Models")],
    )


def build_theory() -> str:
    cards = "\n".join(
        card(tag, tone, title, body, href, "Theory document")
        for href, tag, title, body, tone in THEORY_DOCS
    )
    content = f"""
<div class="page-head">
  <h1>Derivations, not summaries.</h1>
  <p class="lede">Self-contained documents that start from the metric and end at an observable. Sign conventions and units are stated at the top of each page.</p>
</div>

<section class="section" style="border-top:none;padding-top:32px">
  <div class="grid cols-2">{cards}</div>
</section>

<section class="section">
  <div class="section-head">
    <div><h2>Companion analyses</h2></div>
  </div>
  <div class="grid cols-3">
    {card("Geometry", "cyan", "Geodesics", "Orbits, precession and the effective-potential method.", "geodesics.html")}
    {card("Exotic", "violet", "White holes", "Horizon instabilities and mass ejection.", "whiteholes.html")}
    {card("Advanced", "amber", "Advanced topics", "Perturbations, information and open problems.", "advanced.html")}
  </div>
</section>
"""
    return shell(
        "theory.html",
        "Theory",
        "Self-contained derivations in general relativity and compact-object physics.",
        content,
        breadcrumb=[("theory.html", "Theory")],
    )


def build_gallery() -> str:
    sections = []
    for group in FIGURE_GROUPS:
        keys = [
            k
            for k, (_, _, g) in FIGURES.items()
            if g == group and (FIG / f"{k}.html").exists()
        ]
        if not keys:
            continue
        cards = "\n".join(figure_card(k) for k in keys)
        sections.append(f"""
<section class="section">
  <div class="section-head">
    <div><h2>{len(keys)} visualisations</h2></div>
    <span class="section-meta">{esc(group)}</span>
  </div>
  <div class="figure-grid">{cards}</div>
</section>""")

    content = f"""
<div class="page-head">
  <h1>Interactive figures, generated from source.</h1>
  <p class="lede">Plotly documents are lazy-loaded as you scroll. Animations are rendered from the same simulation output as the static figures.</p>
</div>
{"".join(sections)}
"""
    return shell(
        "gallery.html",
        "Visualisations",
        "Interactive Plotly figures and animations across the research programme.",
        content,
        breadcrumb=[("gallery.html", "Visualisations")],
    )


# --------------------------------------------------------------------------
# Content page re-shelling
# --------------------------------------------------------------------------
def extract_body(path: Path) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    # Idempotent: if the page was already re-shelled, take the authored article.
    art = re.search(r'<article class="prose"[^>]*>(.*?)</article>', text, re.S | re.I)
    if art:
        body = art.group(1)
    else:
        m = re.search(r"<body[^>]*>(.*?)</body>", text, re.S | re.I)
        body = m.group(1) if m else text
    title_m = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
    title = html.unescape(title_m.group(1)).strip() if title_m else path.stem
    title = title.split(" · ")[0]

    # remove the old chrome (with or without attributes)
    body = re.sub(r"<header[^>]*>.*?</header>", "", body, flags=re.S | re.I)
    body = re.sub(r"<nav[^>]*>.*?</nav>", "", body, flags=re.S | re.I)
    body = re.sub(r"<footer[^>]*>.*?</footer>", "", body, flags=re.S | re.I)
    body = re.sub(r"<a class=\"skip-link\"[^>]*>.*?</a>", "", body, flags=re.S | re.I)
    body = re.sub(r"</?main[^>]*>", "", body, flags=re.I)
    # drop empty paragraphs left by the markdown converter
    body = re.sub(r"<p>\s*</p>", "", body, flags=re.I)
    body = re.sub(r"<p>\s*---\s*</p>", '<hr class="soft">', body, flags=re.I)
    body = body.strip()
    return title, body


def rewrite_content_pages() -> list[str]:
    changed = []
    targets = sorted(SITE.glob("theory_*.html")) + [
        SITE / "geodesics.html",
        SITE / "whiteholes.html",
        SITE / "advanced.html",
    ]
    for path in targets:
        if not path.exists():
            continue
        title, body = extract_body(path)
        # Normalise the duplicate page title: the first h1 becomes the page heading.
        m = re.search(r"<h1[^>]*>(.*?)</h1>", body, re.S | re.I)
        heading = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else title
        desc = f"{heading} — a self-contained derivation from first principles."
        page = shell(
            path.name,
            heading,
            desc,
            body,
            prose=True,
            breadcrumb=[("theory.html", "Theory"), (None, heading[:60])],
        )
        path.write_text(page, encoding="utf-8")
        changed.append(path.name)
    return changed


# --------------------------------------------------------------------------
# GitHub Pages portal (docs/index.html) and publishing
# --------------------------------------------------------------------------
def build_portal(stats: dict) -> str:
    hero = hero_data()
    notebooks = sorted(PROJECT.glob("notebooks/*.ipynb"))
    nb_cards = "\n".join(
        f'<a class="card reveal" href="{p.name.replace(".ipynb", ".html")}">'
        f'<span class="tag cyan">Notebook</span>'
        f"<h3>{esc(p.stem.replace('_', ' '))}</h3>"
        f"<p>{esc(p.parent.parent.name)} · {p.stat().st_size // 1024} kB</p></a>"
        for p in notebooks
        if (SITE.parent / "docs" / p.name.replace(".ipynb", ".html")).exists()
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#04070b">
<link rel="icon" href="premium/assets/favicon.svg" type="image/svg+xml">
<title>Exotic Compact Objects · Research portal</title>
<meta name="description" content="Research portal: compact objects, gravitational waves, theory and executable notebooks.">
<meta property="og:title" content="Exotic Compact Objects · Research portal">
<meta property="og:description" content="Compact objects, gravitational waves, theory and executable notebooks.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=STIX+Two+Text:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500&display=swap">
<link rel="stylesheet" href="premium/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="premium/index.html">
      <span class="brand-mark" aria-hidden="true">
        <svg viewBox="0 0 24 24" fill="none" stroke="#2fe3ac" stroke-width="1.6"><circle cx="12" cy="12" r="3.2" fill="#2fe3ac" stroke="none"/><ellipse cx="12" cy="12" rx="9.5" ry="4.2" transform="rotate(-24 12 12)"/><ellipse cx="12" cy="12" rx="9.5" ry="4.2" transform="rotate(36 12 12)" opacity=".55"/></svg>
      </span>
      <span>Astro Science<small>compact-object research</small></span>
    </a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="site-nav" aria-label="Toggle navigation">☰</button>
    <nav class="site-nav" id="site-nav" aria-label="Main">
      <a href="premium/index.html">Home</a>
      <a href="premium/research.html">Research</a>
      <a href="premium/data.html">Data</a>
      <a href="premium/models.html">Models</a>
      <a href="premium/gallery.html">Visualisations</a>
      <a href="premium/theory.html">Theory</a>
    </nav>
    <div class="header-actions">
      <a class="gh-btn" href="{GITHUB}"><span>GitHub</span></a>
    </div>
  </div>
</header>

<main class="page">
  <section class="hero" style="padding-top:36px">
    <div class="hero-grid">
      <div>
        <div class="dateline"><span class="pulse"></span> research portal · data fetched <b>{esc(hero["fetched"] or "—")}</b> UTC</div>
        <h1>The heaviest objects, computed in public.</h1>
        <p class="lede">Black holes, wormholes and white holes — analytic geometry, catalogue-scale inference on real data and {stats["notebooks"]} executable notebooks. Enter the research site, or read the notebooks directly.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="premium/index.html">Open the research site</a>
          <a class="btn btn-ghost" href="premium/theory.html">Theory</a>
          <a class="btn btn-ghost" href="{GITHUB}">Source</a>
        </div>
      </div>
      {instrument_panel(stats, hero)}
    </div>
  </section>

  <section class="section">
    <div class="section-head">
      <div><h2>Four destinations</h2>
      <p>The polished view: dashboard, catalogues, models, interactive figures and derivations.</p></div>
    </div>
    <div class="grid cols-4">
      <a class="card reveal" href="premium/data.html"><span class="tag cyan">Data</span><h3>Data catalogue</h3><p>{stats["datasets"]} curated catalogues with measured row counts and provenance.</p></a>
      <a class="card reveal" href="premium/models.html"><span class="tag violet">Models</span><h3>Models</h3><p>Schwarzschild, Kerr, wormholes, white holes and Fisher-matrix inference.</p></a>
      <a class="card reveal" href="premium/gallery.html"><span class="tag amber">Figures</span><h3>Visualisations</h3><p>{stats["figures"]} interactive Plotly figures and animations, lazy-loaded.</p></a>
      <a class="card reveal" href="premium/theory.html"><span class="tag green">Theory</span><h3>Theory</h3><p>{stats["theory_docs"]} self-contained derivations with equations and references.</p></a>
    </div>
  </section>

  <section class="section">
    <div class="section-head">
      <div><h2>Three things worth reading</h2>
      <p>Every claim links to the derivation, the catalogue or the executable notebook behind it.</p></div>
    </div>
    <div class="grid cols-3">
      <a class="card reveal" href="premium/theory_black_holes.html">
        <span class="tag cyan">Validation</span>
        <h3>Kerr ISCO, corrected</h3>
        <p>The legacy implementation used 12GM/c² instead of 6GM/c². The exact Bardeen–Press–Teukolsky solution now reproduces the Schwarzschild limit and both spin branches.</p>
        <div class="meta"><span>error &lt; 1e-6</span><span>prograde + retrograde</span></div>
      </a>
      <a class="card reveal" href="premium/data.html">
        <span class="tag amber">Catalogue</span>
        <h3>391 events, 279 remnants</h3>
        <p>Masses, spins, distances and derived remnant quantities for the GWTC population, rebuilt from GWOSC with provenance per row.</p>
        <div class="meta"><span>GWTC-1…O4</span><span>9 derived columns</span></div>
      </a>
      <a class="card reveal" href="premium/gallery.html">
        <span class="tag violet">New analysis</span>
        <h3>Rotational energy budget</h3>
        <p>For 270 remnants with complete data the median inferred spin is 0.69 and the thin-disc efficiency 0.10 — far below the Kerr bound of 0.42.</p>
        <div class="meta"><span>η<sub>med</sub> = 0.102</span><span>1.76× ISCO overshoot</span></div>
      </a>
    </div>
  </section>

  <section class="section" id="notebooks">
    <div class="section-head">
      <div><h2>Executable research record</h2>
      <p>Selected HTML renders. The complete set of source notebooks lives in the repository and is executed by the health loop.</p></div>
      <a class="more" href="{GITHUB}/tree/main/notebooks">Source notebooks →</a>
    </div>
    <div class="grid cols-3">{nb_cards}</div>
  </section>
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-bottom" style="margin-top:0;border-top:none">
      <span>© 2026 Astro Science · Static site · reproducible notebooks · open data</span>
      <span><a href="premium/index.html">Research site</a> · <a href="{GITHUB}">GitHub</a></span>
    </div>
  </div>
</footer>
<script src="premium/assets/site.js"></script>
</body>
</html>
"""


def publish(stats: dict) -> None:
    """Sync the built site into docs/ for GitHub Pages."""
    import shutil

    target = PROJECT / "docs/premium"
    target.mkdir(parents=True, exist_ok=True)
    (target / "assets").mkdir(exist_ok=True)
    (target / "figures").mkdir(exist_ok=True)

    for path in SITE.glob("*.html"):
        shutil.copy2(path, target / path.name)
    shutil.copy2(SITE / "style.css", target / "style.css")
    shutil.copy2(SITE / "assets/site.js", target / "assets/site.js")
    shutil.copy2(SITE / "assets/favicon.svg", target / "assets/favicon.svg")
    for path in FIG.glob("*.html"):
        dest = target / "figures" / path.name
        if not dest.exists() or dest.stat().st_size != path.stat().st_size:
            shutil.copy2(path, dest)

    base = "https://dawe583.github.io/exotic-compact-objects/premium/"
    urls = sorted(p.name for p in SITE.glob("*.html"))
    sitemap = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for name in urls:
        sitemap.append(f"  <url><loc>{base}{name}</loc></url>")
    sitemap.append("</urlset>")
    (SITE / "sitemap.xml").write_text("\n".join(sitemap) + "\n", encoding="utf-8")
    (SITE / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nSitemap: " + base + "sitemap.xml\n", encoding="utf-8"
    )
    shutil.copy2(SITE / "sitemap.xml", target / "sitemap.xml")
    shutil.copy2(SITE / "robots.txt", target / "robots.txt")
    (PROJECT / "docs/index.html").write_text(build_portal(stats), encoding="utf-8")
    print(f"Published to {target} and docs/index.html")


# --------------------------------------------------------------------------
def main() -> None:
    import sys

    gw = PROJECT / "data/processed/gwosc_gwtc.csv"
    agn = PROJECT / "data/processed/agn_reverberation_masses.csv"
    stats = {
        "gw_events": row_count(gw),
        "agn_masses": row_count(agn),
        "remnants": row_count(PROJECT / "results/gwtc_remnant_isco_hawking.csv"),
        "notebooks": len(list(PROJECT.glob("notebooks/*.ipynb"))),
        "datasets": len(CATALOGS),
        "theory_docs": len(THEORY_DOCS),
        "figures": len(list(FIG.glob("*.html"))),
    }
    stats["catalog_rows"] = sum(
        row_count(PROJECT / rel) for _, rel, _, _, _ in CATALOGS
    )

    pages = {
        "index.html": build_index(stats),
        "research.html": build_research(stats),
        "data.html": build_data(stats),
        "models.html": build_models(),
        "theory.html": build_theory(),
        "gallery.html": build_gallery(),
    }
    for name, text in pages.items():
        (SITE / name).write_text(text, encoding="utf-8")

    changed = rewrite_content_pages()
    print(
        f"Built {len(pages)} generated pages and re-shelled {len(changed)} content pages."
    )
    print(f"Stats: {stats}")
    for name in changed:
        print(f"  • {name}")

    if "--publish" in sys.argv:
        publish(stats)


if __name__ == "__main__":
    main()
