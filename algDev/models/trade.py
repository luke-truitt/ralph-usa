
"""
Instance of this class has 4 variables
1) num_shares: # of shares traded (can be negative or positive)
2) share_price: share price at time of acquisition
3) trade_value: the total value of the trade
4) trade_type: either 'buy' or 'sell or short'
"""

class Trade:

    def __init__(self, num_shares, share_price, date):
        self.num_shares = num_shares
        self.date = date

    def get_type(self):
        if self.num_shares > 0:
            return 'buy'
        else:
            return 'sell or short'

    