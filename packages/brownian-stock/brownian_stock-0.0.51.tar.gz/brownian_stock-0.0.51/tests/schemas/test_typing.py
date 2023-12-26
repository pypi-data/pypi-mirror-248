import pandas as pd
from brownian_stock.schemas import drop_unnecessary
from pydantic import BaseModel


class StockSchema(BaseModel):
    data: int


def test_drop_unnecessary_columns():
    before = pd.DataFrame(
        [
            {"data": 1, "data2": "OK"},
            {"data": 1, "data2": "OK"},
        ]
    )

    df = drop_unnecessary(before, StockSchema)
    assert len(df.columns) == 1
