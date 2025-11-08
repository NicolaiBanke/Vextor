import pandas as pd
import pytest
from baxter.Strategy import Strategy
from baxter.Backtester import Backtester

with pd.HDFStore("data.h5") as store:
    print(store)
    _asset = store.get('asset')
    _indicators = store.get('indicators')


@pytest.fixture(scope="module")
def portfolio():
    return _asset[["Close"]]


@pytest.fixture(scope="module")
def benchmark():
    return _asset[["Close"]]


@pytest.fixture(scope="module")
def indicators():
    return _indicators


@pytest.fixture(scope="module")
def sub_strategy(indicators):
    class SubStrategy(Strategy):
        def __init__(self, indicators):
            super().__init__(indicators)

        def signal():
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
