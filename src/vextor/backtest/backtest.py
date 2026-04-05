import pandas.core.frame
from vextor.strategy import Strategy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from .schemas import AssetsSchema
from pandera.typing import DataFrame


class Backtest(object):
    def __init__(
        self, strategy: Strategy, assets: DataFrame
    ) -> None:
        self.strategy: Strategy = strategy
        self.assets = AssetsSchema.validate(assets)
        self.benchmark: pd.DataFrame = self._calculate_benchmark()
        self.equity_curve = None

    def _calculate_sides(self) -> pd.DataFrame:
        sides = (
            (self.strategy.long() - self.strategy.exit())
            .replace(to_replace=0, value=np.nan)
            .ffill()
            + 1
        ) / 2
        sides.columns.name = 'Ticker'
        return sides

    def _calculate_pf_assets(self) -> pd.DataFrame:
        pf_assets = self.assets.stack().sort_index().groupby(
            'Ticker').pct_change().Close.unstack()
        return pf_assets

    def _calculate_benchmark(self) -> pd.DataFrame:
        pf_assets = self._calculate_pf_assets()
        benchmark = (self._calculate_pf_assets() *
                     (1/(pf_assets.columns.size))).sum(axis=1)
        return np.cumprod(1 + benchmark).to_frame('Benchmark')

    # this method should fill in the self._equity_curve attributes
    def _calculate_equity_curve(self) -> None:
        pf_assets = self._calculate_pf_assets()
        sides = self._calculate_sides()
        pnls = pf_assets * (sides.div(sides.sum(axis=1), axis=0)).shift()
        pf_pnls = pnls.sum(axis=1, skipna=False).dropna()
        self.equity_curve = (np.cumprod(1 + pf_pnls)).to_frame('Strategy')

    def run(self) -> None:
        self._calculate_equity_curve()
        sns.lineplot(data=pd.concat(
            [self.equity_curve, self.benchmark], axis=1))
        plt.yscale("log")
