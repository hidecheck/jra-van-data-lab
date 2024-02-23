from repository.custom_entry_horse_repository import CustomEntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from utils import output

conditions = {
    "kaisai_nen": "2020",
    "kaisai_tsukihi": "1227",
    "keibajo_code": "06",
    "race_bango": "11"
}


class TestCustomEntryHorsesRepository:
    def setup_method(self):
        self.repository = CustomEntryHorsesRepository()

    def teardown_method(self):
        pass

    def test_find(self):
        df = self.repository.find(conditions=conditions)
        print(len(df))
        output.show_one_line(df, True)
