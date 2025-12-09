import pytest
from baxter.Strategy import Strategy


def test_strategy_instantiation(indicators):
    with pytest.raises(TypeError):
        Strategy(
            indicators=indicators), "Strategy is an abstract base class and should not be instantiatable"


@pytest.mark.parametrize("signal", ["long", "short", "close"])
def test_strategy_methods(signal):
    assert signal in Strategy.__abstractmethods__, f".{signal} should be an abstract method of the Strategy base class"
