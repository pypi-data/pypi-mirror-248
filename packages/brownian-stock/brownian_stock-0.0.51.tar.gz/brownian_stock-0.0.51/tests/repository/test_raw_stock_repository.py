import datetime
import pathlib
import tempfile

import polars as pl
import pytest
from brownian_stock.repository import RawStockRepository, RepositoryPath


@pytest.fixture
def stock_df() -> pl.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "2022-04-01.csv"
    df = pl.read_csv(csv_path)
    df = df.drop(df.columns[0])
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_raw_stock_repository(stock_df):
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = RawStockRepository(repo_path)

        # テーブルを正しく作成できるか判定
        assert not repository.table_exists()
        repository.create_table()
        assert repository.table_exists()

        # データの挿入, 存在チェックが正しく動作するか
        assert not repository.has_records(datetime.date(2022, 4, 1))
        repository.insert_daily_df(stock_df.clone())
        assert repository.has_records(datetime.date(2022, 4, 1))

        # データ数が1以上であることを確認
        size = repository.records_size()
        assert size > 0

        # 誤って２回挿入されないことを確認
        repository.insert_daily_df(stock_df.clone())
        assert repository.records_size() == size

        # インデックスを張れるか
        repository.set_index()
        repository.drop_index()


def test_raw_stock_repository_schema_change(stock_df):
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = RawStockRepository(repo_path)

        # テーブルを正しく作成できるか判定
        assert not repository.table_exists()
        repository.create_table()
        assert repository.table_exists()

        # データの挿入, 存在チェックが正しく動作するか
        assert not repository.has_records(datetime.date(2022, 4, 1))
        stock_df = stock_df.with_columns(pl.lit("DUMMY").alias("DUMMY"))
        stock_df = stock_df.clone()
        repository.insert_daily_df(stock_df)
        assert repository.has_records(datetime.date(2022, 4, 1))

        # データ数が1以上であることを確認
        size = repository.records_size()
        assert size > 0

        # 誤って２回挿入されないことを確認
        repository.insert_daily_df(stock_df.clone())
        assert repository.records_size() == size

        # インデックスを張れるか
        repository.set_index()
        repository.drop_index()
