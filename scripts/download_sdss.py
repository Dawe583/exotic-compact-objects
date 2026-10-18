#!/usr/bin/env python3
"""
Download SDSS DR17/DR18 quasar and black hole catalogs via astroquery.
"""
import os
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
BASE_DIR = Path(__file__).parent.parent
EXTERNAL_DIR = BASE_DIR / "data" / "external"
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

try:
    from astroquery.sdss import SDSS
    from astroquery.vizier import Vizier
    import pandas as pd
    import numpy as np
except ImportError as e:
    logger.error(f"Missing dependencies: {e}")
    logger.error("Install with: pip install astroquery pandas numpy --break-system-packages")
    exit(1)


def configure_sdss():
    """Configure SDSS query settings."""
    SDSS.ROW_LIMIT = -1
    logger.info("Configured SDSS query")


def query_sdss_dr17_quasars():
    """Query SDSS DR17 quasar catalog (DR17Q)."""
    # DR17Q quasar catalog
    query = """
    SELECT TOP 500000
        objID, ra, dec, z, z_err, zWarning,
        psfMag_u, psfMag_g, psfMag_r, psfMag_i, psfMag_z,
        psfMagErr_u, psfMagErr_g, psfMagErr_r, psfMagErr_i, psfMagErr_z,
        modelMag_u, modelMag_g, modelMag_r, modelMag_i, modelMag_z,
        extinction_u, extinction_g, extinction_r, extinction_i, extinction_z,
        specObjID, plate, mjd, fiberID,
        sn_median_u, sn_median_g, sn_median_r, sn_median_i, sn_median_z,
        ebv, thing_id, thing_id_spec
    FROM SpecObjAll
    JOIN PhotoObjAll ON SpecObjAll.bestObjID = PhotoObjAll.objID
    WHERE class = 'QSO' AND z > 0 AND zWarning = 0
    ORDER BY z
    """
    
    logger.info("Querying SDSS DR17 quasar catalog...")
    try:
        result = SDSS.query_sql(query)
        if result is not None:
            df = result.to_pandas()
            logger.info(f"Retrieved {len(df)} DR17 quasars")
            return df
        else:
            logger.warning("No DR17 quasar results")
            return None
    except Exception as e:
        logger.error(f"DR17 quasar query failed: {e}")
        return None


def query_sdss_dr18_quasars():
    """Query SDSS DR18 quasar catalog via Vizier (DR18Q)."""
    # Try Vizier for DR18Q
    logger.info("Querying SDSS DR18 quasar catalog via Vizier...")
    try:
        Vizier.ROW_LIMIT = -1
        catalogs = Vizier.get_catalogs("V/154/sdss18q")
        if catalogs:
            df = catalogs[0].to_pandas()
            logger.info(f"Retrieved {len(df)} DR18 quasars")
            return df
        else:
            logger.warning("No DR18 quasar catalog found in Vizier")
            return None
    except Exception as e:
        logger.error(f"DR18 quasar query failed: {e}")
        return None


def query_sdss_bh_masses():
    """Query SDSS black hole mass estimates (from various catalogs)."""
    # Try to get BH mass catalog from Vizier (e.g., Shen et al. 2011, Rakshit et al. 2020)
    logger.info("Querying BH mass catalogs from Vizier...")
    try:
        Vizier.ROW_LIMIT = -1
        # Shen et al. 2011 BH mass catalog
        catalogs = Vizier.get_catalogs("J/ApJS/194/45/table1")
        if catalogs:
            df = catalogs[0].to_pandas()
            logger.info(f"Retrieved {len(df)} BH mass estimates (Shen+2011)")
            return df
        else:
            logger.warning("No Shen+2011 BH mass catalog found")
            return None
    except Exception as e:
        logger.error(f"BH mass query failed: {e}")
        return None


def query_sdss_xray_agn():
    """Query SDSS X-ray AGN cross-match catalogs."""
    logger.info("Querying SDSS-X-ray AGN cross-matches...")
    try:
        Vizier.ROW_LIMIT = -1
        # XMM-SDSS or Chandra-SDSS cross-matches
        catalogs = Vizier.get_catalogs("J/ApJS/221/12/table1")
        if catalogs:
            df = catalogs[0].to_pandas()
            logger.info(f"Retrieved {len(df)} X-ray AGN")
            return df
        else:
            logger.warning("No X-ray AGN catalog found")
            return None
    except Exception as e:
        logger.error(f"X-ray AGN query failed: {e}")
        return None


def save_data(df, name):
    """Save DataFrame to CSV and Parquet."""
    if df is None or len(df) == 0:
        logger.warning(f"No data to save for {name}")
        return 0
    
    csv_path = EXTERNAL_DIR / f"sdss_{name}.csv"
    parquet_path = EXTERNAL_DIR / f"sdss_{name}.parquet"
    
    df.to_csv(csv_path, index=False)
    df.to_parquet(parquet_path, index=False)
    
    size = csv_path.stat().st_size + parquet_path.stat().st_size
    logger.info(f"Saved {len(df)} rows to {csv_path} and {parquet_path} ({size/1e6:.1f} MB)")
    return size


def main():
    logger.info("Starting SDSS DR17/DR18 download...")
    
    configure_sdss()
    
    total_size = 0
    
    # DR17 Quasars
    df_dr17 = query_sdss_dr17_quasars()
    total_size += save_data(df_dr17, "dr17_quasars")
    
    # DR18 Quasars
    df_dr18 = query_sdss_dr18_quasars()
    total_size += save_data(df_dr18, "dr18_quasars")
    
    # BH Masses
    df_bh = query_sdss_bh_masses()
    total_size += save_data(df_bh, "bh_masses_shen2011")
    
    # X-ray AGN
    df_xray = query_sdss_xray_agn()
    total_size += save_data(df_xray, "xray_agn")
    
    logger.info(f"SDSS download complete. Total size: {total_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()