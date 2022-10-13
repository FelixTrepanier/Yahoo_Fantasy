from yahoo_oauth import OAuth2
import xml.etree.ElementTree as ET 
import re
import pandas as pd

class Scrape_League:
    """
    
    """
    def __init__(self, app_config):
        self.app_config = app_config
        self.oauth = OAuth2(
            None,
            None,
            from_file=self.app_config['secrets']['location']
        )

    def weeks_to_scrape(self, comlete_flag=True):
        """
        :param complete_flag: Only include completed weeks. Default is True.
        :return: A list of weeks to scrape
        """
        csv_location = self.app_config['data_config']['scrape_data_location']
        # if csv_location exist:

    def scrape(self, weeks):
        """
        Gather data from Yahoo Fantasy League and return it in a tabular format.
        :param scrape_range: Weeks to scrape
        :return: A Pandas dataframe containing the league data.
        """
        # get config
        league_id = self.app_config['league_config']['league_id']
        team_number = self.app_config['league_config']['team_number']

        # loop through for every team
        for team_num in range(1, team_number + 1):
            url_matchups = f'https://fantasysports.yahooapis.com/fantasy/v2/team/403.l.{league_id}.t.{team_num}/matchups;weeks={",".join([str(week) for week in weeks])}'
            r = self.oauth.session.get(url_matchups)
                
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
            
            # Getting the data in long form from the XML file
            df = pd.DataFrame()
            for matchup in root.findall('./team/matchups/'):
                for week in matchup.findall('week'):
                    week_num = int(week.text)
                for week_s in matchup.findall('week_start'):
                    week_start = week_s.text
                for week_e in matchup.findall('week_end'):
                    week_end = week_e.text
                for playoffs in matchup.findall('is_playoffs'):
                    is_playoffs = playoffs.text
                for consolation in matchup.findall('is_consolation'):
                    is_consolation = consolation.text
                for teams in matchup.findall('./teams/'):
                    for t_name in teams.findall('name'):
                        team_name = t_name.text
                    for t_id in teams.findall('team_id'):
                        team_id = t_id.text
                    for team_stats in teams.findall('./team_stats/stats/'):
                        for s_id in team_stats.findall('stat_id'):
                            stat_id = s_id.text
                        for s_value in team_stats.findall('value'):
                            stat_value = s_value.text
            
            
                        df_temp = pd.DataFrame(
                            {
                                'week_num':[week_num],
                                'week_start':[week_start],
                                'week_end':[week_end],
                                'is_playoffs':[is_playoffs],
                                'is_consolation':[is_consolation],
                                'team_name':[team_name],
                                'team_id':[team_id],
                                'stat_id':[stat_id],
                                'stat_value':[stat_value]
                            }
                        )
                        df = df.append(df_temp)            
            
            # Creating a dataframe for each stat
            stat_ids = df.stat_id.unique()
            
            list_df = []
            for i in range(0,len(stat_ids)):
                list_df = list_df + [df[df.stat_id == stat_ids[i]]]
                list_df[i] = list_df[i].rename(columns={'stat_value':'stat_'+stat_ids[i]})
                list_df[i] = list_df[i].drop(['stat_id'], axis=1)
            
            
            # Joining all those dataframes together
            for i in range(0, len(list_df)):
                if i == 0:
                    df_wide = list_df[i]
                else:
                    df_wide = pd.merge(
                        df_wide,
                        list_df[i],
                        [
                            'is_consolation',
                            'is_playoffs',
                            'team_id',
                            'team_name',
                            'week_end',
                            'week_num',
                            'week_start'
                        ]
                    )
            
            
            # Creating a dataframe for each main team and opponent and joining it back
            df_main = df_wide[df_wide.team_name == main_team_name]
            df_opponent = df_wide[df_wide.team_name != main_team_name]
            
            df_full_temp = pd.merge(
                df_main,
                df_opponent,
                [
                    'is_consolation',
                    'is_playoffs',
                    'week_end',
                    'week_num',
                    'week_start'
                ],
                suffixes=('', '_opponent')
            )
            
            # Adding all team dataframes together
            df_full = df_full.append(df_full_temp)

        return df_full

    def write_data(self, df):
        """
        Writes data to the current csv dump.
        :param df: Pandas dataframe containing the scraped data to be saved
        """
        csv_location = self.app_config['data_config']['scrape_data_location']

        # read previously obtained data and append newly scraped data
        df_full = pd.read_csv(csv_location)
        df_full.append(df, ignore_index=True)

        # write the appended data back to the 
        df_full.to_csv(csv_location)

    def execute(self):
        df = self.scrape(
            weeks=self.weeks_to_scrape()
        )

        self.write_data(df)

