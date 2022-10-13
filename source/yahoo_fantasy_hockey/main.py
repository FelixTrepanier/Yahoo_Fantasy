from yahoo_fantasy_hockey.scrape_league.scrape_league import Scrape_League
from yahoo_fantasy_hockey.preprocessing.data_preprocessing import Preprocessing
from yahoo_fantasy_hockey.util.config_helper import load_config

app_config = load_config()

scraper = Scrape_League(app_config)
scraper.execute()

