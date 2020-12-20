from selenium import webdriver
import time
import pandas as pd
from datetime import datetime
import last10_fourfactors # run web scraper to get each teams average four factors for the last 10 games
from boxScoresLinearRegression import prediction # run linear regression model and import prediction function 

fourFactors = pd.read_csv('/Users/oliverjaros/Develop/nba/last10_fourfactors.csv', index_col = None)
data = []

driver = webdriver.Chrome('/Library/Application Support/Google/chromedriver')


today = datetime.today()
curr_month = today.strftime('%B').lower()
# curr_date = today.strftime("%a, %h %d, %Y")
curr_date = today.strftime("Wed, Dec 23, 2020")

schedule = "https://www.basketball-reference.com/leagues/NBA_2021_games-{}.html".format(curr_month)
driver.get(schedule)

row = driver.find_elements_by_xpath('//*[@id="schedule"]/tbody/tr')
for game in row:
    date = game.find_element_by_xpath('*[@data-stat="date_game"]')
    away = game.find_element_by_xpath('*[@data-stat="visitor_team_name"]')
    home = game.find_element_by_xpath('*[@data-stat="home_team_name"]')
    # get all teams playing on the current date
    if date.text == curr_date:
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
        prediction(data, home.text, away.text)
    data = []
        


