from typing import Dict, Optional

from pandas import DataFrame

from const import const_table_name
from repository.base_repository import BaseRepository


class HorseWeightRankingRepository(BaseRepository):
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
        self.table = const_table_name.HORSE_WEIGHT_RANKING

    def create_table(self):
        pass

    def bulk_insert(self):
        pass
