#!/usr/bin/env python3
"""Download EHT (Event Horizon Telescope) REAL calibrated data for M87* (2017).

Public data release: https://github.com/eventhorizontelescope/2019-D01-01
(EHT Collaboration et al. 2019, ApJL, 875, L1-L6). No registration required.

Falls back to clearly-labeled model parameters only if the download fails.
"""

import json
import logging
from pathlib import Path

import requests

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
EXTERNAL_DIR = BASE_DIR / "data" / "external"
RAW_DIR = BASE_DIR / "data" / "raw"
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)
RAW_DIR.mkdir(parents=True, exist_ok=True)

REPO = "eventhorizontelescope/2019-D01-01"
API = f"https://api.github.com/repos/{REPO}/contents/csv"
RAW_BASE = f"https://raw.githubusercontent.com/{REPO}/master/csv"


def main():
    out_dir = EXTERNAL_DIR / "eht_m87"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Fetch the CSV file list from the public GitHub repo.
    try:
        r = requests.get(API, timeout=60)
        r.raise_for_status()
        files = [f["name"] for f in r.json() if f["name"].endswith(".csv")]
    except Exception as e:
        raise SystemExit(f"Failed to list EHT data files: {e}")

    logger.info("Found %d real EHT M87* CSV files", len(files))

    downloaded = 0
    for name in files:
        dest = out_dir / name
        try:
            rr = requests.get(f"{RAW_BASE}/{name}", timeout=120)
            rr.raise_for_status()
            dest.write_bytes(rr.content)
            downloaded += 1
            logger.info("Downloaded %s (%d bytes)", name, len(rr.content))
        except Exception as e:
            logger.error("Failed %s: %s", name, e)

    # Save a small metadata file with the real M87* parameters (from EHT papers).
    params = {
        "source": "M87*",
        "data_source": "EHT Collaboration et al. 2019, ApJL, 875, L1-L6 (REAL, public)",
        "distance_Mpc": 16.8,
        "mass_Msun": 6.5e9,
        "ring_diameter_uas": 42,
        "observation_date": "2017-04-05/06/10/11",
        "wavelength_mm": 1.3,
        "frequency_GHz": 230,
        "files_downloaded": downloaded,
        "total_files": len(files),
    }
    (out_dir / "m87_parameters.json").write_text(json.dumps(params, indent=2))
    logger.info("Downloaded %d/%d real EHT M87* files", downloaded, len(files))

    if downloaded == 0:
        raise SystemExit("No EHT files downloaded")


if __name__ == "__main__":
    main()
