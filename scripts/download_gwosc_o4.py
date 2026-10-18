#!/usr/bin/env python3
"""
Download LIGO/Virgo/KAGRA O4 strain data via GWOSC.
Downloads event metadata, strain HDF5 files for GWTC-3 and GWTC-4 events.
"""
import os
import json
import logging
import requests
from pathlib import Path
from tqdm import tqdm
import h5py

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directories
BASE_DIR = Path(__file__).parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
EXTERNAL_DIR = BASE_DIR / "data" / "external"
RAW_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

# GWOSC API endpoints
GWOSC_EVENT_API = "https://gwosc.org/eventapi/json/GWTC/"
GWOSC_STRAIN_API = "https://gwosc.org/api/v1/event/"


def fetch_event_catalog():
    """Fetch the full GWTC event catalog from GWOSC."""
    logger.info("Fetching GWOSC event catalog...")
    try:
        response = requests.get(GWOSC_EVENT_API, timeout=60)
        response.raise_for_status()
        data = response.json()
        events = data.get("events", {})
        logger.info(f"Found {len(events)} events in GWTC catalog")
        return events
    except Exception as e:
        logger.error(f"Failed to fetch event catalog: {e}")
        return {}


def filter_o4_events(events):
    """Filter for O4 events (GWTC-3 and GWTC-4)."""
    o4_events = {}
    for name, info in events.items():
        # O4 runs started in May 2023
        # GWTC-3 covers O3b, GWTC-4 covers O4a
        gps_time = info.get("GPS", 0)
        # GPS time for O4 start ~ 1367289618 (May 2023)
        if gps_time >= 1367289618:
            o4_events[name] = info
    logger.info(f"Filtered {len(o4_events)} O4 events")
    return o4_events


def download_strain_data(event_name, event_info, output_dir):
    """Download strain HDF5 for a specific event."""
    # Try to get strain data URLs from GWOSC
    strain_url = f"{GWOSC_STRAIN_API}{event_name}/json/"
    
    try:
        response = requests.get(strain_url, timeout=60)
        response.raise_for_status()
        strain_data = response.json()
        
        # Look for HDF5 strain files
        strain_files = strain_data.get("strain", [])
        downloaded = False
        
        for strain_file in strain_files:
            url = strain_file.get("url", "")
            if url.endswith(".hdf5") or url.endswith(".h5"):
                local_path = output_dir / f"{event_name}_strain.h5"
                if download_file(url, local_path):
                    logger.info(f"Downloaded strain for {event_name}")
                    downloaded = True
                    break
        
        if not downloaded:
            logger.warning(f"No strain HDF5 found for {event_name}")
        return downloaded
    except Exception as e:
        logger.error(f"Failed to get strain info for {event_name}: {e}")
        return False


def download_file(url, local_path, chunk_size=8192):
    """Download a file with progress bar."""
    try:
        response = requests.get(url, stream=True, timeout=120)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        with open(local_path, 'wb') as f:
            with tqdm(total=total_size, unit='B', unit_scale=True, 
                     desc=local_path.name, leave=False) as pbar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        return True
    except Exception as e:
        logger.error(f"Download failed for {url}: {e}")
        if local_path.exists():
            local_path.unlink()
        return False


def save_event_metadata(events, output_file):
    """Save event metadata to JSON and CSV."""
    import pandas as pd
    
    # Save JSON
    with open(output_file.with_suffix('.json'), 'w') as f:
        json.dump(events, f, indent=2)
    
    # Save CSV
    rows = []
    for name, info in events.items():
        row = {"event_name": name}
        row.update(info)
        rows.append(row)
    
    df = pd.DataFrame(rows)
    df.to_csv(output_file.with_suffix('.csv'), index=False)
    logger.info(f"Saved metadata for {len(events)} events to {output_file}")


def main():
    logger.info("Starting GWOSC O4 data download...")
    
    # Fetch catalog
    events = fetch_event_catalog()
    if not events:
        logger.error("No events fetched, exiting")
        return
    
    # Filter O4 events
    o4_events = filter_o4_events(events)
    
    # Save metadata
    save_event_metadata(o4_events, EXTERNAL_DIR / "gwosc_o4_events")
    
    # Download strain data for O4 events (limit to first 10 to save space/time)
    strain_dir = RAW_DIR / "gwosc_o4_strain"
    strain_dir.mkdir(parents=True, exist_ok=True)
    
    downloaded_count = 0
    for i, (name, info) in enumerate(o4_events.items()):
        if i >= 10:  # Limit downloads
            logger.info(f"Reached download limit (10 events), skipping {name}")
            break
        if download_strain_data(name, info, strain_dir):
            downloaded_count += 1
    
    logger.info(f"Downloaded strain data for {downloaded_count} events")
    
    # Calculate total size
    total_size = sum(f.stat().st_size for f in strain_dir.rglob("*") if f.is_file())
    logger.info(f"Total strain data size: {total_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()