from typing import Dict, Optional

from pandas import DataFrame, Series

from const import table_name
from repository.base_repository import BaseRepository
from utils import output


class ZIRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = table_name.ZI

    def create_or_replace(self):
        pass

    def append(self):
        pass
