import datetime
import pathlib
from unittest import mock

import polars as pl
from brownian_stock.commands.download import DailyStockCrawler
from brownian_stock.repository import RepositoryPath

DUMMMY_DF = pl.DataFrame(
    {
        "Date": ["2022-01-01", "2022-01-02"],
        "Code": ["00000", "11111"],
    }
)


@mock.patch("brownian_stock.services.jquants.download_daily_stock", return_value=DUMMMY_DF)
def test_daily_stock_crawler(func_mock: mock.MagicMock, tmp_path: pathlib.Path):
    repo_path = RepositoryPath(tmp_path)
    auth_mock = mock.MagicMock()

    # First time crawling
    crawl_start = datetime.date(2023, 6, 1)
    crawl_end = datetime.date(2023, 6, 30)
    crawler = DailyStockCrawler(repo_path, auth_mock, crawl_start=crawl_start, crawl_end=crawl_end)
    crawler.crawl(interval=0)
    assert func_mock.call_count == 22

    # Second time crawling
    # call count should not increase because cache are enabled.
    crawler.crawl(interval=0)
    assert func_mock.call_count == 22
