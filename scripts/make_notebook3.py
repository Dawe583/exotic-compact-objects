#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "03_data_exploration.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Data Exploration – GWOSC & HEASARC Compact Objects

Quick exploration of downloaded catalogs.
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print('ok')""")

md("## GWOSC GWTC")
code("""gw = pd.read_csv(ROOT/'data/processed/gwosc_gwtc.csv')
print('events:', len(gw))
print(gw['catalog'].value_counts())
m = gw['total_mass_source_msun'].dropna()
print('mass non-null:', len(m))
plt.figure(figsize=(8,5))
plt.hist(m, bins=40, color='#335c99', edgecolor='white')
plt.xlabel('Total mass (Msun)'); plt.ylabel('Events'); plt.title('GWTC total mass'); plt.grid(True, alpha=0.3); plt.show()""")

md("## AGN black hole masses (reverberation mapping)")
code("""agn = pd.read_csv(ROOT/'data/external/agn_bh_mass.csv', skiprows=2)
print('AGN BH masses:', len(agn))
print(agn.head())
print('log M_BH range:', agn['log M_BH'].min(), agn['log M_BH'].max())
plt.figure(figsize=(8,5))
plt.hist(agn['log M_BH'], bins=20, color='#995c33', edgecolor='white')
plt.xlabel('log10 M_BH (Msun)'); plt.ylabel('Objects'); plt.title('AGN BH mass distribution'); plt.grid(True, alpha=0.3); plt.show()""")

md("## HEASARC catalogs")
code("""for name in ['xrbcat','m87cxo','sgraregcsc','ulxrbcat','dxrbs','ulxngcat','vlulxcat','chanulxcat','snrgreen','pulsar']:
    p = ROOT/'data/external'/f'{name}.csv'
    if p.exists():
        d = pd.read_csv(p)
        print(name, d.shape)""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
