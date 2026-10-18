#!/usr/bin/env python3
import nbformat as nbf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
NB = ROOT / "notebooks" / "11_data_synthesis.ipynb"
nb = nbf.v4.new_notebook()
cells = []
def md(t): cells.append(nbf.v4.new_markdown_cell(t))
def code(t): cells.append(nbf.v4.new_code_cell(t))

md("""# Data Synthesis – Black Hole Populations

Combine GWOSC, AGN reverberation masses, and dynamically discovered stellar BHs.
""")

code("""import sys
from pathlib import Path
ROOT = Path('/home/dawe/Projects/astro-science/research/projects/exotic-compact-objects')
sys.path.insert(0, str(ROOT))
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
print('ok')""")

code("""# GWOSC masses
gw = pd.read_csv(ROOT/'data/processed/gwosc_gwtc.csv')
m_gw = gw['total_mass_source_msun'].dropna()
# AGN
agn = pd.read_csv(ROOT/'data/external/agn_bh_mass.csv', skiprows=2)
m_agn = 10**pd.to_numeric(agn['log M_BH'], errors='coerce')
# black_melody
bm = pd.read_csv(ROOT/'data/external/black_melody.csv')
m_bm = pd.to_numeric(bm['MBH_Msun'].astype(str).str.extract(r'([\d\.]+)')[0], errors='coerce').dropna()
print('GWOSC n=', len(m_gw), 'AGN n=', len(m_agn), 'BH melody n=', len(m_bm))""")

code("""plt.figure(figsize=(9,5))
plt.hist(np.log10(m_gw), bins=30, alpha=0.6, label='GWOSC')
plt.hist(np.log10(m_agn), bins=20, alpha=0.6, label='AGN')
if len(m_bm)>0:
    plt.hist(np.log10(m_bm), bins=10, alpha=0.6, label='BH melody')
plt.xlabel('log10 M (Msun)'); plt.ylabel('Count'); plt.legend()
plt.title('Black hole mass distributions (different probes)')
plt.grid(True, alpha=0.3)
plt.savefig(str(ROOT/'figures'/'bh_mass_distributions.png'), dpi=150)
plt.show()""")

md("## HEASARC counts")
code("""import glob, os
for p in sorted(glob.glob(str(ROOT/'data/external/*.csv'))):
    try:
        d=pd.read_csv(p)
        print(os.path.basename(p), d.shape)
    except Exception as e:
        print(os.path.basename(p), 'ERR', e)""")

nb['cells'] = cells
NB.parent.mkdir(parents=True, exist_ok=True)
with open(NB, 'w') as f:
    nbf.write(nb, f)
print('written', NB)
