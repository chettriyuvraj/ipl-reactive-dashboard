#tables modules contains all the dfs(tables) - created using functions from preprocess.py

import pandas as pd 
import numpy as np 
from .preprocess import load_dataset #to load dataset
from .preprocess import find_winner_runnerup_season #for visualization 1
from .preprocess import create_season_table,create_all_time_table #for visualization 2
#nothing required for 3rd and 4th visualization





df = load_dataset() #loading the df





#for 1st visualization - winners and runners up - creating two dictionaries with names of winners/runners-up of each season
def create_winners_runners_up_dictonary():
    dict_winners = {}
    dict_runners_up = {}
    for year in range(2008,2020):
        dict_winners[year],dict_runners_up[year] = find_winner_runnerup_season(year)
    return dict_winners,dict_runners_up





#for 2nd visualizaton 
def create_league_tables_dictonary(): #all time as well as per season
    dict_league_tables ={} #contains df with the league tables for each season as well as all-time table
    for year in range(2008,2020):
        dict_league_tables[year] = create_season_table(year)  #adding league table for each season
    dict_league_tables["All-time"] = create_all_time_table() #all time table - note the spelling and case in the key
    return dict_league_tables







#for 3rd visualization - creating a dictionary with year on year mvps
def create_mvp_dictonary():
    df_mvp=pd.pivot_table(df,
                values=['date'],
                index=['season','player_of_match'],
                aggfunc='count')
    #so this is a multiindex pivot table with all mom's YOY
    dict_mvp={}
    for year in range(2008,2020):
        mvp_table = df_mvp.query(f'season=={year}').sort_values(by='date',ascending=False)
        dict_mvp[year]=mvp_table
    return dict_mvp






# for 4th visualization - scatter geo for cities 

def create_city_matches_dictionary():#pivot table with all city matches count for all seasons
    df_city_count=pd.pivot_table(
    df,
    index=['season','city'],
    values=['date'],
    aggfunc='count',
    )

    city_tables_dict={} #dictionary with cities and corresponding df showing no of matches held
    for year in range(2008,2020):
        city_table = df_city_count.query(f'season=={year}').sort_values(by='date',ascending=False) 
        #'city_table' is a multi-index pivot table - let's convert it into a normal df 
        city_table = pd.DataFrame(city_table.to_records())
        city_table.rename(columns={'date':'matches'},inplace=True)
        city_tables_dict[year]=city_table

    return city_tables_dict




dict_winners,dict_runners_up = create_winners_runners_up_dictonary()

dict_league_tables = create_league_tables_dictonary()    

dict_mvp = create_mvp_dictonary()

city_tables_dict = create_city_matches_dictionary()
