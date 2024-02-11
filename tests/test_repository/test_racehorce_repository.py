import pandas

from repository.racehorce_repository import RacehorseRepository
from utils import output

conditions = {
    # "ketto_toroku_bango": "2014106220",
    "ketto_joho_01a": "1120002084"
    # "ketto_joho_01b": "ハーツクライ"
}


class TestRacehorseRepository:
    def setup_method(self):
        self.repository = RacehorseRepository()

    def teardown_method(self):
        pass

    def test_find(self):
        df = self.repository.find(conditions=conditions)
        print(len(df))
        output.show_one_line(df, True)
