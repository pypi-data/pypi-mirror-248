import brownian_stock.repository.stock_sql_repository as target


def test_is_code() -> None:
    # OKな例
    assert target.is_code("00000")
    assert target.is_code("00100")
    assert target.is_code("11111")
    assert target.is_code("99999")

    # NGな例
    assert not target.is_code("000000")
    assert not target.is_code("0010a")
    assert not target.is_code("HELLO")
    assert not target.is_code("NG")
