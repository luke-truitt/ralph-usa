from models.trade import Trade
import datetime

class Position:
    def __init__(self, eq,verbose=False):
        self.ticker = eq.ticker
        self.eq = eq
        self.trades = []

    ##CHANGE TO ACCOMODATE SHORTING
    def purchase(self, prediction, allocation, today,verbose=False):
        if verbose:
            print("Checking purchase:",prediction)
            print("Allocation:", allocation)

        if prediction == 0:
            return 0

        #if prediction > 0:
        #    if verbose:
        #        print("Making purchase: ", allocation)
        #    left_over = self.trade_value(allocation, today, verbose)
        left_over = self.trade_value(allocation, today, verbose)
        #    return allocation - left_over
        return allocation - left_over
        #return 0
        
    def trade_shares(self, num_shares, date,verbose=False):
        self.trades.append(Trade(date, num_shares))

    def trade_value(self, amt, date,verbose=False):
        day_open = self.eq.get_price(date, 'o')
        print(day_open)
        num_shares = int(amt/day_open)
        total_purchased = num_shares * day_open
        left_over = amt - total_purchased
        if verbose:
            print("Buying ", num_shares, " at ", day_open)
        self.trade_shares(num_shares, date)
        return left_over

    def buy_shares(self, num_shares, date, verbose=False):
        return self.trade_shares(num_shares, date)

    def sell_shares(self, num_shares, date, verbose=False):
        return self.trade_shares(-1 * num_shares, date)

    def value(self, date,verbose=False):
        return self.eq.get_price(date, 'c', verbose) * self.get_shares(date)

    def is_short(self, date, verbose=False):
        return self.get_shares(date, verbose) < 0

    def has_position(self, date, verbose=False):
        return self.get_shares(date, verbose) is not 0

    def get_shares(self, date, verbose=False):
        total = 0
        
        for trade in self.trades:
            if trade.date_sold > date and trade.date_purchased <= date:
                total += trade.num_shares

        return total

    ##Note: lower_limit should be a negative float
    def handle_closings(self, upper_limit, lower_limit, exp, today, verbose=False):
        cash = 0
        if verbose:
            print("Checking position for closings")
        for i,trade in enumerate(self.trades):
            if self.check_closed(trade, verbose):
                continue
            pur_date = trade.purchase_date()
            days_since_pur = today - pur_date
            if days_since_pur > datetime.timedelta(days=exp):
                if verbose:
                    print("Bought at: ", self.eq.get_price(pur_date, 'o'))
                    print("Sold at: ", self.eq.get_price(today, 'c'))
                cash += trade.num_shares * self.eq.get_price(today, 'c', verbose)
                self.trades[i] = trade.sell(today, verbose)
                continue
            upper_limit_price = self.eq.get_price(pur_date, 'o', verbose) * (1 + upper_limit)
            
            if self.eq.get_price(today, 'h', verbose) >= upper_limit_price:
                if verbose:
                    print("Bought at: ", self.eq.get_price(pur_date, 'o', verbose))
                    print("Sold at: ", self.eq.get_price(today, 'h', verbose))
                cash += trade.num_shares * self.eq.get_price(today, 'h', verbose)
                self.trades[i] = trade.sell(today, verbose)

            lower_limit_price = self.eq.get_price(pur_date, 'o', verbose) * (1+ lower_limit)

            if self.eq.get_price(today, 'l', verbose) <= lower_limit_price:
                if verbose:
                    print("Bought at: ", self.eq.get_price(pur_date, 'o', verbose))
                    print("Sold at: ", self.eq.get_price(today, 'l', verbose))
                cash += trade.num_shares * self.eq.get_price(today, 'l', verbose)
                self.trades[i] = trade.sell(today, verbose)

        if verbose:
            print("Trades:",self.trades)
        return cash

    def check_closed(self, trade,verbose=False):
        return trade.sold
