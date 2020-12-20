from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
import pandas as pd

# op = webdriver.ChromeOptions()
# op.add_argument('--headless')

driver = webdriver.Chrome('/Library/Application Support/Google/chromedriver')
data = []


driver.get('https://www.nba.com/stats/teams/four-factors/?sort=W_PCT&dir=-1&Season=2019-20&SeasonType=Regular%20Season&LastNGames=10')
time.sleep(5)

now = datetime.now()
todays_date = now.strftime("%m/%d/%Y, %H:%M:%S")

numRows = len(driver.find_elements_by_xpath('/html/body/main/div/div/div[2]/div/div/nba-stat-table/div[2]/div[1]/table/tbody/tr'))
for i in range(1, numRows+1):
    name = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[2]'.format(i))
    efg = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[8]'.format(i))
    tov = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[10]'.format(i))
    oreb = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[11]'.format(i))
    fta = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[9]'.format(i))
    opp_efg = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[12]'.format(i))
    opp_tov = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[14]'.format(i))
    opp_oreb = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[15]'.format(i))
    opp_fta = driver.find_element_by_xpath('//*[@class="table"]/tbody/tr[{}]/td[13]'.format(i))

    #Creating array of stats for each team, with Def Reb as (100 - Opponent Off Reb)
    team_stats = [todays_date, name.text, efg.text, tov.text, oreb.text, fta.text, opp_efg.text, opp_tov.text, (100 - float(opp_oreb.text)), opp_fta.text]
    data.append(team_stats)
driver.close()

df = pd.DataFrame(data)
df.columns = ['Today', 'Team', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'Opp eFG%', 'Opp TOV%', 'DRB%', 'Opp FT/FGA']
df.replace('LA Clippers', 'Los Angeles Clippers', inplace=True)
df.to_csv('/Users/oliverjaros/Develop/nba/last10_fourfactors.csv', index = False)

