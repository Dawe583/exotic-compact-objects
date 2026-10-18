#!/usr/bin/env python3
"""Parse and join the published BlackCAT CDS/VizieR tables into a clean dynamical sample."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
EXT=ROOT/'data/external'; OUT=ROOT/'data/processed/blackcat_dynamical.csv'
def read_table(name):
    path=EXT/f'blackcat_{name}.tsv'
    frame=pd.read_csv(path,sep='\t',comment='#',dtype=str)
    # VizieR appends a units row and a fixed-width separator after the header.
    frame=frame.iloc[2:].copy()
    if 'Name' in frame: frame['Name']=frame.Name.str.strip()
    return frame
ast=read_table('tablea1').rename(columns={'Year':'discovery_year','RAJ2000':'ra_j2000','DEJ2000':'dec_j2000','GLON':'galactic_lon_deg','GLAT':'galactic_lat_deg','Dist':'distance_kpc','e_Dist':'distance_error_kpc','Noutb':'outbursts_after_discovery','Refs':'astrometry_refs'})
phot=read_table('tablea2').rename(columns={'FX':'peak_xray_flux_2_10_keV','magOut':'outburst_magnitude','Porb':'photometric_period_hours','e_Porb':'photometric_period_error_hours','Refs':'photometry_refs'})
dyn=read_table('tablea4').rename(columns={'M1':'mass_msun_text','E_M1':'mass_error_upper_msun','e_M1':'mass_error_lower_msun','M1u':'mass_interval_upper_msun','l_M1':'mass_limit_flag','f(M1)':'mass_function_msun','e_f(M1)':'mass_function_error_msun','i':'inclination_deg','e_i':'inclination_error_deg','Porb':'orbital_period_hours','e_Porb':'orbital_period_error_hours','K2':'companion_rv_amplitude_km_s','e_K2':'companion_rv_error_km_s','q':'mass_ratio','Ref':'dynamical_refs'})
keep_ast=['Name','discovery_year','ra_j2000','dec_j2000','galactic_lon_deg','galactic_lat_deg','distance_kpc','distance_error_kpc','outbursts_after_discovery','astrometry_refs']
keep_phot=['Name','peak_xray_flux_2_10_keV','outburst_magnitude','photometric_period_hours','photometric_period_error_hours','photometry_refs']
result=dyn.merge(ast[keep_ast],on='Name',how='left').merge(phot[keep_phot],on='Name',how='left')
for col in ['mass_msun_text','mass_error_upper_msun','mass_error_lower_msun','mass_interval_upper_msun','mass_function_msun','mass_function_error_msun','inclination_deg','inclination_error_deg','orbital_period_hours','orbital_period_error_hours','companion_rv_amplitude_km_s','companion_rv_error_km_s','mass_ratio','distance_kpc','distance_error_kpc','peak_xray_flux_2_10_keV','outburst_magnitude','photometric_period_hours','photometric_period_error_hours','discovery_year','outbursts_after_discovery']:
    result[col]=pd.to_numeric(result[col],errors='coerce')
result['source_catalog']='BlackCAT dynamical sample, VizieR J/A+A/587/A61/tablea4'
result['catalog_doi']='10.26093/cds/vizier.35870061'
result['catalog_url']='https://cdsarc.cds.unistra.fr/viz-bin/cat/J/A+A/587/A61'
result['mass_units']='solar masses'; result['distance_units']='kpc'; result['period_units']='hours'
if len(result)!=18 or result.Name.duplicated().any(): raise RuntimeError(f'Unexpected dynamical sample rows/duplicates: {len(result)}')
OUT.parent.mkdir(parents=True,exist_ok=True); result.to_csv(OUT,index=False); print(f'Wrote {len(result)} sources to {OUT}')
