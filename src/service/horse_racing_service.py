from typing import Dict, Optional, List

from pandas import DataFrame, Series

import utils.output
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository


class HorseRacingService:
    def __init__(self, race_repository: RaceRepository, entry_horses_repository: EntryHorsesRepository,
                 payoff_repository: PayoffRepository,
                 conditions: Dict, conditions_string: str = None, order=None, desc=False):
        self.race_repository: RaceRepository = race_repository
        self.entry_horses_repository: EntryHorsesRepository = entry_horses_repository
        self.payoff_repository: PayoffRepository = payoff_repository

        # 指定した条件にマッチする全レース情報
        self.races: Optional[DataFrame] = None
        # 指定した条件にマッチする全レースの払い戻し情報
        self.all_payoff: Dict[str: Series] = {}
        # 指定した条件にマッチする全レースの全出走馬情報のリスト（障害レースも含まれるため、 self.race よりサイズが大きくなる）
        self.all_entry_horses: Dict[str: DataFrame] = {}

        self.initialize(conditions, conditions_string, order, desc)

    def initialize(self, conditions, conditions_string: str = None, order: str = None, desc: bool = False):
        if not conditions_string:
            self.races = self.race_repository.find(conditions, order, desc)
        else:
            self.races = self.race_repository.find_with_conditions_string(conditions, conditions_string, order, desc)

        for i, race in self.races.iterrows():
            race_id = self.to_race_id(race)
            self.races.at[i, 'race_id'] = race_id
            # TODO 出走馬情報をレース毎でとらずに一括取得する
            # 出走馬情報
            entry_horses = self.entry_horses_repository.find_by_race(race=race)
            self.all_entry_horses[race_id] = entry_horses

        df_payoff = self.payoff_repository.find(conditions, order, desc)
        for i, payoff in df_payoff.iterrows():
            race_id = self.to_race_id(payoff)
            self.all_payoff[race_id] = payoff

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


if __name__ == '__main__':
    def main():
        conditions = {
            "kaisai_nen": "2020",
            "kaisai_tsukihi": "1227",
            "keibajo_code": "06",
        }
        race_repository = RaceRepository()
        entry_horses_repository = EntryHorsesRepository()
        payoff_repository = PayoffRepository()

        service = HorseRacingService(race_repository=race_repository, entry_horses_repository=entry_horses_repository,
                                     payoff_repository=payoff_repository,
                                     conditions=conditions)
        print(service.races.head())
        utils.output.show_one_line(service.races, True)
        utils.output.show_line(service.races, 1, True)

        # race1 = service.races.iloc[0]
        # race_id = service.to_race_id(race=race1)
        # print(race_id)

    main()
