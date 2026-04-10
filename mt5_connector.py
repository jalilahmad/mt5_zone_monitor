"""MetaTrader 5 connection management utilities."""

import MetaTrader5 as mt5
import sys


def connect_mt5():
    """Initialize the MetaTrader 5 connection and verify the account.

    If initialization or login verification fails, the process exits with a
    diagnostic message so the Streamlit app does not continue in a bad state.
    """

    if not mt5.initialize():
        print("MT5 initialize failed")
        print(mt5.last_error())
        sys.exit()

    account_info = mt5.account_info()

    if account_info is None:
        print("Not logged in to MT5")
        sys.exit()

    print("Connected to MT5")
    print("Account:", account_info.login)


def shutdown_mt5():
    """Safely shutdown the MetaTrader 5 connection."""
    mt5.shutdown()
