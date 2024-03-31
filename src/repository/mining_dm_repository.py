from const import table_name
from repository.base_repository import BaseRepository


class MiningDmRepository(BaseRepository):
    """
    タイム型マイングのDB操作クラス
    """

    def __init__(self):
        super().__init__()
        self.table = table_name.MINING_DM
