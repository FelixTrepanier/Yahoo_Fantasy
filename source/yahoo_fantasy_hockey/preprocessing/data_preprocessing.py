import pandas as pd
import numpy as np
from yahoo_fantasy_hockey.util.scoring_functions import *

class Preprocessing:
    # def __init__(self):

    def compute_results(self, df, categories):
        """
        Takes the freshly scraped data and calculates the record of each team.
        :param df: Scraped data in a Pandas dataframe.
        :categories: List of all category names.
        :return: A Pandas dataframe with added columns showing each team's record.
        """
        # points
        points_cat = []
        for cat in categories:
            points_cat.append(cat+'_opponent')
            df[cat+'_points'] = df[[cat, cat+'_opponent']].apply(lambda x: points_earned(x[cat], x[cat+'_opponent']))

        # wins
        win_cat = []
        for cat in categories:
            win_cat.append(cat+'_opponent')
            df[cat+'_win'] = df[[cat, cat+'_opponent']].apply(lambda x: win(x[cat], x[cat+'_opponent']))
        
        # losses
        loss_cat = []
        for cat in categories:
            loss_cat.append(cat+'_opponent')
            df[cat+'_loss'] = df[[cat, cat+'_opponent']].apply(lambda x: loss(x[cat], x[cat+'_opponent']))

        # ties
        tie_cat = []
        for cat in categories:
            tie_cat.append(cat+'_opponent')
            df[cat+'_tie'] = df[[cat, cat+'_opponent']].apply(lambda x: tie(x[cat], x[cat+'_opponent']))

        # weekly totals
        df['weekly_points_total'] = np.sum(df[[points_cat]], axis=0)
        df['weekly_win_total'] = np.sum(df[[win_cat]], axis=0)
        df['weekly_loss_total'] = np.sum(df[[loss_cat]], axis=0)
        df['weekly_tie_total'] = np.sum(df[[tie_cat]], axis=0)

