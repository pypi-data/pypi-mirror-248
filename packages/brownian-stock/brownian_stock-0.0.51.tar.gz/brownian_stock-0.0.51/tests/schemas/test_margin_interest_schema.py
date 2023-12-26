import pandas as pd
from brownian_stock.schemas import MarginInterestSchema, cast, validate


def test_margin_interest_schema():
    df = pd.DataFrame(
        {
            "Date": ["2022-01-01", "2022-01-02"],
            "Code": ["00000", "00000"],
            "ShortMarginTradeVolume": [0, 0],
            "LongMarginTradeVolume": [0, 0],
            "ShortNegotiableMarginTradeVolume": [0, 0],
            "LongNegotiableMarginTradeVolume": [0, 0],
            "ShortStandardizedMarginTradeVolume": [0, 0],
            "LongStandardizedMarginTradeVolume": [0, 0],
            "IssueType": [1, 1],
        }
    )

    assert not validate(df, MarginInterestSchema)
    cast_df = cast(df, MarginInterestSchema)
    print(cast_df)
    assert validate(cast_df, MarginInterestSchema)


def test_margin_interest_schema_with_none():
    # Normal Case. ShortMarginTradeVolume is Optional.
    df = pd.DataFrame(
        {
            "Date": ["2022-01-01", "2022-01-02"],
            "Code": ["00000", "00000"],
            "ShortMarginTradeVolume": [0, None],
            "LongMarginTradeVolume": [0, 0],
            "ShortNegotiableMarginTradeVolume": [0, 0],
            "LongNegotiableMarginTradeVolume": [0, 0],
            "ShortStandardizedMarginTradeVolume": [0, 0],
            "LongStandardizedMarginTradeVolume": [0, 0],
            "IssueType": [1, 1],
        }
    )

    assert not validate(df, MarginInterestSchema)
    cast_df = cast(df, MarginInterestSchema)
    print(cast_df)
    assert validate(cast_df, MarginInterestSchema)

    # Irregular Case. Date is not Optional so None is not allowed
    df = pd.DataFrame(
        {
            "Date": ["2022-01-01", None],
            "Code": ["00000", "00000"],
            "ShortMarginTradeVolume": [0, None],
            "LongMarginTradeVolume": [0, 0],
            "ShortNegotiableMarginTradeVolume": [0, 0],
            "LongNegotiableMarginTradeVolume": [0, 0],
            "ShortStandardizedMarginTradeVolume": [0, 0],
            "LongStandardizedMarginTradeVolume": [0, 0],
            "IssueType": [1, 1],
        }
    )

    assert not validate(df, MarginInterestSchema)
    cast_df = cast(df, MarginInterestSchema)
    print(cast_df)
    assert not validate(cast_df, MarginInterestSchema)
