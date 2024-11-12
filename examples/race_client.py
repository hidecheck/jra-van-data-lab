from time import sleep

from repository.race_repository import RaceRepository
from service.race_service import RaceService
from utils import output

TARGET_COLS = [
    "kaisai_nen",
    "kaisai_tsukihi",
    "keibajo_code",
    "kaisai_kai",
    "kaisai_nichime",
    "race_bango",
    "kyosomei_hondai",
    "grade_code",
    "",
    "",
    "",
    "",
    "",
    "",
    "",
]


def main():
    repository = RaceRepository()
    conditions = {
        "kaisai_nen": "2020",
        "kaisai_tsukihi": "1227",
        "keibajo_code": "06",
        "race_bango": "11",
    }
    service = RaceService(race_repository=repository, conditions=conditions)

    print(len(service.races))
    output.show_line(service.races, 0, False)
    # print("#####Wait...")
    # sleep(2)
    # output.show_line(service.races, 1, False)

    print("#####Wait...")
    df = service.races.loc[:, ["data_kubun", "data_sakusei_nengappi"]]
    sleep(2)
    output.show_one_line(df, False)



if __name__ == '__main__':
    main()