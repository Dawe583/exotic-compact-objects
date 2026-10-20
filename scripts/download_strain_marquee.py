#!/usr/bin/env python3
"""Download strain HDF5 files (4 kHz, 4096 s) for marquee GWTC events.

Events chosen for physics value in this project:
  GW170817  (binary neutron star, tidal/GRB counterpart)
  GW190814  (mass-gap secondary 2.6 M_sun)
  GW190521  (IMBH remnant, misaligned/possibly precessing pair)

Each event gets the H1+L1 (V1 when available) 4 kHz HDF5 strain files, saved to
data/raw/strain/<event>/. Files is idempotent: existing files are kept.

After download, run scripts/compute_with_data.py for the analysis.
"""

from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone

import requests

ROOT = Path(__file__).resolve().parents[1]
STRAIN_DIR = ROOT / "data" / "raw" / "strain"
HEADERS = {"User-Agent": "astro-science-exotic-compact-objects/1.1"}

EVENTS = ["GW170817", "GW190814", "GW190521"]


def sha_short(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def download(url: str, dest: Path) -> bool:
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  kept  {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        with requests.get(url, stream=True, timeout=300, headers=HEADERS) as r:
            r.raise_for_status()
            total = int(r.headers.get("content-length", 0))
            with open(dest, "wb") as f:
                got = 0
                for chunk in r.iter_content(1 << 20):
                    if chunk:
                        f.write(chunk)
                        got += len(chunk)
        print(f"  got {dest.name} ({got / 1e6:.1f} MB; announced {total / 1e6:.1f} MB)")
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"  FAIL {url}: {exc}")
        if dest.exists():
            dest.unlink()
        return False


def main():
    manifest = {"fetched_utc": datetime.now(timezone.utc).isoformat(), "events": {}}
    STRAIN_DIR.mkdir(parents=True, exist_ok=True)

    # mapping event -> catalog via previously fetched snapshot's jsonurl
    catalogue = json.loads(
        (ROOT / "data" / "external" / "gwosc_gwtc_all.json").read_text()
    )["events"]

    for event in EVENTS:
        print(f"== {event}")
        entry = next(
            (e for e in catalogue.values() if e.get("commonName") == event), None
        )
        if entry is None:
            print(f"  {event} not in catalog snapshot; skipping")
            continue
        base = entry["jsonurl"]
        r = requests.get(base, timeout=60, headers=HEADERS)
        if not r.ok:
            print(f"  metadata fetch failed ({r.status_code}) for {base}; skipping")
            continue
        j = r.json()

        ev = next(iter(j["events"].values()))
        out = {
            "event": event,
            "metadata_url": base,
            "gps": ev.get("GPS"),
            "catalog": ev.get("catalog.shortName"),
            "files": [],
        }

        for strain in ev.get("strain", []):
            url = strain.get("url", "")
            # 4 kHz HDF5 variants only: LOSC_4 (O1/O2) or GWOSC_4KHZ_R1 (O3+)
            if not url.endswith(".hdf5"):
                continue
            if not ("LOSC_4" in url or "4KHZ_R1" in url):
                continue
            name = url.rsplit("/", 1)[-1]
            if name in out["files"]:
                continue
            dest = STRAIN_DIR / event / name
            if download(url, dest):
                out["files"].append(name)

        out["file_sha256_16"] = [
            sha_short(STRAIN_DIR / event / f) for f in out["files"]
        ]
        manifest["events"][event] = out
        print(f"  -> {len(out['files'])} strain files for {event}")

    (STRAIN_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))
    print("wrote", STRAIN_DIR / "manifest.json")


if __name__ == "__main__":
    main()
