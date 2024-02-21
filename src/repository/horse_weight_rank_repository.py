import utils.output
from const import table_name
from repository.base_repository import BaseRepository


class HorseWeightRankRepository(BaseRepository):
    COLUMNS = [
        "kaisai_nen",
        "kaisai_tsukihi",
        "keibajo_code",
        "race_bango",
        "umaban",
        "ketto_toroku_bango",
        "bataiju",
        "rank_asc",
        "rank_desc",
    ]

    def __init__(self):
        super().__init__()
        self.table = table_name.HORSE_WEIGHT_RANK

    def recreate_table(self):
        pass

    def bulk_insert(self):
        pass


if __name__ == '__main__':
    def main():
        start_year = 2015
        end_year = 2020
        conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen <= '{end_year}'"

        repository = HorseWeightRankRepository()
        df = repository.find_with_conditions_string(conditions_string=conditions_string)
        utils.output.show_one_line(df)


    main()
