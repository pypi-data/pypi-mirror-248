import pathlib
import tempfile

import pandas as pd
import polars as pl
import pytest
from brownian_stock.repository import (
    MarginInterestSQLRepository,
    RawBrandRepository,
    RawMarginInterestRepository,
    RepositoryPath,
)


@pytest.fixture
def margin_df() -> pl.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "margin_interest_2022-03-11.csv"
    df = pl.read_csv(csv_path)
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


@pytest.fixture
def brand_df() -> pl.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "brand.csv"
    df = pl.read_csv(csv_path)
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_margin_repository(margin_df: pl.DataFrame, brand_df: pl.DataFrame) -> None:
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        raw_repo = RawMarginInterestRepository(repo_path)
        raw_repo.create_table()
        raw_repo.insert_df(margin_df)

        brand_repo = RawBrandRepository(repo_path)
        brand_repo.create_table()
        brand_repo.insert_brand_df(brand_df)

        repo = MarginInterestSQLRepository(repo_path)
        loaded = repo.load()
        assert "95310" in loaded
