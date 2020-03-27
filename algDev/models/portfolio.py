import numpy as np
import random
import os
import datetime
import pandas as pd
from models.equity import Equity
from models.position import Position
from models.finance import Finance

## Dummy function for testing purposes
def model_output(position, verbose=False):
    """
    Generate random buy/sell/hold signal
    1:Buy, 0:Hold, -1:Sell
    Confidence Level: # between 0 and 1
    """
    signal = random.randint(-1, 1) ##Placeholder
    confidence = random.random() ##Placeholder

    return signal, alloc

class Portfolio:

    def __init__(self, value, eqs, init_date, days = 500, start = 'O', stop = 'C', verbose=False):
        self.positions = []
        self.free_cash = {init_date: value}
        self.init_positions(eqs, verbose)
        self.cov_arr = np.zeros((len(self.positions),len(self.positions)))

        self.days = days
        self.start = start
        self.stop = stop

        self.update_cov_arr(init_date, days, start, stop)


    ##
    def update_cov_arr(self, init_date, days=500,start = 'O', stop = 'C'):
        for i in range(0, len(self.positions)):
            eq1 = self.positions[i].eq
            for j in range(0, len(self.positions)):
                eq2 = self.positions[j].eq
                self.cov_arr[i, j] = Finance.covariance(eq1, eq2, init_date, days, start, stop)
        print(self.cov_arr)

    def init_positions(self, eqs, verbose=False):
        here = os.path.abspath(os.path.dirname(__file__))
        data_directory = os.path.join(here, '..\\data')
        eq_directory = os.path.join(data_directory, 'equities')
        for eq in eqs:
            eq_file = os.path.join(eq_directory, eq + '.xlsx')
            e = Equity(eq_file)
            position = Position(e, verbose)
            self.positions.append(position)
    
    def getPosition(self, ticker, verbose=False):

        for p in self.positions:
            
            if p.ticker in ticker:
                return p

    def exp_ret(self, position, prediction, confidence, strategy_upper_threshold, strategy_lower_threshold, verebose):
        threshold = 0
        if prediction == 1:
            threshold = strategy_upper_threshold
        elif prediction == -1:
            threshold = strategy_lower_threshold
        
        ##ISSUE HERE IS THAT EXPECTED RETURN IS CAPPED AT THRESHOLD (condiser multiplying is by 2)
        return confidence * threshold * 2

    def realloc(self, date, strategy_lookback, strategy_upper_threshold, strategy_lower_threshold, verbose=False):
        
        ##UNCOMMENT ONCE COVAR CALCULATOR IS MADE MORE EFFICIENT
        ##self.update_cov_arr(date, self.days, self.start, self.stop)

        ##ASK LUKE ABOUT THIS LINE
        self.free_cash[date] = self.free_cash[list(self.free_cash.keys())[len(self.free_cash.keys())-1]]
        
        predictions, confidences, expected_returns = np.zeros((len(self.positions),)), np.zeros((len(self.positions),)), np.zeros((len(self.positions),))
    
        self.update_closings(strategy_lookback, strategy_upper_threshold, strategy_lower_threshold, date, verbose)

        for i,position in enumerate(self.positions):
            ### RUN MODEL FOR PARTICULAR EQUITY
            predictions[i], confidences[i] = model_output(position, verbose)## MODEL WOULD GO HERE
            expected_returns[i] = self.exp_ret(position, predictions[i], confidences[i], strategy_upper_threshold, strategy_lower_threshold, verbose)


        ## After that loop, predictions will be 1/0/-1 corresponding to buy/do nothing/short
        ##Confidence is the output of the model, from which we can calculate expected return
        ## allocations will be a decimal indicating how much of our available cash we should give to that
        
        ## for first try, we will just ignore allocation, but this should turn allcations into dollar amounts
        allocations = self.calculate_allocations(expected_returns, date, verbose)
        
        for i, pos in enumerate(self.positions):
            self.free_cash[date] -= pos.purchase(predictions[i], allocations[i], date, verbose)
        if verbose is True:
            print("Current Free Cash: ", self.free_cash[date])
            print("Current Positions Value: ", self.getValue(date) - self.free_cash[date])
        return self.update(verbose)

    def update(self, verbose=False):
        return 0


    ##UPDATE THIS
    def calculate_allocations(self, expected_returns, date, verbose=False):
        unit_vector = np.ones(len(expected_returns))
        inv_cov_arr = np.linalg.inv(self.cov_arr)

        print("cov_arr:", self.cov_arr)
        print("inv_cov_arr:", inv_cov_arr)

        A = np.dot(np.dot(np.transpose(unit_vector), inv_cov_arr), unit_vector)
        print("A:",A)

        B = np.dot(np.dot(np.transpose(unit_vector),inv_cov_arr), expected_returns)
        print("B:",B)

        C = np.dot(np.dot(np.transpose(expected_returns), inv_cov_arr), expected_returns)
        print("C:",C)

        delta = np.dot(A,C) - np.dot(B,B)

        ##USE THE ABOVE FORMULAS TO CALCULATE THE EFFICIENT FRONTIER

        w_g = np.divide(np.dot(np.linalg.inv(self.cov_arr),unit_vector),A) #Weightings minimum risk portfolio
        w_d = np.divide(np.dot(np.linalg.inv(self.cov_arr),expected_returns),B) #Weightings tangency portfolio for r = 0% 
        print("w_d:", w_d)

        total = 0
        for i, alloc in enumerate(w_d):
            total += alloc
        
        ## Allocate one tenth of free cash
        allocations = w_d/(total * 10)

        allocations = allocations * self.free_cash[date]

        return allocations

    def update_closings(self, strategy_lookback, strategy_upper_threshold, strategy_lower_threshold, date, verbose=False):

        for i, pos in enumerate(self.positions):
        
            self.free_cash[date] += pos.handle_closings(strategy_upper_threshold, strategy_lower_threshold, strategy_lookback, date, verbose)
        
    def date_ob(self, date, verbose=False):

        pos = self.positions[0]

        most_recent_date = pos.eq.dates[0]
        
        return date > most_recent_date

    def getValue(self, date, verbose=False):

        value = self.free_cash[date]
        
        for pos in self.positions:
            if verbose:
                print("Pos:", pos.ticker)
                print("Trades:", pos.trades)
            pos_value = pos.value(date, verbose)
            if verbose:
                print(pos_value)
            value+=pos_value

        return value
        

