import utils
from repository.custom_entry_horse_repository import CustomEntryHorsesRepository
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.custom_entry_horses_service import CustomEntryHorseService
from service.horse_racing_service import HorseRacingService
from utils import output

CONDITIONS = {
    "kaisai_nen": "2020",
    "kaisai_tsukihi": "0725",
    "keibajo_code": "01",
    # "race_bango": "01"
}


class TestCustomEntryHorseService:
    def setup_method(self):
        entry_horses_repository = EntryHorsesRepository()
        custom_entry_horse_repository = CustomEntryHorsesRepository()
        self.service = CustomEntryHorseService(
            custon_horse_entry_repository=custom_entry_horse_repository,
            entry_horses_repository=entry_horses_repository,
            conditions=CONDITIONS)
        print()

    def teardown_method(self):
        pass

    def test_recreate_rank(self):
        self.service.recreate_rank()
        print(f"size of df_custom_entry_horses: {len(self.service.df_custom_entry_horses)}")
        utils.output.show_one_line(self.service.df_custom_entry_horses)
        self.service.df_custom_entry_horses.to_csv("test_out.csv", index=False)


