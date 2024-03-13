import glob

import numpy as np
import pandas as pd

import utils.output


class ZIService:
    """
    ZI データを操作する
    """
    COLUMN_NAMES = ["race_id", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18"]
    DTYPE = {0: str, 1: int, 2: int, 3: int, 4: int, 5: int, 6: int, 7: int, 8: int, 9: int, 10: int, 11: int, 12: int, 13: int, 14: int, 15: int, 16: int, 17: int, 18: int}
    # DTYPE = {0: str, 1: np.int64, 2: np.int64, 3: np.int64, 4: np.int64, 5: np.int64, 6: np.int64, 7: np.int64,
    #          8: np.int64, 9: np.int64, 10: np.int64, 11: np.int64, 12: np.int64, 13: np.int64, 14: np.int64,
    #          15: np.int64, 16: np.int64, 17: np.int64, 18: np.int64}
    MAX_CSV_COLUMN = 19
    MIN_YEAR = "54"   # JRA_VAN の最古のデータは1954年

    def __init__(self, zi_data_folder):
        self.zi_data_folder = zi_data_folder
        self.df_zi_data = pd.DataFrame()

    def read_csv(self):
        files = sorted(glob.glob(f"{self.zi_data_folder}/*"))
        list_df = []
        for file_name in files:
            print(file_name)
            df = pd.read_csv(file_name, names=self.COLUMN_NAMES, dtype={0: str})
            # for i in range(1, self.MAX_CSV_COLUMN):
            #     print(i)
            #     df[i] = pd.to_numeric(df.iloc[i], errors='coerce')
            #
            list_df.append(df)
        self.df_zi_data = pd.concat(list_df, ignore_index=True)
        self.df_zi_data = self.df_zi_data.fillna(-1)
        # self.transform()

    def to_int(self):
        for i in range(1, self.MAX_CSV_COLUMN):
            k = f'{i:02}'
            self.df_zi_data[k] = pd.to_numeric(self.df_zi_data[k], errors='coerce', downcast="integer")

    def transform(self):
        # TODO 次回やる
        self.df_zi_data["keibajo_code"] = self.df_zi_data["race_id"].str[:2]
        # self.df_zi_data["kaisai_nen"] = self.df_zi_data[0].str[2:2]

        pass




if __name__ == '__main__':
    path = "/Users/ore/develop/keiba/jra-van-data-lab/external_data/ZI_DATA"
    service = ZIService(zi_data_folder=path)
    service.read_csv()
    print(service.df_zi_data)
    print(service.df_zi_data.tail(10))
    utils.output.show_one_line(service.df_zi_data)
    service.to_int()
    print(service.df_zi_data)

    print(type(service.df_zi_data.iloc[0]["race_id"]))
    print(type(service.df_zi_data.iloc[0]["08"]))

