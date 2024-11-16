from typing import Dict, Optional, List
import pandas as pd
from pandas import DataFrame, Series

import utils.output
from const import master_code
from const.table_columns import jvd_ra
from repository.race_repository import RaceRepository
from utils import output


class RaceService:
    """
    レース詳細情報サービス
    """
    def __init__(
        self,
        repository:Optional[RaceRepository] = None,
        conditions: Optional[Dict] = None,
        conditions_string: str = None,
        order=None,
        desc=False,
    ):
        if repository:
            self.repository: RaceRepository = repository
        else:
            self.repository: RaceRepository = RaceRepository()

        # 指定した条件にマッチする全レース情報
        self.races: Optional[DataFrame] = None

        self._set_races(conditions, conditions_string, order, desc)

    def _set_races(self, conditions, conditions_string: str = None, order: str = None, desc: bool = False):
        if not conditions_string:
            self.races = self.repository.find(conditions, order, desc)
        else:
            self.races = self.repository.find_with_conditions_string(conditions, conditions_string, order, desc)
        print(f"## 総レース件数: {len(self.races)}")

        # レースID
        self.races[jvd_ra.CUSTOM_COL_RACE_ID] = self.races.apply(self.to_race_id, axis=1)
        # グレード
        self.races[jvd_ra.CUSTOM_COL_RACE_GRADE] = self.races.apply(self.to_race_grade, axis=1)
        # 競走名本題 空白除去
        self.races["kyosomei_hondai"] = self.races["kyosomei_hondai"].apply(lambda x: x.strip())
        # self.races["kyosomei_hondai"] = self.races["kyosomei_hondai"].str.strip()
        # トラック名称
        self.races[jvd_ra.CUSTOM_COL_TRACK_NAME] = self.races["track_code"].apply(lambda x: master_code.TRACK_CODE.get(x))

    @staticmethod
    def to_race_id(series: Series):
        """
        レースIDを返す。
        レースID: YYYY-mm-dd_<競馬場コード>_<レースNo>
            year = race_id[:4]
            month = race_id[5:7]
            day = race_id[8:10]
            racing_venue = race_id[11:13]
            race_no = race_id[14:]

        Parameters
        ----------
        series: Series
          require keys: `kaisai_nen`, `kaisai_tsukihi`, `keibajo_code`, `race_bango`
          PAYOFF, RACE から取得したデータにはこれらの key が含まれる

        Returns
        -------

        """
        year = series["kaisai_nen"]
        month = series["kaisai_tsukihi"][:2]
        day = series["kaisai_tsukihi"][2:4]
        return f"{year}-{month}-{day}_{series['keibajo_code']}_{series['race_bango']}"

    @staticmethod
    def to_race_grade(row: Series):
        if row["kyoso_joken_code"] != "999":
            race_grade = master_code.RACE_CONDITION.get(row["kyoso_joken_code"])
        else:
            race_grade = master_code.GRADE_CODE.get(row["grade_code"])

        return race_grade


if __name__ == '__main__':

    def main():
        conditions = {
            "kaisai_nen": "2020",
            "kaisai_tsukihi": "1227",
            "keibajo_code": "06",
            "race_bango": "01"
        }
        service = RaceService(conditions=conditions)
        print(len(service.races))

        output.show_one_line(service.races, True)

    main()