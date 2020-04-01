from algDev.models.backtest import Backtest
from algDev.models.asset_strategy import AssetStrategy
from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.algorithms.asset_allocation import AssetAllocation
import datetime

def run_test():

    pf_value = 1000000
    start_date = datetime.datetime(2005, 1, 13)
    end_date = datetime.datetime(2019, 1, 13)
    lookback_period = 10
    upper_threshold = 0.025
    lower_threshold = -0.15
    tickers = ["AAPL", "AMZN", "BRK.B"]
    features = ["Volumes", "Prices", "SMA", "EMA"]
    strat_type = 'svm'

    trading_algorithm = TradingAlgorithm(tickers, features, strat_type, lookback_period, lower_threshold, upper_threshold, verbose=False)
    asset_allocation = AssetAllocation(upper_threshold, lower_threshold)
    asset_strategy = AssetStrategy(asset_allocation)

    b = Backtest(tickers, trading_algorithm, asset_strategy, start_date, end_date, pf_value, False)

    after_value, positions = b.simulate({'lookback_period': 14, 'strategy_threshold': .025}, False)

    rtn = ((after_value - pf_value) / pf_value) * 100

    print(str(rtn) + "%")

    b.plot_value(pf_value, start_date, end_date)

run_test()