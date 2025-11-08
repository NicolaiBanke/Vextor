import pytest
from baxter.Strategy import Strategy


def test_strategy_instantiation(indicators):
    with pytest.raises(TypeError):
        Strategy(
            indicators=indicators), "Strategy is an abstract base class and should not be instantiatable"


def test_strategy_methods():
    assert 'long' in Strategy.__abstractmethods__, ".long should be an abstract method of the Strategy base class"
    assert 'short' in Strategy.__abstractmethods__, ".short should be an abstract method of the Strategy base class"
    assert 'close' in Strategy.__abstractmethods__, ".close should be an abstract method of the Strategy base class"
