import datetime
import pathlib

from brownian_stock import ReturnMap, StockSet, const, load_stock_series, trading


def test_long_only() -> None:
    """ロングオンリーの売買が妥当にできるかの検証"""
    file_list = [
        pathlib.Path(__file__).parent.parent / "data" / "stock_39110.csv",
        pathlib.Path(__file__).parent.parent / "data" / "stock_86970.csv",
    ]
    stock_list = []
    for path in file_list:
        stock_series = load_stock_series(path)
        stock_list.append(stock_series)
    stock_set = StockSet(stock_list)

    # 2つの銘柄のみで検証する. 始値での売買ケース
    # 86970が400株買われることを確認する
    # 3/31の終値は2286, 初値は2300
    trade_date = datetime.date(2022, 4, 1)
    return_map = ReturnMap()
    return_map["86970"] = 1
    return_map["39110"] = -1
    order = trading.long_only_trading(
        918000, trade_date, stock_set, return_map, timing=const.COL_OPEN, top_n=1, safety_margin=1.0
    )
    assert order.num_dict["86970"] == 300
    assert order.num_dict["39110"] == 0

    # 86970が400株買われることを確認する. 終値での売買ケース
    # 3/31の終値は2286, 初値は2300
    trade_date = datetime.date(2022, 4, 1)
    return_map = ReturnMap()
    return_map["86970"] = 1
    return_map["39110"] = -1
    order = trading.long_only_trading(
        918000, trade_date, stock_set, return_map, timing=const.COL_CLOSE, top_n=1, safety_margin=1.0
    )
    assert order.num_dict["86970"] == 400
    assert order.num_dict["39110"] == 0


def test_short_only() -> None:
    """ロングオンリーの売買が妥当にできるかの検証"""
    file_list = [
        pathlib.Path(__file__).parent.parent / "data" / "stock_39110.csv",
        pathlib.Path(__file__).parent.parent / "data" / "stock_86970.csv",
    ]
    stock_list = []
    for path in file_list:
        stock_series = load_stock_series(path)
        stock_list.append(stock_series)
    stock_set = StockSet(stock_list)

    # 39110が400株売られることを確認する
    # 始値での検証
    # 始値は323, 終値は329
    trade_date = datetime.date(2022, 4, 1)
    return_map = ReturnMap()
    return_map["86970"] = 0
    return_map["39110"] = -1
    order = trading.short_only_trading(
        130000, trade_date, stock_set, return_map, timing=const.COL_OPEN, top_n=1, safety_margin=1.0
    )
    assert order.num_dict["86970"] == 0
    assert order.num_dict["39110"] == -400

    # 39110が300株売られることを確認する
    # 終値での検証
    # 始値は323, 終値は329
    trade_date = datetime.date(2022, 4, 1)
    return_map = ReturnMap()
    return_map["86970"] = 1
    return_map["39110"] = -1
    order = trading.short_only_trading(
        130000, trade_date, stock_set, return_map, timing=const.COL_CLOSE, top_n=1, safety_margin=1.0
    )
    assert order.num_dict["86970"] == 0
    assert order.num_dict["39110"] == -300


def test_long_short() -> None:
    """ロングオンリーの売買が妥当にできるかの検証"""
    file_list = [
        pathlib.Path(__file__).parent.parent / "data" / "stock_39110.csv",
        pathlib.Path(__file__).parent.parent / "data" / "stock_86970.csv",
    ]
    stock_list = []
    for path in file_list:
        stock_series = load_stock_series(path)
        stock_list.append(stock_series)
    stock_set = StockSet(stock_list)

    # 39110が400株売られることを確認する
    # 始値での検証
    # 始値は323, 終値は329
    trade_date = datetime.date(2022, 4, 1)
    return_map = ReturnMap()
    return_map["86970"] = 1
    return_map["39110"] = -1
    order = trading.long_short_trading(
        2000000, trade_date, stock_set, return_map, timing=const.COL_OPEN, top_n=1, safety_margin=1.0
    )
    assert order.num_dict["86970"] > 0
    assert order.num_dict["39110"] < 0
