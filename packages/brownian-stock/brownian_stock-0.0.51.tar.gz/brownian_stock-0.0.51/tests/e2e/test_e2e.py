import logging
import os
import pathlib

import pytest
from brownian_stock.main import main
from brownian_stock.repository import (
    MarginInterestSQLRepository,
    RepositoryPath,
    StatementsSQLRepository,
    StockSQLRepository,
)


@pytest.mark.e2e
def test_e2e_local(tmp_path: pathlib.Path):
    # Run download command.
    logging.info("Running `download` command.")
    repo_dir = tmp_path / "repository"
    download_args = ["download", "--dir_path", str(repo_dir), "--limit", "5"]
    main(download_args)

    # Run generate command.
    logging.info("Running `generate` command.")
    generate_args = ["generate", "--dir_path", str(repo_dir)]
    main(generate_args)

    repo_dir = RepositoryPath(repo_dir)
    stock_repo = StockSQLRepository(repo_dir)
    stock_repo.load()

    statement_repo = StatementsSQLRepository(repo_dir)
    statement_repo.load()


@pytest.mark.e2e
def test_e2e_sql(caplog):
    path = os.path.expanduser("~/Document/jquants5")
    repo = RepositoryPath(path)
    statement_repo = StatementsSQLRepository(repo)

    statement_repo.load()
    records = [r for r in caplog.records if r.levelname == "ERROR"]
    assert len(records) == 0


@pytest.mark.e2e
def test_e2e_margin_interest(caplog):
    path = os.path.expanduser("~/Document/jquants5")
    repo = RepositoryPath(path)
    margin_repo = MarginInterestSQLRepository(repo)

    margin_dict = margin_repo.load(limit=5)
    records = [r for r in caplog.records if r.levelname == "ERROR"]
    assert len(records) == 0
    assert len(margin_dict) == 5
