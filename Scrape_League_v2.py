# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 16:48:48 2021

@author: Felix Trepanier
"""
from yahoo_oauth import OAuth2
import xml.etree.ElementTree as ET 
import re
import pandas as pd

oauth = OAuth2(None,None,from_file = 'C:/Users/Felix Trepanier/Desktop/Fantasy Hockey/oauth.json')
#if oauth.token_is_valid() == False:
#​    oauth.refresh_access_token()



df_full = pd.DataFrame()

for team_num in range(1,9,1):
    url_matchups = "https://fantasysports.yahooapis.com/fantasy/v2/team/403.l.51114.t."+str(team_num)+"/matchups;weeks=1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16"
    r = oauth.session.get(url_matchups)
    if r.status_code == 200:
        print('Connection status for team {} is ok'.format(str(team_num)))
        
    # Convert to string and remove namespace. Parse the string and return root element of Tree 
    xmlstring = r.text
    xmlstring = re.sub(' xmlns="[^"]+"', '', xmlstring, count=1)
    root = ET.fromstring(xmlstring)
    
    # Getting the main team name
    main_team_name = []
    for content in root:
        for team in content:
            main_team_name = main_team_name + [team.text]
    main_team_name = main_team_name[2]
    
    ## Getting the data in long form from the XML file
    df = pd.DataFrame()
    for matchup in root.findall("./team/matchups/"):
        for week in matchup.findall("week"):
            week_num = int(week.text)
        for week_s in matchup.findall("week_start"):
            week_start = week_s.text
        for week_e in matchup.findall("week_end"):
            week_end = week_e.text
        for playoffs in matchup.findall("is_playoffs"):
            is_playoffs = playoffs.text
        for consolation in matchup.findall("is_consolation"):
            is_consolation = consolation.text
        for teams in matchup.findall("./teams/"):
            for t_name in teams.findall('name'):
                team_name = t_name.text
            for t_id in teams.findall('team_id'):
                team_id = t_id.text
            for team_stats in teams.findall("./team_stats/stats/"):
                for s_id in team_stats.findall('stat_id'):
                    stat_id = s_id.text
                for s_value in team_stats.findall('value'):
                    stat_value = s_value.text
    
    
                df_temp = pd.DataFrame(data = {'week_num':[week_num],
                                               'week_start':[week_start],
                                               'week_end':[week_end],
                                               'is_playoffs':[is_playoffs],
                                               'is_consolation':[is_consolation],
                                               'team_name':[team_name],
                                               'team_id':[team_id],
                                               'stat_id':[stat_id],
                                               'stat_value':[stat_value]})
                df = df.append(df_temp)
    
    del df_temp,week_num,week_start,week_end,is_playoffs,is_consolation,team_name,team_id,stat_id,stat_value
    
    
    ## Creating a dataframe for each stat
    stat_ids = df.stat_id.unique()
    
    
    list_df = []
    for i in range(0,len(stat_ids)):
        list_df = list_df + [df[df.stat_id == stat_ids[i]]]
        list_df[i] = list_df[i].rename(columns={'stat_value':'stat_'+stat_ids[i]})
        list_df[i] = list_df[i].drop(['stat_id'],axis=1)
    
    
    ## Joining all those dataframes together
    for i in range(0,len(list_df)):
        if i == 0:
            df_wide = list_df[i]
        else:
            df_wide = pd.merge(df_wide,list_df[i],on = ['is_consolation', 'is_playoffs', 'team_id','team_name', 'week_end', 'week_num', 'week_start'])
    del i, list_df
    
    
    ## Creating a dataframe for each main team and opponent and joining it back
    df_main = df_wide[df_wide.team_name == main_team_name]
    df_opponent = df_wide[df_wide.team_name != main_team_name]
    
    df_full_temp = pd.merge(df_main,df_opponent,on = ['is_consolation', 'is_playoffs','week_end', 'week_num', 'week_start'],suffixes=('', '_opponent'))
    
    ## Adding all team dataframes together
    df_full = df_full.append(df_full_temp)
    
    print('Dataframe for team {} added successfully'.format(str(team_num)))
    
del df,df_full_temp,df_main,df_opponent,df_wide,main_team_name,stat_ids,team_num,url_matchups,xmlstring