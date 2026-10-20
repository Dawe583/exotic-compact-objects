# Exotic Compact Objects – Research Project

**Objects:** Black holes (BH), wormholes (WH), white holes  
**Focus:** theoretical models and basic equations (first pass)  
**Data:** GWOSC GWTC, HEASARC (XRB, M87, Sgr A* region, ULX), theoretical grids

## Structure

```
exotic-compact-objects/
├── data/
│   ├── raw/          # GWOSC SQLite snapshot
│   ├── external/     # HEASARC catalogs (CSV)
│   └── processed/    # derived CSV/NPY/JSON
├── models/equations.py  # core equations
├── notebooks/
│   ├── 01_exotic_compact_objects_fundamentals.ipynb
│   ├── 02_extended_models.ipynb
│   ├── 03_data_exploration.ipynb
│   ├── 04_white_hole_instability.ipynb
│   ├── 05_equation_derivations.ipynb
│   ├── 06_visual_models.ipynb
│   ├── 07_geodesics.ipynb
│   ├── 08_sympy_christoffel.ipynb
│   ├── 09_white_hole_extended.ipynb
│   ├── 10_complete_theory.ipynb
│   ├── 11_data_synthesis.ipynb
│   ├── 12_advanced_models.ipynb
│   ├── 13_white_hole_deep_dive.ipynb
│   ├── 14_rebound_nbody.ipynb
│   ├── 15_einsteinpy_geodesics.ipynb
│   ├── 16_yt_cosmology.ipynb
│   ├── 17_gw_analysis.ipynb
│   ├── 18_ml_astronomy.ipynb
│   ├── 19_gw_strain_analysis.ipynb
│   ├── 20_gwtc_remnant_catalog.ipynb
│   ├── 21_agn_mass_catalog.ipynb
│   ├── 22_blackcat_dynamical_catalog.ipynb
│   ├── 23_early_smbh_growth.ipynb
│   └── 24_quantum_gravity.ipynb
├── scripts/          # download + build scripts
├── figures/
└── reports/
```

## Research website

The GitHub Pages site (`docs/`) is generated from the catalogues and figures:

- **Portal:** https://dawe583.github.io/exotic-compact-objects/
- **Research site:** https://dawe583.github.io/exotic-compact-objects/premium/

Rebuild and publish:

```bash
cd /home/dawe/Projects/astro-science/research/projects/exotic-compact-objects
/home/dawe/Projects/astro-science/.venv/bin/python scripts/build_premium_site.py --publish
```

The build reads row counts directly from the CSVs, so the data page cannot go
stale. Authored theory pages are re-wrapped in the shared shell and are never
regenerated from scratch.

## Setup / data

```bash
cd /home/dawe/Projects/astro-science
source .venv/bin/activate
cd research/projects/exotic-compact-objects
python scripts/download_gwosc.py
python scripts/download_heasarc.py
python scripts/build_theoretical_data.py
python scripts/make_notebook.py
python scripts/make_notebook2.py
```

## Recent GWTC remnant sample (20 events)

`data/processed/gwtc_recent_20_remnants.csv` contains the 20 latest distinct catalog events with reported final source-frame mass, selected from the local processed GWTC snapshot. It retains component masses, remnant mass, catalog asymmetric signed uncertainty deltas (when available), luminosity distance, redshift, effective spin, SNR, astrophysical probability, catalog and source URL. These are **binary-merger remnants**, not 20 isolated black holes; the convenience selection is not population-unbiased. Catalog measurements and confidence intervals should be interpreted using the linked GWOSC event posterior, not as exact values.

Rebuild the interactive Plotly dashboard with:

```bash
cd /home/dawe/Projects/astro-science/research/projects/exotic-compact-objects
/home/dawe/Projects/astro-science/.venv/bin/python scripts/build_gwtc_remnant_dashboard.py
```

Outputs: `premium/figures/gwtc_recent_20_remnants.html` and exploration notebook `notebooks/20_gwtc_remnant_catalog.ipynb`.

## BlackCAT dynamical stellar-mass systems

Published BlackCAT VizieR tables are mirrored at `data/external/blackcat_tablea1.tsv` through `tablea4.tsv` plus `blackcat_refs.tsv`; fetch again with `scripts/download_blackcat.py` and rebuild the cleaned 18-row joined subset using `scripts/process_blackcat.py`. The cleaned data are `data/processed/blackcat_dynamical.csv`. It includes masses, asymmetric errors or explicit limit flags, orbital periods, mass functions, companion RV amplitudes, distances, positions, outburst counts, and citations. The original local `blackcat_bhxb.csv` contains synthetic `BHXRB_###` rows and was not used as observational evidence. Rebuild the Plotly view via `/home/dawe/Projects/astro-science/.venv/bin/python scripts/build_blackcat_dashboard.py`; see `notebooks/22_blackcat_dynamical_catalog.ipynb`. The notebook audits $f(M)=PK_2^3/(2\pi G)$, but disagreement can arise from mixed per-object literature inputs; reported values remain untouched pending paper-level checks.

## AGN reverberation-mapping mass sample

`data/processed/agn_reverberation_masses.csv` normalizes the local 86-row AGN compilation; 70 entries have numeric log-mass estimates. It retains positions, redshift, original log-mass errors and converted asymmetric linear-mass offsets. Run `/home/dawe/Projects/astro-science/.venv/bin/python scripts/build_agn_reverberation_dashboard.py` to regenerate `premium/figures/agn_reverberation_catalog.html`; see `notebooks/21_agn_mass_catalog.ipynb`. Reported uncertainties are transformed as $\Delta M_-=M(1-10^{-\sigma_-})$ and $\Delta M_+=M(10^{\sigma_+}-1)$, where the catalogue error columns are dex offsets. The literature compilation is heterogeneous and not selection-corrected; use descriptive plots only unless selection and measurement systematics are modeled. Both processed catalogs also include Astropy-derived Schwarzschild radius, Eddington luminosity (using the conventional 1.26×10^38 erg/s per solar mass scaling), and Schwarzschild Hawking temperature. These are model-derived reference quantities, not directly observed measurements; the Hawking temperature is formal for astrophysical holes and ignores accretion/environmental effects. Recompute with `scripts/add_bh_derived_quantities.py` using the project's Astropy environment.

## Open research problems

- [Early supermassive black-hole growth](premium/early_smbh_growth.md) — high-redshift observations, Eddington-growth derivations, and conditional seed-mass scenarios ([notebook](notebooks/23_early_smbh_growth.ipynb)).
- [Quantum gravity](premium/quantum_gravity.md) — Planck-scale derivations, low-energy effective theory, candidate approaches, and model-dependent tests ([notebook](notebooks/24_quantum_gravity.ipynb)).

## Models implemented

- Schwarzschild: Rs, Hawking T, ISCO, photon sphere
- Kerr: outer horizon vs spin, ISCO vs spin
- Morris-Thorne wormhole: shape function b(r), metric components, flare-out, embedding
- White hole: time-reversed Schwarzschild + negative-mass demo, Hawking analog
- Hawking radiation: power, lifetime

## Notes

White holes and wormholes are hypothetical; no direct observational evidence. Models are pedagogical first-pass.
```
## GitHub Pages (online čtení)

Složka `docs/` obsahuje HTML export všech notebooků. Na GitHubu:
1. Vytvořte nový repozitář a pushněte tento projekt.
2. Settings → Pages → Source: `Deploy from a branch` → Branch `main` → Folder `/docs`.
3. Po pár minutách bude dostupné na `https://<user>.github.io/<repo>/`.

Lokálně lze otevřít `docs/index.html`.
