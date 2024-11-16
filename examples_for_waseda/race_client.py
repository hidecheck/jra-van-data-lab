from time import sleep

from const.table_columns import jvd_ra
from repository.race_repository import RaceRepository
from service.race_service import RaceService
from utils import output


def main():
    conditions = {
        "kaisai_nen": "2019",
        "kaisai_tsukihi": "1222",
        "keibajo_code": "06",
        # "race_bango": "11",
    }
    service = RaceService(conditions=conditions)

    print(len(service.races))
    output.show_line(service.races, 0, False)

    # for i in range(12):
    #     print()
    #     print("#####Wait...")
    #     print()
    #     sleep(2)
    #     output.show_line(service.races, i, False)
    #
    # print("#####Wait...")
    df = service.races.loc[:, jvd_ra.MINIMUM_COLUMNS]
    df.drop('track_code', axis=1, inplace=True)
    output.show_one_line(df, False)

    file_name = "2019-12-22_nakayama_race_info.csv"
    df.to_csv(file_name, index=False)


if __name__ == '__main__':
    main()