from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Optional

from pandas import Series

import utils.math
from model.statistics import Statistics
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.horse_racing_service import HorseRacingService


class FavoriteService(HorseRacingService):
    """
    指定した人気馬の馬毎情報を取得する
    """
    def __init__(self, race_repository: RaceRepository, entry_horses_repository: EntryHorsesRepository,
                 payoff_repository: PayoffRepository, conditions: Dict, conditions_string: str = None,
                 favorite: int = 1, order=None, desc=False):
        super().__init__(race_repository=race_repository,
                         entry_horses_repository=entry_horses_repository,
                         payoff_repository=payoff_repository,
                         conditions=conditions,
                         conditions_string=conditions_string)
        self.favorite: str = f"{favorite:02d}"
        self.statistics: Optional[Statistics] = None

        self.all_favorite_horses: Dict[str: Series] = {}
        self.set_favorite_horses()
        self.set_statistics()

    def set_favorite_horses(self):
        for race_id, entry_horses in self.all_entry_horses.items():
            for index, entry_horse in entry_horses.iterrows():
                if entry_horse["tansho_ninkijun"] == "00":
                    continue
                elif entry_horse["tansho_ninkijun"] == self.favorite:
                    self.all_favorite_horses[race_id] = entry_horse
                    continue

    def set_statistics(self):
        # TODO HorseRacingService.initialize をオーバーライドして、統計を出したほうがパフォーマンスがいい（self.races を2回回してるため）
        finishing_position_statistics = [0] * 4
        horses_num = len(self.all_favorite_horses)
        sum_win = 0    # 的中単勝合計
        sum_place = 0  # 的中複勝合計

        # 着順統計
        for race_id, entry_horse in self.all_favorite_horses.items():
            chakujun = int(entry_horse['kakutei_chakujun'])
            if chakujun > 3:
                # 着外
                finishing_position_statistics[3] += 1
            else:
                # 3着以内
                finishing_position_statistics[chakujun-1] += 1

                # 的中複勝合計
                for i in range(1, 6):
                    key_haraimodoshi_fukusho_a = f"haraimodoshi_fukusho_{i}a"    # 複勝馬番のキー
                    key_haraimodoshi_fukusho_b = f"haraimodoshi_fukusho_{i}b"    # 複勝払い戻し金額のキー

                    if not self.all_payoff[race_id][key_haraimodoshi_fukusho_b].isdigit():
                        # haraimodoshi_fukusho_4b 移行は同着データのためデータが入ってないことがある
                        # haraimodoshi_fukusho_4b が貼ってない場合は haraimodoshi_fukusho_5b もはいってないので break で抜ける
                        break

                    fukusho_umaban = int(self.all_payoff[race_id][key_haraimodoshi_fukusho_a])
                    entry_umaban = int(entry_horse["umaban"])
                    if fukusho_umaban == entry_umaban:
                        sum_place += int(self.all_payoff[race_id][key_haraimodoshi_fukusho_b])
                        break

                if chakujun == 1:
                    # 的中単勝勝合計
                    sum_win += int(self.all_payoff[race_id]["haraimodoshi_tansho_1b"])
                    if self.all_payoff[race_id]["haraimodoshi_tansho_2b"].isdigit():
                        sum_win += int(self.all_payoff[race_id]["haraimodoshi_tansho_2b"])
                    if self.all_payoff[race_id]["haraimodoshi_tansho_3b"].isdigit():
                        sum_win += int(self.all_payoff[race_id]["haraimodoshi_tansho_3b"])

        # 単勝率（単勝的中率）
        #   計算式: 1着回数 / 全着数 （全着数 = 頭数）
        hitting_rate_win = utils.math.division_and_round(finishing_position_statistics[0], horses_num)
        print(hitting_rate_win)

        # 複勝率（複勝的中率）
        #   計算式: 1着 ~ 3着の合計着数 / 全着数
        place_count = finishing_position_statistics[0] + finishing_position_statistics[1] + finishing_position_statistics[2]
        hitting_rate_place = utils.math.division_and_round(place_count, horses_num)

        # 単勝的中率と回収率
        #   計算式: 回収率 = 単勝払い戻し合計 / 払った金額
        #   払った金額 = 全着数 * 100（円）
        if finishing_position_statistics[0] == 0:
            return_rate_win = 0
        else:
            return_rate_win = utils.math.division_and_round(sum_win, horses_num * 100)

        # 複勝的中率と回収率
        return_rate_place = utils.math.division_and_round(sum_place, horses_num * 100)

        self.statistics = Statistics(total_arrivals=horses_num,
                                     finishing_position_statistics=finishing_position_statistics,
                                     hitting_rate_win=hitting_rate_win,
                                     hitting_rate_place=hitting_rate_place,
                                     return_rate_win=return_rate_win,
                                     return_rate_place=return_rate_place,
                                     sum_win=sum_win,
                                     sum_place=sum_place)

    def to_summary_text(self, race_id, entry_horse: Series):
        year = race_id[:4]
        month = race_id[5:7]
        day = race_id[8:10]
        racing_venue = race_id[11:13]
        race_no = race_id[14:]

        text = (f"{year}-{month}-{day} 競馬場コード({racing_venue}) {race_no}R: "
                f"{entry_horse['bamei']} {entry_horse['kakutei_chakujun']}着 "
                f"{float(entry_horse['tansho_odds']) / 10}倍 ({self.favorite}人気)")

        return text


if __name__ == '__main__':
    def main():
        conditions_string = None
        # conditions = {
        #     "kaisai_nen": "2019",
        #     "kaisai_tsukihi": "0126",
        #     "keibajo_code": "05",
        # }
        # # 障害含む
        # conditions = {
        #     # "kaisai_nen": "2020",
        #     # "kaisai_tsukihi": "1226",
        #     "keibajo_code": "06",
        # }
        conditions = {
            "keibajo_code": "05",
        }
        conditions_string = "kaisai_nen >= '2010' AND kaisai_nen < '2020' AND track_code < '30'"

        race_repository = RaceRepository()
        entry_horses_repository = EntryHorsesRepository()
        payoff_repository = PayoffRepository()

        service = FavoriteService(race_repository=race_repository, entry_horses_repository=entry_horses_repository,
                                  payoff_repository=payoff_repository, conditions=conditions, conditions_string=conditions_string, favorite=1)

        # for race_id, entry_horse in service.all_favorite_horses.items():
        #     print(service.to_summary_text(race_id, entry_horse))
        #
        print(f"{service.favorite}人気: {service.statistics}")

    main()
