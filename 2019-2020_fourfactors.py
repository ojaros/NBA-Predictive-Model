from selenium import webdriver
import time
import pandas as pd

driver = webdriver.Chrome('/Library/Application Support/Google/chromedriver')
data = []

driver.get('https://www.basketball-reference.com/leagues/NBA_2020.html#all_misc_stats')
# time.sleep(5)

row = driver.find_elements_by_xpath('//*[@id="misc_stats"]/tbody/tr')
for team in row:
    team_name = team.find_element_by_xpath('*[@data-stat="team_name"]')
    wins = team.find_element_by_xpath('*[@data-stat="wins"]')
    losses = team.find_element_by_xpath('*[@data-stat="losses"]')
    off_rtg = team.find_element_by_xpath('*[@data-stat="off_rtg"]')
    def_rtg = team.find_element_by_xpath('*[@data-stat="def_rtg"]')
    efg_pct = team.find_element_by_xpath('*[@data-stat="efg_pct"]')
    tov_pct = team.find_element_by_xpath('*[@data-stat="tov_pct"]')
    orb_pct = team.find_element_by_xpath('*[@data-stat="orb_pct"]')
    ft_rate = team.find_element_by_xpath('*[@data-stat="ft_rate"]')
    opp_efg_pct = team.find_element_by_xpath('*[@data-stat="opp_efg_pct"]')
    opp_tov_pct = team.find_element_by_xpath('*[@data-stat="opp_tov_pct"]')
    drb_pct = team.find_element_by_xpath('*[@data-stat="drb_pct"]')
    opp_ft_rate = team.find_element_by_xpath('*[@data-stat="opp_ft_rate"]')

    team_stats = [team_name.text, wins.text, losses.text, off_rtg.text, def_rtg.text, efg_pct.text, tov_pct.text, orb_pct.text, ft_rate.text, opp_efg_pct.text, opp_tov_pct.text, drb_pct.text, opp_ft_rate.text]
    data.append(team_stats)

driver.close()

df = pd.DataFrame(data)
df.columns = ['Team', 'W', 'L', 'ORtg', 'DRtg', 'eFG%', 'TOV%', 'ORB%', 'FT/FGA', 'Opp eFG%', 'Opp TOV%', 'DRB%', 'Opp FT/FGA']
df.to_csv('/Users/oliverjaros/Develop/nba/2019-2020_fourfactors.csv', index = False)