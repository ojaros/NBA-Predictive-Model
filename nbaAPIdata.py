import pandas as pd
import numpy as np
import time
from nba_api.stats.static import teams
from nba_api.stats.endpoints import leaguegamefinder

custom_headers = {
    'Host': 'stats.nba.com',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}

df = pd.DataFrame(columns=['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'PTS', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PLUS_MINUS'])

# returns every game of each team from the past 10 seasons
nba_teams = teams.get_teams()
for team in nba_teams:
    team_id = team['id']
    gamefinder = leaguegamefinder.LeagueGameFinder(team_id_nullable=team_id)
    time.sleep(2)
    games = gamefinder.get_data_frames()[0]
    for i in range(2010, 2021):
        season_games = games[games.SEASON_ID.str[-4:] == str(i)]
        df = df.append(season_games, ignore_index=True)
    
df.to_csv('/Users/oliverjaros/Develop/nba/Past10Seasons.csv')

    


