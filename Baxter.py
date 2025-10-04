import pandas as pd
import Portfolio
import Strategy


class Baxter(object):
    def __init__(
        self,
        strategy: Strategy,
        portfolio: Portfolio
    ) -> None:
        self._strategy = strategy
        self._portfolio = portfolio

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, st: Strategy):
        self._strategy = st

    @property
    def portfolio(self):
        return self._portfolio

    @portfolio.setter
    def portfolio(self, pf):
        self._portfolio = pf

    def run(self) -> None:
        pnls = [],
        unrlzd = [],
        pnls_pct = [],
        unrlzd_pct = [],
        trade_dates = [],
        dates = [],
        entry = None,
        inpos = 0,
        COMMS = 0.05,

        for i in range(len(asset)-1):
            unr = (asset.Close.iloc[i].item() -
                   asset.Close.iloc[i-1].item()) * inpos
            unr_pct = ((asset.Close.iloc[i].item(
            ) - asset.Close.iloc[i-1].item()) / asset.Close.iloc[i-1].item()) * inpos
            unrlzd.append(unr)
            unrlzd_pct.append(unr_pct)

            # go long
            if mr.signal(i, inpos) == "long":
                entry = asset.Close.iloc[i].item()
                trade_dates.append(asset.index[i+1])
                inpos = 1

            # close position
            elif mr.signal(i, inpos) == "close":
                pnl = asset.Close.iloc[i].item() - entry
                pnls.append(pnl)
                pnl_pct = (asset.Close.iloc[i].item() - entry) / entry
                pnls_pct.append(pnl_pct)
                inpos = 0
            else:
                pass
