#!/usr/bin/env python3
"""Plot observed dynamical BlackCAT masses without converting upper/lower limits to detections."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/processed/blackcat_dynamical.csv')
fig=make_subplots(rows=2,cols=2,subplot_titles=('Dynamical mass estimates and limits','Mass function vs orbital period','Distance and black-hole mass','Companion radial-velocity amplitudes'))
x=df.mass_msun_text; flags=df.mass_limit_flag.fillna('').astype(str).str.strip()
# Limits rendered with distinct symbols and legend groups; quoted asymmetric measurement errors shown only where explicitly present.
for flag,mask,symbol,name in [('',flags.eq(''),'circle','reported mass estimate'),('>',flags.str.strip().eq('>'),'triangle-right','lower limit'),('>=',flags.str.strip().eq('>='),'triangle-right-open','lower/equal limit'),('>~',flags.str.strip().eq('>~'),'triangle-right','approximate lower limit'),('<=',flags.str.strip().isin(['<=','<']),'triangle-left','upper limit')]:
 q=df[mask]
 if q.empty: continue
 fig.add_trace(go.Scatter(x=q.Name,y=q.mass_msun_text,mode='markers',name=name,marker=dict(symbol=symbol,size=11),error_y=dict(type='data',symmetric=False,array=q.mass_error_upper_msun.fillna(0),arrayminus=q.mass_error_lower_msun.fillna(0),visible=True),customdata=q[['mass_limit_flag','mass_function_msun','distance_kpc','orbital_period_hours','dynamical_refs']].fillna('not reported'),hovertemplate='<b>%{x}</b><br>Catalog mass: %{y} M☉<br>Limit flag: %{customdata[0]}<br>Mass function: %{customdata[1]} M☉<br>Distance: %{customdata[2]} kpc<br>Orbital period: %{customdata[3]} h<br>Refs: %{customdata[4]}<extra></extra>'),row=1,col=1)
fig.add_trace(go.Scatter(x=df.orbital_period_hours,y=df.mass_function_msun,mode='markers',name='mass function',text=df.Name,customdata=df[['mass_msun_text','mass_limit_flag','dynamical_refs']],hovertemplate='<b>%{text}</b><br>P=%{x:.3g} h<br>f(M)=%{y:.3g} M☉<br>M_BH catalog=%{customdata[0]} %{customdata[1]}<br>Refs: %{customdata[2]}<extra></extra>',marker=dict(color='#54d6c5',size=10),showlegend=False),row=1,col=2)
fig.add_trace(go.Scatter(x=df.distance_kpc,y=df.mass_msun_text,mode='markers',name='distance',text=df.Name,customdata=df[['mass_limit_flag','dynamical_refs']],hovertemplate='<b>%{text}</b><br>Distance=%{x} kpc<br>Mass=%{y} M☉ %{customdata[0]}<br>Refs: %{customdata[1]}<extra></extra>',marker=dict(color='#a86eff',size=10),showlegend=False),row=2,col=1)
fig.add_trace(go.Scatter(x=df.Name,y=df.companion_rv_amplitude_km_s,mode='markers',name='K₂',text=df.dynamical_refs,hovertemplate='<b>%{x}</b><br>K₂=%{y} km/s<br>Refs: %{text}<extra></extra>',marker=dict(color='#ffb454',size=10),showlegend=False),row=2,col=2)
fig.update_yaxes(title_text='Mass M₁ (M☉)',row=1,col=1); fig.update_xaxes(tickangle=-60,row=1,col=1)
fig.update_xaxes(title_text='Orbital period (h)',type='log',row=1,col=2); fig.update_yaxes(title_text='Mass function f(M) (M☉)',row=1,col=2)
fig.update_xaxes(title_text='Distance (kpc)',row=2,col=1); fig.update_yaxes(title_text='Mass M₁ (M☉)',row=2,col=1)
fig.update_xaxes(tickangle=-60,row=2,col=2); fig.update_yaxes(title_text='Companion RV amplitude K₂ (km/s)',row=2,col=2)
fig.update_layout(template='plotly_dark',height=950,title='BlackCAT dynamical stellar-mass black-hole systems',hovermode='closest',annotations=list(fig.layout.annotations)+[dict(text='Primary source: Corral-Santana et al. 2016, BlackCAT, CDS/VizieR J/A+A/587/A61 (DOI 10.26093/cds/vizier.35870061). Sample is the published dynamical subset (18 entries); mass-limit symbols are retained. Period/velocity and published mass function may use distinct source analyses; audit against cited papers. Not volume-complete.',xref='paper',yref='paper',x=0,y=-.16,showarrow=False,align='left',font=dict(color='#bbb',size=12))],margin=dict(b=150))
out=ROOT/'premium/figures/blackcat_dynamical.html'; out.parent.mkdir(parents=True,exist_ok=True); fig.write_html(out,include_plotlyjs='cdn'); print(out)
