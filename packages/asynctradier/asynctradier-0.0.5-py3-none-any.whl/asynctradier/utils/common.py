import re


def build_option_symbol(
    symbol: str, expiration_date: str, strike: float, option_type: str
) -> str:
    return f"{symbol.upper()}{expiration_date.replace('-', '')[2:]}{option_type.upper()}{str(int(strike * 1000)).zfill(8)}"


def is_valid_expiration_date(expiration: str) -> bool:
    # valid exp date is YYYY-MM-DD
    return bool(re.match(r"\d{4}-\d{2}-\d{2}", expiration))
