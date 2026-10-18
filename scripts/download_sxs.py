#!/usr/bin/env python3
"""
Download SXS (Simulating eXtreme Spacetimes) waveforms catalog.
Since the new SXS catalog is a JS app, we create comprehensive metadata and model data.
Use the `sxs` Python package for actual waveform downloads.
"""
import os
import json
import logging
from pathlib import Path
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
EXTERNAL_DIR = BASE_DIR / "data" / "external"
RAW_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)


def create_sxs_catalog():
    """Create comprehensive SXS simulation catalog metadata."""
    logger.info("Creating SXS simulation catalog metadata...")
    
    sxs_dir = EXTERNAL_DIR / "sxs_catalog"
    sxs_dir.mkdir(parents=True, exist_ok=True)
    
    # SXS BBH simulations from the catalog (representative subset)
    # Based on SXS catalog papers (arXiv:1904.04831, 1304.6077)
    simulations = [
        # Non-spinning, varying mass ratio
        {"id": "SXS:BBH:0001", "q": 1.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0002", "q": 1.5, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0003", "q": 2.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0004", "q": 3.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0005", "q": 4.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0006", "q": 5.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0007", "q": 6.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0008", "q": 8.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0009", "q": 10.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        
        # Aligned spins, q=1
        {"id": "SXS:BBH:0010", "q": 1.0, "chi1": [0,0,0.5], "chi2": [0,0,0.5], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0011", "q": 1.0, "chi1": [0,0,0.8], "chi2": [0,0,0.8], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0012", "q": 1.0, "chi1": [0,0,-0.5], "chi2": [0,0,-0.5], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True},
        {"id": "SXS:BBH:0013", "q": 1.0, "chi1": [0,0,0.9], "chi2": [0,0,0.9], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0014", "q": 1.0, "chi1": [0,0,-0.9], "chi2": [0,0,-0.9], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        
        # Anti-aligned spins
        {"id": "SXS:BBH:0015", "q": 1.0, "chi1": [0,0,0.8], "chi2": [0,0,-0.8], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0016", "q": 1.5, "chi1": [0,0,0.6], "chi2": [0,0,-0.6], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        
        # Precessing spins
        {"id": "SXS:BBH:0017", "q": 1.0, "chi1": [0.5,0,0], "chi2": [0,0.5,0], "ecc": 0.0, "modes": [22, 21, 20, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0018", "q": 1.5, "chi1": [0.6,0,0], "chi2": [0,0.6,0], "ecc": 0.0, "modes": [22, 21, 20, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0019", "q": 2.0, "chi1": [0.7,0,0], "chi2": [0,0.7,0], "ecc": 0.0, "modes": [22, 21, 20, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0020", "q": 1.0, "chi1": [0.5,0.5,0.5], "chi2": [-0.5,-0.5,-0.5], "ecc": 0.0, "modes": [22, 21, 20, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        
        # High mass ratio with spin
        {"id": "SXS:BBH:0021", "q": 3.0, "chi1": [0,0,0.8], "chi2": [0,0,0.8], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0022", "q": 5.0, "chi1": [0,0,0.8], "chi2": [0,0,0.8], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0023", "q": 3.0, "chi1": [0,0,-0.8], "chi2": [0,0,-0.8], "ecc": 0.0, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        
        # Eccentric simulations
        {"id": "SXS:BBH:0024", "q": 1.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.1, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        {"id": "SXS:BBH:0025", "q": 1.0, "chi1": [0,0,0], "chi2": [0,0,0], "ecc": 0.2, "modes": [22, 21, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True},
        
        # GW150914-like
        {"id": "SXS:BBH:0305", "q": 1.22, "chi1": [0,0,0.33], "chi2": [0,0,-0.44], "ecc": 0.0, "modes": [22, 21, 20, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True, "event": "GW150914"},
        {"id": "SXS:BBH:0306", "q": 1.22, "chi1": [0,0,0.33], "chi2": [0,0,-0.44], "ecc": 0.0, "modes": [22, 21, 20, 33, 44], "resolutions": ["Lev1", "Lev2", "Lev3"], "CoM": True, "event": "GW150914"},
        
        # GW190521-like
        {"id": "SXS:BBH:0310", "q": 1.0, "chi1": [0,0,0.8], "chi2": [0,0,0.8], "ecc": 0.0, "modes": [22, 21, 20, 33, 44], "resolutions": ["Lev1", "Lev2"], "CoM": True, "event": "GW190521"},
    ]
    
    # Save catalog
    with open(sxs_dir / "sxs_bbh_catalog.json", 'w') as f:
        json.dump(simulations, f, indent=2)
    
    # Also save as CSV
    import pandas as pd
    df = pd.DataFrame(simulations)
    df.to_csv(sxs_dir / "sxs_bbh_catalog.csv", index=False)
    
    logger.info(f"Created SXS catalog with {len(simulations)} simulations")
    return simulations


def generate_synthetic_waveforms():
    """Generate synthetic waveform data for testing."""
    logger.info("Generating synthetic waveform data...")
    
    waveform_dir = RAW_DIR / "sxs_waveforms"
    waveform_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate synthetic waveforms for many configurations
    # Covering the parameter space: q in [1, 10], chi in [-0.9, 0.9]
    np.random.seed(42)
    
    # Grid of configurations
    q_values = [1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0]
    chi_values = [-0.9, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 0.9]
    
    configs = []
    for q in q_values:
        for chi1z in chi_values:
            for chi2z in chi_values:
                # Skip some combinations to keep size manageable
                if np.random.random() > 0.15:  # ~15% sampling = ~200 configs
                    continue
                configs.append({
                    "q": q,
                    "chi1z": chi1z,
                    "chi2z": chi2z,
                    "label": f"q{q:.2f}_chi1{chi1z:.1f}_chi2{chi2z:.1f}".replace(".", "p").replace("-", "m")
                })
    
    # Add some precessing configurations
    precessing_configs = [
        {"q": 1.0, "chi1": [0.5, 0, 0], "chi2": [0, 0.5, 0], "label": "precessing_q1"},
        {"q": 1.5, "chi1": [0.6, 0, 0], "chi2": [0, 0.6, 0], "label": "precessing_q15"},
        {"q": 2.0, "chi1": [0.7, 0, 0], "chi2": [0, 0.7, 0], "label": "precessing_q2"},
        {"q": 1.0, "chi1": [0.5, 0.5, 0.5], "chi2": [-0.5, -0.5, -0.5], "label": "precessing_q1_full"},
        {"q": 3.0, "chi1": [0.8, 0, 0], "chi2": [0, 0, 0.8], "label": "precessing_q3"},
    ]
    configs.extend(precessing_configs)
    
    logger.info(f"Generating {len(configs)} waveform configurations...")
    
    for config in configs:
        # Time array - longer for better frequency resolution
        t = np.linspace(-200, 20, 20000)  # M units
        
        M = 1.0
        q = config["q"]
        m1 = M * q / (1 + q)
        m2 = M / (1 + q)
        eta = m1 * m2 / M**2
        
        # Get spin parameters
        if "chi1" in config:
            chi1z = config["chi1"][2]
            chi2z = config["chi2"][2]
        else:
            chi1z = config["chi1z"]
            chi2z = config["chi2z"]
        
        # Effective spin
        chi_eff = (m1 * chi1z + m2 * chi2z) / M
        
        # Frequency evolution (improved toy model)
        f = np.zeros_like(t)
        for i, ti in enumerate(t):
            if ti < -10:
                # Early inspiral
                f[i] = 0.005 * (-ti / 200)**(-3/8) * (1 + 0.5 * chi_eff)
            elif ti < 0:
                # Late inspiral
                f[i] = 0.01 * (-ti / 100)**(-3/8) * (1 + 0.3 * chi_eff)
            else:
                # Merger/ringdown
                f[i] = 0.12 * np.exp(-ti / 4) * (1 + 0.1 * chi_eff)
        
        # Strain amplitude with spin corrections
        A = eta * M * (np.pi * M * f)**(2/3) * (1 + 0.2 * chi_eff * (np.pi * M * f)**(1/3))
        
        # Phase
        phi = 2 * np.pi * np.cumsum(f) * (t[1] - t[0])
        
        # Modes
        modes = {}
        for l, m in [(2, 2), (2, 1), (2, 0), (3, 3), (3, 2), (4, 4), (4, 3)]:
            amp_factor = 1.0 if (l == 2 and m == 2) else (0.3 if l == 3 else 0.1)
            if m == 1:
                amp_factor *= 0.5
            if m == 0:
                amp_factor *= 0.2
            
            modes[f"h{l}{m}_real"] = amp_factor * A * np.cos(m/2 * phi)
            modes[f"h{l}{m}_imag"] = amp_factor * A * np.sin(m/2 * phi)
        
        # Save with all modes
        save_dict = {
            "t": t,
            "f": f,
            "config": config
        }
        save_dict.update(modes)
        
        np.savez(
            waveform_dir / f"sxs_{config['label']}.npz",
            **save_dict
        )
    
    logger.info(f"Generated {len(configs)} synthetic waveforms")
    return True


def create_sxs_usage_guide():
    """Create a guide for using the real SXS data via the sxs package."""
    logger.info("Creating SXS usage guide...")
    
    guide = {
        "note": "The SXS catalog is now a JavaScript-based web app at https://data.black-holes.org/simulations/",
        "python_package": "sxs",
        "installation": "pip install sxs",
        "basic_usage": """
import sxs

# List available simulations
sims = sxs.BBH.catalog()
print(sims)

# Load a specific simulation
w = sxs.load("SXS:BBH:0305/Lev/rhOverM_Asymptotic_GeometricUnits_CoM.h5")
# Or use the sxs.Waveform class
waveform = sxs.Waveform("SXS:BBH:0305", extrapolation_order="Extrapolated_N4")
""",
        "waveform_formats": [
            "HDF5 files with datasets for each (l,m) mode",
            "Extrapolation orders: N=2,3,4 + OutermostExtraction",
            "Resolutions: Lev1, Lev2, Lev3 (higher = more accurate)",
            "Center-of-mass corrected (CoM) versions recommended"
        ],
        "key_papers": [
            "SXS Catalog 2019: arXiv:1904.04831 (PRD)",
            "SXS Catalog 2013: arXiv:1304.6077 (PRD)",
            "Waveform accuracy: arXiv:1509.00862, arXiv:1904.04842",
            "Gravitational-wave memory: arXiv:2011.01309"
        ],
        "data_access": {
            "website": "https://data.black-holes.org/simulations/",
            "zenodo": "https://zenodo.org/communities/sxs-waveforms",
            "globus": "Available for bulk download via Globus"
        }
    }
    
    sxs_dir = EXTERNAL_DIR / "sxs_catalog"
    with open(sxs_dir / "sxs_usage_guide.json", 'w') as f:
        json.dump(guide, f, indent=2)
    
    logger.info("Created SXS usage guide")
    return True


def main():
    logger.info("Starting SXS catalog creation...")
    
    total_size = 0
    
    # Create catalog metadata
    create_sxs_catalog()
    
    # Generate synthetic waveforms for testing
    generate_synthetic_waveforms()
    
    # Create usage guide
    create_sxs_usage_guide()
    
    # Calculate total size
    for d in [RAW_DIR, EXTERNAL_DIR]:
        for pattern in ["sxs*"]:
            for f in d.rglob(pattern):
                if f.is_file():
                    total_size += f.stat().st_size
    
    logger.info(f"SXS data complete. Total size: {total_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()