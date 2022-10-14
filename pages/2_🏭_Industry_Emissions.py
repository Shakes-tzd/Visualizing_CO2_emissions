
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Carbon Dioxide Emissions",
    page_icon="🏭",
    layout="wide"
)



def play():
    if st.session_state['end_year'] >= 2019:
        st.session_state['end_year']=1971
    st.session_state['play'] = True
def stop():
    st.session_state['play'] = False
components.html("<h1>Energy Industry CO<sub>2</sub> Emissions</h1><sup>")
# st.markdown("# co<sub>2</sub> Emissions per Energy Industry")
energy = pd.read_csv("energy_use_data_11-29-2021.csv")
energy.sort_values(by=['Year'], inplace=True)
# Rename some Areas
energy["Area"] = energy["Area"].replace(to_replace=["United States of America"],
                                        value=["United States"])
df_energy=energy[(energy.Year>=1971) & (energy.Year<=st.session_state['end_year'])].reset_index(drop=True)
df_energy=df_energy[df_energy['Area']!="China, mainland"]
df_energy=df_energy.groupby(["Area"])["Value"].sum().reset_index()
if 'top_10' not in st.session_state:
    st.session_state['top_10'] = df_energy['Area'][:10]
# Keep the same countries as in Graph 1
areas_to_keep = st.session_state['top_10']#["China","Germany", "Japan", "United States"]
years=energy.Year.unique().tolist()
energy = energy[(energy["Area"].isin(areas_to_keep)) & 
                (energy["Year"]==st.session_state['end_year'])].reset_index(drop=True)

# Rename some Areas
energy["Area"] = energy["Area"].replace(to_replace=["United States of America"],
                                        value=["United States"])

# Group by Area and Item
energy = energy.groupby(["Area", "Item"])["Value"].mean().reset_index()

# Compute percentage per country
totals = energy.groupby("Area")["Value"].sum().reset_index()
energy = pd.merge(energy, totals, on="Area")
energy["Perc"] = energy["Value_x"] / energy["Value_y"]
energy["Perc"] = energy["Perc"].apply(lambda x: round(x*100, 2))


title = f"<b>CO2 Emissions in {st.session_state['end_year']}</b><br><sup>Per Top 10 Emitting Countries and Energy Industries</sup>"
layout = go.Layout(width=980, height=600, plot_bgcolor="white", paper_bgcolor="white",
                   showlegend = False, 
                   title = {'text' : title, 'x':0.5, 'xanchor': 'center'}, 
                   font = {"color" : 'black'})
energy_text=energy[energy["Perc"]>10]
energy_text["Perc"]=energy_text["Perc"].apply(lambda x: str(x))
# Create the figure
fig = go.Figure( layout = layout)

# Create the base Scatter Plot
fig.add_trace(go.Scatter(
    # X and Y axis
    x=energy["Area"],
    y=energy["Item"],
    text=energy["Perc"],
    
    # The marker shape and size
    mode='markers',#'markers', 
    hovertemplate="Country: %{x}<br>" +
                  "Industry: %{y}<br>" +
                  "CO2 Emissions: %{marker.size:,}%" +
                  "<extra></extra>",
    
    marker=dict(color=energy["Perc"],
                size=energy["Perc"],
                showscale=True,
                colorbar=dict(title='%CO2<br>Emissions'),
                opacity=0.7,
                colorscale='Jet')
))
for i in range(len(energy_text)):
    if float(energy_text["Perc"].iloc[i])>45:
        f_size=16
    elif float(energy_text["Perc"].iloc[i])>36:
        f_size=12
    elif float(energy_text["Perc"].iloc[i])>20:
        f_size=9
    else:
        f_size=1
    fig.add_annotation(
            x=energy_text["Area"].iloc[i],
            y=energy_text["Item"].iloc[i],
            text=energy_text["Perc"].iloc[i]+"%",
            showarrow=False,
            font=dict(
                family="Arial",
                size=f_size,
                color="black"
            ),
        )
    
    

fig.update_xaxes(showline=True, linewidth=0.1, linecolor='#c9c4c3', gridcolor='#c9c4c3',
                 tickfont=dict(size=14, color='black'), 
                 title="", showgrid=True, tickangle=0)

fig.update_yaxes(showline=False, linewidth=0.1, gridcolor='#c9c4c3',
                 tickfont=dict(size=14, color='black'), 
                 title="", showgrid=True)
fig.update_layout({
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'paper_bgcolor': 'rgba(0,0,0,0)'
})
select_col,padding=st.columns([3,10])
with select_col:
    option = st.selectbox(
        'Choose a year',years)
    if st.session_state['play']==False:
        if option != st.session_state['end_year']:
                st.session_state['end_year']=option
                st.experimental_rerun() 
            
st.plotly_chart(fig, use_container_width=True)

play_col, stop_col,padding_col = st.columns([1,1,10])
with play_col:
    play_button = st.button('Play', on_click=play)
with stop_col:
    stop_button = st.button('Stop', on_click=stop)

    

if st.session_state['play'] and st.session_state['end_year']<2019:
    
    st.session_state['end_year'] += 1
    time.sleep(0.3)
    st.experimental_rerun()    

if st.session_state['end_year']>=2019:
    st.session_state['play'] = False