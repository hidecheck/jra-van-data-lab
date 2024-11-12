from typing import Dict, Optional, List

from pandas import DataFrame, Series

import utils.output
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from utils import output


class RaceService:
    def __init__(
        self,
        race_repository: RaceRepository,
        conditions: Dict,
        conditions_string: str = None,
        order=None,
        desc=False,
    ):
        self.race_repository: RaceRepository = race_repository
        # 指定した条件にマッチする全レース情報
        self.races: Optional[DataFrame] = None

        self.initialize(conditions, conditions_string, order, desc)

    def initialize(self, conditions, conditions_string: str = None, order: str = None, desc: bool = False):
        if not conditions_string:
            self.races = self.race_repository.find(conditions, order, desc)
        else:
            self.races = self.race_repository.find_with_conditions_string(conditions, conditions_string, order, desc)
        print(f"## 総レース件数: {len(self.races)}")

        # レースID 追加
        self.races["race_id"] = self.races.apply(self.to_race_id, axis=1)


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

    def to_race_name(self):
        # TODO
        pass

    def to_race_grade(self):
        # TODO
        pass


if __name__ == '__main__':

    def main():
        repository = RaceRepository()
        conditions = {
            "kaisai_nen": "2020",
            "kaisai_tsukihi": "1227",
            "keibajo_code": "06",
            "race_bango": "11"
        }
        service = RaceService(race_repository=repository, conditions=conditions)
        print(len(service.races))

        output.show_one_line(service.races, True)

    main()