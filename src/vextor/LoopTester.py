from .Backtester import Backtester
import pandas as pd
import numpy as np


class LoopTester(Backtester):
    def __init__(self, strategy, portfolio, benchmark):
        super().__init__(strategy, portfolio, benchmark)
        # a LoopTester is initialized with these intermediate lists to optimize the loop
        self._loop_results = {
            "pnls": [],
            "unrlzd": [],
            "trade_dates": [],
            "dates": [],
            "position": []
        }

    def _calculate_equity_curve(self) -> None:
        entry = None
        pos = 0
        COMMS = 0.05

        for i in range(1, len(self.benchmark)):
            unr = (
                (self.portfolio.Close.iloc[i] -
                 self.portfolio.Close.iloc[i - 1])
                / self.portfolio.Close.iloc[i - 1]
            ) * pos
            self._loop_results["unrlzd"].append(unr)
            self._loop_results["dates"].append(self.portfolio.index[i])
            self._loop_results["position"].append(pos)

            # go long
            if self.strategy.long(self.strategy.indicators.iloc[i]) and pos == 0:
                entry = self.portfolio.Open.iloc[i + 1]

                pos = 1

            # go short
            elif self.strategy.short(self.strategy.indicators.iloc[i]) and pos == 0:
                pass

            # close position
            elif self.strategy.close(self.strategy.indicators.iloc[i]) and pos != 0:
                pnl = (self.portfolio.Close.iloc[i] - entry) / entry
                self._loop_results["pnls"].append(pnl)
                self._loop_results["trade_dates"].append(
                    self.portfolio.index[i + 1])
                pos = 0

            else:
                pass

        self._equity_curve["Realized P&L"] = pd.Series(
            self._loop_results["pnls"], index=self._loop_results["trade_dates"])

        self._equity_curve["Unrealized P&L"] = pd.Series(
            self._loop_results["unrlzd"], index=self._loop_results["dates"]
        )

        self._equity_curve["Unrealized Benchmark P&L"] = self.benchmark.pct_change(
        )

        self._equity_curve["Strategy Drawdown"] = (
            np.cumprod(1+self._equity_curve["Unrealized P&L"])
            / np.cumprod(1+self._equity_curve["Unrealized P&L"]).expanding().max()
            - 1
        )

        self._equity_curve["Benchmark Drawdown"] = (
            np.cumprod(1+self._equity_curve["Unrealized Benchmark P&L"])
            / np.cumprod(1+self._equity_curve["Unrealized Benchmark P&L"]).expanding().max()
            - 1
        )

        self._equity_curve["Position"] = pd.Series(
            self._loop_results["position"], index=self._loop_results["dates"]).ffill()
