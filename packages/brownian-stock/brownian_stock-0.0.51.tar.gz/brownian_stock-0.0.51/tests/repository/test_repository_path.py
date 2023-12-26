import io
import pathlib
import tempfile

import polars as pl
import pytest
from brownian_stock.repository import RepositoryPath, S3RepositoryPath


@pytest.mark.skip
def test_s3_repository_path():
    with tempfile.TemporaryDirectory() as dirname:
        # "test-bucket-for-brownian-walker" is a dummy bucket
        db_path = pathlib.Path(dirname) / "db.sqlite3"
        repo = S3RepositoryPath("test-bucket-for-brownian-walker", db_path, region="ap-northeast-1")

        df = pl.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        repo.save_df("stock", "test_file.csv", df)

        stream = io.BytesIO()
        repo.save_stream("stock", "test_stream.csv", stream)
        df = repo.read_df("stock", "test_file.csv")
        repo.list_dir("stock")


def test_repository_property():
    # In case not specify connection_str
    repo = RepositoryPath("/home/user/jquants")
    assert str(repo.sqlite_path) == "/home/user/jquants/sqlite3.db"
    assert str(repo.connection_str) == "sqlite:////home/user/jquants/sqlite3.db"

    # In case specify connection_str
    connection_str = "sqlite:////test/directory/sqlite3.db"
    repo = RepositoryPath("xxxx", connection_str)
    assert str(repo.sqlite_path) == "/test/directory/sqlite3.db"


def test_s3_repository_property():
    # In case specify connection_str
    connection_str = "sqlite:////test/directory/db.sqlite"
    repo = S3RepositoryPath("xxxx", connection_str, region="ap-northeast-1")
    assert str(repo.sqlite_path) == "/test/directory/db.sqlite"
