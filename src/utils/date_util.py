from datetime import datetime
from datetime import timedelta
from datetime import timezone

JST = timezone(timedelta(hours=+9), "JST")


def get_current_jst() -> datetime:
    current_time = datetime.now(JST) - timedelta()
    return current_time


def get_current_year():
    current_time = get_current_jst()
    return current_time.year


if __name__ == '__main__':
    current = get_current_jst()
    print(type(current.year))