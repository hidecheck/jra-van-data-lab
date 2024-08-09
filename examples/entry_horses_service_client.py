import pandas as pd

from repository.entry_horses_repository import EntryHorsesRepository
from service.entry_horses_service import EntryHorsesService


def main():
    conditions = {
        "kaisai_nen": "2019",
        "kaisai_tsukihi": "1222",
        "keibajo_code": "06",
    }
    conditions_string = "race_bango > '10'"

    repository = EntryHorsesRepository()
    service = EntryHorsesService(repository, conditions=conditions, conditions_string=conditions_string)
    df = service.entry_horses
    out_df = pd.DataFrame()
    out_df["race_bango"] = df["race_bango"]
    out_df["umaban"] = df["umaban"]
    out_df["bamei"] = df["bamei"]
    out_df["bataiju"] = df["bataiju"]
    out_df["tansho_ninkijun"] = df["tansho_ninkijun"]
    out_df["tansho_odds"] = df["tansho_odds"]

    # for index, row in service.entry_horses.iterrows():
    #     print(row["race_bango"], row["umaban"], row["bamei"], row["bataiju"], row["tansho_ninkijun"],
    #           row["tansho_odds"])
    print(out_df)
    out_df.to_csv("entry_horses_service_client.csv", index=False)


if __name__ == '__main__':
    main()

