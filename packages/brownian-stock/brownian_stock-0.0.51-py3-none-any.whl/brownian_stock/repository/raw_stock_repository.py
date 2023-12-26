import datetime
import sqlite3
from typing import List

import pandas as pd
import polars as pl

from ..schemas import StockSchema, cast, create_table_query, drop_unnecessary, write_database
from . import repository_path as rp

TABLE_PRICES = "stock"


class RawStockRepository:

    """ダウンロードした生のCSVをデータベースに挿入するためのレポジトリ"""

    def __init__(self, repository_path: rp.AbstractRepositoryPath):
        self.repository_path = repository_path

    def insert_daily_df(self, df: pl.DataFrame) -> None:
        """データベースに対象日のレコードを挿入する"""

        # 入力のチェック
        if len(df) == 0:
            raise ValueError("DataFrame is empty.")
        if len(df["Date"].unique()) != 1:
            raise ValueError("DataFrame contains two or more different dates.")

        # 既にレコードが存在していたら一度削除する
        conn = self.__get_connection()
        try:
            date = df["Date"][0]
            if self.has_records(date):
                date_str = date.strftime("%Y-%m-%d")
                conn.execute(f"DELETE FROM stock WHERE Date='{date_str}'")
            df = preprocess_before_insert(df)
            write_database(StockSchema, conn, TABLE_PRICES, df)
        finally:
            conn.close()

    def drop_index(self) -> None:
        """Indexを落とす"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("DROP INDEX IF EXISTS stock_index;")
        conn.commit()
        conn.close()

    def set_index(self) -> None:
        """CodeにIndexを貼る"""
        conn = self.__get_connection()
        cur = conn.cursor()
        cur.execute("CREATE INDEX IF NOT EXISTS stock_index ON stock (Code);")
        conn.commit()
        conn.close()

    def has_records(self, date: datetime.date) -> bool:
        """対象日のデータが存在するか確認する"""
        if not isinstance(date, datetime.date):
            raise TypeError("date must be 'datetiem.date'")
        date_str = date.strftime("%Y-%m-%d")
        conn = self.__get_connection()
        query = f"SELECT COUNT(*) FROM stock WHERE Date='{date_str}';"
        res = conn.execute(query)
        size = res.fetchone()
        is_exist: bool = size[0] > 0
        conn.close()
        return is_exist

    def existing_date(self) -> List[datetime.date]:
        """DB上に存在している日付を列挙する"""
        conn = self.__get_connection()
        res = conn.execute("SELECT DISTINCT(DATE) FROM stock;")
        raw_date_list = [r[0] for r in res.fetchall()]
        date_list = [datetime.datetime.strptime(s, "%Y-%m-%d").date() for s in raw_date_list]
        conn.close()
        return date_list

    def create_table(self) -> None:
        """新しくstockテーブルを生成する"""
        conn = self.__get_connection()
        cur = conn.cursor()
        query = create_table_query(StockSchema, TABLE_PRICES)
        cur.execute(query)
        conn.commit()
        conn.close()

    def table_exists(self) -> bool:
        """priceテーブルが存在するか判定する"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE TYPE='table' AND name='stock';")
        size = res.fetchone()
        is_exist: bool = size[0] > 0
        conn.commit()
        conn.close()
        return is_exist

    def records_size(self) -> int:
        """データ総数を取得"""
        conn = self.__get_connection()
        cur = conn.cursor()
        res = cur.execute("SELECT COUNT(*) FROM stock;")
        size: int = res.fetchone()[0]
        conn.commit()
        conn.close()
        return size

    def __get_connection(self) -> sqlite3.Connection:
        db_path = self.repository_path.sqlite_path
        conn = sqlite3.connect(db_path)
        return conn


def preprocess_before_insert(df: pl.DataFrame) -> pd.DataFrame:
    """Unicode型をSqliteが扱えないので予め処理する"""
    for col in df.columns:
        if df[col].dtype != pl.Utf8:
            continue
        df = df.with_columns(pl.when(pl.col(col) == "－").then(None).otherwise(pl.col(col)).alias(col))
    df = cast(df.to_pandas(), StockSchema, strict=False)
    df = drop_unnecessary(df, StockSchema)
    return df
