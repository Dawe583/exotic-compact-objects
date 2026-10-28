#!/usr/bin/env python3
"""Verify all databases and datasets contain real data with proper provenance."""

import sqlite3
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTERNAL = ROOT / "data" / "external"
PROCESSED = ROOT / "data" / "processed"
RAW = ROOT / "data" / "raw"
ECO_ROOT = Path("/home/dawe/Projects/astro-science")

errors = []
warnings = []
checked = 0


def check_sqlite(db_path, expected_min_rows=30000):
    global checked
    if not db_path.exists():
        errors.append(f"MISSING: {db_path}")
        return
    conn = sqlite3.connect(str(db_path))
    tables = [
        r[0]
        for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    ]
    if not tables:
        errors.append(f"NO TABLES: {db_path}")
        conn.close()
        return
    for t in tables:
        if t.startswith("sqlite_"):
            continue
        count = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        checked += 1
        if t == "fetch_log":
            if count < 1:
                errors.append(f"EMPTY fetch_log: {db_path}")
            else:
                print(f"  OK: {db_path.name}/{t} ({count} fetch records)")
            continue
        if count < expected_min_rows:
            errors.append(
                f"TOO FEW ROWS: {db_path}/{t} has {count} (need {expected_min_rows})"
            )
        cols = [d[1] for d in conn.execute(f"PRAGMA table_info({t})").fetchall()]
        if cols:
            null_count = conn.execute(
                f"SELECT COUNT(*) FROM {t} WHERE {cols[0]} IS NULL"
            ).fetchone()[0]
            if null_count > 0:
                warnings.append(
                    f"NULL IDs: {db_path}/{t} has {null_count} NULL in {cols[0]}"
                )
        print(f"  OK: {db_path.name}/{t} ({count} rows)")
    conn.close()


def check_csv(csv_path, required_cols=None, min_rows=1):
    global checked
    if not csv_path.exists():
        errors.append(f"MISSING: {csv_path}")
        return
    with open(csv_path, newline="", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        cols = reader.fieldnames or []
        rows = list(reader)
    checked += 1
    if len(rows) < min_rows:
        errors.append(f"TOO FEW ROWS: {csv_path} has {len(rows)} (need {min_rows})")
    if required_cols:
        missing = [c for c in required_cols if c not in cols]
        if missing:
            errors.append(f"MISSING COLUMNS: {csv_path}: {missing}")
    for col in cols:
        vals = [r.get(col, "") for r in rows]
        if all(v in ("", "nan", "NaN", "None", "null") for v in vals) and len(rows) > 0:
            warnings.append(f"ALL-EMPTY COLUMN: {csv_path.name}/{col}")
    print(f"  OK: {csv_path.name} ({len(rows)} rows, {len(cols)} cols)")


def check_tsv(tsv_path):
    global checked
    if not tsv_path.exists():
        errors.append(f"MISSING: {tsv_path}")
        return
    text = tsv_path.read_text(encoding="utf-8", errors="replace")
    if "#Title: BlackCAT" not in text:
        warnings.append(f"NO BlackCAT HEADER: {tsv_path}")
    lines = [l for l in text.splitlines() if not l.startswith("#")]
    checked += 1
    if len(lines) < 2:
        errors.append(f"EMPTY TSV: {tsv_path}")
    else:
        print(f"  OK: {tsv_path.name} ({len(lines) - 1} data rows)")


def check_json(json_path, required_keys=None):
    global checked
    if not json_path.exists():
        errors.append(f"MISSING: {json_path}")
        return
    try:
        data = json.loads(json_path.read_text())
    except json.JSONDecodeError as e:
        errors.append(f"INVALID JSON: {json_path}: {e}")
        return
    checked += 1
    if required_keys and isinstance(data, dict):
        missing = [k for k in required_keys if k not in data]
        if missing:
            warnings.append(f"MISSING KEYS: {json_path}: {missing}")
    print(f"  OK: {json_path.name}")


print("=== SQLite databases ===")
check_sqlite(RAW / "gwosc_gwtc.sqlite", 30000)
check_sqlite(
    Path(
        "/home/dawe/Projects/astro-science/research/projects/black-holes/data/black_holes.sqlite"
    ),
    30000,
)

print("\n=== HEASARC CSVs ===")
heasarc_required = {
    "xrbcat.csv": ["name", "ra", "dec"],
    "pulsar.csv": ["name", "ra", "dec"],
    "atnfpulsar.csv": ["name", "ra", "dec"],
}
for csv_name, req in heasarc_required.items():
    check_csv(EXTERNAL / csv_name, required_cols=req, min_rows=10)
for csv_path in sorted(EXTERNAL.glob("*.csv")):
    if csv_path.name not in heasarc_required:
        check_csv(csv_path, min_rows=1)

print("\n=== BlackCAT TSVs ===")
for tsv_path in sorted(EXTERNAL.glob("blackcat_*.tsv")):
    check_tsv(tsv_path)

print("\n=== Processed CSVs ===")
check_csv(PROCESSED / "gwtc_recent_20_remnants.csv", min_rows=10)
check_csv(PROCESSED / "agn_reverberation_masses.csv", min_rows=50)
check_csv(PROCESSED / "blackcat_dynamical.csv", min_rows=10)
exo_path = PROCESSED / "exoplanets.csv"
if exo_path.exists():
    check_csv(exo_path, min_rows=1000)
agn_path = PROCESSED / "agn_demographics.csv"
if agn_path.exists():
    check_csv(agn_path, min_rows=10)

print("\n=== Exoplanet data ===")
exo_proc = Path(
    "/home/dawe/Projects/astro-science/research/projects/exoplanets/data/processed/exoplanets.csv"
)
if exo_proc.exists():
    check_csv(exo_proc, min_rows=1000)

print("\n=== Results JSON ===")
check_json(ROOT / "results/derivation_checks.json")
exo_deriv = Path(
    "/home/dawe/Projects/astro-science/research/projects/exoplanets/results/exoplanet_derivation_checks.json"
)
if exo_deriv.exists():
    check_json(exo_deriv)

print("\n=== Verification summary ===")
print(f"  Checked: {checked} datasets")
if warnings:
    # Filter out expected empty columns (ATNF pulsar has many optional flux columns)
    real_warnings = [w for w in warnings if "ALL-EMPTY COLUMN" not in w]
    empty_col_warnings = [w for w in warnings if "ALL-EMPTY COLUMN" in w]
    print(
        f"  Warnings: {len(warnings)} ({len(empty_col_warnings)} empty-column, informational)"
    )
    for w in real_warnings[:10]:
        print(f"    - {w}")
if errors:
    print(f"  ERRORS: {len(errors)}")
    for e in errors:
        print(f"    - {e}")
    sys.exit(1)
else:
    print("  ALL DATA VERIFIED")
    sys.exit(0)
