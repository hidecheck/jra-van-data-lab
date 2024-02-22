from typing import Dict, Optional

import pandas as pd
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

        # メモリが足りないかも
        self.df_race: Optional[DataFrame] = None
        self.df_entry_horses: Optional[DataFrame] = None

        # TODO 使ってなかったら消す
        self.conditions = conditions
        self.conditions_string = conditions_string
        self.conditions_string_with_jra = query.set_jra_course_conditions_string(conditions_string)

    def recreate_rank(self):
        # レース情報の取得
        self.df_race = self.race_repository.find_with_conditions_string(
            self.conditions, self.conditions_string_with_jra
        )

        # 馬毎レース情報の取得
        self.df_entry_horses = self.entry_horses_repository.find_with_conditions_string(
            self.conditions, self.conditions_string_with_jra
        )

        # ランキング馬体重の取得
        # 例外体重の除外
        print(f"size of self.df_entry_horses: {len(self.df_entry_horses)}")
        df = self.df_entry_horses[self.df_entry_horses["bataiju"] != "   "]
        df = df[(df["bataiju"] > '000') & (df["bataiju"] < '999')]

        # Ranking
        group_cols = ["kaisai_nen", "kaisai_tsukihi", "keibajo_code", "race_bango"]
        grouped = df.groupby(group_cols)
        rank_asc = grouped['bataiju'].rank(method='min').astype(int)
        rank_asc.name = 'rank_asc'
        rank_desc = grouped['bataiju'].rank(ascending=False, method='min').astype(int)
        rank_desc.name = 'rank_desc'
        df_custom_entry_horses = df.join([rank_asc, rank_desc])

        # Debug output
        print(f"size of df_custom_entry_horses: {len(df_custom_entry_horses)}")
        utils.output.show_one_line(df_custom_entry_horses)
        df_custom_entry_horses.to_csv("out.csv", index=False)

    # def initialize(self, conditions, conditions_string: str = None, order: str = None, desc: bool = False):
    #
    #     # レース情報の取得
    #     if not conditions_string:
    #         self.df_all_race = self.race_repository.find(conditions, order, desc)
    #     else:
    #         self.df_all_race = self.race_repository.find_with_conditions_string(conditions, conditions_string, order, desc)


if __name__ == "__main__":

    def main():
        conditions_string = None
        conditions = None

        start_year = 2019
        end_year = 2020
        conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen <= '{end_year}'"
        # conditions = {
        #     "kaisai_nen": "2020",
        #     "kaisai_tsukihi": "0725",
        #     "keibajo_code": "01",
        #     # "race_bango": "01"
        # }

        horse_weight_repository = HorseWeightRankRepository()
        race_repository = RaceRepository()
        entry_horses_repository = EntryHorsesRepository()

        service = HorseWeightRankService(
            horse_weight_repository=horse_weight_repository,
            race_repository=race_repository,
            entry_horses_repository=entry_horses_repository,
            conditions_string=conditions_string,
            conditions=conditions
        )
        service.recreate_rank()
        # utils.output.show_one_line(service.df_entry_horses)

    main()
