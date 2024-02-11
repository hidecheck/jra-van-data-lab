from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class Statistics:
    total_arrivals: int
    """全着回数（馬の頭数相当）"""

    finishing_position_statistics: List[int]
    """着順集計"""

    hitting_rate_win: Decimal
    """単勝的中率"""

    hitting_rate_place: Decimal
    """複勝的中率"""

    return_rate_win: Decimal
    """単勝回収率"""

    return_rate_place: Decimal
    """複勝回収率"""

    sum_win: int
    """単勝合計金額"""

    sum_place: int
    """複勝合計金額"""

    def __str__(self):
        s = f"着回数: {self.finishing_position_statistics} | {self.total_arrivals}\n"
        s += f"単勝的中率: {self.hitting_rate_win * 100}%\n"
        s += f"複勝的中率: {self.hitting_rate_place * 100}%\n"
        s += f"単勝合計: {self.sum_win}円, 単勝回収率: {self.return_rate_win * 100}%\n"
        s += f"複勝合計: {self.sum_place}円, 複勝回収率: {self.return_rate_place * 100}%\n"
        return s
