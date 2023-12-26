import datetime
import pathlib

import brownian_stock
import pytest
from brownian_stock import const


def test_neutralize_stock() -> None:
    """StockSeriesの中立化がうまく計算できているか確認する"""
    filepath = pathlib.Path(__file__).parent.parent / "data" / "stock_86970.csv"
    stock_series = brownian_stock.load_stock_series(filepath)
    stock_series = stock_series.subset_by_range(datetime.date(2022, 4, 1), datetime.date(2022, 4, 5))

    date_ls = [datetime.date(2022, 4, 1), datetime.date(2022, 4, 4), datetime.date(2022, 4, 5)]
    value_ls = [2273.5, 2323, 2325.5]
    index_series = brownian_stock.IndexSeries(date_ls, value_ls)

    # value_lsとしてOpenの数字を選んでいるので中立化されれば0になるはず
    neutralized = brownian_stock.neutralize.neutralize_stock(stock_series, index_series)
    one_list = neutralized.to_list(const.COL_OPEN)

    assert len(one_list) == 3
    for v in one_list:
        assert pytest.approx(0, abs=0.01) == v


def test_neutralize_index() -> None:
    """StockSeriesの中立化がうまく計算できているか確認する"""

    date_ls = [datetime.date(2022, 4, 1), datetime.date(2022, 4, 4), datetime.date(2022, 4, 5)]
    value_ls = [2273.5, 2323, 2325.5]
    index_series = brownian_stock.IndexSeries(date_ls, value_ls)

    # value_lsとしてOpenの数字を選んでいるので中立化されれば0になるはず
    neutralized = brownian_stock.neutralize.neutralize_index(index_series, index_series)
    one_list = neutralized.to_list()

    assert len(one_list) == 3
    for v in one_list:
        assert pytest.approx(0, abs=0.01) == v
