import pandas

from repository.entry_horses_repository import EntryHorsesRepository
from repository.race_repository import RaceRepository
from repository.racehorce_repository import RacehorseRepository
from utils import output

CONDITIONS = {
    "kaisai_nen": "2019",
    "kaisai_tsukihi": "1222",
    "keibajo_code": "06",
    "race_bango": "11"
}


class TestEntryHorsesRepository:
    def setup_method(self):
        self.repository = EntryHorsesRepository()

    def teardown_method(self):
        pass

    def test_find(self):
        df = self.repository.find(conditions=CONDITIONS)
        print(len(df))
        output.show_one_line(df, True)

    def test_find_previous_entry(self):
        ketto_toroku_bango = "2015100600"
        kaisai_nen = "2019"
        kaisai_tsukihi = "1222"

        series = self.repository.find_previous_entry(ketto_toroku_bango=ketto_toroku_bango,
                                                kaisai_nen=kaisai_nen,
                                                kaisai_tsukihi=kaisai_tsukihi)
        output.show_series(series, True)
        df = self.repository.find(conditions=CONDITIONS)

    def test_find_previous_entry_by_entry_horse(self):
        df = self.repository.find(conditions=CONDITIONS)
        series = self.repository.find_previous_entry_by_entry_horse(df.iloc[0])
        output.show_series(series, True)

    def test_find_previous_entry_and_race_info(self):
        df = self.repository.find(conditions=CONDITIONS)
        series = self.repository.find_previous_entry_by_entry_horse(df.iloc[0])
        output.show_series(series, True)

        print("------------------------------------")
        # 前走のレース情報を取得
        race_repository = RaceRepository()
        # print(series.index)
        new_conditions = race_repository.to_conditions(series)
        df = race_repository.find(conditions=new_conditions)
        print(len(df))
        output.show_one_line(df, True)
