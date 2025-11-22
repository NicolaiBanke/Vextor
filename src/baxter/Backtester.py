from abc import ABC, abstractmethod
from .Strategy import Strategy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Backtester(ABC):
    def __init__(
        self,
        strategy: Strategy,
        portfolio: pd.DataFrame,
        benchmark: pd.DataFrame
    ) -> None:
        self.strategy = strategy
        self.portfolio = portfolio
        self.benchmark = benchmark

        self._equity_curve = pd.DataFrame(
            index=benchmark.index,
            columns=["Unrealized Dollar P&L", "Realized Dollar P&L", "Unrealized Pct. P&L", "Realized Pct. P&L", "Unrealized Benchmark P&L", "Realized Benchmark P&L", "Unrealized Drawdown", "Realized Drawdown"])

        self.metrics = pd.DataFrame.from_dict({
            "Sharpe Ratio": np.nan,
            "Sortino Ratio": np.nan,
            "Compounded Annual Growth Rate": np.nan,
            "Beta": np.nan,
            "Max Drawdown": np.nan,
            "Average Drawdown": np.nan,
            "Annual Return": np.nan,
            "Total # of Trades": np.nan,
            "Annual # of Trades": np.nan,
            "Average Return per Trade": np.nan
        }, orient="index", columns=["value"])

    # this method should fill in the self._equity_curve attribute
    @abstractmethod
    def _calculate_equity_curve(self): ...

    def _sharpe(self):
        """Sharpe Ratio"""
        rets = self._equity_curve["Unrealized Pct. P&L"].pct_change()
        return (np.mean(rets) / np.std(rets)) * np.sqrt(252)

    def _sortino(self):
        """Sortino Ratio"""
        rets = self._equity_curve["Unrealized Pct. P&L"].pct_change()
        return (np.mean(rets) / np.std(rets[rets <= 0])) * np.sqrt(252)

    def _cagr(self):
        """Compounded Annual Growth Rate"""
        raise NotImplementedError

    def _beta(self):
        """Beta"""
        raise NotImplementedError

    def _max_dd(self):
        """Max Drawdown"""
        raise NotImplementedError

    def _avg_dd(self):
        """Average Drawdown"""
        raise NotImplementedError

    def _ann_ret(self):
        """Annual Return"""
        raise NotImplementedError

    def _tot_num_trades(self):
        """Total Number of Trades"""
        raise NotImplementedError

    def _ann_num_trades(self):
        """Annual Number of Trades"""
        raise NotImplementedError

    def _avg_ret_per_trade(self):
        """Average Return per Trade"""
        raise NotImplementedError

    def _plot_equity_curves(self):

        fig, (ax0, ax1, ax2) = plt.subplots(
            3, 1, figsize=(20, 15), sharex=True)

        fig.suptitle("Equity Curves and Drawdown")

        ax0.plot(self._equity_curve["Unrealized Dollar P&L"])
        ax0.plot(self._equity_curve["Realized Benchmark P&L"])
        ax0.plot(self._equity_curve["Realized Dollar P&L"], 'g+')
        ax0.legend(['Unrealized', 'Benchmark', 'Realized'])
        ax0.set_title("Dollar P&L")

        ax1.plot(self._equity_curve["Unrealized Pct. P&L"])
        ax1.plot(self._equity_curve["Unrealized Benchmark P&L"])
        ax1.plot(self._equity_curve["Realized Pct. P&L"], 'g+')
        ax1.legend(['Unrealized', 'Benchmark', 'Realized'])
        ax1.set_title("Percentage P&L")

        ax2.plot(self._equity_curve["Unrealized Drawdown"], 'black')
        ax2.plot(self._equity_curve["Realized Drawdown"], 'rv')
        ax2.set_title("Drawdown")

    def run(self) -> None:
        self._calculate_equity_curve()
        self._plot_equity_curves()
