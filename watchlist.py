"""Utility to load visible symbols from MetaTrader 5."""

import MetaTrader5 as mt5


def get_watchlist_symbols():
    """Return the list of visible symbols from the MT5 terminal."""

    symbols = mt5.symbols_get()
    if symbols is None:
        return []

    visible_names = [s.name for s in symbols if getattr(s, "visible", False)]
    if visible_names:
        return visible_names

    # Fallback: return all available symbols when no visible symbols are found
    return [s.name for s in symbols if getattr(s, "name", None) is not None]
