from typing import Dict, Optional

from pandas import DataFrame

import utils.output
from repository.entry_horses_repository import EntryHorsesRepository
from repository.custom_entry_horse_repository import CustomEntryHorsesRepository
from utils import query


class CustomEntryHorseService:
    def __init__(
        self,
        custon_horse_entry_repository: CustomEntryHorsesRepository,
        entry_horses_repository: EntryHorsesRepository,
        conditions: Optional[Dict] = None,
        conditions_string: str = None,
        order=None,
        desc=False,
    ):
        self.custom_horse_entry_repository = custon_horse_entry_repository
        self.entry_horses_repository: EntryHorsesRepository = entry_horses_repository
        self.df_custom_entry_horses: Optional[DataFrame] = None

        # TODO 使ってなかったら消す
        self.conditions = conditions
        self.conditions_string = conditions_string
        self.conditions_string_with_jra = query.set_jra_course_conditions_string(conditions_string)

    def recreate_rank(self):
        # 馬毎レース情報の取得
        df_entry_horses = self.entry_horses_repository.find_with_conditions_string(
            self.conditions, self.conditions_string_with_jra
        )

        # ランキング馬体重の取得
        # 例外体重の除外
        print(f"size of df_entry_horses: {len(df_entry_horses)}")
        # df = df_entry_horses[df_entry_horses["bataiju"] != "   "]
        # df = df[(df["bataiju"] > '000') & (df["bataiju"] < '999')]

        df = df_entry_horses[
            (df_entry_horses["bataiju"] != "   ")
            & (df_entry_horses["bataiju"] > '000')
            & (df_entry_horses["bataiju"] < '999')
        ]
        print(f"Count: df={len(df)}")
        # print(f"Count: df={len(df)} df2={len(df2)}")
        # df_par_race.loc[:, ['rank_asc']] = df_par_race["bataiju"].rank(numeric_only=False).astype(int)
        # df.loc[:,
        #     (df_entry_horses["bataiju"] != "   ")
        #     & (df_entry_horses["bataiju"] > '000')
        #     & (df_entry_horses["bataiju"] < '999')
        # ] = ""

        # 馬体重ランキング列 昇順・降順 の追加
        group_cols = ["kaisai_nen", "kaisai_tsukihi", "keibajo_code", "race_bango"]
        grouped = df.groupby(group_cols)
        rank_asc = grouped['bataiju'].rank(method='min').astype(int)
        rank_asc.name = 'rank_asc'
        rank_desc = grouped['bataiju'].rank(ascending=False, method='min').astype(int)
        rank_desc.name = 'rank_desc'
        self.df_custom_entry_horses = df.join([rank_asc, rank_desc])

        # TODO 上がり 3 ハロンランキング


        # テーブル作成
        self.custom_horse_entry_repository.replace_table(self.df_custom_entry_horses)


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

        custom_entry_horse_repository = CustomEntryHorsesRepository()
        entry_horses_repository = EntryHorsesRepository()

        service = CustomEntryHorseService(
            custon_horse_entry_repository=custom_entry_horse_repository,
            entry_horses_repository=entry_horses_repository,
            conditions_string=conditions_string,
            conditions=conditions
        )
        service.recreate_rank()
        print(f"size of df_custom_entry_horses: {len(service.df_custom_entry_horses)}")
        utils.output.show_one_line(service.df_custom_entry_horses)
        service.df_custom_entry_horses.to_csv("out.csv", index=False)

    main()
