import pytest
from baxter.LoopTester import LoopTester
from baxter.Strategy import Strategy

@pytest.fixture
def strategy():
    return (Strategy)

def test_looptester_instantiation():
    with pytest.raises(TypeError):
        LoopTester()