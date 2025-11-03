import pytest
from baxter.Strategy import Strategy


def test_strategy_instantiation(indicators):
    with pytest.raises(TypeError):
        Strategy(indicators=indicators)
