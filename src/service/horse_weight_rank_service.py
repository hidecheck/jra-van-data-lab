from typing import Dict, Optional

from pandas import DataFrame, Series

import utils.output
from repository.entry_horses_repository import EntryHorsesRepository
from repository.horse_weight_rank_repository import HorseWeightRankRepository
from repository.race_repository import RaceRepository
from utils import query


class HorseWeightRankService:
    def __init__(
        self,
        horse_weight_repository: HorseWeightRankRepository,
        race_repository: RaceRepository,
        entry_horses_repository: EntryHorsesRepository,
        conditions: Optional[Dict] = None,
        conditions_string: str = None,
        order=None,
        desc=False,
    ):
        self.horse_weight_repository = horse_weight_repository
        self.race_repository: RaceRepository = race_repository
        self.entry_horses_repository: EntryHorsesRepository = entry_horses_repository

        self.df_race: Optional[DataFrame] = None
        self.df_entry_horses: Optional[DataFrame] = None

        # TODO 使ってなかったら消す
        self.conditions = conditions
        self.conditions_string = conditions_string
        self.conditions_string_with_jra = query.set_jra_course_conditions_string(conditions_string)

    def recreate_rank(self):
        # レース情報の取得
        self.df_race = self.race_repository.find_with_conditions_string(self.conditions, self.conditions_string_with_jra)

        # 馬毎レース情報の取得
        self.df_entry_horses = self.entry_horses_repository.find_with_conditions_string(self.conditions, self.conditions_string_with_jra)

        # ランキング馬体重の取得
        for i, ser_race in self.df_race.iterrows():
            kaisai_nen = ser_race["kaisai_nen"]
            kaisai_tsukihi = ser_race["kaisai_tsukihi"]
            keibajo_code = ser_race["keibajo_code"]
            race_bango = ser_race["race_bango"]
            print(kaisai_nen, kaisai_tsukihi, keibajo_code, race_bango)
            df = self.df_entry_horses
            df_target = df[df["kaisai_nen"] == kaisai_nen]
            print(len(df_target))
            df_target = df[(df["kaisai_nen"] == kaisai_nen) & (df["kaisai_tsukihi"] == kaisai_tsukihi)]
            print(len(df_target))
            # utils.output.show_one_line(df_target)
            break



    # def initialize(self, conditions, conditions_string: str = None, order: str = None, desc: bool = False):
    #
    #     # レース情報の取得
    #     if not conditions_string:
    #         self.df_all_race = self.race_repository.find(conditions, order, desc)
    #     else:
    #         self.df_all_race = self.race_repository.find_with_conditions_string(conditions, conditions_string, order, desc)

    def setz_hourse_whight_rank(self, race: Series):
        pass


if __name__ == "__main__":

    def main():
        start_year = 2015
        end_year = 2020
        conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen <= '{end_year}'"

        horse_weight_repository = HorseWeightRankRepository()
        race_repository = RaceRepository()
        entry_horses_repository = EntryHorsesRepository()

        service = HorseWeightRankService(
            horse_weight_repository=horse_weight_repository,
            race_repository=race_repository,
            entry_horses_repository=entry_horses_repository,
            conditions_string=conditions_string,
        )
        service.recreate_rank()
        # utils.output.show_one_line(service.df_entry_horses)

    main()
