import pytest

from baxter.Backtester import Backtester


def test_backtester_instantiation(sub_strategy, portfolio, benchmark):
    with pytest.raises(TypeError):
        Backtester(strategy=sub_strategy,
                   portfolio=portfolio, benchmark=benchmark), "Backtester is an abstract base class and should not be instantiatable"

def test_backtester_abstract_methods():
    assert '_calculate_equity_curve' in Backtester.__abstractmethods__, "_calculate_equity_curve should be an abstract method of the Backtester base class"

def test_backtester_plot_equity_curves():
    assert '_plot_equity_curves' in dir(Backtester), "_plot_equity_curves should be an implemented method of Backtester"