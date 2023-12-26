import pathlib
from unittest import mock

import polars as pl
from brownian_stock.commands.download import BrandCrawler
from brownian_stock.repository import RepositoryPath

DUMMMY_DF = pl.DataFrame(
    {
        "Date": ["2022-01-01", "2022-01-02"],
        "Code": ["00000", "11111"],
    }
)


@mock.patch("brownian_stock.services.jquants.download_brand", return_value=DUMMMY_DF)
def test_daily_stock_crawler(func_mock: mock.MagicMock, tmp_path: pathlib.Path):
    repo_path = RepositoryPath(tmp_path)
    auth_mock = mock.MagicMock()

    # First time crawling
    crawler = BrandCrawler(repo_path, auth_mock)
    crawler.crawl()
    assert func_mock.call_count == 1
