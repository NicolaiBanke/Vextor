import numpy as np
import pandas as pd
import pytest
from baxter.Strategy import Strategy
from baxter.Backtester import Backtester

# generate som random numbers for fixtures
rng = np.random.default_rng(42)

# simulate generic backtest results
_equity_curve = rng.normal(loc=5, scale=10, size=10000)

with pd.HDFStore("data.h5") as store:
    _asset = store.get("asset")
    _indicators = store.get("indicators")


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
def equity_curve():
    return _equity_curve

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
