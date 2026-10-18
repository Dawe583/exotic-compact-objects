#!/usr/bin/env python3
"""Build an interactive dashboard from the curated recent GWTC remnant sample."""
from pathlib import Path
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
ROOT=Path(__file__).resolve().parents[1]
df=pd.read_csv(ROOT/'data/processed/gwtc_recent_20_remnants.csv')
out=ROOT/'premium/figures/gwtc_recent_20_remnants.html'
fig=make_subplots(rows=2,cols=2,subplot_titles=('Remnant mass and catalog uncertainty','Component masses','Effective spin versus remnant mass','Distance versus remnant mass'))
lo=df.final_mass_source_msun+df.final_mass_source_lower
hi=df.final_mass_source_msun+df.final_mass_source_upper
hover=[]
for r in df.itertuples():
    lower=r.final_mass_source_msun+r.final_mass_source_lower if pd.notna(r.final_mass_source_lower) else float('nan')
    upper=r.final_mass_source_msun+r.final_mass_source_upper if pd.notna(r.final_mass_source_upper) else float('nan')
    hover.append(f'<b>{r.event_id}</b><br>{r.catalog}<br>Remnant source mass {r.final_mass_source_msun:.2f} M☉ [{lower:.2f}, {upper:.2f}]<br>Components {r.mass_1_source_msun:.2f}, {r.mass_2_source_msun:.2f} M☉<br>Distance {r.luminosity_distance_mpc} Mpc<br>χ_eff {r.chi_eff}<br>P_astro {r.p_astro}<br><a href="{r.source_url}">GWOSC source</a>')
fig.add_trace(go.Scatter(x=df.event_id,y=df.final_mass_source_msun,mode='markers',name='Merger remnant',error_y=dict(type='data',symmetric=False,array=hi-df.final_mass_source_msun,arrayminus=df.final_mass_source_msun-lo,visible=True),text=hover,hovertemplate='%{text}<extra></extra>',marker=dict(color='#a86eff',size=10)),row=1,col=1)
fig.add_trace(go.Scatter(x=df.mass_1_source_msun,y=df.mass_2_source_msun,mode='markers',name='Binary components',text=hover,hovertemplate='%{text}<extra></extra>',marker=dict(color='#54d6c5',size=9)),row=1,col=2)
fig.add_trace(go.Scatter(x=df.final_mass_source_msun,y=df.chi_eff,mode='markers',name='Effective spin',text=hover,hovertemplate='%{text}<extra></extra>',marker=dict(color='#ffb454',size=10)),row=2,col=1)
fig.add_trace(go.Scatter(x=df.luminosity_distance_mpc,y=df.final_mass_source_msun,mode='markers',name='Distance',text=hover,hovertemplate='%{text}<extra></extra>',marker=dict(color='#6bb6ff',size=10)),row=2,col=2)
fig.update_xaxes(title_text='Event (ordered by GPS time)',tickangle=-55,row=1,col=1)
fig.update_xaxes(title_text='Primary source-frame mass (M☉)',row=1,col=2); fig.update_yaxes(title_text='Secondary source-frame mass (M☉)',row=1,col=2)
fig.update_xaxes(title_text='Remnant source-frame mass (M☉)',row=2,col=1); fig.update_yaxes(title_text='χ_eff',range=[-1,1],row=2,col=1)
fig.update_xaxes(title_text='Luminosity distance (Mpc)',type='log',row=2,col=2); fig.update_yaxes(title_text='Remnant source-frame mass (M☉)',row=2,col=2)
fig.update_layout(template='plotly_dark',height=950,title='20 Recent GWTC Binary-Black-Hole Merger Remnants',hovermode='closest',annotations=list(fig.layout.annotations)+[dict(text='Latest 20 distinct GWTC-4.1/GWTC-5.0 catalog entries with reported remnant mass. These are merger remnants, not 20 isolated black holes. Error bars use the catalog signed asymmetric deltas. This convenience selection is not population-unbiased.',xref='paper',yref='paper',x=0,y=-0.17,showarrow=False,font=dict(size=12,color='#bbb'),align='left')],margin=dict(b=140))
out.parent.mkdir(parents=True,exist_ok=True); fig.write_html(out,include_plotlyjs='cdn'); print(out)
