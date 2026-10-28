#!/usr/bin/env python3
"""Fetch the published BlackCAT dynamical sample and related VizieR tables.

Robustness (2026-10-28): VizieR endpoints occasionally become unreachable from
this network (all public mirrors timing out for hours). The script therefore
tries multiple mirrors in order and, if all fail, falls back to the newest
cached TSVs in data/external provided they are < 7 days old. A cache fallback
is announced loudly ("DEGRADED") so the refresh log keeps an audit trail
(data provenance: cached VizieR download, exact fetch date).
"""

from datetime import datetime, timezone
from pathlib import Path
import socket
import sys
from urllib.parse import urlsplit

import requests

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/external"
OUT.mkdir(parents=True, exist_ok=True)

MAX_CACHE_AGE_DAYS = 7
PROBE_TIMEOUT_SEC = 8  # quick reachability probe; a failure skips the mirror
MIRRORS = (
    "https://vizier.cds.unistra.fr/viz-bin/asu-tsv",
    "https://vizier.cfa.harvard.edu/viz-bin/asu-tsv",
    "https://vizier.nao.ac.jp/viz-bin/asu-tsv",
)
TABLES = ("tablea1", "tablea2", "tablea3", "tablea4", "refs")
HEADERS = {"User-Agent": "astro-science research project; BlackCAT reproducibility"}


def reachable_mirrors() -> list[str]:
    """Return mirror base URLs whose host accepts a TCP connection on 443.

    One short connect probe avoids burning minutes of per-request connect
    timeouts when a whole mirror (or route) is blackholed.
    """
    live: list[str] = []
    for base in MIRRORS:
        host = urlsplit(base).hostname
        try:
            socket.create_connection((host, 443), timeout=PROBE_TIMEOUT_SEC).close()
        except OSError as exc:
            print(f"  mirror unreachable: {host} -> {type(exc).__name__}", flush=True)
            continue
        live.append(base)
    return live


def fetch_table(table: str, mirrors: list[str]) -> str:
    """Fetch one VizieR TSV from the first mirror that succeeds.

    A mirror that times out is removed from `mirrors` for the rest of the run:
    a blackholed endpoint stays blackholed, so retrying later tables against
    it would only add minutes of wall time.
    """
    query = f"?-source=J/A%2BA/587/A61/{table}&-out.all"
    for i, base in enumerate(mirrors):
        try:
            response = requests.get(base + query, timeout=30, headers=HEADERS)
            response.raise_for_status()
            if "#Title: BlackCAT" not in response.text:
                raise RuntimeError(f"Unexpected VizieR response for {table} ({base})")
            return response.text
        except Exception as exc:
            mirrors.pop(i)  # trip-wire: retire failed mirror for this run
            print(
                f"  mirror failed for {table}: {base} -> {type(exc).__name__}",
                flush=True,
            )
    raise RuntimeError(f"All reachable VizieR mirrors failed for {table}")


def cache_age_days(path: Path) -> float | None:
    if not path.exists():
        return None
    mtime = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return (datetime.now(timezone.utc) - mtime).total_seconds() / 86400.0


def main() -> int:
    mirrors = reachable_mirrors()
    if not mirrors:
        print("  all VizieR mirrors unreachable (TCP probe failed)", flush=True)
    fetched = 0
    for table in TABLES:
        if not mirrors:
            break
        try:
            text = fetch_table(table, mirrors)
        except RuntimeError as err:
            print(f"  {err}", flush=True)
            continue
        (OUT / f"blackcat_{table}.tsv").write_text(text)
        print(table, len(text.encode()), "bytes", flush=True)
        fetched += 1

    if fetched == len(TABLES):
        return 0

    # Network failure paths — decide whether the cache is acceptable.
    missing = [t for t in TABLES if not (OUT / f"blackcat_{t}.tsv").exists()]
    ages = {
        t: cache_age_days(OUT / f"blackcat_{t}.tsv")
        for t in TABLES
        if (OUT / f"blackcat_{t}.tsv").exists()
    }
    stale = [t for t, age in ages.items() if age is None or age > MAX_CACHE_AGE_DAYS]

    if missing or stale:
        print(
            f"FAIL: {len(missing)} missing {missing or ''} {len(stale)} stale >"
            f"{MAX_CACHE_AGE_DAYS}d {stale or ''} and all VizieR mirrors unreachable",
            flush=True,
        )
        return 1

    oldest = max(days for days in ages.values() if days is not None)
    print(
        f"DEGRADED (cached data): all VizieR mirrors unreachable; using local TSVs "
        f"fetched {oldest:.2f} days ago (limit {MAX_CACHE_AGE_DAYS}). "
        f"Data source for downstream processing: cached VizieR J/A+A/587/A61 — "
        f"re-fetch pending until the service is reachable again.",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
