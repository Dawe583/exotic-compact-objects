#!/usr/bin/env python3
"""Build theoretical/synthetic datasets for BH, wormholes, white holes."""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from astropy import constants as const
from astropy import units as u

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "processed"
OUT.mkdir(parents=True, exist_ok=True)

# Known compact objects catalog (literature values, approximate)
known = [
    ("Sagittarius A*", "black_hole", 4.1e6, "supermassive", "Milky Way center"),
    ("M87*", "black_hole", 6.5e9, "supermassive", "M87 jet"),
    ("Cygnus X-1", "black_hole", 21.2, "stellar", "X-ray binary"),
    ("GW150914 final", "black_hole", 62.0, "stellar", "GW merger remnant"),
    ("GW190521 final", "black_hole", 142.0, "intermediate", "GW merger remnant"),
    ("TON 618", "black_hole", 6.6e10, "supermassive", "quasar"),
    ("Phoenix A*", "black_hole", 1.0e10, "supermassive", "BCG"),
    ("Morris-Thorne wormhole (demo)", "wormhole", 1.0, "theoretical", "hypothetical throat mass scale"),
    ("Ellis drainhole (demo)", "wormhole", 0.0, "theoretical", "massless throat"),
    ("White hole (time-reversed demo)", "white_hole", 10.0, "hypothetical", "theoretical only"),
]
df = pd.DataFrame(known, columns=["name", "object_type", "mass_msun", "class", "note"])
df.to_csv(OUT / "known_compact_objects.csv", index=False)
df.to_json(OUT / "known_compact_objects.json", orient="records", indent=2)

# Physical constants table
consts = {
    "G": float(const.G.value),
    "c": float(const.c.value),
    "hbar": float(const.hbar.value),
    "k_B": float(const.k_B.value),
    "M_sun": float(const.M_sun.value),
    "G_unit": str(const.G.unit),
    "c_unit": str(const.c.unit),
}
(Path(OUT / "constants.json")).write_text(json.dumps(consts, indent=2))

# Parameter grids for models
mass_grid = np.logspace(0, 10, 200)  # Msun
np.save(OUT / "mass_grid_msun.npy", mass_grid)

# Wormhole throat radius grid (km) for Morris-Thorne demo: b0 in km
b0_grid = np.logspace(-1, 6, 100)
np.save(OUT / "wormhole_b0_grid_km.npy", b0_grid)

# White hole: time-reversed mass grid (same as mass grid) + negative mass demo
neg_mass_grid = -np.logspace(0, 6, 50)
np.save(OUT / "whitehole_negative_mass_grid_msun.npy", neg_mass_grid)

print("Theoretical data written to", OUT)
