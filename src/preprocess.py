#this modules defines all functions for pre-processing of data to get tables in tables.py 

import pandas as pd 
import numpy as np 
import requests 
import plotly.express as px
from bs4 import BeautifulSoup #for scraping image url from wiki
from PIL import Image #displaying images 
import requests #getting data from url 
from urllib.request import urlopen #for displaying image
from .connect_to_google_drive import get_file

def load_dataset(): # module to load the dataset required 
    get_file('1S4Qq3FNbrNhcGME2oJaXhgVceeSuqnjJ')#get the csv file - running this script stores it in the directory
    df = pd.read_csv('matches_formatted.csv')
    
    return df 
 





''' First dashboard - winners and runners_up for each season'''

def find_winner_runnerup_season(season_year):  #function which returns winners and runners up if you give them the season year
    df_season_descending = df[df['season']==season_year].sort_values(by='date_datetime64',ascending=False)    #df in descending
    final_match = df_season_descending.iloc[0] #picking up the last match of the season
    season_winner = final_match['winner'] #winner of the last match of the season is the season winner, since last match=final
    if season_winner ==final_match['team1']:
        season_runnerup = final_match['team2']   # runner up is the OTHER team in the finals
    else:
        season_runnerup = final_match['team1']
    
    return season_winner,season_runnerup    #returns winner and runner up of the respective season


def get_team_logo(team_name):
    
    team_name = team_name.replace(' ','_')#replacing all spaces in team name with underscore 
    link = f'https://en.wikipedia.org/wiki/{team_name}' #this is the wikipedia page of the given team 
    page = requests.get(link)#getting all the html data from page using requests
    soup = BeautifulSoup(page.text,'html.parser') #all the data from the page as a BeautifulSoup object
    
    logo_link=soup.find_all('a',class_='image')[0] #getting the 'a' tag which has the logo link, from the page
    img_tag = logo_link.find_all('img') #getting img tag from 'a' tag
    img_src=img_tag[0].attrs['src']#this is the actual SOURCE attribute in the IMAGE tag which is inside the A tag
    
    img = Image.open(urlopen(f'https:{img_src}'))
    img = px.imshow(img)
    #print(img)
    img.update_layout(coloraxis_showscale=False)
    img.update_xaxes(showticklabels=False)
    img.update_yaxes(showticklabels=False)
    return img













'''Second visualization - graphs for per season and all time table'''



def create_all_time_table(): #function that returns  all time league table
    #Let's start with all time league table - we will consider wins losses and points 
    df_all_time_league_table = df['winner'].value_counts().reset_index()
    df_all_time_league_table['matches'] = 0 # matches column initialized - all values set to 0
    df_all_time_league_table.sort_values(ascending=True,by='index',inplace=True)

    team_1 = df['team1'].value_counts().reset_index() #df with no of times team is in column team1
    team_2 = df['team2'].value_counts().reset_index() #df with no of times team is in column team2
    team_1.sort_values(ascending=True,by='index',inplace=True)
    team_2.sort_values(ascending=True,by='index',inplace=True)
    for i in range(len(team_1)): #computing total matches 
        df_all_time_league_table.loc[i,'matches'] += team_1.loc[i,'team1']+team_2.loc[i,'team2'] #total no of matches = combination of the two

    #since no of matches played is diff for each team - let's compute the win percentage too for better context
    #2 more columns -> losses, win percentage 
    df_all_time_league_table['losses'] = df_all_time_league_table['matches']-df_all_time_league_table['winner']
    df_all_time_league_table['win_percentage'] = (df_all_time_league_table['winner']/df_all_time_league_table['matches'])*100
    df_all_time_league_table.sort_values(by='winner',ascending=False,inplace=True)#now let's arrange table according to win percentage

        #changing column names
    df_all_time_league_table.rename(columns={'index':'team','winner':'wins'},inplace=True)
    df_all_time_league_table['points']=df_all_time_league_table['wins']*2#also points column

    return df_all_time_league_table


def create_season_table(season_year):#returns league table for a particular season
 
    df_season = df[df['season']==season_year].sort_values(by='date_datetime64',ascending=False) #taking all matches of a season as a df
    if season_year<2011:
        df_season = df_season[3:] #removing semis and finals for league table computation
    else:
        df_season = df_season[4:]

    df_league_table = df_season['winner'].value_counts().reset_index() #converting the winners count into a df
    df_league_table['matches'] = 0 #adding a column for no of matches played
    df_league_table.rename(columns={'index':'team'},inplace=True) #renaming column

    df_team1 = df_season['team1'].value_counts().reset_index()
    df_team2 = df_season['team2'].value_counts().reset_index() #converting both to df
    df_team1.rename(columns={'index':'team','team1':'matches'},inplace=True)
    df_team2.rename(columns={'index':'team','team2':'matches'},inplace=True) #renaming columns


    for team in list(df_team1['team'].unique()):
            df_league_table.loc[df_league_table['team']==team,'matches'] = int(df_team1.loc[df_team1['team']==team,'matches'])+int(df_team2.loc[df_team2['team']==team,'matches'])

    
    #adding columns for losses points and win percentage
    df_league_table['losses'] = df_league_table['matches']-df_league_table['winner']    
    df_league_table['points'] = df_league_table['winner']*2
    df_league_table['win percentage'] = (df_league_table['winner']/df_league_table['matches'])*100
    df_league_table.sort_values(inplace=True,by=['points','losses'],ascending=[False,True])
    
    #changing name of winner column - to wins
    df_league_table.rename(columns={'winner':'wins'})
    
    return df_league_table

#for plotting visualizations for the per-season and all time league table

def all_time_league_table_visualization(df_all_time_league_table,parameter):
    #grouped bar chart 
    if parameter=='wins' or parameter=='losses':
        import plotly.graph_objects as go
        fig = go.Figure(data=[
            go.Bar(name=parameter, x=df_all_time_league_table['team'], y=df_all_time_league_table[parameter],text=df_all_time_league_table[parameter],textposition='auto'),
            go.Bar(name='matches', x=df_all_time_league_table['team'], y=df_all_time_league_table['matches'],text=df_all_time_league_table['matches'],textposition='auto')
        ])
        # Change the bar mode
        fig.update_layout(barmode='group')
        
    else:
        fig = px.bar(df_all_time_league_table,x='team',y=parameter,text=parameter)
        

    fig.update_layout(width=830,height=600)
    return fig

def per_season_league_table_visualization(league_table,parameter):
    #grouped bar chart 
    import plotly.graph_objects as go
    # league_table = league_tables[season_year] - league table will be given
    if parameter=='winner' or parameter=='losses':
        fig = go.Figure(data=[
            go.Bar(name=parameter, x=league_table['team'], y=league_table[parameter],text=league_table[parameter],textposition='auto'),
            go.Bar(name='matches', x=league_table['team'], y=league_table['matches'],text=league_table['matches'],textposition='auto')
        ])
        # Change the bar mode
        fig.update_layout(barmode='group')
        
    else:
        fig = px.bar(league_table,x='team',y=parameter,text=parameter)
     
    fig.update_layout(width=800,height=600)   
    return fig











'''Third visualization - for year-on-year MVP's bar chart'''


def mvp_bar_chart(mvp_tables,season_year): #takes in dictionary with yoy mvp's and gives out graphs
    df = pd.DataFrame(mvp_tables[season_year].to_records()) #converts the mvp table of that year to a df like the one below
    #note - no_of_awards is called date in this df
    fig = px.bar(df[0:8],x='player_of_match',y='date',text='date') #only top 8 players
    fig.update_traces(textposition='outside')
    fig.update_layout(uniformtext_minsize=15, uniformtext_mode='show')
    return fig










'''Fourth visualization - Scatter-geo for cities'''

def display_scatter_geo(city_tables_dict,season_year):
    fig = px.scatter_geo(add_coordinates_to_df(city_tables_dict[season_year]),lat='lat',lon='lng', color='city',hover_name='city',size='matches')
    return fig


def add_coordinates_to_df(df_cities):
    df_cities_clone=df_cities
    df_cities_clone['lat'] = 0
    df_cities_clone['lng'] = 0
    for i in range(len(df_cities)):
        city = df_cities.iloc[i]['city']
        latitude = df[df['city']==df_cities_clone.iloc[i]['city']].iloc[0]['lat']
        longitude = df[df['city']==df_cities_clone.iloc[i]['city']].iloc[0]['lng']
        df_cities_clone.loc[df_cities_clone['city']==city, 'lat']= latitude
        df_cities_clone.loc[df_cities_clone['city']==city, 'lng']= longitude
        
        
    return df_cities_clone
    






df = load_dataset() #loading the df