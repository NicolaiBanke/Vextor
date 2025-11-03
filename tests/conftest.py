import pandas as pd
import pytest

with pd.HDFStore(".") as store:
    _asset = store.get('asset')
    _indicators = store.get('indicators')


@pytest.fixture(scope="module")
def asset():
    return _asset


@pytest.fixture(scope="module")
def indicators():
    return _indicators
