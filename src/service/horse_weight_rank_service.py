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
        print(f"self.df_entry_horses: {len(self.df_entry_horses)}")
        df = self.df_entry_horses[self.df_entry_horses["bataiju"] != "   "]
        print(f"df 1: {len(df)}")
        df = df[(df["bataiju"] > '000') & (df["bataiju"] < '999')]
        print(f"df 2: {len(df)}")
        df_custom_entry_horses = pd.DataFrame()
        self.df_entry_horses.to_csv("df_entry_horses.csv")
        for i, ser_race in self.df_race.iterrows():

            kaisai_nen = ser_race["kaisai_nen"]
            kaisai_tsukihi = ser_race["kaisai_tsukihi"]
            keibajo_code = ser_race["keibajo_code"]
            race_bango = ser_race["race_bango"]
            # print(kaisai_nen, kaisai_tsukihi, keibajo_code, race_bango, ser_race["data_kubun"])

            # 同年同月日同競馬場同レースの
            df_par_race = df[
                (df["kaisai_nen"] == kaisai_nen)
                & (df["kaisai_tsukihi"] == kaisai_tsukihi)
                & (df["keibajo_code"] == keibajo_code)
                & (df["race_bango"] == race_bango)
                & (df["data_kubun"] == '7')
                # & (df["bataiju"] != "   ")
                ]

            df_par_race.loc[:, ['rank_asc']] = df_par_race["bataiju"].rank(numeric_only=False).astype(int)
            df_par_race.loc[:, ['rank_desc']] = df_par_race["bataiju"].rank(numeric_only=False, ascending=False).astype(int)

            print(f"len = {len(df_par_race)}")
            print(df_par_race['rank_asc'])
            utils.output.show_line(df_par_race)
            utils.output.show_line(df)
            # df_par_race = df_par_race.sort_index(axis=1)
            df_par_race.to_csv(f"df_par_race_{i}.csv", index=False)

            df_custom_entry_horses = pd.concat([df_custom_entry_horses, df_par_race])
        utils.output.show_one_line(df_custom_entry_horses)
        df_custom_entry_horses.to_csv("out.csv", sep=";", index=False)

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
        start_year = 2019
        end_year = 2020
        # conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen <= '{end_year}'"
        conditions = {
            "kaisai_nen": "2020",
            "kaisai_tsukihi": "0725",
            "keibajo_code": "01",
            # "race_bango": "01"
        }

        horse_weight_repository = HorseWeightRankRepository()
        race_repository = RaceRepository()
        entry_horses_repository = EntryHorsesRepository()

        service = HorseWeightRankService(
            horse_weight_repository=horse_weight_repository,
            race_repository=race_repository,
            entry_horses_repository=entry_horses_repository,
            # conditions_string=conditions_string,
            conditions=conditions
        )
        service.recreate_rank()
        # utils.output.show_one_line(service.df_entry_horses)

    main()
