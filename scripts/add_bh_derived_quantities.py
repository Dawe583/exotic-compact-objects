#!/usr/bin/env python3
"""Add SI/astrophysical derived quantities with Astropy units; source catalog values remain intact."""
from pathlib import Path
import numpy as np
import pandas as pd
from astropy import constants as c, units as u
ROOT=Path(__file__).resolve().parents[1]
FILES=[(ROOT/'data/processed/agn_reverberation_masses.csv','mass_msun'),(ROOT/'data/processed/gwtc_recent_20_remnants.csv','final_mass_source_msun')]
for path,col in FILES:
 d=pd.read_csv(path); mass=pd.to_numeric(d[col],errors='coerce').to_numpy()*u.Msun
 d['schwarzschild_radius_km']=(2*c.G*mass/c.c**2).to_value(u.km)
 d['eddington_luminosity_erg_s']=(1.26e38*d[col])
 d['schwarzschild_hawking_temperature_K']=(c.hbar*c.c**3/(8*np.pi*c.G*mass*c.k_B)).to_value(u.K)
 d.to_csv(path,index=False)
 print(path.name,len(d),'derived quantities added')
