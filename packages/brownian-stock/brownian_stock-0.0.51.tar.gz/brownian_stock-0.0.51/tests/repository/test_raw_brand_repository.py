import pathlib
import tempfile

import pandas as pd
import polars as pl
import pytest
from brownian_stock.repository import RawBrandRepository, RepositoryPath


@pytest.fixture
def brand_df() -> pd.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "brand.csv"
    df = pl.read_csv(csv_path)
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_raw_brand_repository(brand_df) -> None:
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = RawBrandRepository(repo_path)

        # テーブルを正しく作成できるか判定
        assert not repository.table_exists()
        repository.create_table()
        assert repository.table_exists()

        # データの挿入, 存在チェックが正しく動作するか
        repository.insert_brand_df(brand_df.clone())

        # データ数が1以上であることを確認
        size = repository.records_size()
        assert size > 0

        # 誤って２回挿入されないことを確認
        repository.insert_brand_df(brand_df.clone())
        assert repository.records_size() == size

        # カラムが増えても挿入できることを確認
        brand_df = brand_df.with_columns(pl.lit("dummy").alias("dummy"))
        repository.insert_brand_df(brand_df.clone())
        assert repository.records_size() == size
