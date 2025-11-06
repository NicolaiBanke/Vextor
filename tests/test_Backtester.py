import pytest

from baxter.Backtester import Backtester


def test_backtester_instantiation(sub_strategy, portfolio, benchmark):
    with pytest.raises(TypeError):
        Backtester(strategy=sub_strategy,
                   portfolio=portfolio, benchmark=benchmark), "Backtester is an abstract base class and should not be instantiatable"
