from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    def __init__(self, indicators: pd.DataFrame):
        self.indicators = indicators
        
    @abstractmethod
    def signal(self): ...
