import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd 
import numpy as np
from .preprocess import get_team_logo, all_time_league_table_visualization,per_season_league_table_visualization
from .preprocess import mvp_bar_chart,display_scatter_geo,add_coordinates_to_df

from .tables import dict_winners,dict_runners_up,dict_league_tables,dict_mvp,city_tables_dict



def winners_visualization():
#Visualization 1 - winners and runners_up of each season
#Sliders which show the winners for each season along with their logo
    st.markdown("# Winners for each season:")
    season_year = st.slider(
            label="Select the year you want winner for",
            min_value=list(dict_winners.keys())[0],
            max_value=list(dict_winners.keys())[-1],
        )

    st.write(get_team_logo(dict_winners[season_year]))

def runners_up_visualization():
    st.markdown('# Runners-up for each season:')
    season_year = st.slider(
            label="Select the year you want runners-up for",
            min_value=list(dict_runners_up.keys())[0],
            max_value=list(dict_runners_up.keys())[-1],
        )

    st.write(get_team_logo(dict_runners_up[season_year]))











def league_table_visualization():
    #Visualization 2 - per season and all time league table + plus graphings for different things 

    st.markdown("# Per season and all-time league table:")
    select_table = st.selectbox(label="Select the format you want",options=["All-time","Per-season"])

    current_table = dict_league_tables['All-time']

    current_year = st.slider(
            label="Select the year you want data for:",
            min_value=list(dict_runners_up.keys())[0],
            max_value=list(dict_runners_up.keys())[-1], #start and end year can be taken from this since it will be same for all dashboards
        )

    if select_table == 'Per-season':
        current_table = dict_league_tables[current_year]

    #to select what we want displayed
    options_display = st.selectbox(label= 'What do you want to display?',options=('league table', 'wins', 'losses', 'points'))

    current_display_content = current_table #by default we display the league table

    

    if options_display!='league table':
        if select_table == 'All-time':
            current_display_content = all_time_league_table_visualization(current_table,options_display)
        else:
            if options_display=='wins':
                current_display_content = per_season_league_table_visualization(current_table,'winner') 
            else:
                current_display_content = per_season_league_table_visualization(current_table,options_display)       

        

    st.write(current_display_content)












def mvp_visualization():
    #Visualization 3 - Year on year player of the match 

    st.markdown("# Player of the match statistics:")

    current_year_potm  = st.slider(
            label="Select the year you want best-players for",
            min_value=list(dict_runners_up.keys())[0],
            max_value=list(dict_runners_up.keys())[-1],
        )

    st.write(mvp_bar_chart(dict_mvp,current_year_potm))







def matches_city_visualization():
#Visualization 4 - scatter-geo plots showing number of matches per city

    st.markdown("# Scatter-geo plots showing number of matches per-city per-season:")
    current_year_city = st.selectbox(label="Select the year you want",options=[year for year in range(2008,2020)])
    st.write(display_scatter_geo(city_tables_dict,current_year_city))


def add_spacing(number_of_spaces):
    for i in range(number_of_spaces):
        st.markdown("  ") #adding spacing

def display_about():
    st.markdown("# About.")
    st.write("Cloud deployment of a small capstone project as part of Kossine - Data Science track.")
    st.markdown("EDA and Visualization on an [IPL Dataset](https://www.kaggle.com/nowke9/ipldata) sourced from [Kaggle](https://www.kaggle.com/).")




def main():


    
    display_about_button = st.button(label='About')
    display_visualizations_button = st.button(label='Visualizations')

    if display_about_button==True: #if about button is pressed
        display_about()
    else: #if visualization button is pressed
        visualization_option = st.selectbox(label="Select the visualization you want to see!",options=['Winners of each season','Runners-up of each season','League-tables','MVP-year on year','Cities with most matches - year on year'])

        if visualization_option == 'Winners of each season':
            winners_visualization()
        
        elif visualization_option == 'Runners-up of each season':
            runners_up_visualization()
        
        elif visualization_option == 'League-tables':
            league_table_visualization()
        
        elif visualization_option == 'MVP-year on year':
            mvp_visualization()

        elif visualization_option == 'Cities with most matches - year on year':
            matches_city_visualization()    

    

    