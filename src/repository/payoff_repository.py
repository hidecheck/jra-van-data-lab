from const import table_name
from repository.base_repository import BaseRepository
from utils import output


class PayoffRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = table_name.PAYOFF


if __name__ == '__main__':

    def main():
        repository = PayoffRepository()
        conditions = {
            "kaisai_nen": "2020",
            "kaisai_tsukihi": "1227",
            "keibajo_code": "06",
            "race_bango": "11"
        }
        df = repository.find(conditions=conditions)
        print(len(df))
        # df = service.find_by_bamei('ハーツクライ')
        # print(len(df))

        output.show_one_line(df, True)

    main()
