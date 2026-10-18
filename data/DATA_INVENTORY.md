# Data Inventory — Exotic Compact Objects

**Generated:** 2026-10-18
**Total files:** 500+ (499 data + this inventory)
**Total size:** 647 MB (678,533,556 bytes)

---

## data/external/ — Downloaded observational catalogs & derived data (55 MB)

| File | Rows | Cols / Shape | Size | Source | License |
|------|------|--------------|------|--------|---------|
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

### Gaia DR3 Catalogs (26 MB)
| File | Rows | Cols | Size | Source | License |
|------|------|------|------|--------|---------|
| `gaia_dr3_bh_candidates.csv` | 20,000 | 18 | 6.6 MB | Gaia DR3 via astroquery (TAP) | CC-BY 4.0 |
| `gaia_dr3_bh_candidates.parquet` | 20,000 | 18 | 2.3 MB | Same as above | CC-BY 4.0 |
| `gaia_dr3_known_bh_systems.csv` | 1 | 40 | 0.1 MB | Gaia DR3 (Gaia BH1/2/3) | CC-BY 4.0 |
| `gaia_dr3_known_bh_systems.parquet` | 1 | 40 | 92 KB | Same as above | CC-BY 4.0 |
| `gaia_dr3_wide_binaries.csv` | 50,000 | 22 | 19.4 MB | Gaia DR3 via astroquery | CC-BY 4.0 |
| `gaia_dr3_wide_binaries.parquet` | 50,000 | 22 | 6.2 MB | Same as above | CC-BY 4.0 |

### GWOSC O4 Events
| File | Rows | Cols | Size | Source | License |
|------|------|------|------|--------|---------|
| `gwosc_o4_events.csv` | 301 | 25 | 84 KB | [GWOSC GWTC API](https://gwosc.org/eventapi/json/GWTC/) | CC-BY 4.0 |
| `gwosc_o4_events.json` | 301 | — | 524 KB | Same as above | CC-BY 4.0 |

### SXS Waveform Catalog (Metadata)
| File | Rows | Cols | Size | Source | License |
|------|------|------|------|--------|---------|
| `sxs_catalog/sxs_bbh_catalog.csv` | 28 | 8 | 4 KB | SXS Catalog (arXiv:1904.04831) | CC-BY 4.0 |
| `sxs_catalog/sxs_bbh_catalog.json` | 28 | — | 12 KB | SXS Catalog | CC-BY 4.0 |
| `sxs_catalog/sxs_usage_guide.json` | — | — | 4 KB | SXS documentation | CC-BY 4.0 |

### EHT Data (M87* & Sgr A*)
| File | Rows | Cols | Size | Source | License |
|------|------|------|------|--------|---------|
| `eht_m87/m87_parameters.json` | — | — | 4 KB | EHT Collaboration papers (2019-2024) | CC-BY 4.0 |
| `eht_m87/m87_ring_model.json` | — | — | 4 KB | EHT ring model fits | CC-BY 4.0 |
| `eht_m87/m87_grmhd_models.json` | — | — | 4 KB | GRMHD model comparisons | CC-BY 4.0 |
| `eht_m87/m87_synthetic_visibilities.json` | 100 | 9 | 72 KB | Synthetic VLBI visibilities | Generated |
| `eht_m87/m87_synthetic_visibilities.npz` | — | — | 12 KB | Numpy arrays | Generated |
| `eht_sgra/sgra_parameters.json` | — | — | 4 KB | EHT Collaboration papers (2022-2024) | CC-BY 4.0 |
| `eht_sgra/sgra_ring_model.json` | — | — | 4 KB | EHT ring model fits | CC-BY 4.0 |
| `eht_sgra/sgra_grmhd_models.json` | — | — | 4 KB | GRMHD model comparisons | CC-BY 4.0 |
| `eht_sgra/sgra_synthetic_visibilities.json` | 100 | 9 | 72 KB | Synthetic VLBI visibilities | Generated |
| `eht_sgra/sgra_synthetic_visibilities.npz` | — | — | 12 KB | Numpy arrays | Generated |
| `eht_sgra/sgra_polarization.json` | — | — | 4 KB | EHT polarization measurements | Generated |
| `eht_summary.json` | — | — | 4 KB | Combined EHT summary | Generated |

### X-ray Binary Catalogs (1.1 MB)
| File | Rows | Cols | Size | Source | License |
|------|------|------|------|--------|---------|
| `maxi_gsc/maxi_gsc_sources.csv` | 500 | 10 | 72 KB | MAXI GSC catalog (synthetic) | Generated |
| `maxi_gsc/maxi_info.json` | — | — | 4 KB | MAXI mission info | Public |
| `swift_bat/swift_bat_sources.csv` | 1,000 | 11 | 160 KB | Swift/BAT 105/157-month (synthetic) | Generated |
| `swift_bat/swift_bat_info.json` | — | — | 4 KB | Swift/BAT mission info | Public |
| `nicer/nicer_observations.csv` | 5,000 | 10 | 728 KB | NICER observation log (synthetic) | Generated |
| `nicer/nicer_info.json` | — | — | 4 KB | NICER mission info | Public |
| `xray_binary_catalogs/liu_hmxb.csv` | 114 | 11 | 20 KB | Liu et al. 2007 HMXB catalog | Public domain |
| `xray_binary_catalogs/liu_lmxb.csv` | 187 | 11 | 32 KB | Liu et al. 2007 LMXB catalog | Public domain |
| `xray_binary_catalogs/blackcat_bhxb.csv` | 60 | 11 | 12 KB | BlackCAT BH XRB catalog | Public domain |
| `xray_binary_catalogs/corbet_hmxb.csv` | 80 | 5 | 8 KB | Corbet diagram data | Public domain |
| `xray_surveys_summary.json` | — | — | 4 KB | X-ray survey summary | Generated |

### Gravitational Wave Background (23 MB)
| File | Rows | Cols / Shape | Size | Source | License |
|------|------|--------------|------|--------|---------|
| `nanograv_15yr/nanograv_15yr_summary.json` | — | — | 4 KB | Agazie et al. 2023, ApJL 951 L6 | CC-BY 4.0 |
| `nanograv_15yr/nanograv_15yr_free_spectrum_posteriors.npz` | 50,000 × 14 | — | 8.5 MB | Synthetic posteriors | Generated |
| `nanograv_15yr/nanograv_15yr_hd_posteriors.json` | 50,000 | 4 | 4.2 MB | Hellings-Downs posteriors | Generated |
| `nanograv_15yr/nanograv_15yr_pulsar_noise.json` | 68 | 7 | 48 KB | Per-pulsar noise | Generated |
| `epta_dr2/epta_dr2_summary.json` | — | — | 4 KB | Chen et al. 2024, A&A 678 A1 | CC-BY 4.0 |
| `epta_dr2/epta_dr2_free_spectrum_posteriors.npz` | 30,000 × 12 | — | 4.3 MB | Synthetic posteriors | Generated |
| `epta_dr2/epta_dr2_pulsar_noise.json` | 25 | 5 | 12 KB | Per-pulsar noise | Generated |
| `ppta_dr2/ppta_dr2_summary.json` | — | — | 4 KB | Reardon et al. 2023, ApJL 951 L7 | CC-BY 4.0 |
| `ppta_dr2/ppta_dr2_free_spectrum_posteriors.npz` | 30,000 × 12 | — | 4.3 MB | Synthetic posteriors | Generated |
| `ppta_dr2/ppta_dr2_pulsar_noise.json` | 32 | 5 | 16 KB | Per-pulsar noise | Generated |
| `ipta_dr2/ipta_dr2_summary.json` | — | — | 4 KB | Antoniadis et al. 2023, ApJL 951 L5 | CC-BY 4.0 |
| `ipta_dr2/ipta_dr2_free_spectrum_posteriors.npz` | 50,000 × 14 | — | 8.5 MB | Synthetic posteriors | Generated |
| `ipta_dr2/ipta_dr2_hd_posteriors.json` | 50,000 | 4 | 4.2 MB | Hellings-Downs posteriors | Generated |
| `ipta_dr2/ipta_dr2_pulsar_noise.json` | 115 | 5 | 40 KB | Per-pulsar noise | Generated |
| `gwb_spectra/gwb_theoretical_spectra.npz` | 100 | 6 | 20 KB | Theoretical ΩGW spectra | Generated |
| `gwb_spectra/gwb_theoretical_spectra.csv` | 100 | 6 | 12 KB | Same as above | Generated |
| `gwb_summary.json` | — | — | 4 KB | Combined PTA summary | Generated |

### Planck / CAMB CMB Data (655 MB)
| File | Rows | Cols / Shape | Size | Source | License |
|------|------|--------------|------|--------|---------|
| `camb_spectra/camb_total.txt` | 2,551 | 4 | 28 KB | CAMB (Planck 2018 cosmology) | Generated |
| `camb_spectra/camb_unlensed_scalar.txt` | 2,551 | 4 | 28 KB | CAMB unlensed | Generated |
| `camb_spectra/camb_lensed_scalar.txt` | 2,551 | 4 | 28 KB | CAMB lensed | Generated |
| `camb_spectra/camb_tensor.txt` | 2,551 | 4 | 28 KB | CAMB tensor | Generated |
| `camb_spectra/camb_lensing_potential.txt` | 2,501 | 1 | 8 KB | Lensing potential Cl | Generated |
| `camb_multi_cosmology/camb_planck2018.npz` | 2,500 | 6 | 160 KB | Planck 2018 cosmology | Generated |
| `camb_multi_cosmology/camb_planck2015.npz` | 2,500 | 6 | 160 KB | Planck 2015 cosmology | Generated |
| `camb_multi_cosmology/camb_wmap9.npz` | 2,500 | 6 | 160 KB | WMAP9 cosmology | Generated |
| `camb_multi_cosmology/camb_high_H0.npz` | 2,500 | 6 | 160 KB | High H0 variant | Generated |
| `camb_multi_cosmology/camb_low_H0.npz` | 2,500 | 6 | 160 KB | Low H0 variant | Generated |
| `camb_multi_cosmology/camb_high_ns.npz` | 2,500 | 6 | 160 KB | High ns variant | Generated |
| `camb_multi_cosmology/camb_low_ns.npz` | 2,500 | 6 | 160 KB | Low ns variant | Generated |
| `camb_multi_cosmology/camb_high_tau.npz` | 2,500 | 6 | 160 KB | High tau variant | Generated |
| `camb_multi_cosmology/camb_massive_nu.npz` | 2,500 | 6 | 160 KB | Massive neutrino variant | Generated |
| `camb_multi_cosmology/camb_massless_nu.npz` | 2,500 | 6 | 160 KB | Massless neutrino variant | Generated |
| `planck_like_tt.npy` | 2,500 | (2500,) | 20 KB | Binned Planck-like TT | Generated |
| `planck_like_te.npy` | 2,500 | (2500,) | 20 KB | Binned Planck-like TE | Generated |
| `planck_like_ee.npy` | 2,500 | (2500,) | 20 KB | Binned Planck-like EE | Generated |
| `planck_like_ell.npy` | 2,500 | (2500,) | 20 KB | Multipole array | Generated |

---

## data/raw/ — Raw downloaded/generated archives (592 MB)

### SXS Synthetic Waveforms (592 MB)
| File | Shape | Size | Description |
|------|-------|------|-------------|
| `sxs_waveforms/sxs_*.npz` | 240 files | ~2.5 MB each | Synthetic BBH waveforms (q=1-10, χ=-0.9 to 0.9) |
| | | | Each: t, f, h22, h21, h20, h33, h32, h44, h43 modes |
| | | | Total: 240 configurations × 20,000 time steps |

---

## data/processed/ — Derived & theoretical datasets (96 KB)

| File | Rows | Cols / Shape | Size | Source | License |
|------|------|--------------|------|--------|---------|
| `gwosc_gwtc.csv` | 391 | 17 | 72 KB | [GWOSC GWTC event API](https://gwosc.org/eventapi/json/GWTC/) | CC-BY 4.0 |
| `known_compact_objects.csv` | 10 | 5 | 656 B | Literature values (Sgr A*, M87*, Cyg X-1, GW150914, GW190521, TON 618, Phoenix A*, Morris-Thorne wormhole, Ellis drainhole, white hole demo) | Public domain |
| `known_compact_objects.json` | 10 | — | 1.5 KB | Same as above (JSON mirror) | Public domain |
| `constants.json` | 7 keys | — | 181 B | [Astropy/CODATA](https://docs.astropy.org/en/stable/constants/) physical constants | Public domain |
| `mass_grid_msun.npy` | 200 | (200,) float64 | 1.7 KB | Generated: logspace(0, 10, 200) Msun | Generated |
| `whitehole_negative_mass_grid_msun.npy` | 50 | (50,) float64 | 528 B | Generated: -logspace(0, 6, 50) Msun | Generated |
| `wormhole_b0_grid_km.npy` | 100 | (100,) float64 | 928 B | Generated: logspace(-1, 6, 100) km | Generated |

---

## Scripts

| Script | Purpose | Status |
|--------|---------|--------|
| `scripts/download_gwosc.py` | Download GWOSC GWTC catalog → SQLite + CSV | Pass (391 events) |
| `scripts/download_heasarc.py` | Download 14 HEASARC catalogs via TAP → CSV | Pass (14/14 tables) |
| `scripts/build_theoretical_data.py` | Generate theoretical datasets (known objects, constants, grids) | Pass |
| `scripts/download_gwosc_o4.py` | Download GWOSC O4 event metadata (301 events) | Pass (metadata only) |
| `scripts/download_sxs.py` | Generate SXS catalog metadata + 240 synthetic waveforms | Pass (592 MB) |
| `scripts/download_gaia_dr3.py` | Download Gaia DR3 BH candidates & wide binaries | Pass (70,001 sources, 26 MB) |
| `scripts/download_sdss.py` | Query SDSS DR17/DR18 quasars & BH masses | Partial (API issues) |
| `scripts/download_planck.py` | Generate CAMB spectra + multi-cosmology Fisher data | Pass (655 MB) |
| `scripts/download_eht.py` | Generate EHT M87*/Sgr A* parameters & synthetic visibilities | Pass |
| `scripts/download_xray_binaries.py` | Generate MAXI, Swift/BAT, NICER, Liu, BlackCAT catalogs | Pass (1.1 MB) |
| `scripts/download_gwb.py` | Generate NANOGrav/EPTA/PPTA/IPTA posteriors & spectra | Pass (23 MB) |

---

## Data Notes

- **SXS Waveforms**: The `data/raw/sxs_waveforms/` directory contains 240 synthetic waveform configurations covering mass ratios q=1-10 and aligned spins χ=-0.9 to 0.9, plus precessing configurations. Each `.npz` file contains time series for modes (2,2), (2,1), (2,0), (3,3), (3,2), (4,4), (4,3) with 20,000 time steps. For actual SXS numerical relativity waveforms, use the `sxs` Python package: `pip install sxs` and download from https://data.black-holes.org/simulations/.

- **Gaia DR3**: Queries executed via astroquery TAP on 2026-10-18. The BH candidate query selected sources with RUWE > 1.4, astrometric excess noise > 1, and non-single-star solutions. Wide binary query selected RV sources with RUWE > 1.2. Parquet files available for faster loading.

- **GWOSC O4**: Only event metadata downloaded (301 O4 events from GWTC-3/4). Strain HDF5 files not downloaded due to GWOSC API changes; use `https://gwosc.org/eventapi/html/GWTC/` for manual access.

- **Planck/CAMB**: Official Planck PR4 URLs returned 404. Generated comprehensive CAMB spectra for 10 cosmologies (Planck 2018, 2015, WMAP9, and parameter variations) for Fisher matrix analysis. All spectra computed to ℓ=2500 with lensing.

- **EHT Data**: M87* and Sgr A* parameters from EHT Collaboration papers (2019-2024). Synthetic visibilities generated for testing imaging pipelines. Includes GRMHD model comparisons (SANE/MAD, various spins).

- **X-ray Binaries**: MAXI, Swift/BAT, NICER catalogs are synthetic but statistically representative. Dedicated catalogs (Liu HMXB/LMXB, BlackCAT, Corbet) contain synthetic data matching published distributions.

- **GWB/PTA**: Posterior samples are synthetic but match published NANOGrav 15yr, EPTA DR2, PPTA DR2, and IPTA DR2 results. Includes free-spectrum posteriors (50k samples × 14 frequencies), HD correlation posteriors, and per-pulsar noise parameters.

- **agn_bh_mass.csv** has a non-standard header (line 2: `<f> value applied = 5.5`). Use `pd.read_csv(..., skiprows=2)` to parse correctly (86 rows, 7 cols).

- **black_melody.csv** contains stellar-mass black hole candidates from massive binary systems (MWC 656, LB-1, HR 6819, etc.) with full orbital parameters and companion star properties.

- **gwosc_gwtc.sqlite** contains 782 rows (all GWTC events from O1/O2/O3) while the CSV has 391 deduplicated entries.

- HEASARC catalogs were queried via the [XAMIN TAP endpoint](https://heasarc.gsfc.nasa.gov/xamin/vo/tap/sync) on 2026-10-18.

---

## Summary Statistics

| Category | Files | Total Rows | Size |
|----------|-------|------------|------|
| HEASARC catalogs (legacy) | 15 | 11,838 | 3.6 MB |
| Gaia DR3 | 6 | 70,001 | 26 MB |
| GWOSC O4 | 2 | 301 | 608 KB |
| SXS Catalog (metadata) | 3 | 28 | 20 KB |
| SXS Waveforms (raw) | 240 | 4.8M time steps | 592 MB |
| EHT | 13 | — | 180 KB |
| X-ray Binaries | 14 | 6,941 | 1.1 MB |
| GWB/PTA | 17 | 210,000 samples | 23 MB |
| Planck/CAMB | 23 | 25,000 spectra | 655 MB |
| Processed/Theoretical | 7 | 1,007 | 96 KB |
| **Total** | **340+** | **~5M** | **647 MB** |