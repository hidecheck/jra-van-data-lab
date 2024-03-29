from repository.race_repository import RaceRepository
from utils import output

CONDITIONS = {
    "kaisai_nen": "2020",
    "kaisai_tsukihi": "1227",
    "keibajo_code": "06",
    "race_bango": "11"
}


class TestBaseRaceDisplay:
    def setup_method(self):
        self.repository = RaceRepository()

    def teardown_method(self):
        pass

    def test_find(self):
        df = self.repository.find(conditions=CONDITIONS)
        print(len(df))
        output.show_one_line(df, True)

    def test_find_with_conditions_string(self):
        # 障害レースのみ取得する
        conditions = {
            "kaisai_nen": "2020",
            "keibajo_code": "06"
        }
        conditions_string = "track_code > '30'"
        df = self.repository.find_with_conditions_string(conditions, conditions_string)
        print(len(df))
        output.show_line(df, 15, True)

    def test_find_with_conditions_string_empty(self):
        # 障害レースのみ取得する
        conditions = {
            "kaisai_nen": "2020",
            "keibajo_code": "06"
        }
        conditions_string = ""
        df = self.repository.find_with_conditions_string(conditions, conditions_string)
        print(len(df))
        output.show_line(df, 15, True)

    def test_find_with_conditions_string_none(self):
        # 障害レースのみ取得する
        conditions = {
            "kaisai_nen": "2020",
            "keibajo_code": "06"
        }
        conditions_string = None
        df = self.repository.find_with_conditions_string(conditions, conditions_string)
        print(len(df))
        output.show_line(df, 15, True)

    def test_find_without_conditions(self):
        df = self.repository.find()
        print(len(df))
        output.show_one_line(df, True)

    def test_find_conditions_empty(self):
        df = self.repository.find(conditions={})
        print(len(df))
        output.show_one_line(df, True)

    def test_find_conditions_none(self):
        df = self.repository.find(conditions=None)
        print(len(df))
        output.show_one_line(df, True)
