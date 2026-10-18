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
│   └── 04_white_hole_instability.ipynb
├── scripts/          # download + build scripts
├── figures/
└── reports/
```

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
