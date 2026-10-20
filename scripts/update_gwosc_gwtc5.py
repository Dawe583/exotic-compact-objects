#!/usr/bin/env python3
"""Refresh the full GWOSC GWTC catalog snapshot (all catalogs, GWTC-1 .. GWTC-5).

Writes:
  data/external/gwosc_gwtc_all.json   raw API dump
  data/external/gwosc_gwtc_all.csv    tidy CSV (per-event rows incl. catalog shortName)
  data/processed/gwtc_catalog_stats.json  counts by catalog + fetched timestamp

Idempotent: safe to rerun, previous snapshot files are overwritten in place.
"""

from datetime import datetime, timezone
from pathlib import Path
import json
import hashlib

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "external"
PROC_DIR = ROOT / "data" / "processed"
API = "https://gwosc.org/eventapi/json/GWTC/"
HEADERS = {"User-Agent": "astro-science-exotic-compact-objects/1.1"}


def main():
    fetched_utc = datetime.now(timezone.utc).isoformat()
    response = requests.get(API, timeout=90, headers=HEADERS)
    response.raise_for_status()
    events = response.json().get("events", {})
    if not events:
        raise RuntimeError("GWOSC response contained no events")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    PROC_DIR.mkdir(parents=True, exist_ok=True)

    # Raw dump (full fidelity)
    raw_path = OUT_DIR / "gwosc_gwtc_all.json"
    raw_path.write_text(json.dumps(response.json(), ensure_ascii=False))

    # Tidy CSV: flatten the nested parameter dictionaries into columns
    rows = []
    for key, e in events.items():
        row = {"event_id": e.get("commonName", key)}
        row.update(
            {
                k: v
                for k, v in e.items()
                if k
                in {
                    "version",
                    "catalog.shortName",
                    "GPS",
                    "reference",
                    "gracedb_id",
                    "mass_1_source",
                    "mass_1_source_lower",
                    "mass_1_source_upper",
                    "mass_2_source",
                    "mass_2_source_lower",
                    "mass_2_source_upper",
                    "total_mass_source",
                    "chirp_mass_source",
                    "chirp_mass_source_lower",
                    "chirp_mass_source_upper",
                    "final_mass_source",
                    "final_mass_source_lower",
                    "final_mass_source_upper",
                    "luminosity_distance",
                    "luminosity_distance_lower",
                    "luminosity_distance_upper",
                    "redshift",
                    "redshift_lower",
                    "redshift_upper",
                    "chi_eff",
                    "chi_eff_lower",
                    "chi_eff_upper",
                    "network_matched_filter_snr",
                    "far",
                    "p_astro",
                    "jsonurl",
                }
            }
        )
        rows.append(row)
    df = pd.DataFrame(rows).sort_values("GPS").reset_index(drop=True)
    csv_path = OUT_DIR / "gwosc_gwtc_all.csv"
    df.to_csv(csv_path, index=False)

    # Catalog statistics
    counts = df["catalog.shortName"].value_counts().sort_index().to_dict()
    with_mass = int(df["mass_1_source"].notna().sum())
    with_dist = int(df["luminosity_distance"].notna().sum())
    with_z = int(df["redshift"].notna().sum())
    stats = {
        "fetched_utc": fetched_utc,
        "total_events": len(df),
        "by_catalog": counts,
        "with_mass_1_source": with_mass,
        "with_luminosity_distance": with_dist,
        "with_redshift": with_z,
        "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest()[:16],
        "source_api": API,
    }
    (PROC_DIR / "gwtc_catalog_stats.json").write_text(json.dumps(stats, indent=2))

    print(json.dumps(stats, indent=2))
    print(f"wrote {csv_path} ({len(df)} rows)")


if __name__ == "__main__":
    main()
