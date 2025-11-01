import pandas as pd
import matplotlib.pyplot as plt
#import seaborn as sns
from .Strategy import Strategy
from .Backtester import Backtester


class LoopTester(Backtester):
    def __init__(
        self,
        strategy: Strategy,
        portfolio: pd.DataFrame
    ) -> None:
        self.strategy = strategy
        self.portfolio = portfolio
        self._results = {
            'pnls': [],
            'unrlzd': [],
            'pnls_pct': [],
            'unrlzd_pct': [],
            'trade_dates': [],
            'dates': []
        }

    def _plot_pnls(self):
        #sns.set_theme()

        equity_curve_dollar_pnl = pd.Series(self._results['pnls'], index=self._results['trade_dates']).to_frame(
            'pnls').cumsum()

        equity_curve_dollar_unrlzd = pd.Series(
            self._results['unrlzd'], index=self._results['dates']).to_frame('unrlzd').cumsum()

        buynhold_dollar = self.portfolio.diff().to_frame("buy and hold").cumsum()

        equity_curve_pct_pnl = (1 + pd.Series(self._results['pnls_pct'], index=self._results['trade_dates'])).to_frame(
            'pnls_pct').cumprod()

        equity_curve_pct_unrlzd = (
            1 + pd.Series(self._results['unrlzd_pct'], index=self._results['dates'])).to_frame('unrlzd_pct').cumprod()

        buynhold_unrlzd = (
            1 + self.portfolio.pct_change().to_frame("buy and hold")).cumprod()

        drawdown_unrlzd = equity_curve_pct_unrlzd / equity_curve_pct_unrlzd.expanding().max() - 1
        drawdown_pnl = equity_curve_pct_pnl / equity_curve_pct_pnl.expanding().max() - 1

        fig, (ax0, ax1, ax2) = plt.subplots(
            3, 1, figsize=(20, 15), sharex=True)
        fig.suptitle("Equity Curves and Drawdown")
        ax0.plot(equity_curve_dollar_unrlzd)
        ax0.plot(buynhold_dollar)
        ax0.plot(equity_curve_dollar_pnl, 'g+')
        ax0.legend(['Unrealized', 'Benchmark', 'Realized'])
        ax0.set_title("Dollar P&L")

        ax1.plot(equity_curve_pct_unrlzd)
        ax1.plot(buynhold_unrlzd)
        ax1.plot(equity_curve_pct_pnl, 'g+')
        ax1.legend(['Unrealized', 'Benchmark', 'Realized'])
        ax1.set_title("Percentage P&L")

        ax2.plot(drawdown_unrlzd, 'black')
        ax2.plot(drawdown_pnl, 'rv')
        ax2.set_title("Drawdown")

    def run(self) -> None:
        entry = None
        inpos = 0
        COMMS = 0.05

        for i in range(1, len(self.portfolio)-1):
            unr = (self.portfolio.iloc[i].item() -
                   self.portfolio.iloc[i-1].item()) * inpos
            unr_pct = ((self.portfolio.iloc[i].item(
            ) - self.portfolio.iloc[i-1].item()) / self.portfolio.iloc[i-1].item()) * inpos
            self._results['unrlzd'].append(unr)
            self._results['unrlzd_pct'].append(unr_pct)
            self._results['dates'].append(self.portfolio.index[i])

            # go long
            if self.strategy.signal(i, inpos) == "long":
                entry = self.portfolio.iloc[i].item()
                self._results['trade_dates'].append(self.portfolio.index[i+1])
                inpos = 1

            # close position
            elif self.strategy.signal(i, inpos) == "close":
                pnl = self.portfolio.iloc[i].item() - entry
                self._results['pnls'].append(pnl)
                pnl_pct = (self.portfolio.iloc[i].item() - entry) / entry
                self._results['pnls_pct'].append(pnl_pct)
                inpos = 0
            else:
                pass

        self._plot_pnls()
