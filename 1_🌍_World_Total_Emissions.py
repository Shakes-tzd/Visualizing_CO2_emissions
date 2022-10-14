import streamlit as st
# Manipulation Libraries
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from modules.gen_color import *
import time
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Carbon Footprint",
    page_icon="🌐",
    layout="wide"
)
components.html("<h1>Total CO<sub>2</sub> Emissions by Country since 1970</h1>")
# st.title("Total Carbon dioxide Emissions by Country since 1970")
# @st.cache # This function will be cached
def get_data():
    return pd.read_csv("energy_use_data_11-29-2021.csv")
energy = get_data()
energy.sort_values(by=['Year'], inplace=True)
# Rename some Areas
energy["Area"] = energy["Area"].replace(to_replace=["United States of America"],
                                        value=["United States"])
years=energy.Year.unique().tolist()

#define the last year in the data
if 'end_year' not in st.session_state:
    st.session_state['end_year'] = 2019


if 'play' not in st.session_state:
    st.session_state['play'] = False
def play():
    st.session_state['end_year']=1971
    st.session_state['play'] = True
options = st.select_slider(
'Select the range of years that to visualize?',
options=years,value=(min(years),st.session_state['end_year']))

# visualize the total emissions by year
df_energy=energy[(energy.Year>=options[0]) & (energy.Year<=options[1])].reset_index(drop=True)
df_energy=df_energy[df_energy['Area']!="China, mainland"]
df_energy=df_energy.groupby(["Area"])["Value"].sum().reset_index()
df_energy['iso_alpha'] = df_energy['Area'].apply(lambda x: energy[energy["Area"]==x]['Area Code (ISO3)'].iloc[0])
df_energy.sort_values(by=['Value'],ascending=False, inplace=True)
y=df_energy['Value'][:20]
x = df_energy['Area'][:20]

title = "<b>CO2 Emissions by Country</b> "
semi_wgyr= semi_wgyr_cmap()
if 'top_10' not in st.session_state:
    st.session_state['top_10'] = df_energy['Area'][:10]
fig = make_subplots(
    rows=2, cols=1,
    row_heights=[1, 1],
    specs=[[{"type": "choropleth"}],[{"type": "bar"}]],
    vertical_spacing=0)

# Add scattergeo globe map of volcano locations
fig.add_trace(go.Bar(
    x=x,
    y=y,
    text=y,
    texttemplate='%{text:.2s}', 
    textposition='outside',
    marker={'color': y,
            'colorscale': semi_wgyr,
            }), 
              # marker color can be a single color value or an iterable
    row=2, col=1
)

# Add locations bar chart
fig.add_trace(
    go.Choropleth( 
                    locations=df_energy['iso_alpha'],
                    z=df_energy['Value'].astype(float), # lifeExp is a column of gapminder
                    # hover_name=df_asgm_air_hg["Country"],
                    colorscale = semi_wgyr,#'Reds',
                    colorbar={"title": 'Emissions (Tons)'}
                    
                    
                    
                    ),
    row=1, col=1
)


# Add 3d surface of volcano
fig.update_traces(marker_cmax=df_energy['Value'].max(), selector=dict(type='bar'))
fig.update_traces(marker_cmin=df_energy['Value'].min(), selector=dict(type='bar'))
# fig.update_traces(marker_colorbar_title_text="Emissions (Million Tons)")

# Update geo subplot properties
fig.update_layout(
    # title="Plot Title",
    xaxis_title="Top 20 Emitting Countries",
    yaxis_title="CO2 Emissions (Tons)",
    
)
fig.update_geos(
    projection_type="natural earth",
    fitbounds="locations", 
    visible=False,
    showcountries=True,
    resolution=110, 
)


# Rotate x-axis labels
fig.update_xaxes(tickangle=35)

# Set theme, margin, and annotation in layout
fig.update_layout(
    autosize=True,
     width=1200,
     height=800,
    template="plotly_white",
    margin={"r":0,"t":0,"l":0,"b":0},
    yaxis =  {'showgrid': False} 
)
# fig.update_yaxes(range=[0,145])
fig.update_coloraxes(
    cmax=df_energy['Value'].max(),
    cmin=df_energy['Value'].min(),
    
    colorbar_dtick=10,
    colorbar_tick0=0
    
)
fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
fig.update_layout(coloraxis=dict(colorscale=semi_wgyr,))
# fig.update_coloraxes(colorscale=semi_wgyr,colorbar_title_text="Hg (t/y)")
# fig_name='07-14-22_gma2018_asgm-emmiting-countries.pdf'
# path=fig_path+fig_name
# fig.write_image(path)
st.plotly_chart(fig, use_container_width=True)
play=st.button("Play",on_click=play)#, on_click=set_end_year)
#  st.button("Play"):#:
#         for year in range(1971, 2020):
            
#             st.session_state['end_year'] = year
#             time.sleep(0.5)
#             st.experimental_rerun()
if st.session_state['play'] and st.session_state['end_year']<2019:
    st.session_state['end_year'] += 1
    time.sleep(0.3)
    st.experimental_rerun()    

if st.session_state['end_year']>=2019:
    st.session_state['play'] = False
# st.session_state['play'] 
# st.session_state['end_year']    