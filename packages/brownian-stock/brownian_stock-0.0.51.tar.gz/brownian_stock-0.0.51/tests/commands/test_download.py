import pathlib
import unittest

import dacite
import polars as pl
import pytest

from brownian_stock.commands.download import DownloadArgs, run_download
from brownian_stock.main import get_parser


def test_command_args() -> None:
    args_dict = {
        "dir_path": "./test_dir",
        "only_stock": False,
        "only_brand": False,
        "only_statements": False,
        "only_yahoo": False,
        "only_margin_interests": False,
        "limit": 10,
        "dot_path": ".brownianrc",
        "username": None,
        "password": None,
        "interval": 1,
        "force": False,
    }
    args = dacite.from_dict(DownloadArgs, args_dict)
    args.validate()
    assert args.do_brand
    assert args.do_stock
    assert args.do_statements
    assert args.do_yahoo
    assert args.do_margin_interests
    assert args.dot_path == ".brownianrc"
    assert args.username is None
    assert args.password is None
    assert args.interval == 1
    assert not args.force


def test_invalid_command_args() -> None:
    # Mutliple only flag
    args_dict = {
        "dir_path": "./test_dir",
        "only_stock": True,
        "only_brand": True,
        "only_statements": False,
        "only_yahoo": False,
        "only_margin_interests": False,
        "limit": 10,
        "dot_path": ".brownianrc",
        "username": None,
        "password": None,
        "interval": 1,
        "force": False,
    }
    args = dacite.from_dict(DownloadArgs, args_dict)
    with pytest.raises(ValueError):
        args.validate()

    args_dict = {
        "dir_path": "./test_dir",
        "only_stock": False,
        "only_brand": False,
        "only_statements": False,
        "only_yahoo": False,
        "only_margin_interests": False,
        "limit": 10,
        "dot_path": ".brownianrc",
        "username": "test_user",
        "password": "test_password",
        "interval": 1,
        "force": False,
    }
    args = dacite.from_dict(DownloadArgs, args_dict)
    with pytest.raises(ValueError):
        args.validate()


def test_stock_download(tmp_path: pathlib.Path):
    dummy_df = pl.DataFrame({"dummy": [1, 2, 3]})

    login_patcher = unittest.mock.patch("brownian_stock.services.jquants.JquantsAuthToken")
    download_patcher = unittest.mock.patch(
        "brownian_stock.services.jquants.download_daily_stock", return_value=dummy_df
    )
    login_mock = login_patcher.start()
    login_mock.login_token.return_value = ""
    login_mock.refresh_token.return_value = ""
    download_mock = download_patcher.start()

    # First time line. There will be 10 files in the raw_stock directory.
    parser = get_parser()
    args = parser.parse_args(
        [
            "download",
            "--dir_path",
            str(tmp_path),
            "--interval",
            "0",
            "--only_stock",
            "--limit",
            "10",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )
    run_download(args)
    assert download_mock.call_count == 10

    stock_dir = tmp_path / "raw_stock"
    assert len(list(stock_dir.iterdir())) == 10

    # Second time line. There will be 20 files in the raw_stock directory.
    run_download(args)
    assert download_mock.call_count == 20

    stock_dir = tmp_path / "raw_stock"
    assert len(list(stock_dir.iterdir())) == 20

    # With `force` run . There will be 20 files in the raw_stock directory.
    # In this case, file count would not be increased because try to download all files again.
    parser = get_parser()
    args = parser.parse_args(
        [
            "download",
            "--dir_path",
            str(tmp_path),
            "--interval",
            "0",
            "--only_stock",
            "--limit",
            "10",
            "--force",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )
    run_download(args)
    assert download_mock.call_count == 30

    stock_dir = tmp_path / "raw_stock"
    assert len(list(stock_dir.iterdir())) == 20


def test_statements_download(tmp_path: pathlib.Path):
    dummy_df = pl.DataFrame({"dummy": [1, 2, 3]})

    login_patcher = unittest.mock.patch("brownian_stock.services.jquants.JquantsAuthToken")
    download_patcher = unittest.mock.patch(
        "brownian_stock.services.jquants.download_daily_statements", return_value=dummy_df
    )
    login_mock = login_patcher.start()
    login_mock.login_token.return_value = ""
    login_mock.refresh_token.return_value = ""
    download_mock = download_patcher.start()

    # First time line. There will be 10 files in the raw_stock directory.
    parser = get_parser()
    args = parser.parse_args(
        [
            "download",
            "--dir_path",
            str(tmp_path),
            "--interval",
            "0",
            "--only_statements",
            "--limit",
            "10",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )
    run_download(args)
    assert download_mock.call_count == 10

    stock_dir = tmp_path / "raw_statements"
    assert len(list(stock_dir.iterdir())) == 10

    # Second time line. There will be 20 files in the raw_stock directory.
    run_download(args)
    assert download_mock.call_count == 20

    stock_dir = tmp_path / "raw_statements"
    assert len(list(stock_dir.iterdir())) == 20

    # With `force` run . There will be 20 files in the raw_stock directory.
    # In this case, file count would not be increased because try to download all files again.
    parser = get_parser()
    args = parser.parse_args(
        [
            "download",
            "--dir_path",
            str(tmp_path),
            "--interval",
            "0",
            "--only_statements",
            "--limit",
            "10",
            "--force",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )
    run_download(args)
    assert download_mock.call_count == 30

    stock_dir = tmp_path / "raw_statements"
    assert len(list(stock_dir.iterdir())) == 20


def test_margin_interest_download(tmp_path: pathlib.Path):
    dummy_df = pl.DataFrame({"dummy": [1, 2, 3]})

    login_patcher = unittest.mock.patch("brownian_stock.services.jquants.JquantsAuthToken")
    download_patcher = unittest.mock.patch(
        "brownian_stock.services.jquants.download_daily_margin_interest", return_value=dummy_df
    )

    login_mock = login_patcher.start()
    login_mock.login_token.return_value = ""
    login_mock.refresh_token.return_value = ""
    download_mock = download_patcher.start()

    # First time line. There will be 10 files in the raw_stock directory.
    parser = get_parser()
    args = parser.parse_args(
        [
            "download",
            "--dir_path",
            str(tmp_path),
            "--interval",
            "0",
            "--only_margin_interest",
            "--limit",
            "10",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )
    run_download(args)
    assert download_mock.call_count == 10

    stock_dir = tmp_path / "raw_margin_interest"
    assert len(list(stock_dir.iterdir())) == 10

    # Second time line. There will be 20 files in the raw_stock directory.
    run_download(args)
    assert download_mock.call_count == 20

    stock_dir = tmp_path / "raw_margin_interest"
    assert len(list(stock_dir.iterdir())) == 20

    # With `force` run . There will be 20 files in the raw_stock directory.
    # In this case, file count would not be increased because try to download all files again.
    parser = get_parser()
    args = parser.parse_args(
        [
            "download",
            "--dir_path",
            str(tmp_path),
            "--interval",
            "0",
            "--only_margin_interest",
            "--limit",
            "10",
            "--force",
            "--username",
            "test_user",
            "--password",
            "test_password",
        ]
    )
    run_download(args)
    assert download_mock.call_count == 30

    stock_dir = tmp_path / "raw_margin_interest"
    assert len(list(stock_dir.iterdir())) == 20
