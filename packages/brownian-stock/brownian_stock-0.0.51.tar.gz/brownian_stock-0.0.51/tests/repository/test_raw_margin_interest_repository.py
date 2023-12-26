import datetime
import pathlib
import tempfile

import polars as pl
import pytest
from brownian_stock.repository import RawMarginInterestRepository, RepositoryPath


@pytest.fixture
def margin_df() -> pl.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "margin_interest_2022-03-11.csv"
    df = pl.read_csv(csv_path)
    df = df.with_columns(pl.col("Date").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_raw_margin_interest_repository(margin_df: pl.DataFrame):
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = RawMarginInterestRepository(repo_path)

        # テーブルを正しく作成できるか判定
        assert not repository.table_exists()
        repository.create_table()
        assert repository.table_exists()

        # データの挿入, 存在チェックが正しく動作するか
        assert not repository.has_records(datetime.date(2022, 3, 11))
        repository.insert_df(margin_df.clone())
        assert repository.has_records(datetime.date(2022, 3, 11))

        # データ数が1以上であることを確認
        size = repository.records_size()
        assert size > 0

        # 誤って２回挿入されないことを確認
        repository.insert_df(margin_df.clone())
        assert repository.records_size() == size

        # インデックスを張れるか
        repository.set_index()
        repository.drop_index()


def test_raw_margin_interest_repository_schema_changed(margin_df: pl.DataFrame):
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = RawMarginInterestRepository(repo_path)

        # テーブルを正しく作成できるか判定
        assert not repository.table_exists()
        repository.create_table()
        assert repository.table_exists()

        # データの挿入, 存在チェックが正しく動作するか
        assert not repository.has_records(datetime.date(2022, 3, 11))
        margin_df = margin_df.with_columns(pl.lit("DUMMY").alias("DUMMY"))
        repository.insert_df(margin_df.clone())
        assert repository.has_records(datetime.date(2022, 3, 11))

        # データ数が1以上であることを確認
        size = repository.records_size()
        assert size > 0

        # 誤って２回挿入されないことを確認
        repository.insert_df(margin_df.clone())
        assert repository.records_size() == size

        # インデックスを張れるか
        repository.set_index()
        repository.drop_index()
