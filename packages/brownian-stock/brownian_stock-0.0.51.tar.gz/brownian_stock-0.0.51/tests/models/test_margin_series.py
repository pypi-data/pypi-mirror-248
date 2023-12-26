import datetime
import pathlib

import pandas as pd
import polars as pl
from brownian_stock import MarginSeries, schemas


def test_margin_series(tmp_path: pathlib.Path):
    df_path = pathlib.Path(__file__).parent.parent / "data" / "margin_interest_95310.csv"

    raw_df = pd.read_csv(df_path)
    print(raw_df)
    raw_df = schemas.cast(raw_df, schemas.MarginInterestSchema)
    df = pl.from_dataframe(raw_df)
    series = MarginSeries(df, _skip_validation=True)

    assert series.latest_value("Date", datetime.date(2023, 5, 26)) == datetime.date(2023, 5, 26)
    assert series.latest_value("LongMarginTradeVolume", datetime.date(2023, 1, 4)) == 219700
    assert series.latest_value("LongMarginTradeVolume", datetime.date(2023, 1, 4), 2) == 231900
    assert series.latest_value("LongMarginTradeVolume", datetime.date(2023, 1, 4), 3) == 204700
