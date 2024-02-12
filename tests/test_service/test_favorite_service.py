import utils
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.favorite_service import FavoriteService
from service.horse_racing_service import HorseRacingService
from utils import output

CONDITIONS = {
    "kaisai_nen": "2019",
    "kaisai_tsukihi": "1222",
    "keibajo_code": "06",
    # "race_bango": "11"
}


class TestFavoriteService:
    def setup_method(self):
        race_repository = RaceRepository()
        entry_horses_repository = EntryHorsesRepository()
        payoff_repository = PayoffRepository()

        self.service = FavoriteService(race_repository=race_repository,
                                       entry_horses_repository=entry_horses_repository,
                                       payoff_repository=payoff_repository,
                                       conditions=CONDITIONS,
                                       favorite=1
                                       )

    def teardown_method(self):
        pass

    def test_to_summary_text(self):
        for race_id, entry_horse in self.service.all_favorite_horses.items():
            print(self.service.to_summary_text(race_id, entry_horse))
