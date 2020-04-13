import numpy as np
from algDev.models.finance import Finance

class AssetAllocation:

    def __init__(self, upper_threshold, lower_threshold, target_return = 0, rf = 0, days = 500, start = 'O', stop = 'C'):
        self.upper_threshold = upper_threshold
        self.lower_threshold = lower_threshold

        if target_return == 0:
            self.target_return = upper_threshold

        self.days = days
        self.start = start
        self.stop = stop

    def get_exp_ret(self, positions, predictions):
        expected_returns = []
        for position in positions:
            expected_returns.append(self.exp_ret(predictions[position.eq.ticker]))

        return expected_returns

    def exp_ret(self, prediction, verbose=False):
        threshold = 0
        pred_val = prediction[0]
        pred_conf = prediction[1]
        if pred_val == 1:
            threshold = self.upper_threshold
        elif pred_val == -1:
            threshold = self.lower_threshold
        
        ##ISSUE HERE IS THAT EXPECTED RETURN IS CAPPED AT THRESHOLD (condiser multiplying is by 2)
        return pred_conf * threshold
    
    ##UPDATE THIS
    def calculate_allocations(self, date, positions, predictions, verbose=False):
        
        expected_returns = self.get_exp_ret(positions, predictions)

        cov_arr = self.get_cov_arr(date, positions)
        unit_vector = np.ones(len(expected_returns))
        inv_cov_arr = np.linalg.inv(cov_arr)

        A = np.dot(np.dot(np.transpose(unit_vector), inv_cov_arr), unit_vector)
        B = np.dot(np.dot(np.transpose(unit_vector),inv_cov_arr), expected_returns)
        C = np.dot(np.dot(np.transpose(expected_returns), inv_cov_arr), expected_returns)
        delta = np.dot(A,C) - np.dot(B,B)

        ##USE THE ABOVE FORMULAS TO CALCULATE THE EFFICIENT FRONTIER

        w_g = np.divide(np.dot(np.linalg.inv(cov_arr),unit_vector),A) #Weightings minimum risk portfolio
        w_d = np.divide(np.dot(np.linalg.inv(cov_arr),expected_returns),B) #Weightings tangency portfolio for r = 0% 
        if verbose:
            print("w_d:", w_d)

        ##ADD USE OF RISK FREE RATE AND TARGET RETURNS
        #lam = np.divide(C-)

        total = 0
        for i, alloc in enumerate(w_d):
            total += alloc
        
        ## Allocate one tenth of free cash
        allocations = w_d/(total * 10)

        return allocations

    def get_DC_arr(self, today, positions):
        DC_arr = []
        for position in positions:
            DC_arr.append(Finance.dailyChanges(position.eq, today, self.days, self.start, self.stop))
        return DC_arr

    def get_cov_arr(self, date, positions):
        DC_arr = self.get_DC_arr(date, positions)
        cov_arr = np.cov(DC_arr)

        return cov_arr