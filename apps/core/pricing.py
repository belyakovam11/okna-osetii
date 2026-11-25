from decimal import Decimal, ROUND_HALF_UP


def calculate_window_prices(price_per_sqm, width, height, quantity):
    area = Decimal(width * height) / Decimal("1000000")
    unit_price = (area * price_per_sqm).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    total_price = (unit_price * quantity).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    return area, unit_price, total_price
