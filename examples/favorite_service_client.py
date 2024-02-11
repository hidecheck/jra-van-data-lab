from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.favorite_service import FavoriteService


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

    print(service.statictics)


def main():
    get_top_10_years_rate()


if __name__ == '__main__':
    main()
