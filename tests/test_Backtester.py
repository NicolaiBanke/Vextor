import pytest
import pandas as pd

from baxter.Backtester import Backtester
from baxter.Strategy import Strategy


@pytest.fixture
def indicators():
    return pd.DataFrame()


@pytest.fixture
def strategy():
    class SubStrategy(Strategy):
        def __init__(self, indicators):
            super().__init__(indicators)

        def signal():
            pass

    ss = SubStrategy(indicators=indicators)
    return ss


@pytest.fixture
def portfolio():
    return pd.DataFrame()


@pytest.fixture
def benchmark():
    return pd.DataFrame()


def test_backtester_instantiation(strategy, portfolio, benchmark):
    with pytest.raises(TypeError):
        Backtester(strategy=strategy, portfolio=portfolio, benchmark=benchmark)
