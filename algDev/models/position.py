from models.trade import Trade

class Position:
    def __init__(self, eq, num_shares, share_price):
        self.eq = eq
        self.num_shares = num_shares
        self.share_price = share_price
        self.weight = 0
        self.trades = {}

    def trade_shares(self, num_shares, share_price, date):
        tr = Trade(num_shares, share_price)
        self.trades[date] = tr
        self.num_shares = self.num_shares + num_shares
        self.share_price = share_price

    # def trade_value(self, amt, date):
    #     num_shares = int(amt/self.share_price)
    #     self.trades[date] = num_shares
    #     self.num_shares = self.num_shares + num_shares
        
    # def buy_shares(self, num_shares):
    #     return self.trade(num_shares)

    # def sell_shares(self, num_shares):
    #     return self.trade(-1 * num_shares)

    #DONE
    def value(self):
        return self.share_price * self.num_shares

    #DONE
    def is_short(self):
        return self.num_shares < 0

    #DONE
    def has_position(self):
        return self.num_shares is not 0

    