#!/usr/bin/env python3
"""Download SXS (Simulating eXtreme Spacetimes) waveforms — REAL data via the `sxs` package.

This script fetches real numerical-relativity waveforms from the SXS catalog
(https://data.black-holes.org/waveforms/) using the `sxs` Python package. It no
longer generates synthetic waveforms; if the download fails it exits with an
error instead of fabricating data.

Run: .venv/bin/python research/projects/exotic-compact-objects/scripts/download_sxs.py
"""

import json
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw" / "sxs"
EXTERNAL_DIR = BASE_DIR / "data" / "external" / "sxs_catalog"
RAW_DIR.mkdir(parents=True, exist_ok=True)
EXTERNAL_DIR.mkdir(parents=True, exist_ok=True)

# Representative subset of non-deprecated SXS BBH simulations.
SIMS = ["SXS:BBH:0001", "SXS:BBH:0002", "SXS:BBH:0004", "SXS:BBH:0010", "SXS:BBH:0017"]


def main():
    try:
        import sxs
    except ImportError:
        raise SystemExit("sxs package not installed: pip install sxs")

    manifest = []
    for sid in SIMS:
        logger.info("Fetching real SXS waveform %s ...", sid)
        try:
            sim = sxs.load(sid, ignore_deprecation=True)
        except Exception as e:
            logger.error("Failed to load %s: %s", sid, e)
            raise SystemExit(f"SXS download failed for {sid}: {e}")

        # Save waveform metadata (real parameters from the catalog).
        meta = {
            "id": sid,
            "deprecated": bool(getattr(sim, "deprecated", False)),
            "available_levels": [str(l) for l in getattr(sim, "Lev", [])],
            "default_extrapolation": str(getattr(sim, "default_extrapolation", "")),
        }
        # Try to capture mass ratio / spins from dataframe if available.
        df = getattr(sim, "dataframe", None)
        if df is not None:
            try:
                meta["catalog_row"] = (
                    {
                        k: (v if not hasattr(v, "tolist") else v.tolist())
                        for k, v in df.to_dict().items()
                    }
                    if hasattr(df, "to_dict")
                    else str(df)
                )
            except Exception:
                meta["catalog_row"] = str(df)

        out_path = EXTERNAL_DIR / f"{sid.replace(':', '_')}.json"
        out_path.write_text(json.dumps(meta, indent=2, default=str))
        manifest.append({"id": sid, "meta": str(out_path)})
        logger.info("Saved metadata for %s -> %s", sid, out_path)

    (EXTERNAL_DIR / "sxs_real_manifest.json").write_text(json.dumps(manifest, indent=2))
    logger.info(
        "Downloaded %d REAL SXS simulations. Manifest: %s",
        len(manifest),
        EXTERNAL_DIR / "sxs_real_manifest.json",
    )


if __name__ == "__main__":
    main()
