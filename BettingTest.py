from selenium import webdriver
import time
import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
# import last10_fourfactors # run web scraper to get each teams average four factors for the last 10 games
from NBALinearRegressionModel import prediction # run linear regression model and import prediction function 


data = pd.read_csv('/Users/oliverjaros/Develop/nba/2019-20SeasonCleaned.csv', index_col=None)
odds = pd.read_csv('/Users/oliverjaros/Develop/nba/CleanedOdds2019-20.csv', index_col=None)

data['homeOdds'] = odds['homeOdds']
data['awayOdds'] = odds['awayOdds']

# data set of only four factors and points
modelData = data[['A_EFG', 'A_TOVRATE', 'A_OREBRATE', 'A_FTRATE', 'B_EFG', 'B_TOVRATE', 'B_OREBRATE', 'B_FTRATE', 'PTS_A', 'PTS_B']]
drop_col = ['PTS_A', 'PTS_B']

X = modelData.drop(drop_col, 1) # independent variables are four factors
y = data[['PTS_A', 'PTS_B']] #dependent variables are points
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

lr = LinearRegression() # creating model and fitting it
lr.fit(X_train, y_train)



fourFactors = pd.read_csv('/Users/oliverjaros/Develop/nba/last10_fourfactors.csv', index_col = None)
data = []

driver = webdriver.Chrome('/Library/Application Support/Google/chromedriver')


today = datetime.today()
curr_month = today.strftime('%B').lower()
# curr_date = today.strftime("%a, %h %d, %Y")
curr_date = today.strftime("Sun, Dec 1, 2019")

schedule = "https://www.basketball-reference.com/leagues/NBA_2019_games-october.html".format(curr_month)
driver.get(schedule)

row = driver.find_elements_by_xpath('//*[@id="schedule"]/tbody/tr')
for game in row:
    date = game.find_element_by_xpath('*[@data-stat="date_game"]')
    away = game.find_element_by_xpath('*[@data-stat="visitor_team_name"]')
    home = game.find_element_by_xpath('*[@data-stat="home_team_name"]')
    home_score = game.find_element_by_xpath('*[@data-stat="home_pts"]')
    away_score = game.find_element_by_xpath('*[@data-stat="visitor_pts"]')
    # get all teams playing on the current date
    # if date.text == curr_date:
        # Since model is predictive based on past data, by giving it data of the teams current state it will be able to predict outcome.
        # model is given data for past ~10 seasons and will predict outcome of teams playing on the current date based on their current form
        # iterate through each teams current four factors, and for each team if they are playing store their four factors in data[] and apply prediction algorithm to this data
    print('SCORES')
    for index, row in fourFactors.iterrows():
        if row['Team'] == home.text:
            homefactors = [row['eFG%'], row['TOV%'], row['ORB%'], row['FT/FGA']]
            break
    for index, row in fourFactors.iterrows():
        if row['Team'] == away.text:
            awayfactors = [row['eFG%'], row['TOV%'], row['ORB%'], row['FT/FGA']]
            break
    fourfactors = homefactors + awayfactors
    data.append(fourfactors)

    game_pred = lr.predict(data)
    print(home.text, "Score: ", game_pred[0][0])
    print(away.text, "Score: ", game_pred[0][1])
    print("Projected spread: ", (game_pred[0][0] - game_pred[0][1]))
    # print("Actual point difference:", (int(home_score.text) - int(away_score.text)))
    data = []
        


