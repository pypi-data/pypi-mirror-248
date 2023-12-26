import datetime
import pathlib

import brownian_stock
import polars as pl
from brownian_stock import const
from brownian_stock.models.stock_series import clean_dataframe


def test_stock() -> None:
    # Success Case
    filepath = pathlib.Path(__file__).parent.parent / "data" / "stock_86970.csv"
    stock_series = brownian_stock.load_stock_series(filepath)

    # get_value関数が機能するかどうか
    price = stock_series.get_value(datetime.date(2022, 4, 1), const.COL_CLOSE)
    assert price == 2323.5
    price = stock_series.get_value(datetime.date(2022, 4, 3), const.COL_CLOSE)
    assert price is None

    price = stock_series.get_value(datetime.date(2022, 10, 1), const.COL_CLOSE)
    assert price is None

    # latest_atが正しく動作するか
    price = stock_series.latest_value(const.COL_CLOSE, at=datetime.date(2022, 4, 1))
    assert price == 2323.5
    # 4/2, 4/3は休日なので4/1を正しく参照できることを確認
    price = stock_series.latest_value(const.COL_CLOSE, at=datetime.date(2022, 4, 3))
    assert price == 2323.5

    # has_recordが正常に機能するかどうか
    assert stock_series.has_record(datetime.date(2022, 4, 1))
    assert not stock_series.has_record(datetime.date(2022, 4, 2))

    # 主要な関数が正しく呼べるか
    stock_series.to_list(const.COL_CLOSE)
    stock_series.to_array(const.COL_CLOSE)
    stock_series.to_series(const.COL_CLOSE)

    # 二分探索がうまく動作しているかどうか
    # エッジケース1. 最初の日
    d = datetime.date(2017, 1, 4)
    idx = stock_series._binary_search_left(d)
    assert stock_series._df[idx, const.COL_DATE] == d

    # エッジケース2. 最後の日
    d = datetime.date(2023, 2, 17)
    idx = stock_series._binary_search_left(d)
    assert stock_series._df[idx, const.COL_DATE] == d

    # エッジケース3. 外挿
    d = datetime.date(2023, 2, 18)
    idx = stock_series._binary_search_left(d)
    assert idx == len(stock_series._df)


def test_clean_data() -> None:
    """入力されたCSVの前処理がうまく行くか"""
    df = pl.DataFrame(
        {
            const.COL_CLOSE: [None, 100, None, 100],
            const.COL_OPEN: [None, 100, None, 100],
            const.COL_HIGH: [None, 200, None, 100],
            const.COL_LOW: [None, 50, None, 100],
            const.COL_TRADING_VOLUME: [None, 100, None, 100],
            const.COL_TURNOVER_VALUE: [None, 100, None, 100],
        }
    )
    df = clean_dataframe(df)

    assert all(df[const.COL_CLOSE] == [100, 100, 100])
    assert all(df[const.COL_OPEN] == [100, 100, 100])
    assert all(df[const.COL_HIGH] == [200, 100, 100])
    assert all(df[const.COL_LOW] == [50, 100, 100])
    assert all(df[const.COL_TRADING_VOLUME] == [100, 0, 100])
    assert all(df[const.COL_TURNOVER_VALUE] == [100, 0, 100])
