import utils
from controller.favorite_controller import FavoriteController
from repository.entry_horses_repository import EntryHorsesRepository
from repository.payoff_repository import PayoffRepository
from repository.race_repository import RaceRepository
from service.favorite_service import FavoriteService
from service.horse_racing_service import HorseRacingService
from utils import output


class TestFavoriteController:
    def setup_method(self):
        self.controller = FavoriteController()

    def test_get_past_years_rate_win_by_racecourse(self):
        keibajo_code = "05"
        favorite = 1
        years_ago = 5
        is_obstacle = False
        statistics = self.controller.get_past_years_rate_win_by_racecourse(keibajo_code=keibajo_code, favorite=favorite,
                                                                      years_ago=years_ago, is_obstacle=is_obstacle)
        print(statistics)

    def test_get_past_years_rate_win(self):
        list_keibajo_code = ["01", "02"]
        list_favorite = list(range(1, 4))
        years_ago = 1
        is_obstacle = False
        controller = FavoriteController()
        df = self.controller.get_past_years_rate_win(list_keibajo_code=list_keibajo_code, list_favorite=list_favorite, years_ago=years_ago, is_obstacle=is_obstacle)
        print(df)

