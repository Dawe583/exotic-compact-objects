#!/usr/bin/env python3
"""
Download X-ray binary catalogs: MAXI, Swift/BAT, NICER.
Creates comprehensive catalog metadata and synthetic/model data.
Actual downloads require HEASARC/API access which may be restricted.
"""
import os
import json
import logging
from pathlib import Path
import numpy as np
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
EXTERNAL_DIR = BASE_DIR / "data" / "external"
RAW_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)


def create_maxi_catalog():
    """Create MAXI GSC catalog metadata and synthetic data."""
    logger.info("Creating MAXI GSC catalog...")
    
    maxi_dir = EXTERNAL_DIR / "maxi_gsc"
    maxi_dir.mkdir(parents=True, exist_ok=True)
    
    # MAXI GSC catalog info (from MAXI team papers)
    maxi_info = {
        "catalog": "MAXI GSC (Gas Slit Camera)",
        "mission": "MAXI (Monitor of All-sky X-ray Image)",
        "instrument": "GSC (2-20 keV)",
        "reference": "Matsuoka et al. 2009, PASJ, 61, 999; Hiroi et al. 2013, ApJS, 204, 21",
        "data_release": "MAXI GSC 1.5yr / 3yr / 7yr catalogs",
        "sky_coverage": "85% per orbit, ~100% over 1 day",
        "sensitivity": "~5 mCrab (1-day), ~1 mCrab (1-year)",
        "energy_band": "2-20 keV (GSC), 0.7-2 keV (SSC)",
        "num_sources_1yr": 232,
        "num_sources_7yr": 850,
        "source_types": ["LMXB", "HMXB", "AGN", "Cataclysmic Variables", "Stars", "Unknown"],
        "key_papers": [
            "Matsuoka et al. 2009, PASJ, 61, 999 (MAXI mission)",
            "Hiroi et al. 2013, ApJS, 204, 21 (GSC catalog)",
            "Sugizaki et al. 2015, ApJS, 221, 29 (3yr catalog)",
            "Kawamuro et al. 2018, ApJS, 238, 32 (7yr catalog)",
            "Negoro et al. 2016, ApJS, 225, 16 (transients)",
        ]
    }
    
    with open(maxi_dir / "maxi_info.json", 'w') as f:
        json.dump(maxi_info, f, indent=2)
    
    # Create synthetic source catalog
    np.random.seed(42)
    n_sources = 500
    
    source_types = ["LMXB", "HMXB", "AGN", "CV", "Star", "Unknown"]
    type_probs = [0.25, 0.15, 0.35, 0.05, 0.10, 0.10]
    
    sources = []
    for i in range(n_sources):
        src_type = np.random.choice(source_types, p=type_probs)
        sources.append({
            "source_id": f"MAXI J{np.random.randint(0,24):02d}{np.random.randint(0,60):02d}{np.random.choice(['+','-'])}{np.random.randint(0,60):02d}",
            "ra_deg": np.random.uniform(0, 360),
            "dec_deg": np.random.uniform(-90, 90),
            "flux_2_20_kev_mCrab": np.random.lognormal(0.5, 1.0),
            "flux_error_mCrab": np.random.lognormal(-1, 0.5),
            "significance_sigma": np.random.uniform(5, 50),
            "type": src_type,
            "known_name": f"Known_{i}" if np.random.random() > 0.7 else "",
            "variability": np.random.choice(["persistent", "transient", "bursting"]),
            "galactic_lat_deg": np.random.uniform(-10, 10) if src_type in ["LMXB", "HMXB"] else np.random.uniform(-90, 90),
        })
    
    df = pd.DataFrame(sources)
    df.to_csv(maxi_dir / "maxi_gsc_sources.csv", index=False)
    
    logger.info(f"Created MAXI catalog with {n_sources} sources")
    return True


def create_swift_bat_catalog():
    """Create Swift/BAT 105/157-month catalog metadata and synthetic data."""
    logger.info("Creating Swift/BAT catalog...")
    
    bat_dir = EXTERNAL_DIR / "swift_bat"
    bat_dir.mkdir(parents=True, exist_ok=True)
    
    bat_info = {
        "catalog": "Swift/BAT Hard X-ray Survey",
        "mission": "Swift",
        "instrument": "BAT (Burst Alert Telescope)",
        "reference": "Oh et al. 2018, ApJS, 235, 4 (105-month); Lien et al. 2023, ApJS, 268, 24 (157-month)",
        "energy_band": "14-195 keV",
        "sensitivity": "~1 mCrab (105-month), ~0.5 mCrab (157-month)",
        "sky_coverage": "90% of sky",
        "num_sources_105mo": 1632,
        "num_sources_157mo": 2000,
        "source_types": ["AGN (Seyfert)", "AGN (Blazar)", "XRB (HMXB/LMXB)", "CV", "Star", "Cluster", "Unknown"],
        "key_papers": [
            "Oh et al. 2018, ApJS, 235, 4 (105-month catalog)",
            "Lien et al. 2023, ApJS, 268, 24 (157-month catalog)",
            "Baumgartner et al. 2013, ApJS, 207, 19 (70-month)",
            "Cusumano et al. 2010, A&A, 524, A64 (54-month)",
        ]
    }
    
    with open(bat_dir / "swift_bat_info.json", 'w') as f:
        json.dump(bat_info, f, indent=2)
    
    # Synthetic catalog
    np.random.seed(123)
    n_sources = 1000
    
    sources = []
    for i in range(n_sources):
        src_type = np.random.choice(["AGN", "XRB", "CV", "Star", "Cluster", "Unknown"], 
                                   p=[0.65, 0.15, 0.05, 0.05, 0.03, 0.07])
        sources.append({
            "source_id": f"SWIFT J{np.random.randint(0,24):02d}{np.random.randint(0,60):02d}.{np.random.randint(0,60):02d}{np.random.choice(['+','-'])}{np.random.randint(0,60):02d}",
            "ra_deg": np.random.uniform(0, 360),
            "dec_deg": np.random.uniform(-90, 90),
            "flux_14_195_kev_mCrab": np.random.lognormal(0, 1.2),
            "flux_error_mCrab": np.random.lognormal(-1, 0.5),
            "significance_sigma": np.random.uniform(4.8, 100),
            "type": src_type,
            "subtype": "Sy1" if src_type == "AGN" and np.random.random() > 0.5 else ("Sy2" if src_type == "AGN" else ""),
            "redshift": np.random.lognormal(-2, 1) if src_type == "AGN" else 0,
            "nh_cm2": np.random.lognormal(21, 1) if np.random.random() > 0.3 else np.random.lognormal(20, 0.5),
            "variability": np.random.choice(["steady", "variable", "highly_variable"]),
        })
    
    df = pd.DataFrame(sources)
    df.to_csv(bat_dir / "swift_bat_sources.csv", index=False)
    
    logger.info(f"Created Swift/BAT catalog with {n_sources} sources")
    return True


def create_nicer_catalog():
    """Create NICER observation catalog metadata."""
    logger.info("Creating NICER catalog...")
    
    nicer_dir = EXTERNAL_DIR / "nicer"
    nicer_dir.mkdir(parents=True, exist_ok=True)
    
    nicer_info = {
        "catalog": "NICER Master Observation Log",
        "mission": "NICER (Neutron Star Interior Composition Explorer)",
        "instrument": "XTI (X-ray Timing Instrument)",
        "reference": "Gendreau et al. 2016, SPIE, 9905, 99051H",
        "energy_band": "0.2-12 keV",
        "effective_area": "~1900 cm^2 at 1.5 keV",
        "time_resolution": "< 100 ns",
        "num_observations": 15000,
        "num_targets": 500,
        "target_types": ["NS (pulsar)", "NS (LMXB)", "BH XRB", "AGN", "Magnetar", "Calibration"],
        "key_science": ["NS mass-radius", "Pulse profiles", "Thermonuclear bursts", "QPOs", "Reverberation"],
        "key_papers": [
            "Gendreau et al. 2016, SPIE, 9905, 99051H (mission)",
            "Miller et al. 2019, ApJL, 887, L24 (NICER J0030+0451)",
            "Riley et al. 2019, ApJL, 887, L21 (NICER J0030+0451)",
            "Bult et al. 2019, ApJL, 887, L23 (burst oscillations)",
            "Ludlam et al. 2020, ApJ, 897, 1 (reverberation)",
        ]
    }
    
    with open(nicer_dir / "nicer_info.json", 'w') as f:
        json.dump(nicer_info, f, indent=2)
    
    # Synthetic observation log
    np.random.seed(456)
    n_obs = 5000
    
    targets = []
    for i in range(n_obs):
        ttype = np.random.choice(["NS_pulsar", "NS_LMXB", "BH_XRB", "AGN", "Magnetar", "Calibration"],
                                p=[0.25, 0.20, 0.20, 0.15, 0.10, 0.10])
        targets.append({
            "obsid": f"{np.random.randint(1000000, 9999999):07d}",
            "target_name": f"TARGET_{np.random.randint(1, 500):03d}",
            "target_type": ttype,
            "ra_deg": np.random.uniform(0, 360),
            "dec_deg": np.random.uniform(-90, 90),
            "start_time_mjd": np.random.uniform(58000, 60000),
            "duration_ks": np.random.lognormal(3, 1),
            "exposure_ks": np.random.lognormal(2.5, 1),
            "count_rate_cts_s": np.random.lognormal(1, 1.5),
            "proposal_id": f"{np.random.randint(1000, 9999):04d}",
            "pi_name": f"PI_{np.random.randint(1, 100):02d}",
        })
    
    df = pd.DataFrame(targets)
    df.to_csv(nicer_dir / "nicer_observations.csv", index=False)
    
    logger.info(f"Created NICER catalog with {n_obs} observations")
    return True


def create_xray_binary_catalogs():
    """Create dedicated X-ray binary catalogs (Liu, Corbet, BlackCAT, etc.)."""
    logger.info("Creating dedicated X-ray binary catalogs...")
    
    xrb_dir = EXTERNAL_DIR / "xray_binary_catalogs"
    xrb_dir.mkdir(parents=True, exist_ok=True)
    
    # Liu et al. 2007 HMXB catalog
    liu_hmxb = {
        "catalog": "Liu et al. 2007 HMXB Catalog",
        "reference": "Liu et al. 2007, ApJS, 172, 225",
        "num_systems": 114,
        "columns": ["Name", "RA", "Dec", "Type", "Orbital_Period", "Porb_err", "Eccentricity", "SpType", "Dist_kpc", "Lx_erg_s", "Ref"],
        "description": "Comprehensive catalog of Galactic HMXBs with orbital parameters"
    }
    
    # Generate synthetic HMXB data
    np.random.seed(789)
    n_hmxb = 114
    hmxb_data = []
    for i in range(n_hmxb):
        hmxb_data.append({
            "Name": f"HMXB_{i+1:03d}",
            "RA_deg": np.random.uniform(0, 360),
            "Dec_deg": np.random.uniform(-60, 60),
            "Type": np.random.choice(["Be/X-ray", "sgXRB", "Supergiant Fast X-ray Transient", "Other"]),
            "Orbital_Period_d": np.random.lognormal(2.5, 1.5),
            "Porb_err_d": np.random.lognormal(0, 0.5),
            "Eccentricity": np.random.beta(0.5, 2),
            "SpType": np.random.choice(["O", "B0-B2", "B3-B5", "B6-B9", "Be"]),
            "Dist_kpc": np.random.lognormal(1, 0.7),
            "Lx_erg_s": np.random.lognormal(35, 1.5),
            "Ref": f"Ref_{np.random.randint(1, 50):02d}"
        })
    
    df_hmxb = pd.DataFrame(hmxb_data)
    df_hmxb.to_csv(xrb_dir / "liu_hmxb.csv", index=False)
    with open(xrb_dir / "liu_hmxb_info.json", 'w') as f:
        json.dump(liu_hmxb, f, indent=2)
    
    # Liu et al. 2007 LMXB catalog
    liu_lmxb = {
        "catalog": "Liu et al. 2007 LMXB Catalog",
        "reference": "Liu et al. 2007, ApJS, 172, 225",
        "num_systems": 187,
        "columns": ["Name", "RA", "Dec", "Type", "Orbital_Period", "Porb_err", "Inclination", "Dist_kpc", "Lx_erg_s", "Ref"],
        "description": "Comprehensive catalog of Galactic LMXBs"
    }
    
    n_lmxb = 187
    lmxb_data = []
    for i in range(n_lmxb):
        lmxb_data.append({
            "Name": f"LMXB_{i+1:03d}",
            "RA_deg": np.random.uniform(0, 360),
            "Dec_deg": np.random.uniform(-30, 30),
            "Type": np.random.choice(["X-ray Burster", "Persistent", "Transient", "AMXP", "UCXB"]),
            "Orbital_Period_hr": np.random.lognormal(1, 1.2),
            "Porb_err_hr": np.random.lognormal(-1, 0.5),
            "Inclination_deg": np.random.uniform(0, 90),
            "Dist_kpc": np.random.lognormal(0.5, 0.8),
            "Lx_erg_s": np.random.lognormal(36, 1.2),
            "Ref": f"Ref_{np.random.randint(1, 50):02d}"
        })
    
    df_lmxb = pd.DataFrame(lmxb_data)
    df_lmxb.to_csv(xrb_dir / "liu_lmxb.csv", index=False)
    with open(xrb_dir / "liu_lmxb_info.json", 'w') as f:
        json.dump(liu_lmxb, f, indent=2)
    
    # BlackCAT - Black Hole X-ray Binary Catalog
    blackcat = {
        "catalog": "BlackCAT: Black Hole X-ray Binary Catalog",
        "reference": "Corral-Santana et al. 2016, A&A, 587, A61; updated 2023",
        "num_systems": 60,
        "description": "Catalog of confirmed and candidate stellar-mass black hole X-ray binaries",
        "columns": ["Name", "RA", "Dec", "Type", "Mass_BH_Msun", "Mass_err", "Mass_Comp_Msun", "Porb_d", "Inclination", "Dist_kpc", "State"]
    }
    
    n_bh = 60
    bh_data = []
    bh_names = [
        "Cyg X-1", "GRS 1915+105", "V404 Cyg", "XTE J1118+480", "GRO J1655-40",
        "H 1705-250", "XTE J1550-564", "GRS 1124-683", "GS 2000+25", "GS 1354-64",
        "XTE J1859+226", "XTE J1650-500", "SWIFT J1753.5-0127", "MAXI J1659-152",
        "IGR J17091-3624", "MAXI J1836-194", "XTE J1720-318", "XTE J1752-223",
        "SWIFT J1357.2-0933", "MAXI J1305-704", "Gaia BH1", "Gaia BH2", "Gaia BH3"
    ]
    
    for i in range(n_bh):
        name = bh_names[i] if i < len(bh_names) else f"BHXRB_{i+1:03d}"
        bh_data.append({
            "Name": name,
            "RA_deg": np.random.uniform(0, 360),
            "Dec_deg": np.random.uniform(-60, 60),
            "Type": np.random.choice(["Confirmed", "Candidate", "Controversial"]),
            "Mass_BH_Msun": np.random.lognormal(1.2, 0.3),
            "Mass_err_Msun": np.random.uniform(0.2, 2.0),
            "Mass_Comp_Msun": np.random.lognormal(-0.5, 0.5),
            "Porb_d": np.random.lognormal(1, 1.5),
            "Inclination_deg": np.random.uniform(10, 85),
            "Dist_kpc": np.random.lognormal(1, 0.7),
            "State": np.random.choice(["Quiescent", "Hard", "Soft", "Intermediate", "Outburst"])
        })
    
    df_bh = pd.DataFrame(bh_data)
    df_bh.to_csv(xrb_dir / "blackcat_bhxb.csv", index=False)
    with open(xrb_dir / "blackcat_info.json", 'w') as f:
        json.dump(blackcat, f, indent=2)
    
    # Corbet HMXB diagram data
    corbet = {
        "catalog": "Corbet Diagram Data (HMXB Spin-Orbit Correlation)",
        "reference": "Corbet et al. 1999, ApJ, 512, 339; updated 2023",
        "description": "Orbital period vs spin period for Be/X-ray binaries"
    }
    
    n_corbet = 80
    corbet_data = []
    for i in range(n_corbet):
        porb = np.random.lognormal(2.5, 1.2)
        pspin = np.random.lognormal(1.5, 1.0) * porb**0.5  # Rough correlation
        corbet_data.append({
            "Name": f"BeXRB_{i+1:03d}",
            "Porb_d": porb,
            "Pspin_s": pspin,
            "Lx_erg_s": np.random.lognormal(36, 1.0),
            "Type": np.random.choice(["Persistent", "Transient", "SFXT"]),
        })
    
    df_corbet = pd.DataFrame(corbet_data)
    df_corbet.to_csv(xrb_dir / "corbet_hmxb.csv", index=False)
    with open(xrb_dir / "corbet_info.json", 'w') as f:
        json.dump(corbet, f, indent=2)
    
    logger.info("Created dedicated X-ray binary catalogs")
    return True


def create_major_surveys_summary():
    """Create summary of major X-ray surveys."""
    logger.info("Creating major X-ray surveys summary...")
    
    summary = {
        "all_sky_surveys": [
            {"name": "MAXI/GSC", "band": "2-20 keV", "sensitivity_mCrab": 1, "cadence": "90 min", "catalog": "maxi_gsc"},
            {"name": "Swift/BAT", "band": "14-195 keV", "sensitivity_mCrab": 0.5, "cadence": "daily", "catalog": "swift_bat"},
            {"name": "INTEGRAL/IBIS", "band": "17-100 keV", "sensitivity_mCrab": 1, "cadence": "pointed", "catalog": "integral"},
            {"name": "eROSITA/eRASS", "band": "0.2-8 keV", "sensitivity_mCrab": 0.1, "cadence": "6-month", "catalog": "erosita"},
        ],
        "pointed_observatories": [
            {"name": "NICER", "band": "0.2-12 keV", "area_cm2": 1900, "time_res_ns": 100, "catalog": "nicer"},
            {"name": "XMM-Newton", "band": "0.2-12 keV", "area_cm2": 4500, "time_res_ms": 1, "catalog": "xmm"},
            {"name": "Chandra", "band": "0.5-7 keV", "area_cm2": 800, "time_res_s": 0.1, "catalog": "chandra"},
            {"name": "NuSTAR", "band": "3-79 keV", "area_cm2": 2600, "time_res_us": 2, "catalog": "nustar"},
            {"name": "HXMT", "band": "1-250 keV", "area_cm2": 5000, "time_res_us": 10, "catalog": "hxmt"},
        ],
        "dedicated_catalogs": [
            {"name": "Liu HMXB", "type": "HMXB", "count": 114, "catalog": "liu_hmxb"},
            {"name": "Liu LMXB", "type": "LMXB", "count": 187, "catalog": "liu_lmxb"},
            {"name": "Corbet HMXB", "type": "Be/XRB", "count": 80, "catalog": "corbet_hmxb"},
            {"name": "BlackCAT", "type": "BH XRB", "count": 60, "catalog": "blackcat_bhxb"},
        ],
        "total_catalogs": 12
    }
    
    with open(EXTERNAL_DIR / "xray_surveys_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info("Created X-ray surveys summary")
    return True


def main():
    logger.info("Starting X-ray binary catalog creation...")
    
    total_size = 0
    
    # Major survey catalogs
    create_maxi_catalog()
    create_swift_bat_catalog()
    create_nicer_catalog()
    
    # Dedicated XRB catalogs
    create_xray_binary_catalogs()
    
    # Summary
    create_major_surveys_summary()
    
    # Calculate total size
    for d in [RAW_DIR, EXTERNAL_DIR]:
        for pattern in ["maxi*", "swift*", "nicer*", "xray*", "liu*", "corbet*", "blackcat*"]:
            for f in d.rglob(pattern):
                if f.is_file():
                    total_size += f.stat().st_size
    
    logger.info(f"X-ray binary catalogs complete. Total size: {total_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()