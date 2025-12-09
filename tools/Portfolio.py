import pandas as pd

class Portfolio(object):
    def __init__(self, asset: pd.DataFrame):
        self._asset = asset
    
    @property
    def asset(self):
        return self._asset
    
    @asset.setter
    def asset(self, df: pd.DataFrame):
        self._asset = df
    
    @asset.getter
    def asset(self):
        return self._asset