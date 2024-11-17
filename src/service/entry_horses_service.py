import datetime
from typing import List, Tuple, Optional, Dict

import pandas as pd
from pandas import DataFrame, Series

import utils.output
from const import master_code
from const.table_columns.jvd_ra import CUSTOM_COL_RACE_ID
from const.table_columns.jvd_se import CUSTOM_COL_GENDER, CUSTOM_COL_WEIGHT_DIFFERENCE, CUSTOM_COL_WIN_FAVORITE, \
    CUSTOM_COL_WIN_BET, CUSTOM_COL_JOCKEY
from repository.entry_horses_repository import EntryHorsesRepository
from service.race_service import RaceService


class EntryHorsesService:
    """
    馬毎情報を操作クラス
    """

    def __init__(
            self,
            repository: Optional[EntryHorsesRepository] = None,
            conditions: Optional[Dict] = None,
            conditions_string: str = None,
            order=None,
            desc=False,
    ):
        # レースの全ての出走馬情報
        self.entry_horses: Optional[DataFrame] = None
        if repository:
            self.repository: EntryHorsesRepository = repository
        else:
            self.repository: EntryHorsesRepository = EntryHorsesRepository()
        self._set_entry_horses(conditions=conditions, conditions_string=conditions_string, order=order, desc=desc)

    def _set_entry_horses(self, conditions, conditions_string, order, desc):
        if conditions_string:
            self.entry_horses = self.repository.find_with_conditions_string(
                conditions=conditions,
                conditions_string=conditions_string,
                order=order,
                desc=desc)
        else:
            self.entry_horses = self.repository.find(conditions=conditions, order=order, desc=desc)

        # 馬名 空白除去
        self.entry_horses["bamei"] = self.entry_horses["bamei"].apply(lambda x: x.strip())

        # 列追加
        # レースID
        self.entry_horses[CUSTOM_COL_RACE_ID] = self.entry_horses.apply(RaceService.to_race_id, axis=1)
        # 性別
        self.entry_horses[CUSTOM_COL_GENDER] = self.entry_horses["seibetsu_code"].apply(lambda x: master_code.GENDER_CODE.get(x))
        # 馬体重増減
        self.entry_horses[CUSTOM_COL_WEIGHT_DIFFERENCE] = self.entry_horses.apply(self.to_weight_difference, axis=1)
        # 単勝オッズ
        self.entry_horses[CUSTOM_COL_WIN_BET] = self.entry_horses["tansho_odds"].apply(self.to_win_bet)
        # 単勝人気
        self.entry_horses[CUSTOM_COL_WIN_FAVORITE] = self.entry_horses["tansho_ninkijun"].astype(int)
        # 騎手名 空白除去
        self.entry_horses[CUSTOM_COL_JOCKEY] = self.entry_horses["kishumei_ryakusho"].apply(lambda x: x.strip())


    @staticmethod
    def to_weight_difference(row: Series):
        if row["zogen_sa"] == "000":
            # 増減差なし
            return "0"

        if row["zogen_sa"].strip() == "":
            # 初出走 or 出走取消
            return "999"

        if pd.isna(row["zogen_sa"]) or row["zogen_sa"] == "999":
            # 計量不能
            return "999"
            # return row["zogen_sa"]

        zogen_fugo = row["zogen_fugo"]
        zogen_sa = row["zogen_sa"].lstrip('0')

        if pd.isna(zogen_fugo):
            zogen_fugo = "+"

        return f"{zogen_fugo}{zogen_sa}"

    @staticmethod
    def to_win_bet(tansho_odds):
        """
        4桁の数字の文字列に3桁目の後に小数点を追加して数値に変換する関数

        Args:
        tansho_odds: 単勝オッズ, 4桁の数字の文字列

        Returns:
        float: 変換後の数値
        """

        integer_part = tansho_odds[:3]
        decimal_part = tansho_odds[3:]
        result = float(integer_part + "." + decimal_part)
        return result


    def get_entry_horse_by_ketto_toroku_bango(self, ketto_toroku_bango: str) -> Series:
        """
        登録番号を指定して出走情報を取得する

        Parameters
        ----------
        key: 検索キー
          血統登録番号, 馬名, 馬番など
        value: 検索バリュー
          血統登録番号, 馬名, 馬番などの値

        Returns
        -------

        """

        return self.get_entry_horse(key="ketto_toroku_bango", value=ketto_toroku_bango)

    def get_entry_horse(self, key: str, value: str) -> Series:
        """
        出走馬情報から指定した馬の出走情報を取得する

        Parameters
        ----------
        key: 検索キー
          血統登録番号, 馬名, 馬番など
        value: 検索バリュー
          血統登録番号, 馬名, 馬番などの値

        Returns
        -------

        """

        df_entry_horse = self.entry_horses[self.entry_horses[key] == value]
        return df_entry_horse.iloc[0].copy()

    def get_previous_entry_by_ketto_toroku_bango(self, ketto_toroku_bango: str):
        current_entry_horse = self.get_entry_horse_by_ketto_toroku_bango(ketto_toroku_bango)
        return self.get_previous_entry(current_entry_horse)

    def get_previous_entry(self, current_entry_horse: Series):
        """
        基準となるレースの出走馬の前走の情報を取得する
        Parameters
        ----------
        entry_horse: 基準となるレースの出走馬１頭

        Returns
        -------

        """
        return self.repository.find_previous_entry_by_entry_horse(current_entry_horse)

    def get_race_interval(self, entry_horse: Series):
        """
        レース間隔を取得
        Parameters
        ----------
        entry_horse

        Returns
        -------

        """
        previous_entry_horse = self.get_previous_entry(entry_horse)
        # 基準年月日
        year = int(entry_horse["kaisai_nen"])
        month = int(entry_horse["kaisai_tsukihi"][:2])
        day = int(entry_horse["kaisai_tsukihi"][2:])
        date_current = datetime.date(year, month, day)

        # 前走年月日
        year = int(previous_entry_horse["kaisai_nen"])
        month = int(previous_entry_horse["kaisai_tsukihi"][:2])
        day = int(previous_entry_horse["kaisai_tsukihi"][2:])
        date_prev = datetime.date(year, month, day)

        # 間隔（日単位）
        delta = date_current - date_prev
        # 間隔（週単位）
        # 日曜に出走したあとに土曜日に出走するケースがあるため、 +1 する
        interval_week = int((delta.days + 1) / 7) - 1
        if interval_week == -1:
            # 規則違反のためありえないが、間隔が５日以内の場合は -1 になるので 0 （連闘）にする
            interval_week = 0

        return delta.days

    @staticmethod
    def to_interval_week(days):
        # 日曜に出走したあとに土曜日に出走するケースがあるため、 +1 する
        interval_week = int((days + 1) / 7) - 1
        if interval_week == -1:
            # 規則違反のためありえないが、間隔が５日以内の場合は -1 になるので 0 （連闘）にする
            interval_week = 0

        return interval_week


if __name__ == '__main__':
    def main():
        conditions = {
            "kaisai_nen": "2019",
            "kaisai_tsukihi": "1222",
            "keibajo_code": "06",
            "race_bango": "11"
        }

        # repository = EntryHorsesRepository()
        # service = EntryHorsesService(repository, conditions)
        service = EntryHorsesService(conditions=conditions)
        df = service.entry_horses
        utils.output.show_one_line(df)

        print("-----------------")
        s = df.iloc[0]
        ketto_toroku_bango = s["ketto_toroku_bango"]
        current_entry_horse = service.get_entry_horse(key="ketto_toroku_bango", value=ketto_toroku_bango)
        interval = service.get_race_interval(current_entry_horse)
        print(f"{interval}（中{service.to_interval_week(interval)}週）")
        print()

    main()
