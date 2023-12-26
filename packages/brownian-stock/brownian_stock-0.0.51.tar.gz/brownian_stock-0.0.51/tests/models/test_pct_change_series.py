import datetime
import pathlib

import brownian_stock
from brownian_stock import const


def test_stock_pct_change():
    # Success Case
    filepath = pathlib.Path(__file__).parent.parent / "data" / "stock_86970.csv"
    stock_series = brownian_stock.load_stock_series(filepath)
    start_date = datetime.date(2021, 4, 1)
    subset = stock_series.subset_by_after_n_days(start_date, 19)
    pct_change = subset.pct_change()

    # 初日の数字がすべて0になっていることをテスト
    close0 = pct_change.get_value(start_date, const.COL_CLOSE)
    open0 = pct_change.get_value(start_date, const.COL_OPEN)
    low0 = pct_change.get_value(start_date, const.COL_LOW)
    high0 = pct_change.get_value(start_date, const.COL_HIGH)
    assert close0 == 0
    assert open0 == 0
    assert low0 == 0
    assert high0 == 0

    # 主要な関数が正しく呼べるか
    pct_change.to_list(const.COL_CLOSE)
    pct_change.to_array(const.COL_CLOSE)
    pct_change.to_series(const.COL_CLOSE)
