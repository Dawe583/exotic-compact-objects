# Data Inventory — Exotic Compact Objects

**Generated:** 2026-18-18
**Total files:** 24 (23 data + this inventory)
**Total size:** 3.6 MB (3,741,168 bytes)

---

## data/external/ — Downloaded observational catalogs (15 files)

| File | Rows | Cols | Size | Source | License |
|------|------|------|------|--------|---------|
| `agn_bh_mass.csv` | 86 | 7 | 7.2 KB | AGN black hole mass catalog (literature compilation) | Public domain (literature values) |
| `atnfpulsar.csv` | 4,503 | 147 | 2.1 MB | [ATNF Pulsar Catalogue](https://www.atnf.csiro.au/research/pulsar/psrcat/) (Manchester et al. 2005) | Academic use with citation |
| `black_melody.csv` | 7 | 97 | 4.2 KB | "Black Melody" — stellar-mass BH candidates from massive binaries (Liu et al. 2019/2020) | Public domain (literature) |
| `changalxrb.csv` | 4,442 | 17 | 526 KB | HEASARC `changalxrb` — Chandra LMXB catalog | Public domain (NASA) |
| `chanulxcat.csv` | 155 | 23 | 28 KB | HEASARC `chanulxcat` — Chandra ULX catalog | Public domain (NASA) |
| `dxrbs.csv` | 229 | 47 | 51 KB | HEASARC `dxrbs` — Deep X-ray Radio Burst catalog | Public domain (NASA) |
| `m83xrbcxo.csv` | 325 | 17 | 46 KB | HEASARC `m83xrbcxo` — M83 XRB/CXO catalog | Public domain (NASA) |
| `m87cxo.csv` | 174 | 13 | 22 KB | HEASARC `m87cxo` — M87 Chandra X-ray source catalog | Public domain (NASA) |
| `pulsar.csv` | 706 | 71 | 254 KB | HEASARC `pulsar` — pulsar catalog (subset) | Public domain (NASA) |
| `sgraregcsc.csv` | 318 | 22 | 41 KB | HEASARC `sgraregcsc` — Sgr A* region Chandra source catalog | Public domain (NASA) |
| `snrgreen.csv` | 295 | 16 | 28 KB | HEASARC `snrgreen` — Green supernova remnant catalog | Public domain (NASA) |
| `ulxngcat.csv` | 107 | 14 | 14 KB | HEASARC `ulxngcat` — ULX in NGC catalog | Public domain (NASA) |
| `ulxrbcat.csv` | 229 | 25 | 35 KB | HEASARC `ulxrbcat` — ULX in RGB catalog | Public domain (NASA) |
| `vlulxcat.csv` | 119 | 15 | 15 KB | HEASARC `vlulxcat` — VLT ULX catalog | Public domain (NASA) |
| `xrbcat.csv` | 229 | 16 | 25 KB | HEASARC `xrbcat` — X-ray binary catalog | Public domain (NASA) |

**External total rows:** 11,838

---

## data/processed/ — Derived & theoretical datasets (7 files)

| File | Rows | Cols / Shape | Size | Source | License |
|------|------|-------------|------|--------|---------|
| `gwosc_gwtc.csv` | 391 | 17 | 72 KB | [GWOSC GWTC event API](https://gwosc.org/eventapi/json/GWTC/) | CC-BY 4.0 |
| `known_compact_objects.csv` | 10 | 5 | 656 B | Literature values (Sgr A*, M87*, Cyg X-1, GW150914, GW190521, TON 618, Phoenix A*, Morris-Thorne wormhole, Ellis drainhole, white hole demo) | Public domain |
| `known_compact_objects.json` | 10 | — | 1.5 KB | Same as above (JSON mirror) | Public domain |
| `constants.json` | 7 keys | — | 181 B | [Astropy/CODATA](https://docs.astropy.org/en/stable/constants/) physical constants | Public domain |
| `mass_grid_msun.npy` | 200 | (200,) float64 | 1.7 KB | Generated: logspace(0, 10, 200) Msun | Generated |
| `whitehole_negative_mass_grid_msun.npy` | 50 | (50,) float64 | 528 B | Generated: -logspace(0, 6, 50) Msun | Generated |
| `wormhole_b0_grid_km.npy` | 100 | (100,) float64 | 928 B | Generated: logspace(-1, 6, 100) km | Generated |

---

## data/raw/ — Raw downloaded archives (1 file)

| File | Size | Tables | Rows | Source | License |
|------|------|--------|------|--------|---------|
| `gwosc_gwtc.sqlite` | 344 KB | `gwtc_events`, `fetch_log` | 782, 2 | [GWOSC GWTC event API](https://gwosc.org/eventapi/json/GWTC/) | CC-BY 4.0 |

---

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/download_gwosc.py` | Download GWOSC GWTC catalog → SQLite + CSV | Pass (391 events) |
| `scripts/download_heasarc.py` | Download 14 HEASARC catalogs via TAP → CSV | Pass (14/14 tables) |
| `scripts/build_theoretical_data.py` | Generate theoretical datasets (known objects, constants, grids) | Pass |

**Note:** `download_heasarc.py` and `build_theoretical_data.py` require `astropy` (installed during this run).

---

## Data notes

- **agn_bh_mass.csv** has a non-standard header (line 2: `<f> value applied = 5.5`). Use `pd.read_csv(..., skiprows=2)` to parse correctly (86 rows, 7 cols).
- **black_melody.csv** contains stellar-mass black hole candidates from massive binary systems (MWC 656, LB-1, HR 6819, etc.) with full orbital parameters and companion star properties.
- **gwosc_gwtc.sqlite** contains 782 rows (all GWTC events from O1/O2/O3) while the CSV has 391 deduplicated entries.
- HEASARC catalogs were queried via the [XAMIN TAP endpoint](https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync) on 2026-10-18.
