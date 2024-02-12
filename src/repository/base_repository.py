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
        self._connect()

    def _connect(self):
        self.engine = create_engine(config.CREATE_ENGINE_URL)

    def __del__(self):
        print(f"## __del__: {self.__class__.__name__}.engine.dispose()")
        self.engine.dispose()

    def read_sql(self, sql):
        # TODO あとで消す
        # print(sql)
        return pd.read_sql(sql=sql, con=self.engine)

    @staticmethod
    def create_conditions_string(conditions: Dict):
        conditions_string = " AND ".join([f"{key} = '{value}'" for key, value in conditions.items()])
        return conditions_string

    @staticmethod
    def create_like_conditions_string(conditions: Dict):
        pass

    @staticmethod
    def create_sql_with_table(
        table: str, conditions: Dict, order: Optional[str] = None, desc: bool = False
    ):
        conditions_string = BaseRepository.create_conditions_string(conditions)
        sql = f"SELECT * FROM {table} WHERE {conditions_string}"

        if order:
            sql += f" ORDER BY {order}"
        if desc:
            sql += " DESC"

        return sql

    def find(self, conditions: Dict, order: Optional[str] = None, desc: bool = False) -> DataFrame:
        sql = self.create_sql_with_table(table=self.table, conditions=conditions, order=order, desc=desc)
        return self.read_sql(sql=sql)
