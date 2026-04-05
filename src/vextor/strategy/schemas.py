import pandas as pd
import pandera.pandas as pa
import numpy as np

SidesSchema = pa.DataFrameSchema(
    {
        r"^[A-Z]+$": pa.Column(checks=pa.Check.isin([0, 1, np.nan]), dtype=int, regex=True, required=True),
    },
    index=pa.Index(pd.Timestamp)
)
