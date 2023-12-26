import pathlib

import polars as pl
import pytest
from brownian_stock.schemas import StockSchema, cast, validate


@pytest.fixture
def stock_df() -> pl.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "2022-04-01.csv"
    df = pl.read_csv(csv_path)
    df = df.drop(df.columns[0])
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_stock_schema(stock_df: pl.DataFrame):
    df = stock_df.to_pandas()

    assert not validate(df, StockSchema)
    cast_df = cast(df, StockSchema)
    print(cast_df)
    assert validate(cast_df, StockSchema)
    assert len(cast_df) == len(df)
