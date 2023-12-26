import datetime

import brownian_stock
import pytest


def test_index_series():
    # Success Case
    dates = []
    values = []
    today = datetime.date(2022, 4, 1)
    for i in range(10):
        dates.append(today + datetime.timedelta(days=i))
        values.append(i)
    index_series = brownian_stock.IndexSeries(dates, values)

    # get_value関数が機能するかどうか
    price = index_series.get_value(datetime.date(2022, 4, 1))
    assert price == 0

    # get_value関数が機能するかどうか
    price = index_series.get_value(datetime.date(2022, 4, 10))
    assert price == 9

    # 主要な関数が正しく呼べるか
    index_series.to_list()
    index_series.to_array()
    index_series.to_series()

    # 異常値の検証
    # 異なる長さのシークエンスを渡す
    with pytest.raises(ValueError):
        brownian_stock.IndexSeries([], [1, 2, 3])

    # Date以外のものを渡す
    with pytest.raises(ValueError):
        brownian_stock.IndexSeries([datetime.datetime.now()], [1])


def test_index_subset():
    dates = []
    values = []
    today = datetime.date(2022, 4, 1)
    for i in range(100):
        dates.append(today + datetime.timedelta(days=i))
        values.append(i)
    index_series = brownian_stock.IndexSeries(dates, values)

    subset = index_series.subset_by_recent_n_days(datetime.date(2022, 6, 1), 20).to_list()
    assert len(subset) == 20

    subset = index_series.subset_by_after_n_days(datetime.date(2022, 6, 1), 20).to_list()
    assert len(subset) == 20


def test_index_series_pct_change():
    # Success Case
    dates = []
    values = []

    value = 1
    today = datetime.date(2022, 4, 1)
    for i in range(10):
        dates.append(today + datetime.timedelta(days=i))
        values.append(value)
        value = value * 1.1
    index_series = brownian_stock.IndexSeries(dates, values)
    pct_series = index_series.pct_change()

    ls = pct_series.to_list()
    assert ls[0] == pytest.approx(0.0, abs=0.01)
    assert ls[1] == pytest.approx(0.1, abs=0.01)
    assert ls[2] == pytest.approx(0.1, abs=0.01)
