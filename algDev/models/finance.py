import pandas as pd
import math
import numpy as np
import statistics as stat 

class Finance:

    """
    Contains methods to calculate important statistical characeristics
    of securities and their relationships to each other to build efficient
    portfolios
    """

    def __init__(self):
        pass
    
    #Calculate the percent change between any two numbers
    #DONE
    @staticmethod
    def pChange(p1, p2):
        return (p2-p1)/p1

    """
    Calculate the percent change each day between p1 and p2
    There are two cases:
    1) If start and stop are the same value, then it calculates the pChange from one day to the next of that value
    2) If start and stop are the same value, then it calculates the pChange of that value in that day

    There are 4 potential inputs for start and stop: 'O', 'C', 'H', 'L'
    days refers to how back you would like to go
    """
    #TESTING
    @staticmethod
    def dailyChanges(eq, days = 500, start = 'O', stop = 'C'):
        
        #Switch Case
        switcher = {'O':eq.opens, 'C':eq.closes, 'H':eq.highs, 'L':eq.lows}

        p1 = switcher.get(start, 0)
        p2 = switcher.get(stop, 0)

        #If IPO date happened < days days ago
        if days > len(p1):
            days = len(p1)

        if(start == stop):
            daily_returns = [0] * (days-1)

            for i in range(0, days - 2):
                daily_returns[i] = Finance.pChange(p1[i+1],p2[i])

        
        else:
            daily_returns = [0] * (days)
        
            for i in range(0,days-1): 
                daily_returns[i] = Finance.pChange(p1[i],p2[i])
        
        return daily_returns

    #DONE
    @staticmethod
    def mean(eq, days = 500, start = 'O', stop = 'C'):
        return stat.mean(Finance.dailyChanges(eq, days, start, stop))

    #DONE
    @staticmethod
    def variance(eq, days = 500, start = 'O', stop = 'C'):
        return stat.pvariance(Finance.dailyChanges(eq,days, start, stop))

    #DONE
    @staticmethod
    def covariance(eq1, eq2, days = 500, start = 'O', stop = 'C'):
        pass
        DCeq1 = Finance.dailyChanges(eq1, days, start, stop)
        DCeq2 = Finance.dailyChanges(eq2, days, start, stop)

        #If one security IPO in the last days days, then adjust so lists are same length
        if(len(DCeq1) != len(DCeq2)):
            if(len(DCeq1)>len(DCeq2)):
                DCeq1 = DCeq1[0:len(DCeq2)-1]
            else:
                DCeq2 = DCeq2[0:len(DCeq1)-1]
        
        return np.cov(DCeq1, DCeq2)[0,1]

    #DONE
    @staticmethod
    def stddev(eq, days = 500, start = 'O', stop = 'C'):
        return math.sqrt(Finance.variance(eq, days, start, stop))
    
    #DONE
    @staticmethod
    def correlation(eq1, eq2, days = 500, start = 'O', stop = 'C'):
        pass
        cov = Finance.covariance(eq1, eq2, days, start, stop)
        std1 = Finance.stddev(eq1, days, start, stop)
        std2 = Finance.stddev(eq2, days, start, stop)

        return cov/(std1*std2)

    

    


     