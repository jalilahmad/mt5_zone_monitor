"""Price and zone utilities for MetaTrader 5 symbols."""

import MetaTrader5 as mt5
import config


def get_symbol_price(symbol):
    """Return the latest bid price for a symbol from MT5."""

    tick = mt5.symbol_info_tick(symbol)

    if tick is None:
        return None

    return tick.bid


def get_pip_size(symbol):
    """Return the pip size for a symbol based on its digit precision."""

    info = mt5.symbol_info(symbol)

    if info is None or info.digits is None:
        return 0.0001

    digits = info.digits

    if digits in (3, 5):
        return 0.0001

    if digits in (2, 4):
        return 0.01

    return 0.0001


def get_symbol_digits(symbol):
    """Return the number of decimal digits for the given symbol."""

    info = mt5.symbol_info(symbol)

    if info is None or info.digits is None:
        return 5

    return info.digits


def format_price(symbol, price):
    """Format numeric price output using the symbol's precision."""

    digits = get_symbol_digits(symbol)
    return f"{price:.{digits}f}"


def format_zone(symbol, low, high):
    """Return a human-readable price zone range string."""

    return (
        f"{format_price(symbol, low)}"
        f" - {format_price(symbol, high)}"
    )


def is_price_near_zone(symbol, price, level):
    """Return True when the current price is within alert distance of a zone level."""

    pip = get_pip_size(symbol)

    distance = abs(price - level)
    max_distance = pip * config.ALERT_DISTANCE_PIPS

    return distance <= max_distance
