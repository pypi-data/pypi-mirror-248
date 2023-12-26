import brownian_stock
import pytest


def test_return_map():
    """ReturnMapの基本的な機能を試す"""
    # on_same_universeが機能するかどうか
    rmap1 = brownian_stock.ReturnMap()
    rmap1["00000"] = 1
    rmap1["00001"] = 10

    rmap2 = brownian_stock.ReturnMap()
    rmap2["00000"] = 2
    assert not rmap1.on_same_universe(rmap2)

    rmap2["00001"] = 20
    assert rmap1.on_same_universe(rmap2)

    # 要素の削除ができるか
    del rmap2["00001"]
    assert "00001" not in rmap2.return_map.keys()

    ls = rmap1.ordered_code_list()
    ls[0] = 10

    ls = rmap1.ordered_code_list()
    ls[0] = 1


def test_return_map_standardize():
    # Standardizeの標準化
    rmap3 = brownian_stock.ReturnMap()
    rmap3["00000"] = 1
    rmap3["00001"] = 10
    rmap3["00002"] = 5
    rmap3["00003"] = 3
    standard_rmap = rmap3.standardize()
    assert standard_rmap["00000"] == 0
    assert standard_rmap["00001"] == 1
    assert standard_rmap["00002"] == pytest.approx(0.44, 0.1)


def test_return_map_ranked():
    rmap3 = brownian_stock.ReturnMap()
    rmap3["00000"] = 1
    rmap3["00001"] = 10
    rmap3["00002"] = 5
    rmap3["00003"] = 3

    ranked_map = rmap3.ranked()
    assert ranked_map["00000"] == 0
    assert ranked_map["00001"] == 1
    assert ranked_map["00002"] == pytest.approx(0.66, 0.1)
    assert ranked_map["00003"] == pytest.approx(0.33, 0.1)


def test_returm_map_add():
    """ReturmMap同士の足し算が正しくできるか検証する"""
    rmap1 = brownian_stock.ReturnMap()
    rmap1["00000"] = 1
    rmap1["00001"] = 10

    rmap2 = brownian_stock.ReturnMap()
    rmap2["00000"] = 2
    rmap2["00001"] = 20

    rmap3 = rmap1 + rmap2
    assert rmap3["00000"] == 3
    assert rmap3["00001"] == 30

    rmap4 = rmap3 + 3
    assert rmap4["00000"] == 6
    assert rmap4["00001"] == 33


def test_returm_map_mul():
    """ReturmMap同士の掛け算が正しくできるか検証する"""
    rmap1 = brownian_stock.ReturnMap()
    rmap1["00000"] = 1
    rmap1["00001"] = 10

    rmap2 = rmap1 * 2
    assert rmap2["00000"] == 2
    assert rmap2["00001"] == 20


def test_intersection():
    rmap1 = brownian_stock.ReturnMap()
    rmap1["00000"] = 1
    rmap1["00001"] = 10
    rmap1["00002"] = 10

    rmap2 = brownian_stock.ReturnMap()
    rmap2["00000"] = 1
    rmap2["00001"] = 10
    rmap2["00003"] = 10

    intersection = rmap1.intersection(rmap2)
    assert len(intersection) == 2

    # 共通部分が存在しているか
    assert "00000" in intersection
    assert "00001" in intersection

    # 非共通部分が存在していないこと
    assert "00002" not in intersection
    assert "00003" not in intersection


def test_equal():
    rmap1 = brownian_stock.ReturnMap()
    rmap1["00000"] = 1
    rmap1["00001"] = 10
    rmap1["00002"] = 10

    rmap2 = brownian_stock.ReturnMap()
    rmap2["00000"] = 1
    rmap2["00001"] = 10
    rmap2["00002"] = 10

    rmap3 = brownian_stock.ReturnMap()
    rmap3["00000"] = 2
    rmap3["00001"] = 10
    rmap3["00002"] = 10

    assert rmap1 == rmap2
    assert rmap1 != rmap3


def test_serealize():
    rmap1 = brownian_stock.ReturnMap()
    rmap1["00000"] = 1
    rmap1["00001"] = 10
    rmap1["00002"] = 10

    text = rmap1.serialize()
    deserialized = brownian_stock.ReturnMap.deserialize(text)
    assert rmap1 == deserialized
