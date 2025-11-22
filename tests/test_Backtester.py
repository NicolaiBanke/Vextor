import pytest
import pandas as pd

from baxter.Backtester import Backtester

with pd.HDFStore("/home/n1c0/Dropbox/Quant/Projects/baxter/tests/test_strategy.h5") as store:
    metric_names = list(store.get("metrics").index)


def test_backtester_instantiation(sub_strategy, portfolio, benchmark):
    with pytest.raises(TypeError):
        Backtester(strategy=sub_strategy,
                   portfolio=portfolio, benchmark=benchmark), "Backtester is an abstract base class and should not be instantiatable"


def test_backtester_abstract_methods():
    assert '_calculate_equity_curve' in Backtester.__abstractmethods__, "_calculate_equity_curve should be an abstract method of the Backtester base class"


def test_backtester_plot_equity_curves():
    assert '_plot_equity_curves' in dir(
        Backtester), "_plot_equity_curves should be an implemented method of Backtester"


def test_backtester_metrics_attribute(backtester):
    assert hasattr(
        backtester, 'metrics'), "metrics should be an attribute of the Backtester class"


@pytest.mark.parametrize("metric_name", metric_names)
def test_backtester_metrics_results(backtester, metrics, metric_name):

    assert getattr(backtester, metrics["method"].loc[metric_name])() == pytest.approx(
        metrics["value"].loc[metric_name]), f"{metric_name} should be approximately {metrics["value"].loc[metric_name]}"
