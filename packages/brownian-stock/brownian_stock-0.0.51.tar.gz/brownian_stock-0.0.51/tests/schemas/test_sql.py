from brownian_stock.schemas import MarginInterestSchema, create_table_query, read_sql_query


def test_create_table_query():
    query = create_table_query(MarginInterestSchema, "test_table")
    answer = (
        "CREATE TABLE test_table(id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "'Code' str, "
        "'Date' str, "
        "'IssueType' integer, "
        "'LongMarginTradeVolume' real, "
        "'LongNegotiableMarginTradeVolume' real, "
        "'LongStandardizedMarginTradeVolume' real, "
        "'ShortMarginTradeVolume' real, "
        "'ShortNegotiableMarginTradeVolume' real, "
        "'ShortStandardizedMarginTradeVolume' real"
        ");"
    )
    assert query == answer


def test_read_sql_query():
    query = read_sql_query(MarginInterestSchema, "test_table")
    answer = (
        "SELECT Code, Date, IssueType, LongMarginTradeVolume, LongNegotiableMarginTradeVolume, LongStandardizedMarginTradeVolume, "
        "ShortMarginTradeVolume, ShortNegotiableMarginTradeVolume, ShortStandardizedMarginTradeVolume "
        "FROM test_table;"
    )
    assert query == answer
