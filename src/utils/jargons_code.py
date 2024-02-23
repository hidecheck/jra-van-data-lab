"""
マスターコードの変換関係のユーティリティ
"""

DICT_RACE_COURSE = {
    "01": "札幌",
    "02": "函館",
    "03": "福島",
    "04": "新潟",
    "05": "東京",
    "06": "中山",
    "07": "中京",
    "08": "京都",
    "09": "阪神",
    "10": "小倉",
}


def to_race_course(code):

    if code in DICT_RACE_COURSE:
        return DICT_RACE_COURSE[code]
    else:
        return "なし"
