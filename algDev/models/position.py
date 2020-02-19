from models.trade import Trade
from models.equity import Equity

class Position:
    def __init__(self, eq): # num_shares, share_price):
        self.eq = eq
        self.num_shares = 0
        self.trades = []

    def trade_shares(self, num_shares, share_price, date):
        tr = Trade(num_shares, share_price, date)
        self.trades.insert(tr)
        self.num_shares = self.num_shares + num_shares

    # def trade_value(self, amt, date):
    #     num_shares = int(amt/self.share_price)
    #     self.trades[date] = num_shares
    #     self.num_shares = self.num_shares + num_shares
        
    # def buy_shares(self, num_shares):
    #     return self.trade(num_shares)

    # def sell_shares(self, num_shares):
    #     return self.trade(-1 * num_shares)

    #DONE
    def get_price(self, date, type = 'O'):

        switcher = {'O':self.eq.opens, 'C':self.eq.closes, 'H':self.eq.highs, 'L':self.eq.lows}
        price_type = switcher.get(type, 0)

        return self.eq[self.eq.getIndexFromDate(date)]

    #DONE
    def value(self, date, type = 'O'):
        return self.get_price(date) * self.num_shares

    #DONE
    def is_short(self):
        return self.num_shares < 0

    #DONE
    def has_position(self):
        return self.num_shares is not 0

    