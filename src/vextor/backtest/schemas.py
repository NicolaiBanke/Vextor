import pandas as pd
import pandera.pandas as pa


AssetsSchema = pa.DataFrameSchema(
    {
        ("Close", r"^[A-Z]+$"): pa.Column(checks=pa.Check.gt(0.0), dtype=float, regex=True, required=True),
        ("High", r"^[A-Z]+$"): pa.Column(checks=pa.Check.gt(0.0), dtype=float, regex=True, required=True),
        ("Low", r"^[A-Z]+$"): pa.Column(checks=pa.Check.gt(0.0), dtype=float, regex=True, required=True),
        ("Open", r"^[A-Z]+$"): pa.Column(checks=pa.Check.gt(0.0), dtype=float, regex=True, required=True),
        ("Volume", r"^[A-Z]+$"): pa.Column(checks=pa.Check.gt(0.0), dtype=int, regex=True, required=True),
    },
    index=pa.Index(pd.Timestamp)
)
