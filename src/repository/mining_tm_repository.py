from typing import Optional, Dict

from pandas import DataFrame

from const import table_name
from repository.base_repository import BaseRepository
from utils import output


class MiningTmRepository(BaseRepository):
    """
    対戦型マイニングのDB操作クラス
    """

    def __init__(self):
        super().__init__()
        self.table = table_name.MINING_TM

    def find(self, conditions: Optional[Dict] = None, order: Optional[str] = None, desc: bool = False) -> DataFrame:
        df = super().find()

        # TODO マイングデータを整形

        # グループ化
        
        # 先頭２文字の切り取り

        # 数値変換

        # ランキング作成



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
