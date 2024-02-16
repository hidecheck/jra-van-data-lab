from typing import Dict, Optional

from pandas import DataFrame, Series

from const import const_table_name
from repository.base_repository import BaseRepository
from utils import output


class RaceRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = const_table_name.RACE

    @staticmethod
    def to_conditions(series: Series):
        if "kaisai_nen" not in series.index:
            raise Exception("kaisai_nen は必須です")
        if "kaisai_tsukihi" not in series.index:
            raise Exception("kaisai_tsukihi は必須です")
        if "keibajo_code" not in series.index:
            raise Exception("keibajo_code は必須です")
        if "race_bango" not in series.index:
            raise Exception("race_bango は必須です")

        conditions = {
            "kaisai_nen": series["kaisai_nen"],
            "kaisai_tsukihi": series["kaisai_tsukihi"],
            "keibajo_code": series["keibajo_code"],
            "race_bango": series["race_bango"]
        }
        return conditions


if __name__ == '__main__':

    def main():
        repository = RaceRepository()
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
