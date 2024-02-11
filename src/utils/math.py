from decimal import Decimal, ROUND_HALF_UP


def division_and_round(value1: int, value2: int) -> Decimal:
    return Decimal(str(value1 / value2)).quantize(Decimal('0.001'), ROUND_HALF_UP)
