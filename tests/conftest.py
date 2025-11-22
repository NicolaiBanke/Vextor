import pandas as pd
import pytest
from baxter.Strategy import Strategy
from baxter.Backtester import Backtester


with pd.HDFStore("/home/n1c0/Dropbox/Quant/Projects/baxter/tests/test_strategy.h5") as store:
    _portfolio = store.get("time_series/portfolio")
    _benchmark = store.get("time_series/benchmark")
    _indicators = store.get("time_series/indicators")
    _equity_curve = store.get("time_series/equity_curve")
    _metrics = store.get("metrics")


@pytest.fixture(scope="module")
def portfolio():
    return _portfolio


@pytest.fixture(scope="module")
def benchmark():
    return _benchmark


@pytest.fixture(scope="module")
def indicators():
    return _indicators


@pytest.fixture(scope="module")
def equity_curve():
    return _equity_curve


@pytest.fixture(scope="module")
def metrics():
    return _metrics


@pytest.fixture(scope="module")
def backtester(equity_curve):
    # override Backtester's abstract method so it can be instantiated
    Backtester.__abstractmethods__ = set()
    bt = Backtester(pd.DataFrame(), pd.DataFrame(), pd.DataFrame())
    bt._equity_curve = equity_curve
    return bt


@pytest.fixture(scope="module")
def sub_strategy(indicators):
    class SubStrategy(Strategy):
        def __init__(self, indicators):
            super().__init__(indicators)

        def long(self):
            pass

        def short(self):
            pass

        def close(self):
            pass

    ss = SubStrategy(indicators=indicators)
    return ss


@pytest.fixture(scope="module")
def sub_tester(sub_strategy, portfolio, benchmark):
    class SubTester(Backtester):
        def __init__(self, strategy, portfolio, benchmark):
            super().__init__(strategy, portfolio, benchmark)

        def _calculate_equity_curve(self):
            pass

    return SubTester(strategy=sub_strategy, portfolio=portfolio, benchmark=benchmark)
