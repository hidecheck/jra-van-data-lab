from typing import Dict, Optional

import pandas as pd
from pandas import DataFrame, Series

import utils.output
from const import const_table_name
from repository.base_repository import BaseRepository


DATA_KUBUN_KAKUTEI = 7


class EntryHorsesRepository(BaseRepository):
    """
    出走馬情報のDB操作クラス
    """
    def __init__(self):
        super().__init__()
        self.table = const_table_name.HORSE_INFO_BY_RACE

    def find_by_race(self, race: Series, order: Optional[str] = None, desc: bool = None):
        conditions = {
            "data_kubun": DATA_KUBUN_KAKUTEI,
            "kaisai_nen": race["kaisai_nen"],
            "kaisai_tsukihi": race["kaisai_tsukihi"],
            "keibajo_code": race["keibajo_code"],
            "race_bango": race["race_bango"]
        }
        return self.find(conditions=conditions)

    def find_previous_entry_by_entry_horse(self, entry_horse: Series) -> Optional[Series]:
        return self.find_previous_entry(ketto_toroku_bango=entry_horse["ketto_toroku_bango"],
                                        kaisai_nen=entry_horse["kaisai_nen"],
                                        kaisai_tsukihi = entry_horse["kaisai_tsukihi"])


    def find_previous_entry(self, ketto_toroku_bango: str, kaisai_nen: str, kaisai_tsukihi: str) -> Optional[Series]:
        """
        前走の結果情報を取得する
        Parameters
        ----------
        current_entry: Series
            出走馬情報

        Returns
        -------

        """
        sql = """SELECT * FROM {table}
WHERE data_kubun = '7'
  AND ketto_toroku_bango = '{ketto_toroku_bango}'
  AND (
    (kaisai_nen < '{kaisai_nen}') 
    OR 
    (kaisai_nen = '{kaisai_nen}' AND  kaisai_tsukihi < '{kaisai_tsukihi}')
  ) 
ORDER BY kaisai_nen DESC, kaisai_tsukihi DESC
""".format(table=self.table,
           ketto_toroku_bango=ketto_toroku_bango,
           kaisai_nen=kaisai_nen,
           kaisai_tsukihi=kaisai_tsukihi)

        df = self.read_sql(sql=sql)
        if len(df) == 0:
            return None
        else:
            return df.iloc[0]


if __name__ == '__main__':

    def main():
        conditions = {
            "kaisai_nen": "2019",
            "kaisai_tsukihi": "1222",
            "keibajo_code": "06",
            "race_bango": "11"
        }

        repository = EntryHorsesRepository()
        df = repository.find(conditions=conditions)
        utils.output.show_one_line(df)

    main()
