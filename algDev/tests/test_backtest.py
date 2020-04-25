from algDev.models.backtest import Backtest
from algDev.models.trading_algorithm import TradingAlgorithm
from algDev.models.asset_strategy import AssetAllocation, AssetStrategy
from algDev.API.models import loadTradingAlgorithm
import datetime

def run_test():

    pf_value = 1000000
    start_date = datetime.datetime(2019, 3, 4)
    end_date = datetime.datetime(2019, 4, 6)
    ta_id = '19124e2f-65e3-4dbb-b9fc-462f6eb96406'
    ta_id_demo = '6ae7528c-5f71-41ab-9c7f-139f1b3ff45e'
    ta = loadTradingAlgorithm(ta_id_demo)
    
    aa = AssetAllocation(0.015, -0.15)
    a_s = AssetStrategy(aa)
    b = Backtest(ta, a_s, start_date, end_date, pf_value, True)

    print(b.simulate(False))

    # rtn = ((after_value - pf_value) / pf_value) * 100

    # print(str(rtn) + "%")

    # b.plot_value(pf_value, start_date, end_date)
