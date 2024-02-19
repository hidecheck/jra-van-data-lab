import abc
from typing import Dict, Optional

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine, Engine

import config


class BaseRepository(metaclass=abc.ABCMeta):
    def __init__(self):
        self.engine: Optional[Engine] = None
        self.table: Optional[str] = None
        self.table_nar: Optional[str] = None  # 地方競馬データ
        self._connect()

    def _connect(self):
        self.engine = create_engine(config.CREATE_ENGINE_URL)

    def __del__(self):
        print(f"## __del__: {self.__class__.__name__}.engine.dispose()")
        self.engine.dispose()

    def read_sql(self, sql):
        # TODO あとで消す
        print(sql)
        return pd.read_sql(sql=sql, con=self.engine)

    @staticmethod
    def create_conditions_string(conditions: Optional[Dict]):
        if not conditions:
            return None
        conditions_string = " AND ".join([f"{key} = '{value}'" for key, value in conditions.items()])
        return conditions_string

    @staticmethod
    def create_like_conditions_string(conditions: Optional[Dict]):
        # TODO
        pass

    @staticmethod
    def create_sql_with_table(
        table: str, conditions: Optional[Dict], order: Optional[str] = None, desc: bool = False
    ):
        conditions_string = BaseRepository.create_conditions_string(conditions)
        if not conditions_string:
            sql = f"SELECT * FROM {table}"
        else:
            sql = f"SELECT * FROM {table} WHERE {conditions_string}"

        if order:
            sql += f" ORDER BY {order}"
        if desc:
            sql += " DESC"

        return sql

    def find(self, conditions: Optional[Dict] = None, order: Optional[str] = None, desc: bool = False) -> DataFrame:
        """

        Parameters
        ----------
        conditions: Dict
          Only equality filter
        order
        desc

        Returns
        -------
        DataFrame

        """
        sql = self.create_sql_with_table(table=self.table, conditions=conditions, order=order, desc=desc)
        return self.read_sql(sql=sql)

    def find_with_conditions_string(self, conditions: Optional[Dict] = None, conditions_string: Optional[str] = None, order: Optional[str] = None, desc: bool = False) -> DataFrame:
        """
        条件を文字列で指定して検索

        Parameters
        ----------
        conditions: Dict
          Only equality filter
        conditions_string: str
          Non equality filter
        order
        desc

        Returns
        -------
        DataFrame

        """
        if not conditions_string:
            return self.find(conditions=conditions, order=order, desc=desc)

        sql = f"SELECT * FROM {self.table}"
        conditions_string_equality = self.create_conditions_string(conditions)
        if not conditions_string_equality:
            sql += f" WHERE {conditions_string}"
        else:
            sql += f" WHERE {conditions_string_equality} AND {conditions_string}"
        return self.read_sql(sql=sql)
