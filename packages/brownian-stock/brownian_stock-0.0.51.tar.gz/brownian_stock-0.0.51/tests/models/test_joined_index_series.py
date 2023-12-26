import datetime

import brownian_stock
import numpy as np
import pandas as pd
import polars as pl


def test_joined_index_series_basic() -> None:
    # JinedIndexSeriesの基本的な機能をテストする
    # 日付が同じ2個のIndexをつなげた場合
    index_dict = {}
    base_date = datetime.date(2022, 10, 1)
    for i in range(2):
        date_ls = [base_date + datetime.timedelta(days=j) for j in range(9)]
        value_ls = list(range(1, 10))
        index = brownian_stock.IndexSeries(date_ls, value_ls)
        index_dict[str(i)] = index

    # 各種取得コードの型が妥当か検証する
    joined_index = brownian_stock.JoinedIndexSeries(index_dict, how="inner")
    assert isinstance(joined_index.to_list("0"), list)
    assert isinstance(joined_index.to_array("0"), np.ndarray)
    assert isinstance(joined_index.to_series("0"), pd.Series)
    assert isinstance(joined_index.to_series("0", to_polars=True), pl.Series)


def test_joined_index_series_inner() -> None:
    # JinedIndexSeriesのinnerでの挙動が妥当か検証する
    # 日付が同じ10個のIndexをつなげた場合
    index_dict = {}
    base_date = datetime.date(2022, 10, 1)
    for i in range(10):
        date_ls = [base_date + datetime.timedelta(days=j) for j in range(10)]
        value_ls = [i] * 10
        index = brownian_stock.IndexSeries(date_ls, value_ls)
        index_dict[str(i)] = index

    joined_index = brownian_stock.JoinedIndexSeries(index_dict, how="inner")
    assert len(joined_index._df) == 10
    assert len(joined_index.available_keys) == 10

    assert joined_index.latest_value("0") == 0
    assert joined_index.latest_value("9") == 9

    # 日付が異なるのIndexをつなげた場合
    index_dict = {}
    base_date = datetime.date(2022, 10, 1)
    for i in range(10):
        d = base_date + datetime.timedelta(days=i)
        date_ls = [d + datetime.timedelta(days=j) for j in range(20)]
        value_ls = [i] * 20
        index = brownian_stock.IndexSeries(date_ls, value_ls)
        index_dict[str(i)] = index

    # Innerで結合した場合に残るのは11日分
    joined_index = brownian_stock.JoinedIndexSeries(index_dict, how="inner")
    assert len(joined_index._df) == 11
    assert len(joined_index.available_keys) == 10

    # 欠損無くデータを取得できるはず
    assert joined_index.oldest_value("0") == 0
    assert joined_index.latest_value("0") == 0
    assert joined_index.oldest_value("9") == 9
    assert joined_index.latest_value("9") == 9


def test_joined_index_series_outer() -> None:
    # JinedIndexSeriesの基本的な機能をテストする
    # 日付が同じ10個のIndexをつなげた場合
    index_dict = {}
    base_date = datetime.date(2022, 10, 1)
    for i in range(10):
        date_ls = [base_date + datetime.timedelta(days=j) for j in range(10)]
        value_ls = [i] * 10
        index = brownian_stock.IndexSeries(date_ls, value_ls)
        index_dict[str(i)] = index

    joined_index = brownian_stock.JoinedIndexSeries(index_dict, how="outer")
    assert len(joined_index._df) == 10
    assert len(joined_index.available_keys) == 10

    assert joined_index.latest_value("0") == 0
    assert joined_index.latest_value("9") == 9

    # 日付が異なるのIndexをつなげた場合
    index_dict = {}
    base_date = datetime.date(2022, 10, 1)
    for i in range(10):
        d = base_date + datetime.timedelta(days=i)
        date_ls = [d + datetime.timedelta(days=j) for j in range(10)]
        value_ls = [i] * 10
        index = brownian_stock.IndexSeries(date_ls, value_ls)
        index_dict[str(i)] = index

    joined_index = brownian_stock.JoinedIndexSeries(index_dict, how="outer")
    assert len(joined_index._df) == 19
    assert len(joined_index.available_keys) == 10

    assert joined_index.oldest_value("0") == 0
    assert joined_index.latest_value("0") is None

    assert joined_index.oldest_value("9") is None
    assert joined_index.latest_value("9") == 9


def test_pct_change() -> None:
    # JinedIndexSeriesの基本的な機能をテストする
    # 日付が同じ2個のIndexをつなげた場合
    # 長さ9の公差1の等差数列
    index_dict = {}
    base_date = datetime.date(2022, 10, 1)
    for i in range(2):
        date_ls = [base_date + datetime.timedelta(days=j) for j in range(9)]
        value_ls = list(range(1, 10))
        index = brownian_stock.IndexSeries(date_ls, value_ls)
        index_dict[str(i)] = index

    # 差分を取ることで長さが1減る
    joined_index = brownian_stock.JoinedIndexSeries(index_dict, how="inner")
    joined_index = joined_index.pct_change()
    assert len(joined_index._df) == 8
    assert len(joined_index.available_keys) == 2

    # 最初の項は1->2なので2倍
    assert joined_index.oldest_value("0") == 1
    assert joined_index.oldest_value("1") == 1

    # 最後の項は8-9なので約1.125
    assert joined_index.latest_value("0") == 0.125
    assert joined_index.latest_value("1") == 0.125

    # 欠損がある場合
    index_dict = {}
    base_date = datetime.date(2022, 10, 1)
    for i in range(2):
        date_ls = [base_date + datetime.timedelta(days=j) for j in range(9)]
        value_ls = list(range(1, 10))
        index = brownian_stock.IndexSeries(date_ls, value_ls)
        index_dict[str(i)] = index

    # 結合して欠損値を挿入. 欠損の場所派10/4
    joined_index = brownian_stock.JoinedIndexSeries(index_dict, how="inner")
    joined_index._df[4, "0"] = None
    joined_index = joined_index.pct_change()

    assert len(joined_index._df) == 8
    assert joined_index.get_value(datetime.date(2022, 10, 5), "0") is None
    assert joined_index.get_value(datetime.date(2022, 10, 6), "0") == 0.5
