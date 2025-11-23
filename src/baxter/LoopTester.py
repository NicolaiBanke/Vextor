from .Backtester import Backtester
import pandas as pd


class LoopTester(Backtester):
    def __init__(self, strategy, portfolio, benchmark):
        super().__init__(strategy, portfolio, benchmark)
        # a LoopTester is initialized with these intermediate lists to optimize the loop
        self._loop_results = {
            "pnls": [],
            "unrlzd": [],
            "trade_dates": [],
            "dates": [],
        }

    def _calculate_equity_curve(self) -> None:
        entry = None
        pos = 0
        COMMS = 0.05

        for i in range(1, len(self.benchmark) - 1):
            unr = (
                (self.portfolio.iloc[i].item() -
                 self.portfolio.iloc[i - 1].item())
                / self.portfolio.iloc[i - 1].item()
            ) * pos
            self._loop_results["unrlzd"].append(unr)
            self._loop_results["dates"].append(self.portfolio.index[i])

            # go long
            if self.strategy.long(self.strategy.indicators.iloc[i]) and pos == 0:
                entry = self.portfolio.iloc[i].item()
                self._loop_results["trade_dates"].append(
                    self.portfolio.index[i + 1])
                pos = 1

            # go short
            elif self.strategy.short(self.strategy.indicators.iloc[i]) and pos == 0:
                pass

            # close position
            elif self.strategy.close(self.strategy.indicators.iloc[i]) and pos != 0:
                pnl = (self.portfolio.iloc[i].item() - entry) / entry
                self._loop_results["pnls"].append(pnl)
                pos = 0

            else:
                pass

        self._equity_curve["Realized P&L"] = (
            1
            + pd.Series(
                self._loop_results["pnls"], index=self._loop_results["trade_dates"]
            )
        ).cumprod()

        self._equity_curve["Unrealized P&L"] = (
            1
            + pd.Series(
                self._loop_results["unrlzd"], index=self._loop_results["dates"]
            )
        ).cumprod()

        self._equity_curve["Unrealized Benchmark P&L"] = (
            1 + self.benchmark.pct_change()
        ).cumprod()

        self._equity_curve["Strategy Drawdown"] = (
            self._equity_curve["Unrealized P&L"]
            / self._equity_curve["Unrealized P&L"].expanding().max()
            - 1
        )

        self._equity_curve["Benchmark Drawdown"] = (
            self._equity_curve["Unrealized Benchmark P&L"]
            / self._equity_curve["Unrealized Benchmark P&L"].expanding().max()
            - 1
        )
