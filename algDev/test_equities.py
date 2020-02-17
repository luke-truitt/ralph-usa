import numpy as np
from models.equity import Equity
import os

print("hello world")

here = os.path.abspath(os.path.dirname(__file__))
data_directory = os.path.join(here, 'data\equities\AAPL.csv')

print(here)
print(data_directory)

#eq = 'AAPL'
#eq_path = r'./data/equities/%s.csv' % eq
testEquity = Equity(data_directory)
print('Equity Created')
print(testEquity.closes)
print(testEquity.volumes)
print(len(testEquity.volumes))
print(testEquity.data)