import pandas as pd
from brownian_stock import IndexSeries, StockSeries, StockSet, const


def stock_percent_change(s: StockSeries):
    close_series = s.df[const.COL_CLOSE]  # / s.df[const.COL_OPEN]
    return close_series


def compute_market_index(stock_set: StockSet, change=False) -> IndexSeries:
    """市場全体の値動きを表す数字を作成"""
    brand_dict = {}
    for s in stock_set:
        if change:
            series = s.df[const.COL_CLOSE] / s.df[const.COL_OPEN]
            series -= 1
        else:
            series = s.df[const.COL_CLOSE]
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


def filter_universe(subset):
    pass
