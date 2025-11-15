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


@pytest.mark.parametrize("_metric_method, metric", [
    ("_sharpe", "Sharpe ratio"),
    ("_sortino", "Sortino ratio"),
    ("_cagr", "compounded annual growth rate"),
    ("_beta", "beta"),
    ("_max_dd", "max drawdown"),
    ("_avg_dd", "average drawdown"),
    ("_ann_ret", "annual return"),
    ("_num_trds", "number of trades"),
    ("_avg_ret_trd", "average return per trade")
])
def test_backtester_metrics_methods(_metric_method, metric):
    assert _metric_method in dir(
        Backtester), f"method {_metric_method} should be implemented in the Backtester class to calculate the {metric} of a run strategy"
