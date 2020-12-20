import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/Users/oliverjaros/Develop/nba/Past10Seasons.csv')

df.drop(['Unnamed: 0', 'SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'GAME_DATE', 'GAME_ID', 'MATCHUP', 'WL', 'MIN'], axis = 1, inplace = True)
# calculating each team's 4 factors and inserting them
EFG = ((df['FGM'] + (0.5 * df['FG3M'])) / df['FGA']) * 100
df.insert(20, 'EFG', EFG)

TOVRATE = (df['TOV'] / (df['FGA'] + (0.44 * df['FTA']) + df['TOV'])) * 100
df.insert(21, 'TOVRATE', TOVRATE)

FTRATE = df['FTM'] / df['FGA']
df.insert(22, 'FTRATE', FTRATE)

# print(df.columns)
print(df.corr())

fig = plt.figure(figsize=(15,37))

for i, col in enumerate(df[1:]):
    fig.add_subplot(15, 5, 1 + i)
    plt.scatter(df[col], df['PTS'])
    plt.xlabel(col)
    plt.ylabel('POINTS')
fig.tight_layout()
plt.show()