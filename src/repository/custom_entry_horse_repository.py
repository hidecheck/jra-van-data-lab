from pandas import DataFrame

import utils.output
from const import table_name
from repository.base_repository import BaseRepository


class CustomEntryHorsesRepository(BaseRepository):

    def __init__(self):
        super().__init__()
        self.table = table_name.CUSTOM_ENTRY_HORSE

    def replace_table(self, df: DataFrame):
        df.to_sql(name=self.table, con=self.engine, if_exists="replace", index=False)

    def append(self, df: DataFrame):
        df.to_sql(name=self.table, con=self.engine, if_exists="append", index=False)


if __name__ == '__main__':
    def main():
        start_year = 2015
        end_year = 2020
        conditions_string = f"kaisai_nen >= '{start_year}' AND kaisai_nen <= '{end_year}'"

        repository = CustomEntryHorsesRepository()
        df = repository.find_with_conditions_string(conditions_string=conditions_string)
        utils.output.show_one_line(df)


    main()
