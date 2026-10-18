#!/usr/bin/env python3
"""Download GWOSC GWTC compact-binary catalog snapshot into this project."""
from datetime import datetime, timezone
from pathlib import Path
import json, sqlite3, requests
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "data" / "raw" / "gwosc_gwtc.sqlite"
OUT = ROOT / "reports"
FIG = ROOT / "figures"
API = "https://gwosc.org/eventapi/json/GWTC/"

def main():
    fetched = datetime.now(timezone.utc).isoformat()
    ROOT.joinpath("data/raw").mkdir(parents=True, exist_ok=True)
    response = requests.get(API, timeout=60, headers={"User-Agent": "astro-science-exotic-compact-objects/1.0"})
    response.raise_for_status()
    events = response.json().get("events", {})
    if not events:
        raise RuntimeError("GWOSC response contained no events")
    rows = []
    for key, e in events.items():
        rows.append({
            "event_id": e.get("commonName", key),
            "version": e.get("version"),
            "catalog": e.get("catalog.shortName"),
            "gps": e.get("GPS"),
            "mass_1_source_msun": e.get("mass_1_source"),
            "mass_2_source_msun": e.get("mass_2_source"),
            "total_mass_source_msun": e.get("total_mass_source"),
            "chirp_mass_source_msun": e.get("chirp_mass_source"),
            "final_mass_source_msun": e.get("final_mass_source"),
            "luminosity_distance_mpc": e.get("luminosity_distance"),
            "redshift": e.get("redshift"),
            "chi_eff": e.get("chi_eff"),
            "network_snr": e.get("network_matched_filter_snr"),
            "far_per_year": e.get("far"),
            "p_astro": e.get("p_astro"),
            "source_url": e.get("jsonurl"),
            "fetched_utc": fetched,
        })
    df = pd.DataFrame(rows).drop_duplicates(["event_id", "version"])
    DB.parent.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    FIG.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS gwtc_events (
            event_id TEXT, version INTEGER, catalog TEXT, gps REAL, mass_1_source_msun REAL,
            mass_2_source_msun REAL, total_mass_source_msun REAL, chirp_mass_source_msun REAL,
            final_mass_source_msun REAL, luminosity_distance_mpc REAL, redshift REAL, chi_eff REAL,
            network_snr REAL, far_per_year REAL, p_astro REAL, source_url TEXT, fetched_utc TEXT,
            UNIQUE(event_id,version,fetched_utc))""")
        df.to_sql("_incoming", con, if_exists="replace", index=False)
        cols = ", ".join(df.columns)
        con.execute(f"INSERT OR IGNORE INTO gwtc_events ({cols}) SELECT {cols} FROM _incoming")
        con.execute("DROP TABLE _incoming")
        con.execute("CREATE TABLE IF NOT EXISTS fetch_log (fetched_utc TEXT, source TEXT, row_count INTEGER, http_status INTEGER)")
        con.execute("INSERT INTO fetch_log VALUES (?,?,?,?)", (fetched, API, len(df), response.status_code))
    # CSV mirror
    df.to_csv(ROOT / "data" / "processed" / "gwosc_gwtc.csv", index=False)
    # figure
    valid = df.dropna(subset=["total_mass_source_msun"])
    fig, ax = plt.subplots(figsize=(9, 5))
    if len(valid):
        ax.hist(valid.total_mass_source_msun, bins=min(30, max(5, int(len(valid) ** 0.5))), color="#335c99", edgecolor="white")
        ax.set_xlabel("Source-frame total mass (Msun)")
        ax.set_ylabel("Catalog events")
    ax.set_title("GWOSC compact-binary detections: source-frame total mass")
    fig.tight_layout()
    fig.savefig(FIG / "gwtc_total_mass.png", dpi=160)
    plt.close(fig)
    report = [
        "# Exotic Compact Objects – GWOSC snapshot",
        "",
        f"Updated UTC: {fetched}",
        f"Source: GWOSC GWTC event API ({API})",
        f"Records: {len(df)}",
        "",
        "This is a gravitational-wave transient catalog (mostly compact binary mergers), not a complete census of black holes.",
    ]
    (OUT / "gwosc_latest.md").write_text("\n".join(report))
    print(f"GWOSC: {len(df)} events -> {DB}")

if __name__ == "__main__":
    main()
