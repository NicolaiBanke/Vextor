import pytest
from baxter.LoopTester import LoopTester


def test_looptester_empty_instantiation():
    with pytest.raises(TypeError):
        LoopTester(), "LoopTester should not be instantiatable without attributes"


def test_looptester_instantiation(sub_tester):
    assert "_equity_curve" in dir(
        sub_tester), "._equity_curve should be an attribute for this Backtester subclass"

    assert "_calculate_equity_curve" in dir(
        LoopTester), "._calculate_equity_curve should be implemented for this class"


def test_subtester_run_method(sub_tester):
    sub_tester.run()
