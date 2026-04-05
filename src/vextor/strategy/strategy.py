import pandas as pd
from abc import ABC, abstractmethod
from pandera.typing import DataFrame


class Strategy(ABC):
    def __init__(self, indicators: pd.DataFrame) -> None:
        self.indicators: pd.DataFrame = indicators

    @abstractmethod
    def long(self) -> DataFrame:
        raise NotImplementedError("Should implement a .long method")

    @abstractmethod
    def short(self) -> DataFrame:
        raise NotImplementedError(
            "Should implement a .short method, at least with a pass keyword"
        )

    @abstractmethod
    def exit(self) -> DataFrame:
        raise NotImplementedError("Should implement a .exit method")
