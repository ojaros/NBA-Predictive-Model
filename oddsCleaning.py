import numpy as np
import pandas as pd
from datetime import datetime, timedelta
pd.set_option("mode.chained_assignment", None) 

def convert_to_datetime(x, year):
  y = str(x)
  if x < 1000:
    date = datetime(year=year, month=int(y[:-2]), day=int(y[-2:]))
    return date.strftime("%Y-%m-%d")
  else:
    date = datetime(year=year-1, month=int(y[:-2]), day=int(y[-2:]))
    return date.strftime("%Y-%m-%d")

odds2020 = pd.read_csv('/Users/oliverjaros/Develop/nba/odds2019-20.csv')

odds2020['VH'].unique()

odds2020['date'] = odds2020['Date'].apply(lambda x: convert_to_datetime(x, 2020))

homeOdds2020 = odds2020.loc[odds2020['VH']=='H'].reset_index(drop=True)[:1230]
awayOdds2020 = odds2020.loc[odds2020['VH']=='V'].reset_index(drop=True)[:1230]

homeOdds2020 = homeOdds2020.rename(columns={'Team': 'homeTeam', 'ML': 'homeOdds'})
awayOdds2020 = awayOdds2020.rename(columns={'Team': 'awayTeam', 'ML': 'awayOdds'})

combinedOdds2020 = homeOdds2020[['date','homeTeam','homeOdds']]
combinedOdds2020['awayTeam'] = awayOdds2020['awayTeam']
combinedOdds2020['awayOdds'] = awayOdds2020['awayOdds']

sortedOdds = combinedOdds2020.sort_values(by=['date', 'homeTeam'])

sortedOdds.to_csv('/Users/oliverjaros/Develop/nba/CleanedOdds2019-20.csv', index = False)

#FIX THE DATES