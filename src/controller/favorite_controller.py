from typing import List

import pandas as pd
from pandas import DataFrame

from model.statistics import Statistics
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.favorite_service import FavoriteService
from utils import jargons_code, date_util


class FavoriteController:

    def __init__(self):
        self.race_repository = RaceRepository()
        self.entry_horses_repository = EntryHorsesRepository()
        self.payoff_repository = PayoffRepository()

    def get_past_years_rate_win_by_racecourse(self, keibajo_code: str, favorite: int, years_ago: int, is_obstacle: bool = False) -> Statistics:
        """
        指定した競馬場の過去 N 年分の N 番人気の単勝回収率を取得する。開始月日は 1月1日固定

        Parameters
        ----------
        keibajo_code
        favorite
        years_ago
        is_obstacle

        Returns
        -------

        """

        end_year = date_util.get_current_year()
        start_year = end_year - years_ago
        conditions = {
            "keibajo_code": keibajo_code,
        }
        conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen < '{end_year}'"

        if is_obstacle is False:
            conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen < '{end_year}' AND track_code < '30'"

        service = FavoriteService(race_repository=self.race_repository,
                                  entry_horses_repository=self.entry_horses_repository,
                                  payoff_repository=self.payoff_repository,
                                  conditions=conditions,
                                  conditions_string=conditions_string,
                                  favorite=favorite)

        return service.statistics

    def get_past_years_rate_win(self, list_keibajo_code: List, list_favorite: List[int], years_ago: int, is_obstacle: bool = False) -> DataFrame:
        """
        複数の競馬場の過去 N 年分の N 番人気の単勝回収率を取得する。開始月日は 1月1日固定

        Parameters
        ----------
        list_keibajo_code
        list_favorite
        years_ago
        is_obstacle

        Returns
        -------

        """

        end_year = date_util.get_current_year()
        start_year = end_year - years_ago
        conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen < '{end_year}'"

        if is_obstacle is False:
            conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen < '{end_year}' AND track_code < '30'"

        # favorite_service コンテナの作成
        #   各競馬場ごとの人気ごとの favorite_service のコンテナ
        #     favorite_services = {
        #        str: List[FavoriteService]
        #        "札幌": list_favorite_service_sapporo
        #        "東京": list_favorite_service_tokyo
        #     }
        favorite_services = {}
        for keibajo_code in list_keibajo_code:
            keibajo_name = jargons_code.to_race_course(keibajo_code)
            conditions = {
                "keibajo_code": keibajo_code,
            }

            services: List[FavoriteService] = []   # 人気毎のFavoriteService
            for favorite in list_favorite:
                service = FavoriteService(race_repository=self.race_repository,
                                          entry_horses_repository=self.entry_horses_repository,
                                          payoff_repository=self.payoff_repository,
                                          conditions=conditions,
                                          conditions_string=conditions_string,
                                          favorite=favorite)
                services.append(service)

            favorite_services[keibajo_name] = services

        # 回収率表の作成
        #   以下のようなデータを作る
        #   column_names = ["人気", "札幌", "東京" ]
        #   data = {
        #       "人気": [1, 2, 3],
        #       "札幌": ["1番人気回収率", "2番人気回収率", "3番人気回収率"],
        #       "東京": ["1番人気回収率", "2番人気回収率", "3番人気回収率"],
        #   }
        race_courses = list(favorite_services.keys())
        column_names = ["人気"] + race_courses
        data = {
            "人気": list_favorite,
        }
        for race_cource, list_service in favorite_services.items():
            return_rate_wins = []
            for service in list_service:
                return_rate_wins.append(service.statistics.return_rate_win)
            # 例) "札幌": ["1番人気回収率", "2番人気回収率", "3番人気回収率"]
            data[race_cource] = return_rate_wins
        df = pd.DataFrame(data, columns=column_names)
        return df


if __name__ == '__main__':
    def main():
        # keibajo_code = "05"
        # favorite = 1
        # years_ago = 5
        # is_obstacle = False
        # controller = FavoriteController()
        # statistics = controller.get_past_years_rate_win_by_racecourse(keibajo_code=keibajo_code, favorite=favorite, years_ago=years_ago, is_obstacle=is_obstacle)
        # print(statistics)

        list_keibajo_code = ["01", "02"]
        list_favorite = list(range(1, 4))
        years_ago = 1
        is_obstacle = False
        controller = FavoriteController()
        df = controller.get_past_years_rate_win(list_keibajo_code=list_keibajo_code, list_favorite=list_favorite, years_ago=years_ago, is_obstacle=is_obstacle)
        print(df)

    main()