import pandas as pd

import utils
from const.table_columns import jvd_se
from const.table_columns.jvd_ra import CUSTOM_COL_RACE_ID
from const.table_columns.jvd_se import CUSTOM_COL_WIN_BET, CUSTOM_COL_WIN_FAVORITE, CUSTOM_COL_GENDER, \
    CUSTOM_COL_WEIGHT_DIFFERENCE
from repository.entry_horses_repository import EntryHorsesRepository
from service.entry_horses_service import EntryHorsesService
from utils import output


def create_csv(conditions, file_name):
    # conditions_string = "race_bango > '10'"
    # service = EntryHorsesService(conditions=conditions, conditions_string=conditions_string)
    service = EntryHorsesService(conditions=conditions)

    df = service.entry_horses.loc[:, jvd_se.MINIMUM_COLUMNS]
    output.show_one_line(df, False)
    print(df)
    df.to_csv(file_name, index=False)


def group_by_bataiju(file_name):
    df = pd.read_csv(file_name)
    print(df)

    group_cols = ["race_bango"]
    grouped = df.groupby(group_cols)
    rank_bataiju = grouped["bataiju"].rank(method="min").astype(int)
    rank_bataiju.name = "rank_bataiju"
    print(rank_bataiju)
    df = df.join([rank_bataiju])
    print(df)
    sorted_df = df.sort_values(by=["race_bango", "bataiju"])
    print(sorted_df)

# def read_from_spleadsheet():
#     from google.colab import auth
#     from google.auth import default
#     import gspread
#
#     import pandas as pd
#
#     auth.authenticate_user()
#     creds, _ = default()
#     gc = gspread.authorize(creds)
#
#     key = "1hO41YOQzjOnIr0VKuDK39FVs2yKOjVjQzPjc2WdeETI"
#     workbook = gc.open_by_key(key)
#     worksheet = workbook.worksheet("2019-12-22_nakayama_11-12R")
#     data = worksheet.get_all_values()
#     # 一行目に不要な行が入っている時  #data .pop(0)
#
#     _df = pd.DataFrame(data, columns=data[0])
#     df = _df.drop(_df.index[0])
#     print(df)

def main():
    conditions = {
        "kaisai_nen": "2019",
        "kaisai_tsukihi": "1222",
        "keibajo_code": "06",
        "race_bango": "11"
    }

    file_name = "2019-12-22_nakayama_11R.csv"
    create_csv(conditions, file_name)
    # group_by_bataiju(file_name)


if __name__ == '__main__':
    main()

