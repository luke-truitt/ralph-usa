import numpy as np
from models.equity import Equity
from models.finance import Finance
import os

print("hello world")

here = os.path.abspath(os.path.dirname(__file__))
data_directory1 = os.path.join(here, 'data\equities\AMZN.xlsx')
data_directory2 = os.path.join(here, 'data\equities\AAPL.xlsx')

"""
print(here)
print(data_directory)
"""
#eq = 'AAPL'
#eq_path = r'./data/equities/%s.csv' % eq
testEquity1 = Equity(data_directory1)
testEquity2 = Equity(data_directory2)
"""
print('Equity Created')
print(testEquity1.closes)
print(testEquity1.volumes)
print(len(testEquity1.volumes))
print(testEquity1.data)
"""

print('Mean Tests')
print(Finance.mean(testEquity1, start = 'O', stop = 'C'))
print(Finance.mean(testEquity1, start = 'O', stop = 'O'))
print(Finance.mean(testEquity2))

print('Variance Tests')
print(Finance.variance(testEquity1, start = 'O', stop = 'O'))
print(Finance.variance(testEquity2))

print('Covariance Tests')
print(Finance.covariance(testEquity1,testEquity2, start = 'O', stop = 'O'))
print(Finance.covariance(testEquity1,testEquity2))

print('Correlation Tests')
print(Finance.correlation(testEquity1, testEquity2, start = 'O', stop = 'O'))
print(Finance.correlation(testEquity2, testEquity1))
print(Finance.correlation(testEquity1, testEquity1))

