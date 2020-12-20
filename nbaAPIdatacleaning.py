# cleaning data and calculating four factors
import numpy as np
import pandas as pd
from datetime import datetime

df = pd.read_csv('/Users/oliverjaros/Develop/nba/Past10Seasons.csv')

# removes duplicates by combining data for identical games into one row
def combine_team_games(df, keep_method='home'):
    '''Combine a TEAM_ID-GAME_ID unique table into rows by game. Slow.

        Parameters
        ----------
        df : Input DataFrame.
        keep_method : {'home', 'away', 'winner', 'loser', ``None``}, default 'home'
            - 'home' : Keep rows where TEAM_A is the home team.
            - 'away' : Keep rows where TEAM_A is the away team.
            - 'winner' : Keep rows where TEAM_A is the losing team.
            - 'loser' : Keep rows where TEAM_A is the winning team.
            - ``None`` : Keep all rows. Will result in an output DataFrame the same
                length as the input DataFrame.
                
        Returns
        -------
        result : DataFrame
    '''
    # Join every row to all others with the same game ID.
    joined = pd.merge(df, df, suffixes=['_A', '_B'],
                      on=['SEASON_ID', 'GAME_ID', 'GAME_DATE'])
    # Filter out any row that is joined to itself.
    result = joined[joined.TEAM_ID_A != joined.TEAM_ID_B]
    # Take action based on the keep_method flag.
    if keep_method is None:
        # Return all the rows.
        pass
    elif keep_method.lower() == 'home':
        # Keep rows where TEAM_A is the home team.
        result = result[result.MATCHUP_A.str.contains(' vs. ')]
    elif keep_method.lower() == 'away':
        # Keep rows where TEAM_A is the away team.
        result = result[result.MATCHUP_A.str.contains(' @ ')]
    elif keep_method.lower() == 'winner':
        result = result[result.WL_A == 'W']
    elif keep_method.lower() == 'loser':
        result = result[result.WL_A == 'L']
    else:
        raise ValueError(f'Invalid keep_method: {keep_method}')
    return result
    
# combine duplicate game rows into one. By default, the home team will be TEAM_A.
df = combine_team_games(df)

# sorting by date oldest to most recent
df['GAME_DATE']=pd.to_datetime(df['GAME_DATE'])
df.sort_values(by=['GAME_DATE'], inplace=True, ascending=True)

# dropping unnecessary data
df.dropna(inplace=True)
df.drop(['Unnamed: 0_A', 'Unnamed: 0_B', 'SEASON_ID', 'TEAM_ID_A', 'TEAM_ID_B', 'TEAM_ABBREVIATION_A', 'TEAM_ABBREVIATION_B', 'GAME_ID'], axis = 1, inplace = True)

# calculating each team's 4 factors and inserting them
A_EFG = ((df['FGM_A'] + (0.5 * df['FG3M_A'])) / df['FGA_A']) * 100
B_EFG = ((df['FGM_B'] + (0.5 * df['FG3M_B'])) / df['FGA_B']) * 100
df.insert(47, 'A_EFG', A_EFG)
df.insert(48, 'B_EFG', B_EFG)

A_TOVRATE = (df['TOV_A'] / (df['FGA_A'] + (0.44 * df['FTA_A']) + df['TOV_A'])) * 100
B_TOVRATE = (df['TOV_B'] / (df['FGA_B'] + (0.44 * df['FTA_B']) + df['TOV_B'])) * 100
df.insert(49, 'A_TOVRATE', A_TOVRATE)
df.insert(50, 'B_TOVRATE', B_TOVRATE)

A_OREBRATE = (df['OREB_A'] / (df['OREB_A'] + df['DREB_B'])) * 100
B_OREBRATE = (df['OREB_B'] / (df['OREB_B'] + df['DREB_A'])) * 100
df.insert(51, 'A_OREBRATE', A_OREBRATE)
df.insert(52, 'B_OREBRATE', B_OREBRATE)

A_FTRATE = df['FTM_A'] / df['FGA_A']
B_FTRATE = df['FTM_B'] / df['FGA_B']
df.insert(53, 'A_FTRATE', A_FTRATE)
df.insert(54, 'B_FTRATE', B_FTRATE)

A_DREBRATE = 100 - df['B_OREBRATE']
B_DREBRATE = 100 - df['A_OREBRATE']
df.insert(55, 'A_DREBRATE', A_DREBRATE)
df.insert(56, 'B_DREBRATE', B_DREBRATE)

df.to_csv('/Users/oliverjaros/Develop/nba/Past10SeasonsCleaned.csv', index = False)