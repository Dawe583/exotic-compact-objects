#!/usr/bin/env python3
"""Fetch the published BlackCAT dynamical sample and related VizieR tables."""

from pathlib import Path
import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/external"
OUT.mkdir(parents=True, exist_ok=True)
BASE = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"
for table in ("tablea1", "tablea2", "tablea3", "tablea4", "refs"):
    url = f"{BASE}?-source=J/A%2BA/587/A61/{table}&-out.all"
    response = requests.get(
        url,
        timeout=300,
        headers={
            "User-Agent": "astro-science research project; BlackCAT reproducibility"
        },
    )
    response.raise_for_status()
    if "#Title: BlackCAT" not in response.text:
        raise RuntimeError(f"Unexpected VizieR response for {table}")
    (OUT / f"blackcat_{table}.tsv").write_text(response.text)
    print(table, len(response.content), "bytes")
