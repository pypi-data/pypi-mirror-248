import pathlib

import pandas as pd
from brownian_stock import IndexSeries, StockSeries, StockSet, const, universe


def stock_percent_change(s: StockSeries):
    close_series = s.df[const.COL_CLOSE]  # / s.df[const.COL_OPEN]
    return close_series


def compute_market_index(stock_set: StockSet, change=False) -> IndexSeries:
    """市場全体の値動きを表す数字を作成"""
    brand_dict = {}
    for s in stock_set:
        if change:
            series = s.to_series(const.COL_CLOSE) / s.to_series(const.COL_OPEN)
            series -= 1
        else:
            series = s.to_series(const.COL_CLOSE)
        brand_dict[s.stock_code] = series
    df = pd.DataFrame(brand_dict)
    df.dropna(axis=1, inplace=True, how="any")
    brand_list = list(df.columns)

    # 最終日の出来高で重み付け平均
    weight = 0
    for s in stock_set:
        code = s.stock_code
        if code not in brand_list:
            continue
        volume = s.latest_value(const.COL_TRADING_VOLUME)
        df[code] *= volume
        weight += volume
    normalized = df.sum(axis=1) / weight
    normalized.name = "IndexValue"
    normalized = normalized.reset_index()
    index_series = IndexSeries(normalized)
    return index_series


cluster_dict = {}
cluster_dict_idx = {}
cluster_csv = pathlib.Path(__file__).parent / "clustering_result.csv"
cluster_df = pd.read_csv(cluster_csv)

for _, row in cluster_df.iterrows():
    code = str(row["Code"])
    cluster = row["Cluster"]
    cluster_dict_idx[code] = cluster


def code_to_cluster(code):
    v = cluster_dict_idx.get(code, None)
    if v is not None:
        return v
    return -1


def stockset_universe(stock_set):
    """実験で使うUniverseを抽出する"""
    # Universeの選択
    univ = universe.TopixSmall1()
    stock_set = stock_set.filter(univ)
    # stock_set = stock_set.filter(lambda s: code_to_cluster(s.stock_code) == 3)
    print(len(stock_set))
    return stock_set
