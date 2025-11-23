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
            columns=["Unrealized P&L", "Realized P&L", "Unrealized Benchmark P&L", "Realized Benchmark P&L", "Strategy Drawdown", "Benchmark Drawdown"])

        self.metrics = np.nan

    # this method should fill in the self._equity_curve attribute
    @abstractmethod
    def _calculate_equity_curve(self): ...

    def _sharpe(self) -> float:
        """Sharpe Ratio (annualized)"""
        rets = self._equity_curve["Unrealized P&L"].pct_change()
        return (np.mean(rets) / np.std(rets)) * np.sqrt(252)

    def _sortino(self) -> float:
        """Sortino Ratio (annualized)"""
        rets = self._equity_curve["Unrealized P&L"].pct_change()
        return (np.mean(rets) / np.std(rets[rets <= 0])) * np.sqrt(252)

    def _cagr(self) -> float:
        """Compounded Annual Growth Rate"""
        cum_rets = self._equity_curve["Unrealized P&L"].dropna()
        return (cum_rets[-1] / cum_rets[0])**(252 / (cum_rets.shape[0])) - 1

    def _beta(self) -> float:
        """Beta"""
        rets = self._equity_curve["Unrealized P&L"].pct_change()
        bm = self.benchmark.pct_change()
        beta = bm.corrwith(rets).squeeze()
        return beta

    def _max_dd(self) -> float:
        """Max Drawdown"""
        return np.min(self._equity_curve["Strategy Drawdown"])

    def _avg_dd(self) -> float:
        """Average Drawdown"""
        return np.mean(self._equity_curve["Strategy Drawdown"])

    def _max_dd_dur(self) -> int:
        """Longest drawdown duration"""
        dds = (self._equity_curve["Strategy Drawdown"] == 0).astype(int)
        dd_chs = dds.diff()
        dd_durs = np.round(dd_chs[dd_chs == -1].index.diff().days[1:])
        max_dd_dur = np.round(np.max(dd_durs))
        return max_dd_dur

    def _avg_dd_dur(self) -> int:
        """Longest drawdown duration"""
        dds = (self._equity_curve["Strategy Drawdown"] == 0).astype(int)
        dd_chs = dds.diff()
        dd_durs = np.round(dd_chs[dd_chs == -1].index.diff().days[1:])
        avg_dd_dur = np.round(np.mean(dd_durs))
        return avg_dd_dur

    def _num_dds(self):
        """Total number of drawdowns"""
        dds = (self._equity_curve["Strategy Drawdown"] == 0).astype(int)
        dd_chs = dds.diff()
        dd_durs = np.round(dd_chs[dd_chs == -1].index.diff().days[1:])
        return dd_durs.size

    def _ann_num_dds(self):
        T = self._equity_curve["Strategy Drawdown"].size
        return self._num_dds() / (T / 252)

    def _ann_ret(self) -> float:
        """Annual Return"""
        return np.mean(self._equity_curve["Unrealized P&L"].pct_change()) * 252

    def _tot_num_trades(self) -> int:
        """Total Number of Trades rounded to nearest integer, where one trade counts as going in and out of position"""
        return int(np.round(self._equity_curve["Realized P&L"].isna().value_counts().loc[False] / 2))

    def _ann_num_trades(self) -> int:
        """Annual Number of Trades rounded to nearest integer, where one trade counts as going in and out of position"""
        tot_num_trading_days = self._equity_curve["Unrealized P&L"].dropna(
        ).shape[0]
        return int(np.round(self._tot_num_trades() / (tot_num_trading_days / 252)))

    def _avg_ret_per_trade(self):
        """Average Return per Trade"""
        tot_ret = self._equity_curve["Realized P&L"].dropna()[-1]
        return tot_ret**(1/self._tot_num_trades()) - 1

    def _calc_metrics(self):
        self.metrics = pd.DataFrame.from_dict({
            "Sharpe Ratio (annualized)": self._sharpe(),
            "Sortino Ratio (annualized)": self._sortino(),
            "Compounded Annual Growth Rate": self._cagr(),
            "Beta": self._beta(),
            "Max Drawdown": self._max_dd(),
            "Average Drawdown": self._avg_dd(),
            "Max Drawdown Duration": self._max_dd_dur(),
            "Average Drawdown Duration": self._avg_dd_dur(),
            "Total # of Drawdowns": self._num_dds(),
            "Annual # of Drawdowns": self._ann_num_dds(),
            "Annual Return": self._ann_ret(),
            "Total # of Trades": self._tot_num_trades(),
            "Annual # of Trades": self._ann_num_trades(),
            "Average Return per Trade": self._avg_ret_per_trade()
        }, orient="index", columns=["value"])

    def _plot_equity_curves(self):

        fig, (ax0, ax1) = plt.subplots(
            2, 1, figsize=(20, 15), sharex=True)

        fig.suptitle("Equity Curves and Drawdown")

        ax0.plot(self._equity_curve["Unrealized P&L"])
        ax0.plot(self._equity_curve["Unrealized Benchmark P&L"])
        ax0.plot(self._equity_curve["Realized P&L"], 'g+')
        ax0.legend(['Unrealized', 'Benchmark', 'Realized'])
        ax0.set_title("Percentage P&L")
        ax0.set_yscale('log')

        ax1.plot(self._equity_curve["Strategy Drawdown"])
        ax1.plot(self._equity_curve["Benchmark Drawdown"])
        ax1.set_title("Drawdown")

    def run(self) -> None:
        self._calculate_equity_curve()
        self._plot_equity_curves()
        self._calc_metrics()
