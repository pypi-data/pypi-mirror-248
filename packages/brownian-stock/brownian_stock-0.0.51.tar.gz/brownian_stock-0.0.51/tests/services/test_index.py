import pathlib

import brownian_stock
from brownian_stock import const


def load_stock(code: str) -> brownian_stock.StockSeries:
    """ダミーの株価を読み込むための補助関数"""
    filepath = pathlib.Path(__file__).parent.parent / "data" / "stock_86970.csv"
    s = brownian_stock.load_stock_series(filepath)
    s.stock_code = code
    return s


def test_average_index() -> None:
    """単純平均の指標計算が正しくできるか検証する"""

    s1 = load_stock("00000")
    s2 = load_stock("00001")
    s3 = load_stock("00002")

    stock_set = brownian_stock.StockSet([s1, s2, s3])
    index = brownian_stock.average_index(stock_set)
    base_list = s1.to_series(const.COL_CLOSE)
    index_list = index.to_series()
    assert (base_list == index_list).all()
