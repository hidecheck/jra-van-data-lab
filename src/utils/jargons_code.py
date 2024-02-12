"""
マスターコードの変換関係のユーティリティ
"""


def to_race_course(code):
    dict_race_course = {
        "01": "札幌",
        "05": "東京",
    }

    return dict_race_course[code]

