#!/usr/bin/env python3
"""Download HEASARC catalogs relevant to compact objects (XRB, M87, Sgr A* region, ULX)."""
from pathlib import Path
from io import BytesIO
import requests
from astropy.table import Table

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "external"
ENDPOINT = "https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync"

TABLES = {
    "xrbcat": "SELECT * FROM xrbcat",
    "m87cxo": "SELECT * FROM m87cxo",
    "sgraregcsc": "SELECT * FROM sgraregcsc",
    "ulxrbcat": "SELECT * FROM ulxrbcat",
    "dxrbs": "SELECT * FROM dxrbs",
    "ulxngcat": "SELECT * FROM ulxngcat",
    "vlulxcat": "SELECT * FROM vlulxcat",
    "chanulxcat": "SELECT * FROM chanulxcat",
    "snrgreen": "SELECT * FROM snrgreen",
    "pulsar": "SELECT * FROM pulsar",
    "atnfpulsar": "SELECT * FROM atnfpulsar",
    "m83xrbcxo": "SELECT * FROM m83xrbcxo",
    "changalxrb": "SELECT * FROM changalxrb",
}

def tap(query):
    r = requests.get(ENDPOINT, params={"REQUEST": "doQuery", "LANG": "ADQL", "QUERY": query, "FORMAT": "votable"}, timeout=120)
    r.raise_for_status()
    return Table.read(BytesIO(r.content), format="votable")

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, q in TABLES.items():
        try:
            t = tap(q)
            for col in list(t.colnames):
                if col.startswith("__"):
                    t.remove_column(col)
            df = t.to_pandas()
            csv_path = OUT / f"{name}.csv"
            df.to_csv(csv_path, index=False)
            # Also save as parquet if pyarrow available
            try:
                df.to_parquet(OUT / f"{name}.parquet", index=False)
            except Exception:
                pass
            print(f"{name}: {len(df)} rows -> {csv_path}")
        except Exception as e:
            print(f"{name}: FAILED {e}")

if __name__ == "__main__":
    main()
