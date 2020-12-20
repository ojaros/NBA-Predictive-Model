import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics


data = pd.read_csv('/Users/oliverjaros/Develop/nba/Past10SeasonsCleaned.csv', index_col = None)

# data set of only four factors and points
data = data[['A_EFG', 'A_TOVRATE', 'A_OREBRATE', 'A_FTRATE', 'B_EFG', 'B_TOVRATE', 'B_OREBRATE', 'B_FTRATE', 'PTS_A', 'PTS_B']]
drop_col = ['PTS_A', 'PTS_B']

X = data.drop(drop_col, 1) # independent variables are four factors
y = data[['PTS_A', 'PTS_B']] #dependent variables are points
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

lr = LinearRegression() # creating model and fitting it
lr.fit(X_train, y_train)
# print(lr.score(X_train, y_train))
# print(lr.score(X_test, y_test))

# for idx, col_name in enumerate(X_train.columns):
#     print("For home points, The coefficient for {} is {}".format(col_name, lr.coef_[0][idx]))

# for idx, col_name in enumerate(X_train.columns):
#     print("For away points, The coefficient for {} is {}".format(col_name, lr.coef_[1][idx]))

# mean absolute error, how much our predictions vary from actual data on average
y_pred = lr.predict(X_test)
y_true = y_test
print(metrics.mean_absolute_error(y_pred, y_true))

# function to predict the outcome of a game given a home and away teams four factors
def prediction(game, home, away):
    game_pred = lr.predict(game)
    print(home, "Score: ", game_pred[0][0])
    print(away, "Score: ", game_pred[0][1])

# prediction([[56.6, 12.4, 25.5, 0.265, 52.8, 11.7, 27.2, 0.294]], 'Suns', 'Mavs')
# prediction([[37.34, 13.07, 29.54, .228, 49.206, 16.87, 24.324, .3809]], 'Magic', 'Pacers')

