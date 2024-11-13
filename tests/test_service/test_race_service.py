import utils
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.horse_racing_service import HorseRacingService
from service.race_service import RaceService
from utils import output

CONDITIONS = {
    "kaisai_nen": "2019",
    "kaisai_tsukihi": "1222",
    "keibajo_code": "06",
    # "race_bango": "11"
}


class TestRaceService:
    def setup_method(self):
        race_repository = RaceRepository()

        self.service = RaceService(race_repository=race_repository, conditions=CONDITIONS)
        print()

    def teardown_method(self):
        pass

    def test_races(self):
        output.show_one_line(self.service.races, True)

    def test_to_race_id(self):
        race_repository = RaceRepository()
        races = race_repository.find(conditions=CONDITIONS)
        print(self.service.to_race_id(races.iloc[0]))
