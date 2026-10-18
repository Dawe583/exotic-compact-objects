#!/usr/bin/env python3
"""Generate reproducible visualization/model summary for AGN reverberation masses."""
from pathlib import Path
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/processed/agn_reverberation_masses.csv'
OUT=ROOT/'premium/figures/agn_reverberation_catalog.html'
df=pd.read_csv(DATA).dropna(subset=['log10_mass_msun']).copy()
fig=make_subplots(rows=2,cols=2,subplot_titles=('Mass estimates with asymmetric 1σ-like reported intervals','Mass versus redshift','Mass distribution','Measurement precision (log-space)'))
hover=[f'<b>{r.name}</b><br>log₁₀(M/M☉)={r.log10_mass_msun:.3f}<br>M={r.mass_msun:.3g} M☉<br>z={r.redshift}<br>Method: reverberation-mapping compilation' for r in df.itertuples()]
fig.add_trace(go.Scatter(x=df.name,y=df.mass_msun,mode='markers',name='AGN mass',text=hover,hovertemplate='%{text}<extra></extra>',error_y=dict(type='data',symmetric=False,array=df.mass_upper_delta_msun,arrayminus=df.mass_lower_delta_msun,visible=True),marker=dict(color='#ff8c69',size=8)),row=1,col=1)
fig.add_trace(go.Scatter(x=df.redshift,y=df.log10_mass_msun,mode='markers',name='AGN versus z',text=hover,hovertemplate='%{text}<extra></extra>',marker=dict(color=df.log10_mass_msun,colorscale='Plasma',size=9)),row=1,col=2)
fig.add_trace(go.Histogram(x=df.log10_mass_msun,nbinsx=18,name='Counts',marker_color='#a86eff'),row=2,col=1)
fig.add_trace(go.Scatter(x=df.log10_mass_msun,y=df.logmass_upper_error_dex,mode='markers',name='Upper log-mass error',text=hover,hovertemplate='%{text}<br>Upper error=%{y:.3f} dex<extra></extra>',marker=dict(color='#54d6c5',size=8)),row=2,col=2)
fig.update_yaxes(type='log',title_text='Mass (M☉)',row=1,col=1); fig.update_xaxes(title_text='AGN name',tickangle=-70,row=1,col=1)
fig.update_xaxes(title_text='Redshift z',row=1,col=2); fig.update_yaxes(title_text='log₁₀(M/M☉)',row=1,col=2)
fig.update_xaxes(title_text='log₁₀(M/M☉)',row=2,col=1); fig.update_yaxes(title_text='Object count',row=2,col=1)
fig.update_xaxes(title_text='log₁₀(M/M☉)',row=2,col=2); fig.update_yaxes(title_text='Reported upper uncertainty (dex)',row=2,col=2)
fig.update_layout(template='plotly_dark',height=1000,title='AGN Black-Hole Reverberation-Mapping Mass Compilation',showlegend=False,annotations=list(fig.layout.annotations)+[dict(text=f'{len(df)} of 86 rows have numeric mass measurements. Error bars are converted from reported log10 dex offsets: ΔM−=M(1−10^(−σ−)); ΔM+=M(10^(σ+)−1). Compilation values are method-dependent and not a homogeneous, selection-corrected sample.',xref='paper',yref='paper',x=0,y=-.15,showarrow=False,align='left',font=dict(color='#bbb',size=12))],margin=dict(b=150))
OUT.parent.mkdir(parents=True,exist_ok=True); fig.write_html(OUT,include_plotlyjs='cdn'); print(f'{OUT}; plotted {len(df)} objects')
