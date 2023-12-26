import pathlib
import tempfile

import pandas as pd
import polars as pl
import pytest
from brownian_stock.repository import BrandRepository, RawBrandRepository, RepositoryPath


@pytest.fixture
def brand_df() -> pd.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "brand.csv"
    df = pl.read_csv(csv_path)
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_brand_repository(brand_df) -> None:
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        raw_repository = RawBrandRepository(repo_path)
        raw_repository.create_table()
        raw_repository.insert_brand_df(brand_df)

        repository = BrandRepository(repo_path)
        symbols = repository.load()
        symbols_dict = {s.code: s for s in symbols}

        print(symbols_dict.keys())
        symbol = symbols_dict["95310"]
        assert symbol.company_name == "東京瓦斯"

        assert symbol.company_name == "東京瓦斯"
        assert symbol.company_name_english == "TOKYO GAS CO.,LTD."

        assert symbol.sector17 == "11"
        assert symbol.sector33 == "4050"
        assert symbol.scale_category == "TOPIX Mid400"
        assert symbol.market_code == "111"
        assert symbol.margin_code == "2"
