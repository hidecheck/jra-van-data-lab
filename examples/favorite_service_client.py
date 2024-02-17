import pandas as pd

from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.favorite_service import FavoriteService


def get_favorite_rate():
    conditions_string = None

<<<<<<< HEAD
    # 障害レースなしの日
=======
    # # 障害レースなしの日
>>>>>>> origin/main
    conditions = {
        "kaisai_nen": "2019",
        "kaisai_tsukihi": "0126",
        "keibajo_code": "05",
    }
    # # 障害レースありの日
    # conditions = {
    #     # "kaisai_nen": "2020",
    #     # "kaisai_tsukihi": "1226",
    #     "keibajo_code": "06",
    # }

    race_repository = RaceRepository()
    entry_horses_repository = EntryHorsesRepository()
    payoff_repository = PayoffRepository()

    service = FavoriteService(race_repository=race_repository, entry_horses_repository=entry_horses_repository,
                              payoff_repository=payoff_repository, conditions=conditions,
                              conditions_string=conditions_string, favorite=1)

    print(f"{service.favorite}人気: {service.statistics}")


def get_top_10_years_rate():
    """
    10 年間の東京競馬場 1 番人気のデータ集計
    """
    conditions = {
        "keibajo_code": "05",
    }
    conditions_string = "kaisai_nen >= '2010' AND kaisai_nen < '2020' AND track_code < '30'"

    race_repository = RaceRepository()
    entry_horses_repository = EntryHorsesRepository()
    payoff_repository = PayoffRepository()

    service = FavoriteService(race_repository=race_repository, entry_horses_repository=entry_horses_repository,
                              payoff_repository=payoff_repository, conditions=conditions,
                              conditions_string=conditions_string, favorite=1)

    print(f"{service.favorite}人気: {service.statistics}")


def get_favorite_rate_tokyo_and_sapporo():
    """
    5 年間の東京競馬場と札幌競馬場の 1 番人気のデータ集計
    """

    conditions_tokyo = {
        "keibajo_code": "05",
    }
    conditions_sapporo = {
        "keibajo_code": "01",
    }
    conditions_string = "kaisai_nen >= '2015' AND kaisai_nen < '2020' AND track_code < '30'"
    race_repository = RaceRepository()
    entry_horses_repository = EntryHorsesRepository()
    payoff_repository = PayoffRepository()

    favorite_service_tokyo = FavoriteService(race_repository=race_repository, entry_horses_repository=entry_horses_repository,
                              payoff_repository=payoff_repository, conditions=conditions_tokyo,
                              conditions_string=conditions_string, favorite=1)

    favorite_service_sapporo = FavoriteService(race_repository=race_repository, entry_horses_repository=entry_horses_repository,
                              payoff_repository=payoff_repository, conditions=conditions_sapporo,
                              conditions_string=conditions_string, favorite=1)
    favorite_services = {
        "札幌": favorite_service_sapporo,
        "東京": favorite_service_tokyo,
    }

    # 以下のようなデータを作る
    # data = {
    #     "人気": [1],
    #     "札幌": ["札幌回収率"],
    #     "東京": ["東京回収率"]
    # }
    race_courses = list(favorite_services.keys())
    column_names = ["人気"] + race_courses
    data = {
        "人気": [1]
    }
    for race_course, service in favorite_services.items():
        data[race_course] = [service.statistics.return_rate_win]

    df = pd.DataFrame(data=data, columns=column_names)
    print(df)


def get_favorite_rate_tokyo_and_sapporo_1to3():
    """
    1 年間の東京競馬場と札幌競馬場の 1 ~ 3 番人気のデータ集計
    """

    conditions_tokyo = {
        "keibajo_code": "05",
    }
    conditions_sapporo = {
        "keibajo_code": "01",
    }
    conditions_string = "kaisai_nen >= '2019' AND kaisai_nen < '2020' AND track_code < '30'"
    race_repository = RaceRepository()
    entry_horses_repository = EntryHorsesRepository()
    payoff_repository = PayoffRepository()

    list_favorite_service_tokyo = []
    list_favorite_service_sapporo = []

    for i in range(1, 4):
        list_favorite_service_tokyo.append(
            FavoriteService(race_repository=race_repository,
                            entry_horses_repository=entry_horses_repository,
                            payoff_repository=payoff_repository, conditions=conditions_tokyo,
                            conditions_string=conditions_string, favorite=i)
        )
        list_favorite_service_sapporo.append(
            FavoriteService(race_repository=race_repository,
                            entry_horses_repository=entry_horses_repository,
                            payoff_repository=payoff_repository, conditions=conditions_sapporo,
                            conditions_string=conditions_string, favorite=i)
        )
    favorite_services = {
        "札幌": list_favorite_service_sapporo,
        "東京": list_favorite_service_tokyo,
    }

    # 回収率表の作成
    # 以下のようなデータを作る
    # column_names = ["人気", "札幌", "東京" ]
    # data = {
    #     "人気": [1, 2, 3],
    #     "札幌": ["1番人気回収率", "2番人気回収率", "3番人気回収率"],
    #     "東京": ["1番人気回収率", "2番人気回収率", "3番人気回収率"],
    # }
    race_courses = list(favorite_services.keys())
    column_names = ["人気"] + race_courses
    data = {
        "人気": [1, 2, 3],
    }
    for race_cource, list_service in favorite_services.items():
        return_rate_wins = []
        for service in list_service:
            return_rate_wins.append(service.statistics.return_rate_win)
        # 例) "札幌": ["1番人気回収率", "2番人気回収率", "3番人気回収率"]
        data[race_cource] = return_rate_wins
    df = pd.DataFrame(data, columns=column_names)
    print(df)


def main():
    # get_favorite_rate()
    # get_top_10_years_rate()
    # get_favorite_rate_tokyo_and_sapporo()
    get_favorite_rate_tokyo_and_sapporo_1to3()


if __name__ == '__main__':
    main()
