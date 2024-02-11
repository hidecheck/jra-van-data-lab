from sqlalchemy import text

from const import const_table_name
from repository.base_repository import BaseRepository
from utils import output


class RacehorseRepository(BaseRepository):
    """
    競争馬情報のDB操作クラス
    """
    def __init__(self):
        super().__init__()
        self.table = const_table_name.RACEHORSE

    def find_by_bamei(self, bamei):
        sql = f"SELECT * FROM {self.table} WHERE bamei LIKE '{bamei}%'"
        return self.read_sql(sql=text(sql))


if __name__ == '__main__':

    def main():
        repository = RacehorseRepository()
        conditions = {
            "ketto_toroku_bango": "2014106220"
        }
        # df = service.find(conditions=conditions)
        # print(len(df))
        df = repository.find_by_bamei('ハーツクライ')
        print(len(df))

        output.show_one_line(df, True)

    main()
