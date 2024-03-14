import utils.output
from repository.zi_repository import ZIRepository
from service.zi_service import ZIService


class TestCustomEntryHorseService:
    def setup_method(self):
        path = "/Users/ore/develop/keiba/jra-van-data-lab/external_data/ZI_DATA"
        repository = ZIRepository()
        self.service = ZIService(zi_data_folder=path, repositroy=repository)

    def teardown_method(self):
        pass

    def test_transform(self):
        utils.output.show_one_line(self.service.df_zi_data)
        assert "race_id" not in self.service.df_zi_data.iloc[0]
        assert "keibajo_code" in self.service.df_zi_data.iloc[0]
        assert "kaisai_nen" in self.service.df_zi_data.iloc[0]
        assert "kaisai_kai" in self.service.df_zi_data.iloc[0]
        assert "kaisai_nichime" in self.service.df_zi_data.iloc[0]
        assert "race_bango" in self.service.df_zi_data.iloc[0]

