import datetime
import pathlib
import tempfile

import polars as pl
import pytest
from brownian_stock.repository import RawStatementsRepository, RepositoryPath


@pytest.fixture
def statements_df() -> pl.DataFrame:
    csv_path = pathlib.Path(__file__).parent.parent / "data" / "statements_2022-04-04.csv"
    df = pl.read_csv(csv_path)
    df = df.with_columns(pl.col("DisclosedDate").str.strptime(pl.Date, format="%Y-%m-%d"))
    return df


def test_raw_statements_repository(statements_df: pl.DataFrame):
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = RawStatementsRepository(repo_path)

        # テーブルを正しく作成できるか判定
        assert not repository.table_exists()
        repository.create_table()
        assert repository.table_exists()

        # データの挿入, 存在チェックが正しく動作するか
        assert not repository.has_records(datetime.date(2022, 4, 4))
        repository.insert_statements_df(statements_df.clone())
        assert repository.has_records(datetime.date(2022, 4, 4))

        # データ数が1以上であることを確認
        size = repository.records_size()
        assert size > 0

        # 誤って２回挿入されないことを確認
        repository.insert_statements_df(statements_df.clone())
        assert repository.records_size() == size

        # インデックスを張れるか
        repository.set_index()
        repository.drop_index()


def test_raw_statements_repository_schema_changed(statements_df: pl.DataFrame):
    with tempfile.TemporaryDirectory() as dirname:
        repo_path = RepositoryPath(dirname)
        repository = RawStatementsRepository(repo_path)

        # テーブルを正しく作成できるか判定
        assert not repository.table_exists()
        repository.create_table()
        assert repository.table_exists()

        # データの挿入, 存在チェックが正しく動作するか
        assert not repository.has_records(datetime.date(2022, 4, 4))
        statements_df = statements_df.with_columns(pl.lit("DUMMY").alias("DUMMY"))
        repository.insert_statements_df(statements_df.clone())
        assert repository.has_records(datetime.date(2022, 4, 4))

        # データ数が1以上であることを確認
        size = repository.records_size()
        assert size > 0

        # 誤って２回挿入されないことを確認
        repository.insert_statements_df(statements_df.clone())
        assert repository.records_size() == size

        # インデックスを張れるか
        repository.set_index()
        repository.drop_index()
