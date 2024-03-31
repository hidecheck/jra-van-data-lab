from typing import Dict, Optional

from pandas import DataFrame

import utils.output
from repository.entry_horses_repository import EntryHorsesRepository
from repository.custom_entry_horse_repository import CustomEntryHorsesRepository
from schema.target.entry_horse import EntryHorseSchema as Es
from utils import query


class CustomEntryHorseService:
    """
    デフォルトの馬毎データをカスタマイズする
    追加要素:
      - レース馬体重のランキング
      - 前走上がり3ハロンランキング
    """

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
        # df = df_entry_horses[df_entry_horses[es.BATAIJU] != "   "]
        # df = df[(df[es.BATAIJU] > '000') & (df[es.BATAIJU] < '999')]

        df = df_entry_horses[
            (df_entry_horses[Es.BATAIJU] != "   ")
            & (df_entry_horses[Es.BATAIJU] > "000")
            & (df_entry_horses[Es.BATAIJU] < "999")
        ]
        print(f"Count: df={len(df)}")
        # print(f"Count: df={len(df)} df2={len(df2)}")
        # df_par_race.loc[:, ['rank_asc']] = df_par_race[es.BATAIJU].rank(numeric_only=False).astype(int)
        # df.loc[:,
        #     (df_entry_horses[es.BATAIJU] != "   ")
        #     & (df_entry_horses[es.BATAIJU] > '000')
        #     & (df_entry_horses[es.BATAIJU] < '999')
        # ] = ""

        group_cols = [Es.KAISAI_NEN, Es.KAISAI_TSUKIHI, Es.KEIBAJO_CODE, Es.RACE_BANGO]
        df_group_by = df.groupby(group_cols)

        # 馬体重ランキング列 昇順 の追加
        rank_bataiju_asc = df_group_by[Es.BATAIJU].rank(method="min").astype(int)
        rank_bataiju_asc.name = "rank_bataiju_asc"
        # 馬体重ランキング列 降順 の追加
        # rank_bataiju_desc = df_group_by[Es.BATAIJU].rank(ascending=False, method="min").astype(int)
        # rank_bataiju_desc.name = "rank_bataiju_desc"

        # 上がり 3 ハロンランキング
        df = df[(df[Es.KOHAN_3F] > "000") & (df[Es.KOHAN_3F] < "999")]
        # 上がり 3 ハロンランキング列 昇順 の追加
        df_group_by = df.groupby(group_cols)
        rank_kohan_3f_asc = df_group_by[Es.KOHAN_3F].rank(method="min").astype(int)
        rank_kohan_3f_asc.name = "rank_kohan_3f_asc"
        # 上がり 3 ハロンランキング列 降順 の追加
        # rank_kohan_3f_desc = df_group_by[Es.KOHAN_3F].rank(ascending=False, method="min").astype(int)
        # rank_kohan_3f_desc.name = "rank_kohan_3f_desc"

        # TODO 対戦型マイングのランキング

        self.df_custom_entry_horses = df.join(
            [rank_bataiju_asc, rank_kohan_3f_asc]
        )
        # self.df_custom_entry_horses = df.join(
        #     [rank_bataiju_asc, rank_bataiju_desc, rank_kohan_3f_asc, rank_kohan_3f_desc]
        # )

        # テーブル作成
        self.custom_horse_entry_repository.create_or_replace_table(self.df_custom_entry_horses)


if __name__ == "__main__":

    def main():
        conditions_string = None
        conditions = None

        # start_year = 2019
        # end_year = 2020
        # conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen <= '{end_year}'"
        conditions = {
            Es.KAISAI_NEN: "2020",
            Es.KAISAI_TSUKIHI: "0725",
            Es.KEIBAJO_CODE: "01",
            Es.RACE_BANGO: "04"}

        custom_entry_horse_repository = CustomEntryHorsesRepository()
        entry_horses_repository = EntryHorsesRepository()

        service = CustomEntryHorseService(
            custon_horse_entry_repository=custom_entry_horse_repository,
            entry_horses_repository=entry_horses_repository,
            conditions_string=conditions_string,
            conditions=conditions,
        )
        service.recreate_rank()
        print(f"size of df_custom_entry_horses: {len(service.df_custom_entry_horses)}")
        utils.output.show_one_line(service.df_custom_entry_horses)
        service.df_custom_entry_horses.to_csv("out.csv", index=False)
        df = service.df_custom_entry_horses
        print(df[["kakutei_chakujun", "rank_kohan_3f_asc", "tansho_ninkijun", "yoso_juni", "yoso_soha_time"]].sort_values("yoso_soha_time"))

    main()
