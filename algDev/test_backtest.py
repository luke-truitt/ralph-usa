from models.backtest import Backtest
import datetime

def run_test():

    pf_value = 1000000
    start_date = datetime.datetime(2019, 1, 13)
    end_date = datetime.datetime(2019, 2, 13)

    b = Backtest(["AAPL", "AMZN", "BRK.B"], start_date, end_date, pf_value, 500, 'O', 'C', True)

    after_value, positions = b.simulate({'lookback_period': 5, 'strategy_upper_threshold': .025, 'strategy_lower_threshold': -0.025}, True)

    rtn = ((after_value - pf_value) / pf_value) * 100

    print(str(rtn) + "%")

    b.plot_value(pf_value, start_date, end_date)

run_test()