import pathlib

import polars as pl
import pytest
from brownian_stock.repository.raw_brand_repository import preprocess_before_insert
from brownian_stock.schemas import SymbolSchema, cast, validate


@pytest.fixture
def symbol_df() -> pl.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "brand.csv"
    df = pl.read_csv(csv_path)
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_symbol_schema(symbol_df: pl.DataFrame):
    df = symbol_df.to_pandas()

    assert not validate(df, SymbolSchema)
    cast_df = cast(df, SymbolSchema)
    print(cast_df)
    assert validate(cast_df, SymbolSchema)
    assert len(cast_df) == len(df)


def test_symbol_value_check(symbol_df: pl.DataFrame):
    cast_df = preprocess_before_insert(symbol_df)

    row = cast_df[cast_df["Code"] == "95310"].squeeze()
    assert row["CompanyName"] == "東京瓦斯"
    assert row["CompanyNameEnglish"] == "TOKYO GAS CO.,LTD."

    assert row["Sector17Code"] == "11"
    assert row["Sector17CodeName"] == "電気・ガス"
    assert row["Sector33Code"] == "4050"
    assert row["Sector33CodeName"] == "電気･ガス業"
    assert row["ScaleCategory"] == "TOPIX Mid400"
    assert row["MarketCode"] == "111"
    assert row["MarketCodeName"] == "プライム"
    assert row["MarginCode"] == "2"
    assert row["MarginCodeName"] == "貸借"

    # Record which contains null
    # TODO: This isn't expected behavior. We should fix this.
    row = cast_df[cast_df["Code"] == "95520"].squeeze()
    assert row["ScaleCategory"] == "None"
