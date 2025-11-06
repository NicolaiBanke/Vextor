import pytest
from baxter.LoopTester import LoopTester


def test_looptester_empty_instantiation():
    with pytest.raises(TypeError):
        LoopTester(), "LoopTester should not be instantiatable without attributes"


def test_looptester_instantiation(sub_strategy, portfolio, benchmark):
    lt = LoopTester(strategy=sub_strategy,
                    portfolio=portfolio, benchmark=benchmark)

    assert "_equity_curve" in lt.__dir__(
    ), "._equity_curve should be implemented for this class"

    assert "_calculate_equity_curve" in lt.__dir__(
    ), "._calculate_equity_curve should be implemented for this class"

    assert "run" in lt.__dir__(
    ), ".run should be implemented for this class"

def test_looptester_run_method(loop_tester):
    loop_tester.run()