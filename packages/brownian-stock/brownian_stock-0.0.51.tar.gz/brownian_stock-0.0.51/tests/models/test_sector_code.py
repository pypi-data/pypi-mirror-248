import brownian_stock
from brownian_stock.models.sector_code import build_sector_code


def test_sector_code():
    """セクターコード周りの処理が正しく動くか"""
    # 比較処理が正しくできるか
    s1 = build_sector_code(1)
    assert s1 == brownian_stock.SectorConst.FOOD

    # 比較処理が正しくできるか
    s2 = build_sector_code(2)
    assert s2 != brownian_stock.SectorConst.FOOD

    # nameが異なってもcodeが等しければOK
    s1 = brownian_stock.SectorCode("食品_テスト", 1)
    assert s1 == brownian_stock.SectorConst.FOOD

    # nameが異なってもcodeが等しければOK
    s2 = brownian_stock.SectorCode("食品_テスト", 2)
    assert s2 != brownian_stock.SectorConst.FOOD

    # セクターの長さが18であること
    assert len(brownian_stock.SectorConst.sector_list()) == 18
