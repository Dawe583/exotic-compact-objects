#!/usr/bin/env python3
"""
Download Gaia DR3 data via astroquery.
Focus on black hole candidate systems (astrometric binaries, etc.).
"""
import os
import logging
from pathlib import Path
from tqdm import tqdm

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
BASE_DIR = Path(__file__).parent.parent
EXTERNAL_DIR = BASE_DIR / "data" / "external"
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

try:
    from astroquery.gaia import Gaia
    import pandas as pd
except ImportError as e:
    logger.error(f"Missing dependencies: {e}")
    logger.error("Install with: pip install astroquery pandas --break-system-packages")
    exit(1)


def configure_gaia():
    """Configure Gaia query settings."""
    Gaia.MAIN_GAIA_TABLE = "gaiadr3.gaia_source"
    Gaia.ROW_LIMIT = -1  # No limit
    logger.info("Configured Gaia DR3 query")


def query_bh_candidates():
    """Query Gaia DR3 for black hole candidates."""
    # Query for astrometric binaries with massive unseen companions
    # Using criteria from Gaia BH candidate papers (e.g., Gaia BH1, BH2, BH3)
    query = """
    SELECT TOP 20000
        source_id, ra, dec, parallax, parallax_error,
        pmra, pmra_error, pmdec, pmdec_error,
        ruwe, phot_g_mean_mag, bp_rp,
        astrometric_excess_noise, astrometric_excess_noise_sig,
        non_single_star, teff_gspphot, logg_gspphot, mh_gspphot,
        distance_gspphot, azero_gspphot
    FROM gaiadr3.gaia_source
    WHERE 
        phot_g_mean_mag < 16
        AND parallax > 0
        AND parallax_error / parallax < 0.2
        AND ruwe > 1.4
        AND astrometric_excess_noise > 1
        AND non_single_star IS NOT NULL
    ORDER BY ruwe DESC
    """
    
    logger.info("Executing Gaia DR3 query for BH candidates...")
    try:
        job = Gaia.launch_job_async(query, dump_to_file=False)
        results = job.get_results()
        logger.info(f"Retrieved {len(results)} candidate rows")
        return results.to_pandas()
    except Exception as e:
        logger.error(f"Gaia query failed: {e}")
        return None


def query_known_bh_systems():
    """Query for known Gaia BH systems by source_id."""
    known_sources = [
        "4373465352415301632",  # Gaia BH1
        "6751965127918764160",  # Gaia BH2
        "4038610822113058816",  # Gaia BH3
    ]
    
    source_list = ",".join(known_sources)
    query = f"""
    SELECT *
    FROM gaiadr3.gaia_source
    WHERE source_id IN ({source_list})
    """
    
    logger.info("Querying known Gaia BH systems...")
    try:
        job = Gaia.launch_job_async(query, dump_to_file=False)
        results = job.get_results()
        logger.info(f"Retrieved {len(results)} known BH systems")
        return results.to_pandas()
    except Exception as e:
        logger.error(f"Known BH query failed: {e}")
        return None


def query_wide_binaries():
    """Query for wide binary candidates with potential BH companions."""
    query = """
    SELECT TOP 100000
        source_id, ra, dec, parallax, parallax_error,
        pmra, pmra_error, pmdec, pmdec_error,
        ruwe, phot_g_mean_mag, bp_rp,
        radial_velocity, radial_velocity_error,
        teff_gspphot, logg_gspphot, mh_gspphot,
        distance_gspphot, azero_gspphot,
        classprob_dsc_combmod_quasar,
        classprob_dsc_combmod_galaxy,
        classprob_dsc_combmod_star
    FROM gaiadr3.gaia_source
    WHERE 
        parallax > 0.5
        AND parallax_error / parallax < 0.1
        AND ruwe > 1.2
        AND phot_g_mean_mag < 15
        AND radial_velocity IS NOT NULL
    ORDER BY ruwe DESC
    """
    
    logger.info("Querying wide binary candidates...")
    try:
        job = Gaia.launch_job_async(query, dump_to_file=False)
        results = job.get_results()
        logger.info(f"Retrieved {len(results)} wide binary candidates")
        return results.to_pandas()
    except Exception as e:
        logger.error(f"Wide binary query failed: {e}")
        return None


def save_data(df, name):
    """Save DataFrame to CSV and optionally Parquet."""
    if df is None or len(df) == 0:
        logger.warning(f"No data to save for {name}")
        return 0
    
    csv_path = EXTERNAL_DIR / f"gaia_dr3_{name}.csv"
    df.to_csv(csv_path, index=False)
    
    # Try parquet, fallback to CSV only
    parquet_path = EXTERNAL_DIR / f"gaia_dr3_{name}.parquet"
    try:
        df.to_parquet(parquet_path, index=False)
    except Exception as e:
        logger.warning(f"Parquet save failed, using CSV only: {e}")
        parquet_path = None
    
    size = csv_path.stat().st_size
    if parquet_path and parquet_path.exists():
        size += parquet_path.stat().st_size
    logger.info(f"Saved {len(df)} rows to {csv_path} ({size/1e6:.1f} MB)")
    return size


def main():
    logger.info("Starting Gaia DR3 download...")
    
    configure_gaia()
    
    total_size = 0
    
    # Query 1: BH candidates
    df_bh = query_bh_candidates()
    total_size += save_data(df_bh, "bh_candidates")
    
    # Query 2: Known BH systems
    df_known = query_known_bh_systems()
    total_size += save_data(df_known, "known_bh_systems")
    
    # Query 3: Wide binaries
    df_wide = query_wide_binaries()
    total_size += save_data(df_wide, "wide_binaries")
    
    logger.info(f"Gaia DR3 download complete. Total size: {total_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()