import pytest

from baxter.Backtester import Backtester


def test_backtester_instantiation(sub_strategy, portfolio, benchmark):
    with pytest.raises(TypeError):
        Backtester(strategy=sub_strategy,
                   portfolio=portfolio, benchmark=benchmark), "Backtester is an abstract base class and should not be instantiatable"


def test_backtester_abstract_methods():
    assert '_calculate_equity_curve' in Backtester.__abstractmethods__, "_calculate_equity_curve should be an abstract method of the Backtester base class"


def test_backtester_plot_equity_curves():
    assert '_plot_equity_curves' in dir(
        Backtester), "_plot_equity_curves should be an implemented method of Backtester"


def test_backtester_metrics_attribute():
    assert 'metrics' in Backtester.__static_attributes__, "metrics should be an attribute of the Backtester class"

# study https://realpython.com/pytest-python-testing/#marks-categorizing-tests to make tests neater


def test_backtester_metrics_methods():
    assert '_sharpe' in dir(
        Backtester), "method _sharpe should be implemented in the Backtester class to calculate the Sharpe ratio of a run strategy"
    assert '_sortino' in dir(
        Backtester), "method _sortino should be implemented in the Backtester class to calculate the Sortino ratio of a run strategy"
    assert '_cagr' in dir(
        Backtester), "method _cagr should be implemented in the Backtester class to calculate the compounded annual growth rate of a run strategy"
    assert '_beta' in dir(
        Backtester), "method _beta should be implemented in the Backtester class to calculate the beta of a run strategy"
    assert '_max_dd' in dir(
        Backtester), "method _max_dd should be implemented in the Backtester class to calculate the max drawdown of a run strategy"
    assert '_avg_dd' in dir(
        Backtester), "method _avg_dd should be implemented in the Backtester class to calculate the average drawdown of a run strategy"
    assert '_ann_ret' in dir(
        Backtester), "method _ann_ret should be implemented in the Backtester class to calculate the annual return of a run strategy"
    assert '_num_trds' in dir(
        Backtester), "method _num_trds should be implemented in the Backtester class to calculate the number of trades of a run strategy"
    assert '_avg_ret_trd' in dir(
        Backtester), "method _avg_ret_trds should be implemented in the Backtester class to calculate the average return per trade of a run strategy"
