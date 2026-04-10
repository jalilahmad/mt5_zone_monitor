"""Utility to load visible symbols from MetaTrader 5."""

import MetaTrader5 as mt5


def get_watchlist_symbols():
    """Return the list of visible symbols from the MT5 terminal."""

    symbols = mt5.symbols_get()
    symbol_names = []

    for s in symbols:
        if s.visible:
            symbol_names.append(s.name)

    return symbol_names
