import pandas as pd

import utils
from repository.entry_horses_repository import EntryHorsesRepository
from service.entry_horses_service import EntryHorsesService


def create_csv(conditions, file_name):
    # conditions_string = "race_bango > '10'"
    # service = EntryHorsesService(conditions=conditions, conditions_string=conditions_string)
    service = EntryHorsesService(conditions=conditions)

    df = service.entry_horses
    utils.output.show_one_line(df)

    out_df = pd.DataFrame()
    out_df["race_bango"] = df["race_bango"]
    out_df["umaban"] = df["umaban"]
    out_df["bamei"] = df["bamei"].apply(lambda x: x.strip())
    # out_df["bamei"] = df["bamei"]
    out_df["bataiju"] = df["bataiju"]
    out_df["zogen_sa"] = df["zogen_sa"]
    out_df["kohan_3f"] = df["kohan_3f"]
    # out_df["tansho_ninkijun"] = df["tansho_ninkijun"]
    out_df["tansho_odds"] = df["tansho_odds"]
    out_df["kakutei_chakujun"] = df["kakutei_chakujun"]
    out_df["time_sa"] = df["time_sa"]

    # for index, row in service.entry_horses.iterrows():
    #     print(row["race_bango"], row["umaban"], row["bamei"], row["bataiju"], row["tansho_ninkijun"],
    #           row["tansho_odds"])
    print(out_df)
    out_df.to_csv(file_name, index=False)

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

    file_name = "entry_horses_service_client.csv"
    file_name = "2019-12-22_nakayama_11R.csv"
    create_csv(conditions, file_name)
    # group_by_bataiju(file_name)

if __name__ == '__main__':
    main()

