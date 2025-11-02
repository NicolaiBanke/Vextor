import pytest

from baxter.Backtester.Backtester import Backtester


def test_backtester_class():
    with pytest.raises(TypeError):
        Backtester()
