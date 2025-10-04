import pandas as pd

class Baxter(object):
    def __init__(
        self,
        pnls=[],
        unrlzd=[],
        pnls_pct=[],
        unrlzd_pct=[],
        trade_dates=[],
        dates=[],
        entry=None,
        inpos=0,
        COMMS=0.05,
    ) -> None:
        self._pnls = pnls
        self._unrlzd = unrlzd
        self._pnls_pct = pnls_pct
        self._unrlzd_pct = unrlzd_pct
        self._trade_dates = trade_dates
        self._dates = dates
        self._entry = entry
        self._inpos = inpos
        self._COMMS = COMMS

    def __repr__(self) -> str:
        return ""
    
    def add_data(self, data: pd.DataFrame):
        raise NotImplementedError
    
    def run(self):
        raise NotImplementedError
