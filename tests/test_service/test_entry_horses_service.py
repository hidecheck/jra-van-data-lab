import utils.output
from repository.entry_horses_repository import EntryHorsesRepository
from service.entry_horses_service import EntryHorsesService

CONDITIONS = {
    "kaisai_nen": "2019",
    "kaisai_tsukihi": "1222",
    "keibajo_code": "06",
    "race_bango": "11"
}


class TestEntryHorsesService:
    def setup_method(self):
        repository = EntryHorsesRepository()
        self.service = EntryHorsesService(repository, conditions=CONDITIONS)

    def teardown_method(self):
        pass

    def test_init_with_conditions_string(self):
        conditions = {
            "kaisai_nen": "2019",
            "kaisai_tsukihi": "1222",
            "keibajo_code": "06",
        }
        conditions_string = "race_bango > '10'"

        repository = EntryHorsesRepository()
        self.service = EntryHorsesService(repository, conditions=conditions, conditions_string=conditions_string)
        for index, row in self.service.entry_horses.iterrows():
            print(row["race_bango"], row["umaban"], row["bamei"], row["bataiju"], row["tansho_ninkijun"], row["tansho_odds"])

    def test_get_entry_horse(self):
        df = self.service.entry_horses
        s = df.iloc[0]
        ketto_toroku_bango = s["ketto_toroku_bango"]
        entry_horse = self.service.get_entry_horse(key="ketto_toroku_bango", value=ketto_toroku_bango)
        utils.output.show_series(entry_horse, True)


    def test_get_previous_entry(self):
        df = self.service.entry_horses
        current_entry_horse = df.iloc[0].copy()
        prev_entry_horse = self.service.get_previous_entry(current_entry_horse)
        print(prev_entry_horse)

    def test_get_interval(self):
        df = self.service.entry_horses
        entry_horse = df.iloc[0].copy()
        interval = self.service.get_race_interval(entry_horse)
        print(f"{interval}（中{self.service.to_interval_week(interval)}週）")
