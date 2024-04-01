from typing import Optional, Dict

import pandas as pd
from pandas import DataFrame

from const import table_name
from repository.base_repository import BaseRepository
from schema.target.mining_tm import MiningTmSchema as Ms

from utils import output


class MiningTmRepository(BaseRepository):
    """
    対戦型マイニングのDB操作クラス
    """

    def __init__(self):
        super().__init__()
        self.table = table_name.MINING_TM

    def find_as_raw(self, conditions: Optional[Dict] = None, order: Optional[str] = None, desc: bool = False) -> DataFrame:
        return super().find(conditions=conditions, order=order, desc=desc)

    def find(self, conditions: Optional[Dict] = None, order: Optional[str] = None, desc: bool = False) -> DataFrame:
        df = super().find(conditions=conditions, order=order, desc=desc)
        # 先頭２文字の切り取り
        col_pref = "mining_yoso_"
        for i in range(1, 19):
            uma_ban = f'{i:02}'
            col = f"{col_pref}{uma_ban}"
            df[col] = df[col].str[2:]
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df.fillna(-1, inplace=True)
        return df


if __name__ == '__main__':

    def main():
        repository = MiningTmRepository()
        conditions = {
            "kaisai_nen": "2020",
            "kaisai_tsukihi": "1227",
            "keibajo_code": "06",
            "race_bango": "11"
        }
        df = repository.find(conditions=conditions)
        print(len(df))
        # df = service.find_by_bamei('ハーツクライ')
        # print(len(df))

        output.show_one_line(df, True)

    main()
