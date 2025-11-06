import pytest
from baxter.Strategy import Strategy


def test_strategy_instantiation(indicators):
    with pytest.raises(TypeError):
        Strategy(indicators=indicators), "Strategy is an abstract base class and should not be instantiatable"
